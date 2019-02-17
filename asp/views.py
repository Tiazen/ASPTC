import os
import random

from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_for_filename

from ascpt.settings import MEDIA_ROOT
from asp import themes
from asp.models import Users, tasks, Solution
from asp.myforms import registForm, loginForm, addtaskForm, uploadForm
from asp.testSystem import runtests


def checkAuth(request):
    try:
        if request.session['name'] is not None and request.session['surname'] is not None and \
                request.session['role'] is not None:
            return True
        else:
            return False
    except KeyError:
        return False


def isAdmin(request):
    if request.session['role'] == 'adm':
        return True
    else:
        return False


def index(request):
    if checkAuth(request) and request.session['role'] == 'adm':
        context = {
            'name': request.session['name'],
            'surname': request.session['surname']
        }
        return render(request, 'teacher.html', context)
    elif checkAuth(request) and request.session['role'] == 'student':
        context = {
            'name': request.session['name'],
            'surname': request.session['surname'],
            'themes': themes.getThemes()
        }
        return render(request, 'student.html', context)
    else:
        return HttpResponseRedirect('/login')


def createTaskList(name=None):
    nl = []
    if name is None or name == '':
        all = tasks.objects.all()
        resp = ''
        for i in all:
            resp += '<div class="task"><h3>Название: ' \
                    + i.taskname + '</h3>' + '<p>{} <a href="/edittask?taskid={}" style="float: right; ' \
                                             'position: relative; top: -16px;"><img src="./static/asp/images/controll.png" style=" width: 32px;' \
                                             ' height: 32px; margin-bottom: 50%;"></a></p>'.format(i.taskdesc,
                                                                                                   i.id) + '</div>'
        return resp
    else:
        all = tasks.objects.all()
        for i in all:
            if i.taskname[:len(name)] == name:
                nl.append(i)
        resp = ''
        for i in nl:
            resp += '<div class="task"><h3>Название: ' \
                    + i.taskname + '</h3>' + '<p>{} <a href="/edittask?taskid={}" style="float: right; ' \
                                             'position: relative; top: -16px;"><img src="./static/asp/images/controll.png" style=" width: 32px;' \
                                             ' height: 32px; margin-bottom: 50%;"></a></p>'.format(i.taskdesc,
                                                                                                   i.id) + '</div>'
        return resp


def searchlist(request):
    if request.method == "POST":
        name = request.POST['name']
        resp = createTaskList(name)
        return HttpResponse(resp)
    else:
        return HttpResponseRedirect('/')


def gettasklist(request):
    resp = createTaskList()
    return HttpResponse(resp)


def getclasslist(request):
    if isAdmin(request):
        degree = request.POST['degree']
        letter = request.POST['letter']
        all = Users.objects.filter(degree=degree, letter=letter)
        pupil_list = []
        if len(all) != 0:
            for i in range(len(all)):
                pupil_list.append((i + 1, all[i]))
            resp = render(request, 'generate_table.html', {'all': pupil_list})
            return HttpResponse(resp)
        else:
            return HttpResponse('Nothing')
    else:
        return HttpResponseRedirect('/')


def stat(request):
    if isAdmin(request):
        user = Users.objects.get(id=request.GET.get('id'))
        solutions = Solution.objects.all().filter(user=user)
        content = []
        unique_tasks = set()
        for i in solutions:
            if not i.task in unique_tasks:
                content.append((i.task, Solution.objects.all().filter(user=user).filter(task=i.task)))
                unique_tasks.add(i.task)
            else:
                pass

        return render(request, 'student_solution.html', {'items': content, 'name': request.session['name'],
                                                         'surname': request.session['surname']})
    else:
        return HttpResponseRedirect('/')

def getcode(request):
    solution = Solution.objects.get(id=request.POST['solution'])
    solution_path = '{}\{}\{}'.format(MEDIA_ROOT, solution.user.login,
                                          solution.file.name[:solution.file.name.find('.')] + '_{}'.format(request.POST['solution'])
                                          + solution.file.name[solution.file.name.find('.'):])

    with open(solution_path) as file:
        solution_code = file.read()
    lexer_for_code = get_lexer_for_filename(solution.file.name)

    return HttpResponse(highlight(solution_code, lexer_for_code, HtmlFormatter()))

def gettests(request):
    solution = Solution.objects.get(id=request.POST['solution'])
    user_tests = list(solution.tests[1:-1].replace(' ', '').split(','))
    tests = []
    for i in range(len(user_tests)):
        a = True
        if user_tests[i] is '0': a = False
        tests.append((i, a))
    return render(request, 'generate_tests_table.html', {'tests': tests})

def registuser(request):
    if request.method == 'POST':
        f = registForm(request.POST)
        login = f.data['login']
        password = make_password(password=f.data['passw'], hasher='md5')
        name = f.data['name']
        surname = f.data['surname']
        degree = f.data['degree']
        letter = f.data['letter']

        record = Users(login=login, password=password, name=name, surname=surname,
                       letter=letter, degree=degree)

        try:
            record.save()
            return HttpResponseRedirect('/')
        except IntegrityError:
            return render(request, 'registration.html', {'error': "Такой пользователь уже существует.", 'form': f})
    else:
        form = registForm()
        return render(request, 'registration.html', {'form': form})


def login(request):
    if request.method == "POST":
        try:
            m = Users.objects.get(login=request.POST['login'])
            if check_password(request.POST['password'], m.password):
                request.session['name'] = m.name
                request.session['surname'] = m.surname
                request.session['role'] = m.role
                request.session['uid'] = m.id
                return HttpResponseRedirect('/')
            else:
                form = loginForm()
                return render(request, 'login_page.html', {'form': form, 'error': True})
        except models.ObjectDoesNotExist:
            form = loginForm()
            return render(request, 'login_page.html', {'form': form, 'error': True})

    else:
        if checkAuth(request):
            return HttpResponseRedirect('/')
        else:
            form = loginForm()
            return render(request, 'login_page.html', {'form': form})


def logout(request):
    if checkAuth(request):
        request.session['name'] = None
        request.session['surname'] = None

    return HttpResponseRedirect('/login')


def addtask(request):
    if isAdmin(request):
        if request.method == 'POST':
            s = request.POST
            recordTask = tasks(taskname=s['taskname'], taskdesc=s['taskdesc'], inputs=s['inputs'], outputs=s['outs'],
                               category=s['category'], testin=(s['inputs'].split(','))[0],
                               testout=(s['outs'].split(','))[0])
            recordTask.save()

            return HttpResponse('OK')
        else:
            form = addtaskForm()

            return render(request, 'addtask.html', {'form': form, 'addMode': True,
                                                    'categories': themes.getThemes()})
    else:
        return HttpResponseRedirect('/')


def edittask(request):
    if isAdmin(request):
        if request.method == 'POST':
            s = request.POST
            taskname = s['taskname']
            taskdesc = s['taskdesc']
            inputs = s['inputs']
            outputs = s['outputs']
            id = s['id']
            cate = s['category']
            testin = (inputs.split(','))[0]
            testout = (outputs.split(','))[0]

            sel = tasks.objects.get(id=id)
            sel.taskname = taskname
            sel.taskdesc = taskdesc
            sel.inputs = inputs
            sel.outputs = outputs
            sel.category = cate
            sel.testin = testin
            sel.testout = testout
            sel.save()

            return HttpResponse('OK')
        else:
            taskid = request.GET.get('taskid')
            task = tasks.objects.get(id=taskid)
            inputs = (task.inputs).split(',')
            outputs = (task.outputs).split(',')
            actualcat = task.category
            tests = []

            for i in range(len(inputs) - 1):
                tests.append('<div class="test" id={}>'.format(i + 1) +
                             '<label for="#inp{}"> {} </label>'.format(i + 1, i + 1) +
                             '<input type="text" name="inp{}" id="{}" value="{}" class="tinp">'.format(i + 1, i + 1,
                                                                                                       str(inputs[i])) +
                             '<input type="text" name="out{}" id="out{}" value={} class="tout">'.format(i + 1, i + 1,
                                                                                                        str(outputs[
                                                                                                                i])) + '</div>')

            return render(request, 'addtask.html', {'editMode': True, 'id': taskid, 'task': task,
                                                    'tests': tests, 'categories': themes.getThemes(),
                                                    'actualcat': actualcat})
    else:
        return HttpResponseRedirect('/')


def returnsettings(request):
    if request.method == "POST":
        return render(request, 'settings.html', {'themes': themes.getThemes()})
    else:
        return HttpResponseRedirect('/')


def updatethemes(request):
    if request.method == "POST":
        themes.updateThemes(request.POST['data'])
        return HttpResponse('OK')
    else:
        return HttpResponseRedirect('/')


def tasktheme(request):
    id = request.GET.get('id')
    loctheme = themes.getThemes()
    taskftheme = tasks.objects.all().filter(category=loctheme[int(id)]['name'])
    upload = uploadForm()
    solutions = Solution.objects.filter(user=get_cu(request))

    taskAndSol = []  # (task, solution)

    for i in range(len(taskftheme)):
        taskAndSol.append((taskftheme[i], solutions.filter(task=taskftheme[i].id)))

    context = {
        "themename": loctheme[int(id)]['name'],
        "tasks": taskftheme,
        'name': request.session['name'],
        'surname': request.session['surname'],
        'form': upload,
        'solutions': solutions,
        'test': taskAndSol,
        'theme_id': id,
    }
    return render(request, "themepage.html", context)


def saveFile(request):
    if request.method == "POST":
        page = request.POST['theme_id']
        user = get_cu(request)
        task = tasks.objects.get(id=int(request.POST['task_id']))
        record = Solution(status="CH", file=request.FILES['file'], points=0, user=user, task=task)
        record.save()
        file_updolad_handler(request.FILES['file'], user.login, record.id)
        record_task = tasks.objects.get(id=request.POST['task_id'])

        f = request.FILES['file']
        newName = f.name[:f.name.find('.')] + '_{}'.format(record.id) + f.name[f.name.find('.'):]
        runtests(MEDIA_ROOT + '\\' + user.login + '\\' + newName, record_task, record)

        return HttpResponseRedirect('/tasktheme/?id=' + page)


def get_cu(request):
    return Users.objects.get(id=request.session['uid'])


def file_updolad_handler(f, cu, r_id):
    try:
        os.mkdir(MEDIA_ROOT + '\\' + cu)
    except FileExistsError:
        pass

    newName = f.name[:f.name.find('.')] + '_{}'.format(r_id) + f.name[f.name.find('.'):]
    os.replace(src=MEDIA_ROOT + '\\' + f.name, dst=MEDIA_ROOT + '\\' + cu + '\\' + newName)


def deleteTask(request):
    if isAdmin(request):
        id = request.GET.get('id')
        record = tasks.objects.get(id=int(id))
        record.delete()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def profile(request):
    content = get_default_content(request)
    return render(request, 'profile.html', content)

def changepass(request):
    if checkAuth(request):
        if request.method == 'POST':
            content = get_default_content(request)
            if check_password(request.POST['old'], get_cu(request).password):
                if request.POST['new'] == request.POST['rnew']:
                    record = get_cu(request)
                    record.password = make_password(password=request.POST['new'], hasher='md5')
                    record.save()
                    return HttpResponseRedirect('/')
                else:
                    content.update({'error': 'Пароли не совпадают'})
                    return render(request, 'profile.html', content)
            else:
                content.update({'error': 'Неправильный пароль'})
                return render(request, 'profile.html', content)
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def get_default_content(request):
    return {'name': request.session['name'],
            'surname': request.session['surname']
            }

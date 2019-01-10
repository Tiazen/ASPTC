from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
# Create your views here.

from asp import themes
from asp.models import Users, tasks
from asp.myforms import registForm, loginForm, addtaskForm


def checkAuth(request):
    try:
        if request.session['name'] is not None and request.session['surname'] is not None and request.session['role'] is not None:
            return True
        else:
            return False
    except KeyError:
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
    degree = request.POST['degree']
    letter = request.POST['letter']
    all = Users.objects.filter(degree=degree, letter=letter)

    resp = '<table><tr><th>№</th><th>Фамилия</th><th>Имя</th><td>Выполненные задания</td></tr>'
    if len(all) != 0:
        for i in all:
            count = 1
            resp += '<tr><td>{}</td><td>{}</td><td>{}</td><td><a href="stats?id={}">Выполненные задания</a></td><tr>'.format(
                count, i.name, i.surname, i.id)
            count += 1
        resp += '</table>'
        return HttpResponse(resp)
    else:
        return HttpResponse('Nothing')


def stat(request):
    user_id = request.GET.get('id')
    p = Users.objects.get(id=user_id)
    u = p.donetask.all()
    resp = ''
    for i in u:
        resp += str(i.taskname)
    return HttpResponse(resp)


def registuser(request):
    if request.method == 'POST':
        f = registForm(request.POST)

        if f.is_valid():
            login = f.data['login']
            password = f.data['passw']
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
                return render(request, 'registration.html', {'error': True, 'form': f})

    else:
        form = registForm()

    return render(request, 'registration.html', {'form': form})


def login(request):
    if request.method == "POST":
        try:
            m = Users.objects.get(login=request.POST['login'])

            if m.password == request.POST['password']:
                request.session['name'] = m.name
                request.session['surname'] = m.surname
                request.session['role'] = m.role
                return HttpResponseRedirect('/')
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
    if request.method == 'POST':
        print(request.POST)
        s = request.POST
        recordTask = tasks(taskname=s['taskname'], taskdesc=s['taskdesc'], inputs=s['inputs'], outputs=s['outs'],
                           category=s['category'], testin=(s['inputs'].split(','))[0], testout=(s['outs'].split(','))[0])
        recordTask.save()

        return HttpResponse('OK')
    else:
        form = addtaskForm()

        return render(request, 'addtask.html', {'form': form, 'addMode': True,
                                                'categories': themes.getThemes()})


def edittask(request):
    if request.method == 'POST':
        print(request.POST)
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
            tests.append('<div class="test" id={}>'.format(i+1) +
                         '<label for="#inp{}"> {} </label>'.format(i + 1, i + 1) +
                         '<input type="text" name="inp{}" id="{}" value="{}" class="tinp">'.format(i+1, i+1, str(inputs[i])) +
                         '<input type="text" name="out{}" id="out{}" value={} class="tout">'.format(i+1, i+1,
                                                                                       str(outputs[i])) + '</div>')

        return render(request, 'addtask.html', {'editMode': True, 'id': taskid, 'task': task,
                                                'tests': tests, 'categories': themes.getThemes(),
                                                'actualcat': actualcat})

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
    taskftheme = tasks.objects.filter(category=loctheme[int(id)]['name'])
    print(taskftheme)
    context = {
        "themename": loctheme[int(id)]['name'],
        "tasks": taskftheme,
        'name': request.session['name'],
        'surname': request.session['surname']
    }
    return render(request, "themepage.html", context)

def saveFile(request):
    if request.method == "POST":
        file = request.FILES
        print(file)
        return HttpResponse(file)
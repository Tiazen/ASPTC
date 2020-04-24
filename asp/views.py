import os
from threading import Thread

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_for_filename

from ascpt.settings import MEDIA_ROOT
from asp.auth import check_auth, is_admin, get_cu, get_default_content
from asp.models import Users, tasks, Solution, Compiler, Theme
from asp.myforms import addtaskForm, uploadForm
from asp.testSystem import runtests


def index(request):
    if check_auth(request) and request.session['role'] == 'adm':
        context = get_default_content(request)
        return render(request, 'teacher.html', context)
    elif check_auth(request) and request.session['role'] == 'student':
        context = {
            'name': request.session['name'],
            'surname': request.session['surname'],
            'themes': Theme.objects.all()
        }
        return render(request, 'student.html', context)
    else:
        return HttpResponseRedirect('/login')


def create_task_list(request, name=None):
    if name is None or name == '':
        all_tasks = tasks.objects.all()
        return render(request, "tasklist.html", {"tasks": all_tasks})
    else:
        all_tasks = tasks.objects.filter(taskname__startswith=name)
        return render(request, "tasklist.html", {"tasks": all_tasks})


def searchlist(request):
    if request.method == "POST":
        name = request.POST['name']
        resp = create_task_list(request, name)
        return HttpResponse(resp)
    else:
        return HttpResponseRedirect('/')


def get_task_list(request):
    resp = create_task_list(request)
    return HttpResponse(resp)


def get_class_list(request):
    if is_admin(request):
        degree = request.POST['degree']
        letter = request.POST['letter']
        all_users = Users.objects.filter(degree=degree, letter=letter)
        pupil_list = []
        if len(all_users) != 0:
            for i in range(len(all_users)):
                pupil_list.append((i + 1, all_users[i]))
            resp = render(request, 'generate_table.html', {'all': pupil_list})
            return HttpResponse(resp)
        else:
            return HttpResponse('Nothing')
    else:
        return HttpResponseRedirect('/')


def stat(request):
    if is_admin(request):
        user = Users.objects.get(id=request.GET.get('id'))
        solutions = Solution.objects.filter(user=user)
        content = []
        unique_tasks = set()
        for i in solutions:
            if not i.task in unique_tasks:
                content.append((i.task, Solution.objects.all().filter(user=user).filter(task=i.task)))
                unique_tasks.add(i.task)
            else:
                pass
        return render(request, 'student_solution.html', {'items': content, 'name': request.session['name'],
                                                         'surname': request.session['surname'], "len": len(content)})
    else:
        return HttpResponseRedirect('/')


def getcode(request):
    solution = Solution.objects.get(id=request.POST['solution'])
    solution_path = '{}/{}/{}'.format(MEDIA_ROOT, solution.user.login,
                                      solution.file.name[:solution.file.name.find('.')] + '_{}'.format(
                                          request.POST['solution'])
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
        if user_tests[i] is '0':
            a = False
        tests.append((i, a))
    return render(request, 'generate_tests_table.html', {'tests': tests})


def addtask(request):
    if is_admin(request):
        if request.method == 'POST':
            s = request.POST
            record_task = tasks(taskname=s['taskname'], taskdesc=s['taskdesc'], inputs=s['inputs'], outputs=s['outs'],
                                category=s['category'], testin=(s['inputs'].split(','))[0].replace('\\n', '<br>'),
                                testout=(s['outs'].split(','))[0].replace('\\n', '<br>'))
            record_task.save()

            return HttpResponse('OK')
        else:
            form = addtaskForm()

            return render(request, 'addtask.html', {'form': form,
                                                    'categories': Theme.objects.all()})
    else:
        return HttpResponseRedirect('/')


def edittask(request):
    if is_admin(request):
        if request.method == 'POST':
            s = request.POST
            taskname = s['taskname']
            taskdesc = s['taskdesc']
            inputs = s['inputs']
            outputs = s['outputs']
            task_id = s['id']
            cate = s['category']
            testin = bytes((inputs.split(','))[0], 'utf-8').replace(b'\n', bytes('<br>', 'utf-8')).decode('utf-8')
            testout = bytes((outputs.split(','))[0], 'utf-8').replace(b'\n', bytes('<br>', 'utf-8')).decode('utf-8')

            sel = tasks.objects.get(id=task_id)
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
            task_id = request.GET.get('taskid')
            task = tasks.objects.get(id=task_id)
            inputs = task.inputs.split(',')
            outputs = task.outputs.split(',')
            actual_category = task.category
            tests = []

            for i in range(len(inputs) - 1):
                tests.append('''
                <div id="test{}" class="test" style="margin-bottom: 7px;">
                        <div class="row">
                            <div class="col-1"><label for="#inp{}">{}</label></div>
                            <div class="col-5">
                                <textarea type="text" name="inp{}" id="in{}" class="tinp form-control" required
                                        oninput="change('in{}', 'testin')" >{}</textarea>
                             </div>
                            <div class="col-5">
                                <textarea type="text" name="out{}" id="out{}" class="tout form-control" required
                                oninput="change('out{}', 'testout')" >{}</textarea>
                            </div>
                        </div>
                    </div>
                '''.format(i + 1, i + 1, i + 1, i + 1, i + 1, i + 1, str(inputs[i]), i + 1, i + 1, i + 1,
                           str(outputs[i])))

            return render(request, 'edit.html', {'id': task_id, 'task': task,
                                                 'tests': tests, 'categories': Theme.objects.all(),
                                                 'actualcat': actual_category, 'testin': task.testin,
                                                 'testout': task.testout})
    else:
        return HttpResponseRedirect('/')


def returnsettings(request):
    return render(request, 'settings.html', {'themes': Theme.objects.all(),
                                                 'compilers': Compiler.objects.all()})


def updatethemes(request):
    if request.method == "POST":
        print(request.POST)
        if request.POST['data'] != '' and request.POST['data'] is not None:
            theme = Theme(theme=request.POST['data'])
            theme.save()
        if request.POST.get('delete', '') != '':
            theme = Theme.objects.get(id=request.POST['delete'])
            theme.delete()

        return redirect('/settings/')
    else:
        return redirect('/')


def addcompiler(request):
    if request.method == 'POST':
        compiler_name = request.POST['name']
        compilation_need = request.POST.get('compilationNeed')
        path = request.POST['path'].replace('\\', '/')
        if compilation_need == 'on':
            compilation_need = True
        else:
            compilation_need = False
        options = request.POST.get('options')
        exetentions = request.POST.get('extentions')
        record = Compiler(name=compiler_name, needCompilation=compilation_need,
                          path=path, params=options, extention=exetentions)
        record.save()

        return HttpResponseRedirect('/')
    else:
        return render(request, 'addcompiler.html')


def tasktheme(request):
    theme_id = request.GET.get('id')
    theme = Theme.objects.get(id=theme_id)
    tasks_for_theme = tasks.objects.all().filter(category=theme.theme)
    upload = uploadForm()
    solutions = Solution.objects.filter(user=get_cu(request))

    task_and_sol = []  # (task, solution)

    for i in range(len(tasks_for_theme)):
        task_and_sol.append((tasks_for_theme[i], solutions.filter(task=tasks_for_theme[i].id)))

    context = {
        "themename": theme.theme,
        "tasks": tasks_for_theme,
        'name': request.session['name'],
        'surname': request.session['surname'],
        'form': upload,
        'solutions': solutions,
        'test': task_and_sol,
        'theme_id': theme_id,
        'langs': Compiler.objects.all(),
    }
    return render(request, "themepage.html", context)


def save_file(request):
    if request.method == "POST":
        print(request.POST)
        page = request.POST['theme_id']
        user = get_cu(request)
        task = tasks.objects.get(id=int(request.POST['task_id']))
        record = Solution(status="CH", file=request.FILES['file'], points=0, user=user,
                          task=task, lang=lang_detect(request.FILES['file'].name, request.POST['lang']))
        record.save()
        file_upload_handler(request.FILES['file'], user.login, record.id)
        record_task = tasks.objects.get(id=request.POST['task_id'])

        f = request.FILES['file']
        new_name = f.name[:f.name.find('.')] + '_{}'.format(record.id) + f.name[f.name.find('.'):]

        tests_th = Thread(target=runtests, args=(MEDIA_ROOT + '/' + user.login + '/' + new_name, record_task, record,))
        tests_th.start()
        return HttpResponseRedirect('/tasktheme/?id=' + page)


def lang_detect(file, passed):
    try:
        lang = Compiler.objects.get(extention=file[file.rfind('.'):]).name
        return lang
    except models.ObjectDoesNotExist:
        return passed


def file_upload_handler(f, cu, r_id):
    try:
        os.mkdir(MEDIA_ROOT + '/' + cu)
    except FileExistsError:
        pass

    new_name = f.name[:f.name.find('.')] + '_{}'.format(r_id) + f.name[f.name.find('.'):]
    os.replace(src=MEDIA_ROOT + '/' + f.name, dst=MEDIA_ROOT + '/' + cu + '/' + new_name)


def delete_task(request):
    if is_admin(request):
        task_id = request.GET.get('id')
        record = tasks.objects.get(id=int(task_id))
        record.delete()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def profile(request):
    content = get_default_content(request)
    return render(request, 'profile.html', content)


def setup(request):
    if request.method == "POST":
        record = Users(login=request.POST['login'], password=make_password(request.POST['password'], hasher='md5'), name=request.POST['name'],
                       surname=request.POST['surname'], degree=12, letter='SPC', role='adm')
        record.save()
        file = request.FILES['logo']

        with open(MEDIA_ROOT + '/../asp/static/asp/images/logo.png', 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

    return render(request, 'setup_page.html')

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.template.backends import django

from asp.models import Users, tasks
from asp.myforms import registForm, loginForm, addtaskForm


def checkAuth(request):
    if request.session['name'] != None and request.session['surname'] != None:
        return True
    else: return False


def index(request):
    if checkAuth(request):
        context = {
            'name': request.session['name'],
            'surname': request.session['surname']
        }
        return render(request, 'mft.html', context)
    else:
        return HttpResponseRedirect('/login')

def createTaskList():
    all = tasks.objects.all()
    resp = ''

    for i in all:
        resp += '<div class="task"><h3>Название: ' + i.taskname + '</h3>' + '<p>{} <a href="/edittask?taskid={}" style="float: right; ' \
                'position: relative; top: -16px;"><img src="./static/asp/images/controll.png" style=" width: 32px;' \
                 ' height: 32px; margin-bottom: 50%;"></a></p>'.format(i.taskdesc, i.id) + '</div>'
    return resp

def gettasklist(request):
    resp = createTaskList()
    return HttpResponse(resp)


def getclasslist(request):
    print(request.POST)
    degree = request.POST['degree']
    letter = request.POST['letter']
    all = Users.objects.filter(degree=degree, letter=letter)

    resp = '<table><tr><th>№</th><th>Фамилия</th><th>Имя</th></tr>'
    if len(all) != 0:
        for i in all:
            count = 1
            resp += '<tr><td>{}</td><td>{}</td><td>{}</td><tr>'.format(count,i.name, i.surname)
            count += 1
        resp += '</table>'
        return HttpResponse(resp)
    else:
        return HttpResponse('Nothing')


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
        m = Users.objects.get(login=request.POST['login'])

        if m.password == request.POST['password']:
            request.session['name'] = m.name
            request.session['surname'] = m.surname
            return HttpResponseRedirect('/')

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
        s = request.POST
        recordTask = tasks(taskname=s['taskname'], taskdesc=s['taskdesc'], inputs=s['inputs'], outputs=s['outs'])
        recordTask.save()

        return HttpResponse('OK')
    else:
        form = addtaskForm()

        return render(request, 'addtask.html', {'form': form, 'addMode': True})

def edittask(request):
    if request.method == 'POST':
        s = request.POST
        print(s)
        return HttpResponse(str(s))
    else:
        taskid = request.GET.get('taskid')
        task = tasks.objects.get(id=taskid)
        return render(request, 'addtask.html', {'editMode': True, 'task': task})
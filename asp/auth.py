from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError, models
from django.http import HttpResponseRedirect
from django.shortcuts import render

from asp.models import Users
from asp.myforms import registForm, loginForm


# Actually would be better to rewrite in official django scheme of logging in


def is_admin(request):
    if request.session['role'] == 'adm':
        return True
    else:
        return False


def registrate_user(request):
    if request.method == 'POST':
        f = registForm(request.POST)
        user_login = f.data['login']
        password = make_password(password=f.data['passw'], hasher='md5')
        name = f.data['name']
        surname = f.data['surname']
        degree = f.data['degree']
        letter = f.data['letter']

        record = Users(login=user_login, password=password, name=name, surname=surname,
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
        if check_auth(request):
            return HttpResponseRedirect('/')
        else:
            form = loginForm()
            return render(request, 'login_page.html', {'form': form})


def logout(request):
    if check_auth(request):
        request.session['name'] = None
        request.session['surname'] = None

    return HttpResponseRedirect('/login')


def get_cu(request):
    return Users.objects.get(id=request.session['uid'])


def change_password(request):
    if check_auth(request):
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


def check_auth(request):
    try:
        if request.session['name'] is not None and request.session['surname'] is not None and \
                request.session['role'] is not None:
            return True
        else:
            return False
    except KeyError:
        return False


def get_default_content(request):
    return {'name': request.session['name'],
            'surname': request.session['surname']
            }
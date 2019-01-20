from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse
from spendtrackapp.views.utils import *


def index(request):
    context = {
        'user': request.user
    }
    return render(request, 'spendtrackapp/account.html', context)


def login_handler(request):
    if request.method == 'GET':
        context = {
            'next': request.GET.get('next'),
            'user': request.user
        }
        return render(request, 'spendtrackapp/login.html', context)

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    next_page = request.POST.get('next')

    if not user:
        context = {
            'next': next_page,
            'errors': True
        }
        return render(request, 'spendtrackapp/login.html', context)

    next_page = next_page if next_page is not None else settings.LOGIN_REDIRECT_URL
    login(request, user)
    return HttpResponseRedirect(next_page)


def logout_handler(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit_handler(request):
    pass


def delete_handler(request):
    pass


def password_change_handler(request):
    pass


def password_reset_handler(request):
    pass


def password_reset_confirm_handler(request):
    pass

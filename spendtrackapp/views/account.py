from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import reverse
from django.utils.http import urlsafe_base64_decode

from spendtrackapp.forms import UserEditForm, CustomPasswordResetForm, RegisterForm
from spendtrackapp.views.utils import *


@login_required
def index(request):
    context = {
        'page_title': 'My account',
        'user': request.user
    }
    return render(request, 'spendtrackapp/account.html', context)


def register_handler(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {
                'page_title': 'Register',
                'errors': form.errors,
                'old_data': request.POST
            }
            return render(request, 'spendtrackapp/register.html', context)

    return render(request, 'spendtrackapp/register.html', {'page_title': 'Register'})


def login_handler(request):
    if request.method == 'GET':
        context = {
            'page_title': 'Login',
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
            'page_title': 'Login',
            'next': next_page,
            'errors': True
        }
        return render(request, 'spendtrackapp/login.html', context)

    next_page = next_page if next_page is not None else settings.LOGIN_REDIRECT_URL
    login(request, user)
    return HttpResponseRedirect(next_page)


@login_required
def logout_handler(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def edit_handler(request):
    form = UserEditForm(request.POST, instance=request.user)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    form.save()
    return JsonResponse({})


@login_required
def delete_handler(request):
    request.user.delete()
    return JsonResponse({})


@login_required
def password_change_handler(request):
    form = PasswordChangeForm(request.user, request.POST)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    form.save()
    login(request, request.user)
    return JsonResponse({})


def password_reset_handler(request):
    if request.method == 'GET':
        return render(request, "spendtrackapp/reset_password.html", {'page_title': 'Password reset'})

    form = CustomPasswordResetForm(request.POST)
    if form.is_valid():
        form.save(
            subject_template_name='spendtrackapp/email/reset_password_title.txt',
            email_template_name='spendtrackapp/email/reset_password.txt',
            html_email_template_name='spendtrackapp/email/reset_password.html',
            from_email=settings.EMAIL_RESET_PASSWORD_SENDER_NAME,
            use_https=not settings.DEBUG,
            request=request
        )
        if request.is_ajax():
            return JsonResponse({})

        context = {
            'page_title': 'Password reset',
            'email': form.cleaned_data['email']
        }
        return render(request, "spendtrackapp/reset_password_done.html", context)

    if request.is_ajax():
        return JsonResponse(form.errors, status=400)

    context = {
        'page_title': 'Password reset',
        'errors': form.errors['email']
    }
    return render(request, "spendtrackapp/reset_password.html", context)


def password_reset_confirm_handler(request, uidb64, token):
    try:
        user_pk = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=user_pk)
    except (User.DoesNotExist, UnicodeError, ValueError):
        return HttpResponseBadRequest('Invalid token')

    if default_token_generator.check_token(user, token):
        # reset password
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()

        # login and render form
        login(request, user)
        context = {
            'page_title': 'Password reset',
            'old_password': password,
        }
        return render(request, "spendtrackapp/reset_password_confirm.html", context=context)

    return HttpResponseBadRequest('Invalid token')

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render

from account.forms import SignUpForm

def validator(errors):
    res = {}
    for e in errors:
        res[e] = errors[e]
    return res

def register_view(request):
    if request.method == 'POST':
        data = {}
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            data['result'] = True
            return JsonResponse(data)
        else:
            data['result'] = False
            data['message'] = 'Пожалуйста, введите корректные данные и повторите попытку.'
            data['res'] = validator(form.errors)
            return JsonResponse(data)

    return render(request, 'registration/signup.html')

def change_password(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        data = {}
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            data['result'] = True
            data['message'] = 'Вы сменили пароль!'
            return JsonResponse(data)
        else:
            data['result'] = False
            data['message'] = 'Пожалуйста, введите корректные данные и повторите попытку.'
            data['res'] = validator(form.errors)
            return JsonResponse(data)
    return render(request, 'registration/password_change_form.html', {'form': form})
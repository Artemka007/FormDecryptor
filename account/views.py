from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from account.forms import SignUpForm, EditUserForm


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
            return HttpResponseRedirect('/account/login/')
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
            data['message'] = 'Вы успешно сменили пароль!'
            return JsonResponse(data)
        else:
            data['result'] = False
            data['message'] = 'Пожалуйста, введите корректные данные и повторите попытку.'
            data['res'] = validator(form.errors)
            return JsonResponse(data)
    return render(request, 'registration/password_change_form.html', {'form': form})

@login_required
def edit_profile(request):
    form = EditUserForm(instance=request.user)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'result': True, 'message': 'Редактирование профиля завершенно успешно!'})
        return JsonResponse({'result': False, 'message': 'Пожалуйста, введите корректные данные и повторите попытку.', 'res': validator(form.errors)})
    return render(request, 'registration/edit_profile.html', {'form': form})
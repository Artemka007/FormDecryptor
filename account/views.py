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
            data['message'] = 'Вы аутентифицированы! Поздравляем!'
            return JsonResponse(data)
        else:
            data['result'] = False
            data['message'] = 'Пожалуйста, введите корректные данные и повторите попытку.'
            data['res'] = validator(form.errors)
            return JsonResponse(data)

    return render(request, 'registration/signup.html')
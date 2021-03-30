from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from account.forms import SignUpForm

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
            res = {}
            for k in form.errors:
                res[k] = form.errors[k]

            data['result'] = False
            data['message'] = 'Пожалуйста, введите корректные данные и повторите попытку.'
            data['res'] = res
            return JsonResponse(data)

    return render(request, 'registration/signup.html')
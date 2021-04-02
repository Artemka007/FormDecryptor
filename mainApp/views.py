from django.http import HttpResponseRedirect
from django.shortcuts import render

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/decryptor/')
    return HttpResponseRedirect('/account/login/')
def about(request):
    return render(request, 'content/about_project.html')
def contacts(request):
    return render(request, 'content/contacts.html')
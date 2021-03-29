from django.http import HttpResponseRedirect
from django.shortcuts import render

def index(request):
    return HttpResponseRedirect('/decryptor/')
def about(request):
    return render(request, 'content/about_project.html')
def contacts(request):
    return render(request, 'content/contacts.html')
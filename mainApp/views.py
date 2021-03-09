from django.shortcuts import render

def index(request):
    return render(request, 'content/index.html')
def about(request):
    return render(request, 'content/about_project.html')
def contacts(request):
    return render(request, 'content/contacts.html')
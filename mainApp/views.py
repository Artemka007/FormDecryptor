from django.http import HttpResponseRedirect
from django.shortcuts import render

from mainApp.forms import CreateInstructionForm
from mainApp.models import Instruction


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/decryptor/')
    return HttpResponseRedirect('/account/login/')
def about(request):
    instruction = Instruction.objects.get(pk=1)
    return render(request, 'content/about_project.html', {'instruction': instruction})

def create_about(request):
    if request.user.is_superuser:
        form = CreateInstructionForm(instance=Instruction.objects.get(pk=1))
        if request.method == 'POST':
            form = CreateInstructionForm(request.POST, instance=Instruction.objects.get(pk=1))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/instruction/')
            return render(request, 'content/create_instruction.html', {'form': form})
        return render(request, 'content/create_instruction.html', {'form': form})
    return HttpResponseRedirect('/')

def contacts(request):
    return render(request, 'content/contacts.html')
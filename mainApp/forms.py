from ckeditor.widgets import CKEditorWidget
from django import forms

from mainApp.models import Instruction


class CreateInstructionForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget(), label='')
    class Meta:
        model = Instruction
        fields = ['text']
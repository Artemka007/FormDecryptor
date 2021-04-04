from django import forms

from mainApp.models import CSVFile


class CreateCSV(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ['user', 'file']

from django.contrib import admin

from formDecryptor.models import Form
from mainApp.models import CSVFile

admin.site.register(Form)
admin.site.register(CSVFile)
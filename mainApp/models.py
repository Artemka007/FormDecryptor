from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

class ManageFileModel(models.Model):
    image = models.ImageField(upload_to='manage/image/', null=True, blank=True)
    file = models.FileField(upload_to='manage/files/', null=True, blank=True)

class Instruction(models.Model):
    text = RichTextUploadingField()

class CSVFile(models.Model):
    file = models.FileField(upload_to='documents/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_file_full_url(self):
        return '.' + str(self.file.url)

    def get_file_name(self):
        return str(self.file.name)

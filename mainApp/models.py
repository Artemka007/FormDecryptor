from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

class ManageFileModel(models.Model):
    image = models.ImageField(upload_to='manage/image/', null=True, blank=True)
    file = models.FileField(upload_to='manage/files/', null=True, blank=True)

class Instruction(models.Model):
    text = RichTextUploadingField()
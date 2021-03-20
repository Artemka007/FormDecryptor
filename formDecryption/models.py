from django.contrib.auth.models import User
from django.db import models

from formDecryption.manage import compress


class Form(models.Model):
    form = models.ImageField(upload_to='formForDecrypt/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_full_url(self):
        return str(self.form.url)

    # Переопределяем метод сохранения, добавляя специальную функцию compress.
    # Она находится в файле manage.py в этой дирректории
    def save(self, *args, **kwargs):
        n_i = compress(self.form)
        self.form = n_i
        super().save(*args, **kwargs)

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excelFiles/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_file_full_url(self):
        return str(self.file.url)

    
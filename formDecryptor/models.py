from django.contrib.auth.models import User
from django.db import models

from formDecryptor.manage import compress


class Form(models.Model):
    form = models.ImageField(upload_to='formForDecrypt/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_full_url(self):
        return '.' + str(self.form.url)

    def get_file_name(self):
        return str(self.form.name).split('/')[1].split('_')[0] + '.' + str(self.form.name).split('.')[1]

    def get_full_file_name(self):
        return str(self.form.name).split('/')[1]

    # Переопределяем метод сохранения, добавляя специальную функцию compress.
    # Она находится в файле manage.py в этой дирректории
    #def save(self, *args, **kwargs):
    #    n_i = compress(self.form)
    #    self.form = n_i
    #    super().save(*args, **kwargs)
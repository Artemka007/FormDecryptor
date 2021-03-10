# FormDecryptor
#### Чтобы все заработало надо убедиться, что вы в директории с файлом manage.py. Далее в командной строке надо написать 
```python manage.py makemigrations```
#### Далее
```python manage.py migrate```
#### И можно запускать сервер
```python manage.py runserver```
#### Для загрузки файлов на сервер со стороны UI будем использовать [jquery-file-upload](https://github.com/blueimp/jQuery-File-Upload), для множественной загрузки изображений, с серверной стороны [pillow](https://github.com/python-pillow/Pillow), для преобразования форпата .jpg в формат .jpeg.

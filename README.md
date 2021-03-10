# FormDecryptor
#### Необходимо установить:
## Python:
```pip install django```
```pip install pillow```
## JavaScript:
```npm install jquery```
```npm install jquery.iframe-transport```
```npm install blueimp-file-upload```
```npm install jquery.ui.widget```
### Че яваскриптовое - надо добавить в директорию manage, которую надо создать в директории static.

#### Чтобы все заработало надо убедиться, что вы в директории с файлом manage.py. Далее в командной строке надо написать 
```python manage.py makemigrations```
#### Далее
```python manage.py migrate```
#### И можно запускать сервер
```python manage.py runserver```
#### Для взаимодействии UI с REST API будем использовать [jQuery](https://github.com/jquery/jquery)
#### Для множественной загрузки файлов на сервер со стороны UI будем использовать [jquery-file-upload](https://github.com/blueimp/jQuery-File-Upload), с серверной стороны для преобразования формата .jpg в формат .jpeg и уменьшения размера файла - [pillow](https://github.com/python-pillow/Pillow).

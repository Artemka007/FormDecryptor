# FormDecryptor
### Чтобы все заработало надо для начала надо активировать виртуальное окружение:
``` shell
  \venv\scripts\activate.bat
```
### Далее необходимо установить:
#### Python:
``` shell
  pip install django
```
``` shell
  pip install pillow
```
#### JavaScript:
```shell
  npm install jquery
```
``` shell 
  npm install jquery.iframe-transport
```
``` shell 
  npm install blueimp-file-upload
```
``` shell 
  npm install jquery.ui.widget
```
### JavaScript плагины надо перенести в директорию manage, которую надо создать в директории static.

#### Далее надо убедиться, что вы в директории с файлом manage.py. В командной строке надо написать 
```python manage.py makemigrations```
#### Далее
```python manage.py migrate```
#### И можно запускать сервер
```python manage.py runserver```
#### Для взаимодействии UI с REST API будем использовать [jQuery](https://github.com/jquery/jquery)
#### Для множественной загрузки файлов на сервер со стороны UI будем использовать [jquery-file-upload](https://github.com/blueimp/jQuery-File-Upload), с серверной стороны для преобразования формата .jpg в формат .jpeg и уменьшения размера файла - [pillow](https://github.com/python-pillow/Pillow).

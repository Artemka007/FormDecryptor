import json
import os

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from formDecryptor.algoritm import create_csv
from formDecryptor.models import Form
from mainApp.models import CSVFile


def index(request):
    if request.user.is_authenticated:
        return render(request, "formDecryptor/index.html")
    return HttpResponseRedirect('/account/login/')

def upload_files_controller(request):
    # Получаем текущего пользователя.
    u = request.user
    # Получаем массив файлов (правда там только один файл), который приходит из input с name="upl" (сокращенно upload).
    file = request.FILES.getlist('upl')
    # Далее делаем проверку на то, что нет нанов, пустых массивов и прочих не зареганных пользователей.
    if(file is None or file == []):
        # Если c массивом файлов чет не так, то возвращаем ответ со статусом BadRequest.
        return JsonResponse({'result': False, 'message': 'Файлов маловато'}, status=400)

    if(not u.is_authenticated):
        # Если пользователь не залогинен, то возвращаем ответ со статусом Unauthorized.
        return JsonResponse({'result': False, 'message': 'Вы не авторизованны.'})

    # Перебираем массив с одним файлом
    for f in file:

        # И создаем объект модели с этим файлом и с текущим пользователем.
        formModelObject = Form(form=f, user=u)

        # Пытаемся сохранить в бд этот объект.
        try:
            formModelObject.save()

        # Если что-то идет не так возвращаем ответ со статусом BadRequest, и с сообщением ошибки.
        # Это сообщение будет анимированно появляться на экране в специальном контейнере, с помощью jQuery.
        except Exception as e:
            return JsonResponse({'result': False, 'message': e.__str__()}, status=400)
        # Ну и если объект сохранился, то возвращаем ответ со статусом Created.
        # Url нужен для взятия изображения с сервера, с последующей передачи его в нейронку.
        # А pk (сокращение от Primary Key) нужен для следующей функции
        return JsonResponse({
            'result': True,
            'url_redirect': str(formModelObject.form.url),
            'url': '/decryptor/upload/createExcel/',
            'pk': formModelObject.pk,
            'form_size': int(formModelObject.form.size),
            'form_name': str(formModelObject.form.name),
            'message': 'Файл успешно загружен на сервер!'
        }, status=201)

def delete_upload_files_controller(request, pk):
    # pk ставится с помощью jquery, как аттрибут data-id к изображению крестика, при нажатии активируется функция, которая отправляет запрос
    # на урл, к которому прикоеплена эта функция, беря из аттрибута data-id соответственное значение и вставляя его в урл.
    # Далее ищется по этому ключу модель бланка.
    try:
        formModelObject = Form.objects.get(pk=pk)
    except Exception as e:
        return JsonResponse({'result': False, 'message': e.__str__()}, status=400)
    # Дальнейшие действия были описаны выше.
    if not formModelObject:
        return JsonResponse({'result': False}, status=400)
    try:
        formModelObject.delete()
    except Exception as e:
        return JsonResponse({'result': False, 'message': e.__str__()}, status=400)
    # И возвращается ответ, что все прошло нормально.
    return JsonResponse({'result': True, 'message': 'Файл успешно удален!'}, status=200)

def send_file(request):
    files_ids = request.GET.get('ids')
    ids = json.loads(files_ids)

    if ids['length'] < 2:
        return JsonResponse({'result': False, 'message': 'Слишком мало файлов.'})

    result = create_csv(user=request.user, file_list=ids, count=ids['length'])

    if result[0] is None:
        return JsonResponse({'result': False, 'message':  result[1][0]})


    if not request.user.is_authenticated:
        return JsonResponse({'result': False, 'message': 'Пользователь не авторизован.'})
    return JsonResponse({'result': True, 'url': '/decryptor/download/' + str(result[0]), 'errors_array':  result[1]})


def download_excel_file(request, pk):
    excel_file_object = CSVFile.objects.get(pk=pk)

    if not request.user.is_authenticated:
        return JsonResponse({'result': False, 'message': 'Пользователь не авторизован.'})

    fp = open(excel_file_object.get_file_full_url(), "rb")
    response = HttpResponse(fp.read(), content_type='application/vnd.ms-excel')
    fp.close()

    file_name = excel_file_object.get_file_name().split('/')[1]

    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)

    return response
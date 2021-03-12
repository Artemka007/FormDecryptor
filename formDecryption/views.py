from django.http import JsonResponse
from django.shortcuts import render

from formDecryption.models import Form


def index(request):
    return render(request, "formDecryption/index.html")

def upload(request):
    # Пока думаем, как будет выглядеть эта страница, и что на ней должно быть.
    return render(request, 'formDecryption/upload.html')

def upload_files_controller(request):
    # Получаем текущего пользователя.
    u = request.user
    # Получаем массив файлов (правда там только один файл), который приходит из input с name="upl" (сокращенно upload).
    file = request.FILES.getlist('upl')
    # Далее делаем проверку на то, что нет нанов, пустых массивов и прочих не зареганных пользователей.
    if(file is None or file == []):
        # Если c массивом файлов чет не так, то возвращаем ответ со статусом BadRequest.
        return JsonResponse({'result': False}, status=400)

    if(not u.is_authenticated):
        # Если пользователь не зареган, то возвращаем ответ со статусом Unauthorized.
        return JsonResponse({'result': False}, status=403)

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
            return JsonResponse({'result': False, 'error': str(e.__str__())}, status=400)
        # Ну и если объект сохранился, то возвращаем ответ со статусом Created.
        # Url нужен для взятия изображения с сервера, с последующей передачи его в нейронку.
        # А pk (сокращение от Primary Key) нужен для следующей функции
        return JsonResponse(
            {
                'result': True,
                'url_redirect': str(formModelObject.form.url),
                'pk': formModelObject.pk,
                'form_size': int(formModelObject.form.size),
                'form_name': str(formModelObject.form.name)
            }, status=201
        )

def delete_upload_files_controller(request, pk):
    # pk ставится с помощью jquery, как аттрибут data-id к изображению крестика, при нажатии активируется функция, которая отправляет запрос
    # на урл, к которому прикоеплена эта функция, беря из аттрибута data-id соответственное значение и вставляя его в урл.
    # Далее ищется по этому ключу модель бланка.
    formModelObject = Form.objects.get(pk=pk)
    # Дальнейшие действия были описаны выше.
    if not formModelObject:
        return JsonResponse({'result': False}, status=400)
    try:
        formModelObject.delete()
    except Exception as e:
        return JsonResponse({'result': False, 'error': str(e.__str__())}, status=400)
    # И возвращается ответ, что все прошло нормально.
    return JsonResponse({'result': True}, status=204)
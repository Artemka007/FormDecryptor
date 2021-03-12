from io import BytesIO
from PIL import Image
from django.core.files import File


def compress(image):
    # Тут мы используем библиотеку pillow.
    # Сначала открываем изображение
    im = Image.open(image)
    # Далее инициализируем байтовую переменную
    im_io = BytesIO()
    # Сохраняем ее в виде байтов в формате .jpeg и немного сжимаем
    im.save(im_io, 'JPEG', quality=70)
    # Создаем из байтов файл
    new_image = File(im_io, name=image.name)
    # И возвращаем его
    return new_image
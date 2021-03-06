## **Подробнее о работе нашего алгоритма**

**1 ШАГ - Преобразование**

Преобразование из цветного документа в черно-белый.

Это нужно для упрощения ускорения алгоритма распознавания четырехугольных фигур. Наш алгоритм распознает тонкие белые или черные(в зависимости от того какой был документ и в какой был преобразован) рамки квадратов или прямоугольников.

Когда в документе присутствует только 2 цвета, то программе гораздо проще сориентироваться в цветах и плотности пикселей.

Преобразование документа в черно-белый цвет, также повышает точность программы.

**2 ШАГ - Разделение**


Здесь, программа разделяет бланк на 2 части.

Первая часть это личные данные: происходит распознавание класса

Во второй части документа, происходит распознавание ответов.

Такое разделение нужно производить для корректной работы нашей программы.

Необходимы данные имеющие как можно меньше лишней информации. Для наилучшего определения ответов я разделяю документ на две части, также задействовав алгоритм распознавания четырехугольников.

После разделения я получаю 2 части с данными для дальнейшей обработки

**3 ШАГ – Поиск ответов**

После получения 2 объектов с определенными массивами, программа начинает обработку.

Вы видите работу алгоритма **просеивание**.

Первый этап: программа убирает все лишнее и пытается найти фигуры содержащие 4 угла.

*Второй этап: после удачного поиска всех фигур запускается второй этап алгоритма просеивания. Это значит, что все фигуры которые не соответствуют определенным параметрам*, отбрасываются, а подходящие, обрезаются до размера своих контуров и отправляются в следующий алгоритм.

Параметры: одна сторона  должны быть примерно равна другой( допустима погрешность в 5 единиц) Координаты не должны повторятся.

После обрезки запускается алгоритм взвешивания. Алгоритм сравнивает кол-во черных и белых пикселей, и при большем количестве белых возвращается True, таким образом программа считает этот ответ как отмеченный.

**4 ШАГ – запись в таблицу**

Самое интересное это алгоритм распределения ответов.

При распознавании контуров, а в последствии четырехугольных фигур алгоритм не распознает объекты в определенном порядке, а делает все в разброс. С этой проблемой нам помогает справиться самообучающийся алгоритм сортировки координат. Он сравнивает все координаты и отбрасывает артефакты образовавшиеся в ходе распознавания клеток.

Создается модель координат которые могут в дальнейшем быть сравнены с координатами отмеченной клетки. И будет возвращена координата привычная для восприятия.

После сортировки ответов в нужном порядке и в вычисление количества баллов, ответы записываются в файл EXCEL.
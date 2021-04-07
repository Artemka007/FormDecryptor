$(function() {

    // Стили будут готовы позже, будет реализованна загрузка и т. д.
    let ul = $('#upload ul');
    let a = 1

    $('#drop a').click(function() {
        // У инпута стоит display: none, поэтому пользователь нажимает на ссылку, и ссылка активирует нажатие на инпут.
        $(this).parent().find('input').click();
    });
    // Как закинули файл
    $('#upload').fileupload({
        // Куда его можно закинуть
        dropZone: ul,

        // Формат отправки
        dataType: 'json',

        start: function (e, data) {
            let val = parseInt($('[data-action="files_count"]').val()) || undefined
            if(val !== undefined && a >= val) {
                e.preventDefault()
                let array = new Array(1)
                array.push(`Больше ${val} файлов скачивать нельзя.`)
                display_warnings.debug_window(array)
                return false
            }
        },

        // Как загрузка заканчивается, дабавляется изображение и на него вешаются события
        done: function(e, data) {
            let display = "display: flex;",
            file_size = $(window).width() > 850
                ? '<div style="padding: 5px 10px; border-right: rgba(0,0,0,0.4) solid 1px;">' + formatFileSize(data.result.form_size) + '</div>'
                : ''

            if(!data.result.result){
                display_warnings.modal_window(data.result, 'error')
                return false
            }
            else {
                $('' +
                    '<div data-action="send_file" class="upload-image-container" data-pk="' + data.result.pk + '" data-url="' + data.result.url + '">' +
                    '   <div class="container dir_row" style="width: 100%; margin: 5px 10px;">' +
                    '      <div class="progress_c_bar"></div>' +
                    '      <div style="' + display + ' flex-direction: column; justify-content: center;object-fit: cover; width: 45px; height: 45px; margin: -10px 10px;">' +
                    a +
                    '      </div>'+
                    '      <div style="padding: 5px 10px; border-right: rgba(0,0,0,0.4) solid 1px; border-left: rgba(0,0,0,0.4) solid 1px;">' + data.result.form_name.toString().split('/')[1] + '</div>' +
                    file_size +
                    '   </div>' +
                    '   <div data-url="/account/profile/photos/delete/" data-action="del_photo" data-id="' + data.result.pk + '" class="question_about_edit_message_close" style="display: flex; justify-content: flex-end; float:right; width: 100%; ">' +
                    '       <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">' +
                    '           <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>' +
                    '       </svg>' +
                    '   </div>'+
                    '</div>').appendTo(ul);
                ul.scrollTop = ul.scrollHeight

                $('[data-id="' + data.result.pk + '"]').on('click', function() { file_actions.del_file(data.result.pk)} );

                a += 1
                return false
            }
        }

    });

    $(document).on('drop dragover', function(e) {
        e.preventDefault();
    });

    // Функция, которая возвращает размер файла
    function formatFileSize(bytes) {
        if (bytes >= 1000000000) {
            return (bytes / 1000000000).toFixed(2) + ' GB';
        }

        if (bytes >= 1000000) {
            return (bytes / 1000000).toFixed(2) + ' MB';
        }

        return (bytes / 1000).toFixed(2) + ' KB';
    }
});

// я решил выделить все действия связанные с файлами в один объект, названный соответственно file_actions = действия_с_файлами
const file_actions = {
    errors: [],
    // т. к. почти все функции здесь - callback-и, то в них автоматически передается событие (event)

    upload: function (event) {
        // страничку не обновляем, это в данном контексте необходимо, поскольку это препятствует нормальной загрузке файлов.
        // Чтобы не обновлять страничку надо указать функцию event.preventDefault().
        event.preventDefault();
        // далее считываем данные (там находится массив с 1-им файлом) из первого инпута формы и передаем его в специальный объект FormData, для последующей отправки на сервер.
        let v = $('form').get(0), data = new FormData(v);

        // отправляем массив с файлом на сервер
        $.ajax({
            url: $(this).attr('action'),           // этот action находится в аттрибутах объекта, к которуму привязана эта функция, в данном случае к форме.
            type: $(this).attr('method') || 'GET',
            data: data || '',
            cache: false,
            processData: false,
            contentType: false
        })
        return false;
    },

    // отправка файлов на сервер для их последующей обработки осуществляется этой функцией
    send_files: function (event) {
        let files = $('[data-action="send_file"]'),
            keys = files.map(function() { return $(this).attr('data-pk') }),
            rows = $('[data-action="rows"]').val(),
            columns = $('[data-action="columns"]').val(),
            answers = $('[data-action="answers"]').val(),
            words = $('[data-action="words"]').val()


        if(keys.length > 2 && rows && columns && answers && words && parseInt(rows) > 0 && parseInt(columns) > 0){
            loading.loading(true)
            $.ajax({
                url: '/decryptor/send',
                data: {
                    ids:  JSON.stringify(keys),
                    rows: rows,
                    columns: columns,
                    answers: answers,
                    words: words
                },
                traditional: true,
                contentType: "application/json",
                dataType: "json",
            }).done(function (res) {
                if(res.result){
                    loading.end_loading(true)
                    display_warnings.modal_window({ message: 'Все прошло успешно! Файл скачался в дирректорию "Загрузки".' }, 'ok')
                    location.href = res.url
                    display_warnings.debug_window(res.errors_array)
                    file_actions.del_all_files()
                }
                else{
                    display_warnings.modal_window(res.data, 'error')
                }
            })
        }
        else if(!rows || !columns || !answers || !words || parseInt(rows) <= 0 || parseInt(columns) <= 0){
            display_warnings.modal_window({ message: 'Пожалуйста, введите корректно все требуемые данные и повторите попытку.' }, 'error')
            display_warnings.debug_window(['Необходимые данные или не введены или не коректны.'])
        }

        else{
            display_warnings.modal_window({ message: 'Вы не загрузили не одного файла.' }, 'error')
            display_warnings.debug_window(['Ни одного файла не загружено.'])
        }

        return false;
    },

    del_file: function (pk) {
        $.get({
            url: '/decryptor/upload/delete/' + pk
        }).done(function (res) {
            let el = $('[data-pk="' + pk +'"]')
            el.remove()
        })
    },

    del_all_files: function (event) {
        let els = $('.upload-image-container'), ids = els.map(function(){
            return $(this).attr('data-pk')
        })
        for(let i = 0; i < els.length; i++){
            let pk = ids[i]
            file_actions.del_file(pk)
        }
        display_warnings.modal_window({ message: 'Все файлы успешно удалены!' }, 'ok')
        return false;
    }
}

$(function() {
    $('[data-action="upload_photos"]').submit(file_actions.upload)
    $('[data-action="delete_all_photos"]').on('click', file_actions.del_all_files)
    $('[data-action="send_photos"]').on('click', function (event) {
        file_actions.send_files(event)
    })
})
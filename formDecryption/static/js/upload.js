$(function() {

    // Стили будут готовы позже, будет реализованна загрузка и т. д.
    var ul = $('#upload ul');

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

        // Как загрузка заканчивается, дабавляется изображение и на него вешаются события
        done: function(e, data) {
            let display = $(window).width() > 850
                ? "display: flex;"
                : "display: none;",
            file_size = $(window).width() > 850
                ? '<div style="padding: 5px 10px; border-right: rgba(0,0,0,0.4) solid 1px;">' + formatFileSize(data.result.form_size) + '</div>'
                : ''

            if(!data.result.result){
                modal_window(data.result, 'error')
                return false
            }
            else {
                $('' +
                    '<div data-action="send_file" class="upload-image-container" data-pk="' + data.result.pk + '" data-url="' + data.result.url + '">' +
                    '   <div class="container dir_row" style="width: 100%; margin: 5px 10px;">' +
                    '      <div class="progress_c_bar"></div>' +
                    '      <div style="' + display + ' flex-direction: column; justify-content: center;object-fit: cover; width: 45px; height: 45px; margin: -10px 10px;">' +
                    '         <img src="' + data.result.url_redirect + '" alt=""/>' +
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

                $('[data-id="' + data.result.pk + '"]').on('click', function() { file_actions.del_file(data.result.pk)} );

                modal_window(data.result, 'ok')
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
    send_files: function (event, is_test) {
        let files = $('[data-action="send_file"]'), keys = files.map(function() {
            return $(this).attr('data-pk')
        })
        // пока не готов excel работает тестовый вариант

        if(is_test){
            if(files.length === 0){
                modal_window({message: 'Test is done.'}, 'error')
            }
            else{
                console.log(files)
                console.log(keys)
                modal_window({message: 'Test is done.'}, 'ok')
                return false
            }
        }

        if(files.length === 0){
            modal_window({message: 'Test is done.'}, 'error')
        }

        else{
            // перебираем и отправляем на сервер все id файлов
            for(let i = 0; i < files.length; i++){
                $.get({
                    url: $(this).attr('data-url') + keys[i]
                }).done(function (res) {
                    modal_window(res, 'error' ? !res.result : 'ok')
                })
            }
        }
        return false;
    },

    del_file: function (pk) {
        $.get({
            url: '/decryptor/upload/delete/' + pk
        }).done(function (res) {
            modal_window(res, res.result ? 'ok' : 'error')
            let el = $('[data-pk="' + pk +'"]')
            el.remove()
        })
        return false;
    },

    del_all_files: function (event) {
        let els = $('.upload-image-container'), ids = els.map(function(){return $(this).attr('data-pk')})
        for(let i = 0; i < els.length; i++){
            let pk = ids[i]
            file_actions.del_file(pk)
            if(i - 1 === els.length){
                modal_window({message: 'Все файлы успешно удалены!'}, 'ok')
            }
        }
        return false;
    }
}

function modal_window(data, add_class){
    let modal_window = $('[data-action="modal_error_window"]')
    modal_window.addClass(add_class)
    modal_window.animate({'opacity': 1, 'z-index': '9', 'bottom': '200px'}, 600)
    $('[data-action="error_message"]').text(data.message)
    $('[data-action="close_modal_error"]').on('click', function (){
        $('[data-action="modal_error_window"]').animate({'opacity': 0, 'z-index': '-2', 'bottom': '-200px'}, 0, null, function (){
            $('[data-action="error_message"]').text('')
            $('[data-action="modal_error_window"]').removeClass(add_class)
        })
    })
    setTimeout(function () {
        modal_window.removeClass('error')
        modal_window.animate({'opacity': 0, 'z-index': '-2', 'bottom': '-200px'}, 600, null, function (){
            $('[data-action="error_message"]').text('')
            $('[data-action="modal_error_window"]').removeClass(add_class)
        })
    }, 10000)
}

$(function() {
    $('[data-action="upload_photos"]').submit(file_actions.upload)
    $('[data-action="delete_all_photos"]').on('click', file_actions.del_all_files)
    $('[data-action="send_photos"]').on('click', function (event) {
        file_actions.send_files(event, true)
    })
})
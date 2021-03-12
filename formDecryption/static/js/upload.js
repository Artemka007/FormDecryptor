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
        dropZone: $('#drop'),

        // Формат отправки
        dataType: 'json',

        // При старте появляется спинер загрузки и затемняющий контэйнер
        start: function(e, data) {
            $('.spinner').css({'display': 'block', 'z-index': '20'})
            $('.blackout_container').css({'z-index': '10', 'background-color': 'rgba(0,0,0,0.7)'})
        },
        // Как загрузка заканчивается, дабавляется изображение и нв него вешаются события
        done: function(e, data) {
            var proc_container = $('' +
                '<div class="upload-image-container" data-pk="' + data.result.pk + '">' +
                '   <div class="progress_c_bar"></div>' +
                '   <div style="display: flex; flex-direction: column; justify-content: center;object-fit: cover; width: 45px; height: 45px; margin: -5px -10px;">' +
                '      <img src="' + data.result.url_redirect + '" alt=""/>' +
                '   </div>'+
                '   <div style="margin-left: 20px;">' + formatFileSize(data.result.form_size) + '</div>'+
                '   <div style="margin-left: 5px;">' + data.result.form_name + '</div>'+
                '   <div data-url="/account/profile/photos/delete/" data-action="del_photo" data-id="' + data.result.pk + '" class="question_about_edit_message_close" style="display: flex; justify-content: flex-end; float:right; width: 100%; ">\n' +
                '        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">\n' +
                '            <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>\n' +
                '        </svg>\n' +
                '    </div>' +
                '</div>').appendTo(ul);
            proc_container.find('p').text(data.files[0].name)
                .append('<i>' + formatFileSize(data.files[0].size) + '</i>');
            $('.spinner').css({'display': 'none', 'z-index': '0'})
            $('.blackout_container').css({'z-index': '-9', 'background-color': 'rgba(0,0,0,0)'})

            $('[data-action="del_photo"]').click(del_photo);
        }

    });

    $(document).on('drop dragover', function(e) {
        e.preventDefault();
    });

    // Функция, которая возвращает формат файла
    function formatFileSize(bytes) {
        if (typeof bytes !== 'number') {
            return '';
        }

        if (bytes >= 1000000000) {
            return (bytes / 1000000000).toFixed(2) + ' GB';
        }

        if (bytes >= 1000000) {
            return (bytes / 1000000).toFixed(2) + ' MB';
        }

        return (bytes / 1000).toFixed(2) + ' KB';
    }
});

// Функция загрузки файла на сервер
function upload(event) {
    event.preventDefault();
    let v = $('form').get(0)
    debugger
    var data = new FormData(v);

    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: data,
        cache: false,
        processData: false,
        contentType: false
    });
    return false;
}

// Функция удаления загруженного файла на сервер
function del_photo(){
    let t = $(this)
    let pk = t.attr('data-id')
    $.ajax({
        url: '/decryptor/upload/delete/' + pk,
        type: 'GET'
    }).done(function(data){
        let el = $('[data-pk="' + pk +'"]')
        el.css('transform', 'scale(0)')
        el.css('display', 'none')
    })
}
$(function() {
    $('[data-action="upload_photos"]').submit(upload);
})
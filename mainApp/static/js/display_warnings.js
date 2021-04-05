const display_warnings = {
    validator: function(errors, form) {
        for (let e in errors) {
            form.find('input[name=' + e + ']').after('<span class="err">' + errors[e] + '</span>')
            form.find('input[name=' + e + ']').addClass('err')
        }
    },
    modal_window: function (data, add_class){
        $('[data-action="container_modal_error_window"]').append('' +
            '<div class="warning_message_container warning_message" data-action="modal_error_window">' +
            '    <div class="container dir_row" style="justify-content: center; width: 100%;">' +
            '        <div data-action="error_message" class="warning_message" style="background-color: rgba(0,0,0,0)">' +
            '        </div>' +
            '    </div>' +
            '    <div class="close" data-action="close_modal_error">' +
            '        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">' +
            '            <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>' +
            '        </svg>' +
            '    </div>' +
            '</div>')

        $('[data-action="modal_error_window"]').animate({'opacity': 0, 'z-index': '-2', 'bottom': '-200px'}, 0, null, function (){
            $('[data-action="error_message"]').text('')
            $('[data-action="modal_error_window"]').removeClass(add_class)
        })
        let modal_window = $('[data-action="modal_error_window"]')
        modal_window.addClass(add_class)
        modal_window.animate({'opacity': 1, 'z-index': '9', 'bottom': '200px'}, 600)
        $('[data-action="error_message"]').html(data.message)
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
}
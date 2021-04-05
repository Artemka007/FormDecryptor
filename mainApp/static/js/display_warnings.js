const display_warnings = {
    validator: function(errors, form) {
        for (let e in errors) {
            form.find('input[name=' + e + ']').after('<span class="err">' + errors[e] + '</span>')
            form.find('input[name=' + e + ']').addClass('err')
        }
    },
    modal_window: function (data, add_class){
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
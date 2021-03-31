const display_warnings = {
    validator: function(errors, form) {
        for (let e in errors) {
            form.find('input[name=' + e + ']').after('<span class="err">' + errors[e] + '</span>')
            form.find('input[name=' + e + ']').addClass('err')
        }
    },
    modal_window: function (data, add_class){
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
}

const auth = {
    button_text: '',

    auth: function (event) {
        event.preventDefault()
        auth.loading()
        $('[data-action="auth_form"]').ajaxSubmit({
            success: function(data) {
                let form = $('[data-action="auth_form"]')
                form.find('input').removeClass('err')
                form.find('.err').remove()
                if (data.result) {
                    display_warnings.modal_window(data, 'ok')
                    auth.end_loading()
                    location.href = '/account/login/'
                }
                else {
                    display_warnings.modal_window(data, 'error')
                    display_warnings.validator(data.res, form)
                    auth.end_loading()
                }
            },
            dataType: 'json'
        });
    },

    loading: function (){
        let lb = $('[data-action="auth_button"]')
        auth.button_text = lb.text()
        lb.text('')
        lb.html('<svg class="spinner login_spinner" viewBox="0 0 50 50"><circle cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>Loading...')
        lb.prop("disabled", true);
    },

    end_loading: function (){
        let lb = $('[data-action="auth_button"]')
        lb.html('')
        lb.text(auth.button_text)
        lb.prop("disabled", false);
    },


}

$(function (){
    $('[data-action="auth_form"]').on('submit', auth.auth)
})
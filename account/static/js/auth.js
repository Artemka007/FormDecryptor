const auth = {
    button_text: '',

    auth: function(event, form_data_action, props) {
        event.preventDefault()
        loading.loading()
        $('[data-action="' + form_data_action + '"]').ajaxSubmit({
            success: function(data) {
                let form = $('[data-action=' + form_data_action + ']')
                form.find('input').removeClass('err')
                form.find('.err').remove()
                if(data.result){
                    display_warnings.modal_window(data, 'ok')
                }
                else{
                    display_warnings.modal_window(data, 'error')
                    display_warnings.validator(data.res, form)
                }


                if(props && props.is_redirect) {
                    location.href = data.redirect_url
                }

                loading.end_loading()
            },
            dataType: 'json'
        });
    },

    signup: function (event) {
        auth.auth(event, "signup_form", { is_redirect: true })
    },

    change_password: function (event) {
        auth.auth(event, "change_password_form")
    },

    edit_profile: function (event) {
        auth.auth(event, "edit_profile_form")
    }
}

$(function (){
    $('[data-action="signup_form"]').on('submit', auth.signup)
    $('[data-action="change_password_form"]').on('submit', auth.change_password)
    $('[data-action="edit_profile_form"]').on('submit', auth.edit_profile)
})
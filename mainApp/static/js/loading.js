const loading = {
    loading: function (is_send){
        let lb = is_send ? $('[data-action="send_photos"]') : $('[data-action="auth_button"]')
        auth.button_text = lb.text()
        lb.text('')
        lb.html('<svg class="spinner login_spinner" viewBox="0 0 50 50"><circle cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>Loading...')
        lb.prop("disabled", true);
    },

    end_loading: function (is_send){
        let lb = is_send ? $('[data-action="send_photos"]') : $('[data-action="auth_button"]')
        lb.html('')
        lb.text(auth.button_text)
        lb.prop("disabled", false);
    }
}
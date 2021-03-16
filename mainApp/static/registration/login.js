$(function () {
    $('[data-action="login_form"]').on('submit', function (e){
        let lb = $('[data-action="login_button"]')
        lb.text('')
        lb.html('<svg class="spinner" viewBox="0 0 50 50"><circle cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>Loading')
        lb.prop("disabled", true);
    })
})
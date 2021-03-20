
// Function for view load spinner in forms buttons
function LoginLoad(e){
    let lb = $('[data-action="login_button"]')
    lb.text('')
    lb.html('<svg class="spinner login_spinner" viewBox="0 0 50 50"><circle cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>Loading...')
    lb.prop("disabled", true);
}

$(function () {
    $('[data-action="login_form"]').on('submit', LoginLoad)
})
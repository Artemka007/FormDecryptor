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
            $('[data-action="modal_error_window"]').removeClass('ok')
            $('[data-action="modal_error_window"]').removeClass('error')
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
    },

    debug_window: function (array){
        let debug_window = $('[data-action="debug_window"]')
        for(let a = 0; a < array.length; a++){
            debug_window.append('' +
                '<div class="upload-image-container">' +
                '   <div class="container dir_row" style="width: 100%; margin: 5px 10px;">' +
                '       <div style="padding: 5px 10px; border-left: rgba(0,0,0,0.4) solid 1px;">' +
                '           <div style="color: #ee2f2f;">' +
                '               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-excel" viewBox="0 0 16 16">\n' +
                '                   <path d="M5.884 6.68a.5.5 0 1 0-.768.64L7.349 10l-2.233 2.68a.5.5 0 0 0 .768.64L8 10.781l2.116 2.54a.5.5 0 0 0 .768-.641L8.651 10l2.233-2.68a.5.5 0 0 0-.768-.64L8 9.219l-2.116-2.54z"/>\n' +
                '                   <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/>\n' +
                '               </svg>' +
                '           </div>' +
                '       </div>' +
                '       <div style="padding: 5px 10px; border-right: rgba(0,0,0,0.4) solid 1px; border-left: rgba(0,0,0,0.4) solid 1px;">' +
                array[a] +
                '       </div>' +
                '  </div>' +
               '</div>')
        }
    }
}
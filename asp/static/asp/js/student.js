$(document).ready(function(){
    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
    })
});

function showCode(n) {
    $('#tr'+n).toggle()
    $.ajax({
        url: '/getcode/',
        type: 'POST',
        data: 'solution=' + n,
        success: function(resp) {
              $('#code' + n).html(resp)
            }
    });
    }

function showTests(n) {
    $('#tr'+n).toggle()
        $.ajax({
        url: '/gettests/',
        type: 'POST',
        data: 'solution=' + n,
        success: function(resp) {
              $('#code' + n).html(resp)
            }
    });
}

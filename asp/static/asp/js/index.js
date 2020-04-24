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
});


   $("#apply").click(function(event){
      console.log(classVal, letterVal);
      let x = new XMLHttpRequest();
      x.open("POST", "/class/");
      x.send("degree=" + classVal + "&letter=" + letterVal);
      $.ajax({
            url: '/class/',
            type: 'POST',
            data: "degree=" + classVal + "&letter=" + letterVal,
            success: function(response) {
                $('#className').html("<h2>" + classVal + " " + letterVal + "</h2>");
                $('#studentTable').html(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
      });
});

function del(el) {
    $.ajax({
        url: '/updatethemes/',
        type: 'POST',
        data: 'data=&delete=' + el,
        success: function(resp) {
              $('#setcon').html('<h4>Настройки</h4>');
              $('#setcon').append(resp)
            }
        });
}

function savech() {
    var i = document.getElementById('newtheme').value;
    console.log(i)
    $.ajax({
        url: '/updatethemes/',
        type: 'POST',
        data: 'data=' + i,
        success: function(resp) {
              $('#setcon').html('<h4>Настройки</h4>');
              $('#setcon').append(resp)
            }
    });
}

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

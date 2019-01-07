$(document).ready(function(){
    $('#filter').hide();
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
      $('#tasklist').html('');
      $('#setcon').html('');
      $('#filter').hide();
      var classF = document.getElementById("num"); // Получаем наш список
      var classVal = classF.options[classF.selectedIndex].value;
      var letter = document.getElementById("letter");
      var letterVal = letter.options[letter.selectedIndex].value;

      console.log(classVal, letterVal);

      $.ajax({
            url: '/getclasslist/',
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

    $("#tasks").click(function(event){
      $('#filter').show();
      $('#className').html('');
      $('#studentTable').html('');
      $('#setcon').html('');
      $.ajax({
        url: '/gettasklist/',
        type: 'POST',
        success: function(response) {
            $('#tasklist').html(response);
        }
      });
    });

    $("#settings").click(function(event) {
       $('#filter').hide();
       $('#tasklist').html('');
       $('#className').html('');
       $('#studentTable').html('');
       $('#setcon').html('<h4>Настройки</h4>');

       $.ajax({
         url: '/settings/',
         type: 'POST',
         success: function(resp) {
              $('#setcon').append(resp)
            }
        });
    });
});

function del(el) {
    $(el).remove();
}

function savech() {
    var i = $('.category');
    var res = ''
    for (var j=0; j < i.length; ++j) {
        res += $(i[j]).text()
        if (j != i.length-1) {
            res += ','
        }
    }
    $.ajax({
        url: '/updatethemes/',
        type: 'POST',
        data: 'data=' + res
    });
}

function addtheme() {
    let count = $('.category').length
    if ($('#newtheme').val() != '') {
    $('#spfthemes').append('<div class="row" style="max-width: 30%;  background-color: #fff; margin-bottom: 10px;' +
    'padding: 6px; border-radius: 4px;border: 1px solid #ddd; margin-left: 1px;" id="r' + count + '"><div class="col">' +
    '<h5 class="category">' + $('#newtheme').val() + '</h5></div><div class="col"><button type="button" class="close" aria-label="Close"' +
     'onclick="del(\'#r' + count + '\')"><span aria-hidden="true">&times;</span></button></div></div>');
     $('#newtheme').val('')
     $('#newtheme').css('border', '1px solid #ced4da')
     }
     else {
        $('#newtheme').css('border', '1px solid red')
     }
}
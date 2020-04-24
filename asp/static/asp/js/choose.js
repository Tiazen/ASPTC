var count = $('.test').length + 1
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


    var del = ''
    var inp = ''


    var field = ['#id_taskName', '#id_textdescription', '#1', '#out1', 'category']
    function updateInp(){
        count++;
        del = '<a onclick="deleteTest(' + count + ')" style="font-size: 28px; margin-top: -5px;">&times;</a>'
        inp = '<div id="test' + count + '" class="test" style="margin-bottom: 7px;">' +
                    '<div class="row">' +
                        '<div class="col-1"><label for="#inp' + count + '">' + count + '</label></div>' +
                        '<div class="col-5">' +
                            '<textarea type="text" name="inp' + count + '" id="' + count + '" class="tinp form-control" required></textarea>' +
                         '</div>' +
                        '<div class="col-5">' +
                            '<textarea type="text" name="out' + count + '" id="out' + count + '" class="tout form-control" required></textarea>' +
                        '</div>' +
                         del +
                        '</div></div>'
    }

    function check() {
        var f = false

        for (var i=0; i<5; ++i) {
            if ($(field[i]).val() == '') {
                $(field[i]).css("border", "1px solid red")
                f = true;
            }
            if ($(field[i]).val() != '') {
                $(field[i]).css('border', '2px solid #ddd')
            }
        }
        if (f) {
            return false;
        }
        else {
        return true;
        }
    }

    $('#add').click(function(event) {
        updateInp();
        $('#vars').append(inp);
    });

     $('#send').click(function(event) {
        var inpVars = ''
        var outVars = ''
        var taskname = $("#id_taskname").val();
        var taskDesc = $("#id_taskdescription").val();
        var category = $('#category').val()

        var allinp = $('.tinp')
        var allout = $('.tout')

        for(var i=0; i < count; ++i) {
            if ($(allinp[i]).val() !== undefined && $(allout[i]).val() !== undefined) {
                console.log('i')
                inpVars += $(allinp[i]).val() + ','
                outVars += $(allout[i]).val() + ','
            }
        }

        if (check()) {
        $.ajax({
            url: '/addtask/',
            type: 'POST',
            data: 'taskname=' + taskname + '&taskdesc=' + taskDesc + '&inputs=' + inpVars + '&outs=' + outVars + '&category=' + category,
            success: function(msg){
                window.location.replace('/');
            }
        });
        }
        else {

        }
    });
    $('#edit').click(function(event) {
        var inpVars = ''
        var outVars = ''
        var taskname = $("#id_taskname").val();
        var taskDesc = $("#id_taskdescription").val();
        var id = $("#id").val();
        var category = $('#category').val()

        var allinp = $('.tinp')
        var allout = $('.tout')

        for(var i=0; i < count; ++i) {
            if ($(allinp[i]).val() !== undefined && $(allout[i]).val() !== undefined) {
                console.log('i')
                inpVars += $(allinp[i]).val() + ','
                outVars += $(allout[i]).val() + ','
            }
        }

        $.ajax({
            url: '/edittask/',
            type: 'POST',
            data: 'id=' + id + '&taskname=' + taskname + '&taskdesc=' + taskDesc + '&inputs=' + inpVars + '&outputs=' + outVars + '&category=' + category,
            success: function(){
                window.location.replace('/')
            }
        });
    });
});

function deleteTest(d){
        count -= 1;
       $('#test'+d).remove();
        }



function change(f,a) {
    $('#'+a).html($('#'+f).val())
}


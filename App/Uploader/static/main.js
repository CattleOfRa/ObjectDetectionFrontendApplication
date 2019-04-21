$(document).ready(function() {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var total_number_of_laptops = 0;
    var total_number_of_keyboards = 0;
    var total_number_of_faces = 0;

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        cache: false
    });

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    setInterval(function() {
        $.ajax({
            type: "POST",
            url:"/get_images/",
            data: {
                'unique_id': unique_id
            },
            success: function(data){
                $.each( data['laptop'], function( i, item ) {
                    total_number_of_laptops += 1;
                    $( "<img class=\"output-image\">" ).attr( "src", "/media" + item ).appendTo("#laptop_results");
                    $('#nav-laptop-tab').text("Laptop (" + total_number_of_laptops + ")")
                });

                $.each( data['keyboard'], function( i, item ) {
                    total_number_of_keyboards += 1;
                    $( "<img class=\"output-image\">" ).attr( "src", "/media" + item ).appendTo("#keyboard_results");
                    $('#nav-keyboard-tab').text("Keyboard (" + total_number_of_keyboards + ")")
                });

                $.each( data['face'], function( i, item ) {
                    total_number_of_faces += 1;
                    $( "<img class=\"output-image\">" ).attr( "src", "/media" + item ).appendTo("#face_results");
                    $('#nav-face-tab').text("Face (" + total_number_of_faces + ")")
                });
            }
        })
    }, 2000);
});

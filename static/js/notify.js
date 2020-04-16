$(document).ready(function () {
$(".send, .mybtn").submit(function (e) { 
        e.preventDefault();
        var data1 = $(this).serialize();
        var uri = $(".send").attr('action');
        $.ajax({
            type: "POST",
            url:uri,
            data: data1,
            success: function (data) {
               $(document).html(data);
            }
        });
    });
    });
$(document).ready(function(){

    $(".next").click(function(){
        $.ajax({
            type: "GET",
            url: 'Redwood-Reservation',
            // data: format_date,
            data: {
                "format_date": format_date,
            },
            dataType: "json",
            success: function (data) {
                // any process in data
                alert("successfull")
            },
            failure: function () {
                alert("failure");
            }
        });
    });

});
$(document).ready(function(){
$("#results").hide();
$('#results_found').hide();
$('#results_number').hide();

    function parseResponse(responseObject) {
        var html = '<tbody>';
        for (var json in responseObject) {
            if (responseObject.hasOwnProperty(json)) {
                html += '<tr>';
                for (var key in responseObject[json]) {
                    if (responseObject[json].hasOwnProperty(key)) {
                        html += '<td>' + responseObject[json][key] + '</td>';
                    }
                }
                html += '</tr>';
            }
        }
        html += '</tbody>';
        return html;
    }


    function success(data) {
        console.log("data received: ", data);
        $('#results').find('tbody').remove();
        var json_obj = JSON.parse(data);
        var html = parseResponse(json_obj);
        $(html).appendTo('#results');
        var count = $('#results').find('tr').length -1;
        alert(count)
        $('#results_number').html(count);
        $('#results_found').show();
        $('#results_number').show();
        $('#results').show();
    }


    $('#show_all_work-id').click(function (e) {
        var url = "http://localhost:8081/show_all_work-id";

        $.ajax({
            type: "POST",
            crossDomain: true,
            url: url,
            data: "ALL",
            success: function (data) {
                success(data);
            }

        });
        e.preventDefault();

    });


    $('#show_all_open').click(function (e) {
        var url = "http://localhost:8081/show_all_open";
        $.ajax({
            type: "POST",
            crossDomain: true,
            url: url,
            data: "ALL",
            success: function (data) {
                success(data);
            }

        });
        e.preventDefault();

    });

    $('#show_all_closed').click(function (e) {
        var url = "http://localhost:8081/show_all_closed";
        $.ajax({
            type: "POST",
            crossDomain: true,
            url: url,
            data: "ALL",
            success: function (data) {
                success(data);
            }

        });
        e.preventDefault();

    });

    $('#show_all_verified').click(function (e) {
        var url = "http://localhost:8081/show_all_verified";
        $.ajax({
            type: "POST",
            crossDomain: true,
            url: url,
            data: "ALL",
            success: function (data) {
                success(data);
            }

        });
        e.preventDefault();


    });
});
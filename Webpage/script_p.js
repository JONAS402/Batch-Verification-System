$(document).ready(function(){

$('#results_found').hide();
$('#results_number').hide();
$('#unverified').hide();
//$('#search_items').hide();
$('#verified').hide();
$('.work-id').hide()
//$('#search_batch').hide();


    var start = moment().subtract(29, 'days');
    var end = moment();
    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }

/*
    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
            'This Year': [moment().startOf('year'), moment()],
            'Last Year': [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')]
        }
    }, cb);
  */ 
    cb(start, end);
    

$('.search_terms').hide();
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


    function success(data, table) {
        var selected_table;
        console.log("data received: ", data);
        //$('.table').find('thead').remove();
        $('.table').find('tbody').remove();
        var json_obj = JSON.parse(data);
        var html = parseResponse(json_obj);
        if(table === 'verified') {
        //alert("verified table");
            selected_table = '#verified';
        } else if(table === 'unverified') {
            selected_table = '#unverified';
        } else if (table === 'work-id') {
            selected_table = '#work-id';
        } else {
            selected_table = '#verified';
        }

        $(html).appendTo(selected_table);
        //$(html).appendTo('#table');
        var $table = $(selected_table);
        //$table.floatThead();
        var count = $(selected_table).find('tr').length -1;
        alert(count)
        $('#results_number').html(count);
        $('#results_found').show();
        $('#results_number').show();
        $(selected_table).show();
    }

$('#search_batch_items').click(function(){

$('.search_terms').hide();
$('#search_items').show();
});


$('#work-id_search').click(function(){

  $('.search_terms').hide();
  $('#search_batch').show();
  
});

$('#search_custom').click(function(){
$('.search_terms').hide();
$('#custom_search').show();
});

    $('#show_all_work-id').click(function (e) {
        var url = "http://localhost:8081/show_all_work-id";
        var table = 'work-id';

        $.ajax({
            type: "POST",
            crossDomain: true,
            url: url,
            data: "ALL",
            success: function (data) {
                success(data, table);
            }

        });
        e.preventDefault();

    });

    $('#work-id_search').click(function () {
        $('.search_terms').hide();
        $('#work-id_buttons').show();

    })

    $('#work-id_button').click(function () {
        var id = $('#work-id_input').val();
        alert(id)
    })


    $('#show_all_open').click(function (e) {
        var url = "http://localhost:8081/show_all_open";
        var table = 'unverified';
        $.ajax({
            type: "POST",
            crossDomain: true,
            url: url,
            data: "ALL",
            success: function (data) {
                success(data, table);
            }

        });
        e.preventDefault();

    });

    $('#show_all_closed').click(function (e) {
        var url = "http://localhost:8081/show_all_closed";
        var table = 'unverified';
        $.ajax({
            type: "POST",
            crossDomain: true,
            url: url,
            data: "ALL",
            success: function (data) {
                success(data, table);
            }

        });
        e.preventDefault();

    });

    $('#show_all_verified').click(function (e) {
        var url = "http://localhost:8081/show_all_verified";
        var table = 'verified';
        $.ajax({
            type: "POST",
            crossDomain: true,
            url: url,
            data: "ALL",
            success: function (data) {
                success(data, table);
            }

        });
        e.preventDefault();


    });
});
$(document).ready(function(){
    $('.table').hide();
    $('.search_terms').hide();


    var start = moment().subtract(29, 'days');
    var end = moment();


    $("#radio1").click(function() {
        $("#radio2").prop("checked", false);
        $("#radio3").prop("checked", false);
    });
    $("#radio2").click(function() {
        $("#radio1").prop("checked", false);
        $("#radio3").prop("checked", false);
    });
    $("#radio3").click(function() {
        $("#radio1").prop("checked", false);
        $("#radio2").prop("checked", false);
    });
    $("#radio4").click(function() {
        $("#radio5").prop("checked", false);
    });
    $("#radio5").click(function() {
        $("#radio4").prop("checked", false);
    });


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


    function success_function(data, table) {
        var selected_table;
        //var html = "";
        console.log("data received: ", data);
        $('.table').hide();
        $('.table').find('tbody').remove();
        var json_obj = JSON.parse(data);
        var html = parseResponse(json_obj);
        if(table === 'verified') {
            selected_table = '#verified';
        } else if(table === 'unverified') {
            selected_table = '#unverified';
        } else if (table === 'work-id') {
            selected_table = '#work-id';
        } else {
            selected_table = '#verified';
        }

        $(html).appendTo(selected_table);
        var $table = $(selected_table);
        //$table.floatThead();
        var count = $(selected_table).find('tr').length -1;
        //alert(count);
        $('#results_returned').html(count);
        $('#results_number').html(count);
        $('#results_found').show();
        $('#results_number').show();
        $('.table').hide();
        $(selected_table).show();
        $('.search_terms').hide();
    }


    function ajax_call(url, data, table) {
        $.ajax({
            type: "POST",
            crossDomain: true,
            url: url,
            data: data,
            success: function (data) {
                success_function(data, table);
            }

        });

    }

    $('#search_batch_items').click(function(){
        $('.search_terms, .table').hide();
        $('#search_items').show();
        $('#items_button').click(function (e) {
            var items = $('#items_input').val();
            var operand;
            if ($('input[id=radio1]:checked').length > 0) {
                operand = "Equal to"
            } else if ($('input[id=radio2]:checked').length > 0) {
                operand = "More Than"
            } else if ($('input[id=radio3]:checked').length > 0) {
                operand = "Less Than"
            } else {operand = "Equal to"}
            if(items>0){
                alert("searching for batches "  +operand+ " "+items+ " items.")
                var url = "http://localhost:8081/search_size";
                var table = "verifed";
                var data = {"items":items, "operand": operand};
                ajax_call(url, data, table);
                e.preventDefault();
            }
        });
    });


    $('#search_custom').click(function(){
        $('.search_terms, .table').hide();
        $('#custom_search').show();
        // create custom button click event
    });


    $('#work-id_search').click(function (e) {
        $('.search_terms, .table').hide();
        $('#work-id_buttons').show();
        $('#work-id_button').click(function () {
            var id = $('#work-id_input').val();
            var table = "work-id"
            var url = 'http://localhost:8081/search_workid';
            ajax_call(url, {"Work_ID": id}, table)
            e.preventDefault();
        });
    });


    $('#search_batch_date').click(function(){

        $('.search_terms, .table').hide();
        $('#search_date').show(); // fix report range
        function cb(start, end) {
            $('#reportrange ').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        }


        $('#reportrange span').daterangepicker({
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

        cb(start, end);

    });

    $('#search_batch_number').click(function(){
        $('.search_terms, .table').hide();
        $('#search_batch').show();
        //create batch number button click event
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
                success_function(data, table);
            }

        });
        e.preventDefault();

    });

    $('#show_all_open').click(function (e) {
        var url = "http://localhost:8081/show_all_open";
        var table = 'unverified';
        $.ajax({
            type: "POST",
            crossDomain: true,
            url: url,
            data: "ALL",
            success: function (data) {
                success_function(data, table);
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
                success_function(data, table);
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
                success_function(data, table);
            }
        });
        e.preventDefault();
    });


});
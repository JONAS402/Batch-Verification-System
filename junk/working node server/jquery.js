$(document).ready(function() {

    $('#size_button').click(function(e){
	$('#response').html("searching for size...");
	 var url = "http://localhost:8081/search_size"; // the script where you handle the form input.
    $.ajax({
           type: "POST",
           crossDomain: true,
           url: url,
           data: $("#size_form").serialize(), // serializes the form's elements.
           //data: $('#size_form');
           success: function(data)
           {
               alert(data); // show response from the php script.
	       $('#response').html(data[2]);
	       
           }
         });
    e.preventDefault(); // avoid to execute the actual submit of the form.
    
    });


    $('#batch_button').click(function(e){
	$('#response').html("searching for batch...");
	 var url = "http://localhost:8081/search_batch"; // the script where you handle the form input.
    $.ajax({
           type: "POST",
           crossDomain: true,
           url: url,
           data: $("#batch_form").serialize(), // serializes the form's elements.
           success: function(data)
           {
               alert(data); // show response from the php script.
               $('#response').html(data);
               var html = '<tbody>';
    for (var i = 0, len = data.length; i < len; ++i) {
        html += '<tr>';
        for (var j = 0, rowLen = data[i].length; j < rowLen; ++j ) {
            html += '<td>' + data[i][j] + '</td>';
        }
        html += "</tr>";
    }
    html += '</tbody><tfoot><tr>....</tr></tfoot>';
    $(html).appendTo('#results');
           }
         });
    e.preventDefault(); // avoid to execute the actual submit of the form.
    
    });
    //$('#response').html(data);

});

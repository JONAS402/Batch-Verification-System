$(document).ready(function() {

$('#size_button').click(function(e){
$('#response').html("searching for size...");
var url = "http://localhost:8081/search_size"; // the script where you handle the form input.
$.ajax({
       type: "POST",
       crossDomain: true,
       //dataType:"json",
       url: url,
       data: $("#size_form").serialize(), // serializes the form's elements.
       //data: $('#size_form');
       success: function(data)
       {
           alert(data); // show response from the php script.
       $('#response').html(data);
       }
     });
e.preventDefault(); // avoid to execute the actual submit of the form.

});



});

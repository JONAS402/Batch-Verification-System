var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var cors = require('cors');


// Create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false })

app.use(cors())

app.post('/search_size', urlencodedParser, function(req, res) {
  response = {batch_size: req.body.batch_size};
if(req.body.batch_size){
    var size = req.body.batch_size;
    console.log('looking for batches with ' +size+ ' items');
    response = {"test": "change"}
    res.end(JSON.stringify(response));
  } else {
  console.log('recieved request for 0 items');
  }

  res.end('request recieved...');
  //res.end(JSON.stringify(response));
});

 var server = app.listen(8081, "localhost", function () {
 var host = server.address().address
 var port = server.address().port
 console.log("Server listening at http://%s:%s", host, port)

})

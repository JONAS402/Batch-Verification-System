var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var mysql = require('mysql');
var cors = require('cors');

// Create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false })

var con = mysql.createConnection({
   host: "localhost",
  user: "jonas",
   password: "dennis",
  database: "bvs_db"
});

con.connect(function(err) {
    if (err) {
        console.error('Error:- ' + err.stack);
        return;
    }
 
    console.log('Connected Id:- ' + con.threadId);
});

app.use(cors())

app.use(express.static('public'));
app.get('/index.htm', function (req, res) {
   res.sendFile( __dirname + "/" + "index.htm" );
  console.log("get request")
})

app.post('/process_post', urlencodedParser, function (req, res) {
   // Prepare output in JSON format
   response = {
      first_name:req.body.first_name,
      last_name:req.body.last_name
   };
   console.log(response);
   res.send(JSON.stringify(response));
})
app.post('/search_batch', urlencodedParser, function(req, res) {
  response = { batch_name:req.body.batch_name };
  var batch = req.body.batch_name
  console.log('searching for batch ' + batch);
  //con.connect(function(err) {
  //if (err) throw err;
    var batchnum = 456
    con.query("SELECT * FROM BVS where batch='" +batch+ "'", function (err, result, fields) {
        res.end(JSON.stringify(result));
    if (err) throw err;
    //console.log(result);
    for(var key in result[0]) {
      if (result[0].hasOwnProperty(key)) {
    //console.log(result[0][key]);
        console.log(key + " : " +result[0][key]);
            
  }
    }
    });
    //con.release;
//});
  //res.end(JSON.stringify(response));
});
app.post('/search_size', urlencodedParser, function(req, res) {
  response = {batch_size: req.body.batch_size};
  if(req.body.batch_size){
    var size = req.body.batch_size;
    console.log('looking for batches with ' +size+ ' items');
    res.end(JSON.stringify(response));
  } else {
  console.log('recieved request for 0 items');
  }
  
  //res.end('request recieved...');
  res.end(JSON.stringify(response));
});

var server = app.listen(8081, "localhost", function () {
   var host = server.address().address
   var port = server.address().port
   
   console.log("Server listening at http://%s:%s", host, port)

})

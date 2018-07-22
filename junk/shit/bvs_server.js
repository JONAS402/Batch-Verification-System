var express = require('express');
var mysql = require('mysql');
var bodyParser = require('body-parser');

var app = express();
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


app.post('/search_batch', urlencodedParser, function(req, res) {
    response = {batch: req.body.batch};
    if(req.body.batch){
        var batch = req.body.batch;
        console.log('looking for ' +batch);
        con.query("SELECT * FROM BVS WHERE batch='" +batch+ "' ORDER BY batch", function(err, result, fields){
        for(var key in result[0]) {
            if (result[0].hasOwnProperty(key)) {
            console.log(key + " : " +result[0][key]);    
            }
        }
        });
    
    res.end(JSON.stringify(response));
    }
});

app.post('/search_size', urlencodedParser, function(req, res) {
    response = {batch_size: req.body.batch_size};
    if(req.body.batch_size){
        var size = req.body.batch_size;
        console.log('looking for batches with ' +size+ ' items');
        con.query("SELECT * FROM BVS WHERE size='" +size+"' ORDER BY size", function(err, result, fields){
        for(var key in result[0]) {
        if (result[0].hasOwnProperty(key)) {
        console.log(key + " : " +result[0][key]);    
        }
    }
});
        
    } else {
  console.log('recieved request for 0 items');
    }
  
  //res.end('request recieved...');
});

var server = app.listen(8081, 'localhost', function () {
   var host = server.address().address
   var port = server.address().port
   
   console.log("Batch Verification System Server listening at http://%s:%s", host, port)

})


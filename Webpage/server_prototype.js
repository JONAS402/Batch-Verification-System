var express = require('express');
var bodyParser = require('body-parser');
var cors = require('cors');
var mysql = require('mysql');

var app = express();

// Create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({extended: false});

app.use(cors());

var con = mysql.createConnection({
    host: "localhost",
    user: "jonas",
    password: "dennis",
    database: "bvs_db"
});

function pad(num) {
    var s = num + "";
    while (s.length < 5) s = "0" + s;
    return s;
}

function logResults(result) {
    for (var json in result) {
        console.log("\n");
        if (result.hasOwnProperty(json)) {
            for (var key in result[json]) {
                if (result[json].hasOwnProperty(key)) {
                    console.log(key + " : " + result[json][key]);
                }
            }
        }

    }
}

con.connect(function (err) {
    if (err) {
        console.error('Error:- ' + err.stack);
        return;
    }

    console.log('Connected Id:- ' + con.threadId + "\n");
});

app.post('/show_all_work-id', urlencodedParser, function (req, res) {
    var query = "SELECT * FROM BVS_ITEMS";
    console.log(query);
    con.query(query, function (err, result, fields) {
        res.end(JSON.stringify(result));
        if (err) throw err;
        logResults(result)

    })
});

app.post('/show_all_open', urlencodedParser, function (req, res) {
    var query = "SELECT * FROM BVS_OPEN";
    console.log(query);
    con.query(query, function (err, result, fields) {
        res.end(JSON.stringify(result));
        if (err) throw err;
        logResults(result)

    })
});

app.post('/show_all_closed', urlencodedParser, function (req, res) {
    var query = "SELECT * FROM BVS_CLOSED";
    console.log(query);
    con.query(query, function (err, result, fields) {
        res.end(JSON.stringify(result));
        if (err) throw err;
        logResults(result)

    })
});

app.post('/show_all_verified', urlencodedParser, function (req, res) {
    var query = "SELECT * FROM BVS_VERIFIED";
    console.log(query);
    con.query(query, function (err, result, fields) {
        res.end(JSON.stringify(result));
        if (err) throw err;
        logResults(result)

    })
});

app.post('/search_batch', urlencodedParser, function (req, res) {
    var batch = req.body.batch;
    var query = "SELECT * FROM BVS_VERIFIED WHERE batch='" + pad(batch) + "'";
    console.log(query);
    con.query(query, function (err, result, fields) {
        res.end(JSON.stringify(result));
        if (err) throw err;
        logResults(result)
    });
});


app.post('/search_workid', urlencodedParser, function (req, res) {
    var batch = req.body.batch;
    alert(body.req)
    var query = "SELECT * FROM BVS_WORKID WHERE work_id='" + pad(batch) + "'";
    console.log(query);
    con.query(query, function (err, result, fields) {
        res.end(JSON.stringify(result));
        if (err) throw err;
        logResults(result)
    });
});


app.post('/search_size', urlencodedParser, function (req, res) {
    if (req.body) {
        var size = req.body.items;
        var query = "SELECT * FROM BVS_VERIFIED WHERE items='" + size + "'";
        console.log(query);
        con.query(query, function (err, result, fields) {
            if (err) throw err;
            res.end(JSON.stringify(result));
            logResults(result)
        });
    } else {
        console.log('recieved request for 0 items');
        res.end(JSON.stringify('recieved request for 0 items'));
    }
});


app.post('/search_various', urlencodedParser, function (req, res) {
    if (req.body) {
        var umi, stationary, inserts, postage;
        stationary = req.body.stationary;
        umi = req.body.umi;
        inserts = req.body.inserts;
        postage = req.body.postage;
        console.log("received from page: UMI: %s, INSERTS: %s, STATIONARY: %s, POSTAGE: %s", umi, inserts, stationary, postage);

        // combos
        // umi, inserts, postage, stationary
        // postage, stationary
        // stationary
        // postage
        // umi, inserts
        // umi, inserts, postage
        // umi, inserts, stationary

        var query = "SELECT * FROM BVS";
        if (umi !== '' && postage !== '' && stationary !== '') {  // umi, inserts, postage, stationary
            //console.log("umi !== '' && postage !== '' && stationary !== ''");
            query += " WHERE postage='" + postage + "' AND umi='" + umi + "' AND inserts='" + inserts + "' AND stationary='" + stationary + "'";

        } else if (umi !== '' && postage === '' && stationary === '') {  // postage, stationary
            //console.log("umi !== '' && postage === '' && stationary === ''");
            query += " WHERE umi='" + umi + "' AND inserts='" + inserts + "'";

        } else if (umi === '' && postage !== '' && stationary !== '') {  // umi, inserts
            //console.log("umi === ''  && postage !== '' && stationary !== ''");
            query += " WHERE postage='" + postage + "' AND stationary='" + stationary + "'";

        } else if (umi === '' && postage === '' && stationary !== '') {  // stationary
            //console.log("umi === ''  && postage === '' && stationary !== ''");
            query += " WHERE stationary='" + stationary + "'";

        } else if (umi === '' && postage !== '' && stationary === '') {  // postage
            //console.log("umi === ''  && postage !== '' && stationary === ''");
            query += " WHERE postage='" + postage + "'";

        } else if (umi !== '' && postage === '' && stationary !== '') {  //umi, inserts, stationary
            //console.log("umi !== ''  && postage === '' && stationary !== ''");
            query += " WHERE stationary='" + stationary + "' AND umi='" + umi + "' AND inserts='" + inserts + "'";

        } else if (umi !== '' && postage !== '' && stationary === '') {  // umi, inserts, postage
            //console.log("umi !== ''  && postage !== '' && stationary === ''");
            query += " WHERE postage='" + postage + "' AND umi='" + umi + "' AND inserts='" + inserts + "'";

        } else {
            console.log("unknown query: UMI: %s, INSERTS: %s, STATIONARY: %s, POSTAGE: %s", umi, inserts, stationary, postage)
        }


        console.log(query);
        con.query(query, function (err, result, fields) {
            if (err) throw err;
            res.end(JSON.stringify(result));
            logResults(result);

        });

    } else {
        console.log('received unknown request', req.body);

    }
});

var server = app.listen(8081, "localhost", function () {
    var host = server.address().address;
    var port = server.address().port;
    console.log("Server listening at http://%s:%s...\n", host, port);

});

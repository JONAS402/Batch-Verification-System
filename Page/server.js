var express = require('express');
var bodyParser = require('body-parser');
var cors = require('cors');
var mysql = require('mysql');
var path = require('path');
var app = express();

app.use(cors());

// Create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({extended: false});

var assetsDir = path.join(__dirname + '/assets/')
app.use(express.static(assetsDir));
console.log('[Assets Directory]: ' + assetsDir)


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


var con = mysql.createConnection({
    host: "localhost",
    user: "BVS",
    password: "3Qu1n1t1",
    database: "bvs_db"
});


con.connect(function (err) {
    if (err) {
        console.error('[Error]: ' + err.stack);
        return;
    }

    console.log('[Connected Id]: ' + con.threadId + "\n");
});


app.get('/', function(req, res) {
    console.log('[ROUTE]: /')
    var ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
    console.log('[connected]: ' + ip);
    res.sendFile(path.join(__dirname + '/index.html'));
    console.log('[sent]: index.html')
});


app.post('/show_all_work-id', urlencodedParser, function (req, res) {
    if (req.body) {
        console.log('[ROUTE]: /show_all_work-id')
        var query = "SELECT * FROM BVS_WORKID";
        console.log('[SQL Query]:', query);
        con.query(query, function (err, result, fields) {
            res.end(JSON.stringify(result));
            if (err) throw err;
            logResults(result)
        });
    };
});


app.post('/show_all_open', urlencodedParser, function (req, res) {
    if (req.body) {
        console.log('[ROUTE]: /show_all_open')
        var query = "SELECT * FROM BVS_OPEN";
        console.log('[SQL Query]:', query);
        con.query(query, function (err, result, fields) {
            res.end(JSON.stringify(result));
            if (err) throw err;
            logResults(result)
        });
    };
});


app.post('/show_all_closed', urlencodedParser, function (req, res) {
    if (req.body) {
        console.log('[ROUTE]: /show_all_closed')
        var query = "SELECT * FROM BVS_CLOSED";
        console.log('[SQL Query]:', query);
        con.query(query, function (err, result, fields) {
            res.end(JSON.stringify(result));
            if (err) throw err;
            logResults(result)
        });
    };
});


app.post('/show_all_verified', urlencodedParser, function (req, res) {
    if (req.body) {    
        console.log('[ROUTE]: /show_all_verified')
        var query = "SELECT * FROM BVS_VERIFIED";
        console.log('[SQL Query]:', query);
        con.query(query, function (err, result, fields) {
            res.end(JSON.stringify(result));
            if (err) throw err;
            logResults(result)
        });
    };
});


app.post('/search_batch', urlencodedParser, function (req, res) {
    console.log('[ROUTE]: /search_batch')
    if (req.body) {    
        var batch = req.body.batch;
        var query = "SELECT * FROM BVS_VERIFIED WHERE batch='" + pad(batch) + "'";
        console.log('[SQL Query]:', query);
        con.query(query, function (err, result, fields) {
            res.end(JSON.stringify(result));
            if (err) throw err;
            logResults(result)
        });
    };
});


app.post('/search_workid', urlencodedParser, function (req, res) {
    console.log('[ROUTE]: /search_workid')
    if (req.body) {
        var id = req.body.Work_ID;
        var query = "SELECT * FROM BVS_WORKID WHERE work_id='" + id + "'";
        console.log('[SQL Query]:', query);
        con.query(query, function (err, result, fields) {
            res.end(JSON.stringify(result));
            if (err) throw err;
            logResults(result)
        });
    }
});


app.post('/search_size', urlencodedParser, function (req, res) {
    console.log('[ROUTE]: /search_size')
    // not returning data
    if (req.body) {
        var size = req.body.items;
        var query = "SELECT * FROM BVS_VERIFIED WHERE items='" + size + "'";
        console.log('[SQL Query]:', query);
        con.query(query, function (err, result, fields) {
            if (err) throw err;
            res.end(JSON.stringify(result));
            logResults(result)
        });
    } else {
        console.log('[request]: 0 items');
        res.end(JSON.stringify('recieved request for 0 items'));
    }
});


app.post('/search_custom', urlencodedParser, function (req, res) {        
    if (req.body) {
        var umi, stationary, inserts, postage, search_type;
        umi = req.body.umi;
        stationary = req.body.stationary;
        inserts = req.body.inserts;
        postage = req.body.postage;
        search_type = req.body.search_type;
        console.log("[Query]: from page: UMI: %s, INSERTS: %s, STATIONARY: %s, POSTAGE: %s, SEARCH_TYPE: %s", umi, inserts, stationary, postage, search_type);

        // combos
        // umi, inserts, postage, stationary
        // postage, stationary
        // stationary
        // postage
        // umi, inserts
        // umi, inserts, postage
        // umi, inserts, stationary
        /*
        if search_type == batch then select * from bvs_verified and open and closed and merge to one table before showing
        if search_type == work-id then select* from bvs_workid (as below)
        create a function to minimize code smell and reuse combos if/else sql nightmare
        */

        var query = "SELECT * FROM BVS_WORKID";
        if (umi !== '' && postage !== '' && stationary !== '') {  // umi, inserts, postage, stationary
            query += " WHERE postage='" + postage + "' AND umi='" + umi + "' AND inserts='" + inserts + "' AND stationary='" + stationary + "'";

        } else if (umi !== '' && postage === '' && stationary === '') {  // postage, stationary
            query += " WHERE umi='" + umi + "' AND inserts='" + inserts + "'";

        } else if (umi === '' && postage !== '' && stationary !== '') {  // umi, inserts
            query += " WHERE postage='" + postage + "' AND stationary='" + stationary + "'";

        } else if (umi === '' && postage === '' && stationary !== '') {  // stationary
            query += " WHERE stationary='" + stationary + "'";

        } else if (umi === '' && postage !== '' && stationary === '') {  // postage
            query += " WHERE postage='" + postage + "'";

        } else if (umi !== '' && postage === '' && stationary !== '') {  //umi, inserts, stationary
            query += " WHERE stationary='" + stationary + "' AND umi='" + umi + "' AND inserts='" + inserts + "'";

        } else if (umi !== '' && postage !== '' && stationary === '') {  // umi, inserts, postage
            query += " WHERE postage='" + postage + "' AND umi='" + umi + "' AND inserts='" + inserts + "'";

        } else {
            console.log("[UNKNOWN QUERY]: UMI: %s, INSERTS: %s, STATIONARY: %s, POSTAGE: %s", umi, inserts, stationary, postage)
        }


        console.log('[SQL Query]:', query);
        con.query(query, function (err, result, fields) {
            if (err) throw err;
            res.end(JSON.stringify(result));
            logResults(result);
        });

    } else {
        console.log('[UNKNOWN REQUEST]:', req.body);
    }
});


var server = app.listen(8081, "localhost", function () {
    var host = server.address().address;
    var port = server.address().port;
    console.log("Server listening at http://%s:%s...\n", host, port);
});


var fs = require('fs');
var http = require('http');
var https = require('https');
var privateKey = fs.readFileSync('../softlinkssh/keydecrypted.pem');
var certificate = fs.readFileSync('../softlinkssh/cert.pem');
var credentials = {key:privateKey, cert: certificate};
var express = require('express');
var app = express();
var bodyParser = require('body-parser');

function postJson(req,rsp) {
    console.log(`postJson ${JSON.stringify(req.body)}`);
    rsp.json(req.body);
    rsp.end();
}
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
app.post('/postjson/:id1/:id2',postJson);
app.post('/postjson',postJson);
app.use((req,res) => {
    res.statusCode = 400;
    res.send('error: request handler not recognized\n');
    res.end();
});

var httpServer = http.createServer(app);
var httpsServer = https.createServer(credentials, app);
httpServer.listen(8080);
httpsServer.listen(8443);
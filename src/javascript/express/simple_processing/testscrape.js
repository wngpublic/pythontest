var https = require('https');
var fetch = require('node-fetch');
var jsdom = require('jsdom');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

// start up handle_https.js

function callFetch1() {
    var options = {
        hostname: 'https://localhost:8443',
        path: '/',
        method: 'GET'
    };

    var headers = {
        'Accept-Encoding': 'gzip'
    };


    let url = 'https://localhost:8443';

    var getData = async options => {
        try {
            const rsp = await fetch(url, headers);
            const txt = await rsp.text();
            console.log(txt);
        } catch(e) {
            console.log(e);
        }
    };

    getData(options);
}

function callFetch2() {
    var jsonData = {
        k1: 1,
        k2: 2
    };

    var optionsJson = {
        method: 'POST',
        body: JSON.stringify(jsonData),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip'
        }
    };

    let url = 'https://localhost:8443/postjson/v1/v2?q1=abc&q2=def';
    var val = fetch(url, optionsJson)
        .then(rsp => rsp.json())
        .then(json => console.log(JSON.stringify(json)));
}

callFetch1();
callFetch2();
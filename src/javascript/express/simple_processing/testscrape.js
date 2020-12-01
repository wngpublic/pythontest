let https = require('https');
let fetch = require('node-fetch');
let jsdom = require('jsdom');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

// start up handle_https.js

function callFetch1() {
    let options = {
        hostname: 'https://localhost:8443',
        path: '/',
        method: 'GET'
    };

    let headers = {
        'Accept-Encoding': 'gzip'
    };


    let url = 'https://localhost:8443';

    let getData = async options => {
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
    let jsonData = {
        k1: 1,
        k2: 2
    };

    let optionsJson = {
        method: 'POST',
        body: JSON.stringify(jsonData),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip'
        }
    };

    let url = 'https://localhost:8443/postjson/v1/v2?q1=abc&q2=def';
    let val = fetch(url, optionsJson)
        .then(rsp => rsp.json())
        .then(json => console.log(JSON.stringify(json)));
}

async function callFetch3() {
    let jsonData = {
        k1: 1,
        k2: 2
    };

    let optionsJson = {
        method: 'POST',
        body: JSON.stringify(jsonData),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip'
        }
    };

    let url = 'https://localhost:8443/postjson/v1/v2?q1=abc&q2=def';
    let rsp = await fetch(url, optionsJson);
    let json = await rsp.json();
    console.log(`await: ${JSON.stringify(json)}`);
}


function callFetchMany() {
    let v1 = 1;
    let v2 = 100;
    let numCalls = 10;
    let jsonData = {
        k1: v1,
        k2: v2
    };

    let q = [];
    for(let i = 0; i < numCalls; i++) {
        let optionsJson = {
            method: 'POST',
            body: JSON.stringify(jsonData),
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip'
            }
        };
        jsonData['k1'] = ++v1;
        jsonData['k2'] = ++v2;

        let url = 'https://localhost:8443/postjson';
        let val = fetch(url, optionsJson)
            .then(rsp => rsp.json())
            .then(json => console.log(JSON.stringify(json)));
    }

}

function aCallback(q, i, json) {
    console.log(`${i}: ${JSON.stringify(json)}`);
}

function callFetchManyCallbackQueue() {
    let v1 = 1;
    let v2 = 100;
    let numCalls = 10;
    let jsonData = {
        k1: v1,
        k2: v2
    };

    let q = [];
    for(let i = 0; i < numCalls; i++) {
        let optionsJson = {
            method: 'POST',
            body: JSON.stringify(jsonData),
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip'
            }
        };
        jsonData['k1'] = ++v1;
        jsonData['k2'] = ++v2;

        let url = 'https://localhost:8443/postjson';
        q.push(fetch(url, optionsJson));
    }
    for(let i = 0; i < q.length; i++) {
        q[i].then(rsp => rsp.json())
            .then(json => aCallback(q, i, json));
    }
}

callFetch1();
callFetch2();
callFetch3();
callFetchMany();
callFetchManyCallbackQueue();

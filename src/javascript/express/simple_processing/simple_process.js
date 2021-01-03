const express = require('express');
const bodyParser = require('body-parser');
const assert = require('assert');
const CookieParser = require('cookie-parser');
const axios = require('axios').default;

// warning: multer will not process any form which is not multipart (multipart/form-data).
const multer = require('multer');

// npm run testserver    for nodemon

class Routes {
    constructor(router) {
        this.router = router; // FIXME: this is not used, so implementation is wrong
        this.jsonpayload1 = {
            'k1':'v1',
            'k2':{
                'k2.1':'v2.1',
                'k2.2':'v2.2'
            },
            'k3':['v3.1','v3.2']
        };
        this.jsonpayload1str = JSON.stringify(this.jsonpayload1);
        this.helloworld = 'hello world';
        this.multerUploadDir = multer({
            dest: './dir_output'
        });
        this.multerUploadStorage = multer({
            destination: (req, file, cb) => {
                cb(null, './dir_output')
            },
            filename: (req, file, cb) => {
                cb(null, file.originalname)
            }
        });
    }
    async get_json1(req,res) {
        //let jsonpayload = this.jsonpayload1str; // JSON.parse(this.jsonpayload1str);
        //jsonpayload['k10'] = 10;
        //res.json(jsonpayload);
        let jsonpayload = {
            'k1':'v1',
            'k2':{
                'k2.1':'v2.1',
                'k2.2':'v2.2'
            },
            'k3':['v3.1','v3.2'],
            'k4':req.params.id1,
            'k5':req.params.id2
        };
        //res.send(this.helloworld);
        console.log('get_json1');
        res.json(jsonpayload);
        res.end();
    }
    async post_json1(req,res) {
        // curl -X POST 'localhost:3000/postjson1/v1/v2' -d '{ "k1":"v1" }' -H 'Content-Type: application/json'

        let jsonpayload = {
            'k1':'v1',
            'k2':{
                'k2.1':'v2.1',
                'k2.2':'v2.2'
            },
            'k3':['v3.1','v3.2'],
            'k4':req.params.id1,
            'k5':req.params.id2
        };
        jsonpayload['body'] = req.body;
        let jsonStr = JSON.stringify(jsonpayload);
        res.json(jsonpayload);  // the client needs to stringify the Object to print out.

        res.end();
        console.log(`post_json1 ${jsonStr}`);
    }
    async postJson(req,res) {
        let body = req.body;
        let jsonpayload = {
            data: body['data']
        };
        res.json(jsonpayload);  // the client needs to stringify the Object to print out.
        res.end();
    }
    async postJsonSeries1(req,res) {
        let body = req.body;
        let jsonpayload = {
            data: body['data'],
            series1: body['data']['data']['k1']+1
        };
        //console.log(`postJsonSeries1 body:`, body);
        //console.log(`postJsonSeries1 json:`, jsonpayload);
        const headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json'
        };
        axios.post('http://localhost:3000/postjsonseries2',
            {
                method:'POST',
                headers: headers,
                data: jsonpayload
            },
            {
                timeout: 500
            })
            .then((r) => {
                let rspdata = r.data;
                res.json(rspdata);
            })
            .catch((e) => {
                res.statusCode = 400;
                res.json(e);
            });
    }
    async postJsonSeries2(req,res) {
        let body = req.body;
        let jsonpayload = {
            data: body['data'],
            series2: body['data']['series1']+1
        };
        //console.log(`postJsonSeries2 body:`, body);
        //console.log(`postJsonSeries2 json:`, jsonpayload);
        const headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json'
        };
        axios.post('http://localhost:3000/postjsonseries3',
            {
                method:'POST',
                headers: headers,
                data: jsonpayload
            },
            {
                timeout: 500
            })
            .then((r) => {
                let rspdata = r.data;
                res.json(rspdata);
            })
            .catch((e) => {
                res.statusCode = 400;
                res.json(e);
            });
    }
    async postJsonSeries3(req,res) {
        let body = req.body;
        let jsonpayload = {
            data: body['data'],
            series3: body['data']['series1']+1
        };
        //console.log(`postJsonSeries3 body:`, body);
        //console.log(`postJsonSeries3 json:`, jsonpayload);
        res.json(jsonpayload);
        res.end();
    }
    async postJsonSeriesCombine(req,res) {
        let body = req.body;
        let jsonpayload = {
            data: body['data'],
            series1: body['data']['data']['k1']+1
        };
        //console.log(`postJsonSeriesCombine body:`, body);
        //console.log(`postJsonSeriesCombine json:`, jsonpayload);
        const url = 'http://localhost:3000/post';
        const headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json'
        };
        let promise2 = axios.post('http://localhost:3000/postjsonseries2',
            {
                method:'POST',
                headers: headers,
                data: jsonpayload
            },
            {
                timeout: 500
            })
            .catch((e) => {
                res.statusCode = 400;
                res.json(e);
            });
        let promise3 = axios.post('http://localhost:3000/postjsonseries3',
            {
                method:'POST',
                headers: headers,
                data: jsonpayload
            },
            {
                timeout: 500
            })
            .catch((e) => {
                res.statusCode = 400;
                res.json(e);
            });
        Promise.all([promise2,promise3]).then((results) => {
            let responseData = {
                data: jsonpayload
            };
            let ctr = 0;
            for(let result of results) {
                let data = result.data;
                //console.log(data);
                responseData[`data${ctr++}`] = data;
            }
            res.json(responseData);
        })
    }
    setRsp(res, jsonData) {
        res.json(jsonData);
        res.end();
        console.log(`postJsonWait ${jsonData}`);
    }
    setRspResolve(res, resolve, jsonData) {
        res.json(jsonData);
        res.end();
        console.log(`postJsonWait ${jsonData}`);
        resolve();
    }
    async postJsonWait(req,res) {
        var json = req.body;
        var data = {};
        //console.log(json);
        if('data' in json) {
            data['data'] = json['data'];
        }
        if('timeoutms' in json['data']) {
            //const cbBindSetRsp = this.setRsp.bind(this);
            var waitMs = parseInt(json['data']['timeoutms']);
            //console.log(`wait ${waitMs}`);
            setTimeout((res, data) => {
                res.json(data);
                res.end();
            }, waitMs, res, data);
        } else {
            res.json(data);
            res.end();
        }
        //console.log(`postJsonWait ${JSON.stringify(data)}`);
    }
    async postJsonPromiseWait(req,res) {
        var json = req.body;
        var data = {
            data: null
        }
        if('data' in json) {
            data['data'] = json['data'];
        }
        if('timeoutms' in json['data']) {
            var waitMs = parseInt(json['data']['timeoutms']);
            var promise = new Promise((resolve, reject) => {
                setTimeout((res, data, resolve) => {
                    res.json(data);
                    res.end();
                    resolve();
                }, waitMs, res, data, resolve);
            });
            await promise;
        } else {
            res.json(data);
            res.end();
        }
        console.log(`postJsonPromiseWait ${JSON.stringify(data)}`);
    }
    async postForm(req,res) {
        console.log('req files: ', req.file);
        const data = {
            filename: req.file
        };
        res.json(data);
        res.end();
    }
    async postFormArray(req,res) {
        for(let file of req.files) {
            console.log(file);
        }
        const data = {
            filename: req.files
        };
        res.json(data);
        res.end();
    }
    async postFile(req,res) {
        const data = {
            filename: req.file,
            foo: 'foo'
        };
        res.json(data);
    }
    async postBlob(req,res) {

    }
}

const app = express();
app.use(CookieParser());
const router = express.Router();
const PORT = 3000;
const routes = new Routes(router);


//app.use('/test_routes',routes);
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());

// deprecated
//app.use(express.json());
//app.use(express.urlencoded());

app.get('/getjson1/:id1/:id2',routes.get_json1);
app.post('/postjson1/:id1/:id2',routes.post_json1);
app.post('/postjson',routes.postJson);
app.post('/postjsonseries1',routes.postJsonSeries1);
app.post('/postjsonseries2',routes.postJsonSeries2);
app.post('/postjsonseries3',routes.postJsonSeries3);
app.post('/postjsonseriescombine',routes.postJsonSeriesCombine);
app.post('/postjsonwait',routes.postJsonWait); // accepts json 'timeoutms' and 'data'
app.post('/postjsonpromisewait',routes.postJsonPromiseWait);

app.post('/postform',routes.multerUploadDir.single('file'),routes.postForm); 
// why does it have to be called file for both client and this??

//app.post('/postform',routes.multerUploadStorage.single('file'),routes.postForm);
app.post('/postformarray',routes.multerUploadDir.array('file',5),routes.postFormArray);

app.post('/postfile',routes.multerUploadDir.single('file'),routes.postFile);
app.post('/postblob',routes.postBlob);
app.use((req,res) => {
    res.statusCode = 400;
    res.send('error: request handler not recognized\n');
    res.end();
});

app.listen(PORT, () => console.log(`started app on port ${PORT}`));

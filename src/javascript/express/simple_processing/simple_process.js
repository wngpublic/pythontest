const express = require('express');
const bodyParser = require('body-parser');

// npm run testserver    for nodemon

class SimpleProcess {
    constructor() {
    }

}

class Routes {
    constructor(router) {
        this.router = router;
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
}

const app = express();
const router = express.Router();
const PORT = 3000;
const simpleProcess = new SimpleProcess();
const routes = new Routes(router);

//app.use('/test_routes',routes);
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());

// deprecated
//app.use(express.json());
//app.use(express.urlencoded());

app.get('/getjson1/:id1/:id2',routes.get_json1);


app.post('/postjson1/:id1/:id2',routes.post_json1);

app.use((req,res) => {
    res.statusCode = 400;
    res.send('error: request handler not recognized\n');
    res.end();
});

app.listen(PORT, () => console.log(`started app on port ${PORT}`));

const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const PORT = 3000;

app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
app.post('/postjsonwait',(req,res) => {
    try {
        let json = req.body;
        let data = {};
        if('data' in json) {
            data['data'] = json['data'];
        }
        if('timeoutms' in json['data']) {
            let waitMs = parseInt(json['data']['timeoutms']);
            setTimeout((res, data) => {
                res.json(data);
                res.end();
            }, waitMs, res, data);
        } else {
            res.json(data);
            res.end();
        }
    } catch(e) {
        res.statusCode = 500;
        res.send(e);
        res.end();
        console.log(e);
    }
});
app.use((req,res) => {
    res.statusCode = 400;
    res.send('error: request handler not recognized\n');
    res.end();
});
app.listen(PORT, () => console.log(`started app on port ${PORT}`));

const axios = require('axios').default;
const assert = require('assert');
const PORT = 3030;  // port to docker container. use docker-compose yml for network config
const URL = `http://127.0.0.1:${PORT}`;
const headers = {
    'Accept': 'application/json',
    'Content-Type':'application/json'
};
const toms = 500;

// docker run --network host --name test_client2 test_client
// if --network host not specified, then cannot reach container!

class DockerTest {
    async test1() {
        const url = `${URL}/postjsonwait`;
        const json = {
            timeoutms: toms,
            data: {
                k1:'v1',
                k2:'v2'    
            }
        };
        let t1 = Date.now();
        let flag = false;
        axios.post(
            url,
            {
                method:'POST',
                headers: headers,
                data: json
            },
            {
                timeout: toms/2
            })
            .then(r => {
                let t3 = Date.now();
                let data = r.data;
                assert(data['data']['data']['k1'] === 'v1');
                assert((t3-t1) >= toms);
                console.log(data);
            })
            .catch(e => {
                console.log('expected error:', e.code);
                flag = true;
            })
            .finally(() => {
                assert(flag);
                console.log('test passed');
            });
    }
    async test2() {
        const url = `${URL}/postjsonwait`;
        const json = {
            timeoutms: toms,
            data: {
                k1:'v1',
                k2:'v2'    
            }
        };
        let t1 = Date.now();
        let flag = false;
        axios.post(
            url,
            {
                method:'POST',
                headers: headers,
                data: json
            },
            {
                timeout: toms*2
            })
            .then(r => {
                let t3 = Date.now();
                let data = r.data;
                assert(data['data']['data']['k1'] === 'v1');
                assert((t3-t1) >= toms);
                console.log(data);
            })
            .catch(e => {
                flag = true;
                console.log('unexpected error:', e.code);
            })
            .finally(() => {
                assert(!flag);
                console.log('test passed');
            });
    }
    test() {
        this.test2();
        this.test1();
    }
}

var t = new DockerTest();
t.test();
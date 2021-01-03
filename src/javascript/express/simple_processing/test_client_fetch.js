const fs = require('fs');
const fetch = require('node-fetch');
const assert = require('assert');
const AbortController = require('abort-controller');
const formdata = require('form-data');
const axios = require('axios').default;

class Tests {
    constructor() {
        this.controller = new AbortController();
    }
    async testPostJson() {
        {
            // simple case
            try {
                const url = 'http://localhost:3000/postjson1/v1/v2';
                const headers = {
                    'Accept': 'application/json',
                    'Content-Type':'application/json'
                };
                const json = {
                    'k1':'v1',
                    'k2':'v2'
                };
                const jsonStr = JSON.stringify(json);
                const res = await fetch(url, { method:'POST', headers: headers, body: jsonStr });   // body cannot be json
                const rspjson = await res.json();
                const rspjsonstr = JSON.stringify(rspjson, null, 4);
                console.log(`post example: \n${rspjsonstr}`);
            } catch(e) {
                console.log(e);
                throw e;
            }
        }
        {
            // delayed response case with settimeout on server side, using fetch.then syntax
            var toms = 500;
            try {
                const url = 'http://localhost:3000/postjsonwait';
                const headers = {
                    'Accept': 'application/json',
                    'Content-Type':'application/json'
                };
                const json = {
                    timeoutms: toms,
                    data: {
                        k1:'v1',
                        k2:'v2'    
                    }
                };
                const jsonStr = JSON.stringify(json);
                let t1 = Date.now();
                let t2 = null, t3 = null;
                const res = fetch(url,
                    {
                        method:'POST',
                        headers: headers,
                        body: jsonStr
                    })
                    .then(r => {
                        t2 = Date.now();
                        return r.json();
                    })
                    .then(r => {
                        t3 = Date.now();
                        const rspjsonstr = JSON.stringify(r, null, 4);
                        console.log(`post example: \n${rspjsonstr}`);
                        assert((t3-t1) >= toms);
                        assert((t3-t2) < toms);
                        assert((t2-t1) >= toms);
                    });
                assert(res instanceof Promise);
                console.log(res.resolve());
            } catch(e) {
                console.log(e);
                throw e;
            }
        }
        {
            // delayed response case with settimeout on server side, using await syntax
            var toms = 500;
            try {
                const url = 'http://localhost:3000/postjsonwait';
                const headers = {
                    'Accept': 'application/json',
                    'Content-Type':'application/json'
                };
                const json = {
                    timeoutms: toms,
                    data: {
                        k1:'v1',
                        k2:'v2'    
                    }
                };
                const jsonStr = JSON.stringify(json);
                let t1 = Date.now();
                const res = await fetch(url, { method:'POST', headers: headers, body: jsonStr });   // body cannot be json
                let t2 = Date.now();
                const rspjson = await res.json();
                let t3 = Date.now();
                const rspjsonstr = JSON.stringify(rspjson, null, 4);
                console.log(`post example: \n${rspjsonstr}`);
                assert((t3-t1) >= toms);
                assert((t3-t2) < toms);
            } catch(e) {
                console.log(e);
                throw e;
            }
        }
        {
            var toms = 500;
            try {
                // delayed response case with promise on server side
                const url = 'http://localhost:3000/postjsonpromisewait';
                const headers = {
                    'Accept': 'application/json',
                    'Content-Type':'application/json'
                };
                const json = {
                    timeoutms: toms,
                    data: {
                        k1:'v1',
                        k2:'v2'
                        }
                };
                const jsonStr = JSON.stringify(json);
                let t1 = Date.now();
                const res = await fetch(url, { method:'POST', headers: headers, body: jsonStr });   // body cannot be json
                let t2 = Date.now();
                const rspjson = await res.json();
                let t3 = Date.now();
                const rspjsonstr = JSON.stringify(rspjson, null, 4);
                console.log(`post example: \n${rspjsonstr}`);
                assert((t3-t1) >= toms);
                assert((t3-t2) < toms);
            } catch(e) {
                console.log(e);
                throw e;
            }
        }
        {
            // delayed response with local timeout not aborting
            try {
                var timeoutremote = 1000;
                var timeoutlocal = 2000;
                let controller = new AbortController();
                const url = 'http://localhost:3000/postjsonwait';
                const headers = {
                    'Accept': 'application/json',
                    'Content-Type':'application/json'
                };
                const json = {
                    timeoutms: timeoutremote,
                    data: {
                        k1:'v1',
                        k2:'v2'
                    }
                };
                const jsonStr = JSON.stringify(json);
                let t1 = Date.now();
                let tohandler = setTimeout(() => controller.abort(), timeoutlocal);
                let res = await fetch(url, {
                    signal: controller.signal,
                    method:'POST',
                    headers: headers,
                    body: jsonStr 
                });
                let t2 = Date.now();
                const rspjson = await res.json();
                clearTimeout(tohandler);
                let t3 = Date.now();
                const rspjsonstr = JSON.stringify(rspjson, null, 4);
                console.log(`post example: \n${rspjsonstr}`);
                assert((t3-t1) >= timeoutremote);
                assert((t3-t2) < timeoutremote);
            } catch(e) {
                console.log(e);
                throw e;
            }    
        }
        {
            // delayed response with localtimeout aborting
            var timeoutremote = 1000;
            var timeoutlocal = 500;
            let controller = new AbortController();
            const url = 'http://localhost:3000/postjsonwait';
            const headers = {
                'Accept': 'application/json',
                'Content-Type':'application/json'
            };
            const json = {
                timeoutms: timeoutremote,
                data: {
                    k1:'v1',
                    k2:'v2'
                }
            };
            const jsonStr = JSON.stringify(json);
            let t1 = Date.now();
            try {
                let tohandler = setTimeout(() => controller.abort(), timeoutlocal);
                let res = await fetch(url, {
                    signal: controller.signal,
                    method:'POST',
                    headers: headers,
                    body: jsonStr 
                });
                let t2 = Date.now();
                clearTimeout(tohandler); // this is too late, and doesn't clear
                const rspjson = await res.json();
                assert(false); // tohandler should have aborted, not gotten here
            } catch(e) {
                if(e.name !== 'AbortError') {
                    throw e;
                } else {
                    assert(e.name === 'AbortError');
                }
            } finally {
                console.log('timeout abort case finished');
            }
        }
    }
    async testSingle() {
        try {
            {
                // delayed response case with settimeout on server side, using fetch.then syntax
                var toms = 500;
                try {
                    const url = 'http://localhost:3000/postjsonwait';
                    const headers = {
                        'Accept': 'application/json',
                        'Content-Type':'application/json'
                    };
                    const json = {
                        timeoutms: toms,
                        data: {
                            k1:'v1',
                            k2:'v2'    
                        }
                    };
                    const jsonStr = JSON.stringify(json);
                    let t1 = Date.now();
                    let t2 = null, t3 = null;
                    const res = fetch(url,
                        {
                            method:'POST',
                            headers: headers,
                            body: jsonStr
                        })
                        .then(r => {
                            t2 = Date.now();
                            return r.json();
                        })
                        .then(r => {
                            t3 = Date.now();
                            const rspjsonstr = JSON.stringify(r, null, 4);
                            console.log(`post example: \n${rspjsonstr}`);
                            assert((t3-t1) >= toms);
                            assert((t2-t1) >= toms);
                            assert((t3-t2) < toms);
                        });
                    assert(res instanceof Promise);
                    const r1 = await res;
                    assert(r1 === undefined);
                } catch(e) {
                    console.log(e);
                    throw e;
                }
            }

        } catch(e) {
            console.log(e);
            throw e;
        }
    }
    async testPostFile() {
        {
            // this has to be a form post
            const url = 'http://localhost:3000/postfile';
            const filename = './dir_input/inputfile1.txt';
            const readstream = fs.createReadStream(filename);
            const filesize = fs.statSync(filename).size;
            console.log(filesize);
            const headers = {
                'Accept': 'application/json',
                //'Content-Type':'multipart/form-data', // do not specify
                'Content-length': filesize
            };
            const promise = fetch(url,
                {
                    method:'POST',
                    headers: headers,
                    body: readstream
                });
            const res = await promise;
            const json = await res.json();
            console.log(json);
        }
    }
    async testPostFileForm() {
        {
            // this has to be a form post
            const url = 'http://localhost:3000/postform';
            const filename = 'inputfile1.txt';
            const filepath = './dir_input/' + filename;
            const readstream = fs.createReadStream(filepath);
            const filesize = fs.statSync(filepath).size;
            const form = new formdata();
            console.log(filesize);
            const headers = {
                'Accept': 'application/json',
            };

            // the server side has to also be called file
            form.append('file', readstream, {
                filename: filename,
                filepath: filepath
            });
            const res = await fetch(url,
                {
                    method:'POST',
                    body: form
                });
            const json = await res.json();
            console.log(json);
        }
        {
            // this has to be a form post
            const url = 'http://localhost:3000/postformarray';
            const filename = 'inputfile2.txt';
            const filepath = './dir_input/' + filename;
            const readstream = fs.createReadStream(filepath);
            const filesize = fs.statSync(filepath).size;
            const form = new formdata();
            console.log(filesize);
            const headers = {
                'Accept': 'application/json',
            };

            // the server side has to also be called file
            form.append('file', readstream, {
                filename: filename,
                filepath: filepath
            });
            const res = await fetch(url,
                {
                    method:'POST',
                    body: form
                });
            const json = await res.json();
            console.log(json);
        }
    }
    async testPostMultipleFileForm() {
        {
            // this has to be a form post
            const url = 'http://localhost:3000/postformarray';
            const filename1 = 'inputfile1.txt';
            const filepath1 = './dir_input/' + filename1;
            const readstream1 = fs.createReadStream(filepath1);

            const filename2 = 'inputfile2.txt';
            const filepath2 = './dir_input/' + filename2;
            const readstream2 = fs.createReadStream(filepath2);

            const filename3 = 'inputfile3.txt';
            const filepath3 = './dir_input/' + filename3;
            const readstream3 = fs.createReadStream(filepath3);

            const form = new formdata();

            // the server side has to also be called file
            form.append('file', readstream1, {
                filename: filename1,
                filepath: filepath1
            });
            form.append('file', readstream2, {
                filename: filename2,
                filepath: filepath2
            });
            form.append('file', readstream3, {
                filename: filename3,
                filepath: filepath3
            });
            const res = await fetch(url,
                {
                    method:'POST',
                    body: form
                });
            const json = await res.json();
            console.log(json);
        }
    }

    async testSingleAxiosDelay() {
        // delayed response case with settimeout on server side, using fetch.then syntax
        var toms = 500;
        const url = 'http://localhost:3000/postjsonwait';
        const headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json'
        };
        const json = {
            timeoutms: toms,
            data: {
                k1:'v1',
                k2:'v2'    
            }
        };
        let t1 = Date.now();
        axios.post(
            url,
            {
                method:'POST',
                headers: headers,
                data: json
            })
            .then(r => {
                let t3 = Date.now();
                let data = r.data;
                //console.log(data);
                //console.log(`t1: ${t1} t3:${t3} diff: ${t3-t1}`);
                assert(data['data']['data']['k1'] === 'v1');
                assert((t3-t1) >= toms);
            });
    }
    async testSingleAxiosDelayTimeout() {
        // delayed response case with settimeout on server side, using fetch.then syntax
        var toms = 500;
        const url = 'http://localhost:3000/postjsonwait';
        const headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json'
        };
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
            })
            .catch(e => {
                //console.log('timed out:', e.code);
                //console.log('timed out:', e.toJSON());
                flag = true;
            })
            .finally(() => {
                assert(flag);
            });
    }
    async testaAxiosMultiCall() {
        // delayed response case with settimeout on server side, using fetch.then syntax
        var toms = 500;
        const url = 'http://localhost:3000/postjsonseriescombine';
        const headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json'
        };
        const json = {
            timeoutms: toms,
            data: {
                k1:100,
                k2:'v2'    
            }
        };
        axios.post(
            url,
            {
                method:'POST',
                headers: headers,
                data: json
            },
            {
                timeout: toms
            })
            .then(r => {
                let data = r.data;
                console.log(data);
            })
            .catch(e => {
                console.log('timed out:', e.code);
            });
    }
    async testSingleDockerAxiosDelayTimeoutCall() {
        // delayed response case with settimeout on server side, using fetch.then syntax
        var toms = 500;
        const url = 'http://localhost:3030/postjsonwait';
        const headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json'
        };
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
                //console.log('error:', e.code);
                //console.log('timed out:', e.toJSON());
                flag = true;
            })
            .finally(() => {
                assert(flag);
                console.log('test passed');
            });
    }
    test() {
        /*
        this.testPostJson();
        this.testSingle();
        this.testPostMultipleFileForm();
        this.testPostFile();
        this.testPostFileForm();
        this.testSingleAxiosDelay();
        this.testSingleAxiosDelayTimeout();
        this.testaAxiosMultiCall();
        */

        this.testSingleDockerAxiosDelayTimeoutCall();
    }
}

var t = new Tests();
t.test();
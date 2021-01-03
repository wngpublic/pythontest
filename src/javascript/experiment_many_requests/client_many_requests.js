const fetch = require('node-fetch');
const assert = require('assert');
const AbortController = require('abort-controller');
const http = require('http');
const events = require('events');
const AgentKeepAlive = require('agentkeepalive');

class ClientManyRequests {
    constructor() {
        this.numActive = 0;
        this.concurrentLimit = 250;
        this.pendingLimit = 100;
        this.delay = 100;
        this.qPending = [];
        this.qActive = [];
        this.qCompleted = [];
        this.counterCompleted1 = 0;
        this.ctrCompleted = 0;
        this.ctrRetry = 0;
        this.ctrReject = 0;
        this.eventEmitter = new events.EventEmitter();
        this.isHeld = false;
        this.id = 0;
        this.ctr1 = 0;
        this.ctr2 = 1_000_000;
        this.ctr3 = 0;
        this.numError = 0;
        this.retriesCompleted = 0;
        this.url = 'http://localhost:3000/postjson';
        this.isDone = false;
        this.q = [];
        this.tstart = 0;
        this.retriesMax = 3;
        this.totalNumReqs = 0;
        this.headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json'
        };
        this.httpAgent = new http.Agent({
            keepAlive: true,
            maxSockets: this.concurrentLimit
        });
        this.agentKeepAlive = new AgentKeepAlive({
            maxSockets: this.concurrentLimit
        });
    }
    async fetchMany(numReqs) {
        let numCompleted = 0;
        const url = 'http://localhost:3000/postjson1';
        const headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json'
        };
        let ctr1 = 0;
        let ctr2 = 1_000_000;
        for (let i = 0; i < numReqs; i++) {
            const json = {
                k1: ctr1++,
                k2: ctr2++
            };

        }
    }
    // this causes ECONNRESET because too many connections
    // this seems to work on laptop for up to 1000 reqs (sometimes)
    async singleFetchMany(numReqs) {
        let q = [];
        let ms = 1;
        let ctr1 = 0;
        let ctr2 = 1_000_000;
        let t1 = Date.now();

        for (let i = 0; i < numReqs; i++) {
            const data = {
                timeoutms: ms,
                data: {
                    k1: ctr1++,
                    k2: ctr2++    
                }
            };
            let p = fetch(this.url, {
                method: 'POST',
                headers: this.headers,
                body: JSON.stringify(data)
            })
            .then((res) => res.json())
            .then((json) => {
                assert(json['data']['k1'] === data['data']['k1']);
                assert(json['data']['k2'] === data['data']['k2']);
            });
            q.push(p);
        }
        Promise.all(q).then(() => {
            let t2 = Date.now();
            console.log(`test ms elapsed: ${t2-t1}`);    
        });
    }
    async fetchRetry(url, options, n) {
        n--;
        return new Promise((resolve,reject) => {
            fetch(url, options)
            .then((r) => resolve(r))
            .catch((e) => {
                if(n < 0) {
                    reject(e);
                } else {
                    this.fetchRetry(url,options,n)
                    .then((r) => resolve(r))
                    .catch((e) => reject(e));
                }
            });
        });
    }
    // this works with 1M requests with 0.015% (150/1_000_000)error rate with ECONNRESET , but it took a looong time..
    // try not to do the promise wait all, and do a pipeline instead. maybe that will speed up.
    // and do retries with ECONNRESET
    async testManyFetchLoopCB(numReqs, q) {
        if(this.isHeld) {
            return;
        }
        this.isHeld = true;
        console.log(`enter testManyFetchLoopCB ${this.ctr3} numcompleted: ${this.counterCompleted1} numerror: ${this.numError}`);
        this.ctr3++;

        let localq = [];
        while(this.numActive < this.concurrentLimit && 
            (this.counterCompleted1 + this.numActive) < numReqs) {
            this.numActive++;
            let ms = 1;
            const data = {
                timeoutms: ms,
                data: {
                    k1: this.ctr1++,
                    k2: this.ctr2++
                }
            };
            let p = fetch(this.url, {
                method: 'POST',
                headers: this.headers,
                body: JSON.stringify(data)
            })
            .then((res) => res.json())
            .then((json) => {
                assert(json['data']['k1'] === data['data']['k1']);
                assert(json['data']['k2'] === data['data']['k2']);
                this.numActive--;
                this.counterCompleted1++;
            })
            .catch(e => {
                this.numError++;
                let pRetry = this.fetchRetry(this.url, options, 3);
                console.log('ERROR FETCH: ', e.code);
            });
            q.push(p);
        }
        if(this.counterCompleted1 >= numReqs) {
            console.log(`completed ${this.counterCompleted1}`);
        }
        Promise.all(q).then(() => {
            this.isHeld = false;
            if(this.numActive < this.concurrentLimit && 
                (this.counterCompleted1 + this.numActive) < numReqs && !this.isHeld) {
                this.testManyFetchLoopCB(numReqs,q);
            } else if((this.counterCompleted1+this.numError) >= numReqs) {
                console.log(`cb completed ${this.counterCompleted1}`);
            }
            q = [];
        });
    }
    async testManyFetchEventEmitter(numReqs) {
        //console.log(`numreqs: ${numReqs}`);
        while(this.numActive < this.concurrentLimit && 
            (this.counterCompleted1 + this.numActive + this.numError) < numReqs) {
            this.numActive++;
            const data = {
                timeoutms: 1,
                data: {
                    k1: this.ctr1++,
                    k2: this.ctr2++
                }
            };
            const options = {
                method: 'POST',
                headers: this.headers,
                body: JSON.stringify(data)
            };
            let p = fetch(this.url,options)
                .then((res) => res.json())
                .then((json) => {
                    assert(json['data']['k1'] === data['data']['k1']);
                    assert(json['data']['k2'] === data['data']['k2']);
                    this.numActive--;
                    this.counterCompleted1++;
                    if(this.numActive < this.concurrentLimit) {
                        //console.log(`emit supply`);
                        this.eventEmitter.emit('supply', numReqs);
                    }
                    if(this.counterCompleted1 % 100 == 0) {
                        console.log(`completed ${this.counterCompleted1}`);
                    }
                    //console.log(`completed ${this.counterCompleted1}`);
                })
                .catch(e => {
                    this.counterCompleted1++;
                    this.numError++;
                    //let pRetry = this.fetchRetry(this.url, options, 3);
                    console.log('ERROR FETCH: ', e.code);
                });
            this.q.push(p);
        }
    }
    testManyFetchEventEmitterDone() {
        console.log(`DONE: completed ${this.counterCompleted1}`);
        this.isDone = true;
    }
    async testManyFetchEventEmitterRegister() {
        this.eventEmitter.on('supply', this.testManyFetchEventEmitter);
        this.eventEmitter.on('done', this.testManyFetchEventEmitterDone);
    }
    // FIXME this doesnt work.
    async testManyFetchWhileLoop(numReqs) {
        let ctr = 0;
        let localq = [];
        let numcompleted = 0;
        while(ctr < this.concurrentLimit) {
            const data = {
                timeoutms: 1,
                data: {
                    k1: this.ctr1++,
                    k2: this.ctr2++
                }
            };
            const options = {
                method: 'POST',
                headers: this.headers,
                body: JSON.stringify(data)
            };
            let p = fetch(this.url,options)
                .catch((e) => {
                    this.numError++;
                    console.log(`fetch err: ${e.code}`);
                });
            let ds = {
                data: data,
                promise: p
            };
            localq.push(ds);
            this.numActive++;
            ctr++;
        }
        while(localq.length != 0) {
            let ds = localq.shift();

            //console.log(`ds: `, ds);
            let curp = ds['promise'];
            let rsp = await curp;
            //console.log(`rsp: `, rsp);

            if(rsp != undefined) {

                let json = await rsp.json();
                //console.log(`json: `,json);
                //console.log(`json data: `, json['data']);
                //console.log(`ds json: `, ds['data']['data']);
                assert(json['data']['k1'] === ds['data']['data']['k1']);
                assert(json['data']['k2'] === ds['data']['data']['k2']);
                if(numcompleted % 1000 === 0) {
                    console.log(`numcompleted: ${numcompleted} numactive: ${this.numActive} numErr: ${this.numError}`);
                }
                numcompleted++;
                this.numActive--;
                if((numcompleted + this.numActive) < numReqs) {
                    const data = {
                        timeoutms: 1,
                        data: {
                            k1: this.ctr1++,
                            k2: this.ctr2++
                        }
                    };
                    const options = {
                        method: 'POST',
                        headers: this.headers,
                        body: JSON.stringify(data)
                    };
                    let p = fetch(this.url,options)
                        //.then((r) => r.json())
                        .catch((e) => {
                            this.numError++;
                            console.log(`fetch err: ${e.code}`);
                        });
                    let ds = {
                        data: data,
                        promise: p
                    };
                    localq.push(ds);
                    this.numActive++;    
                }

            } else {
                console.log(`rsp is undefined`);
            }

        }
        console.log(`completed ${numcompleted}`);

    }
    async fetchJsonWithRetries1(url, data, n, derr) {
        const options = {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data)
        };
        let p = new Promise((resolve,reject) => {
            fetch(this.url,options)
            .then((r) => {
                this.ctrCompleted++;
                derr[data['id']]['complete']++;
                resolve(r);
            })
            .catch((e) => {
                if(n <= 0) {
                    derr[data['id']]['error']++;
                    this.ctrReject++;
                    reject(e);
                } else {
                    //console.log(`retry id: ${data['id']}`);
                    derr[data['id']]['retry']++;
                    this.ctrRetry++;
                    n--;
                    this.fetchJsonWithRetries1(url, data, n, derr);
                }
            });
        });
        return p;
    }
    async fetchJsonWithRetries(url, data, n, derr) {
        const options = {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data)
        };
        let p = fetch(this.url,options)
            .then((r) => r.json())
            .then((json) => {
                if(n < this.retriesMax) {
                    this.retriesCompleted++;
                }
                this.ctrCompleted++;
                derr[data['id']]['complete']++;
                assert(json['data']['k1'] === data['data']['k1']);
                assert(json['data']['k2'] === data['data']['k2']);
            })
            .catch((e) => {
                if(n <= 0) {
                    derr[data['id']]['error']++;
                    this.ctrReject++;
                    if(!(e.code in derr[data['id']]['code'])){
                        derr[data['id']]['code'][e.code] = 0;
                    }
                    derr[data['id']]['code'][e.code]++;
                } else {
                    //console.log(`retry id: ${data['id']}`);
                    derr[data['id']]['retry']++;
                    this.ctrRetry++;
                    n--;
                    return this.fetchJsonWithRetries(url, data, n, derr);
                }
            });
        return p;
    }
    async promiseAllCheck(q, derr, numReqs) {
        return new Promise((resolve,reject) => {
            Promise.all(q).then((r) => {
                if((this.ctrCompleted + this.ctrReject) === numReqs) {
                    for(let i = 0; i < numReqs; i++) {
                        if(i in derr){
                            if(derr[i]['error'] > 0) {
                                //console.log(`RETRY: retry ${derr[i]['retry']} complete ${derr[i]['complete']} err ${derr[i]['error']} code: ${JSON.stringify(derr[i]['code'])}`);
                            }
                        }
                    }
                    let tnow = Date.now();
                    console.log(`time elapsed: ${tnow-this.tstart}`);
                    console.log(`complete ${this.ctrCompleted} retries: ${this.ctrRetry} reject: ${this.ctrReject} retriesCompleted: ${this.retriesCompleted}`);    
                }
                resolve();
            }).catch((e) => {
                for(let i = 0; i < numReqs; i++) {
                    if(i in derr){
                        if(derr[i]['error'] > 0 || derr[i]['retry'] > 0) {
                            console.log(`RETRY: retry ${derr[i]['retry']} complete ${derr[i]['complete']} err ${derr[i]['error']} code: ${JSON.stringify(derr[i]['code'])}`);
                        }
                    }
                }
                console.log(`CATCH complete ${this.ctrCompleted} retries: ${this.ctrRetry} reject: ${this.ctrReject}`);
                reject();
            });    
        });
    }
    // this works with retries
    async testFetchRetries(numReqs) {
        let q = [];
        let ctr1 = 0;
        let ctr2 = 100_000;
        let derr = {};
        this.tstart = Date.now();
        for(let i = 0; i < numReqs; i++) {
            const data = {
                timeoutms: 1,
                id: i,
                data: {
                    k1: ctr1++,
                    k2: ctr2++
                }
            };
            derr[i] = {
                retry: 0,
                complete: 0,
                error: 0,
                code: {}
            };
            let p = this.fetchJsonWithRetries(this.url,data,this.retriesMax,derr);
            q.push(p);
            // 284408 for 500
            // 224211 for 100
            // 243162 for 100
            // 223932 for 200
            // 224965 for 200
            if((q.length % 200) === 0) {
                await this.promiseAllCheck(q, derr, numReqs);
                if((this.ctrCompleted + this.ctrReject) % 5000 === 0) {
                    console.log(`complete ${this.ctrCompleted} retries: ${this.ctrRetry} reject: ${this.ctrReject} retriesCompleted: ${this.retriesCompleted}`);    
                }
                q = [];
            }
        }
        await this.promiseAllCheck(q);
    }
    async fetchJsonWithRetriesUpdateStructs(url, data, n, derr, d, id) {
        //let controller = new AbortController();
        //let timeoutHandler = null;
        try {
            //timeoutHandler = setTimeout(() => controller.abort(), 500);
        } catch(e) {
            if(e.name === 'AbortController') {
                derr[id]['retry']++;
                this.ctrRetry++;
                return this.fetchJsonWithRetriesUpdateStructs(url, data, n, derr, d, id);
            }
        }
        const options = {
            //signal: controller.signal,
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data)
        };
        let p = fetch(this.url,options)
            .then((r) => r.json())
            .then((json) => {
            //.then(async (r) => {
                this.numActive--;
                //clearTimeout(timeoutHandler);
                //let json = await r.json();
                if(n < this.retriesMax) {
                    this.retriesCompleted++;
                }
                this.ctrCompleted++;
                derr[id]['complete']++;
                if(json['data']['k1'] !== data['data']['k1'] || json['data']['k2'] !== data['data']['k2']) {
                    console.log('assertion error');
                }
                assert(json['data']['k1'] === data['data']['k1']);
                assert(json['data']['k2'] === data['data']['k2']);    
                //delete d[id];
                if((this.numActive + this.ctrCompleted) < this.totalNumReqs) {
                    this.testAddFetchesToQueue(d,derr,1);
                }
            })
            .catch((e) => {
                n--;
                if(n <= 0) {
                    derr[id]['error']++;
                    derr[id]['complete']++;
                    this.ctrReject++;
                    this.numActive--;
                    this.ctrCompleted++;
                    if(!(e.code in derr[data['id']]['code'])){
                        derr[id]['code'][e.code] = 0;
                    }
                    derr[id]['code'][e.code]++;
                    //delete d[id];
                } else {
                    derr[id]['retry']++;
                    this.ctrRetry++;
                    return this.fetchJsonWithRetriesUpdateStructs(url, data, n, derr, d, id);
                }
            });
        return p;
    }
    async fetchJsonWithRetriesKeepAliveUpdateStructs(url, data, n, derr, d, id) {
        const options = {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data),
            agent: this.httpAgent //,
            //agent: this.agentKeepAlive
        };
        let p = fetch(this.url,options)
            .then((r) => r.json())
            .then((json) => {
                this.numActive--;
                if(n < this.retriesMax) {
                    this.retriesCompleted++;
                }
                this.ctrCompleted++;
                derr[id]['complete']++;
                assert(json['data']['k1'] === data['data']['k1']);
                assert(json['data']['k2'] === data['data']['k2']);    
                if(derr[id]['retry'] < 1) {
                    delete derr[id];
                    delete d[id];
                }
                if((this.numActive + this.ctrCompleted) < this.totalNumReqs) {
                        this.testAddFetchesToQueueKeepAlive(d,derr,1);
                }
            })
            .catch((e) => {
                n--;
                if(n <= 0) {
                    derr[id]['error']++;
                    derr[id]['complete']++;
                    this.ctrReject++;
                    this.numActive--;
                    this.ctrCompleted++;
                    if(!(e.code in derr[data['id']]['code'])){
                        derr[id]['code'][e.code] = 0;
                    }
                    derr[id]['code'][e.code]++;
                    delete d[id];
                } else {
                    derr[id]['retry']++;
                    this.ctrRetry++;
                    return this.fetchJsonWithRetriesKeepAliveUpdateStructs(url, data, n, derr, d, id);
                }
            });
        return p;
    }
    async sleepPromise(ms) {
        return new Promise((resolve) => {
            setTimeout(() => resolve(), ms);
        });
    }
    async testAddFetchesToQueue(d, derr, numReqs) {
        for(let i = 0; i < numReqs; i++) {
            let id = this.id++;
            const data = {
                timeoutms: 1,
                id: id,
                data: {
                    k1: this.ctr1++,
                    k2: this.ctr2++
                }
            };
            assert(!(id in derr));
            derr[id] = {
                id: id,
                retry: 0,
                complete: 0,
                error: 0,
                code: {}
            };
            let n = this.retriesMax;
            let p = this.fetchJsonWithRetriesUpdateStructs(this.url,data,n,derr,d,id);
            this.numActive++;
            d[id] = p;
        }

    }
    async testAddFetchesToQueueKeepAlive(d, derr, numReqs) {
        for(let i = 0; i < numReqs; i++) {
            let id = this.id++;
            const data = {
                timeoutms: 1,
                id: id,
                data: {
                    k1: this.ctr1++,
                    k2: this.ctr2++
                }
            };
            assert(!(id in derr));
            derr[id] = {
                id: id,
                retry: 0,
                complete: 0,
                error: 0,
                code: {}
            };
            let n = this.retriesMax;
            let p = this.fetchJsonWithRetriesKeepAliveUpdateStructs(this.url,data,n,derr,d,id);
            this.numActive++;
            d[id] = p;
        }

    }
    async testAddFetchesToQueueMain(numReqs) {
        this.totalNumReqs = numReqs;
        this.concurrentLimit = 200;
        let starterLimit = (numReqs < this.concurrentLimit) ? numReqs : this.concurrentLimit;
        let d = {};
        let derr = {};
        let t1 = Date.now();
        this.testAddFetchesToQueue(d, derr, starterLimit);
        while(this.ctrCompleted < numReqs) {
            await this.sleepPromise(1000);
            let t2 = Date.now();
            console.log(`tmp completed ${this.ctrCompleted} numactive: ${this.numActive} retries: ${this.ctrRetry} reject: ${this.ctrReject} retriesCompleted: ${this.retriesCompleted} time: ${(t2-t1)/1000}`);    
            if(((t2-t1)/1000) > 500) {
                break;
            }
        }
        let localctr = 0;
        let localsum = 0;
        for(let [k,v] of Object.entries(derr)) {
            if(v['complete'] < 1 && v['error'] < 1) {
                console.log(`key ${k} val: ${JSON.stringify(v)}`);
            } else {
                localctr++;
                localsum += v['complete'] + v['error'];
            }
        }
        console.log(`num keys in derr: ${Object.entries(derr).length}`);
        console.log(`complete ${this.ctrCompleted} retries: ${this.ctrRetry} reject: ${this.ctrReject} retriesCompleted: ${this.retriesCompleted} localctr ${localctr} localsum: ${localsum}`);

    }
    /*
    performance: 
    1M:
        completed 1000000 numactive: 0 retries: 0 reject: 0 retriesCompleted: 0 time: 221.097
    1M delete structs: 
        completed 1000000 numactive: 0 retries: 0 reject: 0 retriesCompleted: 0 time: 215.064
    1M with 500 sockets:
        completed 1000000 numactive: 0 retries: 10 reject: 0 retriesCompleted: 10 time: 212.186
    1M with 250 sockets:
        completed 1000000 numactive: 0 retries: 0 reject: 0 retriesCompleted: 0 time: 218.067
    1M with 500 sockets and 2000 queued:
        completed 1000000 numactive: 0 retries: 28 reject: 0 retriesCompleted: 28 time: 215.39
    2M with 2 processes of 250 each:
        completed 1000000 numactive: 0 retries: 47 reject: 0 retriesCompleted: 47 time: 429.479
        completed 1000000 numactive: 0 retries: 0 reject: 0 retriesCompleted: 0 time: 428.496
    200k without keepalive:
        completed 200248 numactive: 200 retries: 3793 reject: 0 retriesCompleted: 3310 time: 467.362
    1M with AgentKeepAlive and 250 concurrentLimit:
        completed 1000000 numactive: 0 retries: 0 reject: 0 retriesCompleted: 0 time: 209.107
    */
    async testAddFetchesToQueueKeepAliveMain(numReqs) {
        let locallimit = this.concurrentLimit;
        this.totalNumReqs = numReqs;
        let starterLimit = (numReqs < locallimit) ? numReqs : locallimit;
        let d = {};
        let derr = {};
        let t1 = Date.now();
        this.testAddFetchesToQueueKeepAlive(d, derr, starterLimit);
        while(this.ctrCompleted < numReqs) {
            await this.sleepPromise(1000);
            let t2 = Date.now();
            console.log(`tmp completed ${this.ctrCompleted} numactive: ${this.numActive} retries: ${this.ctrRetry} reject: ${this.ctrReject} retriesCompleted: ${this.retriesCompleted} time: ${(t2-t1)/1000}`);    
            if(((t2-t1)/1000) > 500) {
                break;
            }
        }
        let localctr = 0;
        let localsum = 0;
        for(let [k,v] of Object.entries(derr)) {
            if(v['complete'] < 1 && v['error'] < 1) {
                console.log(`key ${k} val: ${JSON.stringify(v)}`);
            } else {
                localctr++;
                localsum += v['complete'] + v['error'];
            }
        }
        console.log(`num keys in derr: ${Object.entries(derr).length}`);
        console.log(`complete ${this.ctrCompleted} retries: ${this.ctrRetry} reject: ${this.ctrReject} retriesCompleted: ${this.retriesCompleted} localctr ${localctr} localsum: ${localsum}`);

    }
    async testFetchRetries1(numReqs) {
        let q = [];
        let ctr1 = 0;
        let ctr2 = 100_000;
        let derr = {};
        this.tstart = Date.now();
        for(let i = 0; i < numReqs; i++) {
            const data = {
                timeoutms: 1,
                id: i,
                data: {
                    k1: ctr1++,
                    k2: ctr2++
                }
            };
            derr[i] = {
                retry: 0,
                complete: 0,
                error: 0,
                code: {}
            };
            let p = this.fetchJsonWithRetries(this.url,data,this.retriesMax,derr);
            q.push(p);
            if((q.length % 200) === 0) {
                await this.promiseAllCheck(q, derr, numReqs);
                if((this.ctrCompleted + this.ctrReject) % 5000 === 0) {
                    console.log(`complete ${this.ctrCompleted} retries: ${this.ctrRetry} reject: ${this.ctrReject} retriesCompleted: ${this.retriesCompleted}`);    
                }
                q = [];
            }
        }
        await this.promiseAllCheck(q);
    }
    async test() {
        let t1 = Date.now();

        /*
        this.singleFetchMany(500);
        this.testManyFetchLoopCB(1_000_000);
        this.testManyFetchEventEmitterRegister();
        this.testManyFetchEventEmitter(100_000);
        Promise.all(this.q);
        this.testManyFetchWhileLoop(50_000);
        this.testFetchRetries(100_000);
        this.testAddFetchesToQueueMain(20_000);
        */

       //this.testAddFetchesToQueueMain(1_000_000);
       this.testAddFetchesToQueueKeepAliveMain(1_000_000);

        //setTimeout(() => {
        //    Promise.all(this.q);
        //}, 1_000_000);


        let t2 = Date.now();
        console.log(`main test ms elapsed: ${t2-t1}`);
    }
}

const client = new ClientManyRequests();
client.test();

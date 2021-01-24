const assert = require('assert');
const { resolve } = require('path');

class Test {
    constructor() {
        this.cntDown = 5;
        this.cntUp = 0;
        this.counts = {
            v0: 5,
            v1: 4,
            v2: 3
        };
    }
    async countUp() {
        let v = this.cntUp++;
        if(v > 10) {
            throw `cntUp > 10`;
        }
        return v;
    }
    resetCountUp(v = 0) {
        this.cntUp = v;
    }
    async countDown() {
        this.cntDown--;
        console.log(`countDown ${this.cntDown}`);
        if(this.cntDown > 0) {
            return 2;
        }
        else if(this.cntDown === 0) {
            return 1;
        }
        else {
            throw `cntDown less than 0`;
        }
    }
    countDownCounts(k) {
        this.counts[k]--;
        console.log(`countDownCounts ${k}: ${this.counts[k]}`);
        if(this.counts[k] > 0) {
            return 2;
        }
        else if(this.counts[k] === 0) {
            return 1;
        }
        else {
            throw `countDownCounts ${k} less than 0`;
        }
    }
    resetCountDown(v = 5) {
        this.cntDown = v;
        let i = v;
        for(let k of Object.keys(this.counts)) {
            this.counts[k] = i--;
        }
    }
    async countdownPromise(retries) {
        return new Promise(async (resolve, reject) => {
            try {
                let result = await this.countDown();
                if(result === 1) {
                    console.log(`result === 1`);
                    resolve(1);
                } else {
                    retries--;
                    console.log(`retry ${retries}`);
                    if(retries < 0) {
                        reject(-1);
                    } else {
                        /*
                        let res = await this.countdownPromise(retries);
                        console.log(`retry res = ${res}`);
                        resolve(res);
                        */
                       resolve(this.countdownPromise(retries));
                    }
                }
            } catch(e) {
                console.log(`reject -2`);
                reject(-2);
            }
        });
    }
    async countdownPromise1(retries) {
        return new Promise(async (resolve, reject) => {
            try {
                let result = await this.countDown();
                if(result === 1) {
                    console.log(`result === 1`);
                    resolve(1);
                } else {
                    retries--;
                    console.log(`retry ${retries}`);
                    if(retries < 0) {
                        reject(-1);
                    } else {
                       resolve(this.countdownPromise(retries));
                    }
                }
            } catch(e) {
                console.log(`reject -2`);
                reject(-2);
            }
        });
    }
    async countdownPromise2(retries) {
        return new Promise(async (resolve, reject) => {
            try {
                while(retries > 0) {
                    let result = await this.countDown();
                    if(result === 1) {
                        console.log(`result === 1`);
                        resolve(1);
                        return; // does this get executed??
                    } else {
                        retries--;
                        console.log(`retry ${retries}`);
                        if(retries < 0) {
                            reject(-1);
                        }
                    }
                }
                reject(-3);
            } catch(e) {
                console.log(`reject -2`);
                reject(-2);
            }
        });
    }
    async testCountdownPromise() {
        if(false) 
        {
            let p = await this.countdownPromise(3);
            console.log(`testCountdownPromise result ${p}`);
        }
        {
            // this is how to catch
            this.resetCountDown();
            this.countdownPromise(3)
            .then((r) => {
                console.log(`testCountdownPromise result ${r}`);
            })
            .catch((e) => {
                console.log(`testCountdownPromise error ${e}`);
            });
        }
        {
            // this is how to catch
            this.resetCountDown();
            this.countdownPromise(5)
            .then((r) => {
                console.log(`testCountdownPromise result ${r}`);
            })
            .catch((e) => {
                console.log(`testCountdownPromise error ${e}`);
            })
        }
    }
    async testCountdownPromise1() {
        if(false) 
        {
            let p = await this.countdownPromise(3);
            console.log(`testCountdownPromise result ${p}`);
        }
        {
            // this is how to catch
            this.resetCountDown();
            // countdownPromise1 throws, and this should be caught within
            this.countdownPromise1(3)
            .then((r) => {
                console.log(`testCountdownPromise1 result ${r}`);
            })
            .catch((e) => {
                console.log(`testCountdownPromise1 error ${e}`);
            });
        }
        {
            // this is how to catch
            this.resetCountDown();
            this.countdownPromise1(5)
            .then((r) => {
                console.log(`testCountdownPromise1 result ${r}`);
            })
            .catch((e) => {
                console.log(`testCountdownPromise1 error ${e}`);
            })
        }
    }
    async testCountdownPromise2() {
        let flag = false;
        if(false) 
        {
            let p = await this.countdownPromise(3);
            console.log(`testCountdownPromise result ${p}`);
        }
        if(false)
        {
            // this is how to catch
            this.resetCountDown();
            this.countdownPromise2(3)
            .then((r) => {
                console.log(`testCountdownPromise2 result ${r}`);
            })
            .catch((e) => {
                console.log(`testCountdownPromise2 error ${e}`);
            });
        }
        if(false)
        {
            // this is how to catch
            this.resetCountDown();
            this.countdownPromise2(5)
            .then((r) => {
                console.log(`testCountdownPromise2 result ${r}`);
            })
            .catch((e) => {
                console.log(`testCountdownPromise2 error ${e}`);
            });
        }
        {
            // this doesnt catch the promise!
            try {
                flag = false;
                this.resetCountDown();
                let r = await this.countdownPromise2(3);
                console.log(`testCountdownPromise2 result ${r}`);
            } catch(e) {
                flag = true;
            } finally {
                assert(flag);
            }
        }
        {
            // this is how to catch the right way
            this.resetCountDown();
            let r = await this.countdownPromise2(3)
            .then((v) => {
                console.log(`testCountdownPromise2 result ${r}`);
            })
            .catch((e) => {
                console.log(`testCountdownPromise2 error ${e}`);
            });
        }
    }
    async countdownPromiseKey(retries, k) {
        return new Promise(async (resolve, reject) => {
            try {
                let result = this.countDownCounts(k);
                if(result === 1) {
                    console.log(`${k} result === 1`);
                    resolve(1);
                } else {
                    retries--;
                    console.log(`${k} retry ${retries}`);
                    if(retries < 0) {
                        reject(-1);
                    } else {
                        this.countdownPromiseKey(retries);
                    }
                }
            } catch(e) {
                console.log(`reject -2`);
                reject(-2);
            }
        });
    }
    async testPromisesAllRejectOne() {
        {
            let flag = false;
            let flag2 = false;
            let p0 = new Promise((resolve, reject) => { resolve(0); });
            let p1 = new Promise((resolve, reject) => { resolve(1); });
            let p2 = new Promise((resolve, reject) => { reject(2); });
            // the promises that reject, catch them here and dont make Promise.all
            // go to catch, except for throw, which will cause it to go to catch block
            let r0 = p0.then(r => r).catch(e => null);
            let r1 = p1.then(r => r).catch(e => null);
            let r2 = p2.then(r => r).catch(e => {
                flag2 = true;
                throw e;
            });
            Promise.all([r0,r1,r2])
            .then((lr) => {
                for(let r of lr) {
                    console.log(`r = ${r}`);
                }
            })
            .catch((e) => {
                flag = true;
                console.log(`ERROR ${e}`);
            })
            .finally((e) => {
                assert(flag);
                assert(flag2);
            });
        }
        {
            let flag = false;
            let flag2 = false;
            let p0 = new Promise((resolve, reject) => { resolve(0); });
            let p1 = new Promise((resolve, reject) => { resolve(1); });
            let p2 = new Promise((resolve, reject) => { reject(2); });
            // the promises that reject, catch them here and dont make Promise.all
            // go to catch
            let r0 = p0.then(r => r).catch(e => null);
            let r1 = p1.then(r => r).catch(e => null);
            let r2 = p2.then(r => r).catch(e => {
                flag2 = true;
                return -2;
            });
            Promise.all([r0,r1,r2])
            .then((lr) => {
                for(let r of lr) {
                    console.log(`r = ${r}`);
                }
            })
            .catch((e) => {
                flag = true;
                console.log(`ERROR ${e}`);
            })
            .finally((e) => {
                assert(!flag);
                assert(flag2);
            });
        }
    }
    async testAsyncCountdown() {
        {
            this.resetCountDown(5);
            let p = this.countDown();
            assert(p instanceof Promise);
            let v = await p;
            assert(!(v instanceof Promise));
            assert(v === 2);
        }
    }
    async test() {
        await this.testAsyncCountdown();
    }
}

const t = new Test();
(async (() => {
    await this.testAsyncCountdown();
}))();
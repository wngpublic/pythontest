class TestAlgos {
    assert = require('assert');
    debug = false;

    logdbg(s) {
        if(this.debug) {
            console.log(s);
        }
    }
    randList(list) {
        let sz = list.length;
        let idx = this.randInt(0,sz);
        return list[idx];
    }
    randInt(min, max) {
        let r = Math.random() * (max-min) + min;
        let i = Math.floor(r); 
        // Math.round(r) -> 50% distro for min and max
        return i;
    }
    testRandom() {
        const min = 1;
        const max = 4;
        const numRuns = 10000;
        let map = {};
        for(let i = 0; i < numRuns; i++) {
            const res = this.randInt(min, max);

            if(!(res in map)) {
                map[res] = 0;
            }
            map[res]++;
            this.assert(res >= min && res <= max);
        }
        // the min and max are likely to be 50% of middle numbers because it uses
        // round instead of floor or ceil
        for(let [k,v] of Object.entries(map)) {
            this.logdbg(`${k}: ${v}`);
        }
        const l = [2,4,6];
        this.assert(l.length == 3);

    }
    testMontyHall() {
        const min = 1;
        const max = 4;
        const numRuns = 10000;
        let map = {  };
        // no switch
        {
            map = { win: 0, lose: 0 };
            for(let i = 0; i < numRuns; i++) {
                const dst = this.randInt(min, max);
                let choose = this.randInt(min, max);
                if(dst == choose) {
                    map['win']++;
                } else {
                    map['lose']++;
                }
            }
            for(let [k,v] of Object.entries(map)) {
                this.logdbg(`${k}: ${v}`);
            }
            const winPct = (map['win']/numRuns).toFixed(3);
            const deviation = Math.abs(1-winPct/0.33).toFixed(2);
            this.assert(deviation < 0.1);
        }
        // switch
        {
            map = { win: 0, lose: 0 };
            for(let i = 0; i < numRuns; i++) {
                const dst = this.randInt(min, max);
                let choose = this.randInt(min, max);
                const l = [dst];
                if(choose != dst) {
                    l.push(choose);
                } else {
                    for(let j = min; j < max; j++) {
                        if(j != dst) {
                            l.push(j);
                            break;
                        }
                    }
                }
                this.assert(l.length == (max-min-1));
                let secondChoice = this.randList(l);
                if(dst == secondChoice) {
                    map['win']++;
                } else {
                    map['lose']++;
                }
            }
            for(let [k,v] of Object.entries(map)) {
                this.logdbg(`${k}: ${v}`);
            }
            const winPct = (map['win']/numRuns).toFixed(3);
            const deviation = Math.abs(1-winPct/0.5).toFixed(2);
            this.assert(deviation < 0.1);
        }
    }
    jsonDiff(a,b) {
        function jsonDiffMem(src,dst,mem,subpath) {
            let path = subpath.join('/');
            if(src.constructor !== dst.constructor) {
                mem[path] = {};
                mem[path]['o'] = src;
                mem[path]['n'] = dst;
                return;
            }
            else if(src.constructor === Array) {
                // values can be objects, string, array, number. just stringfiy and replace them completely.
                // assume ordering does not matter in JSON. rewrite with levenshtein if ordering does matter

            } 
            else if(src.constructor Object) {
                let overlapKeys = [];
                let tmpdel = [];
                let tmpadd = [];
                let oldKeys = Object.keys(src);
                let newKeys = Object.keys(dst);
                for(let k of oldKeys) {
                    if(!(k in dst)) {
                        tmpdel.push(k);
                    } else {
                        overlapKeys.push(k);
                    }
                }
                if(tmpdel.length != 0) {
                    mem[path]['-'] = tmpdel;
                }
                for(let k of newKeys) {
                    if(!(k in src)) {
                        tmpadd.push(k);
                    }
                }
                if(tmpadd.length != 0) {
                    mem[path]['+'] = tmpadd;
                }
                for(let k of overlapKeys) {
                    let vOld = src[k];
                    let vNew = dst[k];
                    subpath.push(k);
                    jsonDiffMem(vOld,vNew,mem,subpath);
                    subpath.pop();
                }
            }
            else if(src.constructor === String) {
                if(src != dst) {
                    mem[path] = {};
                    mem[path]['o'] = src;
                    mem[path]['n'] = dst;
                }
            }
            else if(src.constructor === Number) {
                if(src != dst) {
                    mem[path] = {};
                    mem[path]['o'] = src;
                    mem[path]['n'] = dst;
                }
            }
        }
        let mem = {};
        let subpath = [];
        jsonDiffMem(a,b,mem,subpath);
        return mem;
    }
    testEditDistance() {
        function editDistance(a,b) {
            this.assert(a.constructor === String && b.constructor === String);
            let sza = a.length;
            let szb = b.length;
            let mem = new Array(sza);
            for(let i = 0; i < sza; i++) {
                mem[i] = new Array(szb);
                mem[i].fill(0);
            }
            for(let i = 0; i < sza; i++) {
                for(let j = 0; j < szb; j++) {
                    let ca = a.charAt(i);
                    let cb = b.charAt(j);
                    let lasti = (i == 0) ? 0 : i-1;
                    let lastj = (j == 0) ? 0 : j-1;
                    if(ca === cb) {
                        mem[i][j] = mem[lasti][lastj];
                    } else {
                        mem[i][j] = Math.min(mem[lasti][lastj],mem[i][lastj],mem[lasti][j]) + 1;
                    }
                }
            }
            // path to lowest cost, annotate mem
            let i = sza-1, j = szb-1, buf = {};
            while(i != 0 && j != 0) {
                let lasti = (i == 0) ? 0 : i - 1;
                let lastj = (j == 0) ? 0 : j - 1;
                if(mem[i][lastj] < mem[lasti][j]) {
                    if(mem[lasti][lastj] < mem[i][lastj]) {
                        i--;
                        j--;
                    } else {
                        buf[`${i},${j}`] = b.charAt(j);
                        j--;
                    }
                } else {
                    if(mem[lasti][lastj] < mem[lasti][j]) {
                        i--;
                        j--;
                    } else {
                        buf[`${i}${j}`] = a.charAt(i);
                        i--;
                    }
                }
            }
        }
        function tc() {
            let bindedCB = editDistance.bind(this);
        }
        tc();
    }
    test() {
        //this.testRandom();
        this.testMontyHall();
    }
}

try {
    t = new TestAlgos();
    t.test();
} catch(e) {
    console.log(e);
} finally {
    console.log(`test finished`);
}

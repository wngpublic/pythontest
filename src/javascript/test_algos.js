class TestAlgos {
    assert = require('assert');
    debug = true;

    log(s) {
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
            this.log(`${k}: ${v}`);
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
                this.log(`${k}: ${v}`);
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
                this.log(`${k}: ${v}`);
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
            else if(src.constructor === Object) {
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
                mem[i][0] = i+1;
            }
            for(let j = 0; j < szb; j++) {
                mem[0][j] = j+1;
            }
            for(let i = 0; i < sza; i++) {
                for(let j = 0; j < szb; j++) {
                    let ca = a.charAt(i);
                    let cb = b.charAt(j);
                    let lasti = (i == 0) ? 0 : i-1;
                    let lastj = (j == 0) ? 0 : j-1;
                    if(ca === cb) {
                        if(i == 0 && j == 0) {
                            mem[i][j] = 0;
                        } else {
                            mem[i][j] = mem[lasti][lastj];
                        }
                    } else {
                        mem[i][j] = Math.min(mem[lasti][lastj],mem[i][lastj],mem[lasti][j]) + 1;
                    }
                }
            }
            // path to lowest cost, annotate mem
            // i (row/vertical) change is -char
            // j (col/horizontal) change is +char
            // diag change is -char and +char
            // always walk backward lower up, left, or diag.
            // always choose diag if lower or equal to left/up
            let i = sza-1, j = szb-1, buf = {};
            let flag = true;
            while(flag) {
                let lasti = (i == 0) ? 0 : i - 1;
                let lastj = (j == 0) ? 0 : j - 1;

                if(i == 0 && j == 0) {
                    if(mem[i][j] != 0) {
                    }
                    flag = false;
                }
                else if(mem[i][lastj] < mem[lasti][j]) {
                    if(mem[lasti][lastj] <= mem[i][lastj]) {
                        if(mem[lasti][lastj] < mem[i][j]) {
                            buf[`${i},${j}->${lasti},${lastj}`] = `-${a[i]},+${b[j]}`;
                        }
                        i = lasti;
                        j = lastj;
                    } else {
                        if(mem[i][lastj] < mem[i][j]) {
                            buf[`${i},${j}->${i},${lastj}`] = `+${b[j]}`;
                        }
                        j = lastj;
                    }
                }
                else {
                    if(mem[lasti][lastj] <= mem[lasti][j]) {
                        if(mem[lasti][lastj] < mem[i][j]) {
                            buf[`${i},${j}->${lasti},${lastj}`] = `-${a[i]},+${b[j]}`;
                        }
                        i = lasti;
                        j = lastj;
                    } else {
                        if(mem[lasti][j] < mem[i][j]) {
                            buf[`${i},${j}->${lasti},${j}`] = `-${a[i]}`;
                        }
                        i = lasti;
                    }
                }
            }
            let line = [];
            for(let i = 0; i < szb; i++) {
                line[i] = i;
            }
            this.log(`    ${line.join(' ')}`);
            this.log(`    ${b.split('').join(' ')}`);
            for(let i = 0; i < sza; i++) {
                this.log(`${i} ${a[i]} ${mem[i].join(' ')}`);
            }
            this.log('-----');
            this.log(`a: ${a}\nb: ${b}`);
            for(let [k,v] of Object.entries(buf)) {
                this.log(`${k}:${v}`);
            }
        }
        let bindedEditDistance = editDistance.bind(this);
        function tc() {
            let localBindedEditDistance = editDistance.bind(this);
            let a = 'abcdefg';
            let b = 'abcdefg';

            this.log('-------');    // need to use binded function
            bindedEditDistance(a,b);
            this.log('expect');

            this.log('-------');    // need to use binded function
            //editDistance(a,b); // definitely doesnt work!
            //localBindedEditDistance(a,b); // doesnt work!
            a = 'abcdefg';
            b = 'abddegghh';
            bindedEditDistance(a,b);
            this.log('expect -c/+d,-f/+g,+h,+h');

            this.log('-------');    // need to use binded function
            bindedEditDistance(b,a);
            this.log('expect -d/+c,-g/+f,-h,-h');

            this.log('-------');    // need to use binded function
            a = 'abcdefg';
            b = 'bcdegg'
            bindedEditDistance(a,b);
            // getting wrong answer for this
            this.log('expect -a,-f/+g');

            this.log('-------');    // need to use binded function
            bindedEditDistance(b,a);
            // getting wrong answer for this
            this.log('expect +a,-g/+f');

            this.log('-------');    // need to use binded function
            a = 'abcdefg';
            b = 'cdegghij'
            bindedEditDistance(a,b);
            // getting wrong answer for this
            this.log('expect -a,-b,-f/+g,+h,+i,+j');

            this.log('-------');    // need to use binded function
            bindedEditDistance(b,a);
            // getting wrong answer for this
            this.log('expect +a,+b,-g/+f,-h,-i,-j');
        }
        let bindedTC = tc.bind(this);
        bindedTC(); // this works, but inner function doesnt bind anyway!
        //tc(); // bindedTC works, but cannot do inner binding, so why bother?
        // if use tc, cannot use this.log, so using bindedTC

    }
    test() {
        /*
        this.testRandom();
        this.testMontyHall();
        */
        this.testEditDistance();
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

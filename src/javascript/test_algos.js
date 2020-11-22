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
        function jsonDiffMem(a,b,mem) {
            if(a instanceof Array) {

            } 
            else if(a instanceof Object){

            }
            else {

            }
        }
        let mem = {};
        jsonDiffMem(a,b,mem);
        return mem;
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

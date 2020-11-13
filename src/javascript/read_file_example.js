'use strict';

const assert = require('assert');
const fs = require('fs');
const fname = 'testinputlarge.json';
let lines = [];
const cbConsumeLines = (lines) => {
    let ctr = 0;
    for(let line of lines) {
        ctr++;
    }
    console.log(ctr);
    return lines;
}
const cbProcessFile = (err,dat) => {
    let splitValues = dat.split('\n');
    for(let line of splitValues) {
        lines.push(line);
    }
    return cbConsumeLines(lines);
};

// this is cb way of reading file.
fs.readFile(fname,'utf8',cbProcessFile);

assert(lines.length == 0);  // because callback hasn't finished yet

//this is Sync way of reading file. no cb
let data2 = fs.readFileSync(fname, {encoding:'utf8',flag:'r'});
let lines2 = cbProcessFile(null,data2);
assert(lines2 != null);

let data3 = fs.promises.readFile(fname);
//let fAsync = await () => Promise.all([data3]);


return;




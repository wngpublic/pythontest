const yargs = require('yargs');
const args = yargs.argv;
const assert = require('assert');
const zlib = require('zlib');
const fs = require('fs');

// datagen.js --numchars=<numchars> --outfile=<filename> --compress --hex

const charslc = 'abcdefghijklmnopqrstuvwxyz';
const charsuc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const charsn  = '0123456789';
const charsp  = '~!@#$%^&*(){}[]|';
const alphanum = charslc + charsuc + charsn;
const DEBUG   = 1;

function debug(s) {
    if(DEBUG === 0) {
        return;
    }
    console.log(s);
}

class DataGen {

    randInt(min, max) {
        // [min,max)
        let r = Math.random() * (max-min) + min;
        let i = Math.floor(r); 
        return i;
    }
    test(args) {
        var numchars = (args.numchars !== undefined) ? parseInt(args.numchars) : 0;
        var outfile  = (args.outfile !== undefined) ? args.outfile : null;
        var compress = (args.compress !== undefined) ? true : false;
        var hex      = (args.hex !== undefined) ? true : false;
        var array = [];
        var bytes = [];
        const limit = 1_000_000;
        const sz = alphanum.length;
        debug(`numchars:${numchars} outfile:${outfile} compress:${compress}`);
        assert(numchars < limit);
        for(let i = 0; i < numchars; i++) {
            let v = this.randInt(0,sz);
            let c = alphanum.charAt(v);
            let x = c.charCodeAt(0);
            array.push(c);
            bytes.push(x);
        }

        var s = array.join('');
        var encoded = new TextEncoder('utf-8').encode(s);
        var decoded = new TextDecoder('utf-8').decode(encoded);
        var uint8Array = new Uint8Array(bytes);

        debug(s);
        debug('encoded    ' + encoded);
        debug('decoded    ' + decoded);
        debug('array      ' + array);
        debug('bytes      ' + bytes);
        debug('uint8array ' + uint8Array);
        if(hex) {
            {
                var h = Array.prototype.map.call(uint8Array, x => ('0x' + x.toString(16)));
                var hs = h.join(',');
                debug(hs);
            }
            {
                var h = Array.from(uint8Array, x => ('0x' + x.toString(16)));
                var hs = h.join(',');
                debug(hs);
            }
        }
    }
}

var dataGen = new DataGen();
dataGen.test(args);

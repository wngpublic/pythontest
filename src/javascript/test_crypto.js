const cryptojs = require('crypto-js');
const crypto = require('crypto');
const assert = require('assert');
const zlib = require('zlib');
const fs = require('fs');
const stream = require('stream');
const util = require('util');
var dbgflag = true;

function debug(s) {
    if(dbgflag) {
        console.log(s);
    }
}

class Test {
    constructor() {
        this.s1 =   
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ\n'+
                    'abcdefghijklmnopqrstuvwxyz\n'+
                    '0123456789\n'+
                    '!@#$%^&*(){}[]<>';
        this.s2 =   
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'+
                    'abcdefghijklmnopqrstuvwxyz'+
                    '0123456789'+
                    '!@#$%^&*(){}[]<>';
        this.s3 =   'hello world';
        this.s4 =   'Hello World!';
        this.barray1 = [
                    0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8,
                    0x11111111,0x22222222,0x33333333,0x44444444,
                    0x55555555,0x66666666,0x77777777,0x88888888];
        this.barray2 = [
                    0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8,
                    0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,
                    0x99,0xAA,0xBB,0xCC,0xDD,0xEE,0xFF,0x00
                    ];
        this.barray3 = [
            0,1,2,3,4,5,6,7,8,9,
            10,11,12,13,14,15,16,17,18,19,
            20,21,22,23,24,25,26,27,28,29,
            30,31,32,33,34,35,36,37,38,39,
            40,41,42,43,44,45,46,47,48,49,
            50,51,52,53,54,55,56,57,58,59,
            60,61,62,63,64,65,66,67,68,69,
            70,71,72,73,74,75,76,77,78,79,
            80,81,82,83,84,85,86,87,88,89,
            90,91,92,93,94,95,96,97,98,99,
            100,101,102,103,104,105,106,107,108,109,
            110,111,112,113,114,115,116,117,118,119,
            120,121,122,123,124,125,126,127,128,129,
            130,131,132,133,134,135,136,137,138,139,
            140,141,142,143,144,145,146,147,148,149,
            150,151,152,153,154,155,156,157,158,159,
            160,161,162,163,164,165,166,167,168,169,
            170,171,172,173,174,175,176,177,178,179,
            180,181,182,183,184,185,186,187,188,189,
            190,191,192,193,194,195,196,197,198,199,
            200,201,202,203,204,205,206,207,208,209,
            210,211,212,213,214,215,216,217,218,219,
            220,221,222,223,224,225,226,227,228,229,
            230,231,232,233,234,235,236,237,238,239,
            240,241,242,243,244,245,246,247,248,249,
            250,251,252,253,254,255 ];
        this.barray4 = [1,16,32,64,127,128,200,230,254,255];
        this.barray5 = [1,16,32,64,127,128,130,200,230,254,255];
        this.salt1 = 'ThIsIsSaLt1';
        this.salt2 = 'ThiSISSalT2';
        this.key1  = 'ThIsIsKeY1';
        this.key2  = 'ThisIsKey2';
    }
    testGetRandom() {
        let szlist = [1,4,8,16];
        for(let i = 0; i < szlist.length; i++) {
            let sz = szlist[i];
            let salt = cryptojs.lib.WordArray.random(sz);
            //debug(salt);
            // each word is 4B with min of 4B
            assert(salt.words.length === (sz < 4) ? 1 : (sz/4));
            assert(salt.length === undefined);
            assert(salt.sigBytes === sz);
        }
    }
    testAES() {
        // text
        {
            let encrypted = cryptojs.AES.encrypt(this.s1, this.key1).toString();
            // it HAS To be this!
            let decrypted = cryptojs.AES.decrypt(encrypted, this.key1).toString(cryptojs.enc.Utf8);
            assert(decrypted === this.s1);
            // this does NOT work!
            decrypted = cryptojs.AES.decrypt(encrypted, this.key1).toString();
            assert(decrypted !== this.s1);
        }
        // text
        {
            let key = cryptojs.enc.Utf8.parse(this.key1).toString(cryptojs.enc.Utf8);
            assert(key === this.key1);
            let encrypted = cryptojs.AES.encrypt(this.s1, key).toString();
            let decrypted = cryptojs.AES.decrypt(encrypted, key).toString(cryptojs.enc.Utf8);
            assert(decrypted === this.s1);
        }

        // binary
        {
            let base64String = Buffer.from(this.barray4).toString('base64');
            assert(base64String === 'ARAgQH+AyOb+/w==');
            let encrypted = cryptojs.AES.encrypt(base64String, this.key1).toString();
            let decrypted = cryptojs.AES.decrypt(encrypted, this.key1).toString(cryptojs.enc.Utf8);
            let buffer = Buffer.from(decrypted, 'base64');
            assert(buffer.join(',') === this.barray4.join(','));
        }
        {
            let base64String = Buffer.from(this.barray3).toString('base64');
            assert(base64String === 'AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/w==');
            let encrypted = cryptojs.AES.encrypt(base64String, this.key1).toString();
            let decrypted = cryptojs.AES.decrypt(encrypted, this.key1).toString(cryptojs.enc.Utf8);
            let buffer = Buffer.from(decrypted, 'base64');
            assert(buffer.join(',') === this.barray3.join(','));
        }
    }
    testSHA() {
        {
            let hashed = null, str = null, hashedUpdate

            hashed = cryptojs.SHA256(this.s1 + this.salt1);
            str = hashed.toString();
            assert(str === '5fd640f82d4b25411f7a6b2189cadd7fa0a34a00f269cd830d6a6ad4fe2c2271');

            hashed = cryptojs.SHA256(this.s1);
            str = hashed.toString();
            assert(str === 'b8259969151b69e2d6a7734652f5240104e18f3747ae6f1728de98787e936fad');

            // this doesnt work!!
            //str = hashed.toString(cryptojs.enc.Utf8);

            str = hashed.toString(cryptojs.enc.Base64);
            assert(str === 'uCWZaRUbaeLWp3NGUvUkAQThjzdHrm8XKN6YeH6Tb60=');
            str = hashed.toString(cryptojs.enc.Hex);
            assert(str === 'b8259969151b69e2d6a7734652f5240104e18f3747ae6f1728de98787e936fad');

            hashed = cryptojs.SHA512(this.s1).toString();

            hashedUpdate = cryptojs.algo.SHA256.create();
            hashedUpdate.update(this.s1);
            hashed = hashedUpdate.finalize();
            str = hashed.toString();
            assert(str === 'b8259969151b69e2d6a7734652f5240104e18f3747ae6f1728de98787e936fad');

            hashedUpdate = cryptojs.algo.SHA256.create();
            hashedUpdate.update(this.s1);
            hashedUpdate.update(this.s2);
            hashed = hashedUpdate.finalize();
            str = hashed.toString();
            assert(str === 'b412cc48637bf05c85489f0e5fa5b645470d941a9d207b74e747dc1afbac52d3');

            hashedUpdate = cryptojs.algo.SHA256.create();
            hashedUpdate.update(this.s2);
            hashedUpdate.update(this.s1);
            hashed = hashedUpdate.finalize();
            str = hashed.toString();
            assert(str === 'c76801d0345785aed34aae257c7a8160d9d4a2ff7108aa4f874e49ff8850e037');

        }
    }
    testAsymmetric() {
    }

    testBase64() {

    }
    testZip() {

    }
    testGzip() {

    }
    testBuffer() {

    }
    testArrayVsArrayBuffer() {
        {
            let array = new Array();
            array.push('apple');
            array.push('orange');
            array.push('banana');
            assert(array.length === 3);
            assert(array.shift() === 'apple');
            assert(array.pop() === 'banana');
        }
        {
            // cannot do anything with this
            let arrayBuffer = new ArrayBuffer();
            let arrayWords = cryptojs.lib.WordArray.random(16);
            let buffer = Buffer.from(arrayWords.words);
            let uint8ArrayOf = Uint8Array.of(arrayWords.words);
            let uint16ArrayOf = Uint16Array.of(arrayWords.words);
            let uint32ArrayOf = Uint32Array.of(arrayWords.words);
            let s8Of = uint8ArrayOf.toString('base64');
            let s16Of = uint16ArrayOf.toString('base64');
            let s32Of = uint32ArrayOf.toString('base64');
            let uint8ArrayFrom = Uint8Array.from(arrayWords.words); // truncates!
            let uint16ArrayFrom = Uint16Array.from(arrayWords.words); // truncates!
            let uint32ArrayFrom = Uint32Array.from(arrayWords.words); // truncates!
            let int8ArrayFrom = Int8Array.from(arrayWords.words);
            let int16ArrayFrom = Int16Array.from(arrayWords.words);
            let int32ArrayFrom = Int32Array.from(arrayWords.words);
            let s8From = uint8ArrayFrom.toString('base64');
            let s16From = uint16ArrayFrom.toString('base64');
            let s32From = uint32ArrayFrom.toString('base64');

            for(let i = 0; i < arrayWords.words.length; i++) {
                let word = arrayWords.words[i];
                if(word & 0xffff_ffff === word) {
                    if(word < 0) {
                        assert(int32ArrayFrom[i] !== word);
                        assert(uint32ArrayFrom[i] === word);
                    } else {
                        assert(int32ArrayFrom[i] === word);
                        assert(uint32ArrayFrom[i] === word);
                    }
                    assert(uint16ArrayFrom[i] !== word);
                    assert(uint8ArrayFrom[i] !== word);
                    assert(int16ArrayFrom[i] !== word);
                    assert(int8ArrayFrom[i] !== word);
                }
                else if(word & 0xffff === word) {
                    assert(uint16ArrayFrom[i] === word);
                }
                else if(word & 0xff === word) {
                    assert(uint8ArrayFrom[i] === word);
                }
            }
            /*
            debug(arrayWords.words);
            debug(buffer);
            debug(uint8ArrayFrom);
            debug(uint16ArrayFrom);
            debug(uint32ArrayFrom);
            debug(int8ArrayFrom);
            debug(int16ArrayFrom);
            debug(int32ArrayFrom);
            */

            assert(uint8ArrayOf.join('') === '0');
            assert(uint16ArrayOf.join('') === '0');
            assert(uint32ArrayOf.join('') === '0');
            assert(s8Of === '0');
            assert(s16Of === '0');
            assert(s32Of === '0');
        }
        {
            let words = [0x12_23_34_45,0x22_33_44_55,0x66_77_88_99];
            let buffer = Buffer.from(words); // truncates!
            let uint8ArrayFrom = Uint8Array.from(words); // truncates!
            let uint16ArrayFrom = Uint16Array.from(words); // truncates!
            let uint32ArrayFrom = Uint32Array.from(words); // 
            for(let i = 0; i < buffer.length; i++) {
                assert(buffer[i] === (words[i] & 0xff));
                assert(buffer[i] !== words[i] & 0xff);
                assert(uint16ArrayFrom[i] === (words[i] & 0xffff));
                assert(uint32ArrayFrom[i] === words[i]);
            }
        }
        {
            // wrong way!
            let uint8Array = Uint8Array.from(this.s1);
            let expected = [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5,
                6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0
              ];
            assert(uint8Array.length === expected.length);
            for(let i = 0; i < expected.length; i++) {
                assert(uint8Array[i] === expected[i]);
            }

            // right way!
            let textEncoded = new TextEncoder('utf-8').encode(this.s1);
            expected = [
                65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,
                77,  78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,
                89,  90,  10,  97,  98,  99, 100, 101, 102, 103, 104, 105,
               106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117,
               118, 119, 120, 121, 122,  10,  48,  49,  50,  51,  52,  53,
                54,  55,  56,  57,  10,  33,  64,  35,  36,  37,  94,  38,
                42,  40,  41, 123, 125,  91,  93,  60,  62
             ];
             uint8Array = Uint8Array.from(textEncoded);
             assert(uint8Array.length === expected.length);
             for(let i = 0; i < expected.length; i++) {
                 assert(uint8Array[i] === expected[i]);
             }
             let textDecoded = new TextDecoder('utf-8').decode(uint8Array);
             assert(textDecoded === this.s1);
             textDecoded = new TextDecoder('utf-8').decode(textEncoded);
             assert(textDecoded === this.s1);
        }
        {
            let buffer = null, str = null;

            buffer = Buffer.from(this.s4);
            assert(buffer.join(',') === '72,101,108,108,111,32,87,111,114,108,100,33');

            buffer = Buffer.from(this.s4).toString();
            assert(buffer === this.s4);

            buffer = Buffer.from(this.s4).toString('utf8');
            assert(buffer === this.s4);

            buffer = Buffer.from(this.s4).toString('hex');
            assert(buffer === '48656c6c6f20576f726c6421')
            str = Buffer.from(buffer, 'hex').toString();
            assert(str === this.s4);

            buffer = Buffer.from(this.s4).toString('base64');
            assert(buffer === 'SGVsbG8gV29ybGQh');
            str = Buffer.from(buffer, 'base64').toString();
            assert(str === this.s4);
        }
    }
    testCryptoBuffer() {
        {
            let buffer = null, str = null;

            buffer = Buffer.from(this.s4);
            assert(buffer.join(',') === '72,101,108,108,111,32,87,111,114,108,100,33');

            buffer = Buffer.from(this.s4).toString();
            assert(buffer === this.s4);

            buffer = Buffer.from(this.s4).toString('utf8');
            assert(buffer === this.s4);

            buffer = Buffer.from(this.s4).toString('hex');
            assert(buffer === '48656c6c6f20576f726c6421')
            str = Buffer.from(buffer, 'hex').toString();
            assert(str === this.s4);

            buffer = Buffer.from(this.s4).toString('base64');
            assert(buffer === 'SGVsbG8gV29ybGQh');
            str = Buffer.from(buffer, 'base64').toString();
            assert(str === this.s4);
        }
        {
            let buffer = null, str = null, wordArray = null;

            wordArray = cryptojs.enc.Utf8.parse(this.s4);

            str = wordArray.words.join(',');
            assert(str === '1214606444,1864390511,1919706145');

            str = wordArray.toString();
            assert(str === '48656c6c6f20576f726c6421');
            str = cryptojs.enc.Hex.parse(str).toString(cryptojs.enc.Utf8);
            assert(str === this.s4);

            str = wordArray.toString(cryptojs.enc.Base64);
            assert(str === 'SGVsbG8gV29ybGQh'); // see Buffer.from version

            str = this.barray4.toString();
            assert(str === '1,16,32,64,127,128,200,230,254,255');
            // base64 doesnt work!
            str = this.barray4.toString('base64');
            assert(str === '1,16,32,64,127,128,200,230,254,255');
            str = Buffer.from(this.barray4).join(',');
            assert(str === '1,16,32,64,127,128,200,230,254,255');
            // base64 does work!
            str = Buffer.from(this.barray4).toString('base64');
            assert(str === 'ARAgQH+AyOb+/w==');

            // binary array to base64 back to binary array
            str = Buffer.from(this.barray4).toString('base64');
            assert(str === 'ARAgQH+AyOb+/w==');
            buffer = Buffer.from(str, 'base64');
            str = buffer.join(',');
            assert(str === '1,16,32,64,127,128,200,230,254,255');
            assert(str === this.barray4.join(','));

            // string or array to base64 back to string
            buffer = Buffer.from(this.s4);
            assert(this.s4 === 'Hello World!')
            str = buffer.join(',');
            assert(str === '72,101,108,108,111,32,87,111,114,108,100,33')
            str = Buffer.from(buffer).toString('base64');
            assert(str === 'SGVsbG8gV29ybGQh');
            str = buffer.toString();
            assert(str === 'Hello World!');
            str = buffer.toString('base64');
            assert(str === 'SGVsbG8gV29ybGQh');
            buffer = Buffer.from(str, 'base64');
            str = buffer.toString();
            assert(str === 'Hello World!');

        }
    }
    testGenerateBytes() {
        let ba = [];
        for(let i = 0; i < 256; i++) {
            ba[i] = i;
        }
        //debug(ba.join(','));
    }
    test() {
        /*
        this.testBase64();
        this.testZip();
        this.testGzip();
        this.testBuffer();
        this.testGetRandom();
        this.testArrayVsArrayBuffer();
        this.testGenerateBytes();
        this.testCryptoBuffer();
       this.testAES();
       this.testSHA();
        */
       this.testAsymmetric();
    }
}

var t = new Test();
t.test();
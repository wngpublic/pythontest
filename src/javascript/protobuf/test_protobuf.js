// not needed
const goog = require('google-closure-library');
// not needed
const protobuf = require('protobufjs');             

const message = require('./protobuf_lib/message-t1_pb.js')
const assert = require('assert');
const { SSL_OP_NO_TLSv1_1 } = require('constants');

class Test {
    debug = true;
    test1() {
        const t1 = new message.Test1();
        t1.setId(100);
        t1.setIval2(20);
        const t1Inner = new message.Test1.InnerTest1();
        t1Inner.setId(200);
        t1Inner.setSval1('hello world');
        t1.setInnert1(t1Inner);
        assert(t1.getId() == 100);
        assert(t1Inner.getId() == 200);

        let serializedData = t1.serializeBinary();
        let deserializedData = message.Test1.deserializeBinary(serializedData);

        assert(deserializedData.getId() == 100);
        let t1InnerDS = deserializedData.getInnert1();
        assert(t1InnerDS.getId() == 200);
        assert(t1InnerDS.getSval1() === 'hello world');

        // convert to object then convert to JSON
        let dataObject = t1.toObject();
        let dataString = JSON.stringify(dataObject);
        let dataJSON = JSON.parse(dataString);          // doesnt seem to be needed
        assert(typeof dataObject === 'object');
        assert(typeof dataJSON === 'object');
        assert(dataObject['id'] === 100);
        assert(dataObject['innert1']['id'] === 200);
        assert(dataJSON['id'] === 100);
        assert(dataJSON['innert1']['id'] === 200);
        assert(dataString === '{"id":100,"rivalList":[],"ival2":20,"rsvalList":[],"innert1":{"id":200,"rivalList":[],"sval1":"hello world","rsvalList":[]},"rinnertList":[]}');

        const t2 = t1.cloneMessage();
        assert(t1.getId() == t2.getId());
    }
    test() {
        this.test1();
    }
}

const t = new Test();
t.test();
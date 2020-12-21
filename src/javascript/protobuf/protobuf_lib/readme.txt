protobuf

protoc --js_out=./ in.proto
protoc --java_out=./ in.proto
protoc --decode

// do this instead, the --js_out by itself does not work
protoc message-t1.proto --js_out=import_style=commonjs,binary:.

- get error:    goog.provide(
    npm i protobufjs --save // this works
    npm i protobufjs -g     // this will not work
    npm i google-closure-library --save
    npm i google-protobuf --save
    npm i @grpc/proto-loader --save // for directly loading *.proto defs
    npm i grpc --save       // for server

    after installing these, just include the require
    const proto = require('./protobuf_lib/message-t1_pb.js')


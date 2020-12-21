const grpc = require('grpc');
const protoLoader = require('@grpc/proto-loader');
const messaget1 = grpc.load('./protobuf_lib/message-t1.proto');
const pkgDef = protoLoader.loadSync(
    './protobuf_lib/message-t1.proto'
);
const testProto = grpc.loadPackageDefinition(pkgDef).Test1;
const PORT = 5050;
const server = new grpc.Server();
server.bind(
    `localhost: ${PORT}`, 
    grpc.ServerCredentials.createInsecure());
// proto uses service call, which i do not want. i only want basic data structure,
// so i may not be able to use service call.
//server.addService(); 
server.start();
const express = require('express');
const ws = require('ws');
const expressws = require('express-ws');
const app = express();
const PORT_WS = 3001;
const PORT_HTTP = 8001;
const server = app.listen(PORT_HTTP);
const wss = new ws.Server({
    server: server,
    path: '/ws'
});

wss.on('connection', socket => {
    socket.on('message', message => console.log(message))
});



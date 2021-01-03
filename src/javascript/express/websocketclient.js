const ws = require('ws');
const PORT = 3001;
const client = new ws(`ws://localhost:${PORT}`);
client.on('open', () => client.send('hello'));
npm install -> creates package-lock.json and node_modules

node handle_https.js

curl -H 'Accept:application/json' -H 'Content-type:application/json' -d '{"k1":"v1","k2":["123","23"]}' 'http://localhost:8080/postjson'

curl -k -H 'Accept:application/json' -H 'Content-type:application/json' -d '{"k1":"v1","k2":["123","23"]}' 'https://localhost:8443/postjson'

// -k is for insecure connection, because self signed certificate


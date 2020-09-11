git push https://<username>@github.com/<username>/<project>.git

export FLASK_APP=myserver.py
flask run


curl http:/127.0.0.1:5000/arg/something
curl http:/127.0.0.1:5000/arg2/1234/term
curl 'http:/127.0.0.1:5000/argparams?p1=yo&p2=hi&p3=what'
curl -H 'Content-Type:application/json' -H 'accept:application/json' -d '{"k1":"v1","k2":"v2"}' 'http:/127.0.0.1:5000/argjson'
curl -v -H 'Content-Type:application/json' -H 'accept:application/json' -d '{"k1":"v1","k2":"v2","wait":2000}' 'http:/127.0.0.1:5000/statusjson/200/jsonwait'


import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('foo','bar')
r.get('foo')

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
r = redis.Redis(unix_socket_path='/tmp/redis.sock')
pool = redis.ConnectionPool(connection_class=YourConnectionClass,our_arg='...', ...)

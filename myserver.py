#!/usr/local/bin/python3

import flask
import json
import time

app = flask.Flask(__name__)

def p(s):
    print(s)

@app.route('/hello')
def hello():
    return 'hello world\n'

@app.route('/bye')
def bye():
    return 'bye bye\n'

@app.route('/arg/<string:id>')
def arg(id):
    return 'called arg {}\n'.format(id)

@app.route('/arg/<int:id>')
def argint(id):
    return 'called argint {}\n'.format(id)

@app.route('/arg2/<string:id>/term')
def arg2(id):
    return 'called arg2 {}\n'.format(id)

# argparams p1=str,p2=str,p3=str
@app.route('/argparams', methods=['GET','POST'])
def argparams():
    p1 = flask.request.args.get('p1', default='DEFAULT1')
    p2 = flask.request.args.get('p2', default=None)
    p3 = flask.request.args.get('p3', default=None)
    ret = 'p1:{} p2:{} p3:{}'.format(p1,p2,p3)
    p(ret)
    return ret + '\n'

@app.route('/argjson', methods=['POST'])
def argjson():
    content = flask.request.get_json()
    ret = '{}'.format(json.dumps(content, indent=2))
    p(ret)
    return ret + '\n'

@app.route('/statuscode/<int:statusval>/justreturn', methods=['GET','POST'])
def statuscode(statusval):
    return flask.Response('called statuscode {}\n'.format(statusval),status=statusval)

@app.route('/statuscode/<int:statusval>/json', methods=['GET','POST'])
def statuscodejson(statusval):
    content = flask.request.get_json()
    ret = '{}'.format(json.dumps(content, indent=2))
    return flask.Response('called statuscode {}\n'.format(ret),status=statusval,mimetype='application/json')

@app.route('/statusjson/<int:statusval>/jsonwait', methods=['GET','POST'])
def statuscodejsonwait(statusval):
    content = flask.request.get_json()
    if content is None:
        p('content is none')
        return flask.Response(status=statusval)
    else:
        ret = '{}'.format(json.dumps(content, indent=2))
        waitperiod = content.get('wait')
        if waitperiod is not None:
            waitperiod = float(waitperiod/1000)
            p('wait for {} seconds'.format(waitperiod))
            time.sleep(waitperiod)
    return flask.Response('called statuscode {}\n'.format(ret),status=statusval,mimetype='application/json')

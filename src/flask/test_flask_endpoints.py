import flask
import sqlalchemy
import json
import time

'''

- dir structure
-- templates
-- static: css, js, png
-- modules: custom code for endpoints
-- venv
    virtualenv venv
    source venv/bin/activate
    deactivate

'''

app = flask.Flask(__name__)

def p(s):
    print(s)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/test_sql')
def test():
    return 'Test SQL'

@app.route('/timeout-endpoint')
def timeout_endpoint():
    time.sleep(0.5) # sleep 500 ms
    return 'slept for 500 ms'

@app.route('/echo/<string:val>/')
def get_string_echo(val):
    app.logger.debug('get_string_echo {}'.format(val))
    return val

@app.route('/echo/<string:val>/path2')
def get_string_echo_2(val):
    return val

@app.route('/read-cookie')
def get_read_cookie():
    d = flask.request.cookies
    p('read-cookie:{}'.format(d))
    return flask.jsonify(d)

@app.route('/set-cookie')
def get_set_cookie():
    d = flask.request.cookies
    p('set-cookie:{}'.format(d))
    response = flask.make_response(flask.jsonify(d))
    response.set_cookie("rk1","rv1")
    response.set_cookie("rk2","rv2")
    response.set_cookie("rk3","rv3",path='/cookies')
    '''
    #response.set_cookie("rk4","rv4",path='/cookies',domain='localhost')
    exception because localhost is not valid, need to have hosts file to point to dns name, eg dev.localhost
    '''
    return response


@app.route('/post-params-echo', methods=['POST'])
def post_params_echo():
    params = flask.request.args
    result = json.dumps(params)
    #p('post-params {}'.format(result))
    return flask.jsonify(params)

@app.route('/post-json-echo', methods=['POST'])
def post_json_echo():
    return flask.jsonify(flask.request.json)

@app.route('/get-json-echo', methods=['GET'])
def get_json_echo():
    return flask.jsonify(flask.request.json)

@app.route('/get-or-post-json-echo', methods=['GET','POST'])
def get_or_post_json_echo():
    if flask.request.method == 'GET':
        #p('get_or_post_json_echo GET {}'.format(flask.request.json))
        return jsonify(flask.request.json)
    elif flask.request.method == 'POST':
        #p('get_or_post_json_echo POST {}'.format(flask.request.json))
        return flask.jsonify(flask.request.json)

if __name__ == "__main__":
    app.run(debug=True, port=8123) # default is port 5000

# run as python3 test_flask_endpoints.py and go to http://localhost:8123
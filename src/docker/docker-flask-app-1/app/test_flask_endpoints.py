import flask
from flask import request
from flask import render_template
import json
import time
import json
import random
import datetime
import calendar
import sqlite3
import os
import mysql.connector
import sys

'''
run as python3 test_flask_endpoints.py

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
app.config.from_pyfile('flask_config.py')
TEST_USER = app.config.get('TEST_USER')
TEST_PW = app.config.get('TEST_PW')

#if TEST_USER == None or TEST_PW == None:
#    sys.exit("no env user or pw, failed")
#else:
#    app.logger.debug('test_usr:{} and pw defined in env'.format(TEST_USER,TEST_PW))

#print('{}'.format(app.config))
#print('config TESTING:{}'.format(app.config.get('TESTING')))
#print('config DB_USERNAME:{}'.format(app.config.get('DB_USERNAME'))) # loaded from config.py

# you have to have test2_db with username and password enabled on mysql for this startup
MYSQL_HOST = app.config.get('MYSQL_HOST')
MYSQL_DBNAME = app.config.get('MYSQL_DBNAME')
#MYSQL_CONN   = None # mysql.connector.connect(host=MYSQL_HOST,database=MYSQL_DBNAME,user=TEST_USER,password=TEST_PW)
#MYSQL_CURSOR = MYSQL_CONN.cursor()
SQLITE_DB = app.config.get('SQLITE_DATABASE')
#SQLITE_CONN = sqlite3.connect(SQLITE_DB)

def get_db_sqlite():
    if 'db' not in flask.g:
        flask.g.db = sqlite3.connect(SQLITE_DB)
        return flask.g.db

# this needs to be set for every write to db
def db_sqlite_commit():
    conn = get_db_sqlite()
    cursor = conn.cursor()
    cursor.commit()

def get_db_mysql():
    return MYSQL_CONN

def close_db_mysql():
    if MYSQL_CONN != None and MYSQL_CONN.is_connected():
        MYSQL_CONN.close()

def close_db_sqlite():
    if 'db' in flask.g:
        conn = None
        try:
            conn = flask.g.db
            cursor = conn.cursor()
            cursor.close()
        except Exception as e:
            app.logger.debug('close_db_sqlite error ' + e)
        finally:
            if conn != None:
                conn.cursor.close()

def p(s):
    print(s)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/index')
def load_template_javascript():
    t = get_time()
    d = {}
    d['time'] = t
    return flask.render_template("test_template_javascript.html",date=d)

@app.route('/time_call')
def get_time():
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return t

@app.route('/test_html')
def test_html():
    d = {
        'v1':'v1value',
        'v2':'v2value'
    }
    app.logger.debug("test_html")
    # passing in a dict does not work, use v1,v2
    #return flask.render_template("test_html.html",d)
    return flask.render_template("test_html.html",v1='v1value',v2='v2value')

@app.route('/test_template_html')
def test_template_html():
    app.logger.debug("test_template_html")
    return flask.render_template("test_template.html",name='joe',v1='not sure')

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
    return "0: " + val

@app.route('/echo/<string:val>/path2')
def get_string_echo_2(val):
    return "0: " + val

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

@app.route('/form_1', methods=['GET','POST'])
def form_1():
    cb1 = None
    cb2 = None
    cb3 = None
    if request.method == 'POST':
        tb1 = request.form['id-textbox-1']
        tb2 = request.form['id-textbox-2']
        cbsingle = request.form.get('name-cb-1')
        cbl = request.form.getlist('name-cb-1')
        namecb1 = None
        if 'name-cb-1' in request.form:
            namecb1 = request.form['name-cb-1']
        for cb in cbl:
            if cb == 'cb1':
                cb1 = cb
            if cb == 'cb2':
                cb2 = cb
        debugstr = 'cbsingle:{},{},form:{},cblist:{}'.format(cbsingle,namecb1,request.form,cbl)
        resultstr = 'POST method: {}'.format(debugstr)
        app.logger.debug(resultstr)

        cbredirect = request.form.getlist('name-cb-redirect')
        if len(cbredirect) != 0:
            postcode = 307  # redirect post
            postcode = 302  # redirect get
            params1 = 'abc=123&cde=234'
            params2 = 'v1=222&v2=333'

            # cannot post with json data, but maybe with params?
            return flask.redirect(flask.url_for('form_1_redirect',arg1=params1,arg2=params2), code=postcode)

        cbv = request.form.getlist('name-cb-3')
        if len(cbv) != 0:
            print('cbv:{}'.format(cbv))
            #app.logger.debug('cbv:{}'.format(cbv))
            cb3 = 'checked'
            # all fields get preserved
            return render_template('test_form_refresh.html',title='Test Form Refresh',vid_tb1=tb1,vid_tb2=tb2,cb1=cb1,cb2=cb2,cb3=cb3,result_text=resultstr)
        else:
            # no fields get preserved
            return render_template('test_form_refresh.html',title='Test Form Refresh',cb1=None,cb2=None,cb3=None,result_text=resultstr)
    else:
        # no fields set
        return render_template('test_form_refresh.html',title='Test Form Refresh',cb1=cb1,cb2=cb2,cb3=None,result_text='GET method')

@app.route('/form_1_redirect', methods=['GET','POST'])
def form_1_redirect():
    params = flask.request.args
    #jsonval = json.dumps(params)   # i dont think params are json
    resultstr='redirect jsonval = {}'.format(params)
    if request.method == 'POST':
        return render_template('redirect_generic.html',title='Redirected POST',status_text=resultstr)
    else:
        return render_template('redirect_generic.html',title='Redirected GET',status_text=resultstr)


@app.route('/upload_data_sqlite', methods=['GET','POST'])
def form_upload_data_sqlite():
    pass

@app.route('/query_data_sqlite', methods=['GET','POST'])
def form_query_data_to_table_sqlite():
    conn = get_db_sqlite()
    pass


@app.route('/upload_data_mysql', methods=['GET','POST'])
def form_upload_data_mysql():
    pass

@app.route('/query_data_mysql', methods=['GET','POST'])
def form_query_data_to_table_mysql():
    sql_query = 'select * from test_table limit 1000'
    #MYSQL_CURSOR.execute(sql_query)
    #data = MYSQL_CURSOR.fetchall()
    #if data != None:
    #    for row in data:
    #        pass
    pass

@app.route('/test_query_sqlite_1', methods=['GET'])
def test_query_sqlite_1():
    conn = get_db_sqlite()
    cursor = conn.cursor()
    sql = 'select * from test_table_1 limit 10'
    cursor.execute(sql)
    rows = cursor.fetchall()
    response = ''
    for row in rows:
        response = response + '<tr><td>' + row + '<td></tr>'
    return response

@app.route('/test_query_mysql_1', methods=['GET'])
def test_query_mysql_1():
    conn = get_db_mysql()
    cursor = conn.cursor()
    sql = 'select * from test_table_1 limit 10'
    cursor.execute(sql)
    rows = cursor.fetchall()
    response = ''
    for row in rows:
        response = response + '<tr><td>' + row + '<td></tr>'
    return response

@app.before_first_request
def activate_job():
    pass

@app.cli.command('initdb')
def initdb():
    pass

@app.route('/form_2_js', methods=['GET','POST'])
def form_2_js():
    pass

if __name__ == "__main__":
    #app.run(debug=True, port=8123) # default is port 5000
    app.run(debug=True, host='0.0.0.0', port=8123) # default is port 5000

# run as python3 test_flask_endpoints.py and go to http://localhost:8123

import requests
import requests_html
import json
import bs4
import csv
import re

'''
- how to use http connection pooling?
- how to use http connection timeout?
- how to keep alive?
- sessions?
- cookie put and get?
- streaming?
- chunked?


'''

'''
bs4 has the following properties
  tag
    name        tag.name
    attrs       tag.attrs
                tag.attrs.get('fieldkey')
    string      tag.string  text within tag
    head        tag.head    usually for soup.head
    title       tag.title   usually for soup.title
    text        tag.text
                tag.text            if there is text
    contents    tag.contents[x]    all the tag's children
    children    tag.children[x]     len(list(tag.children))
    descendants tag.descendants[x]  len(list(tag.descendants)) # all subchildren too
    parent      immediate parent
    parents     all parents up the chain
    next_sibling
    previous_sibling
    next_siblings
    previous_siblings
    next_element
    next_elements   sometimes it's siblings, mostly something else
methods
  find_all
  find_all(re.compile("*"))
  find_all([listvals])
  find_all(id="x")
  find_all("tag","classval")    find_all("td","x")
  find_all(attrs={"key":"val"}) find_all(attrs={"div":"val"})
  prettify
'''

def p(s):
    print(s)
def br():
    p('-----breaker-----')

class TestRequests:
    def print_response_json(self, response):
        r = response
        p('url:{}'.format(r.url))
        p('status_code:{}'.format(r.status_code))
        p('headers:{}'.format(r.headers))
        p('json:{}'.format(r.json()))
        p('text:{}'.format(r.text))
    def print_response_text(self, response):
        r = response
        p('url:{}'.format(r.url))
        p('status_code:{}'.format(r.status_code))
        p('headers:{}'.format(r.headers))
        p('text:{}'.format(r.text))
    def test_localhost_flask_json_post(self):
        data_json = {"k1":"v1","k2":"v2","k3":{"k3.1":"v3.1","k3.2":"v3.2"}}
        data_headers = {'Content-Type':'application/json','Accept':'text/plain'}
        r = requests.post('http://localhost:8123/get-or-post-json-echo',json=data_json,headers=data_headers)
        p('url:{}'.format(r.url))
        p('status_code:{}'.format(r.status_code))
        p('headers:{}'.format(r.headers))
        p('json:{}'.format(r.json()))
        p('text:{}'.format(r.text))
    def test_localhost_flask_data_json_post(self):
        data_json = {"k1":"v1","k2":"v2","k3":{"k3.1":"v3.1","k3.2":"v3.2"}}
        data_headers = {'Content-Type':'application/json','Accept':'text/plain'}
        r = requests.post('http://localhost:8123/get-or-post-json-echo',data=json.dumps(data_json),headers=data_headers)
        p('url:{}'.format(r.url))
        p('status_code:{}'.format(r.status_code))
        p('headers:{}'.format(r.headers))
        p('json:{}'.format(r.json()))
        p('text:{}'.format(r.text))
    def test_localhost_flask_param_post(self):
        #data_param = {"k1":"v1","k2":"v2","k3":{"k3.1":"v3.1","k3.2":"v3.2"}}
        data_param = {"k1":"v1","k2":"v2","k3":"v3"}
        data_headers = {'Content-Type':'application/json','Accept':'text/plain'}
        r = requests.post('http://localhost:8123/post-params-echo',params=data_param,headers=data_headers)
        p('url:{}'.format(r.url))
        p('status_code:{}'.format(r.status_code))
        p('headers:{}'.format(r.headers))
        p('json:{}'.format(r.json()))
        p('text:{}'.format(r.text))
    def test_localhost_flask_hello_world(self):
        r = requests.get('http://localhost:8123/') # not post!
        p('status_code:{}'.format(r.status_code))
        p('text:{}'.format(r.text))
    def test_localhost_flask_echo_string(self):
        r = requests.get('http://localhost:8123/echo/something123') # not post!
        p('status_code:{}'.format(r.status_code))
        p('text:{}'.format(r.text))
    def test_localhost_flask_echo_string_2(self):
        r = requests.get('http://localhost:8123/echo/something1234/path2') # not post!
        p('status_code:{}'.format(r.status_code))
        p('text:{}'.format(r.text))
    def test_localhost_cookie_get(self):
        jar = requests.cookies.RequestsCookieJar()
        jar.set('v1','v2',domain='something1.org',path='/cookies')
        jar.set('v3','v4',domain='something2.org',path='/cookies') # must be 2 positional args
        jar.set('v5','v6')
        jar.set('v7','v8',path='/cookies')
        jar.set('v9','va')
        jar.set('x1','x2',domain='localhost')
        jar.set('x3','x4',domain='localhost',path='/cookies')
        r = requests.get('http://localhost:8123/read-cookie',cookies=jar)
        p('url:{}'.format(r.url))
        p('status_code:{}'.format(r.status_code))
        p('headers:{}'.format(r.headers))
        p('json:{}'.format(r.json()))
        p('text:{}'.format(r.text))
    def test_localhost_cookie_set(self):
        jar = requests.cookies.RequestsCookieJar()
        jar.set('v1','v2',domain='something1.org',path='/cookies')
        jar.set('v3','v4',domain='something2.org',path='/cookies') # must be 2 positional args
        jar.set('v5','v6')
        jar.set('v7','v8',path='/cookies')
        jar.set('v9','va')
        jar.set('x1','x2',domain='localhost')
        jar.set('x3','x4',domain='localhost',path='/cookies')
        r = requests.get('http://localhost:8123/set-cookie',cookies=jar)
        p('url:{}'.format(r.url))
        p('status_code:{}'.format(r.status_code))
        p('headers:{}'.format(r.headers))
        p('json:{}'.format(r.json()))
        p('text:{}'.format(r.text))
    def test_localhost_flask_endpoint_timeout_1(self):
        try:
            r = requests.get('http://localhost:8123/timeout-endpoint',timeout=0.1)
            p('status_code:{}'.format(r.status_code))
            p('text:{}'.format(r.text))
        except requests.exceptions.ReadTimeout as e:
            p(e)
    def test_localhost_flask_endpoint_timeout_2(self):
        try:
            r = requests.get('http://localhost:8123/timeout-endpoint',timeout=1)
            p('status_code:{}'.format(r.status_code))
            p('text:{}'.format(r.text))
        except requests.exceptions.ReadTimeout as e:
            p(e)
    def test_localhost_flask_endpoint_timeout_3(self):
        try:
            r = requests.get('http://localhost:8123/timeout-endpoint')
            p('status_code:{}'.format(r.status_code))
            p('text:{}'.format(r.text))
        except requests.exceptions.ReadTimeout as e:
            p(e)
    def test_localhost(self):
        t = self
        p("------")
        t.test_localhost_flask_json_post()
        p("------")
        t.test_localhost_flask_data_json_post()
        p("------")
        t.test_localhost_flask_hello_world()
        p("------")
        t.test_localhost_flask_echo_string()
        p("------")
        t.test_localhost_flask_echo_string_2()
        p("------")
        t.test_localhost_flask_param_post()
        p("------")
        t.test_localhost_cookie_get()
        p("------")
        t.test_localhost_cookie_set()
        p("------")
        t.test_localhost_flask_endpoint_timeout_1()
        p("------")
        t.test_localhost_flask_endpoint_timeout_2()
        p("------")
        t.test_localhost_flask_endpoint_timeout_3()
        p("------")
    def test_requests_sessions(self):
        '''
        once you login with auth, you can use sessions object to continue making requests, instead
        of passing user/pass to each request
        '''
        url = None
        session = requests.Session()
        response = session.get(url)
        response = session.get(url)
        response = session.get(url)
        pass
    def test_parse_url(self):
        # TODO: remove url
        url = None
        #url = 'https://www.<>.com'
        response = requests.get(url)
        self.print_response_text(response)
        #soup = bs4.BeautifulSoup
    def test_parse_url_with_javascript(self):
        url = ''
        session = requests_html.HTMLSession()
        response = session.get(url)
        response.html.render()
        p(response.text)
        #soup = bs4.BeautifulSoup
    def test_parse_bs4_with_file_1(self):
        filename = '../../tmp_output/1.html'
        soup = bs4.BeautifulSoup(open(filename), features="lxml")   # you HAVE to specify parser, lxml is fast, is l for lenient xml?
        p(soup.prettify())
        p('------------------------')
        soup = bs4.BeautifulSoup(open(filename), features="xml")   # you HAVE to specify parser, this is from lxml, assuming non lenient?
        p(soup.prettify())
        p('------------------------')
        soup = bs4.BeautifulSoup(open(filename), features='html.parser')    # this is default parser, keeps track of line number
        p(soup.prettify())
        p('------------------------')
        soup = bs4.BeautifulSoup(open(filename), features='html5lib') # slow but emulates browser
        p(soup.prettify())
        p('------------------------')
    def test_parse_bs4_with_file_parse_fields(self):
        filename = '../../tmp_output/1.html'
        soup = bs4.BeautifulSoup(open(filename), features="lxml")   # you HAVE to specify parser
        res = soup.find_all('tbody')
        assert isinstance(res,list)
        p("------breaker-----")
        p('size:{}'.format(len(res)))
        p("------breaker-----")
        #p(res[22])                  # the 22nd tag with tbody
        p("------breaker-----")
        cnt = 0
        d = {}
        vset = set()
        buf_output = []
        for parent in res[22].parents:      # all the parents up to html
            if parent is None:
                buf_output.append('{:2}: parent is NONE:{}'.format(cnt, parent))
            else:
                attrs = list(parent.attrs)
                if 'class' in attrs:
                    buf_output.append('{:2}: parent is ATTRS T1:{};{}'.format(cnt, parent.name,attrs))      # prints div|table|html
                    for attr in attrs:
                        if attr == 'class':
                            v = parent.attrs.get('class')
                            # can be indexed, eg <div class="val0 val1 val2">, so parent.attrs.get('class')[1] == val1 if exists
                            vals = ' '.join(v)
                            buf_output.append('    attr:{};class_val={}'.format(attr,vals))
                            text = parent.text
                            text_stripped = re.sub(r'\n+','\n',text)
                            if vals in vset:
                                buf_output.append('{} is already in vset'.format(vals))
                                d[vals] = text_stripped
                            else:
                                vset.add(vals)
                                d[vals] = text_stripped
                            '''
                            if text is None:
                                p('    textEMPTY:{}'.format(text))
                            else:
                                p('    text:{}'.format(text))
                            '''
                else:
                    buf_output.append('{:2}: parent is ATTRS T2:{};{}'.format(cnt, parent.name,attrs))      # prints div|table|html
            cnt += 1
        #p(buf_output)
        p("------breaker-----")
        res = soup.find_all('table',attrs={'class':'data-table'})
        buf_output = []
        for r in res:
            buf_output.append(r)
            buf_output.append("------breaker_small-----")
        #p(buf_output)
        p("------breaker-----")

        # todo DELETE THIS
        class_tag_val = ''
        h3_tag_val = ''

        filtered_tags = soup.find_all('div', {'class': lambda tag: tag == class_tag_val})
        #filtered_tags = soup.find_all(lambda tag: tag == class_tag_val, 'h3': h3_tag_val})
        #filtered_tags = soup.find_all(text=lambda text: text == h3_tag_val)
        filtered_tags = soup.find_all(h3_tag_val,string=h3_tag_val) # wrong
        filtered_tags = soup.find_all(h3_tag_val) # wrong because find all with tags "string search val" is wrong

        #filtered_tags = soup.find_all(tag=lambda tag: tag.attrs['class'] == class_tag_val)
        #filtered_tags = soup.find_all(lambda tag:  tag.name == 'div' and tag.has_attr('class') and tag.string == class_tag_val)
        #filtered_tags = soup.find_all('h3',text=re.compile(h3_tag_val)) # doesnt work
        filtered_tags = soup.find_all(lambda tag: tag.name == 'a')
        filtered_tags = soup.find_all('div', {'class': lambda tag: tag == class_tag_val}) # this works
        filtered_tags = soup.find_all('h3', {'string': lambda tag: tag == h3_tag_val}) # string and text both dont work for <h3>textval <tag2>..</tag2></h3>
        #filtered_tags = soup.find_all('h3',text=lambda s: h3_tag_val in s) # doesnt work compile error NoneType is not iterable
        #filtered_tags = soup.find_all('h3',{'text':[h3_tag_val]}) # doesnt work compile error
        filtered_tags = soup.find_all('h3',text_stripped=re.compile(h3_tag_val)) # doesnt find...
        filtered_tags = soup.find_all('h3',text=re.compile(h3_tag_val)) # doesnt find...
        filtered_tags = soup.find_all('h3') # only this seems to work for h3

        for filtered_tag in filtered_tags:
            p('--------------------------------------------------------')
            if filtered_tag.text is None:
                p('-----------------------filtered_tag text is None')
            elif h3_tag_val in filtered_tag.text:
                text_stripped = re.sub(r'\n\n+','\n\n',filtered_tag.text)
                p('-----------------------filtered_tag :                 {}'.format(filtered_tag)) # all its values
                p('-----------------------filtered_tag_text:             {}'.format(text_stripped)) # stripped tag
                p('-----------------------filtered_tag get_text():       {}'.format(filtered_tag.get_text()))
                p('-----------------------filtered_tag attrs:            {}'.format(filtered_tag.attrs)) # returns attrs of div and its values (space separate value array)
                p('-----------------------filtered_tag attrs get class:  {}'.format(filtered_tag.attrs.get('class')))  # returns attr_vals of <div class=attr_vals>
                p('-----------------------filtered_tag attrs string:     {}'.format(filtered_tag.string)) # div doesnt have string associated, eg no <div xx>stringval</div>
                p('-----------------------filtered_tag attrs name:       {}'.format(filtered_tag.name))  # div because find_all was searching for div attr
                p('-----------------------filtered_tag attrs contents:   {}'.format(filtered_tag.contents)) # list
        p("------breaker-----")
    def test_pull_data_1(self):
        t = self
        p("------")
        #t.test_parse_url()
        t.test_parse_url_with_javascript()
        #t.test_parse_bs4_with_file_1()
        #t.test_parse_bs4_with_file_parse_fields()
        p("------")
    def test_main(self):
        t = self
        #t.test_localhost()
        t.test_pull_data_1()



t = TestRequests()
t.test_main()

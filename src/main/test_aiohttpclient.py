#!/usr/local/bin/python3

import asyncio
import aiohttp
import concurrent.futures
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import random
import threading
import queue
import time
import argparse
import sys
import os
import json
import html.parser
import requests

debug = False

def p(s):
    print(s)
def d(s):
    if(debug):
        p(s)

class HTMLParserGetText1(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.state = 0
    def handle_data(self, data):
        d('data:           {}'.format(data))
        if data is None:
            return
        data = data.replace('\n','')

        if(len(data) == 0):
            return
        if(self.state == 2):      # paragraph state
            self.text.append(data)
            if(data == 'Related Articles'):
                self.state = 3

    def get_data(self):
        return self.text
    def handle_startendtag(self, tag, attrs):
        d('startendtag t:  {}'.format(tag))
        d('startendtag a:  {}'.format(attrs))
    def handle_endtag(self, tag):
        d('endtag:         {}'.format(tag))
    def handle_starttag(self, tag, attrs):
        d('starttag t:     {}'.format(tag))
        d('starttag a:    {}'.format(attrs))
        if(tag == 'div'):
            if(attrs is not None and len(attrs) != 0 and len(attrs[0]) == 2):
                if(attrs[0][0] == 'class' and attrs[0][1] == 'journal-entry-text'):
                    d('wayne attrs: {}'.format(attrs))
        if(tag == 'title'):
            self.state = 1
        elif(tag == 'p' and self.state == 1):
            self.state = 2

class HTMLParserGetBodyLinks1(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []
        self.text = []
        self.urls = []
        self.state = 0
        self.tags_prv = None
        self.attr_prv = None

    def handle_data(self, data):
        d('data:           {}'.format(data))
        if data is None:
            return
        data = data.replace('\n','')

        if(len(data) == 0):
            return

        self.data.append(data)
        if(self.state == 2):      # paragraph state
            self.text.append(data)
            if(data == 'Related Articles'):
                self.state = 3

    def get_text(self):
        return self.text
    def get_data(self):
        return self.data
    def get_urls(self):
        return self.urls

    def handle_startendtag(self, tag, attrs):
        return
    def handle_endtag(self, tag):
        return
    def handle_starttag(self, tag, attrs):
        d('starttag t:     {}'.format(tag))
        d('starttag a:    {}'.format(attrs))
        if(tag == 'div'):
            if(attrs is not None and len(attrs) != 0 and len(attrs[0]) == 2):
                if(attrs[0][0] == 'id' and attrs[0][1] == 'content'):
                    self.state = 1
        if(self.state == 1 and tag == 'a' and self.tags_prv == 'li'):
            if(attrs is not None and len(attrs) != 0 and len(attrs[0]) == 2):
                if(attrs[0][0] == 'href'):
                    self.urls.append(attrs[0][1])
        self.tags_prv = tag
        self.attr_prv = attrs


class TestAioHttpClient:
    def __init__(self):
        self.tsem = threading.Semaphore(value=20)
        self.asem = asyncio.Semaphore(value=20)

    def set_semaphore_asyncio_max(self, max):
        self.asem = asyncio.Semaphore(value=max)

    def set_semaphore_thread_max(self, max):
        self.tsem = threading.Semaphore(value=max)

    def test_thread_semaphore_function(self, name, maxloops=20):
        for i in range(0,maxloops):
            p('{} acquire  loop {}'.format(name, i))
            self.tsem.acquire()
            p('{} acquired loop {}'.format(name, i))
            time.sleep(0.01)
            self.tsem.release()
            p('{} release  loop {}'.format(name, i))

    def test_thread_semaphore(self):
        t1 = threading.Thread(target=self.test_thread_semaphore_function, args=['t0',10])
        t2 = threading.Thread(target=self.test_thread_semaphore_function, kwargs={'name':'t1','maxloops':10})
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    async def await_get_msg(self, name, i):
        return '{} acquired loop {}'.format(name, i)

    async def test_asyncio_semaphore_function(self, name, maxloops=20):
        for i in range(0,maxloops):
            p('{} acquire  loop {}'.format(name, i))
            async with self.asem:
                await asyncio.sleep(0.01)
                msg = await self.await_get_msg(name, i)
                p(msg)
            p('{} release  loop {}'.format(name, i))
        return name

    def test_asyncio_semaphore(self):
        loop = asyncio.get_event_loop()
        tasks = []
        for i in range(0,2):
            task = asyncio.ensure_future(self.test_asyncio_semaphore_function('t{}'.format(i), 10))
            tasks.append(task)
        names = loop.run_until_complete(asyncio.wait(tasks))

    async def async_fetch(self, url, session):
        if url is None or url == '':
            return None
        #p('async_fetch url {}'.format(url))
        async with self.asem:
            try:
                async with session.get(url) as response:
                    rsp = await response.read()
                    return rsp
            except Exception as e:
                p('-------invalidurl:{}'.format(url))
                return None


    async def async_fetch_all(self, urls):
        tasks = []
        responses = []
        async with aiohttp.ClientSession() as session:
            for url in urls:
                if url is None or url == '':
                    continue
                task = asyncio.ensure_future(self.async_fetch(url, session))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
        return responses

    def async_get_urls(self, urls):
        self.set_semaphore_asyncio_max(100)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.async_fetch_all(urls))
        loop.run_until_complete(future)
        results = future.result()
        return results

    def test_asyncio_fetch(self, urls):
        results = self.async_get_urls(urls)
        return results

    def test_asyncio_get_urls(self):
        urls = [
            ''
        ]
        results = self.test_asyncio_fetch(urls)
        for result in results:
            p(result)

    def parse_html(self, result):
        #p(result)
        p('-----------------------------------')
        htmlParser = HTMLParserGetText1()
        htmlParser.feed(result)
        data = htmlParser.get_data()
        htmlParser.close()
        p('---------------begindata-------------------')
        p(data)
        return data

    def parse_html_links(self, result):
        p('-----------------------------------')
        htmlParser = HTMLParserGetBodyLinks1()
        htmlParser.feed(result)
        urls = htmlParser.get_urls()
        htmlParser.close()
        p('---------------begindata-------------------')
        for url in urls:
            p(url)
        p('---------------begincallurl-------------------')
        results = self.test_asyncio_fetch(urls)
        for result in results:
            p('---------------resultcallurl-------------------')
            if(result is not None):
                result = result.decode('utf-8')
                self.parse_html(result)

    def test_follow_links(self):
        urls = [
            ''
        ]
        results = self.test_asyncio_fetch(urls)
        for result in results:
            result = result.decode('utf-8')
            self.parse_html_links(result)

    def test_parse_html(self):
        fi = open('tmp.link.html', 'r')
        lines = fi.readlines()
        buffer = ""
        for line in lines:
            buffer += line
        fi.close()
        self.parse_html_links(buffer)

    '''
    based on urllib3 connection pooling, so underlying socket can be reused
    '''
    def test_request_sessions_dummydata(self):
        session = requests.Session()
        url = 'https://somewhere'
        data = {'k1':'v1'}

        rsp = session.post(url, data=data)

        p(rsp.text)
        p(rsp.status_code)
        p(rsp.is_redirect)
        p(rsp.cookies)
        p(rsp.content)
        p(rsp.json())
        p(rsp.url)
        if(rsp.headers is not None):
            for k,v in rsp.headers.items():
                p('{}:{}'.format(k,v))

        params = {'arg1':'blah'}
        headers = {'user-agent':'blah'}

        rsp = session.get(url, params=params, headers=headers)
        p(rsp.status_code)

        session.auth = ('user','pass')
        session.headers.update({'k1':'v1'})
        rsp = session.get(url, headers=headers)     # headers AND update(..) combined
        rsp = session.get(url, cookies={'k1':'v1'})
        rsp = session.get(url, proxies={'http':'http://proxy','https':'https://proxy'})

    def test_request_get_post_nosession(self):
        url = 'https://somewhere'
        data = {'k1':'v1'}

        rsp = requests.post(url, data=data)
        p(rsp.text)
        p(rsp.status_code)
        p(rsp.is_redirect)
        p(rsp.cookies)
        p(rsp.content)
        p(rsp.json())
        p(rsp.url)
        if(rsp.headers is not None):
            for k,v in rsp.headers.items():
                p('{}:{}'.format(k,v))

        params = {'arg1':'blah'}
        headers = {'user-agent':'blah'}

        rsp = requests.get(url, params=params, headers=headers)
        p(rsp.status_code)

        rsp = requests.post(url, data=json.dumps(data))
        p(rsp.txt)

        rsp = requests.post(url, json=data)
        p(rsp.txt)

        files = {'file1':open('path1','rb'), 'file2':open('path2','rb')}
        rsp = requests.post(url, files=files)
        p(rsp.txt)

    def process_test(self, methodname=None, arg1=None, arg2=None, arg3=None):
        if(methodname is None or len(methodname) == 0):
            return
        resuly = None
        if(arg1 is not None and arg2 is not None and arg3 is not None):
            result = getattr(self, methodname)(arg1,arg2,arg3)
        elif(arg1 is not None and arg2 is not None):
            result = getattr(self, methodname)(arg1,arg2)
        elif(arg1 is not None):
            result = getattr(self, methodname)(arg1)
        else:
            result = getattr(self, methodname)()
        return result

    def process(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-test', type=str, help='test methodname')
        parser.add_argument('-a1', type=str, help='arg1')
        parser.add_argument('-a2', type=str, help='arg2')
        parser.add_argument('-a3', type=str, help='arg3')
        parser.add_argument('-url', help='url')
        parser.add_argument('-num', type=int, help='num types to call url')
        args = parser.parse_args()
        tbeg = time.time()
        if args.test is not None:
            self.process_test(args.test,args.a1,args.a2,args.a3)
        tend = time.time()
        tdif = (tend - tbeg)
        p('\ncompleted. time diff {} ms'.format(tdif))


t = TestAioHttpClient()
t.process()



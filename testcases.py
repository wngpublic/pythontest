#!/usr/local/bin/python3

import sys
import os
import os.path
import getopt
import argparse
import fileinput
import subprocess
import random
import re
import string
import copy
import math
import threading
import calendar
import cmd
import collections
from collections import OrderedDict
import time
import urllib.request as url
import pathlib
import myclasses
import json
import unittest
import argparse
import threading
import gossip
import abc
import asyncio
import queue
import gzip
import multiprocessing

def p(s):
    print(s)


class MyAsyncBasicTest:
    def __init__(self):
        pass
    async def basic_task(self, id, seconds):
        await asyncio.sleep(seconds)
        return 'basic_task done {} sleep {}'.format(id,seconds)
    async def basic_task_no_return(self, id, seconds):
        await asyncio.sleep(seconds)
        p('basic_task_no_return done {} sleep {}'.format(id,seconds))
    def test_basic(self):
        event_loop = asyncio.get_event_loop()
        try:
            task = event_loop.create_task(self.basic_task(1,3))
            event_loop.run_until_complete(task)
        finally:
            event_loop.close()
    async def test_many_fixed_list_tasks(self, num_tasks):
        list_tasks = []
        for i in range(0, num_tasks):
            task = asyncio.create_task(self.basic_task(i, random.randint(1,5)))
            list_tasks.append(task)
            task = asyncio.create_task(self.basic_task_no_return(i, random.randint(1,5)))
            list_tasks.append(task)
        for task in list_tasks:
            await task
    def test(self):
        self.test_basic()

class DependencyTest:
    def __init__(self):
        pass
    class Node:
        def __init__(self, id, router):
            self.id = id
            self.s_ids = set()
            self.router = router
            self.log = []

        def addneighborid(self, id):
            self.s_ids.add(id)

        def caller(self, dst):
            rsp = self.router.route(self.id,dst)
            self.log.append(rsp)

        def callee(self):
            return self.s_ids

        def getlog(self):
            return self.log

    class Route:
        def __init__(self, numnodes):
            self.d_nodes = {}
            for i in range(0, numnodes):
                n = DependencyTest.Node(i, self)
                self.d_nodes[i] = n
            ids = self.d_nodes.keys()
            for k,v in self.d_nodes.items():
                for id in ids:
                    v.addneighborid(id)

        def route(self, idsrc, iddst):
            if idsrc not in self.d_nodes or iddst not in self.d_nodes:
                return None
            ndst = self.d_nodes[iddst]
            ids = ndst.callee()
            return ids

        @abc.abstractmethod
        def abmethod(self):
            """nothing"""

        def getIds(self):
            return self.d_nodes.keys()

        def getNode(self, id):
            return self.d_nodes[id]

    def p(self,s):
        print(s)

    def t(self):
        router = DependencyTest.Route(3)
        ids = router.getIds()
        assert 0 in ids and 1 in ids and 2 in ids
        src = router.getNode(0)
        src.caller(1)
        logs = src.getlog()
        assert len(logs) == 1
        src.caller(2)
        logs = src.getlog()
        assert len(logs) == 2
        self.p(logs)
        self.p('passed')


class MyBaseClass:
    def __init__(self):
        self._id = None
        self._name = None
    def name(self):
        return self._name
    def name(self, v):
        self._name = v
    def id(self):
        return self._id
    def id(self, v):
        self._id = v
    def p(self):
        p('MyBaseClass id:{} name:{}'.format(self._id, self._name))

class MyBaseClass2:
    def __init__(self):
        self._id2 = None

class MyClass2(MyBaseClass):
    def __init__(self):
        self._id2 = None
        pass
    def id2(self):
        return self._id2
    def id2(self, v):
        self._id2 = v
    def p(self):
        p('MyClass2 id:{} name:{} id2:{}'.format(self._id, self._name, self._id2))

class MyClass3(MyBaseClass):
    def __init__(self):
        self._id3 = None
        pass
    def id3(self):
        return self._id3
    def id3(self, v):
        self._id3 = v
    def p(self):
        p('MyClass3 id:{} name:{} id3:{}'.format(self._id, self._name, self._id3))

class MyNode:
    pass

class Tests:
    def __init__(self):
        self.utils = myclasses.Myutils()

        pass

    @staticmethod
    def p1(s):
        print(s)

    def p2(self,s):
        print(s)

    def t1(self):
        t = myclasses.ClassTest1()
        p('{0}'.format(t.getV1()))
        p('{0}'.format(t.getV3()))
        t.setV1(11)
        p('{0}'.format(t.getV1()))
        t.setV1(12)
        p('{0}'.format(t.getV1()))

    def t2(self):
        v = self.utils.readfile('input/tnf_rtb_request.json')
        p(v)
        vjson = self.utils.getJsonFromString(v)
        p('accessing json stuff')
        p('{0}'.format(vjson['id']))
        p('{0}'.format(vjson['site']['domain']))

        if 'id' in vjson:
            p('id exists = {0}'.format(vjson['id']))
        else:
            p('id not exists')

        if 'breakid' in vjson['imp'][10]['video']['ext']:
            p('breakid exists = {0}'.format(vjson['imp'][10]['video']['ext']['breakid']))
        else:
            p('breakid not exists')

        if 'breakfast' in vjson['imp'][10]['video']['ext']:
            p('breakfast exists = {0}'.format(vjson['imp'][10]['video']['ext']['breakfast']))
        else:
            p('breakfast not exists')

        p('length of imp is {0}'.format(len(vjson['imp'])))

        vjson['imp'][10]['video']['ext']['breakid'] = vjson['imp'][10]['video']['ext']['breakid'] + 1
        vjson['imp'][10]['video']['ext']['breakid'] += 1

        p('breakid exists = {0}'.format(vjson['imp'][10]['video']['ext']['breakid']))

    def t3(self):
        pass

    def t4(self):
        # randomization testing
        l = 'abcdef'
        for i in range (0,len(l)):              # 0 1 2 3 4     size = 5
                                                #               min <= range < max
            p('{0}={1}'.format(i,l[i]))
        p('---------------')
        for i in range (0,10):
            idx = random.randint(0,len(l)-1)    # 0 1 2 3 4     size = 5, but max @ 4
                                                # a b c d e     min <= randint <= max
            v = l[idx]
            p('{0}={1}'.format(i,v))

    def t5(self):
        p('val: {0}'.format(self.utils.getRandString(5)))
        p('val: {0}'.format(self.utils.getRandString(5, charsettype='n')))
        p('val: {0}'.format(self.utils.getRandString(5, charsettype='x')))

    def t6(self):
        p('{0}'.format(self.utils.getDatetimeMicro()))
        p('{0}'.format(self.utils.getTimeCurMillis()))

    def t7(self):
        a = []
        a.append(10)
        a.append(20)
        a.append(30)
        for v in a:
            p('{0}'.format(v))
        p('--------')
        for i in range(0, len(a)):
            p('{0}'.format(a[i]))
        p('--------')

        d = {}
        d[1] = 10
        d[2] = 20
        d[3] = {}
        d[3][10] = 300
        d[3][20] = 600
        d[3][30] = 900

        p('{0}'.format(d[1]))
        p('{0}'.format(d[2]))
        p('{0}'.format(d[3][10]))
        for k in d[3]:
            p('loop {0} = {1}'.format(k, d[3][k]))

    def t8(self):
        # illustrate variable in if gets propagated out
        flag = False
        if flag:
            v = 10
        else:
            v = 20
        p('v is {0}'.format(v))

    def t9(self):
        # assert test
        try:
            assert 1+1==3,'t9 eval error 1'
        except Exception as e:
            p(e)
        # this raises error to top level, so below this never called
        assert 1+1==3,'t9 eval error 2'
        try:
            assert 1+1==3,'t9 eval error 3'
        except Exception as e:
            p(e)
        assert False, "should not be here"

    def t10(self):
        Tests.p1('hello world 1')   # has no self
        self.p2('hello world 2')    # has self
        p('hello world 3')          # has no self

    def t11(self):
        # test raising exception
        try:
            raise ValueError('value error1 ')
        except Exception as e:
            p(e)
        try:
            raise ValueError('value error2 ',1,2,3,4,5)
        except Exception as e:
            p(e)
        raise ValueError('value error3 ')

    def generateJSONTest(self, type=1):

        pass

    @staticmethod
    def diffJsonSubtree(json):
        pass

    def testRegex(self):
        pass

    @staticmethod
    def testDifflib(self):
        pass

    @staticmethod
    def getPathAndFile(filename):
        ary  = filename.split('/')
        if len(ary) == 1:
            path = None
            file = ary[0]
        else:
            path = None
            for i in range(0, len(ary)-1):
                if path is None:
                    path = ary[i]
                else:
                    path = path + '/' + ary[i]
            file = ary[len(ary)-1]
        result = {'path':path, 'file':file}
        return result

    @staticmethod
    def testFileCreateDestroy(filename='log1/tmp/hello.txt'):
        # https://docs.python.org/3/library/os.path.html
        # https://docs.python.org/3/library/os.html
        maxcount = 5
        res = Tests.getPathAndFile(filename)
        spath = res['path']
        sfile = res['file']
        file = None
        if not os.path.exists(filename):
            if not os.path.exists(spath):               # redundant because exist_ok=True
                os.makedirs(name=spath, exist_ok=True)
            file = open(filename, 'w')
        else:
            for i in range(0,maxcount):
                filenametmp = filename + '.' + str(i)
                pathobj = pathlib.Path(filenametmp)
                if not pathobj.exists():
                    file = open(filenametmp, 'w')
                    break
                assert os.path.isfile(filenametmp)
                assert pathobj.is_file()

        if file is None:
            # https://docs.python.org/3/library/exceptions.html
            raise ValueError('no file created for {0}'.format(filename), filename, maxcount)
        assert os.path.isfile(file.name)
        file.write('hello world 1\n')
        file.write('hello world 2\n')
        file.close()

        pathobj = pathlib.Path(file.name)
        if not pathobj.exists():
            raise ValueError('no file exists {0}'.format(file.name))
        filehandle = open(file.name, 'r')
        lines = ''
        # https://docs.python.org/3/tutorial/inputoutput.html
        for line in filehandle:
            lines += line
        filehandle.close()

        return {'filename': file.name,'data': lines}

    def testFileOp(self):
        res = Tests.testFileCreateDestroy('./logtmp/test/filetxt.txt')
        p(res['filename'])
        lines = res['data'].split('\n')
        for line in lines:
            p(line)

    def testListCompare(self):
        l1 = [10,8,3,6]
        l2 = [6,8,10,3]
        l3 = [2,8,10,3]
        l4 = [2,8,10,3,1]
        l5 = [2,8,10,3]
        res = collections.Counter(l1) == collections.Counter(l2)
        p('l1 l2 = {0}'.format(res))
        res = collections.Counter(l1) == collections.Counter(l3)
        p('l1 l3 = {0}'.format(res))
        res = collections.Counter(l3) == collections.Counter(l4)
        p('l3 l4 = {0}'.format(res))
        res = collections.Counter(l3) == collections.Counter(l5)
        p('l3 l5 = {0}'.format(res))
        res = sorted(l1) == sorted(l2)
        p('l1 l2 = {0}'.format(res))

    def testSetIntersect(self):
        l1 = [10,8,3,6]
        l2 = [6,8,10,3]
        l3 = [1,2,3,4]
        res = set(l1).intersection(l2)
        p(res)
        res = set(l1).intersection(l3)
        p(res)

    @staticmethod
    def testFileTXT(filename, overwrite=False):
        pass

    @staticmethod
    def testFileJSON(filename='input/testinputsmall.json'):
        vjson = myclasses.Myutils.getFileJSON(filename)
        p('{0}'.format(json.dumps(vjson, indent=2)))
        p('-----')
        myclasses.Myutils.traverseDictOld('',vjson,printStats=True)

    @staticmethod
    def testDiffJSON(filename1, filename2):
        json1 = myclasses.Myutils.getFileJSON(filename1)
        json2 = myclasses.Myutils.getFileJSON(filename2)
        res = myclasses.Myutils.jsondiff(json1=json1,json2=json2,prefix='',printStats=True,printKeysOnly=True)
        p('{0} diff {1} = {2}'.format(filename1, filename2, res))

    def testDiffJSONTest(self):
        filename1='input/testinputsmall.json'
        filename2='input/testinputsmall1.json'
        json1 = myclasses.Myutils.getFileJSON(filename1)
        json2 = myclasses.Myutils.getFileJSON(filename2)
        json2['k.3'][1]['k.3.1.2'][0]['k.3.1.2.0']['k.3.1.2.0.0']['k.3.1.2.0.0.1'] = 'v.3.1.2.0.0.1'
        res = myclasses.Myutils.jsondiff(json1=json1,json2=json2,printStats=True)
        p('{0} diff {1} = {2}'.format(filename1, filename2, res))
        p('--------------')
        json2['k.3'][1]['k.3.1.2'][0]['k.3.1.2.0']['k.3.1.2.0.0']['k.3.1.2.0.0.1'] = 'v.3.1.2.0.0.2'
        res = myclasses.Myutils.jsondiff(json1=json1,json2=json2,printStats=True)
        p('{0} diff {1} = {2}'.format(filename1, filename2, res))
        p('--------------')
        json2['k.3'][1]['k.3.1.2'][0]['k.3.1.2.0']['k.3.1.2.0.0']['k.3.1.2.0.0.1'] = 'v.3.1.2.0.0.1'
        json2['k.3'][1]['k.3.1.2'][0]['k.3.1.2.0'].pop('k.3.1.2.0.1', None)
        res = myclasses.Myutils.jsondiff(json1=json1,json2=json2,printStats=True)
        p('{0} diff {1} = {2}'.format(filename1, filename2, res))

    @staticmethod
    def testFileObject(filename):
        pass

    @staticmethod
    def testFileCSV(filename):

        pass

    @staticmethod
    def testReadXMLFile():
        r = myclasses.Myutils.getFileXML(filename='input/testinput.small.xml')
        myclasses.Myutils.parseXML(r)
        p('--------------')
        v0 = r[1]
        v1 = r[1][2]
        v2 = v1.text
        p('{0},{1},{2}'.format(v0,v1,v2))
        #time.sleep(1)
        assert v2 == '59900'
        for v1 in r.findall('country'):
            v2 = v1.find('gdppc')
            if v2 is not None:
                if v2.text == '59900':
                    p('found: {0}'.format(v2.text))

    @staticmethod
    def testReadXMLFileVAST():
        r = myclasses.Myutils.getFileXML(filename='input/testinput.xml')
        myclasses.Myutils.parseXML(r)

    @staticmethod
    def testFileXML(filename):
        pass


    @staticmethod
    def testFileOperations():
        pass

    @staticmethod
    def testPickle(self):
        pass

    @staticmethod
    def testCrypto(self):
        pass

    @staticmethod
    def testArgparse(self):
        pass

    def testSort(self):
        li = [9,3,5,1,8,6,7,4,2,0]
        ls = ['hello9','nihao','yo','wassup','hello2','hihi']
        ld = [
            {'k0':1,'k1':9},
            {'k0':5,'k1':3},
            {'k0':3,'k1':5},
            {'k0':8,'k1':1},
            {'k0':9,'k1':8},
            {'k0':4,'k1':6},
            {'k0':2,'k1':7},
            {'k0':6,'k1':4},
            {'k0':7,'k1':2},
            {'k0':0,'k1':0}
        ]

        l = sorted(li)
        p(li)
        p(l)
        li.sort()
        p(li)
        p('--------')
        l = sorted(ls)
        p(ls)
        p(l)
        ls.sort()
        p(ls)
        p('--------')
        l = sorted(ld, key=lambda x: x['k1'])
        p(ld)
        p(l)
        l = sorted(ld, key=lambda x: x['k0'])
        p(l)

    def testThreadPrint(self, msg, numloops, lock):
        for i in range(0, numloops):
            lock.acquire(True)
            p(msg)
            lock.release()

    def testThreading(self):
        lock = threading.Lock()
        t1 = threading.Thread(target=self.testThreadPrint, args=('a',5,lock))
        t2 = threading.Thread(target=self.testThreadPrint, args=('b',5,lock))
        t1.start()
        t2.start()

    def testSHA256(self):
        s = 'the cat in the hat'
        h = myclasses.Myutils.hashSHA256(s)
        p(s)
        p(h)

    def testReadWriteFile(self):
        filename = 'input/filetest1.txt'
        if not os.path.isfile(filename):
            fh = open(filename,'w')
            fh.close()
        fh = open(filename,'r')
        lines = fh.readlines()
        fh.close()
        data = ''.join(lines)

    def testRegex(self):
        data =  'the cat in the hat\n' + \
                '111   222  3333 44a 44aa b55 bb55 6c6666 789 123 321 54321\n' + \
                'thedigit1isbetween number12\n' + \
                '1 here\r\n' + \
                '15 16:17:18 19:20 eol\n' + \
                '15 16:17:18 19:20:21 eol\n' + \
                '15 16:17:18 19:20:21:22 eol\n' + \
                '15 16:17:18 19:20:2122 eol\n' + \
                '15 16:17:1822 19:20:2122 eol\n' + \
                '15 16:17 19:20 eol\n' + \
                'Oct 1 2018\n' + \
                'Oct/1 2018\n' + \
                'Oct/1/2018\n' + \
                '1/2018\n' + \
                '10/01/2018' + \
                'extracting 10/01/2018 from here and 11/01/2018 here\n' + \
                'extracting 1:2 and 2:3:4 and 10:11:12 and 13:14:156 and 8:8\n' + \
                'extracting 1:2 and 10:11:12 and 13:14:15 and 2:3:4 and 8:8\n' + \
                '10/01/18'
        lines = data.split('\n')
        words = re.split(r'\s+',data)
        p(lines)
        p(words)

        # match starts from beginnng of string
        # search is anywhere in string

        for w in words:
            cnt = 0
            if re.match(r'^\d+$',w):
                p('digits1 only:        {0}'.format(w))
                cnt += 1
            if re.search(r'\d+',w):
                p('digits4 only:        {0}'.format(w))
                cnt += 1
            if re.match(r'\d+',w):
                p('digits5 only:        {0}'.format(w))
                cnt += 1
            if re.search(r'^[0-9]+$',w):
                p('digits2 only:        {0}'.format(w))
                cnt += 1
            if re.search(r'^[a-z]+$',w):
                p('alphabet only:       {0}'.format(w))
                cnt += 1
            if re.search(r'[0-9]+',w):
                p('digits3 only:        {0}'.format(w))
                cnt += 1
            if re.search(r'[a-z]+',w):
                p('alphabet1 only:      {0}'.format(w))
                cnt += 1
            if re.match(r'^([0-9]+)([a-z]+)$',w):
                p('alphanumeric1 only:  {0}'.format(w))
                cnt += 1
            if re.match(r'^([a-z]+)([0-9]+)$',w):
                p('alphanumeric2 only:  {0}'.format(w))
                cnt += 1
            if re.match(r'^(.*[a-z])(.*[0-9])$',w):
                p('alphanumeric4 only:  {0}'.format(w))
                cnt += 1
            if re.match(r'^(.*[0-9])(.*[a-z])$',w):
                p('alphanumeric5 only:  {0}'.format(w))
                cnt += 1
            if re.match(r'[0-9]+',w) and re.match(r'[a-z]+',w):
                p('alphanumeric3 only:  {0}'.format(w))
                cnt += 1
            if re.search(r'[0-9]+',w) and re.search(r'[a-z]+',w):
                p('alphanumeric6 only:  {0}'.format(w))
                cnt += 1
            if re.search(r'^\d+/\d+/\d+$',w):
                p('date format:         {0}'.format(w))
                cnt += 1
            if re.search(r'^\d+:\d+:\d+$',w):
                p('time format:         {0}'.format(w))
                cnt += 1
            if cnt == 0:
                p('no category:         {0}'.format(w))
        for line in lines:
            if re.search(r'\s+(\d){2}:(\d){2}:(\d){2}\s+',line):
                p('match line1:         {0}'.format(line))
            if re.search(r'.*((\d){2}:(\d){2}:(\d){2}\s+).*((\d){2}:(\d){2}:(\d){2}\s+)',line):
                p('match line2:         {0}'.format(line))
            if re.search(r'(\d){2}:(\d){2}:(\d){2}',line):
                p('match line3:         {0}'.format(line))
            if re.search(r'\d{2}:\d{2}:\d{2}',line):
                p('match line4:         {0}'.format(line))
        match = re.search(r'.*(\d{1}:\d{1}:\d{1}).*(\d{1}:\d{1}:\d{1})','extracting 1:2 and 2:3:4 and 10:11:12 and 13:14:156 and 8:8\n')
        assert match is None
        match = re.search(r'.*(\d{2}:\d{2}:\d{2}).*(\d{2}:\d{2}:\d{2})','extracting 1:2 and 2:3:4 and 10:11:12 and 13:14:156 and 8:8\n')
        assert match is not None
        p('group 0={0} group 1={1}'.format(match.group(1),match.group(2)))

    def testString(self):
        str = 'the  cat in the hat  is not in zip 94089 nor 94401 and not  even in Burlingame \n'
        words = re.split(r'\s+', str)
        for i in range(0, len(words)):
            w = words[i].strip()
            if len(w) == 0:
                continue
            wnew = ''
            for j in range(0, len(w)):
                c = w[j]
                wnew += c
            p('{:>2} = {:<10}. wlen = {}'.format(i, wnew, len(wnew)))

        p('----------')

        p('{:>10}'.format(1.123456789))
        p('{:>10.2f}'.format(1.123456789))
        p('{:>10.2f}'.format(111.123456789))

        s = '111.123456789'
        f = float(s)

        p('{:>10.2f}'.format(f))

    def testSortDictList(self):
        d = {
            'k3':'v3',
            'k1':'v1',
            'k4':'v4',
            'k5':'v5',
            'k2':'v2'
        }

        for k,v in d.items():
            p('{} = {}'.format(k,v))

        p('------')

        od = OrderedDict(sorted(d.items()))
        for k,v in od.items():
            p('{} = {}'.format(k,v))

        p('----- sorting with lambda value')
        list = sorted(d.items(), key=lambda x: x[1])
        for v in list:
            p('{} = {}'.format(v[0],v[1]))

        p('----- sorting with lambda key')
        list = sorted(d.items(), key=lambda x: x[0])
        for v in list:
            p('{} = {}'.format(v[0],v[1]))

        p('----- sort by keys to list')

        list = sorted(d.items())
        for v in list:
            p('{} = {}'.format(v[0],v[1]))

        p('----- sort reverse by keys to list')

        list = sorted(d.items(), reverse=True)
        for v in list:
            p('{} = {}'.format(v[0],v[1]))

        p('---- print keys only')
        for k in d.keys():
            p(k)

        p('----- print dict values only')

        for v in d.values():
            p(v)

        p('----- sort list')
        l = [5,2,3,1,4]
        a = sorted(l)
        for v in a:
            p(v)


        p('----- reverse sort')
        a = sorted(l, reverse=True)
        for v in a:
            p(v)

        d = {
            'k1':{
                'kx':'1',
                'ky':'3',
                'kz':'2'
            },
            'k2':{
                'kx':'3',
                'ky':'2',
                'kz':'1'
            },
            'k3':{
                'kx':'2',
                'ky':'1',
                'kz':'3'
            }
        }

        p('---- obj sort by top key')
        list = sorted(d.items(), key=lambda x:x[0])
        for v in list:
            p(v)

        p('---- obj sort by top val ky')
        list = sorted(d.items(), key=lambda x:x[1]['ky'])
        for v in list:
            p(v)

        p('---- obj sort by top val kz')
        list = sorted(d.items(), key=lambda x:x[1]['kz'])
        for v in list:
            p(v)

        p('test passed')


    def testNumbers(self):
        v1 = 1658581700688169
        v2 = 1658581800689991
        d1 = v2 - v1
        p('{} - {} = {}'.format(v2,v1,d1))

        dns = d1
        dus = d1 / 1000
        dms = d1 / 1000000
        p('')
        p('dns:{},\ndus:{},\ndms:{}\n'.format(dns,dus,dms))
        p('dns:{},\ndus:{:.0f},\ndms:{:.0f}\n'.format(dns,dus,dms))

    def testTimeDiff(self,filename):
        if not os.path.isfile(filename):
            return
        try:
            fh = open(filename,'r')
            lines = fh.readlines()
            fh.close()
        except Exception as e:
            p(e)
            return
        finally:
            fh.close()

        time_ns_prv = None
        for line in lines:
            a = line.split()
            if len(a) != 2:
                continue
            time_ns = int(a[0])
            if time_ns_prv != None:
                time_ns_diff = time_ns - time_ns_prv
                time_ms_diff = time_ns_diff / 1000000
                p('diff_ms:{:>10.2f} time_ns:{:>20} title:{}'.format(time_ms_diff,time_ns,a[1]))
            time_ns_prv = time_ns
        p('done')

    @staticmethod
    def testArgParse():
        # ./mymain.py hello 2
        # ./mymain.py hello 2 --opt1s opt1v --opt2s opt2v
        # args Namespace(opt1s='opt1v', opt2s='opt2v', opt3i=None, req1s='hello', req2i=2)
        parser = argparse.ArgumentParser()
        parser.add_argument("req1s",help='req1s is string')
        parser.add_argument("req2i",help='req2i is int',type=int)
        parser.add_argument("--opt1s",help='opt1s is string')
        parser.add_argument("--opt2s",help='opt2s is string')
        parser.add_argument("--opt3i",help='opt3i is int',type=int)
        args = parser.parse_args()
        v1 = args.req1s
        v2 = args.req2i
        v3 = args.opt1s
        v4 = args.opt2s
        v5 = args.opt3i
        p('args v1:{},v2:{},v3:{},v4:{},v5:{}'.format(v1,v2,v3,v4,v5))

    @staticmethod
    def testCmdLoop1():
        for i in range(0,5):
            p('prompt {} > '.format(i))
            inv = input()
            p('input was: {}'.format(inv))
        p('bye')

    @staticmethod
    def testCmdLoop2():
        for i in range(0,5):
            p('prompt {} > '.format(i))
            inv = input()
            p('input was: {}'.format(inv))
        p('bye')

    def testMyClass2(self):
        mc_0  = MyBaseClass()
        mc_0.id(0)
        mc_0.name('mc0')

        mc_1  = MyBaseClass()
        mc_1.id(1)
        mc_1.name('mc1')

        mc2_0 = MyClass2()
        mc2_0.id(20)
        mc2_0.name('mc20')
        mc2_0.id2(20)

        mc2_1 = MyClass2()
        mc2_1.id(21)
        mc2_1.name('mc21')
        mc2_1.id2(21)

        mc3_0 = MyClass3()
        mc3_0.id(30)
        mc3_0.name('mc30')
        mc3_0.id3(30)

        mc3_1 = MyClass3()
        mc3_1.id(31)
        mc3_1.name('mc31')
        mc3_1.id3(31)

        l = []
        l.append(mc_0)
        l.append(mc_1)
        l.append(mc2_0)
        l.append(mc2_1)
        l.append(mc3_0)
        l.append(mc3_1)
        for mc in l:
            mc.p()

    def randint(self,max):
        return random.randint(0,max)

    def testGossip(self):
        nodes = []
        numnodes = 5
        numcycles = 3

        for i in range(0,numnodes):
            node = gossip.GossipDistributed.MyNodeGossip(2,False,3)
            nodes.append(node)

        fanout = 2
        cycle = 1
        for i in range(0,numcycles):
            targets = []
            for j in range(0,fanout):
                node = nodes[self.randint(len(nodes))]
                targets.append(node)

            nextstate = []
            cycle += 1
            pass

    def testMiscCalls(self):
        d = {}
        l = []
        s = set()
        l.append(random.randint(0,0))
        l.append(random.randint(1,1))
        l.append(random.randint(0,1))
        l.append(random.randint(0,2))

        assert l[0] == 0
        assert l[1] == 1
        assert l[2] >= 0 and l[2] <= 1
        assert l[3] >= 0 and l[3] <= 2
        l = []

        # set operation
        assert len(s) == 0
        s.add(None)
        assert len(s) == 1
        s.add('k1')
        s.add('k2')
        assert len(s) == 3
        s1 = s.copy()
        s2 = s
        s.clear()
        assert len(s) == 0
        assert len(s1) == 3
        assert len(s2) == 0
        s.add('k1')
        s.add('k2')
        assert len(s) == 2

        d.clear()
        l.append(len(d))
        d['d1'] = {}
        d['d2'] = {}
        assert len(d) == 2

        l.append(len(d))
        assert l[0] == 0
        assert l[1] == 2

        l.clear()
        assert len(l) == 0

        d['d1']['k1'] = None
        d['d1']['k2'] = 'v2'
        d['d1']['k3'] = 'v3'
        d['d2']['k1'] = 'v1'
        d['d2']['k2'] = 'v2'
        assert len(d) == 2
        assert len(d['d1']) == 3
        assert len(d['d2']) == 2

        l.append(len(d['d1']))

        dc1 = d.copy()
        dc2 = d
        dcd1 = d['d1'].copy()
        dcd2 = d['d1']
        d['d1'].clear()
        d.clear()
        assert len(d) == 0
        assert len(dc1) == 2
        assert len(dc2) == 0
        assert len(dcd1) == 3
        assert len(dcd2) == 0

        d.clear()
        d['k4'] = 'v4'
        d['k3'] = 'v3'
        d['k2'] = 'v2'
        d['k1'] = 'v1'
        l = d.keys()
        s = set(l)
        assert 'k1' in s
        assert 'k2' in s
        assert 'k3' in s
        assert 'k4' in s
        assert 'k5' not in s

        refk = {'k1','k2','k3','k4'}
        refv = {'v1','v2','v3','v4'}

        for k,v in d.items():
            assert k in refk
            assert v in refv

        assert 'kv' not in refk
        assert 'kv' not in refv
        assert '' not in refk
        assert None not in refk

        d = None
        reached = False
        try:
            for k in d: # this should except because cannot iterate None
                pass
        except Exception as e:
            reached = True
        assert reached

        d = {}
        for k,v in d.items():
            pass

        p('testMiscCalls passed')

    def testSyscall(self):
        p('system ls | wc')
        v = os.system('ls .. | wc')
        p(v)
        p(os.system('ls | wc'))

        p('system pwd')
        v = os.system('pwd')
        p(v)

        p('\nnow try subprocess way')

        task = subprocess.Popen(['ls','..'], stdout=subprocess.PIPE)
        v = task.stdout.read()
        p(v.decode('utf-8'))

        p('now try pipe command ls | wc')
        t1 = subprocess.Popen(['ls'], stdout=subprocess.PIPE)
        t2 = subprocess.Popen(['wc'], stdin=t1.stdout, stdout=subprocess.PIPE)
        t1.stdout.close()
        out,err = t2.communicate()
        p(out.decode('utf-8'))

    def testFileRead(self, fname = 'input/filetest1.txt'):
        if os.path.isfile(fname):
            fh = open(fname, 'r')
            for line in fh:
                p(line)
            fh.close()

    def testDependencyStructure(self):
        DependencyTest().t()

    def testGossip(self):
        gossip.TestGossip.test()

    def testQueue(self):
        q = queue.Queue()
        for i in range(0, 10):
            q.put(item=i)
        i = 0
        while not q.empty():
            v = q.get()
            assert v == i
            i += 1


        q = queue.PriorityQueue()
        q.put(3,'v3')
        q.put(1,'v1')
        q.put(2,'v2')
        i = 1
        while not q.empty():
            v = q.get()
            assert v == i
            i += 1
        p('queue test passed')

    def testTimersAndDates(self):
        tbegms = time.time()
        tbegnsperf = time.perf_counter_ns()
        time_since_epoch = time.localtime()
        p('time_since_epoch {}'.format(time_since_epoch))
        gm_time = time.gmtime()
        p('gm_time {}'.format(gm_time))
        curtime = time.time()
        p('time.time() num seconds since epoch, as floating point = {}'.format(curtime))
        p('time calendar: {}'.format(time.ctime()))
        p('time calendar + 1 year: {}'.format(time.ctime(time.time() + 60*60*24*365)))
        p('time clock: {}'.format(time.clock()))
        p('strptime: {}'.format(time.strptime(time.ctime())))
        p('strptime formatted: {}'.format(time.strftime('%a %b %d %H:%M:%S %Y'.format(time.ctime()))))
        tendms = time.time()
        tendnsperf = time.perf_counter_ns()
        tdifms = tendms - tbegms
        tdifms = int(round(tdifms * 1000))
        tdifns = tendnsperf - tbegnsperf
        p('time elapsed ms: {} , {}'.format(tdifms, tdifns))

        tbegnsperf = time.perf_counter_ns()
        time.sleep(1)
        tendnsperf = time.perf_counter_ns()
        tdifns = tendnsperf - tbegnsperf
        tdifus = tdifns / 1000
        tdifms = tdifus / 1000
        tdifcs = tdifms / 10
        tdifds = tdifcs / 10
        p('time elapsed after 1s sleep: {} ms'.format(tdifms))

        tbegnsperf = time.perf_counter_ns()
        time.sleep(0.05)
        tendnsperf = time.perf_counter_ns()
        tdifns = tendnsperf - tbegnsperf
        tdifus = tdifns / 1000
        tdifms = tdifus / 1000
        p('time elapsed after 50ms sleep: {} ms'.format(tdifms))


    def testInnerFunction(self):
        def innerF(v1,v2):
            return v1,v2
        v1,v2 = innerF(2,3)
        assert v1 == 2
        assert v2 == 3

    def testReturnTuple(self):
        def returnTuple(sizetuple, listval):
            if len(listval) < sizetuple or sizetuple < 1 or sizetuple > 5:
                p('invalid sizing of testReturnTuple')
                return None
            size = len(listval)
            v0 = None
            v1 = None
            v2 = None
            v3 = None
            v4 = None
            if size >= 1:
                v0 = listval[0]
            if size >= 2:
                v1 = listval[1]
            if size >= 3:
                v2 = listval[2]
            if size >= 4:
                v3 = listval[3]
            if size >= 5:
                v4 = listval[4]
            if sizetuple == 1:
                return v0
            if sizetuple == 2:
                return v0,v1
            if sizetuple == 3:
                return v0,v1,v2
            if sizetuple == 4:
                return v0,v1,v2,v3
            if sizetuple == 5:
                return v0,v1,v2,v3,v4

        v0,v1,v2 = returnTuple(3,[10,20,30,40,50,60])
        assert v0 == 10
        assert v1 == 20
        assert v2 == 30
        p('test passed')

    def testStringConversion(self):
        def intit(k):
            try:
                d = int(k)
            except Exception as e:
                p('exception')
                p(e)
                return None
            return d

        s = 'a1'
        for k in s:
            p(intit(k))
            p('--------')
        p('ord and chr')
        p('--------')
        for k in s:
            p(k)
            p(ord(k))
            p(chr(ord(k)))
            p('--------')

    def test_read_gzip_dict(self):
        a = []
        with gzip.open('input/dictionary.gz','r') as f:
            for line in f:
                a.append(line)
        for i in range(0, 10):
            p(a[i].decode('utf-8').strip())
        p('len of dic {}'.format(len(a)))

    def test_multiprocessor(self):
        pool = multiprocessing.Pool(3)

    def test_missing_value(self):
        # ascii to int
        def a2i(v):
            vi = 0
            for i in range(0,len(v)):
                c = v[i]
                ci = ord(c)
                ci = ci & 0xff
                vi = vi << 8 | ci
            return vi

        def i2a(v):
            vs = ''
            while v != 0:
                vb = v & 0xff
                vc = chr(vb)
                vs = vc + vs
                v = v >> 8
            return vs

        a = [
            'Bob joe',
            'bobby Jim',
            'willy Wonka',
            'Willy Wonka II',
            'will turner',
            'jack Sparrow',
            'captain Jack Sparrow',
            'frodo baggins',
            'big brother',
            'winston smith'
        ]

        aint = []
        for v in a:
            aint.append(a2i(v))

        atxt = []
        for v in aint:
            atxt.append(i2a(v))

        vxor = 0
        for v in aint:
            vxor ^= v
        vxoro = vxor

        #p('{}'.format(vxor))

        l = [
            'Bob joe',
            'bobby Jim',
            'willy Wonka',
            'Willy Wonka II',
            'will turner',
            'captain Jack Sparrow',
            'frodo baggins',
            'big brother',
            'winston smith'
        ]

        for v in l:
            vi = a2i(v)
            vxor ^= vi
        v = i2a(vxor)
        assert v == 'jack Sparrow'
        p('{}'.format(v))
        p('this only works for 1 missing value')

    def test_random_out(self):
        relate_types = ['friend','friend','friend','friend','relative','colleague','colleague','enemy']

        d = {}
        d['friend'] = ['relative','colleague']
        d['relative'] = ['friend','colleague','enemy']
        d['colleague'] = ['friend','relative','enemy']
        d['enemy'] = ['relative','colleague']

        ctr = 0
        s = set()
        listitems = [i for i in range(0,25)]
        num_ppl = len(listitems)

        for i in range(0,num_ppl):
            numlinks = random.randint(1,5)
            s.clear()
            s.add(i)
            res = myclasses.Myutils.choose(listitems,numlinks,s)
            if res is None or len(res) == 0:
                p('error!')
                return
            for j in res:
                numtypes = random.randint(1,3)
                idx = random.randint(0,len(relate_types)-1)
                t = relate_types[idx]
                s.clear()
                if numtypes > 1:
                    res = myclasses.Myutils.choose(d[t],numtypes-1,s)
                    for v in res:
                        s.add(v)
                s.add(t)
                for v in s:
                    p('insert into relations_small (gid,idsrc,iddst,relationtype) values ({},{},{},"{}");'.format(ctr,i,j,v))
                    ctr += 1

    def test_choose(self):
        array = [1,2,3,4,5]
        setexclude = set()
        setexclude.add(2)
        setexclude.add(3)

        ret = myclasses.Myutils.choose(array,3,setexclude)
        assert ret is not None
        assert 1 in ret
        assert 2 not in ret
        assert 3 not in ret
        assert 4 in ret
        assert 5 in ret
        assert len(ret) == 3
        p(ret)

        setexclude.clear()
        setexclude.add(2)

        ret = myclasses.Myutils.choose(array,4,setexclude)
        assert ret is not None
        assert 1 in ret
        assert 2 not in ret
        assert 3 in ret
        assert 4 in ret
        assert 5 in ret
        assert len(ret) == 4
        p(ret)

        p('test_choose passed')

    def test_isinstance(self):
        l = [1,2,3]
        le = []
        se = set()
        s = set()
        s.add(1)
        s.add(2)
        de = {}
        d = {'k1':1,'k2':2}
        vs = 'hello'
        vi = 1

        assert isinstance(l,list)
        assert isinstance(le,list)
        assert not isinstance(vs,list)
        assert isinstance(vs,str)
        assert not isinstance(vs,int)
        assert isinstance(vi,int)
        assert not isinstance(vi,str)
        assert isinstance(se,set)
        assert isinstance(s,set)
        assert not isinstance(l,set)
        assert isinstance(de,dict)
        assert isinstance(d,dict)
        assert not isinstance(s,dict)

        bc = MyBaseClass()
        assert isinstance(bc, MyBaseClass)
        assert not isinstance(bc, dict)

        p('test_isinstance pass')


    def test(self):
        #Tests.testCmdLoop1()
        #self.testMyClass2()
        #self.testMiscCalls()
        #self.testSyscall()
        #self.testGossip()
        #self.testDependencyStructure()
        #self.testSortDictList();
        #self.testQueue()
        #self.testTimersAndDates()
        #self.testStringConversion()
        #self.test_read_gzip_dict()
        #self.test_missing_value()
        #self.test_choose()
        #self.test_random_out()
        self.test_isinstance()
        #self.testReturnTuple()
        #Tests.testArgParse()
        #self.testTimeDiff('/Users/ngwayne/Documents/docs_work/CURLS/logs/tmp.txt')
        #self.testNumbers()
        #self.testDict()
        #self.testString()
        #self.testRegex()
        #self.testSHA256()
        #Tests.testReadXMLFile()
        #Tests.testDiffJSON(filename1='input/testinputsmall.json',filename2='input/testinputsmall1.json')
        #self.testListCompare()
        #Tests.testFileJSON()
        #self.testSort()
        #self.testFileOp()
        #Tests.testFileTXT('./logtmp/test/filetxt.txt')
        pass

#!/usr/local/bin/python3

import sys
sys.path.append('../algos')
import os
import os.path
import getopt
import fileinput
import subprocess
import re
import string
import datetime
import numpy
import copy
import math
import calendar
import cmd
import collections
from collections import deque
from collections import OrderedDict
import urllib.request as url
import pathlib
import algos
from src.main import myclasses
import myclasses
#import src.main.myclasses
#from src.algos import algos
#import algos
import json
import unittest
import argparse
#from src.main import gossip
import gossip
import abc
import gzip
import multiprocessing
#from src.main import asynciotests
import asynciotests
from enum import Enum
from enum import auto
import inspect
import asyncio
import time
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import random
import threading
import queue
import aiohttp
import uuid
import logging
import hashlib
import zlib
import datetime
import numpy
import requests

global_output_to_file_ = False
global_fh_ = None

def p(s):
    global global_output_to_file_
    global global_fh_
    print(s)
    if(global_output_to_file_):
        if(global_fh_ is None):
            global_fh_ = open('output_debug.log','w')
        global_fh_.write(s + '\n')

class ENUMTEST1(auto):
    CAT = auto()
    DOG = auto()
    MOUSE = auto()
    TREE = auto()

class ENUMTEST2(Enum):
    CAT = 1
    DOG = 2
    MOUSE = 3
    TREE = 4

'''
0           000:359                                         0 moved
0,1         000:179,180:359                                 180 moved
0,1,2       000:119,120:239,240:359                         
0,1,2,3     000:089,090:179,180:269,270:359                 
0,1,2,3,4   000:071,072:143,144:215,216:287,288:359         
'''
class HashRing:
    def __init__(self):
        pass

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
        #self._global_simple_queue = queue.SimpleQueue()
        self._global_deque = collections.deque()
        #self._global_multiprocessing_manager = multiprocessing.Manager()
        #self._global_multiprocessing_queue = self._global_multiprocessing_manager.Queue()
        #SimpleQueue objects should only be shared between processes through inheritance
        #self._global_multiprocessing_queue = multiprocessing.SimpleQueue()
        #self._global_multiprocessing_queue = multiprocessing.Queue()
        pass

    def top_level_count(self,id, max):
        i = 0
        while i < max:
            i += 1
        return id

    def top_level_sleep(self, id, ms):
        s = ms / 1_000
        time.sleep(s)
        return id

    @staticmethod
    def p1(s):
        print(s)

    def test_old_cases(self):
        def p2(self,s):
            print(s)

        def t1():
            t = myclasses.ClassTest1()
            p('{0}'.format(t.getV1()))
            p('{0}'.format(t.getV3()))
            t.setV1(11)
            p('{0}'.format(t.getV1()))
            t.setV1(12)
            p('{0}'.format(t.getV1()))

        def t2():
            v = self.utils.readfile('inputrequest.json')
            p(v)
            vjson = self.utils.getJsonFromString(v)
            p('accessing json stuff')
            p('{0}'.format(vjson['id']))
            p('{0}'.format(vjson['site']['domain']))

            if 'id' in vjson:
                p('id exists = {0}'.format(vjson['id']))
            else:
                p('id not exists')

            if 'id' in vjson['iii'][10]['v']['ext']:
                p('id exists = {0}'.format(vjson['iii'][10]['v']['ext']['id']))
            else:
                p('id not exists')

            if 'breakfast' in vjson['iii'][10]['v']['ext']:
                p('breakfast exists = {0}'.format(vjson['iii'][10]['v']['ext']['breakfast']))
            else:
                p('breakfast not exists')

            p('length of is {0}'.format(len(vjson['iii'])))

            vjson['iii'][10]['v']['ext']['id'] = vjson['iii'][10]['v']['ext']['id'] + 1
            vjson['iii'][10]['v']['ext']['id'] += 1

            p('id exists = {0}'.format(vjson['iii'][10]['v']['ext']['id']))

        def t4():
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

        def t5():
            p('val: {0}'.format(self.utils.getRandString(5)))
            p('val: {0}'.format(self.utils.getRandString(5, charsettype='n')))
            p('val: {0}'.format(self.utils.getRandString(5, charsettype='x')))

        def t6():
            p('{0}'.format(self.utils.getDatetimeMicro()))
            p('{0}'.format(self.utils.getTimeCurMillis()))

        def t7():
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

        def t8():
            # illustrate variable in if gets propagated out
            flag = False
            if flag:
                v = 10
            else:
                v = 20
            p('v is {0}'.format(v))

        def t9():
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

        def t11():
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

    def t10(self):
        Tests.p1('hello world 1')   # has no self
        self.p2('hello world 2')    # has self
        p('hello world 3')          # has no self

    @staticmethod
    def testPickle(self):
        pass

    @staticmethod
    def testCrypto(self):
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



    def testDependencyStructure(self):
        DependencyTest().t()

    def testGossip(self):
        gossip.TestGossip.test()



    def test_utils_module(self):

        def testSHA256():
            s = 'the cat in the hat'
            h = myclasses.Myutils.hashSHA256(s)
            p(s)
            p(h)


        def test_random_out():
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


        def test_choose():
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
        def test_inner_main():
            test_choose()

        test_inner_main()



    def test_yield_syntax(self):
        def yield_func1():
            yield 1
            yield 2
            yield 3

        def yield_func2(n):
            for i in range(n):
                yield i

        def yield_func3():
            yield 11
            yield 12
            yield 13
            yield 14

        def yield_func1_yield1():
            for v in yield_func3():
                yield v

        def yield_func1_yield_from():
            yield from yield_func3()

        def test_yield():

            def f_gen(min, max):
                for i in range(min, max):
                    p('f_gen: {}'.format(i))
                    yield i

            def f_con(min, max):
                f = f_gen(min,max)
                for v in f:
                    p('f_con: {}'.format(v))

            f_con(1,5)

            p('passed {}'.format(inspect.stack()[0][3]))

        def test_yield_func1():
            p('this prints the generator')
            f = yield_func1()
            p(f)

            p('this loop prints the values')

            ctr = 0
            for v in f:
                p(v)
                ctr += 1
            for v in f:
                p(v)
                ctr += 1
            assert ctr == 3

            ctr = 0
            f = yield_func1()
            for v in f:
                ctr += 1
            assert ctr == 3

            # yield loop
            ctr = 0
            f = yield_func2(4)
            for v in f:
                ctr += 1
            assert ctr == 4

            # use next to get the next value, exception if out of range
            f = yield_func2(4)
            assert next(f) == 0
            assert next(f) == 1
            assert next(f) == 2
            assert next(f) == 3

            flag = False
            try:
                assert next(f) == None
            except Exception as e:
                flag = True
                pass
            assert flag

            # this is new generator, so next always returns 0
            assert next(yield_func2(4)) == 0
            assert next(yield_func2(4)) == 0

            # test double yield
            f = yield_func1_yield1()
            assert next(f) == 11
            assert next(f) == 12
            assert next(f) == 13

            # test yield from
            f = yield_func1_yield_from()
            ctr = 0
            for v in f:
                ctr += 1
            assert ctr == 4

            p('done')
        def test_inner_main():
            test_yield_func1()

        test_inner_main()

    def test_foo(self, v1, v2):
        p('test_foo:{}:{}'.format(v1,v2))
        return v1

    def test_async_concepts(self):

        def getopt_kwargs(k, default, **kwargs):
            if k in kwargs:
                return kwargs[k]
            return default

        def get_kwargs(k, **kwargs):
            return getopt_kwargs(k, None, **kwargs)

        async def test_async(id, **kwargs):
            ms          = get_kwargs('ms', **kwargs)
            debug       = getopt_kwargs('debug', False, **kwargs)
            q           = get_kwargs('q', **kwargs)
            is_return   = getopt_kwargs('is_return', False, **kwargs)

            if(debug):
                p('test_async beg id:{} ms:{}'.format(id, ms))
            if q is not None:
                q.put('test_async beg id:{} ms:{}'.format(id, ms))
            if ms is not None:
                ts = ms / 1000
                await asyncio.sleep(ts)
            if(debug):
                p('test_async end id:{} ms:{}'.format(id, ms))
            if q is not None:
                q.put('test_async end id:{} ms:{}'.format(id, ms))
            if(is_return):
                return id

        async def test_sync(id, **kwargs):
            ms          = get_kwargs('ms', **kwargs)
            debug       = getopt_kwargs('debug', False, **kwargs)
            q           = get_kwargs('q', **kwargs)
            is_return   = getopt_kwargs('is_return', False, **kwargs)

            if(debug):
                p('test_sync beg id:{} ms:{}'.format(id, ms))
            if q is not None:
                q.put('test_async beg id:{} ms:{}'.format(id, ms))
            if ms is not None:
                ts = ms / 1000
                time.sleep(ts)
            if(debug):
                p('test_sync end id:{} ms:{}'.format(id, ms))
            if q is not None:
                q.put('test_async end id:{} ms:{}'.format(id, ms))
            if(is_return):
                return id

        async def wrapper_async(id, **kwargs):
            return await test_async(id, **kwargs)

        def wrapper_sync(id, **kwargs):
            return test_sync(id, **kwargs)

        def test_task():
            q = queue.SimpleQueue()

            def resetq():
                while not q.empty():
                    q.get()

            def checker(expected_val):
                ctr = 0
                while not q.empty():
                    v = q.get()
                    ctr += 1
                assert ctr == expected_val

            async def test_task_return_1():
                t = asyncio.create_task(test_sync(10, debug=True, is_return=False))
                result = await t
                p('test_task_return_1: {}'.format(result))
            def test_1():
                #t = test_task_return_1
                loop = asyncio.get_event_loop()
                loop.run_until_complete(test_task_return_1())
            def test_1_0():
                loop = asyncio.get_event_loop()
                loop.run_until_complete(test_sync(10, debug=True, is_return=False))


            async def test_task_return_2():
                t = asyncio.create_task(test_async(10, debug=True, q=q, is_return=False))
                result = await t
                p('test_task_return_2: {}'.format(result))
            def test_2():
                #t = test_task_return_1
                p('here')
                loop = asyncio.get_event_loop()
                loop.run_until_complete(test_task_return_2())


            async def test_task_return_3():
                return asyncio.create_task(test_async(10, debug=False, q=q, is_return=False))

            def test_3():
                t = test_task_return_3
                loop = asyncio.get_event_loop()
                loop.run_until_complete(t())
                checker(2)

            def callback_get_result(future):
                result = future.result()
                p('callback_get_result:{}'.format(result))
                return result

            async def test_task_return_4_0():
                # returns task with result() 10
                return asyncio.create_task(test_async(10, debug=False, q=q, is_return=True))
            async def test_task_return_4_1():
                # returns value id
                return await asyncio.create_task(test_async(10, debug=False, q=q, is_return=True))
            async def test_task_return_4_2():
                # returns value None
                return await asyncio.create_task(test_async(10, debug=False, q=q, is_return=False))
            async def test_task_return_4_3():
                # returns task with result() None
                return asyncio.create_task(test_async(10, debug=False, q=q, is_return=False))
            async def test_task_return_4_4():
                # returns task with result() 10 wait 500, MUST BE EXTERNALLY AWAITED!
                return asyncio.create_task(test_async(10, ms=500, debug=False, q=q, is_return=True))
            async def test_task_return_4_5():
                # returns value id wait 500
                return await asyncio.create_task(test_async(10, ms=500, debug=False, q=q, is_return=True))
            async def test_task_return_4_6():
                # returns value None wait 500
                return await asyncio.create_task(test_async(10, ms=500, debug=False, q=q, is_return=False))
            async def test_task_return_4_7():
                # returns task with result() None wait 500, MUST BE EXTERNALLY AWAITED!
                return asyncio.create_task(test_async(10, ms=500, debug=False, q=q, is_return=False))
            async def test_task_return_5_0(loop):
                # returns task with result() 10
                return loop.run_in_executor(test_sync(10, debug=False, q=q, is_return=True))
            async def test_task_return_5_1(loop):
                # returns value id
                return await loop.run_in_executor(test_sync(10, debug=False, q=q, is_return=True))
            async def test_task_return_5_2(loop):
                # returns value None
                return await loop.run_in_executor(test_sync(10, debug=False, q=q, is_return=False))
            async def test_task_return_5_3(loop):
                # returns task with result() None
                return loop.run_in_executor(test_sync(10, debug=False, q=q, is_return=False))
            async def test_task_return_5_4(loop):
                # returns task with result() 10 wait 500, MUST BE EXTERNALLY AWAITED!
                return loop.run_in_executor(test_sync(10, ms=500, debug=False, q=q, is_return=True))
            async def test_task_return_5_5(loop):
                # returns value id wait 500
                return await loop.run_in_executor(test_sync(10, ms=500, debug=False, q=q, is_return=True))
            async def test_task_return_5_6(loop):
                # returns value None wait 500
                return await loop.run_in_executor(test_sync(10, ms=500, debug=False, q=q, is_return=False))
            async def test_task_return_5_7(loop):
                # returns task with result() None wait 500, MUST BE EXTERNALLY AWAITED!
                return loop.run_in_executor(test_sync(10, ms=500, debug=False, q=q, is_return=False))
            async def test_task_return_6_0(loop):
                # returns task with result() 10
                return asyncio.run_coroutine_threadsafe(test_sync(10, debug=False, q=q, is_return=True), loop)
            async def test_task_return_6_1(loop):
                # returns value id
                return await asyncio.run_coroutine_threadsafe(test_sync(10, debug=False, q=q, is_return=True), loop)
            async def test_task_return_6_2(loop):
                # returns value None
                return await asyncio.run_coroutine_threadsafe(test_sync(10, debug=False, q=q, is_return=False), loop)
            async def test_task_return_6_3(loop):
                # returns task with result() None
                return asyncio.run_coroutine_threadsafe(test_sync(10, debug=False, q=q, is_return=False), loop)
            async def test_task_return_6_4(loop):
                # returns task with result() 10 wait 500, MUST BE EXTERNALLY AWAITED!
                return asyncio.run_coroutine_threadsafe(test_sync(10, ms=500, debug=False, q=q, is_return=True), loop)
            async def test_task_return_6_5(loop):
                # returns value id wait 500
                return await asyncio.run_coroutine_threadsafe(test_sync(10, ms=500, debug=False, q=q, is_return=True), loop)
            async def test_task_return_6_6(loop):
                # returns value None wait 500
                return await asyncio.run_coroutine_threadsafe(test_sync(10, ms=500, debug=False, q=q, is_return=False), loop)
            async def test_task_return_6_7(loop):
                # returns task with result() None wait 500, MUST BE EXTERNALLY AWAITED!
                return asyncio.run_coroutine_threadsafe(test_sync(10, ms=500, debug=False, q=q, is_return=False), loop)

            def test_4_0():
                loop = asyncio.get_event_loop()
                future = loop.run_until_complete(test_task_return_4_0())
                assert future.result() == 10
                checker(2)

            def test_4_1():
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete(test_task_return_4_1())
                assert result == 10
                checker(2)

            def test_4_2():
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete(test_task_return_4_2())
                assert result == None
                checker(2)

            def test_4_3():
                loop = asyncio.get_event_loop()
                future = loop.run_until_complete(test_task_return_4_3())
                assert future.result() == None
                checker(2)

            def test_4_4():
                loop = asyncio.get_event_loop()
                future = loop.run_until_complete(test_task_return_4_4())
                flag = False
                try:
                    assert future.result() == 10  # result is not set because no wait
                except Exception as e:
                    flag = True
                assert flag
                checker(1)

            def test_4_4_1():
                async def inner_wait():
                    return await test_task_return_4_4()
                loop = asyncio.get_event_loop()
                task = loop.run_until_complete(inner_wait())
                result = loop.run_until_complete(task)
                assert result == 10
                checker(2)

            def test_4_4_2():

                async def inner_wait():
                    return await asyncio.create_task(test_task_return_4_4())

                async def inner_wait_2():
                    task = asyncio.create_task(test_task_return_4_4())
                    task.add_done_callback(callback_get_result)
                    return await task

                loop = asyncio.get_event_loop()
                task = loop.run_until_complete(inner_wait())
                result = loop.run_until_complete(task)
                assert result == 10
                checker(2)

                resetq()
                task = loop.run_until_complete(inner_wait_2())
                result = loop.run_until_complete(task)
                assert result == 10
                checker(2)

            def test_4_5():
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete(test_task_return_4_5())
                assert result == 10
                checker(2)

            def test_4_6():
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete(test_task_return_4_6())
                assert result == None
                checker(2)

            def test_4_7():
                loop = asyncio.get_event_loop()
                future = loop.run_until_complete(test_task_return_4_7())
                try:
                    assert future.result() == None  # result is not set because no wait
                except Exception as e:
                    flag = True
                assert flag
                checker(1)


            def test_5():
                loop = asyncio.get_event_loop()
                loop.run_until_complete(asyncio.create_task(test_async(10, debug=False, q=q, is_return=True)))
                checker(2)

            def test_6():
                t = asyncio.create_task(test_async(10, debug=False, q=q, is_return=True))
                loop = asyncio.get_event_loop()
                loop.run_until_complete(t)
                checker(2)

            '''
            this seems to run forever. how to stop?
            '''
            def test_7():
                def start_worker(loop):
                    asyncio.set_event_loop(loop)
                    loop.run_forever()

                loop = asyncio.get_event_loop()
                loop_worker = asyncio.new_event_loop()
                t = threading.Thread(target=start_worker, args=(loop_worker,))
                t.start()
                loop_worker.stop()
                t.join()

            def test_8():
                def start_worker(loop):
                    asyncio.set_event_loop(loop)
                    loop.run_forever()

                resetq()
                loop = asyncio.get_event_loop()
                loop_worker = asyncio.new_event_loop()
                t = threading.Thread(target=start_worker, args=(loop_worker,))
                t.start()
                loop_worker.stop()
                t.join()

            def inner_main():
                '''
                test_task_return_1() # error! never awaited!
                test_task_return_2() # error! never awaited!
                test_1_0()
                test_2()
                test_3()
                test_5()    # error! test_async never awaited
                test_6()    # error! test_async never awaited
                test_4_0()  # ok
                resetq()
                test_4_1()  # ok
                resetq()
                test_4_2()  # ok
                resetq()
                test_4_3()  # ok
                resetq()
                test_4_4()  # ok
                resetq()
                test_4_5()  # ok
                resetq()
                test_4_6()  # ok
                resetq()
                test_4_7()  # ok
                test_4_4_1()
                test_4_4_1()
                test_4_4_2()
                '''

                test_7()

            inner_main()

        def inner_main():
            test_task()
            p('test_task inner_main done')

        inner_main()


    def test_async_concepts_old(self):

        def test_asynciotests():
            asynciotests.AsyncIOTests().test()

        async def test_async_sleep(id, ms=None, debug=False, is_return=False, q=None):
            if(debug):
                p('test_async_sleep beg id:{} ms:{}'.format(id, ms))
            if q is not None:
                q.put('test_async_sleep beg id:{} ms:{}'.format(id, ms))
            if ms is not None:
                ts = ms / 1000
                await asyncio.sleep(ts)
            if(debug):
                p('test_async_sleep end id:{} ms:{}'.format(id, ms))
            if q is not None:
                q.put('test_async_sleep end id:{} ms:{}'.format(id, ms))
            if(is_return):
                return id

        def test_sync_sleep(id, ms=None, debug=False, is_return=False, q=None):
            if(debug):
                p('test_sync_sleep beg id:{} ms:{}'.format(id, ms))
            if q is not None:
                q.put('test_async_sleep beg id:{} ms:{}'.format(id, ms))
            if ms is not None:
                ts = ms / 1000
                time.sleep(ts)
            if(debug):
                p('test_sync_sleep end id:{} ms:{}'.format(id, ms))
            if q is not None:
                q.put('test_async_sleep end id:{} ms:{}'.format(id, ms))
            if(is_return):
                return id

        def test_task():
            async def test_task_return_1():
                t = asyncio.create_task(test_sync_sleep(10, 0, True, False, None))
                await t
            async def test_task_return_2():
                t = asyncio.create_task(test_async_sleep(10, 0, True, False, None))
                await t
                return t.result()
            def inner_main():
                pass
            inner_main()

        def test_syntax_async_array():

            def test_forever_loop():
                p('test_forever_loop')
                fs = [test_async_sleep(i) for i in range(5)]
                assert len(fs) == 5
                loop = asyncio.get_event_loop()
                taskl = [loop.create_task(f) for f in fs]
                try:
                    p('test_syntax_async_array running forever, do ctl-c to kill')
                    loop.run_forever()
                    p('test_syntax_async_array should not be here')
                    assert False
                except KeyboardInterrupt:
                    p('KeyboardInterrupt received, as expected')
                finally:
                    p('clean up test_syntax_async_array')
                    loop.stop()

            def test_run_until_complete_futures():
                p('test_run_until_complete_futures')
                fs = [test_async_sleep(i) for i in range(5)]
                assert len(fs) == 5
                loop = asyncio.get_event_loop()
                for f in fs:
                    loop.run_until_complete(f)

            def test_run_until_complete_gather_futures():
                p('test_run_until_complete_gather_futures')
                fs = [test_async_sleep(i) for i in range(5)]
                assert len(fs) == 5
                loop = asyncio.get_event_loop()
                loop.run_until_complete(asyncio.gather(*fs))

            def test_run_until_complete_task():
                p('test_run_until_complete_task')
                fs = [test_async_sleep(i) for i in range(5)]
                assert len(fs) == 5
                loop = asyncio.get_event_loop()
                taskl = [loop.create_task(f) for f in fs]
                for t in taskl:
                    loop.run_until_complete(t)

            def test_run_until_first_complete_futures():
                p('test_run_until_first_complete_futures')
                fs = [test_async_sleep(i) for i in range(5)]
                assert len(fs) == 5
                loop = asyncio.get_event_loop()
                res = loop.run_until_complete(asyncio.wait(fs, return_when=asyncio.FIRST_COMPLETED))
                p('finished:{} unfinished:{}'.format(len(res[0]), len(res[1])))
                if(len(res[1]) != 0):
                    finished,unfinished = loop.run_until_complete(asyncio.wait(res[1]))
                    p('finishing up now: finished:{} unfinished:{}'.format(len(finished), len(unfinished)))

            #test_forever_loop()
            #test_run_until_complete_task()
            #test_run_until_complete_futures()
            #test_run_until_complete_gather_futures()
            test_run_until_first_complete_futures()

        async def test_sync_sleep(id, ms, q):
            ts = ms / 1000
            q.put('beg test_sync_sleep id {} sleep {} ms'.format(id, ms))
            time.sleep(ts)
            q.put('end test_sync_sleep id {} sleep {} ms'.format(id, ms))
            return id

        async def test_sync_sleep_exec(id, ms, q, exec):
            ts = ms / 1000
            q.put('beg test_sync_sleep id {} sleep {} ms'.format(id, ms))
            time.sleep(ts)
            q.put('end test_sync_sleep id {} sleep {} ms'.format(id, ms))
            return id

        async def test_async_sleep(id, ms, q):
            ts = ms / 1000
            q.put('beg test_async_sleep id {} sleep {} ms'.format(id, ms))
            await asyncio.sleep(ts)
            q.put('end test_async_sleep id {} sleep {} ms'.format(id, ms))
            return id

        async def test_wrapper_sync_sleep(id, ms, q):
            return await test_sync_sleep(id, ms, q)

        async def test_wrapper_sync_sleep_exec(id, ms, q, exec, loop):
            return await asyncio.wait([loop.run_in_executor(exec, test_sync_sleep_exec, id, ms, q, exec)])

        async def test_wrapper_async_sleep(id, ms, q):
            return await test_async_sleep(id, ms, q)

        def test_loop_sleep_sync():
            q = queue.SimpleQueue()
            #fs = [test_sync_sleep(i, 100, q) for i in range(10)]
            fs = [test_wrapper_sync_sleep(i, 100, q) for i in range(10)] # wrapper makes no difference
            loop = asyncio.get_event_loop()
            #loop.run_until_complete(asyncio.gather(*fs))
            loop.run_until_complete(asyncio.wait(fs)) # wait, gather makes no difference in time elapsed
            while not q.empty():
                p(q.get())


        def test_loop_sleep_sync_separate_executor():
            '''
            '''
            q = queue.SimpleQueue()
            executor = ThreadPoolExecutor()
            loop = asyncio.get_event_loop()
            fs = [test_wrapper_sync_sleep_exec(i, 100, q, executor, loop) for i in range(10)] # wrapper makes no difference
            #fs = [loop.run_in_executor(executor, test_wrapper_sync_sleep, i, 100, q) for i in range(10)] # wrapper makes no difference
            loop.run_until_complete(asyncio.wait(fs)) # wait, gather makes no difference in time elapsed
            while not q.empty():
                p(q.get())

        def test_loop_async_loop_separate_blocking_loop():
            '''
            async loop using separate worker loop to call blocking function
            '''


            def test_sync_sleep(id, ms, q):
                ts = ms / 1000
                p('beg test_sync_sleep id {} sleep {} ms'.format(id, ms))
                time.sleep(ts)
                p('end test_sync_sleep id {} sleep {} ms'.format(id, ms))
                return id

            async def test_sync_sleep_async_wrapper(id, ms, q):
                return test_sync_sleep(id, ms, q)

            def start_worker(worker_loop):
                asyncio.set_event_loop(worker_loop)
                worker_loop.run_forever()

            async def test_wrapper_sync_sleep_worker_future(id, ms, q, loop, loop_worker):
                ts = ms / 1000
                future = asyncio.run_coroutine_threadsafe(test_sync_sleep_async_wrapper(id, ms, q), loop_worker)
                await asyncio.sleep(ts)
                # must fetch future, else get pending task error
                #future.result()
                return future

            def test_inner_main():
                q = queue.SimpleQueue()
                loop = asyncio.get_event_loop()
                loop_worker = asyncio.new_event_loop()
                threading.Thread(target=start_worker, args=(loop_worker,)).start()
                fs = []
                for i in range(10):
                    f = test_wrapper_sync_sleep_worker_future(i, 500, q, loop, loop_worker)
                    fs.append(f)
                #fs = [test_wrapper_sync_sleep_worker_future(i, 500, q, loop, loop_worker) for i in range(10)]
                loop.run_until_complete(asyncio.wait(fs)) # wait, gather makes no difference in time elapsed
                #loop_worker.run_until_complete(asyncio.wait(fs)) # wait, gather makes no difference in time elapsed
                for f in fs:
                    f.get()
                    #f.result()
                loop_worker.stop()
                loop.stop()
                #loop_worker.call_soon_threadsafe(loop_worker.stop)
            try:
                test_inner_main()
                p('passed test_loop_async_loop_separate_blocking_loop')
            except Exception as e:
                p(e)
            finally:
                p('finally test_loop_async_loop_separate_blocking_loop')

        def test_loop_sleep_sync_separate_worker_loop():
            '''
            async loop using separate worker loop to call blocking function
            '''

            async def test_sync_sleep(id, ms, q):
                ts = ms / 1000
                q.put('beg test_sync_sleep id {} sleep {} ms'.format(id, ms))
                time.sleep(ts)
                q.put('end test_sync_sleep id {} sleep {} ms'.format(id, ms))
                return id

            def start_worker(worker_loop):
                asyncio.set_event_loop(worker_loop)
                worker_loop.run_forever()

            async def test_wrapper_sync_sleep_worker_future(id, ms, q, loop, loop_worker):
                future = asyncio.run_coroutine_threadsafe(test_sync_sleep(id, ms, q), loop_worker)
                future.result()

            async def test_wrapper_sync_sleep_worker_no_future_async(id, ms, q, loop, loop_worker):
                # cannot do return await because Future can;t be used in await expression
                #return await asyncio.run_coroutine_threadsafe(test_sync_sleep(id, ms, q), loop_worker)
                return asyncio.run_coroutine_threadsafe(test_sync_sleep(id, ms, q), loop_worker)

            def test_wrapper_sync_sleep_worker_no_future_sync(id, ms, q, loop, loop_worker):
                return asyncio.run_coroutine_threadsafe(test_sync_sleep(id, ms, q), loop_worker)

            p('beg test_loop_sleep_sync_separate_worker_loop')

            q = queue.SimpleQueue()

            loop = asyncio.get_event_loop()
            loop_worker = asyncio.new_event_loop()
            threading.Thread(target=start_worker, args=(loop_worker,)).start()
            # with sync call, it is error: asyncio.Future, coroutine, or awaitable is required
            #fs = [test_wrapper_sync_sleep_worker_no_future_sync(i, 1000, q, loop, loop_worker) for i in range(10)]
            fs = [test_wrapper_sync_sleep_worker_no_future_async(i, 1000, q, loop, loop_worker) for i in range(10)]

            loop.run_until_complete(asyncio.wait(fs)) # wait, gather makes no difference in time elapsed

            #while not q.empty():
            #    p(q.get())
            #for task in asyncio.Task.all_tasks():
            #    task.cancel()

            #loop.stop()
            #loop.close()
            #loop_worker.stop()
            #loop_worker.close()
            p('done test_loop_sleep_sync_separate_worker_loop')

        def test_loop_sleep_async():
            q = queue.SimpleQueue()
            #q = asyncio.Queue() # put has to be awaited if using asyncio.Queue
            #fs = [test_async_sleep(i, 100, q) for i in range(10)]
            fs = [test_wrapper_async_sleep(i, 100, q) for i in range(10)] # wrapper makes no difference
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(fs))
            while not q.empty():
                p(q.get())

        def test_asyncio_semaphore_many_futures():
            async def test_async_sleep(id, ms, q, semaphore):
                async with semaphore:
                    ts = ms / 1000
                    q.put('beg test_async_sleep id {} sleep {} ms'.format(id, ms))
                    await asyncio.sleep(ts)
                    q.put('end test_async_sleep id {} sleep {} ms'.format(id, ms))
                    return id

            p('start  test_asyncio_semaphore')
            semaphore = asyncio.Semaphore(3) # max of 3 workers
            q = queue.SimpleQueue()
            l = [test_async_sleep(id, 100, q, semaphore) for id in range(20)]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(l))
            while not q.empty():
                p(q.get())

            # Let's also finish all running tasks:
            pending = asyncio.Task.all_tasks()
            loop.run_until_complete(asyncio.gather(*pending))

            p('passed test_asyncio_semaphore')

        def inner_main():
            '''
            test_asyncio_semaphore_many_futures()
            test_syntax_async_array()
            test_loop_sleep_async()
            test_loop_sleep_sync_separate_executor()
            test_asynciotests()
            test_loop_sleep_sync()
            test_loop_async_loop_separate_blocking_loop()
            test_loop_sleep_sync_separate_worker_loop()
            '''
            test_loop_async_loop_separate_blocking_loop()

        inner_main()
        p('passed test_async_loops')


    def test_multithread_concepts(self):

        def test_threadpool_threads():

            def waiting_op(id, ms_sleep, semaphore, q):
                s_sleep = ms_sleep / 1_000
                with semaphore:
                    q.put('id:{} sleep'.format(id))
                    time.sleep(s_sleep)
                    q.put('id:{} wake'.format(id))

                '''
                with semaphore:
                    stuff
    
                is the same as
    
                semaphore.acquire()
                stuff
                semaphore.release()
                
                '''

            def task(n, id, semaphore, q):
                q.put('beg id:{} n:{}'.format(id, n))
                for i in range(n):
                    waiting_op(id, 50, semaphore, q)
                q.put('end id:{} n:{}'.format(id, n))

            num_threads = 10
            num_semaphore = 3
            num_loops = 5
            q = queue.SimpleQueue()
            p('------------ num_threads {} num_semaphores {}'.format(num_threads, num_semaphore))
            semaphore = threading.Semaphore(num_semaphore)
            executor = futures.ThreadPoolExecutor(max_workers=num_threads)
            lthreads = []
            for i in range(0, num_threads):
                t = threading.Thread(target=task, args=(num_loops, i, semaphore, q))
                lthreads.append(t)
            for t in lthreads:
                t.start()
            p('------------ start threads wait')
            for t in lthreads:
                t.join()
            while not q.empty():
                p(q.get())
            p('------------ done test_threadpool')

        def test_threadpool_futures():

            def waiting_op(id, ms_sleep, semaphore, q):
                s_sleep = ms_sleep / 1_000
                with semaphore:
                    q.put('id:{} sleep'.format(id))
                    time.sleep(s_sleep)
                    q.put('id:{} wake'.format(id))

                '''
                with semaphore:
                    stuff
    
                is the same as
    
                semaphore.acquire()
                stuff
                semaphore.release()
                
                '''

            def task(n, id, semaphore, q):
                q.put('beg id:{} n:{}'.format(id, n))
                for i in range(n):
                    waiting_op(id, 50, semaphore, q)
                q.put('end id:{} n:{}'.format(id, n))

            num_threads = 10
            num_semaphore = 3
            num_loops = 5
            q = queue.SimpleQueue()
            p('------------ num_threads {} num_semaphores {}'.format(num_threads, num_semaphore))
            semaphore = threading.Semaphore(num_semaphore)
            executor = futures.ThreadPoolExecutor(max_workers=num_threads)
            lfuture = []
            for i in range(0, num_threads):
                f = executor.submit(task, n=num_loops, id=i, semaphore=semaphore, q=q)
                lfuture.append(f)
            p('------------ start futures wait')
            futures.wait(lfuture)
            while not q.empty():
                p(q.get())
            p('------------ done test_threadpool')
            #executor.shutdown()


        def test_asyncio_semaphore():
            semaphore = asyncio.Semaphore(3) # not threadsafe, async only

        def test_threaded_semaphore():
            semaphore = threading.Semaphore(3) # thread safe, but cannot asyncio await

        def testThreadPrint(msg, numloops, lock):
            for i in range(0, numloops):
                lock.acquire(True)
                p(msg)
                lock.release()

        def testThreading():
            lock = threading.Lock()
            t1 = threading.Thread(target=testThreadPrint, args=('a',5,lock))
            t2 = threading.Thread(target=testThreadPrint, args=('b',5,lock))
            t1.start()
            t2.start()

        def testGILSpeed():
            '''
            GIL is a lock for multi threads to sync on reference countdown for GC, effectively
            serializing thread to single runner at a given time, which makes this not useful
            for CPU intensive activity, but OK for IO intensive activity. Use multiproc for
            CPU intensive activity.
            '''
            local_max = 1_000_000
            num_thread = 16
            q = queue.SimpleQueue()
            locallist = []

            def count(id, max):
                i = 0
                while i < max:
                    i += 1
                q.put('done count {}'.format(id))
                #p('done count {}'.format(id))
                return id

            def count_fixed():
                i = 0
                while i < local_max:
                    i += 1
                q.put('done count {}'.format(i))

            def sleep_ms(id, ms):
                s = ms / 1_000
                time.sleep(s)
                q.put('done sleep {}'.format(id))
                return id


            def inner_test_cpu():
                def thread_multi_cpu():
                    l = [threading.Thread(target=count,args=(i,local_max,)) for i in range(num_thread)]
                    [t.start() for t in l]
                    [t.join() for t in l]
                    return True

                def no_thread_cpu():
                    for i in range(num_thread):
                        count(i, local_max)
                    return True

                def thread_executor_pool_cpu():
                    executor = futures.ThreadPoolExecutor(max_workers=4)
                    lfutures = [executor.submit(count, i, local_max) for i in range(num_thread)]
                    futures.wait(lfutures)
                    return True

                def processes_cpu():
                    listp = [multiprocessing.Process(target=count,args=(i,local_max,)) for i in range(num_thread)]
                    [p.start() for p in listp]
                    [p.join() for p in listp]
                    return True

                def proc_pool_cpu():
                    pool = multiprocessing.Pool(processes=4)

                    # NOTE
                    # cannot use count! MUST USE TOP LEVEL METHOD because of pickle error!
                    # pool uses queue.Queue to pass tasks, and must be pickleable, and only
                    # methods defined in top level module are pickleable. and method
                    # definition must precede initialization of pool!

                    # same as below
                    #results = []
                    #[results.append(pool.apply_async(self.top_level_count, args=(i, local_max, localq,))) for i in range(num_thread)]

                    results = [pool.apply_async(self.top_level_count, args=(i, local_max,)) for i in range(num_thread)]
                    pool.close()
                    pool.join()
                    [r.get() for r in results]
                    return True

                p('start testGILSpeed CPU {} threads count {}'.format(num_thread, local_max))
                l = [thread_multi_cpu, no_thread_cpu, thread_executor_pool_cpu, processes_cpu, proc_pool_cpu]
                for f in l:
                    tb = int(time.time_ns()/1_000_000)
                    f()
                    te = int(time.time_ns()/1_000_000)
                    td = te - tb
                    p('runtime {} ms {}'.format(td, f.__name__))
                    while not q.empty():
                        q.get()

                p('done inner test cpu')


            def inner_test_io():
                def thread_multi_io():
                    l = [threading.Thread(target=sleep_ms,args=(i, 1000,)) for i in range(num_thread)]
                    [t.start() for t in l]
                    [t.join() for t in l]
                    return True

                def no_thread_io():
                    for i in range(num_thread):
                        sleep_ms(i, 1000)
                    return True

                def thread_executor_pool_io():
                    #executor = futures.ThreadPoolExecutor(max_workers=4)   # this is slowest
                    #executor = futures.ThreadPoolExecutor(max_workers=8)   # medium
                    executor = futures.ThreadPoolExecutor()                 # this is fastest
                    lfutures = [executor.submit(sleep_ms, i, 1000) for i in range(num_thread)]
                    futures.wait(lfutures)
                    return True

                def processes_io():
                    listp = [multiprocessing.Process(target=sleep_ms,args=(i,1000,)) for i in range(num_thread)]
                    [p.start() for p in listp]
                    [p.join() for p in listp]
                    return True

                def proc_pool_io():
                    pool = multiprocessing.Pool(processes=4)

                    results = [pool.apply_async(self.top_level_sleep, args=(i, 1000,)) for i in range(num_thread)]
                    pool.close()
                    pool.join()
                    [r.get() for r in results]
                    return True

                p('start testGILSpeed IO {} threads count {}'.format(num_thread, local_max))
                l = [thread_multi_io, no_thread_io, thread_executor_pool_io, processes_io, proc_pool_io]
                for f in l:
                    tb = int(time.time_ns()/1_000_000)
                    f()
                    te = int(time.time_ns()/1_000_000)
                    td = te - tb
                    p('runtime {} ms {}'.format(td, f.__name__))
                    while not q.empty():
                        q.get()

                p('done inner test IO')

            inner_test_cpu()
            inner_test_io()


        def test_inner_main():
            '''
            test_threadpool_futures()
            '''
            testGILSpeed()

        test_inner_main()


    def test_files_and_json(self):

        def testReadWriteFile():
            filename = 'input/filetest1.txt'
            if not os.path.isfile(filename):
                fh = open(filename,'w')
                fh.close()
            fh = open(filename,'r')
            lines = fh.readlines()
            fh.close()
            data = ''.join(lines)


        def test_read_gzip_dict():
            a = []
            with gzip.open('input/dictionary.gz','r') as f:
                for line in f:
                    a.append(line)
            for i in range(0, 10):
                p(a[i].decode('utf-8').strip())
            p('len of dic {}'.format(len(a)))

        def diffJsonSubtree(json):
            pass

        def testDifflib(self):
            pass

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

        def testFileOp():
            res = Tests.testFileCreateDestroy('./logtmp/test/filetxt.txt')
            p(res['filename'])
            lines = res['data'].split('\n')
            for line in lines:
                p(line)

        def testFileJSON(filename='input/testinputsmall.json'):
            vjson = myclasses.Myutils.getFileJSON(filename)
            p('{0}'.format(json.dumps(vjson, indent=2)))
            p('-----')
            myclasses.Myutils.traverseDictOld('',vjson,printStats=True)

        def testDiffJSON(filename1, filename2):
            json1 = myclasses.Myutils.getFileJSON(filename1)
            json2 = myclasses.Myutils.getFileJSON(filename2)
            res = myclasses.Myutils.jsondiff(json1=json1,json2=json2,prefix='',printStats=True,printKeysOnly=True)
            p('{0} diff {1} = {2}'.format(filename1, filename2, res))

        def testDiffJSONTest():
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

        def testReadXMLFileVAST():
            r = myclasses.Myutils.getFileXML(filename='input/testinput.xml')
            myclasses.Myutils.parseXML(r)

        def testFileXML(filename):
            pass


        def testFileOperations():
            pass

        def test_inner_main():
            testDiffJSONTest()

        test_inner_main()



    def test_syntax(self):

        def testQueue():
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

        def testInnerFunction():
            def innerF(v1,v2):
                return v1,v2
            v1,v2 = innerF(2,3)
            assert v1 == 2
            assert v2 == 3

        def randint(max):
            return random.randint(0,max)

        def testMiscCalls():
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

            d = {'k1':'v1','k2':'v2'}
            assert len(d.keys()) == 2
            assert isinstance(d, dict)
            p('testMiscCalls passed')

        def test_sys_call():

            flag = False

            if flag:
                # this has no redirect output, so pwd is printed to stdout
                # adding false flag to not run this so no output to console, but it works
                v = os.system('pwd')
                assert v == 0
                v = os.popen('ls .. | wc').read()
                v = os.system('ls | wc')

            # output is redirected to v in this case
            v = os.popen('pwd').read()
            assert re.search(r'/python/src/main',v)

            task = subprocess.Popen(['ls','..'], stdout=subprocess.PIPE)
            v = task.stdout.read()

            t1 = subprocess.Popen(['ls'], stdout=subprocess.PIPE)
            t2 = subprocess.Popen(['wc'], stdin=t1.stdout, stdout=subprocess.PIPE)
            t1.stdout.close()
            out,err = t2.communicate()
            v = out.decode('utf-8')

            t = subprocess.run(['ps','aux'], stdout=subprocess.PIPE)
            t = t.stdout.decode('utf-8')
            assert re.search(r'python', t)

            t = subprocess.run('ps aux | grep python', shell=True, stdout=subprocess.PIPE)
            t = t.stdout.decode('utf-8')
            assert re.search(r'grep python', t)

            flag = False
            if flag:
                # this runs and directs output to stdout, so no output redirect
                t = subprocess.run('ps aux | grep python', shell=True)
                assert t.stdout == None
                # call is equivalent to run(...).returncode, so no output
                t = subprocess.call('ps aux | grep python', shell=True)
                assert t == 0

            pass

        def testFileRead(fname = 'input/filetest1.txt'):
            if os.path.isfile(fname):
                fh = open(fname, 'r')
                for line in fh:
                    p(line)
                fh.close()

        def testTimersAndDates():
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

        def test_isinstance():
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

        def test_function_args():
            def foo(arg1int, sizelist, arglist, arg2int):
                assert len(arglist) == sizelist
                p('foo: {}:{}:{}:{}'.format(arg1int, sizelist, arglist, arg2int))
                return arg1int+arg2int

            def fooargs(*args): # for arbitrary number of args
                p('fooargs: * {}'.format([*args]))
                p('fooargs:   {}'.format(args))
                p('print individuals')
                for a in args:
                    p('a:{}'.format(a))

            def fookwargs(**kwargs):    # for keyword decoding
                if kwargs is None:
                    p('fookwargs is None')
                    return
                if len(kwargs) == 0:
                    p('fookwargs is empty')
                    return
                p('fookwargs:    {}'.format(kwargs))
                p('fookwargs:  * {}'.format([*kwargs]))
                #p('fookwargs: ** {}'.format([**kwargs])) # invalid!
                for k in kwargs:
                    p('k:{}:{}'.format(k, kwargs[k]))

            def fooargskwargs(toplevelonly,*args, **kwargs):
                p('fooargskwargs: args:{}, kwargs:{}'.format(args, kwargs))
                if(toplevelonly):
                    return
                fooargs(args)
                fookwargs(**kwargs) # this unpacks, and ends up being **kwargs in function
                #fookwargs(kwargs)  # this is wrong! passing in dict


            def test_args():
                l1 = [1,2,3,4,5]
                kv = {'k1':'v1','k2':'v2','k3':'v3'}
                p('call foo part 1')
                fooargskwargs(True, l1, kv)  # invalid because *args is tuple of l1,kv ([1,2,3,4,5],{'k1':'v1','k2':'v2','k3':'v3'})
                p('call foo part 2')
                fooargskwargs(True, *l1, *kv) # invalid because *l1,*kv is tuple: (1,2,3,4,5,'k1','k2','k3'})
                p('call foo part 3')
                fooargskwargs(True, l1, *kv) # invalid because *l1,*kv is tuple: ([1,2,3,4,5],'k1','k2','k3'})
                p('call foo part 4')
                fooargskwargs(False, l1, k1='v1',k2='v2',k3='v3') # invalid because *l1,*kv is tuple: ([1,2,3,4,5],'k1','k2','k3'})
                fookwargs()

            def foolist():
                l1 = [1,2,3,4,5]
                l2 = 1,2,3,4,5
                p('l1 {}'.format(l1))
                p('l2 {}'.format(l2))
                p('l1[4] {}'.format(l1[4]))
                p('l2[4] {}'.format(l2[4]))
                *l3,v1=l1
                p('unpacking *l3,v1 = l1')
                p('l3 {}'.format(l3))
                p('v1 {}'.format(v1))
                p('unpacking *l3 to [] {}'.format([*l3]))                   # [1, 2, 3, 4]
                p('normal     l3 to [] {}'.format(l3))                      # [1, 2, 3, 4]
                p('unpacking *l3 to elements {},{},{},{}'.format(*l3))      # 1,2,3,4
                p('unpacking *l3 to [] {}'.format(*l3))                     # 1
                kv = {'k1':'v1','k2':'v2','k3':'v3'}
                p('  kv:{}'.format(kv))                                     # {'k1':'v1','k2':'v2','k3':'v3'}
                p(' *kv:{}'.format([*kv]))                                  # {'k1','k2','k3'}
                #p('**kv:{}'.format([**kv])) # invalid



            def test_specific_kwargs():
                def foo_kwargs0(**kwargs):
                    ctr = 0
                    args = ['arg1','arg2','arg3']
                    for arg in args:
                        if(arg in kwargs):
                            p('{} detected:{}'.format(arg, kwargs[arg]))
                            ctr += 1
                    return ctr
                def foo_kwargs1(v, **kwargs):
                    ctr = 0
                    args = ['arg1','arg2','arg3']
                    for arg in args:
                        if(arg in kwargs):
                            p('{} detected:{}'.format(arg, kwargs[arg]))
                            ctr += 1
                    return ctr
                def call_foo_kwargs():
                    assert foo_kwargs0() == 0
                    assert foo_kwargs0(arg1=2) == 1
                    assert foo_kwargs0(argx=2) == 0
                    assert foo_kwargs0(arg1=1,arg2=2,arg3=3) == 3
                    assert foo_kwargs1(1) == 0
                    assert foo_kwargs1(1,arg1=2) == 1
                    assert foo_kwargs1(1,argx=2) == 0
                    assert foo_kwargs1(1,arg1=1,arg2=2,arg3=3) == 3

                call_foo_kwargs()

            def test_range_for_loop():
                a = []
                for i in range(1,5):
                    a.append(i)
                assert a == [1,2,3,4]
                a = []
                for i in range(1,6,2):
                    a.append(i)
                assert a == [1,3,5]
                a = []
                for i in range(5,0,-1):
                    a.append(i)
                assert a == [5,4,3,2,1]

                s = 'abcde'
                a = []
                for i in range(len(s)):
                    a.append(s[i:i+2])  # this goes out of bounds, but python knows, so no exception
                assert a == ['ab','bc','cd','de','e']

                p('test_range_loop passed')

            def test():
                '''
                foolist()
                test_args()
                test_specific_kwargs()
                '''
                test_range_for_loop()
                test_sys_call()
                p('test syntax passed')

            test()

        def testListCompare():
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

        def testSetIntersect():
            l1 = [10,8,3,6]
            l2 = [6,8,10,3]
            l3 = [1,2,3,4]
            res = set(l1).intersection(l2)
            p(res)
            res = set(l1).intersection(l3)
            p(res)

        def test_random_choices():
            strv = string.ascii_lowercase + string.digits
            v = ''.join(random.choices(strv, k=5))
            p(v)
            id = str(uuid.uuid4())
            p('uuid:{}'.format(id))

        def test_echo(v):
            p('test_echo {}'.format(v))
            return v

        def test_inner_function():
            def test_inner_function_1(v):
                return v
            def test_inner_function_2(v):
                return v

            l = []
            l.append(test_inner_function_1(10))
            l.append(test_inner_function_2(20))
            p(l)

        def test_methodcall_by_name():
            p('f name is {}'.format(inspect.stack()[0][3]))

            v1 = getattr(Tests, 'test_foo')(self,20,30)
            assert v1 == 20

            foo = getattr(Tests, 'test_foo')
            v1 = foo(self,31,32)
            assert v1 == 31

            p('passed test_methodcall_by_name')

        def test_ranges():
            l = range(10)
            assert len(l) == 10
            l = range(0,10,2) # 0-9, step 2, so 5 elements
            assert len(l) == 5
            l = range(0,-10,-1) # 0- -9, step -1
            assert len(l) == 10
            l = [i for i in range(3)]
            assert len(l) == 3
            l = [3,5,4,1,2]
            l.sort()
            lref = [i for i in range(1,6)]
            v = set(l).intersection(lref)
            assert len(v) == 5

            set1 = set([1,2,3])
            set2 = set([2,3,4])
            set3 = set1 & set2
            assert len(set3) == 2

            idx = 0
            assert len(l) == len(lref)
            for idx in range(len(l)):
                assert l[idx] == lref[idx]

            l = [range(10)]
            ctr = 0
            for v in l:
                ctr += 1
            assert ctr == 1 # just range(10) itself
            l = [i for i in range(10)]
            ctr = 0
            for v in l:
                ctr += 1
            assert ctr == 10

            l1 = l[1:1]
            assert len(l1) == 0
            l1 = l[1:2]
            assert len(l1) == 1
            l1 = l[1:]
            assert len(l1) == 9
            l1 = l[:1]
            assert len(l1) == 1

            l = [i for i in range(5)]
            l1 = l.copy()
            l1.reverse()
            p(l)
            p(l1)


        def test_missing_value():
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



        def test_queue_list_deque_array():
            #p('start test_queue_list_deque_array')
            size = 10
            q = queue.SimpleQueue()
            dq = collections.deque()
            a = [i for i in range(size)]
            [dq.append(v) for v in a]
            [q.put(v) for v in a]
            l = list(dq)
            assert len(dq) == size
            assert q.qsize() == size
            assert q.empty() == False
            assert len(l) == size

            flag = False
            try:
                l = list(q) # q is not iterable
            except Exception as e:
                flag = True
            assert flag

            while not q.empty():
                q.get()
            assert q.empty() == True

            dq.clear()
            assert len(dq) == 0

            q = queue.Queue()
            [q.put(v) for v in a]
            assert q.qsize() == size
            while not q.empty():
                q.get()
            assert q.empty() == True and q.qsize() == 0



            p('passed test_queue_list_deque_array')

        def testSortDictList():
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

        def testNumbers():
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

        def testTimeDiff(filename):
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

        def testString():
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


        def test_time(self):
            s = time.time()
            ms = s * 1000
            ns = ms * 1000
            int_ms = int(ms)
            int_s = int(s)
            p(s)
            p(ms)
            p(ns)
            p(int_ms)
            p(int_s)
            ns = time.time_ns()
            p(ns)

        def test_loop(self):
            l = []
            for i in range(0,4):    # stops at 3
                l.append(i)
            assert len(l) == 4
            p('-----')
            l1 = []
            for i in range(4,8):    # stops at 7
                l1.append(i)
            assert len(l1) == 4
            l.append(l1)
            assert len(l) == 5      # because [0,1,2,3,[4,5,6,7]]
            l.pop(4)
            l.extend(l1)
            assert len(l) == 8
            p('pass test_loop')

        '''
        given array of a, we call (i,j) an important reverse pair if i<j and a[i]>a[j]*2
        return the number of important reverse pairs in given array
        '''
        def test_reverse_pairs(self):
            def reverse_pairsv1(a):
                sz = len(a)
                numpairs = 0
                for j in range(sz):
                    for i in range(j):
                        if a[i] > a[j] * 2:
                            numpairs = numpairs + 1
                    pass
            def testcase():
                a = [1,3,2,3,1]
                numpairs = reverse_pairsv1(a)
                assert numpairs == 2
            testcase()

        def get_array_1(num_elements, starting_idx):
            l = []
            for i in range(starting_idx,starting_idx+num_elements):
                l.append(i)
            return l

        def get_array_2(num_elements, starting_idx):
            l = [i for i in range(starting_idx,starting_idx+num_elements)]
            return l

        def test_syntax_loops_and_arrays():
            l = []
            l.append(get_array_2(3,0))
            l.append(get_array_2(3,3))
            p(l)
            pass

        def test_methods_in_list():
            def foo1(v1,v2):
                return v1,v2
            def foo2(v1):
                return v1
            def foo3():
                return True
            def inner_test():
                l = [foo3,foo3]
                r = []
                for f in l:
                    r.append(f())
                for v in r:
                    p(v)
                p('pass inner_test')
            inner_test()

        def testReturnTuple():
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

        def test_gen_arrays():
            # 3 x 4 matrix of 1
            a1 = [[1] * 3 for i in range(4)]
            # 3 x 4 matrix of 0,1,2
            a2 = [[i for i in range(3)] for j in range(4)]
            # 3 x 4 matrix of 0-11
            a3 = [[3*j+i for i in range(3)] for j in range(4)]
            # array of 3 of 1
            a4 = [1] * 3
            # array of 3 of 0,1,2
            a5 = [i for i in range(3)]

            assert len(a1) == 4 and len(a1[0]) == 3
            assert len(a2) == 4 and len(a2[0]) == 3
            assert len(a3) == 4 and len(a3[0]) == 3
            assert len(a4) == 3
            assert len(a5) == 3

            l = [test_echo(i) for i in range(5)]
            assert len(l) == 5


        def inner_main():
            '''
            test_random_choices()
            test_ranges()
            testSortDictList()
            testNumbers()
            testTimeDiff('/Users/ngwayne/Documents/docs_work/CURLS/logs/tmp.txt')
            self.testStringConversion()
            self.testString()
            test_syntax_array()
            test_methods_in_list()
            test_queue_list_deque_array()
            test_isinstance()
            testReturnTuple()
            test_gen_arrays()
            '''
            #test_function_args()
            testMiscCalls()

        inner_main()
        p('passed test_syntax')


    def test_with(self):
        pass


    def test_parse_args(self, argv):
        ctr = 0
        p('test_parse_args')
        for v in argv:
            p('{}: {}'.format(ctr, v))
            ctr += 1
        list_args_short = 'di:o:v' # : is after each required arg, eg i and o

        list_args_verb = [
            'debug'
            'input=',
            'output=',
            'verbose'
        ]

        '''
        -i inputval -o outval -d            # valid
            opts:[(-i,'inputval'),(-o,'outval'),('-d','')]
            args:[]
        -i inputval -d a b c                # valid
            opts:[(-i,'inputval'),('-d','')]
            args:['a','b','c']
        aa bb cc -i inputval -d a b c       # invalid
        '''

        try:
            debug = False
            input = None
            output = None
            verbose = False

            opts, args = getopt.getopt(argv, list_args_short, list_args_verb)
            p('opts: {}'.format(opts))
            p('args: {}'.format(args))

            for opt,arg in opts:
                if opt in ('-d'):
                    debug = True
                elif opt in ('-i','--input'):
                    input = arg
                    pass
                elif opt in ('-o', '--output'):
                    output = arg
                    pass
                elif opt in ('-v'):
                    verbose = True
            p('debug:{} input:{} output:{} verbose:{}'.format(debug, input, output, verbose))
        except Exception as e:
            p(e)
        return opts

    def test_logging(self):
        log_filename = 'logging.py.data.txt'
        logging.basicConfig(filename=log_filename, level=logging.INFO)
        logger1 = logging.getLogger('package1.modulename')
        logging.debug('debug message timestamp: {}'.format(time.time()))
        logging.info('info message timestamp: {}'.format(time.time()))
        for i in range(5):
            logging.debug('debug: i:{} ts:{}'.format(i, time.time()))
            logging.info('info: i:{} ts:{}'.format(i, time.time()))
        with open(log_filename, 'rt') as f:
            for line in f:
                p(line.strip())
        pass

    def test_algos(self):
        algos.algos().test()

    def test_convert_int(self):
        vd = 100.1
        vi = 100
        vsi = str(vi)
        vsd = str(vd)
        assert '100.1' == vsd
        assert '100' == vsi
        vc = int(vsi)
        assert vc == vi
        vc = float(vsd)
        assert vc == vd
        p('pass test_convert_int')

    def test_round_number(self):
        '''
        given a number, round it up to multiple of 5
        '''
        def round_int_to_multiple(v, multiple):
            if(v % multiple != 0):
                remainder = v % multiple
                result = v + (multiple - remainder)
                assert result % multiple == 0

        def test_round_int():
            multiple = 5
            round_int_to_multiple(0, multiple)
            round_int_to_multiple(2, multiple)
            round_int_to_multiple(5, multiple)
            round_int_to_multiple(7, multiple)
            round_int_to_multiple(8, multiple)
            round_int_to_multiple(10, multiple)

        def round_double_to_multiple(v, multiple):
            assert v <= 1.0 and v >= 0.0 and multiple <= 1.0 and multiple >= 0.0
            v_times_100 = int(v * 100)
            multiple_times_100 = int(multiple * 100)
            if(v_times_100 % multiple_times_100 != 0):
                remainder = v_times_100 % multiple_times_100
                result = v_times_100 + (multiple_times_100 - remainder)
                assert result % multiple_times_100 == 0

        def test_round_double():
            multiple = 0.05

            flag = True
            try:
                round_double_to_multiple(-0.0, multiple)
            except Exception as e:
                flag = False
            assert flag

            flag = False
            try:
                round_double_to_multiple(-0.1, multiple)
            except Exception as e:
                flag = True
            assert flag


            flag = False
            try:
                round_double_to_multiple(10, multiple)
            except Exception as e:
                flag = True
            assert flag

            round_double_to_multiple(0.0, multiple)
            round_double_to_multiple(0.03, multiple)
            round_double_to_multiple(0.04, multiple)
            round_double_to_multiple(0.05, multiple)
            round_double_to_multiple(0.06, multiple)
            round_double_to_multiple(0.10, multiple)
            round_double_to_multiple(0.12, multiple)
            round_double_to_multiple(0.15, multiple)
            round_double_to_multiple(0.19, multiple)
            round_double_to_multiple(0.20, multiple)

        test_round_int()
        test_round_double()
        p('passed test_round_number')

    def test_tuple_list_ops(self):
        a1 = [1,2,3]
        a2 = [1,2,3]
        a3 = [2,3,4]
        a4 = [4,3,2]
        a5 = [4,3,2]
        for v1,v2 in zip(a1,a2):        # loop over 2 or more sequences, use zip
            assert v1 == v2

        assert a1 == a2
        assert a1 != a3
        assert a3 != a4
        assert a4 == a5

        a1 = [(1,2,3),(4,5,6),(7,8,9)]
        a2 = [(1,2,3),(4,5,6),(7,8,9)]
        for v1,v2 in zip(a1,a2):        # loop over 2 or more sequences, use zip
            assert v1 == v2

        a1 = [(4,5,6),(7,8,9),(1,2,3)]
        a2 = [(1,2,3),(4,5,6),(7,8,9)]
        a3 = [(4,5,6),(7,8,9),(1,2,3)]
        for v1,v2,v3 in zip(a1,a2,a3):  # loop over 2 or more sequences, use zip
            assert v1 != v2
            assert v1 == v3

        p('passed test_tuple_list_ops')

    def test_set_operations(self):
        set1 = set([1,2,3,4,5])
        set2 = set([4,5,6,7])
        set3 = set([2,3,4])
        set4 = set()
        set4.update(set1)
        set4.update(set2)
        set5 = set1.difference(set2)    # 1,2,3,4,5 - 4,5,6,7 = 1,2,3
        set6 = set2.difference(set1)    # 4,5,6,7 - 1,2,3,4,5 = 6,7
        set7 = set1.intersection(set2)  # 1,2,3,4,5 & 4,5,6,7 = 4,5
        set8 = set()
        for v in range(1,8):
            set8.add(v)
        list1 = [1,2,3,4,5]
        set9 = set(list1)
        assert len(set4) == 7
        assert len(set5) == 3 and 1 in set5 and 2 in set5 and 3 in set5
        assert len(set6) == 2 and 6 in set6 and 7 in set6
        assert len(set7) == 2 and 4 in set7 and 5 in set7
        assert len(set8) == 7
        assert len(set9) == 5

        set10 = set1.copy()
        assert len(set10.difference(set1)) == 0
        set1 = set([(1,2),(3,4),(5,5),(1,4),(6,7)]) # these are sets of tuples!
        set2 = set([(1,2),(3,4),(5,5),(1,4),(6,7)])
        set3 = set([(2,1),(3,4),(5,5),(4,1),(7,6)])
        count = 0
        for t1 in set1:
            v1,v2 = t1
            for t2 in set2:
                v3,v4 = t2
                if v1 == v3 and v2 == v4:
                    count += 1
                    break
        assert count == len(set1)

        # tuple comparison
        lt1 = [(1,2),(2,3),(4,5)]
        lt2 = [(1,2),(2,3),(4,5)]
        lt3 = [(1,2),(2,3),(6,7)]
        lt4 = [(2,2),(3,3),(7,7)]
        lt5 = [(0,2),(1,3),(5,7)]
        assert lt1 == lt2
        assert lt2 != lt3
        assert lt4 > lt3
        assert lt5 < lt4        # compares in order of tuples

        set1 = set()
        set2 = None
        set3 = set()
        set4 = set([1,2,3])
        flag = False
        try:
            set1.update(set2)
        except Exception as e:
            flag = True
        assert flag
        set1.update(set3)
        set1.update(set4)
        assert len(set1.difference(set4)) == 0
        p('passed test_set_operations')

    def test_dict_operations(self):
        d = {}
        d['k1'] = set([1,2,3])
        assert 'k2' not in d
        assert 'k1' in d
        flag = False
        try:
            set1 = d['k2']
        except Exception as e:
            flag = True
        assert flag

        for k,v in d.items():
            assert k == 'k1'
            assert k != 'bogus'

        d['k2'] = set([2,3,4])
        assert 'k2' in d
        d.pop('k2',None)                    # asserts if None not provided
        assert 'k2' not in d
        flag = False
        try:
            d.pop('k3')
            assert 'should have asserted k3'
        except Exception as e:
            flag = True
        assert flag
        d['k2'] = set([2,3,4])
        assert 'k2' in d
        del d['k2']
        assert 'k2' not in d
        p('passed test_dict_operations')
        pass


    pass

    def test_listops(self):
        l = []
        l.append('1,2,3')
        l.append('4,5,6')

    def test_regex_2(self):
        # substitute and groups, using variable regex

        s1         = 'abc 1 2 3 fixed1/3.3 (bbb 1.2) ccc/222.0 (ddd, eee) ffff/1.2.3.4.5 fixed2/30.12 def hij'
        s2 = re.sub(r'fixed1/(.*) fixed2/([\d\.]+)',r'"fixed1/\1 fixed2/\2"', s1)
        assert s2 == 'abc 1 2 3 "fixed1/3.3 (bbb 1.2) ccc/222.0 (ddd, eee) ffff/1.2.3.4.5 fixed2/30.12" def hij'

        r1 = r'fixed1/(.*) fixed2/([\d\.]+)'
        r2 = r'"fixed1/\1 fixed2/\2"'

        s1         = 'abc 1 2 3 fixed1/3.3 (bbb 1.2) ccc/222.0 (ddd, eee) ffff/1.2.3.4.5 fixed2/30.12 def hij'
        s2 = re.sub(r1,r2, s1)
        assert s2 == 'abc 1 2 3 "fixed1/3.3 (bbb 1.2) ccc/222.0 (ddd, eee) ffff/1.2.3.4.5 fixed2/30.12" def hij'

        s1         = 'abc 1 2 3 fixed1/3.3 (bbb 1.2) ccc/22200 (ddd, eee) ffff/1.2.3.4.5 fixed2/30012 def hij'
        s2 = re.sub(r'fixed1/(.*) fixed2/([\d\.]+)',r'"fixed1/\1 fixed2/\2"', s1)
        assert s2 == 'abc 1 2 3 "fixed1/3.3 (bbb 1.2) ccc/22200 (ddd, eee) ffff/1.2.3.4.5 fixed2/30012" def hij'

        s1         = 'abc 1 2 3 fixed1/3.3 (bbb 1.2) ccc/22200 (ddd, eee) ffff/1.2.3.4.5 fixed2/30012  [zz/yy;bb_vv/111.222.3333;] def hij'
        s2 = re.sub(r'fixed1/(.*) fixed2/([\d\.]+)\s+\[(.*)\]',r'"fixed1/\1 fixed2/\2 [\3]"', s1)
        assert s2 == 'abc 1 2 3 "fixed1/3.3 (bbb 1.2) ccc/22200 (ddd, eee) ffff/1.2.3.4.5 fixed2/30012 [zz/yy;bb_vv/111.222.3333;]" def hij'

        s1          = 'a.b.c'
        s2 = re.sub(r'.',r'|',s1)
        assert s2 == '|||||'
        s2 = re.sub(r'\.',r'|',s1)
        assert s2 == 'a|b|c'

        p('pass test_regex2')
        pass


    def test_regex(self):
        s1 = 'k: {1,2,3}.  b: {2,3,4} c: {4,5,6} d: {7,8,9}'
        s2 = 'k: {1,2,3} b:  {2,3,4}   c: {4,5,6} d: {7,8,9}'
        s3 = 'k: {1,2,3} b: {2,3,4}'
        s4 = 'this is date1: 02/01/18 this is date2: 02/02/19 this is date3: 02/03/20, this is not date 020304. this is zip code 95000,95001 95002 this is not zip 95 912345 '

        def get_dict1(s):
            d = {}
            a = re.split(r'\s+', s)
            i = 0
            while i < len(a):
                v = a[i].strip()
                if(re.match(r'^\w+:$', v)):
                    key = v.strip(':')
                    dat = a[i+1]
                    dat = dat.replace('{', '')
                    dat = dat.replace('}', '')
                    ad  = re.split(r',', dat)
                    set1 = set(ad)
                    d[key] = set1
                    i += 2
                else:
                    i += 1
            return d
        def test_grouping(s):
            #p(s)
            m1 = re.findall('\w+:\s+\{.*\}',s2)
            m2 = re.search(r'\s+(\w+)\:\s+{(.*)}', s2)
            m3 = re.findall('\w+:\s+\{[\d+\,]+}',s2)        # this seems to be the right one
            m4 = re.findall('\w+:\s+\{[\d+\,]}',s2)
            m5 = re.findall('\w+:\s+{[\d+\,]+}',s2)         # this seems to be same as m3
            m6 = re.findall('\w+:\s+{[\d,]+}',s2)           # this seems to be same as m3
            v0 = m2.group()
            v1 = m2.group(0)
            v2 = m2.group(1)
            v3 = m2.group(2)
            v4 = m2.groups()
            flag = False
            try:
                v4 = m2.group(3)
            except Exception as e:
                flag = True
            assert flag
            m7 = re.search(r'\s+(\w+)\:\s+{[\d\w,]+}', s2)
            v5 = m7.group()
            v6 = m7.groups()
            v7 = m7.group(0)
            v8 = m7.group(1)
            pass

        def test_parse1():
            s = 'this is date1: 02/01/18 this is date2: 02/02/19 this is date3: 02/03/20, ' + \
                'this is date 02/03/2100 this is not date w02/02/02 this is not date 020304. ' + \
                'this is zip code 95000,95001 95002,95003. 03/01/20. this is not zip ' + \
                '95 912345 919292 188111,717117,81234567' + \
                'this is not a date 01/02/123 this is a date 01/02/2013. '

            a = re.findall('\s(\d{2}/\d{2}/\d{2})[\s,\.]', s)   # group the date (01/02/03)
            set2 = set(a)
            assert len(a) == 4
            set1 = set(['02/01/18','02/02/19','02/03/20','03/01/20'])
            setd = set1.difference(set2)
            assert len(setd) == 0

            a = re.findall('\s\d{2}/\d{2}/\d{2}[\s,\.]', s)   # do not group the date (01/02/03), so includes all the misc symbols
            set2 = set(a)
            assert len(a) == 4
            set1 = set([' 02/01/18 ',' 02/02/19 ',' 02/03/20,',' 03/01/20.'])
            setd = set1.difference(set2)
            assert len(setd) == 0

            a = re.findall('\d{2}/\d{2}/\d{2}', s)   # not accounting for lhs and rhs symbols
            set2 = set(a)
            assert len(a) == 8
            set1 = set(['02/01/18','02/02/19','02/03/20','02/03/21','02/02/02','03/01/20','01/02/12','01/02/20'])
            setd = set1.difference(set2)
            assert len(setd) == 0

            # noncapture non capture non-capture
            # non capture is when you want to group expression, but do not want to save it as matched portion
            # either 2 digit year or 4 digit year but not 3, use NON CAPTURE ?: WITH CAPTURE. contrast with no NON CAPTURE
            a = re.findall(' (\d{2}/\d{2}/(?:\d{2}|\d{4}))[\s,\.]', s)
            set2 = set(a)
            assert len(a) == 6
            set1 = set(['02/01/18','02/02/19','02/03/20','02/03/2100','03/01/20','01/02/2013'])
            setd = set1.difference(set2)
            assert len(setd) == 0

            # bad regex, same as above, but with CAPTURE groups
            # either 2 digit year or 4 digit year but not 3, use NON CAPTURE ?: WITH CAPTURE. contrast with no NON CAPTURE
            # this ONLY returns what is grouped, with is ONLY (\d{2}|\d{4})
            a = re.findall(' \d{2}/\d{2}/(\d{2}|\d{4})[\s,\.]', s)
            set2 = set(a)
            assert len(a) == 6
            assert len(set2) == 5       # because of duplicates
            setd = set1.difference(set2)
            set1 = set(['18','19','20','2100','2013'])
            setd = set1.difference(set2)
            assert len(setd) == 0

            # nested capture groups return tuples as answers
            a = re.findall(' (\d{2}/\d{2}/(\d{2}|\d{4}))[\s,\.]', s)
            set2 = set(a)
            assert len(a) == 6
            assert len(set2) == 6
            setd = set1.difference(set2)
            set1 = set([('02/01/18','18'),('02/02/19','19'),('02/03/20','20'),('02/03/2100','2100'),('03/01/20','20'),('01/02/2013','2013')])
            setd = set1.difference(set2)

            # get all zip codes, which are 5 digits
            # this regex is wrong because it looks for ,zip, ,zip,
            # so result is less than expected
            a = re.findall('[ ,\.;](\d{5})[ ,\.;]',s)
            assert len(a) == 2
            set1 = set(['95000','95002'])
            set2 = set(a)
            assert len(set1.difference(set2)) == 0

            # get all zip codes, which are 5 digits, but this matcher is also wrong
            a = re.findall('[ ,\.;]?(\d{5})[ ,\.;]?',s)
            assert len(a) != 4

            # get all zip codes, which are 5 digits
            a = re.findall(r'\b\d{5}\b',s)
            assert len(a) == 4
            set1 = set(['95000','95001','95002','95003'])
            set2 = set(a)
            assert len(set1.difference(set2)) == 0

            # get all zip codes, which are 5 digits
            a = re.findall(r'\b(\d{5})\b',s)
            assert len(a) == 4
            set1 = set(['95000','95001','95002','95003'])
            set2 = set(a)
            assert len(set1.difference(set2)) == 0

            # not as regex, it returns 0!
            a = re.findall('\b\d{5}\b',s)
            assert len(a) == 0

            # takes all numbers
            a = re.findall('\d{5}',s)
            set1 = set(['02030','95000','95001','95002','95003','91234','91929','18811','71711','81234'])
            assert len(a) == len(set1)

            s = '1234567'

            # how to get 1234 2345 3456 4567?
            # use lookahead capture
            # this syntax is wrong, and returns 4 blanks
            a = re.findall(r'(?=\d{4})',s)
            assert len(a) == 4
            for v in a: assert v == ''

            # how to get 1234 2345 3456 4567?
            # use lookahead capture
            a = re.findall(r'(?=(\d{4}))',s)
            assert len(a) == 4
            set1 = set(['1234','2345','3456','4567'])
            set2 = set(a)
            assert len(set1.difference(set2)) == 0

            pass

        def test_grouping_keyset():
            s = 'k: {1,2,3} b:  {2,3,4}   c: {4,5,6} d: {7,8,9}'

            a = re.findall('[^\s]((\w):\s+{([\w,]+)})',s)               # empty!
            assert len(a) == 0

            a = re.findall('[^\s]((\w+):\s+{([\d,]+)})',s)              # empty!
            assert len(a) == 0

            a = re.findall('\w+:\s+{[\d,]+}',s)                         # better!
            assert len(a) == 4
            set1 = set(a)
            set2 = set(['k: {1,2,3}','b:  {2,3,4}','c: {4,5,6}','d: {7,8,9}'])
            setd = set1.difference(set2)
            assert len(setd) == 0

            a = re.findall('(\w+):\s+{([\d,]+)}',s)                     # this returns tuple
            assert len(a) == 4
            a_cmp = [('k','1,2,3'),('b','2,3,4'),('c','4,5,6'),('d','7,8,9')]
            for i in range(len(a)): assert a[i] == a_cmp[i]

            # loop over 2 or more sequences, use zip
            for v1,v2 in zip(a,a_cmp): assert v1 == v2

        def t1():
            '''
            split into groups as a key:set
            '''
            d = get_dict1(s1)
            assert len(d) == 4
            d = get_dict1(s2)
            assert len(d) == 4
            d = get_dict1(s3)
            assert len(d) == 2

        def t2():
            #test_grouping(s1)
            test_grouping(s2)
            #test_grouping(s3)

        def test_basic_regex():
            s = '     this     is   trimming.'
            a = ['this','is','trimming.']

            v = re.sub(r'\s+',' ', s)
            assert v == ' this is trimming.'
            v = v.strip()
            assert v == 'this is trimming.'

            s1 = s.strip()
            assert s1 == 'this     is   trimming.'

            a1 = s1.split()
            assert len(a1) == 3 and a1 == ['this','is','trimming.']

            a1 = s.split()
            assert len(a1) == 3 and a1 == ['this','is','trimming.']

            a1 = s1.split(' ')
            assert a1 == ['this','','','','','is','','','trimming.']

            a1 = re.split(r'\s+',s1)
            assert a1 == ['this','is','trimming.']

            a1 = re.split(r'\s+',s)
            assert a1 == ['','this','is','trimming.']

            # this does nothing
            s1 = s.replace(r'\s+',' ')
            assert s1 == s

            s1 = re.sub(r'\s+',' ',s)
            assert s1 == ' this is trimming.'
            s1 = s1.strip()
            assert s1 == 'this is trimming.'

            s1 = ';;;this;;;;is;;;trimming.;;'.strip(';')
            assert s1 == 'this;;;;is;;;trimming.'

            s1 = re.sub(r';+',' ','this;;;;is;;;trimming.')
            assert s1 == 'this is trimming.'

            a1 = re.split(r';+',';;;this;;;;is;;;trimming.;;')
            assert a1 == ['','this','is','trimming.','']

            s1 = ';;;this;;;;is;;;trimming.;;'.strip(';')
            a1 = re.split(r';+',s1)
            assert a1 == ['this','is','trimming.']

            # split every third position
            s = 'actbatcatratsathat'
            a = ['act','bat','cat','rat','sat','hat']
            a1 = []
            for i in range(0, len(s), 3):
                a1.append(s[i:i+3])
            a2 = [s[i:i+3] for i in range(0, len(s), 3)]
            assert a1 == a2
            s = 'actbatcatratsathats'
            a2 = [s[i:i+3] for i in range(0, len(s), 3)]
            assert a2 == ['act','bat','cat','rat','sat','hat','s']

            s1 = '  hey, what   are you doing   there?   i am here, ,  not   there.'
            a2 = ['hey','what','are','you','doing','there','i','am','here','not','there']
            a1 = re.findall(r'\w+', s1)
            assert a1 == a2

            # multiple substitutions
            s = ' {1,2,3}, {{2,3,4},{5,6,7}}.'
            v = re.sub(r'[\s{}\.]','',s)
            assert v == '1,2,3,2,3,4,5,6,7'

            # braces matching
            s = ' {1,2,3}, {{2,3,4},{5,6,7}}.'
            a = re.findall(r'\{[\d,\s]+\}',s)
            assert len(a) == 3
            assert a[0] == '{1,2,3}'
            assert a[1] == '{2,3,4}'
            assert a[2] == '{5,6,7}'


            # greedy vs lazy
            # greedy matches til last } seen
            a = re.findall(r'{.*}',s)
            assert len(a) == 1
            assert a[0] == '{1,2,3}, {{2,3,4},{5,6,7}}'

            # lazy matches til first } seen
            a = re.findall(r'{.*?}',s)
            assert len(a) == 3
            assert a[0] == '{1,2,3}'
            assert a[1] == '{{2,3,4}'
            assert a[2] == '{5,6,7}'

            s = 'word:cat word:!@# word:dog'
            v = re.search(r'word:\w+',s)
            assert v
            v = re.search(r'whatever:\w+',s)
            assert not v

            # group matching
            # (()()) -> group|group(1) == (()()), group(2) = () first, group(3) = () second
            s = 'date:[01/01/02:12345,01/01/02:12346,01/01/02:12347,01/02/02:1111]'
            m = re.search(r'((\d{2}/\d{2}/\d{2}):(\d+))',s)
            assert m.group() == '01/01/02:12345'
            assert m.group(1) == '01/01/02:12345'
            assert m.group(2) == '01/01/02'
            assert m.group(3) == '12345'
            a = re.findall(r'((\d{2}/\d{2}/\d{2}):(\d+))',s)
            assert len(a) == 4
            assert a[0] == ('01/01/02:12345','01/01/02','12345')
            assert a[1] == ('01/01/02:12346','01/01/02','12346')
            assert a[2] == ('01/01/02:12347','01/01/02','12347')
            assert a[3] == ('01/02/02:1111','01/02/02','1111')
            pass

        def test_conditional_text_validation():
            '''
            validate that lines of text fit certain rules.
            eg if detect word1, then subsequent has to follow certain order, else etc.
            '''
            pass

        def test_multiline_1():
            a1 = '''
            this is line 1
            this is line 2
            this is line 3
            '''
            a2 = a1.splitlines()
            assert a2[0] == ''
            assert a2[1] == '            this is line 1'
            a3 = [l.lstrip() for l in a2]
            assert a3[1] == 'this is line 1'
            s1 = '\n'.join(a3)
            assert s1 == '\nthis is line 1\nthis is line 2\nthis is line 3\n'

            # what is the starting position of the first letter in line 1 of a2?
            m = re.search(r'\w',a2[1])
            v = m.start()
            assert v == 12
            pass

        def test_pattern_matching_with_capture_groups():
            # find all ABBA patterns
            a = [
                'aehheb',       # y
                'abcde',        # n
                'aehhebc',      # y
                'ehhe',         # y
                'agehhegcb'     # y
            ]
            a = [
                'http://abc.com',
                'https://abc.com',
                'https://abc.com/123',
                'https://abc.bbb.com',
                'http://vvv.net',
                'http://c-now.b-then.com',
                'https://c-now.b-then.com',
                'http://abc.com/here',
                'https://abc.com/here/you',
                'http://abc.com/123/222',
                'https://123.234.432.111',
                'https://123.234.432;111',
                'https://123.234.432-111',
                'https://123.234.432.111/here',
                'http://123.234.432.111/here',
                'ftp://123.234.432.111',
                'https://123.234.432.111/abc?k1=v1&k2=v2',
                'https://bird.box/abc?k1=v1&k2=v2',
                'https://bird.box/abc?k111=v1&k2=v2',
                'https://bird.box/?k111=v1&k2=v2',
                'https://bird.box/k111=v1&k2=v2',
                'https://bird.box/abc?k121=v1&k2=v2',
                'https://bird.box/abc?k1=v1&k2=v2&k3=v3'
            ]
            r = []
            for v in a:
                if(re.search(r'^https?://abc.com', v)): r.append(v)
            assert len(r) == 6
            c = [
                'http://abc.com',
                'https://abc.com',
                'https://abc.com/123',
                'http://abc.com/here',
                'https://abc.com/here/you',
                'http://abc.com/123/222'
            ]
            assert r == c

            r = []
            for v in a:
                if(re.search(r'^https?://\d{3}\.\d{3}\.\d{3}\.\d{3}/?', v)): r.append(v)
            c = [
                'https://123.234.432.111',
                'https://123.234.432.111/here',
                'http://123.234.432.111/here',
                'https://123.234.432.111/abc?k1=v1&k2=v2'
            ]
            assert r == c

            r = []
            for v in a:
                if(re.search(r'^https?://[\w\.]+/\w+\?(\w+)=(\w+)',v)): r.append(v)
            c = [
                'https://123.234.432.111/abc?k1=v1&k2=v2',
                'https://bird.box/abc?k1=v1&k2=v2',
                'https://bird.box/abc?k111=v1&k2=v2',
                'https://bird.box/abc?k121=v1&k2=v2',
                'https://bird.box/abc?k1=v1&k2=v2&k3=v3'
            ]
            assert r == c

            g = re.search(r'^https?://[\w\.]+/\w+\?(\w+)=(\w+)','https://bird.box/abc?k1=v1&k2=v2&k3=v3')
            assert g.group(1) == 'k1' and g.group(2) == 'v1'

            v = re.search(r'^https?://[\w\.]+/\w+\?(.*)','https://bird.box/abc?k1=v1&k2=v2&k3=v3')
            a = re.findall(r'((\w+)=(\w+))',v.group(1))
            assert v.groups() == ('k1=v1&k2=v2&k3=v3',)
            assert v.group(1) == 'k1=v1&k2=v2&k3=v3'
            assert len(a) == 3
            c = [
                ('k1=v1','k1','v1'),
                ('k2=v2','k2','v2'),
                ('k3=v3','k3','v3')
            ]
            assert a == c

            v = re.search(r'^https?://[\w\.]+/\w+\?(.*)','https://bird.box/abc')
            assert v == None
            assert v is None

            s = 'abc key_1_2: {1,2,3,4} key_2_3: {1a,2a,3a} key_3_4: {2,3,4} key_4: {} somethingelse'
            a = re.findall(r'\b([a-zA-Z0-9_]+):\s+{([\w,]+)}',s)
            #a = re.findall(r'\b([\w\_]+):\s+{([\w,]+)}',s)
            assert len(a) == 3
            assert a[0] == ('key_1_2','1,2,3,4')
            assert a[1] == ('key_2_3','1a,2a,3a')
            assert a[2] == ('key_3_4','2,3,4')
            # no match on key_4: {}

            s = 'abc k1: {kv1,kv2,kv3} blah'
            t = re.search(r'k1:\s+{(\w+),(\w+),(\w+)}',s)
            assert len(t.groups()) == 3
            assert t.group(0) == 'k1: {kv1,kv2,kv3}'
            assert t.group(1) == 'kv1'
            assert t.group(2) == 'kv2'
            assert t.group(3) == 'kv3'

            t = re.search(r'(?:this|that) is a string','this is a string')
            assert t.groups() == ()
            assert t.group() == 'this is a string'

            t = re.search(r'(this|that) is a string','this is a string')
            g = t.groups()
            assert t.groups() == ('this',)
            assert t.group() == 'this is a string'

            t = re.search(r'(?:this|that) is a string','that is a string')
            g = t.group()
            assert t.group() == 'that is a string'

            # cannot do repeating subgroups with a first match
            # in this specific case, capture the first group and do separate check on tuple
            a = re.findall(r'key: {(\w+),(\w+)} (\w+): {([\w\,]+)}','key: {k1,v1} key1: {1,2,3} key2: {2,3,4} key3: {3,4,5}')

            pass

        def test_string_validate():
            # ip match

            v = re.search(r'^(\d{1,3}\.?){4}$','123.2.22.211')
            assert v != None
            assert v.group(1) == '211'

            v = re.search(r'^(\d{1,3}\.){3}(\d{1,3})$','123.2.22')
            assert v == None

            v = re.search(r'^(\d{1,3}\.){3}(\d{1,3})$','123.2.22.312')
            assert v != None
            assert v.groups() == ('22.','312',)
            assert v.group() == v.group(0)
            assert v.group(0) == '123.2.22.312'
            assert v.group(1) == '22.'
            assert v.group(2) == '312'

            # non capture
            v = re.search(r'^(?:\d{1,3}\.){3}(\d{1,3})$','123.2.22.312')
            assert v.groups() == ('312',) and v.group(1) == '312'

            v = re.search(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.(\d{1,3})','123.2.22.312')
            assert v.group(1) == '312'

            v = re.search(r'^(\d{1,3})\.\d{1,3}\.\d{1,3}\.(\d{1,3})','123.2.22.312')
            assert v.group(1) == '123'
            assert v.group(2) == '312'

            v = re.search(r'^((\d{1,3})(?:\.)){3}(\d{1,3})$','123.2.22.312')
            assert v.groups() == ('22.','22','312')

            v = re.search(r'^(\d{1,3}\.?){4}','123.2.22.312')
            g = v.group()
            assert g == '123.2.22.312'

            v = re.search(r'^(\d{1,3}[\.$]){4}','123.2.22')
            assert v == None

            # this is exact search
            v = re.search(r'^(\d{1,3}(\.|$)){4}$','123.2.22.234')
            g = v.group()
            assert g == '123.2.22.234'

            # this is exact search
            v = re.search(r'^(\d{1,3}(\.|$)){4}$','123.2.22.234.322')
            assert v == None

            # this is exact search
            v = re.search(r'^(\d{1,3}(\.|$)){4}$','123.2.22')
            assert v == None

            v = re.search(r'^(\d{1,3}\.?){4}$','123.2.22.312.234')
            assert v == None

            v = re.search(r'^(\d{1,3}\.){4}','123.2.22.312.234')
            g = v.group()
            assert g == '123.2.22.312.'

            v = re.search(r'^(\d{1,3}\.){3}(\d{1,3})$','123.2.22.312.2')
            assert v == None

            pass

        def test_all():
            try:
                #t1()
                #t2()
                test_parse1()
                test_grouping_keyset()
                test_basic_regex()
                test_conditional_text_validation()
                test_multiline_1()
                test_pattern_matching_with_capture_groups()
                test_string_validate()
                p('passed test_regex')
            except Exception as e:
                p(e)
                raise e

        test_all()

    def test_list(self):
        l1 = [i for i in range(4)]
        assert l1 == [0,1,2,3]

        l2 = l1.copy()
        assert l2 == [0,1,2,3]

        v = l2.pop()
        assert l2 == [0,1,2]
        assert l1 == [0,1,2,3]
        assert v == 3

        l2.insert(0,3)
        assert l2 == [3,0,1,2]

        l2.append(4)
        assert l2 == [3,0,1,2,4]

        p('pass test_list')

        q = deque()

        q.append(1)
        q.append(2)
        q.append(3)
        q.pop()
        assert len(q) == 2
        s0 = 'tyqbac'
        s1 = sorted(s0)
        assert s0 == 'tyqbac'
        assert s1 == ['a','b','c','q','t','y']
        assert ''.join(s1) == 'abcqty'
        l = []
        l.append('hello this is a sentence\nand another one\n')
        l.append('hello this is a sentence\nand another one\n')
        l.append('hello this is a sentence\nand another one\n')
        assert len(l) == 3
        p('pass test_list')

    def test_arg(self, arg1, arg2):
        p('test pass test_arg {} {}'.format(arg1, arg2))

    @staticmethod
    def test_static_arg(arg1, arg2):
        p('test pass test_static_arg {} {}'.format(arg1, arg2))

    def next_match(self, strval, idx_s, chars):
        l = len(strval)
        if l == 0 or l <= idx_s:
            return None
        for i in range(idx_s, l):
            c = strval[i]
            if c == chars:
                return i
        return None

    # returns the index of
    def match_brace(self, strval, idx_s):
        l = len(strval)
        if l == 0 or l <= idx_s:
            return None

        lifo = []
        last_pushed = strval[idx_s]
        lifo.append(last_pushed)
        last_char = None

        discarded = ''

        for i in range(idx_s+1, l):
            chars = strval[i]
            if chars == '{' or chars == '[' or chars == '(':
                last_pushed = chars
                lifo.append(last_pushed)
            elif chars == '}' and last_pushed != '{' or \
                 chars == ']' and last_pushed != '[' or \
                 chars == ')' and last_pushed != '(':
                break
            elif chars == '}' or chars == ']' or chars == ')':
                lifo.pop()
                if len(lifo) == 0:
                    return i
                last_pushed = lifo[len(lifo)-1]
            elif chars == '/' and last_char == '/':
                return len(lifo) == 0
            else:
                discarded += chars
            last_char = chars

        return None


    def test_match_braces(self):
        #    0 0 0 0 0 1 1 1 1 1 2
        #    0 2 4 6 8 0 2 4 6 8 0
        s = '{a{b{{}}c}}'
        assert len(s) == 11
        res = self.match_brace(s, 0)
        assert res == 10
        res = self.match_brace(s, 1)
        assert res == None
        res = self.match_brace(s, 2)
        assert res == 9

        #    0 0 0 0 0 1 1 1 1 1 2
        #    0 2 4 6 8 0 2 4 6 8 0
        s = '{a{b{{}}c}} '
        assert len(s) == 12
        res = self.match_brace(s, 0)
        assert res == 10
        res = self.match_brace(s, 1)
        assert res == None
        res = self.match_brace(s, 2)
        assert res == 9

        #    0 0 0 0 0 1 1 1 1 1 2
        #    0 2 4 6 8 0 2 4 6 8 0
        s = '{ a { b { { } } c } }'
        assert len(s) == 21
        res = self.match_brace(s, 0)
        assert res == 20
        res = self.match_brace(s, 1)
        assert res == None
        res = self.match_brace(s, 2)
        assert res == None
        res = self.match_brace(s, 4)
        assert res == 18
        res = self.match_brace(s, 8)
        assert res == 14


        #    0 0 0 0 0 1 1 1 1 1 2
        #    0 2 4 6 8 0 2 4 6 8 0
        s = '{a{b{{}c}}'
        assert len(s) == 10
        res = self.match_brace(s, 0)
        assert res == None
        res = self.match_brace(s, 1)
        assert res == None
        res = self.match_brace(s, 2)
        assert res == 9
        res = self.match_brace(s, 5)
        assert res == 6

        p('pass test_match_braces')

    def test_string(self):
        v = 'abc,de,fg,{"hi":"jk","l":["m","n"]},"o":["p q","r s t","uv"]'
        t = ''
        for i in range(4,6):
            t += v[i]
        assert t == 'de'
        assert v[4:6] == 'de'
        assert v[0:3] == 'abc'
        assert v[11:15] == '"hi"'

        v1 = 'abcdefg hijk lmnop'
        assert 'efg' in v1
        assert 'dfg' not in v1
        assert 'abcdefg hijk lmnop' == v1
        assert 'abcdefg hij' in v1
        assert not 'efg'.isdigit()
        assert '123'.isdigit()
        assert 'abc' < 'efg' and 'efg' > 'abc'

        v1 = '2019-01-20'
        assert re.match(r'^\d{4}-\d{2}-\d{2}$', v1)
        v1 = '2019-01-201'
        assert not re.match(r'^\d{4}-\d{2}-\d{2}$', v1)

        # loop string characters
        s = 'this is a string'
        l = len(s)
        assert l == 16
        cnt = 0
        result = ""
        for i in range(l):
            result += s[i:i+1]
            cnt += 1

        assert result == 'this is a string'
        assert cnt == 16 and len(result) == 16

        s_list = [c for c in s]
        assert len(s_list) == len(s)

        # substrings
        v = s[0:1]
        assert v == 't'
        assert not isinstance(v,list)
        v = s[0]
        assert v == 't'
        assert not isinstance(v,list)

        # this is now an array
        v = s_list[0:1]
        assert v != 't'
        assert v[0] == 't'
        assert isinstance(v,list)

        v = s[1]
        assert v == 'h'
        assert not isinstance(v,list)
        v = s[1:2]
        assert v == 'h'
        assert not isinstance(v,list)

        assert s[0:2] == 'th'
        assert s[5:13] == 'is a str'
        assert len(s[5:13]) == 8

        a = ['abc','def','gi','hj']
        assert len(a) == 4
        v = ''.join(a)
        assert len(v) == 10
        v = ','.join(a)
        assert len(v) == 13
        a1 = v.split(',')
        assert len(a1) == 4
        v = 'abc  def   gi     hj    lmn'
        a1 = re.split(r'\s+',v)
        assert len(a1) == 5

        p('pass test_string')
        pass

    def json_to_string(self):
        j = json.loads('[{"a":"1","b":"2"},{"c":"3","d":"4"}]')
        for v in j:
            p(json.dumps(v))
            p(json.dumps(v, sort_keys=True, indent=2))
        pass

    def test_map_of_lists_and_dicts(self):
        def gen_dict(depth,size,prefix):
            def gen_dict_rec(d,depth,size,prefix):
                for i in range(size):
                    k = '{}{}'.format(i,depth)
                    if(depth == 0):
                        d[k] = '{}{}{}'.format(prefix,depth,i)
                    else:
                        d[k] = {}
                        gen_dict_rec(d[k],depth-1,size,prefix)
            d = {}
            gen_dict_rec(d,depth,size,prefix)
            return d
        def gen_list(size,prefix):
            l = []
            for i in range(size):
                l.append('{}{}'.format(prefix,i))
            return l
        def print(d):
            pass
        def run():
            l = []
            l.append(gen_list(2,'a'))
            l.append(gen_list(2,'b'))
            lextend = []
            lextend.extend(gen_list(2,'c'))
            lextend.extend(gen_list(2,'d'))
            l.append(lextend)
            d = gen_dict(1,2,'c')
            l.append(d)
            for v in l:
                if(isinstance(v,list)):
                    p(v)
                elif(isinstance(v,dict)):
                    p(json.dumps(v))
                    p(json.dumps(v, sort_keys=True, indent=2))
            pass
        run()

    def test_external_command_capture(self):
        p('--------------')
        p('run ls -l')
        v = subprocess.run(['ls','-l'])     # this runs and output is stdout
        p('done run ls -l')

        p('--------------')
        p('run ls -l')
        # this redirects output to pipe to v
        v = subprocess.run(['ls','-l'],stdout=subprocess.PIPE)
        p('this is the output')
        p('{}'.format(v.stdout.decode('utf-8')))
        p('done output')
        p('--------------')

        # no need to run this
        flag = False
        if(flag):
            v = subprocess.run(['ls','-l'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
            p('{}'.v.stderr.decode('utf-8'))

            # this doesnt capture output and redirects to null
            v = subprocess.run(['ls','-l'],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
        p('--------------')
        p('run os.system')  # this method allows pipe piping, passes to os so pipe as well
        os.system('ls -l')
        p('--------------')
        p('getoutput method')
        v = subprocess.getoutput('ls -l')
        p('print output')
        p('{}'.format(v))
        p('--------------')
        p('popen method')
        v = os.popen('ls -l')
        p('print output')
        p('{}'.format(v.read()))
        p('--------------')

        p('--------------')
        p('--------------')
        p('--------------')
        p('done test')


        pass

    class test_hashlib:
        '''
        https://docs.python.org/3/library/hashlib.html
        '''
        def list_hashlib(self):
            setv = hashlib.algorithms_available
            for v in setv:
                p(v)

        def test_hash(self):
            sha256 = hashlib.sha256()
            sha256.update(b'hello here')
            sha256.update(b'bye bye')
            v = sha256.hexdigest()
            p('{}'.format(v))

            md5 = hashlib.md5()
            md5.update(b'hello here')
            md5.update(b'bye bye')
            v = md5.hexdigest()
            p('{}'.format(v))


        def is_callable_user_defined(self, s):
            if not callable(getattr(self, s)):
                return False
            if re.search(r'^__', s):
                return False
            return True

        def run_function_map(self):
            l_functions = [ m for m in dir(self) if self.is_callable_user_defined(m)]
            h = {}
            for i in range(len(l_functions)):
                h[i] = l_functions[i]
            return h

        def list_methods(self):
            l = [m for m in dir(self) if self.is_callable_user_defined(m)]
            p(l)

        def run(self, i):
            pass
            #if i in h:
                #getattr(self, h[i])()

        def __init__(self):
            self.h = self.run_function_map()

    def test_call_testhashlib_list(self):
        t = Tests.test_hashlib()
        t.list_methods()

    def test_call_testhashlib(self, i):
        t = Tests.test_hashlib()
        t.run(i)

    def test_list_of_list(self):
        ll = []
        sum_exp = 0
        sum_act = 0
        for i in range(0,3):
            vi = i * 10
            l = []
            ll.append(l)
            for j in range(0,5):
                vj = vi + j
                sum_exp += vj
                l.append(vj)
        cnt_row = 0
        for l in ll:
            cnt_col = 0
            for v in l:
                sum_act += v
                cnt_col += 1
            cnt_row += 1
            assert cnt_col == 5
            #p(l)
        assert cnt_row == 3
        assert sum_exp == sum_act
        p('done test_list_of_list')

    def test_requests(self):
        r = requests.get('https://github.com/wngpublic')
        r = requests.post('https://github.com/wngpublic/maventest')

    @staticmethod
    def parse_token(s, idx_s, max, delimiter):
        def next_non_char(s, idx_s, max, c):
            i = idx_s
            while i < max:
                if s[i] != c:
                    return i
                i += 1
            return None


        lifo = []
        lifoq = []
        cp = None
        last_pushed = None

        idx_s = next_non_char(s, idx_s, max, ' ')
        i = idx_s
        if i is None:
            return (None,None)

        if s[i] == '"':
            lifoq.append(s[i])
            i += 1

        while i < max:
            cc = s[i]
            if cc == '\\':
                i += 2
                if i >= max:
                    return (None,None)
                cc = s[i]

            if cc == '{' or cc == '[' or cc == '(':
                last_pushed = cc
                lifo.append(cc)
            elif \
                    cc == '}' and last_pushed != '{' or \
                            cc == ']' and last_pushed != '[' or \
                            cc == ')' and last_pushed != '(':
                return (None,None)
            elif cc == '}' or cc == ']' or cc == ')':
                lifo.pop()
                last_pushed = None if len(lifo) == 0 else lifo[len(lifo)-1] # if else, a = b ? 1 : 2
            elif cc == '"':
                if(len(lifo) == 0):
                    lifoq.append(cc)
            elif cc == ',':
                if(len(lifo) == 0 and len(lifoq) % 2 == 0):
                    token = s[idx_s:i]
                    return (token, i)
            cp = cc
            i += 1

        if(i == max):
            if(len(lifo) == 0 and len(lifoq) % 2 == 0):
                token = s[idx_s:i]
                return (token, i)
        return (None, None)

    @staticmethod
    def parse_tokens(s):
        max = len(s)
        a = []
        i = 0
        while True:
            (token,i) = Tests.parse_token(s, i, max, ',')
            if token is not None:
                a.append(token)
            if i is None or token is None:
                break
            if i < max and s[i] == ',':
                i += 1
        return a

    def test_parse_tokens(self):
        s = '"abc", "hello"'
        a = Tests.parse_tokens(s)
        p(a)
        s = "\"abc\", \"hello\""
        a = Tests.parse_tokens(s)
        p(a)
        s = "\"\"\"abc\", \"hello\""
        a = Tests.parse_tokens(s)
        p(a)
        s = '"abc", {"k1":"v1", "k2":"v2"}'
        a = Tests.parse_tokens(s)
        p(a)
        s = '"abc", {"k1":"v1", "k2":"v2","k3":["v3a", "v3b"]}, {"k11":"v11", "k12":"v12","k13":{"k13k1":"k13v1","k13k2":"k13v2"}}'
        a = Tests.parse_tokens(s)
        p(a)
        p('pass test_parse_tokens')

    # using numpy to pregenerate list is about 25x faster than using randint for each loop.
    # but using numpy to generate a single number in each loop is much slower than randint
    def test_model_entries_ttl_hit_rate(self):
        # fps is frames per second
        # qps is number of requests per second
        num_entries = 100_000
        qps = 100
        fps = 1
        insert_rate = 50
        max_time = 96 * 60 * 60
        max_range = fps * max_time
        ctr = 0
        idx = 0
        d = {}
        ttl = 24 * 60 * 60
        hit = 1
        miss = 1
        num_expired = 0
        l_rand_size = 10_000
        l_rand = numpy.random.randint(low=0,high=1000,size=l_rand_size)
        l_rand_idx = 0
        bypass_ttl = True
        p('num_enrties:{} qps:{} insert_rate:{} max_time:{} test stops at iter:{}'
            .format(num_entries,qps,insert_rate,max_time,max_range))
        for i in range(max_range):
            if(ctr >= 10_000):
                hit_rate = hit / (hit + miss) * 1.0
                p('iter {:10} hit_rate: {{:5.4f} num_entries:{:10} num_expired:{:10}'
                    .format(i, hit_rate, len(d), num_expired))
                ctr = 0
            list_to_del = []
            if not bypass_ttl:
                for k,v in d.items():
                    d[k] = d[k] - 1
                    if d[k] <= 0:
                        list_to_del.append(k)
                for k in list_to_del:
                    del d[k]
                    num_expired = num_expired + 1
            for j in range(qps):
                idx = idx + 1
                if idx >= num_entries:
                    idx = 0
                if idx in d:
                    hit = hit + 1
                else:
                    miss = miss + 1
                    if(l_rand_idx >= l_rand_size):
                        l_rand = numpy.random.randint(low=0,high=1000,size=l_rand_size)
                        l_rand_idx = 0
                    randval = l_rand[l_rand_idx]
                    l_rand_idx = l_rand_idx + 1
                    if randval <= insert_rate:
                        d[idx] = ttl
            ctr = ctr + 1
        hit_rate = hit / (hit + miss) * 1.0
        p('hit rate = {}'.format(hit_rate))
    def test_list(self):
        l = []
        l.append('hello 1\nhello 2\n')
        l.append('hello 1\nhello 2\n')
        l.append('hello 1\nhello 2\n')
        assert len(l) == 3
    def test_datetime(self):
        t1 = datetime.datetime.now()
        t2 = datetime.datetime.now()
        d  = t2 - t1
    def test_numpy_basic(self):
        num_iter = 1_000
        size = 1_000
        lo = 0
        hi = 10_000
        l = []
        for i in range(num_iter):
            l = numpy.random.randint(low=lo,high=hi,size=size)
            assert len(l) == size
            for v in l:
                assert v >= lo and v < hi
        p('test_numpy_basic_pass')
        return l
    def test_loop_speed(self):
        max = 1_000_000
        ctr = 0
        maxrange = 10_000
        for i in range(10):
            t1 = datetime.datetime.now()
            for i in range(max):
                v = numpy.random.randint(0,maxrange)
                ctr = ctr + 1
            max = max + max
            t2 = datetime.datetime.now()
            diff = t2 - t1
            p('t1:{} t2:{} time elapsed: {} max:{}'.format(t1,t2,diff,max))
    def test_hashlib(self):
        m = hashlib.md5()
        m.update("string val")
        m.digest()
        pass


    def is_callable_user_defined(self, s):
        if not callable(getattr(self, s)):
            return False
        if re.search(r'^__', s):
            return False
        return True

    def cmd_line_input(self, argv):
        def parse_cmd_line_input(s, map_functions):
            def print_methods(map_functions):
                for k,v in map_functions.items():
                    p('{:2} {}'.format(k,v))
                p('type function number to execute')
            if(s is None or len(s) == 0):
                print_methods(map_functions)
            elif(s == 'q' or s == 'quit'):
                return False
            elif(s == '?' or s == 'h'):
                print_methods(map_functions)
            else:
                a = re.split(r'\s+',s)
                if len(a) == 1:
                    if(a[0].isdigit()):
                        i = int(s)
                        if(i in map_functions):
                            p('exec {}'.format(map_functions[i]))
                            t1 = datetime.datetime.now()
                            getattr(self, map_functions[i])()
                            t2 = datetime.datetime.now()
                            diff = t2 - t1
                            p('time elapsed: {}'.format(diff))
                else:
                    pass
            return True
        def get_function_map():
            l_functions = [ m for m in dir(self) if self.is_callable_user_defined(m)]
            h = {}
            for i in range(len(l_functions)):
                h[i] = l_functions[i]
            return h
        map_functions = get_function_map()
        for i in range(0,1000):
            s = input('prompt> ')
            if not parse_cmd_line_input(s, map_functions):
                break
        p('quitting cmd_line_input')

    def list_methods(self):
        l = dir(self)
        n = len(l)
        l1 = []
        l_exclude = []
        for m in l:
            if callable(getattr(self, m)):
                l1.append(m)
            else:
                l_exclude.append(m)
        n1 = len(l1)
        p('len n:{} n1:{}'.format(n, n1))
        p('non callable: {}'.format(l_exclude))
        l2 = [m for m in dir(self) if callable(getattr(self, m))]
        p(l2)
        p('static methods not in this list')
        p('methods user defined')
        l3 = [ m for m in dir(self) if self.is_callable_user_defined(m)]
        p(l3)
        #locals()["test_string"]()
        #globals()["test_string"]()
        getattr(self, 'test_string')()      # reflection way to call methods
        getattr(self, 'test_arg')(1,2)      # this calls methods with args
        getattr(Tests, 'test_static_arg')(3,4)
        getattr(self, 'test_static_arg')(4,5)

        # having map of methods
        h = {
            'test_arg': self.test_arg,
            'test_static_arg': Tests.test_static_arg
        }
        h['test_arg'](2,3)
        h['test_static_arg'](1,3)

        p('done')

    def test_model_entries_ttl_hit_rate(self):
        # fps is frames per second
        # qps is number of requests per second
        dist_type   = 0                     # distype 0 = uniform, 1 = gaussian
        num_entries = 100_000
        qps         = 100
        fps         = 1
        insert_rate = 50 # 0.3%
        hit_rate    = 0
        max_time    = 96 * 60 * 60
        max_range   = fps * max_time
        ctr         = 0
        idx         = 0
        d           = {}
        ttl         = 24 * 60 * 60
        hit         = 1
        miss        = 1
        num_expired = 0
        l_rand_size = 10_000
        l_rand      = numpy.random.randint(low=0,high=1000,size=l_rand_size)
        l_rand_idx  = 0
        bypass_ttl  = True

        p('num_entries:{} qps:{} insert_rate:{} max_time:{} test stops at iter:{}'
          .format(num_entries, qps, insert_rate, max_time, max_range))
        for i in range(max_range):
            if ctr >= 10_000:
                hit_rate = hit / (hit + miss) * 1.0
                p('iter {:10} hit_rate: {:>5.4f} num_entries:{:10} num_expired:{:10}'
                  .format(i, hit_rate, len(d), num_expired))
                ctr = 0
            list_to_del = []
            if not bypass_ttl:
                for k,v in d.items():
                    d[k] = d[k] - 1
                    if d[k] <= 0:
                        list_to_del.append(k)
                for k in list_to_del:
                    del d[k]
                    num_expired = num_expired + 1
            for j in range(qps):
                idx = (idx + 1)
                if idx >= num_entries:
                    idx = 0
                if idx in d:
                    hit = hit + 1
                else:
                    miss = miss + 1
                    if(l_rand_idx >= l_rand_size):
                        l_rand = numpy.random.randint(low=0,high=1000,size=l_rand_size)
                        l_rand_idx = 0
                    randval = l_rand[l_rand_idx]
                    l_rand_idx = l_rand_idx + 1
                    if(randval <= insert_rate):
                        d[idx] = ttl
            ctr = ctr + 1
        hit_rate = hit / (hit + miss) * 1.0
        p('hit rate = {}'.format(hit_rate))


    def test_numpy_basic(self):
        num_iter = 1_000
        size = 1_000
        lo = 0
        hi = 10_000
        l = []
        for i in range(num_iter):
            l = numpy.random.randint(low=lo,high=hi,size=size)
            assert len(l) == size
            for v in l:
                assert v >= lo and v < hi
        p('test_numpy_basic_pass')
        return l

    '''

    loop has only ctr
    t1:2019-09-23 22:29:40.415139 t2:2019-09-23 22:29:41.220705 time elapsed: 0:00:00.805566 max:20000000
    t1:2019-09-23 22:29:41.220793 t2:2019-09-23 22:29:42.637146 time elapsed: 0:00:01.416353 max:40000000
    t1:2019-09-23 22:29:42.637249 t2:2019-09-23 22:29:45.457262 time elapsed: 0:00:02.820013 max:80000000
    t1:2019-09-23 22:29:45.457348 t2:2019-09-23 22:29:52.435351 time elapsed: 0:00:06.978003 max:160000000
    
    loop has randint
    t1:2019-09-23 22:32:04.668355 t2:2019-09-23 22:32:27.835413 time elapsed: 0:00:23.167058 max:20000000
    t1:2019-09-23 22:32:27.835639 t2:2019-09-23 22:33:02.176667 time elapsed: 0:00:34.341028 max:40000000
    t1:2019-09-23 22:33:02.176729 t2:2019-09-23 22:34:09.553533 time elapsed: 0:01:07.376804 max:80000000

    numpy.random
    t1:2019-09-23 22:41:28.935097 t2:2019-09-23 22:42:49.433340 time elapsed: 0:01:20.498243 max:20000000
    t1:2019-09-23 22:42:49.433398 t2:2019-09-23 22:45:29.752893 time elapsed: 0:02:40.319495 max:40000000

    '''

    def test_loop_speed(self):
        max = 1_000_000
        ctr = 0
        for i in range(10):
            t1 = datetime.datetime.now()
            for i in range(max):
                v = numpy.random.randint(0,10_000)
                ctr = ctr + 1
            max = max + max
            t2 = datetime.datetime.now()
            diff = t2 - t1
            p('t1:{} t2:{} time elapsed: {} max:{}'.format(t1,t2,diff,max))

    def rand_string(self, charset, len):
        r = ""
        for i in range(len):
            pass
        return r

    def rand_json_generator(self, charset, d, levels, fanout, maxarray, maxset):
        this_fanout = random.randint(1,fanout)
        for i in range(this_fanout):
            data_type = random.randint(0,3)
            if data_type == 0:      # data type string
                pass
            if data_type == 1:      # data type array
                pass
            if data_type == 2:      # data type set
                pass

    def test_hashlib(self):
        m = hashlib.md5()
        m.update("string val")
        m.digest()
        pass

    def test(self, argv):
        '''
        self.test_parse_args(argv)
        Tests.testCmdLoop1()
        self.testMyClass2()
        self.testGossip()
        self.testDependencyStructure()
        self.test_utils_module()
        self.test_files_and_json()
        self.test_multithread_concepts()
        self.test_logging()
        self.test_algos()
        self.test_async_concepts()
        self.test_multithread_concepts()
        self.test_convert_int()
        self.test_round_number()
        self.test_tuple_list_ops()
        self.test_dict_operations()
        self.test_set_operations()
        self.test_syntax()
        self.test_regex()
        self.test_string()
        self.test_list()
        self.test_map_of_lists_and_dicts()
        self.test_dict_operations()
        self.test_list()
        self.test_external_command_capture()
        self.list_methods()
        #self.testCmdLoop1()
        self.list_methods()
        '''
        self.cmd_line_input(None)
        pass

def check_args(args):
    if(len(args) <= 1):
        return
    for arg in args:
        print(arg)
    print(len(args))

def maintestcases():
    if(sys.version_info[0] < 3):
        print("version is {},{}".format(sys.version_info[0],sys.version_info[1]))
    #assert sys.version_info[0] == 3 and sys.version_info[1] >= 4 # OK
    assert sys.version_info >= (3,4) # OK
    check_args(sys.argv)
    global global_fh_
    t = Tests()
    t.test(None)
    if(global_fh_ is not None):
        global_fh_.close()

maintestcases()


#
#        #if(not re.match(r'^\d{4}-\d{2}-\d{2}$', v)):
#    return False
#try:
#    pattern = '%Y-%m-%d'
#    seconds = time.mktime(time.strptime(v,pattern))
#    return seconds
#except Exception as e:
#    return 0


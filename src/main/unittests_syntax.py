import unittest
import queue
import heapq
import math
import collections
import re
import functools
import array
import sys
import string
import collections
import os
import json
import time
import random
import datetime
import numpy
import calendar
import string           # this is for string templates
import enum
#import utils.myutils    # test import from utils directory
#from src.main import utils     # this works
#from src.main.utils import myutils     # this works
import src.main.utils.myutils as myutils1   # this works
from .utils.myutils import my_utils   # this works
import zlib
import hashlib
import typing
import logging
import csv
import pandas
import types
import copy
import struct
import binascii
import codecs
import base64
import site
import bisect
import matplotlib
import secrets
import asyncio
import concurrent.futures
import threading
import difflib
import pprint

# install pycrypto, dont use crypto, use cryptodome
# install cryptodomex
#import Crypto.Hash.SHA256 # from Crypto.Hash import SHA256
#import Cryptodome.Cipher.AES # from Crypto.Cipher import AES
#import Cryptodome.Random
#from Crypto.Hash import SHA256
#from Crypto.Cipher import AES
#from Crypto import Random
#from Crypto.Util import Padding

'''
python3 -m unittest syntax_unittests.ut.test_method
python3 syntax_unittests.py syntax_ut.test_method
python3 unittest_algos.py ut.test_list
or alias pythonut syntax_unittests.ut.test_main 
where pythonut='python3 -m unittest'
pythonut syntax_unittests.ut.main

this class is for testing python basic syntax
this class is not for algos or non built-in library testing
this class can be for object testing syntax
'''


global_debug_level_ = 0  # 0 to 5. 0 = off, 1 = highest, 5 = lowest
global_output_to_file_ = False
global_fh_ = None

def printit(s):
    p(s)

def p(s):
    global global_output_to_file_
    global global_fh_
    if(global_output_to_file_):
        if(global_fh_ is None):
            global_fh_ = open('output_debug.log','w')
        global_fh_.write(s + '\n')
    else:
        print(s)

class OuterClass:
    z = "abc"               # class variable
    def __init__(self,x,y):
        self.x = x          # instance variable
        self.y = y

class AmbiguousClass:
    def __init__(self,x,y):
        self.x = x
        self.y = y

#logging.basicConfig(level=logging.INFO)  #basicConfig outputs to STDOUT, so comment out

fh = logging.FileHandler('logging_output.log')
fh.setLevel(logging.INFO)

# log formatter is optional         time          appname    level space align
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-10s - line:%(lineno)-5s - %(message)s')
log_formatter = logging.Formatter('%(asctime)s - %(levelname)-9s - %(message)s')
fh.setFormatter(log_formatter)

logger = logging.getLogger('unittests_syntax_logger')
logger.setLevel(logging.INFO)
logger.addHandler(fh)
v_global = 100

class bnode:
    ID = 0
    def __init__(self,k,v,l=None,r=None):
        self.k_ = k
        self.v_ = v
        self.l_ = l
        self.r_ = r
        self.id_ = bnode.ID
        bnode.ID += 1
    def reset_id(self):
        bnode.ID = 0
    def id(self):
        return self.id_
    def l(self,n=None):
        if n != None:
            self.l_ = n
        return self.l_
    def r(self,n=None):
        if n != None:
            self.r_ = n
        return self.r_
    def k(self):
        return self.k_
    def v(self):
        return self.v_

class ut(unittest.TestCase):
    v_class = 200
    def __init__(self, *args, **kwargs):
        self.v_class = 300
        super(ut, self).__init__(*args, **kwargs)

    def get_v_class(self):
        return self.v_class

    class InnerClass:
        def __init__(self,x,y):
            self.x = x
            self.y = y

    class AmbiguousClass:
        def __init__(self,x,y,z):
            self.x = x
            self.y = y
            self.z = z
    def setUp(self):
        #p('setup called')
        pass

    def tearDown(self) -> None:
        #p('teardown called')
        pass

    def test_import_class(self):
        myutils = my_utils()
        myutilsx = myutils1.my_utils()          # import AS something
        v = myutils.rand(1,2)                   # instance function
        v = my_utils.rand(1,2)    # static function
        assert my_utils.charset_num == '0123456789'
        assert myutils.charset_num == '0123456789'
        assert 1 == myutilsx.get(1)             # instance function

    def test_class_scope(self):
        v_class = 400
        v_method = 500
        v_global = 1000
        class InnerInnerClass:
            _parent_class = self
            def __init__(self,x,y):
                self.x = x
                self.y = y
                self.v_class = 500

            def test_scope_case1(self):
                v_global = None
                v = v_global
                assert v == None

            def test_scope_case2(self):
                self.test_scope_case2_1()
                self.test_scope_case2_2()

            def test_scope_case2_1(self):
                global v_global         # this takes global v_global
                v = v_global
                assert v == 100

            def test_scope_case2_2(self):
                nonlocal v_global       # this takes method's v_global
                v = v_global
                assert v == 1000

            def test_scope_case3(self):
                v = ut.v_class
                assert v == 200

                v = self._parent_class.get_v_class()    # access outer class methods
                assert v == 300

                v = v_class
                assert v_class == 400

                v = self.v_class
                assert v == 500

                #v_class = 600
                #v = v_class
                #assert v == 600

            def test_scope_case4(self):
                nonlocal v_class
                v = v_class
                assert v == 400

                v_class = 500

                self.test_scope_case_inner()

                v = v_class
                assert v == 600


            def test_scope_case_inner(self):
                nonlocal v_class
                v = v_class
                assert v == 500

                v_class = 600

            def test_scope(self):
                self.test_scope_case1()
                self.test_scope_case2()
                self.test_scope_case3()
                self.test_scope_case4()

        oc      = OuterClass(1,2)
        aco     = AmbiguousClass(2,3)
        ic      = ut.InnerClass(3,4)
        aci     = ut.AmbiguousClass(4,5,6)
        iic     = InnerInnerClass(6,7)
        iic.test_scope()
        assert oc.x == 1
        assert aco.y == 3
        assert ic.y == 4
        assert aci.z == 6
        assert iic.y == 7
        assert oc.z == "abc"

        oc1     = OuterClass(1,2)
        oc2     = OuterClass(2,3)
        assert oc1.x == 1
        assert oc2.x == 2           # instance variable
        assert oc1.z == "abc"
        assert oc2.z == "abc"
        assert oc1.z == oc2.z
        oc1.z = "def"
        assert oc1.z == "def"       # class variable == static variable
        assert oc2.z == "abc"       # class variable == static variable
        assert oc1.z != oc2.z
        #p('pass test_class_scope')

    def test_logger(self):
        logger.debug("test_logger_debug")
        logger.info("test_logger_info")
        logger.warning("test_logger_warning")
        logger.error("test_logger_error")
        logger.critical("test_logger_critical")

    def test_random(self):
        def rand_uniform(min,max,numruns):
            for i in range(numruns):
                val = random.randint(min, max)  # randint is min <= x <= max
                assert val >= min and val <= max
            for i in range(numruns):
                val = random.randrange(min, max)  # randint is min <= x < max
                assert val >= min and val < max
        def rand_gauss_normal(min,max,mu,sigma,numruns,debug=True):
            res = []
            dist = {}
            ctr = 0
            max_ctr = numruns * 1000
            while ctr < numruns:
                f = random.gauss(mu,sigma)  # same as random.normalvariate(mu,sigma)
                if f >= min and f <= max:
                    #v = round(f,2)
                    v = int(f)
                    res.append(v)
                    ctr += 1
                if ctr > max_ctr:
                    break
            assert ctr < max_ctr
            for v in res:
                if v not in dist:
                    dist[v] = 0
                dist[v] += 1
                #print(v)
            ordered_dist = collections.OrderedDict(sorted(dist.items()))
            if debug:
                for k,v in ordered_dist.items():
                    print('val:count = {}:{}'.format(k,v))
        def rand_choice_and_choices(choices,cum_weights,numruns,debug=True):
            res = []
            for i in range(numruns):
                v = random.choice(choices)
                res.append(v)
            dist = {}
            for v in res:
                if v not in dist:
                    dist[v] = 0
                dist[v] += 1
            ordered_keys = sorted(dist.keys())
            if debug:
                print('\n')
                print('choices\n')
                for k in ordered_keys:
                    print('val:count = {}:{}'.format(k,dist[k]))
                print('\n')
            res = random.choices(choices,cum_weights=cum_weights,k=numruns)
            dist = {}
            for v in res:
                if v not in dist:
                    dist[v] = 0
                dist[v] += 1
            ordered_keys = sorted(dist.keys())
            if debug:
                for k in ordered_keys:
                    print('val:count = {}:{}'.format(k,dist[k]))
                print('\n')

        min = 1
        max = 10
        mu = 2          # mean
        sigma = 3       # deviation f(x)=(1/(sigma*sqrt(2*pi)))*(e^((-1/2)*((x-mu)/sigma))^2))
        numruns = 1000
        choices = [ 1, 2, 3, 4, 5, 6, 7, 8, 9]

        #  %       20 20 20 10  5  5  5  5  5
        cum_w   = [20,40,60,70,75,80,85,90,95]
        debug = False
        rand_uniform(min,max,numruns)
        rand_gauss_normal(min,max,mu,sigma,numruns,debug=debug)
        numruns = 10000
        rand_choice_and_choices(choices,cum_w,numruns,debug=debug)

    def test_list(self):
        # push and pop
        l = []
        l.append(1)
        l.append(2)
        l.insert(0,10)
        l.insert(0,20)
        l.insert(-1,30)
        l.insert(len(l),40)
        l.append(50)
        assert l == [20,10,1,30,2,40,50]
        l.pop()
        assert l == [20,10,1,30,2,40]
        l.pop(0)
        assert l == [10,1,30,2,40]

        l = []
        l.append(1)
        l.append(2)

        assert len(l) == 2

        v = l.pop()
        assert v == 2
        assert len(l) == 1
        assert l == [1]

        l2 = []                 # empty list operations
        assert l2[-1:] == []    # empty list, no exception
        flag = False
        try:
            flag = False
            v = l2[-1:]
            assert v == []
            v2 = v[0]           # index error
            assert False
        except Exception as e:
            flag = True         # expect Exception
        assert flag

        try:
            flag = False
            v = l2[-1]          # IndexError
            assert False
        except Exception as e:
            flag = True         # expect Exception
        assert flag

        # push and pop left and right
        l = [1,2,3,4,5]
        assert l[-1] == 5       # peek, generates IndexError if empty
        assert l[-1] == 5       # peek repeat
        assert l[-1:] == [5]    # dont raise error if empty

        v = l.pop()
        assert l[-1] == 4       # peek
        assert l[-1:] == [4]    # peek into array
        assert l[0] == 1        # peek head
        assert v == 5 and len(l) == 4
        v = l.pop(0)
        assert v == 1 and len(l) == 3

        l.insert(0, 1)
        assert l == [1,2,3,4]
        l.append(5)
        assert l == [1,2,3,4,5]

        l.clear()
        assert l == []

        l.extend([1,2,3])
        l.extend([4,5,6])
        assert l == [1,2,3,4,5,6]
        lcopy = l.copy()
        l.reverse()
        assert l == [6,5,4,3,2,1]
        assert lcopy == [1,2,3,4,5,6]
        l = list(reversed(l))
        assert l == [1,2,3,4,5,6]
        #idx = [0,2,4]
        #res = l[idx]
        #assert l[idx] == [1,3,5]


        # append list vs extend list
        l.clear()
        l.append(1)
        l.append([2,3,4])
        l.append(5)
        l.extend([6,7])
        assert l == [1,[2,3,4],5,6,7]

        # list compare
        l1 = [1,2,3]
        l2 = [2,3,4]
        l3 = [2,3,4]
        assert l1 != l2
        assert l2 == l3

        ctr = 0
        for v in l1:
            ctr += 1
        assert ctr == 3

        # list is empty check
        l = []
        ctr = 0
        if(l):          # empty list check
            ctr = 1
        assert ctr == 0

        # peek check on empty list
        v = None
        try:
            v = l[-1]
        except IndexError as e:
            ctr = 1
        assert ctr == 1

        # peek check with no exception on empty list. v is empty list
        ctr = 0
        v = l[-1:]
        assert not v
        assert v == []

        # peek on populated list
        v = l3[-1]
        assert v == 4
        v = l3[-1:]
        assert v == [4]

        # ways to initialize list
        l = [i for i in range(3)]
        assert l == [0,1,2]

        l = [i*2 for i in l]
        assert l == [0,2,4]

        l = [[2] * 3]
        assert l == [[2,2,2]]

        l = [2] * 3
        assert l == [2,2,2]

        l = [0] * 3
        assert l == [0,0,0]

        l = [[0] * 3,[1] * 3]
        assert l == [[0,0,0],[1,1,1]]

        l = [[] for i in range(3)]
        assert l == [[],[],[]]
        l[0].append([0,1,2])
        assert l == [[[0,1,2]],[],[]]
        l[1].extend([2,3,4])
        assert l == [[[0,1,2]],[2,3,4],[]]
        del l[0][0]         # delete from array
        assert l == [[],[2,3,4],[]]

        l = [
            [1,2],
            [3,4],
            [5,6],
            [7,8]
        ]
        assert l == [[1,2],[3,4],[5,6],[7,8]]
        assert l != [[1,2],[3,4],[5,6],[7,9]]
        assert l != [[1,2],[3,4],[4,6],[7,8]]
        del l[2]
        assert l == [[1,2],[3,4],[7,8]]
        del l[0]
        assert l == [[3,4],[7,8]]
        del l[0]
        assert l == [[7,8]]

        # 2d array by reading vars
        v1 = 'abc'
        v2 = '123'
        l = [['{}{}'.format(c,i) for i in v2] for c in v1]
        assert l == [['a1','a2','a3'],['b1','b2','b3'],['c1','c2','c3'],]

        l = [1,2,3]
        l = l*2
        assert l == [1,2,3,1,2,3]

        l = [1,2,3]
        assert l == [1,2,3]
        assert l != [2,3,4]

        r = l[:1]
        assert r == [1]
        r = l[1:]
        assert r == [2,3]

        l = [1,2,3,4,5]
        r = l[1:3]
        assert r == [2,3]

        r = l[0:2] + l[3:5]
        assert r == [1,2,4,5]

        r = l[1:2] + l[3:5]
        assert r == [2,4,5]

        r = l[0:2] + l[2:5]
        assert r == [1,2,3,4,5]

        # string split
        s = 'abcde'
        l = s.split()
        assert len(l) == 1
        assert l == ['abcde']
        assert len(s) == 5
        l = list(s)
        assert len(l) == 5
        assert l == ['a','b','c','d','e']
        l = [c for c in l]
        assert len(l) == 5
        assert l == ['a','b','c','d','e']

        # split by char
        s = 'a,b,c,d,e'
        l = s.split(',')
        assert len(l) == 5
        assert l == ['a','b','c','d','e']

        s = 'aa bb cc dd ee'
        l = s.split()
        assert len(l) == 5
        assert l == ['aa','bb','cc','dd','ee']

        s = 'aa   bb cc dd   ee'
        l = s.split()
        assert len(l) == 5
        assert l == ['aa','bb','cc','dd','ee']

        # list del add elements
        l = []
        l.append(1)
        l.append(2)
        l.extend([3,4,5])
        assert len(l) == 5
        del l[4]
        assert len(l) == 4
        del l[0]
        assert len(l) == 3
        assert l == [2,3,4]
        l.clear()
        assert len(l) == 0
        l = [1,2,3,4,5]
        l[0] = 8
        assert l == [8,2,3,4,5]
        l[1] = 8
        assert l == [8,8,3,4,5]

        # ways to generate list
        l1 = [1,2,3,4,5]

        l = [0] * 5
        assert l == [0,0,0,0,0]
        l[1] = 1
        assert l == [0,1,0,0,0]
        l = [x for x in range(5)]
        assert l == [0,1,2,3,4]
        l = [x for x in l1]
        assert l == [1,2,3,4,5]
        l = [(x*2) for x in l1]
        assert l == [2,4,6,8,10]
        l = [x for x in l1 if x % 2 == 0]
        assert l == [2,4]
        l = [x for x in l1 if x % 2 == 1]
        assert l == [1,3,5]

        l = [1 for i in range(3)]
        assert l == [1,1,1]
        l[1] = 2
        assert l == [1,2,1]
        l = [1] * 3
        assert l == [1,1,1]
        l[1] = 2
        assert l == [1,2,1]

        l = [[1]*3]
        assert l == [[1,1,1]]
        assert l != [[1,2,3]]
        l = [[1]*3]*2   # this is replica!
        assert l == [[1,1,1],[1,1,1]]
        assert l != [[1,1,2],[1,1,1]]
        l[0][1] = 2     # this is copied to all arrays!
        assert l != [[1,2,1],[1,1,1]]
        assert l == [[1,2,1],[1,2,1]]
        l = [[1]*i for i in range(5)]
        assert l == [[],[1],[1,1],[1,1,1],[1,1,1,1]]
        l = [[0]*i for i in range(5)]
        assert l == [[],[0],[0,0],[0,0,0],[0,0,0,0]]


        # this is one way to create list of list
        l = [[]]*2
        assert l == [[],[]]
        for i in range(2):
            l[i] = [0] * 3      # this is not replica
        assert l == [[0,0,0],[0,0,0]]
        l[0][1] = 2
        assert l == [[0,2,0],[0,0,0]]

        l = [[] for i in range(2)]
        assert l == [[],[]]
        assert l != [[],[],[]]
        assert [[] for i in range(2)] == [[]] * 2
        for i in range(2):
            l[i] = [0] * 3
        assert l == [[0,0,0],[0,0,0]]
        l[0][1] = 2             # modifying 1 value doesnt affect others
        assert l == [[0,2,0],[0,0,0]]

        # another way of doing 2d array not by replicas
        l = [[0 for x in range(3)] for x in range(2)]
        assert l == [[0,0,0],[0,0,0]]
        l[0][1] = 2
        assert l == [[0,2,0],[0,0,0]]

        l = [[0 for y in range(3)] for x in range(2)]
        assert l == [[0,0,0],[0,0,0]]
        l[0][1] = 1
        l[1][0] = 2
        assert l == [[0,1,0],[2,0,0]]

        s1 = '1234'
        s2 = '123'
        l = [[0 for c in range(len(s2)+1)] for r in range(len(s1)+1)]
        assert l == [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        l[0][3] = 3
        l[3][0] = 30
        l[4][3] = 43
        assert l == [[0,0,0,3],[0,0,0,0],[0,0,0,0],[30,0,0,0],[0,0,0,43]]

        cols = 3
        rows = 2
        l = [[(i*cols+j) for j in range(cols)] for i in range(rows)]
        assert l == [[0,1,2],[3,4,5]]   # yay

        l = [None] * 3
        assert l == [None,None,None]

        l = list(range(5))              # init list to sequential
        assert l == [0,1,2,3,4]

        l = list(range(5,10))
        assert l == [5,6,7,8,9]

        l = array.array('i',(1,)*5)
        assert l == array.array('i',[1,1,1,1,1])

        # is l2 a subpath of l1? not
        def is_subpath(l1,l2):
            if(len(l1) > len(l2)):
                return False
            flag = False
            for k1,k2 in zip(l1,l2):
                if k1 != k2:
                    return False
            return True

        l1 = [2,4,6,8]
        l2 = [2,4,6,8,10]
        l3 = [2,6,7,8]
        l4 = [2,4,6,8]

        assert is_subpath(l1,l2) == True
        assert is_subpath(l2,l1) == False
        assert is_subpath(l1,l3) == False
        assert is_subpath(l1,l4) == True

        l1 = [1,2,3,4,5]
        l2 = [2,3,4,5,6]


        l3 = []
        for x,y in zip(l1,l2): l3.append(x+y)
        assert l3 == [3,5,7,9,11]

        def f(x,y): return x+y
        l3 = [f(x,y) for x,y in zip(l1,l2)]
        assert l3 == [3,5,7,9,11]

        l1 = [1,2,3,4,5]
        l2 = [2,3,4,5,6]
        l3 = [3,4,5,6,7]
        def f(x,y,z): return x+y+z
        l4 = [f(x,y,z) for x,y,z in zip(l1,l2,l3)]
        assert l4 == [6,9,12,15,18]

        assert sum([1,2,3,4,5]) == 15

        l = [1,2,3,4,5]
        assert min(l) == 1
        assert max(l) == 5
        assert l[2] == 3

        t = (1,2,3,4,5)         # does min/max matter if this is tuple?
        assert min(t) == 1
        assert max(t) == 5
        assert t[2] == 3

        assert (1,2,3,4,5) != [1,2,3,4,5]

        s = 'test'
        l = []
        for c in s:
            l.append(c)
        assert l == ['t','e','s','t']

        # list of list
        ll0 = None
        ll1 = None
        assert ll0 is None
        assert ll0 == None
        assert ll0 is not []
        assert ll0 != []
        ll0 = []
        assert ll0 is not None
        assert ll0 != None
        assert ll0 == []
        assert ll0 != ll1
        ll0 = [[0,1,2],[3,4,5]]
        ll1 = [[0,1,2],[3,4,5]]
        assert ll0 != None
        assert len(ll0) == 2
        assert len(ll0[0]) == 3
        assert ll0 == ll1
        assert ll0[0][1] == 1
        assert ll0[1][0] == 3
        ll1 = [[0,1,2],[3,4,6]]
        assert ll0 != ll1


        # matrix, two dimensional array
        a = []
        for i in range(3):
            a.append([])
            for j in range(4):
                a[i].append(i*10 + j)
        assert len(a) == 3 and len(a[0]) == 4
        assert a[0][0] == 0 and a[1][0] == 10 and a[0][1] == 1 and a[2][3] == (2*10+3)

        a = [[0 for j in range(4)] for i in range(3)]
        for i in range(3):
            for j in range(4):
                a[i][j] = (i*10+j)
        assert len(a) == 3 and len(a[0]) == 4
        assert a[0][0] == 0 and a[1][0] == 10 and a[0][1] == 1 and a[2][3] == (2*10+3)

        a = [   [0,1,2,3],
                [10,11,12,13],
                [20,21,22,23]]
        assert len(a) == 3 and len(a[0]) == 4
        assert a[0][0] == 0 and a[1][0] == 10 and a[0][1] == 1 and a[2][3] == (2*10+3)

        a = [[],[],[]]
        for i in range(3):
            for j in range(4):
                a[i].append(i*10 + j)
        assert len(a) == 3 and len(a[0]) == 4
        assert a[0][0] == 0 and a[1][0] == 10 and a[0][1] == 1 and a[2][3] == (2*10+3)

        a = [[] for i in range(3)]
        for i in range(3):
            for j in range(4):
                a[i].append(i*10 + j)
        assert len(a) == 3 and len(a[0]) == 4
        assert a[0][0] == 0 and a[1][0] == 10 and a[0][1] == 1 and a[2][3] == (2*10+3)

        #    0 1 2 3 4 5 6
        l = [0,1,2,3,4,5,6]
        r = [l[i] for i in range(1,4)]      # range of values of index
        assert r == [1,2,3]

        '''
        a = [[]]    # doesnt work
        for i in range(3):
            for j in range(4):
                a[i].append(i*10 + j)
        '''

        a = {}
        for i in range(3):
            for j in range(4):
                a[i,j] = i*10+j
        assert len(a) == 3*4
        assert a[0,0] == 0 and a[1,0] == 10 and a[0,1] == 1 and a[2,3] == (2*10+3)  # index is [x,y]

        l1 = [1.123,2.123,3.123,4.123,5.123,6.123,7.123,8.123,9.123]
        l = [round(v,1) for v in l1]
        assert l == [1.1,2.1,3.1,4.1,5.1,6.1,7.1,8.1,9.1]

        # join list of list int to string, iterating nested for loop for ints
        l1 = [[1,2],[3,4],[5,6]]
        vsum = 0
        s = [','.join([str(i) for i in l1])]
        assert s == ['[1, 2],[3, 4],[5, 6]']
        s = [';'.join([','.join([str(i) for i in t]) for t in l1])]
        assert s == ['1,2;3,4;5,6']
        s = ';'.join([','.join([str(i) for i in t]) for t in l1])
        assert s == '1,2;3,4;5,6'

        l1 = ['12','34','56']
        s = ','.join(l1)
        assert s == '12,34,56'
        s = ';'.join([','.join(c for c in tmps) for tmps in l1])
        assert s == '1,2;3,4;5,6'

        # filter a list in single line conditional list
        l1 = [1,2,3,4,5,6,7,8,9]
        l2 = [i for i in l1 if i % 2 == 0]
        assert l2 == [2,4,6,8]
        l2 = [i*2 for i in l1]
        assert l2 == [2,4,6,8,10,12,14,16,18]

        # if else ternary single line
        v = 10
        r = 1 if v % 2 == 0 else 2
        assert r == 1
        v = 11
        r = 1 if v % 2 == 0 else 2
        assert r == 2

        # operate list of list , nested list, in single line
        l1 = [[1,2],[3,4],[5,6]]
        l2 = [[i+1 for i in lx] for lx in l1]
        assert l1 == [[1,2],[3,4],[5,6]]
        assert l2 == [[2,3],[4,5],[6,7]]

        l = []
        l.append([])
        l.append([])
        l.append([])
        for i in range(len(l)):
            for j in range(2):
                l[i].append(i*10+j)
        assert l == [[0,1],[10,11],[20,21]]
        assert len(l) == 3

        l1 = [1,2,3,4,5]
        l2 = l1.copy()
        l2.reverse()
        l3 = l1.copy().reverse()    # produces None
        assert l1 == [1,2,3,4,5]
        assert l2 == [5,4,3,2,1]
        assert l3 == None
        #p('pass test_list')

        l = [
                [
                    [1,2],
                    [3,4]
                ],
                [
                    [5,6],
                    [7,8]
                ]
            ]

        l1 = l.copy()               # this is not a deep copy, so arrays are still by reference
        assert l[0][0] == [1,2]
        assert l[0][1] == [3,4]
        assert l[0][1][0] == 3
        assert l[1][1] == [7,8]

        l[0][1][0] = 33
        assert l[0][1] == [33,4]    # original got modified and the copy
        assert l1[0][1] == [33,4]

        l = [
                [
                    [1,2],
                    [3,4]
                ],
                [
                    [5,6],
                    [7,8]
                ]
            ]

        l2 = copy.deepcopy(l)       # this is a deep copy
        assert l[0][1][0] == 3
        l[0][1][0] = 33
        assert l[0][1] == [33,4]    # original got modified but not the copy
        assert l2[0][1] == [3,4]

        l1 = [1,2,3,4,5]
        l2 = 'hello'
        s = ' '.join([str(i) for i in l1])
        assert s == '1 2 3 4 5'
        s = ' '.join(l2)
        assert s == 'h e l l o'
        space = ' '
        s = space.join(l2)
        assert s == 'h e l l o'

        l = []
        l.append([])
        l[0].append(1)
        l[0].append([2,3,4,5])      # append list to list
        l.append([])
        l[1].append(1)
        l[1].extend([2,3,4,5])      # extend list to list
        l.append([1,2,3,4,5])
        assert l == [[1,[2,3,4,5]],[1,2,3,4,5],[1,2,3,4,5]]

        # stack ops push and pop queue LIFO
        l = [1,2,3,4]
        l.append(5)
        l.append(6)
        v = l.pop()
        assert l == [1,2,3,4,5]
        assert v == 6

        # queue ops FIFO
        l = [1,2,3,4]
        l.append(5)
        l.append(6)
        v = l.pop(0)
        assert v == 1
        assert l == [2,3,4,5,6]
        v = l.pop()
        assert v == 6

        v1,v2,v3 = 10,20,30
        assert v1 == 10
        assert v2 == 20
        assert v3 == 30

        return

    def test_numpy(self):
        debug = False
        numpy.random.seed(0)
        lo = 10
        hi = 20
        l1d = numpy.random.randint(lo,hi,size=3)        # 1d list
        l2d = numpy.random.randint(lo,hi,size=(3,4))    # 2d list
        l3d = numpy.random.randint(lo,hi,size=(3,4,5))  # 3d list

        assert len(l1d) == 3
        assert len(l2d) == 3 and len(l2d[0]) == 4
        assert len(l3d) == 3 and len(l3d[0]) == 4 and len(l3d[0][0]) == 5

        l = numpy.random.random(10)
        assert len(l) == 10
        l = numpy.random.randint(0,10,10)
        assert len(l) == 10
        numpy.sum(l) < (10*10)
        sum(l) < (10*10)


    def test_input(self):
        p('enter an int:')
        i = int(input())
        p('you entered {}'.format(i))

    '''
    test priority queue, heap, queue
    '''
    def testQueue(self):
        # heapq
        l = []
        heapq.heappush(l,3)
        heapq.heappush(l,4)
        heapq.heappush(l,1)
        heapq.heappush(l,10)
        r = []
        while(l != []):
            r.append(heapq.heappop(l))
        assert r == [1,3,4,10]

        l = [3,10,1,4]
        heapq.heapify(l)
        r = []
        while(l != []):
            r.append(heapq.heappop(l))
        assert r == [1,3,4,10]

        # queue package is synchronized, while heapq is not synchronized
        q = queue.Queue()
        for i in range(0, 10):
            q.put(item=i)
        i = 0
        while not q.empty():
            v = q.get()
            assert v == i
            i += 1

        q = queue.PriorityQueue()   # lowest values retrieved first
        q.put(3)
        q.put(4)
        q.put(1)
        q.put(10)
        r = []
        while not q.empty():
            r.append(q.get())
        assert r == [1,3,4,10]

        q = queue.PriorityQueue()   # lowest values retrieved first
        q.put('v3')
        q.put('v4')
        q.put('v1')
        q.put('v10')
        r = []
        while not q.empty():
            r.append(q.get())
        assert r == ['v1','v10','v3','v4']

        #p('queue test passed')

    def test_methods_and_vars_in_scope(self):
        '''
        test inner methods and references to vars in inner methods
        '''
        perfctr = 0 # must be declared nonlocal if used in inner scope

        def incperfctr():
            nonlocal perfctr
            perfctr += 1
            return perfctr

        def getperfctr():
            nonlocal perfctr
            return perfctr

        def t1(v1) -> list:
            incperfctr()
            return [v1,perfctr]

        def t2(v1) -> list:
            def t2_v1_inc(v1) -> int:   # inner inner function
                incperfctr()
                return v1+1
            incperfctr()
            v2 = t2_v1_inc(v1)
            perfctr = getperfctr()
            return [v2,perfctr]

        def test0():
            l = t1(2)
            assert l == [2,1]
            l = t2(3)
            assert l == [4,3]

        test0()

        #p('test_methods_and_vars_in_scope')

    def test_string(self):
        s_orig = ' abc  def   123 \n'

        # split by space
        l = re.split(r'\s+', s_orig)
        assert l == ['','abc','def','123','']

        s = s_orig.strip()
        l = re.split(r'\s+',s)
        assert l == ['abc','def','123']

        # join a list of string
        s = ''.join(l)
        assert s == 'abcdef123'
        s = ','.join(l)
        assert s == 'abc,def,123'
        l = s.split(',')
        assert l == ['abc','def','123']

        pat = 'abc'
        repeat = 3
        s = ''.join([c*repeat for c in pat])    # repeating strings
        assert s == 'aaabbbccc'
        s = pat * 3
        assert s == 'abcabcabc'
        s = ''.join([c for c in pat]*3)
        assert s == 'abcabcabc'

        flag = False
        s = None
        try:
            assert len(s) == 0      # error for len of null
        except Exception as e:
            flag = True
        assert flag

        s = 'abcabc'
        assert s[1:] == 'bcabc'
        assert s[:2] == 'ab'
        assert s[1:3] == 'bc'
        assert len(s[1:3]) == (3-1)
        s1 = s[0:1] + s[1:3] + s[3:]
        assert s1 == 'abcabc'

        l = ['ab','cd','ef']
        s = ''.join(l)
        assert s == 'abcdef'

        s = ','.join(l)
        assert s == 'ab,cd,ef'

        s = ','.join(['ab','cd','ef']) * 3
        assert s == 'ab,cd,efab,cd,efab,cd,ef'

        s = ','.join(['ab','cd','ef'] * 3)
        assert s == 'ab,cd,ef,ab,cd,ef,ab,cd,ef'

        s = ''.join(['ab','cd','ef']) * 3
        assert s == 'abcdefabcdefabcdef'

        s = ''.join(['ab','cd','ef'] * 3)
        assert s == 'abcdefabcdefabcdef'

        s = ','.join([''.join(l) * 3])
        assert s == 'abcdefabcdefabcdef'

        s = ','.join([''.join(l)] * 3)
        assert s == 'abcdef,abcdef,abcdef'

        s = ','.join(''.join(l) * 3)
        assert s == 'a,b,c,d,e,f,a,b,c,d,e,f,a,b,c,d,e,f'

        s = ','.join('abcdefabcdefabcdef')
        assert s == 'a,b,c,d,e,f,a,b,c,d,e,f,a,b,c,d,e,f'

        s = ''.join('abcdef')
        assert s == 'abcdef'

        s = ','.join('abcdef')
        assert s == 'a,b,c,d,e,f'

        s = ''.join(reversed('abcdef'))
        assert s == 'fedcba'
        s = 'abcdef'[::-1]
        assert s == 'fedcba'

        s = ','.join(['abcdef'])
        assert s == 'abcdef'

        # string to char list
        a = list('abcde')
        assert a == ['a','b','c','d','e']
        a = [c for c in 'abcde']
        assert a == ['a','b','c','d','e']

        # char list to string
        s = ''.join(a)
        assert s == 'abcde'
        s = ''
        for c in a:
            s += c
        assert s == 'abcde'

        # test slice slicing
        #    012345
        s = 'abcdef'
        assert s[0:] == 'abcdef'
        assert s[0:6] == 'abcdef'
        assert s[0:7] == 'abcdef'       # index out of bound but no error!
        assert s[1:] == 'bcdef'
        assert s[1:2] == 'b'
        assert s[1:3] == 'bc'
        assert s[:2] == 'ab'
        assert s[5:] == 'f'
        assert s[6:] == ''              # index out of bound but no error!
        assert len(s[6:]) == 0
        assert s[6:] is not None
        assert s[7:] == ''
        assert s[0] == 'a'
        assert s[-1] == 'f'

        s = '111 111\n' + \
            '222  222 \n' + \
            ' 333 333  \n'

        assert s == '111 111\n222  222 \n 333 333  \n'
        l = s.split('\n')
        assert l == ['111 111','222  222 ',' 333 333  ','']
        l = s.splitlines()
        assert l == ['111 111','222  222 ',' 333 333  ']

        template_map = {
            'k1':'v1',
            'k2':'v2',
            'k3':'v3'
        }
        string_template = """
            Template String
            line1: {k1}
            line2:  {k2}
            line3: {k3}
        """
        exp = '\n' + \
              '            Template String\n' + \
              '            line1: v1\n' + \
              '            line2:  v2\n' + \
              '            line3: v3\n' + \
              '        '
        v = string_template.format(**template_map)
        assert v == exp

        s = "hello\n\n\nhi\n\n\nbye\n"
        s1 = re.sub(r"\n+","\n",s)
        assert s1 == "hello\nhi\nbye\n"
        idx = s.find('hi')              # string search
        assert idx != 0
        idx = s.find('badstring')
        assert idx == -1

        groups = re.search(r'hi',s)
        assert groups is not None
        group = groups.group()
        assert group is not None
        groups = re.search(r'badstring',s)
        assert groups is None

        assert 'hi' in s
        assert 'badstring' not in s

        l = ['v1','v2','v3']
        assert 'v2' in l
        assert 'badstring' not in l
        assert l.index('v2') == 1
        assert l.index('v3') == 2
        assert l[2] == 'v3'
        #assert l.index('badstring') is None # this will exception

        res = [i for i, j in enumerate(l) if j == 'v2']
        assert len(res) == 1 and res[0] == 1

        l = ['v1','v2','v3','v2']
        res = [i for i, j in enumerate(l) if j == 'v2']
        assert len(res) == 2 and res == [1,3]

        res = [j for j, j in enumerate(l) if j == 'v2']
        assert len(res) == 2 and res == ['v2','v2']

        res = [j for j, j in enumerate(l) if j == 'v1' or j == 'v3']
        assert len(res) == 2 and res == ['v1','v3']

        res = [i for i, j in enumerate(l) if j == 'v1' or j == 'v3']
        assert len(res) == 2 and res == [0,2]

        # repeat string
        s = ' ' * 5
        assert s == '     '
        s = 'a' * 3
        assert s == 'aaa'
        s = 'a ' * 3
        assert s == 'a a a '
        s = 'abc' * 3
        assert s == 'abcabcabc'

        s = """
        this is a multiline
        string where there
        should be three.
        """

        assert s == "\n        this is a multiline\n        string where there\n        should be three.\n        "
        #p(s)

        s = \
"""this is a multiline
string where there
should be three."""
        assert s == "this is a multiline\nstring where there\nshould be three."

        s = "this is a multiline\n" \
            "string where there\n" \
            "should be three."
        assert s == "this is a multiline\nstring where there\nshould be three."

        s = "this is a multiline\n" + \
            "string where there\n" + \
            "should be three."
        assert s == "this is a multiline\nstring where there\nshould be three."

        s = "this is a multiline\n" + "string where there\n" + "should be three."
        assert s == "this is a multiline\nstring where there\nshould be three."

        vdog = "dog"
        vcat = "cat"
        s = \
"""this is a multiline {}
string where there {}
should be three.""".format(vdog,vcat)
        assert s == "this is a multiline dog\nstring where there cat\nshould be three."


        #p('test_string')

        s = 'abc'
        assert s.isalpha()
        assert not s.isdecimal()
        s = 'abc ?'
        assert not s.isalpha()
        s = '123'
        assert s.isdecimal()
        s = '12.3'
        assert not s.isdecimal()
        s = ''
        assert not s.isspace()
        s = '  '
        assert s.isspace()
        s = 'hello little big world!'
        assert s.startswith('hello ')
        assert s.endswith('rld!')
        a = s.split()
        assert a == ['hello','little','big','world!']

        #    0 0 0 0 0 1 1 1 1 1 2
        #    0 2 4 6 8 0 2 4 6 8 0
        s = 'hello there'

        #             0 0 0 0 0 1 1 1 1 1 2
        #             0 2 4 6 8 0 2 4 6 8 0
        s1 = s.rjust(20)
        assert s1 == '         hello there'
        s1 = s.rjust(20,'-')
        assert s1 == '---------hello there'
        s1 = s.ljust(20)
        assert s1 == 'hello there         '
        s1 = s.ljust(20,'-')
        assert s1 == 'hello there---------'
        s1 = s.center(20,'-')
        assert s1 == '----hello there-----' # centered with 1 off left

        vcat = "cat"
        vdog = "dog"
        vint = 123
        s = f"hello {vcat}, you are a {vdog}, and you are {vint} years old"
        assert s == "hello cat, you are a dog, and you are 123 years old"
        s = "hello {}, you are a {}, and you are {} years old".format(vcat,vdog,vint)
        assert s == "hello cat, you are a dog, and you are 123 years old"

        # templates used for html output and stuff
        d = {
            'k1s':'v1',
            'k2i':22,
            'k3i':33,
            'k4s':'v4'
        }
        st1 = string.Template("""
var:  $k1s and $k2i
esc:  $$
str:  var${k1s}end with ${k2i} and ${k4s}blah
""")

        # the variables must have data type appended s,d,f,x
        st2 = """
var:  %(k1s)s and %(k2i)d
esc:  %%
str:  var%(k1s)send with %(k2i)d and %(k4s)sblah
"""

        st3 = """
var:  {k1s} and {k2i}
esc:  {{}}
str:  var{k1s}end with {k2i} and {k4s}blah
"""

        s = st1.substitute(d)
        assert s == "\nvar:  v1 and 22\nesc:  $\nstr:  varv1end with 22 and v4blah\n"

        s = st2 % d
        assert s == "\nvar:  v1 and 22\nesc:  %\nstr:  varv1end with 22 and v4blah\n"

        s = st3.format(**d)
        assert s == "\nvar:  v1 and 22\nesc:  {}\nstr:  varv1end with 22 and v4blah\n"

        s = 'abc 2:4:56PM def'
        m = re.search('([\d]{2}):([\d]{2}):([\d]{2})(AM|PM)',s)   # group match
        assert m == None

        m = re.search('([\d]{1,2}):([\d]{1,2}):([\d]{1,2})(AM|PM)',s)   # group match
        assert m.group(0) == '2:4:56PM' and m.group(1) == '2' and m.group(2) == '4' and m.group(4) == 'PM'
        assert len(m.groups()) == 4                                     # number of groups. groups itself is a tuple
        assert m.group(1,2,3) == ('2','4','56')                         # multiple args in group gives a tuple
        assert re.search('.*\d{1}:\d{1}:\d{1,2}(?:AM|PM).*',s)
        assert re.search('\d{1}:\d{1}:\d{1,2}(?:AM|PM)',s)              # this would fail match

        assert re.match('2:4:56PM',s) == None
        assert re.match('.*\d{1,2}:\d{1,2}:\d{1,2}(?:AM|PM).*',s)           # (?:AM|PM) means non group capture
        assert re.match('.*\d{1}:\d{1,2}:\d{1,2}(?:AM|PM).*',s)             # (?:AM|PM) means non group capture
        assert re.match('.*\d{1}:\d{1}:\d{1,2}(?:AM|PM).*',s)               # (?:AM|PM) means non group capture
        assert re.match('[\w\s]+\d{1}:\d{1}:\d{1,2}(?:AM|PM).*',s)          # (?:AM|PM) means non group capture
        assert re.match('[\w\s]+\d{1}:\d{1}:\d{1,2}(?:AM|PM)[\w\s]+',s)     # (?:AM|PM) means non group capture
        assert re.match('^[\w\s]+\d{1}:\d{1}:\d{1,2}(?:AM|PM)[\w\s]+',s)    # (?:AM|PM) means non group capture
        assert re.match('[\w\s]+\d{1}:\d{1}:\d{1,2}(AM|PM).*',s)            # (AM|PM) means group capture
        assert re.match('.*\d{1}:\d{2}:\d{1,2}(?:AM|PM).*',s) == None       # (?:AM|PM) means non group capture

        s = 'abc 12:34:56PM def'
        m = re.search('([\d]{2}):([\d]{2}):([\d]{2})(AM|PM)',s)   # group match
        assert m.group(0) == '12:34:56PM' and m.group(1) == '12' and m.group(2) == '34' and m.group(4) == 'PM'

        s = 'abc 12:34:56AM def'

        m = re.search('([\d]{2}):([\d]{2}):([\d]{2})(AM|PM)',s)   # group match
        assert m.group(0) == '12:34:56AM' and m.group(1) == '12' and m.group(2) == '34'

        m = re.search('(\d{2}):(\d{2}):(\d{2})(AM|PM)',s)   # group match
        assert m.group(0) == '12:34:56AM' and m.group(1) == '12' and m.group(2) == '34'

        s = 'abc 1:2:3PM 1:2:3AM 2:3:4PM 4:5:6PM 5:6:7AM def'
        m = re.search('(\d+):(\d+):(\d+)(AM|PM)',s)
        assert m.group(0) == '1:2:3PM'
        m = re.findall('(\d+):(\d+):(\d+)(?:PM)',s)                         # (?:PM) is non capturing, find all
        assert len(m) == 3
        assert m[0] == ('1','2','3')
        assert m[1] == ('2','3','4')
        assert m[2] == ('4','5','6')

        m = re.findall('(\d+):(\d+):(\d+)(?:AM|PM)',s)                      # (?:PM) is non capturing, find all
        assert len(m) == 5
        assert m[0] == ('1','2','3')
        assert m[1] == ('1','2','3')
        assert m[2] == ('2','3','4')
        assert m[3] == ('4','5','6')
        assert m[4] == ('5','6','7')

        #    ___
        #      ___
        #        ___
        #          ___
        #            ___
        s = '1:2:3:4:5:6:7'

        m = re.findall('(\d+):(\d+):(?:\d+)',s)                             # non group capture
        assert len(m) == 2
        assert m == [('1','2'),('4','5')]

        m = re.findall('(\d+):(\d+):(?=\d+)',s)                             # positive lookahead == non group capture and non overlap
        assert len(m) == 3
        assert m == [('1','2'),('3','4'),('5','6')]

        m = re.findall('(\d+):(\d+):(\d+)',s)                               # all group capture
        assert len(m) == 2
        assert m == [('1','2','3'),('4','5','6')]

        m = re.findall('(\d+):(\d+)',s)
        assert len(m) == 3
        assert m == [('1','2'),('3','4'),('5','6')]

        s = '1:2:3:b:4:5:6:7'

        m = re.findall('(\d+):(\d+):(?:\d+)',s)                             # non group capture
        assert len(m) == 2
        assert m == [('1','2'),('4','5')]

        m = re.findall('(\d+):(\d+):(?=\d+)',s)                             # positive lookahead == non group capture and non overlap
        assert len(m) == 2
        assert m == [('1','2'),('4','5')]

        m = re.findall('(\d+):(?![a-z]+)',s)                                # negative lookahead == non group capture and non overlap
        assert len(m) == 5
        assert m == [('1'),('2'),('4'),('5'),('6')]

        m = re.findall('(\d+):(\d+):(\d+)',s)                               # all group capture
        assert len(m) == 2
        assert m == [('1','2','3'),('4','5','6')]

        m = re.findall('(\d+):(\d+)',s)
        assert len(m) == 3
        assert m == [('1','2'),('4','5'),('6','7')]


        s = ' 1 2 3 4  5 '

        a = s.split()
        assert a == ['1','2','3','4','5']

        a = re.split('\s+',s)
        assert a == ['','1','2','3','4','5','']

        a = re.split('\s+',s.strip())
        assert a == ['1','2','3','4','5']

        s = 'the cat in the hat is fat'

        s0 =    '00 abcdefg hijklmnop qrstuv wxyz 1234567890 x0000\n' + \
                '01 abcdefg hijklmnop qrstuv wxyz 1234567890 x0001\n' + \
                '02 abcdefg hijklmnop qrstuv wxyz 1234567890 x0002\n' + \
                '03 abcdefg hijklmnop qrstuv wxyz 1234567890 x0003\n' + \
                '04 abcdefg hijklmnop qrstuv wxyz 1234567890 x0004\n' + \
                '05 abcdefg hijklmnop qrstuv wxyz 1234567890 x0005\n' + \
                '06 abcdefg hijklmnop qrstuv wxyz 1234567890 x0006\n' + \
                '07 abcdefg hijklmnop qrstuv wxyz 1234567890 x0007\n' + \
                '08 abcdefg hijklmnop qrstuv wxyz 1234567890 x0008\n' + \
                '09 abcdefg hijklmnop qrstuv wxyz 1234567890 x0009\n' + \
                '0A abcdefg hijklmnop qrstuv wxyz 1234567890 x000A\n' + \
                '0B abcdefg hijklmnop qrstuv wxyz 1234567890 x000B\n' + \
                '0C abcdefg hijklmnop qrstuv wxyz 1234567890 x000C\n' + \
                '0D abcdefg hijklmnop qrstuv wxyz 1234567890 x000D\n' + \
                '0E abcdefg hijklmnop qrstuv wxyz 1234567890 x000E\n' + \
                '0F abcdefg hijklmnop qrstuv wxyz 1234567890 x000F\n' + \
                '10 abcdefg hijklmnop qrstuv wxyz 1234567890 x0012\n'


        i = 1234
        si = str(i)
        assert si == '1234'
        rsi = list(reversed(si))
        assert rsi == ['4','3','2','1']
        rs = ''.join(rsi)
        assert rs == '4321'
        ri = int(rs)
        assert ri == 4321

        assert int(str(i)[::-1]) == 4321

        s = 'abcdefghijk'
        assert 'def' in s
        assert 'fed' not in s

        v1 = 'hello'
        v2 = 'cat'
        v3 = f"i said: {v1}, you are a {v2}"    # another way of formatting
        assert v3 == 'i said: hello, you are a cat'

        p('pass regex')

    def test_byte_binary_conversion(self):
        '''
        ascii table

        hex     char
        20      space
        21      !
        22      "
        23      #
        24      $
        25      %
        26      &
        27      '
        28      (
        29      )
        2A      *
        2B      +
        2C      ,
        2D      -
        2E      .
        2F      /
        30      0
        31      1
        32      2
        33      3
        34      4
        35      5
        36      6
        37      7
        38      8
        39      9
        3A      :
        3B      ;
        3C      <
        3D      =
        3E      >
        3F      ?
        40      @   `   @
        41      A
        42      B
        43      C
        44      D
        45      E
        46      F
        47      G
        48      H
        49      I
        4A      J
        4B      K
        4C      L
        4D      M
        4E      N
        4F      O
        50      P
        51      Q
        52      R
        53      S
        54      T
        55      U
        56      V
        57      W
        58      X
        59      Y
        5A      Z
        5B      [
        5C      \   ~   \
        5D      ]
        5E      ↑   ^
        5F      ←   _
        60      @   `
        61      a
        62      b
        63      c
        64      d
        65      e
        66      f
        67      g
        68      h
        69      i
        6A      j
        6B      k
        6C      l
        6D      m
        6E      n
        6F      o
        70      p
        71      q
        72      r
        73      s
        74      t
        75      u
        76      v
        77      w
        78      x
        79      y
        7A      z
        7B      {
        7C      ACK   ¬   |
        7D      }
        7E      ESC   |   ~
        '''

        # byte array, string to byte, ascii, int byte

        # test char to ascii decimal and ascii to char
        s = 'hello'
        l = []
        for i in range(len(s)):
            c = s[i]
            vascii = ord(c)
            vchar  = chr(vascii)
            l.append(vascii)
            assert vchar == c
        assert l == [104,101,108,108,111]

        # convert string to bytes binary and bytes to string
        vs = 'hello'
        lb = []
        for i in range(len(vs)):
            vc = s[i]
            va = ord(vc)


        # char to ascii, unicode encode/decode
        s  = 'hello'
        lc = [c for c in s]
        la = [ord(c) for c in lc]
        lb = bytes(la)  # bytes uses a list input
        ba = bytearray(la)
        lr = [chr(a) for a in la]
        assert lc == ['h','e','l','l','o']
        assert la == [0x68,0x65,0x6c,0x6c,0x6f]
        assert lb == b'\x68\x65\x6c\x6c\x6f'
        assert ba == b'\x68\x65\x6c\x6c\x6f'
        assert ba[1] == 0x65
        assert ba[1] != b'\x65'
        assert 0x65 != b'\x65'
        assert lr == ['h','e','l','l','o']
        assert 'hello' == ''.join(lr)
        rb = b"hello"
        assert rb == b'\x68\x65\x6c\x6c\x6f'
        rb = 'hello'.encode('utf-8')
        assert rb == b'\x68\x65\x6c\x6c\x6f'
        assert rb == bytearray(b'\x68\x65\x6c\x6c\x6f')
        rs = rb.decode('utf-8')
        assert rs == 'hello'
        ba = bytearray('hello','utf-8')
        assert ba == bytearray(b'hello')
        assert ba == b'\x68\x65\x6c\x6c\x6f'

        # modify bytearray
        ba[0] = 0x20
        assert ba == b'\x20\x65\x6c\x6c\x6f'
        ba[3] = 0x21
        assert ba == b'\x20\x65\x6c\x21\x6f'
        flag = False
        try:
            # ValueError because must be byte
            ba[3] = 0x2222
        except Exception as e:
            flag = True
        assert flag
        assert ba == b'\x20\x65\x6c\x21\x6f'


        # int array to byte, byte to int array, length of bytearray
        lb = bytes([6,8,10,12,14,255])              # bytes is immutable
        assert lb == b'\x06\x08\x0a\x0c\x0e\xff'
        assert len(lb) == 6
        assert lb != b'\x06\x08\x0a\x0c\x0f\xfe'
        li = [i for i in lb]
        assert li == [6,8,10,12,14,255]
        lb = [b for b in li]
        assert lb == [6,8,10,12,14,255]
        lb = bytes([255])
        assert lb == b'\xff'

        # int.from_bytes
        r = int.from_bytes(b'\x00\x10', byteorder='big')
        assert r == 0x10
        r = int.from_bytes([0x30,0x20,0x00,0x10], byteorder='big')
        assert r == 0x30200010
        r = int.from_bytes(b'\x00\x10', byteorder='little')
        assert r == 0x1000
        r = int.from_bytes([0x30,0x20,0x00,0x10], byteorder='little')
        assert r == 0x10002030



        # bytearray is mutable
        ba = bytearray()
        ba.append(6)
        assert ba == b'\x06'
        ba.append(8)
        assert ba == b'\x06\x08'
        ba.append(16)
        assert ba == b'\x06\x08\x10'
        assert len(ba) == 3
        assert ba[0] == 0x06 and ba[1] == 0x08
        li = [i for i in ba]
        assert li == [0x06,0x08,0x10]



        # packed unpack struct binary data
        '''
        with open(filename,'rb') as file:
            binary_data = file.read()
        '''

        # convert string to base64 and base64 to string
        s = 'hello this is a sentence'
        ba = s.encode('utf-8')
        b64 = codecs.encode(ba,'base64')

        out_ba = codecs.decode(b64,'base64')
        out_s = out_ba.decode('utf-8')
        assert s == out_s
        assert ba == b'hello this is a sentence'
        assert b64 == b'aGVsbG8gdGhpcyBpcyBhIHNlbnRlbmNl\n'

        # binary to hex and hex to binary
        bahex = binascii.hexlify(ba)
        baunhex = binascii.unhexlify(bahex)
        s_out = baunhex.decode('utf-8')
        assert bahex == b'68656c6c6f207468697320697320612073656e74656e6365'
        assert baunhex == b'hello this is a sentence'
        assert s_out == 'hello this is a sentence'

        l1 = [hex(v) for v in bahex]
        l2 = [v for v in bahex]
        assert bahex[0] == 0x36 # this is hex of 0x68, which is wrong
        assert baunhex[0] == 0x68   # h
        assert baunhex[1] == 0x65   # e

        ba = bytearray()    # mutable bytearray
        sz = 0x11
        for i in range(sz):
            ba.append(i)
        assert ba == b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10'
        bahex = binascii.hexlify(ba)
        baunhex = binascii.unhexlify(bahex)
        assert bahex == b'000102030405060708090a0b0c0d0e0f10'
        assert baunhex == b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10'

        # convert long (> 4 bytes) binary data to string of 0 and 1 and convert back for equivalence
        s1 = 'njfwehr32jrnkw'
        ba = s1.encode('utf-8')
        b64 = codecs.encode(ba,'base64')
        assert b64 == b'bmpmd2VocjMyanJua3c=\n'
        lbi = [i for i in ba]
        assert lbi == [110, 106, 102, 119, 101, 104, 114, 51, 50, 106, 114, 110, 107, 119]
        lh = [hex(i) for i in lbi]
        assert lh == ['0x6e', '0x6a', '0x66', '0x77', '0x65', '0x68', '0x72', '0x33', '0x32', '0x6a', '0x72', '0x6e', '0x6b', '0x77']
        sz_s1 = len(s1)
        assert sz_s1 == 14
        assert len(lh) == sz_s1
        assert len(lbi) == sz_s1
        lbinarystring = []
        for i in lbi:
            for j in range(7,-1,-1):
                v = (i >> j) & 0x1
                lbinarystring.append(str(v))
        sbin = ''.join(lbinarystring)
        assert sbin == '0110111001101010011001100111011101100101011010000111001000110011001100100110101001110010011011100110101101110111'
        sz_sbin = len(sbin)
        assert sz_sbin == (sz_s1*8)
        # now convert string binary 1 and 0 to string
        ctr = 0
        b = 0x00
        out_ba = bytearray()
        for c in sbin:
            i = 0 if c == '0' else 1
            b = (b << 1) | (i & 0x1)
            ctr += 1
            if ctr % 8 == 0:
                out_ba.append(b)
                b = 0x00
                ctr = 0
        assert out_ba == ba

        # int to bytes and bytes to int
        i = 0x12_34_56_78
        # b = bytes([i]) # not allowed because i is not a byte 0-255
        # b1 = (i).to_bytes(4) # must specify endian
        b2 = (i).to_bytes(4,byteorder='little')
        b3 = (i).to_bytes(4,byteorder='big')
        i21 = int.from_bytes(b2,byteorder='little')
        i22 = int.from_bytes(b2,byteorder='big')
        i31 = int.from_bytes(b3,byteorder='little')
        i32 = int.from_bytes(b3,byteorder='big')
        s2 = b2.hex()
        s3 = b3.hex()
        s21 = hex(i21)
        s22 = hex(i22)
        s31 = hex(i31)
        s32 = hex(i32)

        assert len(b2) == 4
        assert len(b3) == 4
        assert b3 != b'\x12345678'
        assert b3 == b'\x12\x34\x56\x78'
        assert i == 0x12345678
        assert i21 == 0x12345678
        assert i22 == 0x78563412
        assert i31 == 0x78563412
        assert i32 == 0x12345678
        assert s2 == '78563412'
        assert s3 == '12345678'
        assert s21 == '0x12345678'
        assert s22 == '0x78563412'
        assert s31 == '0x78563412'
        assert s32 == '0x12345678'

        l = [
            0x12345678,
            0x23456789,
            0x3456789a,
            0x456789ab,
            0x56789abc
        ]

        lb = [(i).to_bytes(4,byteorder='big') for i in l]

        for bval in lb:
            assert len(bval) == 4

        li = [int.from_bytes(b,byteorder='big') for b in lb]
        assert li == l

        lb = [(i).to_bytes(8,byteorder='big') for i in l]

        for bval in lb:
            assert len(bval) == 8

        # string to bytearray and bytearray to string byte to string

        s1 = 'hello there '
        s2 = 'cat dog'

        ba = bytearray()
        ba.extend(s1.encode('utf-8'))
        ba.extend(s2.encode('utf-8'))
        sa = ba.decode("utf-8")
        assert sa == 'hello there cat dog'

        ba2 = bytearray(s1,encoding="utf-8")
        sa2 = ba2.decode('utf-8')
        assert sa2 == 'hello there '

        h1 = ba.hex()   # bytearray to hex string
        assert h1 == '68656c6c6f2074686572652063617420646f67'

        h2 = ba2.hex()
        assert h2 == '68656c6c6f20746865726520'

        slc = 'abcdefghijklmnopqrstuvwxyz'
        suc = slc.upper()
        assert suc == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        dlc = {}
        duc = {}
        sz = len(slc)
        # a-97=0, A-65=0
        for i in range(sz):
            vlc = ord(slc[i]) - 97
            vuc = ord(suc[i]) - 65
            dlc[i]=vlc
            duc[i]=vuc
        assert dlc == duc
        assert dlc[25] == 25
        assert 'A' == 'a'.upper()
        assert 'a' == 'A'.lower()


        s0 =    '00 abcdefg hijklmnop qrstuv wxyz 1234567890 x0000\n' + \
                '01 abcdefg hijklmnop qrstuv wxyz 1234567890 x0001\n' + \
                '02 abcdefg hijklmnop qrstuv wxyz 1234567890 x0002\n' + \
                '03 abcdefg hijklmnop qrstuv wxyz 1234567890 x0003\n' + \
                '04 abcdefg hijklmnop qrstuv wxyz 1234567890 x0004\n' + \
                '05 abcdefg hijklmnop qrstuv wxyz 1234567890 x0005\n' + \
                '06 abcdefg hijklmnop qrstuv wxyz 1234567890 x0006\n' + \
                '07 abcdefg hijklmnop qrstuv wxyz 1234567890 x0007\n' + \
                '08 abcdefg hijklmnop qrstuv wxyz 1234567890 x0008\n' + \
                '09 abcdefg hijklmnop qrstuv wxyz 1234567890 x0009\n' + \
                '0A abcdefg hijklmnop qrstuv wxyz 1234567890 x000A\n' + \
                '0B abcdefg hijklmnop qrstuv wxyz 1234567890 x000B\n' + \
                '0C abcdefg hijklmnop qrstuv wxyz 1234567890 x000C\n' + \
                '0D abcdefg hijklmnop qrstuv wxyz 1234567890 x000D\n' + \
                '0E abcdefg hijklmnop qrstuv wxyz 1234567890 x000E\n' + \
                '0F abcdefg hijklmnop qrstuv wxyz 1234567890 x000F\n' + \
                '10 abcdefg hijklmnop qrstuv wxyz 1234567890 x0012\n'

        # string to byte array and byte array to string

        ba0 = bytes(s0,'utf-8')
        ba1 = s0.encode('utf-8')
        ba2 = bytearray(s0,'utf-8')

        vs0 = ba0.decode('utf-8')
        vs1 = ba1.decode('utf-8')
        vs2 = ba2.decode('utf-8')

        assert vs0 == s0
        assert vs1 == s0
        assert vs2 == s0

        sz = len(ba1)
        szchunk = 16
        szmod = sz % szchunk
        bchunks = [ ba1[i:i+szchunk] for i in range(0, len(ba1), szchunk) ]
        for chunk in bchunks:
            if len(chunk) != szchunk:   # for final chunk
                assert len(chunk) == szmod

        ba = bytearray()                # bytes immutable, use bytearray
        for chunk in bchunks:
            ba += bytearray(chunk)      # append bytes
        bv0 = bytes(ba)
        assert len(bv0) == sz
        vs = bv0.decode('utf-8')
        assert vs == s0

        ba = bytearray()
        for chunk in bchunks:
            ba.extend(chunk)            # extend bytes
        bv0 = bytes(ba)
        assert len(bv0) == sz
        vs = bv0.decode('utf-8')
        assert vs == s0

        bins = s0.encode('utf-8')
        b64e = base64.b64encode(bins)
        b64d = base64.b64decode(b64e)
        vs   = b64d.decode('utf-8')
        assert vs == s0

        b64e = base64.encodebytes(bins) # inserts newline after every 76 bytes
        b64d = base64.decodebytes(b64e)
        vs   = b64d.decode('utf-8')
        assert vs == s0
        b64d = base64.b64decode(b64e)   # this seems to remove newline too!
        vs   = b64d.decode('utf-8')
        assert vs == s0

        return


    def test_set_vs_map_vs_list(self):
        vset = set() # there is no literal for empty set, use this
        vm1 = dict()
        vm2 = {}

        vset.add(1)
        vset.add(1)
        vset.add(2)
        vset.add(3)
        assert len(vset) == 3
        assert isinstance(vset,set)
        assert isinstance(vm1,dict)
        assert isinstance(vm2,dict)
        assert isinstance(vset,dict) == False

        l = None
        assert l == None
        assert l is None

        l = [1,2,3,3,4,5,5]
        d = {}
        cnt = 0
        for v in l:
            if v in d: d[v] += 1
            else:      d[v] = 1
            cnt += 1
        assert cnt == 7
        assert len(d) == 5

        numduplicates = 0
        for k,v in d.items():
            if(v > 1): numduplicates += v
        assert numduplicates == 4

        s = set(l)
        assert len(s) == 5
        assert len(l) == 7
        assert s == {1,2,3,4,5}
        assert l == [1,2,3,3,4,5,5]

        assert 3 in s
        s.remove(3)
        assert 3 not in s
        assert s == {1,2,4,5}

        try:
            flag = False
            s.remove(10)
        except KeyError as e:
            flag = True
        assert flag == True

        s.remove(1)
        s.remove(2)
        s.remove(4)
        s.remove(5)
        assert len(s) == 0
        assert s != {}      # there is no literal for empty set, this is empty dict
        assert s == set()

        l = []
        l.append(None)
        l.append(1)
        l.append(None)
        l.append(1)
        assert l == [None,1,None,1]

        s1 = {1,2,3,4,5}
        s2 = {3,2,4,5,1}
        s4 = {} # there is no literal for empty set
        assert isinstance(s1,set)
        assert not isinstance(s1,dict)
        assert not isinstance(s4,set)
        assert isinstance(s4,dict)
        s3 = s1.difference(s2)
        assert len(s3) == 0
        s1 = {1,2,3,4,5}            # delete set
        assert 3 in s1
        assert len(s1) == 5
        s1.remove(3)
        assert len(s1) == 4
        assert 3 not in s1

        s1 = {1,2,3,4,5}
        s2 = {3,2,4,5,1,6}
        s3 = s1.difference(s2)
        assert len(s3) == 0         # because s1-s2 is empty
        s3 = s2.difference(s1)
        assert len(s3) == 1         # because s2-s1 is not empty
        assert 6 in s3
        s3 = s1.symmetric_difference(s2)
        assert len(s3) == 1         # because in either s1 or s2 but not both
        assert 6 in s3

        if 6 in s2:
            s2.remove(6)            # KeyError if not present. use discard if no KeyError
        s3 = s1.symmetric_difference(s2)
        assert len(s3) == 0
        s2.discard(6)               # no KeyError
        flag = False
        try:
            s2.remove(6)            # error
        except Exception as e:
            flag = True
        assert flag
        s2.discard(6)               # no error
        s3 = s1.symmetric_difference(s2)
        assert len(s3) == 0

        s1 = {1,2,3}
        s2 = {3,4,5}
        s3 = s1.union(s2)
        assert len(s3) == 5
        s3 = s1.intersection(s2)
        assert len(s3) == 1
        assert 3 in s3

        # ordered set to list
        l1 = [5,4,3,2,1,3,5]
        l1.sort()
        s1 = set(l1)
        l2 = list(dict.fromkeys(s1).keys())
        assert l2 == [1,2,3,4,5]

        l1 = [1,1,2,2,2,3,4,4,5,6,6]
        assert len(l1) == 11
        d = collections.Counter(l1)
        assert len(d) == 6
        assert 2 in d
        assert d[2] == 3    # Counter stores count only

        d = { i:(i+1) for i in range(5) }
        assert len(d) == 5
        assert d[0] == 1
        s1 = set(d.keys())
        s2 = set(d.values())
        assert s1 == {0,1,2,3,4}
        assert s2 == {1,2,3,4,5}

        d = {1:2,2:2,3:4,4:5,5:4}
        assert len(d) == 5
        s1 = set(d.keys())
        s2 = set(d.values())
        assert s1 == {1,2,3,4,5}
        assert s2 == {2,4,5}

        flag = False
        d = {1:10,2:20,3:30,4:40,5:50}
        assert len(d) == 5
        v = d.pop(2,None)
        assert v == 20
        v = d.pop(10,None)      # no key error raised here
        assert v == None
        try:
            d.pop(10)
        except Exception as e:
            flag = True
        assert flag == True
        d.pop(10,None)      # no key error raised here
        assert 10 not in d
        assert len(d) == 4
        del d[3]            # no key error raised here
        flag = False
        try:
            del d[10]
        except Exception as e:
            flag = True
        assert flag == True

        l = []
        l.append(1)
        l.append(2)
        l.append(3)
        l.append(4)
        l.pop()
        assert l == [1,2,3]
        l.pop(0)
        assert l == [2,3]
        l.clear()
        assert l == []

        l = [[] for i in range(3)]
        assert l == [[],[],[]]
        assert l != []
        assert l != [[],[]]
        l[0].append(1)
        l[1].append(2)
        l[2].append(3)
        assert l == [[1],[2],[3]]

        l = [i for i in range(3)]
        assert l == [0,1,2]

        l = [[2] * 3]
        assert l == [[2,2,2]]

        l = [2] * 3
        assert l == [2,2,2]
        l[1] = 3
        assert l == [2,3,2]
        l1 = l.copy()
        assert l1 == [2,3,2]
        l1[0] = 3
        assert l1 == [3,3,2]
        assert l == [2,3,2]

        # list to set
        l = [1,1,2,3,4,5,5]
        assert len(l) == 7
        s = set(l)
        assert len(s) == 5
        l = list(s)                 # set to list
        assert len(l) == 5

        # merge dict
        d1 = {'k1':'v1','k2':'v2','k3':'v3'}
        d2 = {'k4':'v4','k5':'v5','k6':'v6','k7':'v7'}
        d3 = dict(k1='v1',k2='v2',k3='v3')
        d4 = {'k1':'v1','k2':'v2','k3':'v3'}
        assert len(d1) == 3
        assert len(d2) == 4
        d5 = d1.copy() # make copy first
        d1.update(d2)
        assert len(d1) == 7
        assert len(d2) == 4
        d1 = d5.copy()
        assert len(d1) == 3
        assert d1 == d4
        assert d1 == d3
        assert d2 != d4
        assert len(d3) == 3
        assert d3['k1'] == 'v1'

        s1 = d1.keys() & d2.keys()  # overlapping keys
        assert len(s1) == 0
        s1 = d1.keys() & d3.keys()  # overlapping keys
        assert len(s1) == 3
        assert d1.items() == d3.items()

        assert {'k1':'v1','k2':'v2'} == {'k1':'v1','k2':'v2'}
        assert {'k1':'v1','k2':'v2'} == {'k2':'v2','k1':'v1'}
        assert {'k1':'v2','k2':'v2'} != {'k1':'v1','k2':'v2'}

        d1 = {'k1':'v1','k2':'v2','k3':'v3'}
        d2 = {'k1':'v1','k2':'v2','k3':'v3'}
        assert d1.items() == d2.items()
        d2 = {'k1':'v2','k2':'v2','k3':'v3'}
        assert d1.items() != d2.items()
        s1 = d1.keys() & d2.keys()
        assert len(s1) == 3
        s1 = d1.items() & d2.items()
        assert len(s1) == 2

        # tuple
        v = ('v1','v2')
        v[0] == 'v1'
        v[1] == 'v2'
        v = ('v2','v1')
        v[0] == 'v2'
        v[1] == 'v1'

        d = {(0,1):20,(1,0):10}
        assert d[(1,0)] == 10
        assert d[(0,1)] == 20

        d1 = {
            'k1':10,
            'k2':20,
            'k3':10
        }

        d2 = {
            'k1':10,
            'k2':20,
            'k3':30
        }

        keys1 = d1.keys()
        keys2 = d2.keys()
        assert keys1 == keys2
        assert d1.values() != d2.values()

        assert len(keys1) == 3
        assert len(keys2) == 3                  # when underlying dict changes, the view changes
        d2['k4'] = 40                           # change underlying dict and the view changes
        assert len(keys2) == 4                  # change underlying dict and the view changes
        assert 'k1' in keys1
        assert 'k9' not in keys1
        vals1 = d1.values()
        vals2 = d1.values()
        assert vals1 != vals2                   # equality of dict.values() always returns False
        assert vals1 == vals1
        assert len(vals1) == 3                  # returns all the values
        assert not isinstance(vals1,list)       # dict view is not a list

        set1 = set([1,2,2,3])
        set2 = set([2,3,4,5,5])
        assert len(set1) == 3
        assert len(set2) == 4
        diff1 = set1 - set2
        diff2 = set2 - set1
        assert len(diff1) == 1
        assert len(diff2) == 2
        assert diff1 == set([1])
        assert diff2 == set([4,5])
        set3 = set1 & set2
        assert set3 == set([2,3])

        # numeric dict/map
        d = {
            1:2,
            3:4,
            10:20,
            20:30,
            50:50
        }
        assert len(d) == 5
        assert d[1] == 2 and d[20] == 30

        # invert dict/map, assuming all uniq
        dinv1 = {v:k for k,v in d.items()}
        dinv2 = dict(zip(d.values(),d.keys()))
        dinv3 = dict([[v,k] for k,v in d.items()])
        assert len(dinv1) == 5
        assert dinv1[2] == 1 and dinv1[30] == 20
        assert dinv1 == dinv2
        assert dinv1 == dinv3

        # modify map values in single line
        d1 = dict([['%{:02}'.format(k),'%{:02}'.format(v)] for k,v in d.items()])
        d2 = {'%{:02}'.format(k):'%{:02}'.format(v) for k,v in d.items()}
        dexp = {
            '%01':'%02',
            '%03':'%04',
            '%10':'%20',
            '%20':'%30',
            '%50':'%50'
        }
        assert d1 == dexp
        assert d2 == dexp

        # dict to json
        d1 = {"k1":"v1","k2":"v2","k3":[1,2,3],"k4":{"k4.1":"v4.1","k4.2":"v4.2"}}
        d2 = {"k1":"v1","k2":"v2","k3":[1,2,3],"k4":{"k4.1":"v4.1","k4.2":"v4.2"}}
        d3 = {"k1":"v1","k2":"v2","k3":[1,2,3],"k4":{"k4.1":"v4.1","k4.2":"v4.x"}}
        assert d1 == d2
        assert d2 != d3

        j1 = json.dumps(d1)
        json_pretty = json.dumps(d1,indent=4,sort_keys=True)
        print(json_pretty)
        d4 = json.loads(j1)

        assert d1 == d4
        assert j1 == '{"k1": "v1", "k2": "v2", "k3": [1, 2, 3], "k4": {"k4.1": "v4.1", "k4.2": "v4.2"}}'
        # stupid string value MUST be like this. dont ever compare string vals
        assert isinstance(j1,str)
        assert isinstance(d1,dict)

        a_points = [
            (5,5,5),
            (3,5,8),
            (7,2,4),
            (8,8,8),
            (2,2,2)
        ]

        assert isinstance(a_points,list)
        assert len(a_points) == 5
        p = a_points[2]
        assert len(p) == 3
        assert isinstance(p,tuple)
        assert p[0] == 7 and p[2] == 4 and p == (7,2,4) and p != (7,2,4,1) and p != (7,1,4)

        flag = False
        p = (1,2,3)
        try:
            p[1] = 3        # cannot modify immutable tuple
        except Exception as e:
            flag = True
        assert flag
        assert p[1] == 2

        l = [None for i in range(3)]
        assert l == [None,None,None]
        assert len(l) == 3
        assert l != [None,None]
        l[2] = 1
        assert l == [None,None,1]

        # deepcopy vs copy of 2 dimension list
        ap1 = [[10,20],[30,40],[50,60]]
        ap2 = copy.copy(ap1)
        ap3 = copy.deepcopy(ap1)
        assert ap2 == ap1
        assert ap3 == ap1
        assert ap1 == [[10,20],[30,40],[50,60]]
        ap1[0][1] = 21      # modify the deep element
        ap2[1][0] = 31      # modify the deep element
        assert ap1 == [[10,21],[31,40],[50,60]]
        assert ap2 == [[10,21],[31,40],[50,60]]
        assert ap3 == [[10,20],[30,40],[50,60]]
        ap1[2] = [51,61]    # modify the shallow element
        ap1[0][0] = 11      # modify the deep element
        ap2[1] = [32,42]    # modify the shallow element
        assert ap1 == [[11,21],[31,40],[51,61]]
        assert ap2 == [[11,21],[32,42],[50,60]]
        assert ap3 == [[10,20],[30,40],[50,60]]

        tup = (1,2,3)
        sum = 0
        for v in tup:
            sum += v
        assert sum == 6

        l1 = [1,2,3]
        l2 = [4,5,6]
        l3 = [7,8,9]

        t1 = (1,2,3)
        t2 = (4,5,6)
        t3 = (7,8,9)

        s = 0
        for x,y in zip(l1,l2):
            s += x + y
        assert s == 21

        s = 0
        for x,y,z in zip(l1,l2,l3):
            s += x + y + z
        assert s == 45

        s = 0
        for x,y,z in zip(t1,t2,t3):
            s += x + y + z
        assert s == 45

        s = 0
        for x,y,z in zip(t1,t1,t1):
            s += x + y + z
        assert s == 18

        # join tuple int to string
        p1 = (1,2,3)
        p2 = ('1','2','3')
        s = ','.join(p2)
        assert s == '1,2,3'

        flag = False
        try:
            s = ','.join(p1)        # cannot convert int to str
            assert s == '1,2,3'
        except Exception as e:
            flag = True
        assert flag

        s = ','.join([str(i) for i in p1])  # first convert it to string
        assert s == '1,2,3'

        # join list int to string
        l1 = [1,2,3]

        flag = False
        try:
            s = ','.join(l1)        # cannot convert int to str
            assert s == '1,2,3'
        except Exception as e:
            flag = True
        assert flag

        s = ','.join([str(i) for i in l1])  # first convert it to string
        assert s == '1,2,3'

        # join list of list int to string, iterating nested for loop for ints
        l1 = [[1,2],[3,4],[5,6]]
        vsum = 0
        s = [','.join([str(i) for i in l1])]
        assert s == ['[1, 2],[3, 4],[5, 6]']
        s = [';'.join([','.join([str(i) for i in t]) for t in l1])]
        assert s == ['1,2;3,4;5,6']
        s = ';'.join([','.join([str(i) for i in t]) for t in l1])
        assert s == '1,2;3,4;5,6'

        l1 = ['12','34','56']
        s = ','.join(l1)
        assert s == '12,34,56'
        s = ';'.join([','.join(c for c in tmps) for tmps in l1])
        assert s == '1,2;3,4;5,6'

        # if char c in dict/set/list/string
        l1 = [1,2,3]
        l2 = [7,8,9]
        s1 = set([1,2,3])
        s2 = set([7,8,9])
        d1 = {1:1,2:2,3:3}
        d2 = {7:7,8:8,9:9}
        str1 = 'abc'
        str2 = 'xyz'
        assert 3 in l1
        assert 3 not in l2
        assert 3 in s1
        assert 3 not in s2
        assert 3 in d1
        assert 3 not in d2
        assert 'c' in str1
        assert 'c' not in str2

        # add to sets
        s3 = set([1,2,3])
        s3.update([4,5,6])
        assert len(s3) == 6
        diff = s3.difference({1,2,3,4,5,6})
        assert diff != None and len(diff) == 0
        diff = s3.difference({1,2,3,4,5})
        assert diff != None and len(diff) == 1 # diff == {6}
        diff = s3.difference({1,2,3,4,5,6,7})
        assert diff != None and len(diff) == 0
        diff = {1,2,3,4,5,6,7}.difference(s3)
        assert diff != None and len(diff) == 1 # diff == {7}

        # add to sets
        s1 = {1,2,3}
        s2 = {4,5,6}
        s3 = s1 | s2
        s4 = set([1,2,3,4,5,6])
        assert len(s2) == 3
        assert s3 == s4
        s4 |= s3
        assert s3 == s4

        d = {
            'k1':'v1',
            'k2':'v2',
            'k7':'v7',
            'k6':'v2',
            'k4':'v2',
            'k8':'v8',
            'k3':'v3',
            'k5':'v5'
        }
        assert len(d) == 8
        l_keys = list(d.keys())
        l_vals = list(d.values())
        l_keys.sort()
        l_vals.sort()
        assert l_keys == ['k1','k2','k3','k4','k5','k6','k7','k8']
        assert l_vals == ['v1','v2','v2','v2','v3','v5','v7','v8']

        set_keys = set(d.keys())
        set_vals = set(d.values())

        assert set_keys == {'k1','k2','k3','k4','k5','k6','k7','k8'}
        assert set_keys != ('k1','k2','k3','k4','k5','k6','k7','k8')
        assert set_vals == {'v1','v2','v3','v5','v7','v8'}
        assert set_vals != ('v1','v2','v3','v5','v7','v8')

        s = set()
        s.add((1,2))
        s.add((2,3))
        s.add((4,5))
        assert (1,2) in s
        assert (2,1) not in s

        s = '10 20 30 40 50'

        # maps string to type int
        l = list(map(int, s.rstrip().split()))
        assert l == [10,20,30,40,50]

        l = list(s.rstrip().split())
        assert l == ['10','20','30','40','50']

        s = 'aa bb cc dd ee '
        l = list(s.rstrip().split())
        assert l == ['aa','bb','cc','dd','ee']

        d1 = {1:1,2:2,3:3}
        d2 = {1:1,2:2,3:3}
        d3 = {1:1,2:2,3:4}

        # this is one level copy, but use d2 = copy.deepcopy(d1) for complex nested dicts
        # d2 = d1.copy() also works for one level copy of references
        d4 = {k:v for k,v in d1.items()}
        assert d1 == d2 and d1 != d3
        assert d1 == d4
        d5 = d1.copy()
        d6 = copy.deepcopy(d1)
        assert d1 == d5
        assert d1 == d6

        # delete key from map pop key from map
        d1 = {'k1':'v1','k2':'v2','k3':'v3'}
        flag = False
        d1.pop('k1')
        try:
            d1.pop('k1')
        except Exception as e:
            flag = True
        assert flag == True

        flag = False
        del d1['k2']
        try:
            del d1['k2']
        except Exception as e:
            flag = True
        assert flag == True

        assert d1 == {'k3':'v3'}

        d1 = {1:1,2:2,3:3,4:4}
        d2 = {1:1,2:2,3:3,5:5,6:6}

        keys1 = d1.keys()
        keys2 = d2.keys()
        assert not isinstance(keys1,set)
        assert not isinstance(keys2,set)
        assert isinstance(d1,dict)

        skeys1 = set(keys1)
        skeys2 = set(keys2)
        assert isinstance(skeys1,set)
        assert isinstance(skeys2,set)

        # set diff
        keys_symdiff1 = skeys1.symmetric_difference(skeys2)
        assert keys_symdiff1 == {4,5,6}

        keys_diff2 = skeys1 ^ skeys2
        assert keys_diff2 == {4,5,6}

        keys_diff1 = skeys1.difference(skeys2)
        assert keys_diff1 == {4}

        keys_diff2 = skeys2.difference(skeys1)
        assert keys_diff2 == {5,6}

        keys_union1 = set(skeys1)
        keys_union1.union(skeys2)
        assert keys_union1 == {1,2,3,4}

        keys_union2 = skeys1 | skeys2
        assert keys_union2 == {1,2,3,4,5,6}

        d1dump = json.dumps(d1)
        d2dump = json.dumps(d2)
        assert isinstance(d1,dict)
        d1 = json.loads(d1dump)
        d2 = json.loads(d2dump)
        assert isinstance(d1,dict)

        skeys1 = set(d1.keys())
        skeys2 = set(d2.keys())
        assert isinstance(skeys1,set)
        assert isinstance(skeys2,set)

        # set diff
        keys_symdiff1 = skeys1.symmetric_difference(skeys2)
        assert keys_symdiff1 == {'4','5','6'}

        keys_diff2 = skeys1 ^ skeys2
        assert keys_diff2 == {'4','5','6'}

        keys_diff1 = skeys1.difference(skeys2)
        assert keys_diff1 == {'4'}

        keys_diff2 = skeys2.difference(skeys1)
        assert keys_diff2 == {'5','6'}

        keys_union1 = set(skeys1)
        keys_union1.union(skeys2)
        assert keys_union1 == {'1','2','3','4'}

        keys_union2 = skeys1 | skeys2
        assert keys_union2 == {'1','2','3','4','5','6'}

        d = {}
        keys = set(d.keys())
        assert len(keys) == 0
        return

    def test_difflib(self):
        str = 'this is line 1\n' + \
            'this is line 2\n' + \
            'this is line 3\n' + \
            'this is line 4\n' + \
            'this is line 5\n'
        slist = str.split('\n')
        json1 = {
            'k1':[1,2,3],
            'k2':[10,20,30],
            'k3':   'this is line 1\n' + \
                    'this is line 2\n' + \
                    'this is line 3\n' + \
                    'this is line 4\n' + \
                    'this is line 5\n',
            'k4':10,
            'k5':20,
            'k6':{
                'k6a':[1,2,3],
                'k6b':[10,20,30],
                'k6c':20,
                'k6d':30
            },
            'k8':'this is line 1\n' + \
                 'this is line 2\n' + \
                 'this is line 3\n' + \
                 'this is line 4\n' +
                 'this is line 5\n',
            'k9':['1','2','3'],
            'k10':['10','20','30']
        }

        json2 = {
            'k1':[1,2,3],
            'k2':[11,20,30,40],
            'k3':   'this is line 1\n' + \
                    'this is line 2\n' + \
                    'this is line 3\n' + \
                    'this is line 4\n' +
                    'this is line 5\n',
            'k4':10,
            'k5':21,
            'k6':{
                'k6a':[1,2,3],
                'k6b':[10,20,35,40],
                'k6c':20,
                'k6d':40
            },
            'k7':[2,3,4],
            'k8':'this is line 1\n' + \
                 'this is line 2\n' + \
                 'this is a thing 3\n' + \
                 'this is line 5\n' + \
                 'this is line 6\n' + \
                 'this is line 7\n',
            'k9':['1','2','3'],
            'k10':['10','20','25','34']
        }
        diff_sm = difflib.SequenceMatcher()
        diff_text  = difflib.Differ()

        result = list(diff_text.compare(json1['k3'].split('\n'),json2['k3'].split('\n')))
        for line in result:
            print(line)
        #print(result)
        #pprint.pprint(result)
        #sys.stdout.writelines(result)
        print('\n')

        result = list(diff_text.compare(json1['k8'].split('\n'),json2['k8'].split('\n')))
        for line in result:
            print(line)
        #print(result)
        #pprint.pprint(result)
        #sys.stdout.writelines(result)
        print('\n')

        #result = difflib.context_diff(json1['k1'],json2['k1'])
        #for line in result:
        #    print(line)
        #pprint.pprint(result)
        #sys.stdout.writelines(result)
        #print(result)
        print('\n')

        result = list(difflib.unified_diff(json1['k8'].split('\n'),json2['k8'].split('\n')))
        for line in result:
                print(line)
        print('\n')

        result = list(difflib.unified_diff(json1['k10'],json2['k10']))
        for line in result:
            print(line)
        print('\n')

        return

    def test_struct_pack_unpack(self):
        '''
        c = 1B
        b = signed 1B
        B = unsigned 1B
        h = 2B signed
        H = 2B unsigned
        i = 4B
        I = 4B unsigned
        l = 4B
        L = 4B unsigned
        q = 8B long long
        Q = 8B unsigned long long
        f = float 4B
        d = double 8B
        s = char []
        p = char []


        = native
        < little endian
        > big endian

        pack(format,v1,v2,...)
        pack_into(format,buf,offset,v1,v2,...)
        unpack(format,buf)
        unpack_from(format,buf,offset=0)
        calcsize(format)

        '''

        a1 = [
            [
                0x12,
                0x23,
                0x34
            ],
            [
                0x12_34,
                0x23_45,
                0x34_56
            ],
            [
                0x12_34_56_78,
                0x23_45_67_89,
                0x34_56_78_90
            ]
        ]

        v1 = struct.pack('BBB',a1[0][0],a1[0][1],a1[0][2])
        v2 = struct.pack('hhh',a1[0][0],a1[0][1],a1[0][2])
        v3 = struct.pack('hhh',a1[1][0],a1[1][1],a1[1][2])
        v4 = struct.pack('iii',a1[2][0],a1[2][1],a1[2][2])
        s  = 'the cat in the hat'
        v5 = s.encode('utf-8')

        (uv01,uv02,uv03) = struct.unpack('BBB',v1)
        (uv11,uv12,uv13) = struct.unpack('hhh',v2)
        (uv21,uv22,uv23) = struct.unpack('hhh',v3)
        (uv31,uv32,uv33) = struct.unpack('iii',v4)
        s1 = v5.decode('utf-8')
        assert (uv01,uv02,uv03) == (0x12,0x23,0x34)
        assert (uv21,uv22,uv23) == (0x1234,0x2345,0x3456)
        assert (uv31,uv32,uv33) == (0x12345678,0x23456789,0x34567890)
        assert s1 == 'the cat in the hat'

        return

    def test_built_in_functions(self):
        assert max(4,10,8,3) == 10  # max(a1,a2,*args[,key])
        assert min(4,10,8,3) == 3
        assert abs(-10) == 10
        assert abs(10) == 10

        # bit manipulation, shift
        i = 0x8a
        assert i == 138
        assert i == 0b10001010
        assert (i >> 3) & 1 == 1
        assert (i >> 2) & 1 == 0
        assert (i >> 4) & 0xf == 8

        d1 = dict(k1=10,k2=20,k3=30,k4=40)
        d2 = {'k1':10,'k2':20,'k3':30,'k4':40}
        d3 = dict(k1=11,k2=22,k3=33,k4=44)
        assert d1['k1'] == 10
        assert d2['k1'] == 10
        assert d1 == d2
        assert d1 != d3

        assert int(1.23) == 1
        assert int(1.51) == 1
        assert round(1.51) == 2
        assert round(1.5) == 2
        assert float(1.23) == 1.23
        assert float(2) == 2.0

        assert sum([1,2,3]) == 6

        assert set([1,2,2,3,3,4]) == set([1,2,3,4])

        assert len('abc') == 3
        assert len([1,2,3]) == 3
        assert len(['one','two','three']) == 3

        l = ['v1','v2','v3','v4']
        assert list(enumerate(l)) == [(0,'v1'),(1,'v2'),(2,'v3'),(3,'v4')]
        assert list(enumerate(l,start=10)) == [(10,'v1'),(11,'v2'),(12,'v3'),(13,'v4')]

        assert pow(2,3) == 8

        s = set([1,2,3])
        assert 1 in s
        assert 5 not in s

        d = dict(k1=1,k2=2,k3=3)
        assert 'k1' in d
        assert 'k10' not in d

        assert 'gg' in 'eggs'
        assert 'bb' not in 'eggs'

        #p('pass test_built_in_functions')

    def test_bisect(self):
        l = [i*5 for i in range(10)]
        #            0    2     4     6     8
        assert l == [0,5,10,15,20,25,30,35,40,45]
        i = bisect.bisect_left(l,25)
        assert i != None and i == 5
        i = bisect.bisect(l,25)
        assert i != None and i == 6
        i = bisect.bisect(l,23)
        assert i != None and i == 5
        i = bisect.bisect(l,-100)
        assert i == 0
        i = bisect.bisect(l,100)
        assert i == 10 and i == len(l) and l[i-1] == 45
        i = bisect.bisect_left(l,100)
        assert i == 10 and i == len(l)

        i = bisect.bisect_left(l,39)
        assert i == 8 and l[i] == 40
        i = bisect.bisect(l,39)
        assert i == 8 and l[i] == 40
        i = bisect.bisect_right(l,39)   # bisect_left vs bisect_right are same if not exact match, choose next largest
        assert i == 8 and l[i] == 40

        i = bisect.bisect_left(l,40)    # bisect_left vs bisect differ in exact match
        assert i == 8 and l[i] == 40    # bisect_left i is exact
        i = bisect.bisect(l,40)         # bisect_right is next largest
        assert i == 9 and l[i] == 45    # bisect_right and bisect behave the same
        i = bisect.bisect_right(l,40)
        assert i == 9 and l[i] == 45

        i = bisect.bisect_left(l,41)
        assert i == 9 and l[i] == 45
        i = bisect.bisect(l,41)
        assert i == 9 and l[i] == 45
        i = bisect.bisect_right(l,41)   # bisect_left vs bisect_right are same if not exact match, choose next largest
        assert i == 9 and l[i] == 45


        i = bisect.bisect_left(l,43)
        assert i == 9
        i = bisect.bisect_left(l,45)
        assert i == 9
        i = bisect.bisect(l,45)
        assert i == 10

    def test_math_functions(self):
        vact = math.factorial(5)
        vexp = 5 * 4 * 3 * 2 * 1
        assert vact == vexp

        l = []
        for i in range(2,4):
            l.append(i)
        assert l == [2,3]

        assert (10//3) == 3         # floored 10/3 = 3
        assert int(10/3) == 3
        assert int(11/3) == 3
        assert int(10/2) == 5
        assert int(11/2) == 5
        assert (10//2) == 5
        assert (11//2) == 5
        assert (12//2) == 6
        assert (10//2) == int(10/2)
        assert (11//2) == int(11/2)
        assert (10/3) != 3.33
        assert round(10/3,2) == 3.33

        v = 10/3
        assert '{:.2f}'.format(v) == '3.33'
        assert float('{:.2f}'.format(v)) == 3.33
        assert round(v,2) == 3.33
        assert round(v,3) == 3.333
        assert round(v,3) != 3.3333
        assert round(10/3,3) == 3.333

        assert math.floor(3.333) == 3
        assert math.ceil(3.333) == 4
        assert math.ceil(3.5) == 4

        assert '{}'.format(1) == '1'
        assert '{:2}'.format(1) == ' 1'
        assert '{:02}'.format(1) == '01'
        assert "{:2}".format(1) == " 1"
        assert "{:02}".format(1) == "01"

        assert abs(-10) == 10
        assert abs(10) == 10

        assert (2**0) == 1
        assert (2**1) == 2
        assert (2**3) == 8
        assert (2**4) == 16

        #p('pass test_math_functions')

    def test_control_statements(self):

        # if else single line and effects of parentheses

        v = 1
        s = 'a ' + ('b ' if v == 1 else 'c ') + 'd'
        assert s == 'a b d'

        v = 1
        s = 'a ' + 'b ' if v == 1 else 'c ' + 'd'
        assert s == 'a b '

        v = 2
        s = 'a ' + ('b ' if v == 1 else 'c ') + 'd'
        assert s == 'a c d'

        v = 2
        s = 'a ' + 'b ' if v == 1 else 'c ' + 'd'
        assert s == 'c d'

        l = []
        for i in range(5,0,-1): # [5,0)
            l.append(i)
        assert l == [5,4,3,2,1]

        i = 0
        l.clear()
        for _ in range(5):      # underscore variable
            l.append(i)
            i += 1
        assert l == [0,1,2,3,4]

        l.clear()
        assert l == []
        assert len(l) == 0

        for i in range(0,5,1):
            l.append(i)
        assert l == [0,1,2,3,4]
        l.clear()

        for i in range(0,5):
            l.append(i)
        assert l == [0,1,2,3,4]
        l.clear()

        for i in range(5):
            l.append(i)
        assert l == [0,1,2,3,4]
        l.clear()

        for i in range(0,5,2):
            l.append(i)
        assert l == [0,2,4]

        l.clear()
        for i in range(10,15,1):        # start at 10 til 15
            l.append(i)
        assert l == [10,11,12,13,14]

        v = 10
        flag = False
        if v < 0:
            flag = False
        elif v < 10:
            flag = False
        elif v < 20:
            flag = True
        else:
            flag = False
        assert flag

        s = 'abcdefg'
        sz = len(s)
        li = []
        lc = []
        for i in range(sz-1,0,-1):
            li.append(i)
            lc.append(s[i])
        assert li == [6,5,4,3,2,1]
        assert lc == ['g','f','e','d','c','b']

        li = []
        lc = []
        for i in range(sz-1,-1,-1):     # count down to 0
            li.append(i)
            lc.append(s[i])
        assert li == [6,5,4,3,2,1,0]
        assert lc == ['g','f','e','d','c','b','a']

        li = []
        lc = []
        for i in range(sz):     # count up to sz-1
            li.append(i)
            lc.append(s[i])
        assert li == [0,1,2,3,4,5,6]
        assert lc == ['a','b','c','d','e','f','g']


        #p('pass test_control_loops')

    def test_lambda(self):
        s3 = lambda x,y,z: x+y+z
        assert 12 == s3(3,4,5)

        l1 = [1,2,3,4,5]
        l2 = list(map(lambda x: x*2, l1))
        assert l2 == [2,4,6,8,10]

        f = lambda x: x*2
        l2 = [f(x) for x in l1]
        assert l2 == [2,4,6,8,10]

        l2 = [(lambda x: x*2) for x in l1]      # i dont know what this means but not expected answer
        assert l2 != [2,4,6,8,10]

        def f(x): return x*2
        l2 = [f(x) for x in l1]
        assert l2 == [2,4,6,8,10]

        l1 = [1,2,3,4,5]
        l2 = [2,3,4,5,6]
        l3 = list(map(lambda x,y: x+y, l1,l2))
        assert l3 == [3,5,7,9,11]

        l3 = []
        for x,y in zip(l1,l2):      # it's not x,y in l1,l2
            l3.append(x+y)
        assert l3 == [3,5,7,9,11]

        def f(x,y): return x+y
        l3 = [f(x,y) for x,y in zip(l1,l2)]
        assert l3 == [3,5,7,9,11]

        l1 = [1,2,3,4,5]
        l2 = [2,3,4]
        l3 = []
        for x,y in zip(l1,l2):      # stops at shortest list
            l3.append(x+y)
        assert l3 == [3,5,7]

        sum = functools.reduce((lambda x,y: x+y), l1)
        assert sum == (1+2+3+4+5)

        f1 = lambda x,y: [x,y,x+y]          # return multiple values
        assert f1(1,2) == [1,2,3]

        l2 = list(filter(lambda x: x%2 == 0, l1))
        assert l2 == [2,4]

        l2 = list(filter(lambda x: x%2 == 1, l1))
        assert l2 == [1,3,5]

        l1 = [{"k":"k1","v":80},{"k":"k4","v":30},{"k":"k5","v":90},{"k":"k3","v":20},{"k":"k2","v":40}]
        assert l1[4]["k"] == 'k2'
        l2 = sorted(l1,key = lambda x: x['v'])  # sort by v
        l3 = list(map(lambda x: x["v"], l2))
        assert l3 == [20,30,40,80,90]

        l2 = sorted(l1,key = lambda x: x['k'])  # sort by k
        l3 = list(map(lambda x: x["v"], l2))
        assert l3 == [80,40,20,30,90]

        #p('pass test_lambda')

    def test_functions(self):
        class CBType(enum.Enum):
            INT = 1
            STR = 2
        def callback_add(v1:int,v2:int)->int:
            return v1+v2
        def callback_mult(v1:int,v2:int)->int:
            return v1*v2
        def callback_concat(v1:str,v2:str)->str:
            return v1 + v2
        def passthrough(v1,v2,cb,cb_type:CBType):
            #assert isinstance(cb,function)
            if cb_type == CBType.INT:
                return cb(v1,v2)
            if cb_type == CBType.STR:
                return cb(v1,v2)
            return None
        def t0():
            v = passthrough(2,3,callback_add,CBType.INT)
            assert v == 5
            v = passthrough(2,3,callback_mult,CBType.INT)
            assert v == 6
            v = passthrough('the ','cat ',callback_concat,CBType.STR)
            assert v == 'the cat '
        t0()
    def test_sort(self):
        class my_o1:
            def __init__(self, a, b, c):
                self.a = a
                self.b = b
                self.c = c
            def __lt__(self, other):
                return self.c < other.c
            def __eq__(self, other):
                return self.c == other.c
            def __gt__(self, other):
                return self.c > other.c
        class my_o2:
            def __init__(self, a, b, c):
                self.a = a
                self.b = b
                self.c = c

        o1_1 = my_o1(5,5,30)
        o1_2 = my_o1(2,2,40)
        o1_3 = my_o1(1,1,20)
        o1_4 = my_o1(4,4,50)
        o1_5 = my_o1(3,3,10)
        o1_6 = my_o1(6,6,40)
        o1_7 = my_o1(2,2,30)

        o2_1 = my_o2(5,5,30)
        o2_2 = my_o2(2,2,40)
        o2_3 = my_o2(1,1,20)
        o2_4 = my_o2(4,4,50)
        o2_5 = my_o2(3,3,10)
        o2_6 = my_o2(6,6,40)
        o2_7 = my_o2(2,2,30)
        o2_8 = my_o2(2,2,40)

        l = [o1_1,o1_2,o1_3,o1_4,o1_5]
        lsorted = sorted(l)
        lexp = [3,1,5,2,4]

        lact = list(map(lambda x: x.a, lsorted))
        assert lact == lexp

        lact = []
        for o in lsorted:       # same thing as above
            lact.append(o.a)
        assert lact == lexp


        l = [o2_1,o2_2,o2_3,o2_4,o2_5]
        lsorted = l.copy()
        lsorted.sort(key=lambda x: x.a)
        lexp = [1,2,3,4,5]
        lact = list(map(lambda x: x.a, lsorted))
        assert lact == lexp

        lsorted = l.copy()
        lsorted.sort(key=lambda x: x.c)
        lexp = [3,1,5,2,4]
        lact = list(map(lambda x: x.a, lsorted))
        assert lact == lexp

        assert o1_1 < o1_2
        assert o1_1 > o1_3
        assert o1_2 == o1_6 and o1_2.c == 40 and o1_6.c == 40

        # this is by reference and __eq__ not overridden so it's address comparison
        assert o2_2 != o2_8 and o2_2.a == o2_8.a and o2_2.b == o2_8.b and o2_2.c == o2_8.c

        # sort string
        s =       '78291372'
        sortedv = '12237789'
        res = ''.join(sorted(s))
        assert res == sortedv

        l = sorted([5,4,5,2,1])
        assert l == [1,2,4,5,5]

        d = {'k0':'v90','k1':'v81','k2':'v72','k3':'v63','k3.1':'v63','k4':'v54'}
        l = sorted(d.keys())
        assert l == ['k0','k1','k2','k3','k3.1','k4']
        l = sorted(d.items())
        assert l == [('k0','v90'),('k1','v81'),('k2','v72'),('k3','v63'),('k3.1','v63'),('k4','v54')]
        l = sorted(d.items(), key=lambda kv:(kv[0],kv[1]))
        assert l == [('k0','v90'),('k1','v81'),('k2','v72'),('k3','v63'),('k3.1','v63'),('k4','v54')]
        l = sorted(d.items(), key=lambda kv:(kv[1],kv[0]))
        assert l == [('k4','v54'),('k3','v63'),('k3.1','v63'),('k2','v72'),('k1','v81'),('k0','v90')]
        l = sorted(d.items(), key=lambda kv:kv[1])
        assert l == [('k4','v54'),('k3','v63'),('k3.1','v63'),('k2','v72'),('k1','v81'),('k0','v90')]
        l = sorted(d, key=d.get)
        assert l == ['k4','k3','k3.1','k2','k1','k0']
        l = sorted(d, key=d.get, reverse=True)
        assert l == ['k0','k1','k2','k3','k3.1','k4']
        l = [(v,k) for k,v in sorted(d.items(), key=lambda x:x[1])] # sort by val
        assert l == [('v54','k4'),('v63','k3'),('v63','k3.1'),('v72','k2'),('v81','k1'),('v90','k0')]
        dictv = {v:k for k,v in sorted(d.items(), key=lambda x:x[1])} # sort by val
        l = sorted(dictv)
        assert l == ['v54','v63','v72','v81','v90'] # duplicate  key was overwritten
        l = sorted(list(dictv.keys()))
        assert l == ['v54','v63','v72','v81','v90']
        l = sorted(dictv.items())
        assert l == [('v54','k4'),('v63','k3.1'),('v72','k2'),('v81','k1'),('v90','k0')] # v63,k3 overwritten
        l = sorted(dictv.values())
        assert l == ['k0','k1','k2','k3.1','k4']    # k3 was overwritten because duplicate key

        # minheap with ints
        # maxheap with ints
        hqmin = []
        hqmax = []

        ctr = 0
        while hqmin:
            heapq.heappop(hqmin)
            heapq.heappop(hqmax)
            ctr += 1
        assert ctr == 0


        # heapq for char has to be converted to int for maxheap

        i = ord('a')
        c = chr(i)
        assert c == 'a'

        c = chr(97)
        i = ord(c)
        assert i == 97

        #          0 2 4 6 8
        lo = list('abcdefghij')
        la = lo.copy()
        random.shuffle(la)
        assert la != lo
        hqmin = []
        hqmax = []
        for c in la:
            i = ord(c)
            heapq.heappush(hqmin,i)
            heapq.heappush(hqmax,-1*i)

        assert chr(hqmin[0]) == 'a'
        assert chr(-1*hqmax[0]) == 'j'

        res = []
        while hqmin:
            i = heapq.heappop(hqmin)
            c = chr(i)
            res.append(c)
        assert res == lo

        res = []
        while hqmax:
            i = heapq.heappop(hqmax)
            c = chr(-1*i)
            res.append(c)
        assert res == list(reversed(lo))

        # heapq for max words has to be special class that implements __lt__(self,o): return self.v > o.v

        class TMPW:
            def __init__(self,w):
                self.w = w
            def __lt__(self,o):
                return self.w > o.w

        lo = ['ab','bb','cb','db','db','eb','fb','gb']
        la = lo.copy()
        random.shuffle(la)
        assert la != lo

        hqmin = []
        hqmax = []

        for w in la:
            t = TMPW(w)
            heapq.heappush(hqmin,w)
            heapq.heappush(hqmax,t)

        assert hqmin[0] == 'ab'
        assert hqmax[0].w == 'gb'

        res = []
        while hqmin:
            w = heapq.heappop(hqmin)
            res.append(w)
        assert res == lo

        res = []
        while hqmax:
            t = heapq.heappop(hqmax)
            res.append(t.w)
        assert res == list(reversed(lo))

        # regular ints sorting with heapq
        hqmin = []
        hqmax = []

        li = [11,15,22,2,8,5,1,3,7]
        lc = li.copy()

        ls = sorted(lc)
        assert ls == [1,2,3,5,7,8,11,15,22]
        ls = list(reversed(sorted(lc)))
        assert ls == [22,15,11,8,7,5,3,2,1]

        ctr = 0
        for i in li:
            heapq.heappush(hqmin,i)         # default is minheap
            heapq.heappush(hqmax,i*-1)      # have to do -1 for maxheap or define class for _lt_
            ctr += 1
        assert ctr == len(li)
        lmin = []
        lmax = []
        while hqmin:
            lmin.append(heapq.heappop(hqmin))
        while hqmax:
            lmax.append(heapq.heappop(hqmax) * -1) # have to do -1 for maxheap
        assert lmin == [1,2,3,5,7,8,11,15,22]
        assert lmax == [22,15,11,8,7,5,3,2,1]
        lrev = list(reversed(lmax))
        assert lmin == list(reversed(lmax))

        # minheap with ints using priority queue
        # maxheap with ints using priority queue
        hqmin = queue.PriorityQueue()
        hqmax = queue.PriorityQueue()
        ctr = 0
        li = [11,15,22,2,8,5,1,3,7]
        for i in li:
            hqmin.put(i)
            hqmax.put(i*-1)
        lmin = []
        lmax = []
        while not hqmin.empty():
            lmin.append(hqmin.get())
        while not hqmax.empty():
            lmax.append(hqmax.get()*-1)
        assert lmin == [1,2,3,5,7,8,11,15,22]
        assert lmax == [22,15,11,8,7,5,3,2,1]

        # minheap tuple with ints using priority queue
        # maxheap tuple with ints using priority queue
        hqmin = queue.PriorityQueue()       # default is minheap
        hqmax = queue.PriorityQueue()
        ctr = 0
        li = [11,15,22,2,8,5,1,3,7]
        lj = [ 9, 8, 7,6,5,4,3,2,1]
        for i,j in zip(li,lj):
            hqmin.put((i,j))
            hqmax.put((i*-1,j))
        lmin = []
        lmax = []
        while not hqmin.empty():
            lmin.append(hqmin.get())
        while not hqmax.empty():
            t = hqmax.get()
            lmax.append((t[0]*-1,t[1]))
        assert lmin == [(1,3),(2,6),(3,2),(5,4),(7,1),(8,5),(11,9),(15,8),(22,7)]
        assert lmax == list(reversed(lmin))

        # minheap tuple with class override of comparator for string
        class TMIN:
            def __init__(self,k,v):
                self.k = k
                self.v = v
            def __lt__(self,other):
                return self.k < other.k
        l = [TMIN('k12','vx'),TMIN('k23','v11'),TMIN('k1','vy'),TMIN('k2','v2'),TMIN('k21','v32')]
        hqmin = queue.PriorityQueue()
        for o in l:
            hqmin.put(o)
        lmin = []
        while not hqmin.empty():
            o = hqmin.get()
            lmin.append(o.k)
        assert lmin == ['k1','k12','k2','k21','k23']

        hqmin = []
        for o in l:
            heapq.heappush(hqmin,o)
        lmin = []
        while len(hqmin) != 0:
            o = heapq.heappop(hqmin)
            lmin.append(o.k)
        assert lmin == ['k1','k12','k2','k21','k23']


        # max priority queue, just create class where __lt__ self.k > other.k
        class TMAX:
            def __init__(self,k,v):
                self.k = k
                self.v = v
            def __lt__(self,other):
                return self.k > other.k
        l = [TMAX('k12','vx'),TMAX('k23','v11'),TMAX('k1','vy'),TMAX('k2','v2'),TMAX('k21','v32')]

        hqmax = queue.PriorityQueue()
        for o in l:
            hqmax.put(o)
        lmax = []
        while not hqmax.empty():
            o = hqmax.get()
            lmax.append(o.k)
        assert lmax == ['k23','k21','k2','k12','k1']

        hqmax = []
        for o in l:
            heapq.heappush(hqmax,o)
        lmax = []
        while len(hqmax) != 0:
            o = heapq.heappop(hqmax)
            lmax.append(o.k)
        assert lmax == ['k23','k21','k2','k12','k1']

        # heapq
        li = ['k4','k0','k11','k3','k1','k2']
        heapq.heapify(li)
        assert li != ['k0','k1','k11','k2','k3','k4'] # not sorted!
        l = li.copy()

        lo = []
        while len(l) != 0:
            lo.append(heapq.heappop(l))
        assert lo == ['k0','k1','k11','k2','k3','k4'] # sorted!

        # sort dict in heapq
        hq = []
        for k,v in d.items():
            heapq.heappush(hq,(k,v))
        l = list(x for x in hq)
        assert l == [('k0','v90'),('k1','v81'),('k2','v72'),('k3','v63'),('k3.1','v63'),('k4','v54')]

        # sort tuple in heapq with custom key, or the obj should implement __lt__ __cmp__ __gt__ methods
        li = [('k4','y0','z1'),('k3','y1','z4'),('k2','y2','z0'),('k1','y3','z3'),('k0','y4','z2')]

        # this doesnt put tuples in order
        hq = []
        for t in li:
            heapq.heappush(hq,(t[0],t))
        l = list(x for x in hq) # this is not in order
        assert l == [('k0',('k0','y4','z2')),('k1',('k1','y3','z3')),('k3',('k3','y1','z4')),('k4',('k4','y0','z1')),('k2',('k2','y2','z0'))]
        l = []
        # this is in order! you have to pop it off q
        while len(hq) != 0:
            l.append(heapq.heappop(hq))
        assert l == [('k0',('k0','y4','z2')),('k1',('k1','y3','z3')),('k2',('k2','y2','z0')),('k3',('k3','y1','z4')),('k4',('k4','y0','z1'))]
        l = list(x[1] for x in l)
        assert l == [('k0','y4','z2'),('k1','y3','z3'),('k2','y2','z0'),('k3','y1','z4'),('k4','y0','z1')]

        # sort tuple by lambda key
        lunsorted = [('k4','y0','z1'),('k0','y4','z2'),('k2','y2','z0'),('k3','y1','z4'),('k1','y3','z3')]
        lsorted = sorted(lunsorted, key=lambda x:x[0])
        assert lsorted == [('k0','y4','z2'),('k1','y3','z3'),('k2','y2','z0'),('k3','y1','z4'),('k4','y0','z1')]

        # sort numeric keys ALPHABETICAL ORDER
        lunsorted = [(3,3,3),(5,4,2),(12,1,20),(4,5,1),(2,1,5),(1,2,4)]
        lsorted = sorted(lunsorted, key=lambda x:str(x[0]))
        assert lsorted == [(1,2,4),(12,1,20),(2,1,5),(3,3,3),(4,5,1),(5,4,2)]
        lsorted = sorted(lunsorted, key=lambda x:str(x[1]))
        assert lsorted == [(12,1,20),(2,1,5),(1,2,4),(3,3,3),(5,4,2),(4,5,1)]
        lsorted = sorted(lunsorted, key=lambda x:str(x[2]))
        assert lsorted == [(4,5,1),(5,4,2),(12,1,20),(3,3,3),(1,2,4),(2,1,5)]

        # sort numeric keys NATURAL ORDER
        lunsorted = [(3,3,3),(5,4,2),(12,1,20),(4,5,1),(2,1,5),(1,2,4)]
        lsorted = sorted(lunsorted, key=lambda x:int(x[0]))
        assert lsorted == [(1,2,4),(2,1,5),(3,3,3),(4,5,1),(5,4,2),(12,1,20)]
        lsorted = sorted(lunsorted, key=lambda x:int(x[1]))
        assert lsorted == [(12,1,20),(2,1,5),(1,2,4),(3,3,3),(5,4,2),(4,5,1)]
        lsorted = sorted(lunsorted, key=lambda x:int(x[2]))
        assert lsorted == [(4,5,1),(5,4,2),(3,3,3),(1,2,4),(2,1,5),(12,1,20)]

        # sort numeric keys ALPHABETICAL ORDER but why does it execute as NATURAL ORDER??
        lunsorted = [(3,3,3),(5,4,2),(12,1,20),(4,5,1),(2,1,5),(1,2,4)]
        lsorted = sorted(lunsorted, key=lambda x:x[0])
        assert lsorted == [(1,2,4),(2,1,5),(3,3,3),(4,5,1),(5,4,2),(12,1,20)]
        lsorted = sorted(lunsorted, key=lambda x:x[1])
        assert lsorted == [(12,1,20),(2,1,5),(1,2,4),(3,3,3),(5,4,2),(4,5,1)]
        lsorted = sorted(lunsorted, key=lambda x:x[2])
        assert lsorted == [(4,5,1),(5,4,2),(3,3,3),(1,2,4),(2,1,5),(12,1,20)]


        hq = []
        for t in li:
            heapq.heappush(hq,(t[1],t))
        l = list(x for x in hq) # this is not in order
        assert l == [('y0',('k4','y0','z1')),('y1',('k3','y1','z4')),('y2',('k2','y2','z0')),('y3',('k1','y3','z3')),('y4',('k0','y4','z2'))]

        # this doesnt put tuples in order
        li = [('k4','y0','z1'),('k3','y1','z4'),('k2','y2','z0'),('k1','y3','z3'),('k0','y4','z2')]
        l = li.copy()
        heapq.heapify(l)
        assert l != [('k0','y4','z2'),('k1','y3','z3'),('k2','y2','z0'),('k3','y1','z4'),('k4','y0','z1')]        # this is not in order!
        lo = []
        while len(l) != 0:
            lo.append(heapq.heappop(l))
        assert lo == [('k0','y4','z2'),('k1','y3','z3'),('k2','y2','z0'),('k3','y1','z4'),('k4','y0','z1')] # sorted!

        li = [('k4',('k4','y0','z1')),('k1',('k1','y3','z3')),('k0',('k0','y4','z2')),('k2',('k2','y2','z0')),('k3',('k3','y1','z4'))]
        l = li.copy()
        heapq.heapify(l)
        assert l != [('k0',('k0','y4','z2')),('k1',('k1','y3','z3')),('k3',('k3','y1','z4')),('k4',('k4','y0','z1')),('k2',('k2','y2','z0'))] # this is not in order!
        lo = []
        while len(l) != 0:
            lo.append(heapq.heappop(l))
        assert lo == [('k0',('k0','y4','z2')),('k1',('k1','y3','z3')),('k2',('k2','y2','z0')),('k3',('k3','y1','z4')),('k4',('k4','y0','z1'))] # sorted!

        # this doesnt put tuples in order
        hq = []
        for t in li:
            heapq.heappush(hq,t)
        l = list(x for x in hq)
        assert l != [('k0','y4','z2'),('k1','y3','z3'),('k2','y2','z0'),('k3','y1','z4'),('k4','y0','z1')]

        bn0 = bnode(6,18)
        bn1 = bnode(10,20)
        bn2 = bnode(1,11)
        bn3 = bnode(13,2)
        bn4 = bnode(7,12)
        bn5 = bnode(5,7)

        ln = [bn0,bn1,bn2,bn3,bn4,bn5]
        lnid = [n.id() for n in ln]
        lnk = [(n.id(),n.k()) for n in ln]
        assert bn0.k() == 6

        # heapq of bnode by key by natural int order
        #hq = ln.copy()
        #heapq.heapify(hq)
        #lo = list(x for x in hq)
        #lok = [(n[1].id(),n[1].k()) for n in lo]

        # this works
        hq = []
        for n in ln:
            heapq.heappush(hq,(int(n.k()),n))
        lo = []
        while len(hq) != 0:
            t = heapq.heappop(hq)
            n = t[1]
            lo.append(n)
        lnk = [n.k() for n in lo]
        assert len(lo) == 6
        assert lo == [bn2,bn5,bn0,bn4,bn1,bn3]
        assert lnk == [1,5,6,7,10,13]

        # this does not output in sorted order!
        hq = []
        for n in ln:
            heapq.heappush(hq,(int(n.k()),n))
        lo = list(x[1] for x in hq)
        lnk = [n.k() for n in lo]
        assert len(lo) == 6
        assert lnk != [1,5,6,7,10,13]

        # this works heapq min in sorted order
        hq = []
        for n in ln:
            heapq.heappush(hq,(int(n.k()),n))
        sz_hq = len(hq)
        lo = [heapq.heappop(hq)[1] for i in range(sz_hq)]
        lnk = [n.k() for n in lo]
        assert lnk == [1,5,6,7,10,13]

        # heapq of bnode by key by string order
        hq = []
        for n in ln:
            heapq.heappush(hq,(str(n.k()),n))
        sz_hq = len(hq)
        lo = [heapq.heappop(hq)[1] for i in range(sz_hq)]
        lnk = [n.k() for n in lo]
        assert lnk == [1,10,13,5,6,7]

        # this works
        lo = sorted(ln, key=lambda x:int(x.k()))
        lnk = [n.k() for n in lo]
        assert lo == [bn2,bn5,bn0,bn4,bn1,bn3]
        assert ln == [bn0,bn1,bn2,bn3,bn4,bn5]
        assert lnk == [1,5,6,7,10,13]

        # heapq of bnode by key by string order
        lo = sorted(ln, key=lambda x:str(x.k()))
        lnk = [n.k() for n in lo]
        assert lo == [bn2,bn1,bn3,bn5,bn0,bn4]
        assert ln == [bn0,bn1,bn2,bn3,bn4,bn5]
        assert lnk == [1,10,13,5,6,7]

        so = 'hgfedcba'
        ss = sorted(so)
        rs = reversed(ss)
        ls = [c for c in 'abcdefgh']
        assert ss == ls
        joinss = ''.join(ss)
        assert joinss == 'abcdefgh'
        joinrs = ''.join(rs)
        assert joinrs == 'hgfedcba'
        pass


    def is_approximate(self, act_int_val,exp_int_val,delta) -> bool:
        diff = int(math.fabs(act_int_val - exp_int_val))
        return diff <= delta

    def test_time(self) -> None:
        time_s = "12-31-2019 23:59:00"
        lcl_delta_dec = 8 * 60 * 60  # dec 8 hours between UTC and PST. what about daylight savings?? 28800
        time_utc_12_31_2019_23_59_00 = 1577836740                                       # 12-31-19 23:59:00
        time_utc_12_31_2019_15_59_00 = time_utc_12_31_2019_23_59_00 - lcl_delta_dec     # 12-31-19 15:59:00
        time_utc_01_01_2020_07_59_00 = time_utc_12_31_2019_23_59_00 + lcl_delta_dec     # 01-01-20 07:59:00

        # string to time.struct_time
        time_obj_1 = time.strptime("12-31-2019 23:59:00", "%m-%d-%Y %H:%M:%S")
        assert isinstance(time_obj_1, time.struct_time)
        assert time_obj_1.tm_isdst == -1
        assert time_obj_1.tm_year == 2019 and time_obj_1.tm_mon == 12 and time_obj_1.tm_mday == 31 and time_obj_1.tm_hour == 23

        # time.struct_time to string
        time_s_2 = time.strftime("%m-%d-%Y %H:%M:%S", time_obj_1)
        assert isinstance(time_s_2, str)
        assert time_s_2 == "12-31-2019 23:59:00"

        time_obj_june = time.strptime("06-30-2019 23:59:00", "%m-%d-%Y %H:%M:%S")
        assert isinstance(time_obj_june, time.struct_time)
        assert time_obj_june.tm_isdst == -1 # ????
        assert time_obj_june.tm_year == 2019 and time_obj_june.tm_mon == 6 and time_obj_june.tm_mday == 30 and time_obj_june.tm_hour == 23

        # string to datetime.datetime
        time_obj_2 = datetime.datetime.strptime("12-31-2019 23:59:00", "%m-%d-%Y %H:%M:%S")
        assert isinstance(time_obj_2,datetime.datetime)
        assert time_obj_2.tzinfo is None
        assert time_obj_2.year == 2019 and time_obj_2.month == 12 and time_obj_2.day == 31 and time_obj_2.hour == 23

        # datetime.datetime to string
        assert isinstance(time_obj_2,datetime.datetime)
        time_s_3 = time_obj_2.strftime("%m-%d-%Y %H:%M:%S")     # converted to local time
        assert time_s_3 == "12-31-2019 23:59:00"
        time_utc_int_3 = int(time_obj_2.timestamp())
        assert time_utc_int_3 == 1577865540 and time_utc_int_3 == time_utc_01_01_2020_07_59_00

        time_dt_1 = datetime.datetime(time_obj_1.tm_year,time_obj_1.tm_mon,time_obj_1.tm_mday,time_obj_1.tm_hour,time_obj_1.tm_min,time_obj_1.tm_sec)
        assert isinstance(time_dt_1, datetime.datetime)
        assert time_dt_1.tzinfo is None
        assert time_dt_1.year == 2019 and time_dt_1.month == 12 and time_dt_1.day == 31 and time_dt_1.hour == 23

        time_utc_int = calendar.timegm(time_dt_1.timetuple())           # UTC output
        assert isinstance(time_utc_int,int)
        assert time_utc_int == 1577836740
        time_lcl_int = int(time.mktime(time_dt_1.timetuple()))          # local time output
        assert time_lcl_int == (time_utc_int + lcl_delta_dec)

        datetime_1 = datetime.datetime.fromtimestamp(time_utc_int)      # this gets adjusted to local from 12-31-2019 23:59:00 -> 12-31-2019 15:59:00
        assert isinstance(datetime_1, datetime.datetime)
        assert datetime_1.tzinfo is None
        assert datetime_1.year == 2019 and datetime_1.month == 12 and datetime_1.day == 31 and datetime_1.hour == 15
        time_sec_2_int = int(time.mktime(datetime_1.timetuple()))        # assumes pass in localtime
        time_sec_3_int = int(calendar.timegm(datetime_1.timetuple()))    # assumes pass in UTC

        assert time_sec_2_int == 1577836740 and time_sec_2_int == time_utc_int
        datetime_2 = datetime.datetime.fromtimestamp(time_sec_2_int)
        assert datetime_2.year == 2019 and datetime_2.month == 12 and datetime_2.day == 31 and datetime_2.hour == 15

        assert time_sec_3_int == 1577807940 and time_sec_3_int == (time_sec_2_int - lcl_delta_dec)
        datetime_3 = datetime.datetime.fromtimestamp(time_sec_3_int)
        assert datetime_3.year == 2019 and datetime_3.month == 12 and datetime_3.day == 31 and datetime_3.hour == 7

        time_obj_3 = time.gmtime(time_utc_int)
        assert isinstance(time_obj_3, time.struct_time)
        assert time_obj_3.tm_year == 2019 and time_obj_3.tm_mon == 12 and time_obj_3.tm_mday == 31 and time_obj_3.tm_hour == 23

        time_obj_4 = time.localtime(time_utc_int)
        assert isinstance(time_obj_4, time.struct_time)
        assert time_obj_4.tm_year == 2019 and time_obj_4.tm_mon == 12 and time_obj_4.tm_mday == 31 and time_obj_4.tm_hour == 15

        time_utc_int = calendar.timegm(time_obj_1)
        time_lcl_flt = time.mktime(time_obj_1)
        assert isinstance(time_lcl_flt,float)
        time_lcl_int = int(time_lcl_flt)
        time_lcl_int_exp = time_utc_int + lcl_delta_dec
        assert time_lcl_int == time_lcl_int_exp

        time_s_1 = time.strftime("%m-%d-%Y %H:%M:%S", time_obj_1)
        assert time_s_1 == "12-31-2019 23:59:00"

        time_obj_3 = datetime.datetime.strptime(time_s, "%m-%d-%Y %H:%M:%S").replace(tzinfo=None).astimezone(tz=datetime.timezone.utc).timetuple()
        assert isinstance(time_obj_3, time.struct_time)
        assert time_obj_3.tm_year == 2020 and time_obj_3.tm_mon == 1 and time_obj_3.tm_mday == 1 and time_obj_3.tm_hour == 7

        time_s_2 = time.strftime("%m-%d-%Y %H:%M:%S", time_obj_3)
        assert isinstance(time_s_2, str)
        assert time_s_2 == "01-01-2020 07:59:00"

        time_obj_4 = datetime.datetime.strptime(time_s_2, "%m-%d-%Y %H:%M:%S")
        assert isinstance(time_obj_4,datetime.datetime)
        assert time_obj_4.year == 2020 and time_obj_4.month == 1 and time_obj_4.day == 1 and time_obj_4.hour == 7

        assert isinstance(time_obj_2,datetime.datetime)
        assert time_obj_2.year == 2019 and time_obj_2.month == 12 and time_obj_2.day == 31 and time_obj_2.hour == 23
        time_s_3 = time.strftime("%m-%d-%Y %H:%M:%S", time_obj_2.replace(tzinfo=None).astimezone(tz=datetime.timezone.utc).timetuple())
        assert isinstance(time_s_3, str)
        assert time_s_3 == "01-01-2020 07:59:00"

        assert time_obj_2.year == 2019 and time_obj_2.month == 12 and time_obj_2.day == 31 and time_obj_2.hour == 23
        time_s_4 = time.strftime("%m-%d-%Y %H:%M:%S", time_obj_2.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).timetuple())
        assert isinstance(time_s_4, str)
        assert time_s_4 == "12-31-2019 15:59:00"

        assert isinstance(time_obj_3, time.struct_time)
        assert time_obj_3.tm_year == 2020 and time_obj_3.tm_mon == 1 and time_obj_3.tm_mday == 1 and time_obj_3.tm_hour == 7

        # convert time.struct_time to datetime.datetime
        time_obj_5 = datetime.datetime.fromtimestamp(time.mktime(time_obj_3))
        assert isinstance(time_obj_5, datetime.datetime)
        assert time_obj_5.year == 2020 and time_obj_5.month == 1 and time_obj_5.day == 1 and time_obj_5.hour == 7

        # convert datetime.datetime to time.struct_time
        assert isinstance(time_obj_5, datetime.datetime)
        time_obj_6 = time_obj_5.timetuple()
        assert isinstance(time_obj_6, time.struct_time)

        # replace timezone to UTC, which is +8 hr from 01-01-2020 07:59:00
        time_s_5 = time.strftime("%m-%d-%Y %H:%M:%S", time_obj_5.replace(tzinfo=None).astimezone(tz=datetime.timezone.utc).timetuple())
        assert isinstance(time_s_5, str)
        assert time_s_5 == "01-01-2020 15:59:00"

        # replace timezone from UTC to lcl, which -8 from 01-01-2020 07:59:00
        time_s_6 = time.strftime("%m-%d-%Y %H:%M:%S", time_obj_5.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).timetuple())
        assert isinstance(time_s_6, str)
        assert time_s_6 == "12-31-2019 23:59:00"

        # local timezone difference has no DST (daylight savings) in june!
        time_obj_7 = datetime.datetime.strptime("06-01-2020 23:59:00", "%m-%d-%Y %H:%M:%S").replace(tzinfo=None).astimezone(tz=datetime.timezone.utc).timetuple()
        assert isinstance(time_obj_7, time.struct_time)
        assert time_obj_7.tm_year == 2020 and time_obj_7.tm_mon == 6 and time_obj_7.tm_mday == 2 and time_obj_7.tm_hour == 6

        # local timezone difference uses DST (daylight savings) in jan!
        time_obj_8 = datetime.datetime.strptime("01-01-2020 23:59:00", "%m-%d-%Y %H:%M:%S").replace(tzinfo=None).astimezone(tz=datetime.timezone.utc).timetuple()
        assert isinstance(time_obj_8, time.struct_time)
        assert time_obj_8.tm_year == 2020 and time_obj_8.tm_mon == 1 and time_obj_8.tm_mday == 2 and time_obj_8.tm_hour == 7

        # strftime converstion
        assert isinstance(time_obj_2,datetime.datetime)
        assert time_obj_2.year == 2019 and time_obj_2.month == 12 and time_obj_2.day == 31 and time_obj_2.hour == 23
        assert isinstance(time_obj_1, time.struct_time)
        assert time_obj_1.tm_year == 2019 and time_obj_1.tm_mon == 12 and time_obj_1.tm_mday == 31 and time_obj_1.tm_hour == 23
        time_s_8 = time.strftime("%m-%d-%Y %H:%M:%S", time_obj_1)   # works for time.struct_time, not for datetime.datetime
        #time_s_9 = datetime.strftime("%m-%d-%Y %H:%M:%S", time_obj_2)   # works for time.struct_time, not for datetime.datetime

        datenow = datetime.datetime.now()
        assert isinstance(datenow, datetime.datetime)
        time_s_7 = time.strftime("%m-%d-%Y %H:%M:%S")       # current time
        assert isinstance(time_s_7, str)

        time_s_1 = "12-31-2019 23:59:00"

        time_utc_diff_1 = datetime.datetime.utcnow() - datetime.datetime.now()
        assert isinstance(time_utc_diff_1, datetime.timedelta)
        assert time_utc_diff_1.days == 0
        #this sometimes works
        #assert self.is_approximate(time_utc_diff_1.seconds,lcl_delta_dec,5)

        time_sec_lcl_1  = datetime.datetime.fromtimestamp(time_utc_12_31_2019_23_59_00)
        time_sec_utc_1  = datetime.datetime.utcfromtimestamp(time_utc_12_31_2019_23_59_00)
        time_sec_diff_2 = time_sec_utc_1 - time_sec_lcl_1
        assert isinstance(time_sec_lcl_1, datetime.datetime)
        assert isinstance(time_sec_utc_1, datetime.datetime)
        assert isinstance(time_sec_diff_2, datetime.timedelta)
        assert time_sec_diff_2.days == 0 and time_sec_diff_2.seconds == lcl_delta_dec

        datetime_1 = datetime.datetime.fromtimestamp(time_utc_12_31_2019_23_59_00)
        time_sec_lcl_2 = int(time_sec_lcl_1.timestamp())
        time_sec_utc_2 = int(time_sec_utc_1.timestamp())
        time_sec_utc_3 = int(calendar.timegm(datetime_1.timetuple()))

        assert isinstance(time_sec_lcl_2, int) and time_sec_lcl_2 == time_utc_12_31_2019_23_59_00
        assert isinstance(time_sec_utc_2, int) and time_sec_utc_2 == time_utc_01_01_2020_07_59_00
        assert isinstance(time_sec_utc_3, int) and time_sec_utc_3 == time_utc_12_31_2019_15_59_00

        # parsing out time formats
        time_dt_1 = datetime.datetime.strptime("12-31-2019 23:59:00",         "%m-%d-%Y %H:%M:%S") # no spaces or extra chars allowed. chop off or split
        time_dt_2 = datetime.datetime.strptime("Dec 31, 2019 23:59:00",       "%b %d, %Y %H:%M:%S")   # comma ok
        time_dt_3 = datetime.datetime.strptime("Dec 31 2019 11:59:00PM",      "%b %d %Y %H:%M:%S%p")  # 24 hr clock reads this as 11th hr, PM doesnt matter
        time_dt_4 = datetime.datetime.strptime("Dec 31 2019 11:59:00PM",      "%b %d %Y %I:%M:%S%p")  # 12 hr clock reads this as 23rd hr
        time_dt_5 = datetime.datetime.strptime("Dec 31 2019 11:59:00AM",      "%b %d %Y %I:%M:%S%p")  # 12 hr clock reads this as 11th hr, AM matters
        time_dt_6 = datetime.datetime.strptime("2019/12/31 23:59:00.000",     "%Y/%m/%d %H:%M:%S.%f")
        time_dt_7 = datetime.datetime.strptime("2019/12/31 23:59:00 -0800",   "%Y/%m/%d %H:%M:%S %z") # timezone offset
        time_dt_8 = datetime.datetime.strptime("2019/12/31   23:59:00 -0800", "%Y/%m/%d %H:%M:%S %z") # extra space doesnt matter
        time_dt_9 = datetime.datetime.strptime("2019/12/31 23:59:00 +0800",   "%Y/%m/%d %H:%M:%S %z") # timezone offset

        assert isinstance(time_dt_1, datetime.datetime)
        assert time_dt_3 != time_dt_4 # 12-31-2019 11:59:00 != 12-31-2019 23:59:00
        assert time_dt_3 == time_dt_5 # 12-31-2019 11:59:00
        assert time_dt_4 == time_dt_1 # 12-31-2019 23:59:00

        # creating datetimes
        tz_pst = datetime.timezone(datetime.timedelta(hours=8))
        time_dt_1 = datetime.datetime(2019,12,31,23,59,0)
        time_dt_2 = datetime.datetime(2019,6,30,23,59,0)                # 2019-12-31 23:59:00
        time_dt_3 = datetime.datetime(2019,6,30,23,59,0,tzinfo=None)    # 2019-12-31 23:59:00
        time_dt_4 = datetime.datetime(2019,6,30,23,59,0,tzinfo=tz_pst)      # 2019-12-31 23:59:00+08:00

        tzname = time.tzname
        assert isinstance(tzname,tuple)
        local_non_dst_timezone = tzname[0]
        local_dst_timezone = tzname[1]
        assert local_non_dst_timezone == 'PST' and local_dst_timezone == 'PDT'

        timezone = time.timezone
        assert isinstance(timezone,int) and timezone == lcl_delta_dec       # non DST timezone delta/offset from utc in seconds
        is_currently_dst = time.localtime().tm_isdst    # this is currently 03/08-11/01 and non_dst is 11/01-03/08

        s = time.gmtime()   # gmtime in epoch
        # time.struct_time(tm_year=2020, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=0, tm_isdst=1)
        #p('gmtime:       {}'.format(s))

        # YYYY-MM-DD HH:MM:SS.micro
        t = datetime.datetime.now()
        #p('now:          {}'.format(t))

        # YYYY-MM-DD HH:MM:SS
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #p('now format:   {}'.format(t))

        # YYYY-MM-DD
        t = datetime.datetime.date(datetime.datetime.now())
        #p('date:         {}'.format(t))

        # HH:MM:SS.micro
        t = datetime.datetime.time(datetime.datetime.now())
        #p('time:         {}'.format(t))

        #t = datetime.datetime(time.gmtime())
        #p('datetime:     {}'.format(t))

        #p('pass test_time')

    @staticmethod
    def method_return_val(v:int) -> int:
        return v

    @staticmethod
    def method_return_val_shell(v:int) -> int:
        return ut.method_return_val(v)

    @staticmethod
    def method_call_inner(v:int) -> int:
        def inner_call(v:int) -> int:
            return v
        return inner_call(v)

    def test_static_function(self):
        assert ut.method_return_val_shell(10) == 10
        assert ut.method_call_inner(10) == 10
        pass

    def inner_outer_var(self):
        cnt = 10
        def inner_func():
            def inner_inner_func():
                nonlocal cnt
                assert cnt == 0
                cnt = 20
            nonlocal cnt
            assert cnt == 10
            cnt = 0
            inner_inner_func()
        assert cnt == 10
        inner_func()
        assert cnt == 20

    def test_secrets(self):
        v = 0x1000_2000
        r = secrets.randbelow(v)
        assert r <= v
        r = secrets.token_hex(32)
        v = str(r)
        assert len(r) == 64
        assert len(v) == 64
        r = secrets.token_bytes(32)
        v = str(r)
        l = bytes(r)
        assert len(r) == 32
        assert len(l) == 32
        v0 = secrets.randbits(16)
        v1 = secrets.randbits(32)
        v2 = secrets.randbits(64)
        v3 = secrets.randbits(128)

        return

    '''
    def testHash(self):
        from Crypto.Hash import SHA256
        from Crypto.Cipher import AES
        from Crypto import Random
        from Crypto.Util import Padding


        m1 = hashlib.sha1()
        m2 = hashlib.sha1()

        b1 = b"hello"
        b2 = b'hello'
        assert b1 == b2
        m1.update(b1)
        m2.update(b2)
        val1 = m1.hexdigest()
        val2 = m2.hexdigest()
        assert isinstance(val1,str)
        assert val1 == val2

        b1 = b"i am a cat"
        b2 = b'i am a cat'
        assert b1 == b2
        m1.update(b1)
        m2.update(b2)
        val3 = m1.hexdigest()
        val4 = m2.hexdigest()
        assert isinstance(val1,str)
        assert val1 == val2
        assert val1 != val3

        m1.update(b"{aval=123 anotherval='null'}")  # these are not the same
        m2.update(b'{aval=123 anotherval="null"}')
        val1 = m1.hexdigest()
        val2 = m2.hexdigest()
        assert val1 != val2

        ll = [
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ]

        m256 = hashlib.sha256()
        for row in ll:
            for i in row:
                m256.update((i).to_bytes(4,byteorder='big'))
        val5 = m256.hexdigest()


        # AES crypto encrypt/decrypt
        # ivt must be 16 bytes long
        # key must be 16,24,32 bytes long
        # input string must be multiple of 16 in length
        #iv16 = Crypto.Random.new().read(Crypto.Cipher.AES.block_size)

        v = 1000000
        assert sys.getsizeof(v) == 28

        s0 =    '00 abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '01 abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '02 abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '03 abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '04 abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '05 abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '06 abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '07 abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '08 abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '09 abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '0A abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '0B abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '0C abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '0D abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '0E abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '0F abcdefg hijklmnop qrstuv wxyz 1234567890\n' + \
                '10 abcdefg hijklmnop qrstuv wxyz 1234567890\n'

        keyword = 'mykeyword'
        # AES is 16B aligned, so you either need to pad it, or turn it to basey64, which is 64B align
        salt = Random.get_random_bytes(AES.block_size)
        private_key = hashlib.scrypt(keyword.encode('utf-8'),salt=salt,n=2**14,r=8,p=1,dklen=32)
        cipher = AES.new(private_key,AES.MODE_EAX)
        # nonce for CCM/GCM/OCB
        nonce = cipher.nonce
        sutfe = s0.encode('utf-8')
        b64ev = base64.b64encode(sutfe)
        #txtenc = cipher.encrypt(Padding.pad(sutfe, AES.block_size))
        txtenc,tag = cipher.encrypt_and_digest(b64ev)

        assert len(tag) == 16

        cipherd = AES.new(private_key,AES.MODE_EAX,nonce)
        sutfd = cipherd.decrypt(txtenc)
        b64dv = base64.b64decode(sutfd)
        sval = b64dv.decode('utf-8')
        assert sval == s0

        # sha256
        sha256 = SHA256.new()
        sha256.update(sutfe)
        sha256_val = sha256.hexdigest()
        sz = len(sha256_val)
        assert sz == 64
        assert 64 != (256/8)

        # this doesnt work!
        cipherd = AES.new(private_key,AES.MODE_EAX,nonce)
        sval = cipher.decrypt_and_verify(txtenc,tag)
        verify = cipherd.verify(sutfd)


        # iv16 for MODE_CBC/CFB/OFB/OPENPGP only, not GCM
        # for CBC/CFB/OFB, must be 16B long
        iv16 = 'whatisiv must16b'
        key16 = '0123456789abcdef'
        key32 = '0123456789abcdef0123456789abcdef'  # this is AES 256? 32*8 = 256

        aes_cbc_1 = AES.new(key16,AES.MODE_CBC,iv16)
        b_encrypted_1 = aes_cbc_1.encrypt('hello there bye ') # this is 16B
        b_encrypted_2 = aes_cbc_1.encrypt('this is another ') # this is 16B
        b_encrypted_3 = aes_cbc_1.encrypt('hello there bye ') # this is 16B
        aes_cbc_2 = AES.new(key16,AES.MODE_CBC,iv16)
        b_decrypted_1 = aes_cbc_1.decrypt(b_encrypted_1)
        b_decrypted_2 = aes_cbc_1.decrypt(b_encrypted_2)
        b_decrypted_3 = aes_cbc_1.decrypt(b_encrypted_3)
        b_decrypted_4 = aes_cbc_2.decrypt(b_encrypted_1)
        b_decrypted_5 = aes_cbc_2.decrypt(b_encrypted_2)
        b_decrypted_6 = aes_cbc_2.decrypt(b_encrypted_3)

        aes_cbc_32_1 = AES.new(key32,AES.MODE_CBC,iv16)
        b_encrypted_32_1 = aes_cbc_32_1.encrypt('hello there bye ') # this is 16B
        b_encrypted_32_2 = aes_cbc_32_1.encrypt('hello there bye ') # this is 16B
        b_encrypted_32_3 = aes_cbc_32_1.encrypt('hello there bye ') # this is 16B
        aes_cbc_32_2 = AES.new(key32,AES.MODE_CBC,iv16)
        b_decrypted_32_1_1 = aes_cbc_32_1.decrypt(b_encrypted_32_1)
        b_decrypted_32_1_2 = aes_cbc_32_1.decrypt(b_encrypted_32_2)
        b_decrypted_32_1_3 = aes_cbc_32_1.decrypt(b_encrypted_32_3)
        b_decrypted_32_2_1 = aes_cbc_32_2.decrypt(b_encrypted_32_1)
        b_decrypted_32_2_2 = aes_cbc_32_2.decrypt(b_encrypted_32_2)
        b_decrypted_32_2_3 = aes_cbc_32_2.decrypt(b_encrypted_32_3)

        return
    '''

    def test_hints(self):
        def ret_tuple_1(i:int,j:int,k:int) -> tuple:
            return (j,k)
        def ret_tuple_2(i:int,j:int,k:int) -> typing.Tuple[int,int]:
            return (j,k)

        # return multiple return tuple

        assert ret_tuple_1(1,2,3) == (2,3)
        assert ret_tuple_1(1,2,3) != [2,3]
        assert ret_tuple_2(1,2,3) == (2,3)
        assert ret_tuple_2(1,2,3) != [2,3]
        assert isinstance((2,3), typing.Tuple)
        assert isinstance((2,3), tuple)
        assert isinstance([2,3], list)

        tup = 2,3
        assert isinstance(tup, tuple)

    def test_all(self) -> None:
        self.test_list()
        self.test_methods_and_vars_in_scope()
        self.test_set_vs_map_vs_list()
        self.test_math_functions()
        self.test_built_in_functions()
        self.test_control_statements()
        self.test_string()
        self.test_lambda()
        self.test_sort()
        self.test_time()
        self.test_random()
        self.test_functions()
        self.test_import_class()
        p('passed main')

    def test_class_args(self) -> None:
        class N:
            ID = 0
            def __init__(self,v=None):
                self.id = N.ID
                N.ID += 1
                self.v = v
        class T:
            def __init__(self):
                self.r = N()
            def get_root(self) -> N:
                return self.r
            # self instance variable not allowed because default evaluated before instances exist
            #def get_n(self,n:N=self.get_root()) -> N:
            def get_n(self,n:N=None) -> N:
                if n is None:
                    return self.get_root()
                return n
            def get_int(self,v:int) -> int:
                return v
        t = T()
        n = N(1)
        r = t.get_root()
        assert t.get_n(n) == n
        assert t.get_n(None) == r
        assert t.get_n() == r
        assert t.get_int('hello') == 'hello'  # hints not enforced!! static typing probably needs library for enforce

    def test_named_vars(self) -> None:      # return type is None
        pass

    def returnlist1(self, in_list: list) -> list:   # optional hint typing
        return in_list

    def returnlist2(self, in_list: list, in_str: str, in_int: int = 5) -> list:
        return in_list

    def test_print_format(self):
        width = 3
        v1 = 1
        v2 = 2
        #p('--| ---|')
        assert f"{v1:{width}} {v2:{width+1}}" == '  1    2'     # print width with f" formatter

        v3 = '|'
        assert f"{v3:{width}}"  == '|  '
        assert f"{v3:>{width}}" == '  |'

        # old format with % operator
        s = 'hello %s' % v1
        assert s == 'hello 1'

        s = 'hello %s %d' % (v1,v2)
        assert s == 'hello 1 2'

        # format operator
        s = 'hello {}'.format(v1)
        assert s == 'hello 1'

        s = 'hello {} {}'.format(v1,v2)
        assert s == 'hello 1 2'

        # string interpolation f-strings newer python 3.6
        s = f'hello {v1}'
        assert s == 'hello 1'

        s = f'hello {v1} {v2}'
        assert s == 'hello 1 2'

        s = f'{v1:5}'
        assert s == '    1'

        s = f'{v1:>5}'
        assert s == '    1'

        s = f'{v1:<5}'
        assert s == '1    '

        s = 'hello %5d %5d'%(v1,v2)
        assert s == 'hello     1     2'

        s = 'hello {:5d} {:5d}'.format(v1,v2)
        assert s == 'hello     1     2'

        # string.Template is for user supplied format
        t = string.Template('hello $v_1')
        s = t.substitute({'v_1':v1})
        assert s == 'hello 1'

        t = string.Template('hello $v_1 $v_2')
        s = t.substitute({'v_2':v2,'v_1':v1})
        assert s == 'hello 1 2'

    def test_yield_generator(self):
        def get_next_1():
            yield 10
            yield 20
            yield 30
        def get_next(max=None):
            num = 0
            while True:
                yield num       # this replaces return
                num += 1
                if max is not None:
                    if num > max:
                        break
        def gen_blob_no_yield(sz_bytes,max,c):
            num = 0
            sz_c = len(c)
            pat = c
            if sz_c == 0:
                pat = 'x'
            num_repeat_pat = int(sz_bytes / sz_c) + 1
            l = []
            while num <= max:
                blob = pat * num_repeat_pat
                l.append(blob)
                num += 1
            return l
        def gen_blob(sz_bytes,max,c):
            num = 0
            sz_c = len(c)
            pat = c
            if sz_c == 0:
                pat = 'x'
            num_repeat_pat = int(sz_bytes / sz_c) + 1
            while num <= max:
                blob = pat * num_repeat_pat
                yield blob
                num += 1
        def test_not_out_of_memory():
            pat = 'ababababababababaababababa' * 1000
            g = gen_blob(100_000_000,1000,pat)
            ctr = 0
            for v in g:
                ctr += 1
            pass
        def test_out_of_memory():
            pat = 'ababababababababaababababa' * 1000
            gen_blob_no_yield(100_000_000,1000,pat)
            pass
        def test_get_next():
            ctr = 0
            max = 1000
            flag = False

            gen = get_next()        # gen is a generator with None
            for i in gen:
                ctr = i
                if ctr >= max:
                    break

            #g = get_next_1         # invalid syntax
            g = get_next_1()
            v = next(g)
            assert v == 10
            v = next(g)
            assert v == 20
            v = next(g)
            assert v == 30
            try:
                v = next(g)         # cannot call anymore
            except Exception as e:  # StopIteration
                flag = True
            assert flag
            flag = False

            ctr = 0
            gen = get_next(1000)    # this works
            for i in gen:           # this stops eventually
                ctr = i
            assert ctr == 1000

            gen = get_next(10)
            for i in gen:
                ctr = i
            assert ctr == 10

            gen = get_next(10)
            v = next(gen)           # you can call next(iterator)
            assert v == 0
            v = next(gen)
            assert v == 1

            gen = (i for i in range(100))   # this is also a generator
            l   = [i for i in range(100)]   # this is a list
            assert isinstance(l,list)
            #assert isinstance(l,types.ListType) # this exists in 2.7, not in 3+
            assert isinstance(gen,types.GeneratorType)
            assert isinstance(gen,list) == False
            l2  = [i for i in gen]          # now use the generator
            assert l == l2
            gen = (i for i in range(100))
            l2  = list(gen)
            assert l == l2

            gen = (i for i in range(100))
            v = next(gen)
            v = next(gen)
            v = next(gen)
            assert v == 2

            # give an example of generator chaining with g1 = (gen1), g2 = (g for g in g1), for v in g2:

            # coroutines are routines that yield, you can chain them for memory efficiency. coroutine
            # has .send .close .__next__ etc
            # coroutines used in async context where coroutine can be passed as asyncio.coroutine into future

        test_get_next()
        #test_out_of_memory()
        #test_not_out_of_memory()

    def test_os_env(self):
        p(os.environ)
        if 'PASSWORD_TEST' in os.environ:
            p(os.environ['PASSWORD_TEST'])
        if 'GDMSESSION' in os.environ:
            p(os.environ['GDMSESSION'])
        p(sys.prefix)
        #p(site.getpackages())   # where third party libs are placed
        return

    def test_file_read(self):
        def file_reader(filename):
            lines = [ line.strip() for line in open(filename,'r').readlines() ]
            p(lines)
        def file_reader_with(filename):
            '''
            with is for working with resources, such as files and sockets, descriptors

            with expression [as variable]:
                with-block

            '''
            lines = []
            with open(filename,'r') as f:
                lines = [ line.strip() for line in f.readlines() ]
            p(lines)
        def file_reader_generator(filename):
            g1 = (line for line in open(filename))    # generator chaining
            g2 = (line.strip() for line in g1)        # another generator
            lines = []
            for line in g2:                           # line is already stripped
                lines.append(line)
            p(lines)
        def file_reader_without(filename):
            f = open(filename,'r')
            try:
                lines = [ line.strip() for line in f.readlines() ]
                p(lines)
            finally:
                f.close()

        def csv_reader(filename):
            data = {}
            keys = []
            filehandle = open(filename,'r')
            csv_reader = csv.reader(filehandle)
            keys = next(csv_reader)
            assert isinstance(keys,list)
            for key in keys: data[key] = []
            for line in csv_reader:
                for k,v in zip(keys,line):
                    data[k].append(v)
            filehandle.close()
            for key in keys:
                p(key)
                for v in data[key]:
                    p('    {}'.format(v))

        def csv_dict_reader(filename):
            data = {}
            keys = []
            filehandle = open(filename,'r')
            csv_reader = csv.DictReader(filehandle)
            keys = csv_reader.fieldnames
            assert isinstance(keys,list)
            for key in keys: data[key] = []
            for line in csv_reader:
                for key in keys:
                    data[key].append(line[key])
            filehandle.close()
            for key in keys:
                p(key)
                for v in data[key]:
                    p('    {}'.format(v))
        def csv_pandas(filename):
            data = pandas.read_csv(filename)
            p(data) # this layout is truncated!
        def csv_format(f):
            '''
            input is    k1,k2,k3
                        v11,v12,v13
                        v21,v22,v23
            output is:
                        d1[k1]=[v11,v21]
                        d1[k2]=[v12,v22]
                        d1[k3]=[v13,v23]
            output is
                        d2[v11]={k1:v11,k2:v12,k3:v13}
                        d2[v21]={k1:v21,k2:v22,k3:v23}
                        make the key as one of the values and a map
            '''
            d1 = {}
            d2 = {}
            d3 = {}
            fh = open(f,'r',encoding='utf-8-sig')
            csvreader = csv.reader(fh)
            keys = next(csvreader)
            for k in keys:
                d1[k] = []
            assert isinstance(keys,list)
            for line in csvreader:
                if line is None or len(line) == 0: continue
                # this is for 3 column table only
                assert isinstance(line,list)

                # 3 different ways of parsing
                for i in range(len(keys)):
                    k = keys[i]
                    d1[k].append(line[i])
                k = line[0]
                d2[k] = dict(zip(keys,line))
                d3[k] = {
                    keys[0]:line[0],
                    keys[1]:line[1],
                    keys[2]:line[2]
                }
            fh.close()

            ftmp1 = 'tmp.1.log'
            fho = open(ftmp1,'w',encoding='utf-8')
            csvwriter = csv.DictWriter(fho,fieldnames=[keys[0],keys[1],keys[2]])
            csvwriter.writeheader()
            for k,v in d2.items():
                csvwriter.writerow(v)
            fho.close()

            ftmp2 = 'tmp.2.log'
            fho = open(ftmp2,'w',encoding='utf-8')
            csvwriter = csv.writer(fho,delimiter=',')
            csvwriter.writerow([keys[0],keys[1],keys[2]])
            for k,v in d2.items():
                csvwriter.writerow(v)
            fho.close()

            return (d1,d2)
        def csv_format_dictreader(f):
            d1 = {}
            d2 = {}
            d3 = {}
            fh = open(f,'r')
            reader = csv.DictReader(fh)
            keys = reader.fieldnames
            for k in keys:
                d1[k] = []
            for row in reader:
                assert isinstance(row,dict)
                for k,v in row.items():
                    d1[k].append(v)
                # same thing but this looks better
                for k in keys:
                    d3[k].append(row[k])
                d2[row[keys[0]]]=row
            fh.close()
            return (d1,d2)
        def t0():
            filename = None
            if filename is None:
                return
            csv_reader(filename)
        def t1():
            f = 'input/test1.csv'
            d1,d2 = csv_format(f)
            assert d1 == {'k1': ['11','12','13','14','15'],
                          'k2': ['25','24','23','22','21'],
                          'k3': ['31','32','33','34','35']}
            assert d2 == {'11': {'k1':'11','k2':'25','k3':'31'},
                          '12': {'k1':'12','k2':'24','k3':'32'},
                          '13': {'k1':'13','k2':'23','k3':'33'},
                          '14': {'k1':'14','k2':'22','k3':'34'},
                          '15': {'k1':'15','k2':'21','k3':'35'}}
            d1,d2 =csv_format_dictreader(f)
            assert d1 == {'k1': ['11','12','13','14','15'],
                          'k2': ['25','24','23','22','21'],
                          'k3': ['31','32','33','34','35']}
            assert d2 == {'11': {'k1':'11','k2':'25','k3':'31'},
                          '12': {'k1':'12','k2':'24','k3':'32'},
                          '13': {'k1':'13','k2':'23','k3':'33'},
                          '14': {'k1':'14','k2':'22','k3':'34'},
                          '15': {'k1':'15','k2':'21','k3':'35'}}
        t1()
    def test_zip_lists(self):
        def t0():
            l0 = [1,2,3,4,5]
            l1 = [11,12,13,14,15]
            l2 = [21,22,23,24,25]
            z  = zip(l0,l1,l2)
            assert isinstance(z,zip)    # zip is an iterator
            a = list(z)
            assert a == [(1,11,21),(2,12,22),(3,13,23),(4,14,24),(5,15,25)]

            s = []
            for i,j,k in a:
                v = '{},{},{}'.format(i,j,k)
                s.append(v)
            assert s == ['1,11,21','2,12,22','3,13,23','4,14,24','5,15,25']

            l0 = [11,12,13]
            l1 = [21,22,23]
            l2 = [31,32,33]
            z  = zip(l0,l1,l2)
            s = []
            for i,j,k in z: # z is an iterator
                v = '{},{},{}'.format(i,j,k)
                s.append(v)
            assert s == ['11,21,31','12,22,32','13,23,33']

            z  = zip(l0,l1,l2)
            a = list(z)
            assert a == [(11,21,31),(12,22,32),(13,23,33)]
            a = list(z)                 # iterator all used up!!
            assert a == []

            l0 = (11,12,13)
            l1 = (21,22,23)
            l2 = (31,32,33)
            a  = list(zip(l0,l1,l2))
            assert a == [(11,21,31),(12,22,32),(13,23,33)]
            assert a == [(11,21,31),(12,22,32),(13,23,33)]

            l0 = [11,12,13]
            l1 = [21,22,23]
            l2 = [31,32,33]
            a  = list(zip(l0,l1,l2))
            assert a == [(11,21,31),(12,22,32),(13,23,33)]
            l0,l1,l2 = zip(*a)          # unzip
            assert isinstance(l0,tuple)
            assert l0 == (11,12,13) and l1 == (21,22,23) and l2 == (31,32,33)
            l0 = list(l0)               # convert tuple to list
            assert l0 == [11,12,13]
            a  = [list(l) for l in zip(l0,l1,l2)]       # convert from tuple to list
            assert a == [[11,21,31],[12,22,32],[13,23,33]]

            # lists to list of tuples
            l0 = [11,12,13]
            l1 = [21,22]
            l2 = [31,32,33,34]
            a  = list(zip(l0,l1,l2))    # truncates at shortest list
            assert a == [(11,21,31),(12,22,32)]

            # list of tuples to lists
            assert list(zip([1,2,3],[2,3,4])) == [(1,2),(2,3),(3,4)]
            l0 = [(1,2),(2,3),(3,4)]
            l1,l2 = zip(*[(1,2),(2,3),(3,4)])
            assert isinstance(l1,tuple)
            assert (l1,l2) == ((1,2,3),(2,3,4))

        t0()

    def test_sleep(self):
        def test_sync_sleep():
            tbegms = time.time() * 1000
            time.sleep(0.5) # this is blocking. sleep is for seconds, so 0.5 is 500ms
            tendms = time.time() * 1000

            tdiffms = tendms - tbegms
            assert tdiffms > 500 and tdiffms < 800

        async def test_async_sleep():
            # this returns a function that waits, but this doesnt block. it pauses coroutine
            tbegms = time.time() * 1000
            # asyncio.sleep registers function to be called in x seconds,
            # doesnt actually block. works like a yield.
            # time.sleep() actually blocks and sleeps
            await asyncio.sleep(0.5)
            tendms = time.time() * 1000

            tdiffms = tendms - tbegms
            assert tdiffms > 500 and tdiffms < 800

        async def test_get_async_sleep(s,v):
            await asyncio.sleep(s)
            return v

        async def test_get_list_async_sleep(time_sec,int_beg,int_end):
            await asyncio.sleep(time_sec)
            l = [i for i in range(int_beg,int_end)]
            return l

        async def test_get_asyncio1():
            tbegms = time.time() * 1000

            coroutine_obj = test_get_async_sleep(0.5,10)

            assert asyncio.iscoroutinefunction(test_get_async_sleep) == True
            assert asyncio.iscoroutine(coroutine_obj) == True

            tmidms = time.time() * 1000 # this returns before timer starts
            res = await coroutine_obj

            tendms = time.time() * 1000
            tdiffms = tendms - tbegms

            assert tdiffms > 500 and tdiffms < 800

            tdiffmid = tendms - tmidms
            assert tdiffmid > 500

            assert res == 10

            tbegms = time.time() * 1000
            coroutine_obj = test_get_list_async_sleep(0.5,1,6)
            res = await coroutine_obj
            tendms = time.time() * 1000
            tdiffms = tendms - tbegms
            assert tdiffms > 500 and tdiffms < 800
            assert res == [1,2,3,4,5]

        async def test_get_asyncio2():
            tbegms = time.time() * 1000
            l_handlers = []
            l_times = []
            for i in range(3,7):
                rand_time_s = random.randint(5,10)/10
                handler = test_get_async_sleep(rand_time_s,i)
                l_times.append(rand_time_s)
                l_handlers.append(handler)
            results = await asyncio.gather(*l_handlers)  # wait for all, there is no timeout
            tendms = time.time() * 1000
            tdiffms = tendms - tbegms
            assert tdiffms > 500 and tdiffms < (1000 + 200)
            assert results == [3,4,5,6]

            '''

            tbegms = time.time() * 1000
            l_handlers = []
            l_times = []
            for i in range(3,7):
                rand_time_s = random.randint(5,10)/10
                handler = test_get_async_sleep(rand_time_s,i)
                l_times.append(rand_time_s)
                l_handlers.append(handler)
            results = await asyncio.wait(*l_handlers,timeout=1)  # wait for all
            tendms = time.time() * 1000
            tdiffms = tendms - tbegms
            assert tdiffms > 500 and tdiffms < (1000 + 200)
            assert results == [3,4,5,6]
            '''


        async def test_get_async_timeout():
            # multiple coroutines/futures
            l_handlers = []
            max_timeout = 1.0
            l_return_vals  = [1,  2,  3,  4,  5]
            l_timeout_vals = [1.5,0.5,0.8,1.8,0.5]
            tbegms = time.time() * 1000
            for i in range(len(l_return_vals)):
                v = l_return_vals[i]
                ms = l_timeout_vals[i]
                handler = test_get_async_sleep(ms,v)
                l_handlers.append(handler)
            flag = False
            try:
                done,pending = await asyncio.wait(l_handlers,timeout=max_timeout)  # wait for all
                tdiffms = time.time() * 1000 - tbegms
                assert tdiffms > 500 and tdiffms < (1000 + 200)

                results = set([f.result() for f in done])
                assert results == set([2,3,5])
            except asyncio.TimeoutError as e:
                flag = True
            except Exception as e:
                flag = True
            assert flag == False

        async def test_get_async_timeout_single_cases():
            # single cases

            # this one times out
            tbegms = time.time() * 1000
            handler = test_get_async_sleep(1,5)
            done,pending = await asyncio.wait({handler},timeout=0.5)
            tdiffms = time.time() * 1000 - tbegms
            assert tdiffms > 500 and tdiffms < (500 + 200)
            assert len(done) == 0 and len(pending) == 1

            # this one does not time out
            tbegms = time.time() * 1000
            handler = test_get_async_sleep(1,5)
            done,pending = await asyncio.wait({handler},timeout=1.5)
            tdiffms = time.time() * 1000 - tbegms
            assert tdiffms > 1000 and tdiffms < (1000 + 200)
            assert len(done) == 1 and len(pending) == 0
            results = set([f.result() for f in done])
            assert results == set([5])

            # this one does not time out
            tbegms = time.time() * 1000
            handler = test_get_async_sleep(1,5)
            result = await asyncio.wait_for(handler,timeout=1.5)
            tdiffms = time.time() * 1000 - tbegms
            assert tdiffms > 1000 and tdiffms < (1000 + 200)
            assert result == 5

            # this one times out
            try:
                flag = False
                tbegms = time.time() * 1000
                handler = test_get_async_sleep(1,5)
                result = await asyncio.wait_for(handler,timeout=0.5)
                assert flag
            except asyncio.TimeoutError as e:
                flag = True
            assert flag == True


            #assert isinstance(done,types.Set)
            #assert isinstance(done,types.CoroutineType)

        async def test_many_async_tasks():
            lh = []
            numcases = 10000
            tbegms = time.time() * 1000
            for i in range(numcases):
                timeout = random.randint(1,20)/10 # 0.1-2 seconds
                lh.append(test_get_async_sleep(timeout,i))
            tmidms = time.time() * 1000
            done,pending = await asyncio.wait(lh,timeout=2.5)
            tendms = time.time() * 1000
            tdiffms = tendms - tbegms
            assert tdiffms < (2500+200)
            assert len(pending) == 0
            lres = [f.result() for f in done]
            assert len(lres) == numcases
            set_exp = set([i for i in range(numcases)])
            assert set_exp == set(lres)

        async def test_many_async_tasks_continuous_queue_til_drain():
            # limit the number of in-flight tasks to X, with pending ones in queue
            # allow 100 concurrent requests in flight with 10000 requests
            # each request takes 0.1 seconds
            # 10000request/100concurrent = 100 * 0.1 = 10 seconds expected to finish this job

            num_cases = 10000
            timems = 0.1
            maxconcur = 100
            refill = int(maxconcur*3/4)
            lres = []

            ctr = 0
            num_completed = 0
            num_submitted = 0
            pending = set()

            tbegms = time.time() * 1000

            while num_submitted < num_cases:
                while num_submitted < num_cases and len(pending) < maxconcur:
                    coro = test_get_async_sleep(timems,num_submitted)
                    pending.add(coro)
                    num_submitted += 1
                assert len(pending) <= maxconcur
                while len(pending) > refill:
                    done,pending = await asyncio.wait(pending,return_when=asyncio.FIRST_COMPLETED)
                    for task in done:
                        lres.append(task.result())
                        num_completed += 1

            if len(pending) != 0:
                done,pending = await asyncio.wait(pending,return_when=asyncio.ALL_COMPLETED)
                for result in done:
                    lres.append(result.result())
                    num_completed += 1

            tendms = time.time() * 1000

            assert num_completed == num_cases
            set_act = set(lres)
            set_exp = set([i for i in range(num_cases)])
            set_dif = set_act.symmetric_difference(set_exp)

            #print('num_completed:{}'.format(num_completed))
            #print('set_dif:{}'.format(set_dif))

            assert set_act == set_exp

            tdiffms = tendms - tbegms
            #print(tdiffms)
            assert tdiffms < (10000+1000) # should be less than 11 seconds

            pass

        async def test_many_sync_tasks1():
            # same as test_many_sync_tasks1 except FIRST_COMPLETED with many loops
            # test_asyncio_sempahore is more sensible way of doing it
            lh = []
            numcases = 10000
            tbegms = time.time() * 1000
            for i in range(numcases):
                timeout = random.randint(1,20)/10 # 0.1-2 seconds
                lh.append(test_get_async_sleep(timeout,i))

            num_completed = 0
            remaining = lh
            results = set()
            num_loops_visited = 0
            while num_completed < numcases:
                done,pending = await asyncio.wait(remaining,return_when=asyncio.FIRST_COMPLETED)
                for result in done:
                    results.add(result.result())
                    num_completed += 1
                remaining = pending
                num_loops_visited += 1
            assert len(remaining) == 0
            tendms = time.time() * 1000
            tdiffms = tendms - tbegms
            assert tdiffms < (2000+800)
            set_exp = set([i for i in range(numcases)])
            assert set_exp == set(results)

        async def test_many_sync_tasks2():
            # same as test_many_sync_tasks1 except ALL_COMPLETED with 1 loop
            lh = []
            numcases = 10000
            tbegms = time.time() * 1000
            for i in range(numcases):
                timeout = random.randint(1,20)/10 # 0.1-2 seconds
                lh.append(test_get_async_sleep(timeout,i))

            num_completed = 0
            remaining = lh
            results = set()
            num_loops_visited = 0
            while num_completed < numcases:
                done,pending = await asyncio.wait(remaining,return_when=asyncio.ALL_COMPLETED)
                for result in done:
                    results.add(result.result())
                    num_completed += 1
                remaining = pending
                num_loops_visited += 1
            assert len(remaining) == 0
            assert num_loops_visited == 1
            tendms = time.time() * 1000
            tdiffms = tendms - tbegms
            assert tdiffms < (2000+800)
            set_exp = set([i for i in range(numcases)])
            assert set_exp == set(results)

        async def test_many_sync_tasks3():
            # same as test_many_sync_tasks1 except FIRST_COMPLETED and create_task with many loops
            lh = []
            numcases = 10000
            tbegms = time.time() * 1000
            for i in range(numcases):
                timeout = random.randint(1,20)/10 # 0.1-2 seconds
                lh.append(asyncio.create_task(test_get_async_sleep(timeout,i)))

            num_completed = 0
            remaining = lh
            results = set()
            num_loops_visited = 0
            while num_completed < numcases:
                done,pending = await asyncio.wait(remaining,return_when=asyncio.FIRST_COMPLETED)
                for result in done:
                    results.add(result.result())
                    num_completed += 1
                remaining = pending
                num_loops_visited += 1
            assert len(remaining) == 0
            tendms = time.time() * 1000
            tdiffms = tendms - tbegms
            assert tdiffms < (2000+800)
            set_exp = set([i for i in range(numcases)])
            assert set_exp == set(results)

        def test_sync_function_call_async1():
            # cannot call await handler in sync function.

            # need to create event loop. a new_event_loop or existing one is ok either way
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            #loop = asyncio.get_event_loop() # existing one also works

            tbegms = time.time() * 1000

            coroutine_handler = test_get_async_sleep(0.5,10)
            res = loop.run_until_complete(coroutine_handler)

            tendms = time.time() * 1000
            tdiffms = tendms - tbegms

            assert tdiffms > 500 and tdiffms < 700
            assert res == 10
            #loop.close()

        def test_sync_function_call_async2():
            # cannot call await handler in sync function.

            loop = asyncio.get_event_loop() # existing one also works

            tbegms = time.time() * 1000

            coroutine_handler = test_get_async_sleep(0.5,10)
            res = loop.run_until_complete(coroutine_handler)

            tendms = time.time() * 1000
            tdiffms = tendms - tbegms

            assert tdiffms > 500 and tdiffms < 700
            assert res == 10
            loop.close()


        def test_call_get_asyncio():
            # get_event_loop is for calling async within sync function
            #loop = asyncio.get_event_loop()
            #loop.run_until_complete(test_get_asyncio())
            asyncio.run(test_get_asyncio1())
            asyncio.run(test_get_asyncio2())


        def test_await_async():
            test_sync_sleep()
            asyncio.run(test_async_sleep()) # asyncio.run on non async function to wait

        def test_asyncio_sempahore():
            async def return_bounded_by_semaphore(semaphore,ms,v):
                async with semaphore:
                    await asyncio.sleep(ms)
                    return v
            async def many_tasks():
                semaphore = asyncio.Semaphore(100)
                num_tasks = 1000
                ltasks = [asyncio.create_task(return_bounded_by_semaphore(semaphore,0.1,i)) for i in range(num_tasks)]
                results = await asyncio.gather(*ltasks)
                set_exp = set([i for i in range(num_tasks)])
                set_act = set(results)
                assert set_exp == set_act

            def test():
                asyncio.run(many_tasks())

            test()

        def test():
            assert asyncio.iscoroutinefunction(test_get_async_timeout) == True
            assert asyncio.iscoroutine(test_get_async_timeout) == False
            assert asyncio.iscoroutinefunction(test_sync_function_call_async1) == False
            test_await_async()
            test_call_get_asyncio()
            asyncio.run(test_get_async_timeout())
            asyncio.run(test_many_async_tasks())
            asyncio.run(test_get_async_timeout_single_cases())
            asyncio.run(test_many_sync_tasks1())
            asyncio.run(test_many_sync_tasks2())
            asyncio.run(test_many_sync_tasks3())
            test_sync_function_call_async1()
            test_sync_function_call_async2()
            asyncio.run(test_many_async_tasks_continuous_queue_til_drain())
            test_asyncio_sempahore()
            #loop = asyncio.get_event_loop() # this will raise RuntimeError(there is no current event loop in thread

        test()

    def test_with_statement(self):
        pass

    async def async_ret_val(self,v,ms):

        await asyncio.sleep()

if __name__ == "__main__":
    unittest.main() # not ut.main()!

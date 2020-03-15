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
import hashlib
import datetime
import numpy
import calendar
import string           # this is for string templates
import enum
import utils.myutils    # test import from utils directory
import utils.myutils as myutils1

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

class ut(unittest.TestCase):
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
        myutils = utils.myutils.my_utils()
        myutilsx = myutils1.my_utils()          # import AS something
        v = myutils.rand(1,2)                   # instance function
        v = utils.myutils.my_utils.rand(1,2)    # static function
        assert utils.myutils.my_utils.charset_num == '0123456789'
        assert myutils.charset_num == '0123456789'
        assert 1 == myutilsx.get(1)             # instance function

    def test_class_scope(self):
        class InnerInnerClass:
            def __init__(self,x,y):
                self.x = x
                self.y = y

        oc      = OuterClass(1,2)
        aco     = AmbiguousClass(2,3)
        ic      = ut.InnerClass(3,4)
        aci     = ut.AmbiguousClass(4,5,6)
        iic     = InnerInnerClass(6,7)
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

    def test_random(self):
        min = 1
        max = 10
        numruns = 100
        for i in range(numruns):
            val = random.randint(min, max)  # randint is min <= x <= max
            assert val >= min and val <= max
        for i in range(numruns):
            val = random.randrange(min, max)  # randint is min <= x < max
            assert val >= min and val < max

    def test_list(self):
        # push and pop
        l = []
        l.append(1)
        l.append(2)
        assert len(l) == 2

        v = l.pop()
        assert v == 2
        assert len(l) == 1

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

        l = [[2] * 3]
        assert l == [[2,2,2]]

        l = [2] * 3
        assert l == [2,2,2]

        l = [0] * 3
        assert l == [0,0,0]

        l = [[0] * 3,[1] * 3]
        assert l == [[0,0,0],[1,1,1]]

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

        #p('pass test_list')

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

        #p('test_string')

    def test_set_vs_map_vs_list(self):
        vset = set()
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

        s1 = {1,2,3,4,5}
        s2 = {3,2,4,5,1}
        s3 = s1.difference(s2)
        assert len(s3) == 0

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
        l = list(s)
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

    def test_built_in_functions(self):
        assert max(4,10,8,3) == 10  # max(a1,a2,*args[,key])
        assert min(4,10,8,3) == 3
        assert abs(-10) == 10
        assert abs(10) == 10

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

    def test_math_functions(self):
        vact = math.factorial(5)
        vexp = 5 * 4 * 3 * 2 * 1
        assert vact == vexp

        l = []
        for i in range(2,4):
            l.append(i)
        assert l == [2,3]

        v = 10//3       # floored 10/3 = 3
        assert v == 3

        v = 10/3
        assert v != 3.33
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

        #p('pass test_math_functions')

    def test_control_statements(self):
        l = []
        for i in range(5,0,-1):
            l.append(i)
        assert l == [5,4,3,2,1]

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

        #p('pass test_sort')

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
                assert cnt == 0
                cnt = 20
            assert cnt == 10
            cnt = 0
            inner_inner_func()
        assert cnt == 10
        inner_func()
        assert cnt == 20

    def main(self) -> None:
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

    def test_named_vars(self) -> None:      # return type is None
        pass

    def returnlist1(self, in_list: list) -> list:   # optional hint typing
        return in_list

    def returnlist2(self, in_list: list, in_str: str, in_int: int = 5) -> list:
        return in_list

if __name__ == "__main__":
    ut.main()
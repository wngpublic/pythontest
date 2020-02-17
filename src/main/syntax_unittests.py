import unittest
import queue
import heapq
import math
import collections
import re
import functools
import array

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

class ut(unittest.TestCase):

    def setUp(self):
        #p('setup called')
        pass

    def tearDown(self) -> None:
        #p('teardown called')
        pass

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

    def test_list_of_list(self) -> None:   # return type is none
        '''
        examples of list of list
        '''
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

        #p('test_list_of_list passed')

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

        l = re.split(r'\s+', s_orig)
        assert l == ['','abc','def','123','']

        s = s_orig.strip()
        l = re.split(r'\s+',s)
        assert l == ['abc','def','123']

        s = ''.join(l)
        assert s == 'abcdef123'
        s = ','.join(l)
        assert s == 'abc,def,123'
        l = s.split(',')
        assert l == ['abc','def','123']

        s = '111 111\n' + \
            '222  222 \n' + \
            ' 333 333  \n'

        assert s == '111 111\n222  222 \n 333 333  \n'
        l = s.split('\n')
        assert l == ['111 111','222  222 ',' 333 333  ','']
        l = s.splitlines()
        assert l == ['111 111','222  222 ',' 333 333  ']

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

        #p('pass test_set_vs_map_vs_list')

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

        assert math.floor(3.333) == 3
        assert math.ceil(3.333) == 4
        assert math.ceil(3.5) == 4

        #p('pass test_math_functions')

    def test_control_loops(self):
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

    def main(self) -> None:
        self.test_list()
        self.test_methods_and_vars_in_scope()
        self.test_set_vs_map_vs_list()
        self.test_math_functions()
        self.test_built_in_functions()
        self.test_control_loops()
        self.test_string()
        self.test_lambda()
        self.test_sort()
        p('passed main')

    def test_named_vars(self) -> None:      # return type is None
        pass

    def returnlist1(self, in_list: list) -> list:   # optional hint typing
        return in_list

    def returnlist2(self, in_list: list, in_str: str, in_int: int = 5) -> list:
        return in_list

if __name__ == "__main__":
    syntax_ut.main()
import unittest
import queue
import math
import collections


'''
python3 -m unittest unittests.ut.test_list
or
python3 unittest_algos.py ut.test_list
or alias pythonut ut.test_something 
pythonut unittest_algos.ut.main
where pythonut='python3 -m unittest'

pythonut unittest_algos.ut.main
'''

global_debug_level_ = 0  # 0 to 5. 0 = off, 1 = highest, 5 = lowest
global_output_to_file_ = False
global_fh_ = None

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
    '''
    cannot override __init__ of unittest, which is
    __init__(self,*args,**kwargs)

    def __init__(self):
        self.perfctr = 0
        self.vdbg = False

    '''

    def setUp(self):
        self.perfctr = 0
        self.dbg = False

    def incperfctr(self):
        self.perfctr += 1

    def getperfctr(self):
        return self.perfctr

    def dbg(s):
        if self.dbg:
            p(s)

    #    p('setup')
    #def tearDown(self) -> None:
    #    p('teardown')
    def test_increasing_val(self):
        '''
        given list of vals, return a list that says when next val is higher than itself.
        '''
        def _increasing_val_brute(l):
            result = []
            for i in range(len(l)):
                j = i
                while(j < len(l) and l[i] >= l[j]):
                    j += 1
                if j == len(l):
                    result.append(0)
                else:
                    result.append(j-i)
            return result
        def _increasing_val(l):
            stack = []
            result = []
            for i in range(len(l)):
                result.append(0)
            # store the index in the stack, not the values
            for i in range(len(l)):
                # while stack is not empty and peek value < l[i], pop it and calculate separation value
                # i is index, stack[-1] is peek index value, and l[stack[-1] is actual value
                while(stack != [] and l[stack[-1]] < l[i]):
                    k = stack.pop()
                    result[k] = i - k
                stack.append(i)     # push index ptr to stack, not its value
            return result
        def _tc1():
            l = [13, 14, 15, 11, 9, 12, 16, 13]
            c = [ 1,  1,  4,  2, 1,  1,  0,  0]
            r1 = _increasing_val_brute(l)
            assert r1 == c
            r2 = _increasing_val(l)
            assert r2 == c
        def _tc2():
            #     0   1   2   3   4   5   6   7   8
            l = [13, 11, 10, 15, 11, 12, 10, 16, 13]
            c = [ 3,  2,  1,  4,  1,  2,  1,  0,  0]
            r1 = _increasing_val_brute(l)
            assert r1 == c
            r2 = _increasing_val(l)
            assert r2 == c
        def _tc3():
            l = [10, 11, 12, 13, 14]
            c = [ 1,  1,  1,  1,  0]
            r1 = _increasing_val_brute(l)
            assert r1 == c
            r2 = _increasing_val(l)
            assert r2 == c
        def _tc4():
            l = [14, 13, 12, 11, 10]
            c = [ 0,  0,  0,  0,  0]
            r1 = _increasing_val_brute(l)
            assert r1 == c
            r2 = _increasing_val(l)
            assert r2 == c
        def _tc5():
            l = [14, 13, 12, 11, 13]
            c = [ 0,  0,  2,  1,  0]
            r1 = _increasing_val_brute(l)
            assert r1 == c
            r2 = _increasing_val(l)
            assert r2 == c
        _tc1()
        _tc2()
        _tc3()
        _tc4()
        _tc5()
        p('pass test_increasing_val')

    '''
    given list l and window size k, return list of max values of the sliding window
    i = 0 1 2 3 4 5 6 7 8 9 A B 
    k = 4
    l = 3 6 2 4 7 3 8 9 4 7 7 3
        3 6 2 4                         6
          6 2 4 7                       7
            2 4 7 3                     7
              4 7 3 8                   8
                7 3 8 9                 9
                  3 8 9 4               9
                    8 9 4 7             9
                      9 4 7 7           9
                        4 7 7 3         7
    '''
    def testSlidingWindowMax(self):
        _perfctr = 0
        def _get_sliding_window_max_brute(l: list, k: int) -> list:
            _perfctr = 0
            r = [0] * (len(l)-k+1)
            for i in range(0,len(l)-k+1):
                window = l[i:i+k]
                max = window[0]
                for j in range(len(window)):
                    _perfctr += 1
                    if(max < window[j]):
                        max = window[j]
                r[i] = max
            return r
        def _get_sliding_window_max_heap(l: list, k: int) -> list:
            r = [0] * (len(l)-k+1)
            return r
        def _get_sliding_window_max(l: list, k: int) -> list:
            _perfctr = 0
            r = [0] * (len(l)-k+1)
            window = []
            for i in range(0,len(l)):
                _perfctr += 1
                max = l[i]
                # remove previous indices where index value < less than current index val
                # this is because rightmost would be max anyway
                while(window != []):
                    _perfctr += 1
                    peekval = l[window[len(window)-1]]
                    if(peekval <= l[i]):
                        window.pop()
                    else:
                        max = peekval
                        break
                window.append(i)
                if((i+1) >= k):
                    r[(i+1)-k] = max
                # remove out of bound left value
                idxleft = i-k
                if(window != [] and window[0] < idxleft):
                    window.pop(0)
            return r
        def _t0():
            l = [3,6,2,4,7,3,8,9,4,7,7,3]
            r = _get_sliding_window_max(l,4)
            e = [6,7,7,8,9,9,9,9,7]
            assert r == e
        def _t1():
            l = [3,6,2,4,7,3,8,9,4,7,7,3]
            r = _get_sliding_window_max(l,4)
            e = [6,7,7,8,9,9,9,9,7]
            assert r == e
        _t0()
        p('pass testSlidingWindowMax')


    def testFindSumInArrayFirst(self):
        '''
        find first combination in varray that sums to vsum. if none, return none
        '''
        perfctr=0

        def find_sum_in_array_first_recursive(vsum,varray):
            def find_sum_in_array_first_recursive(vsum,varray,set,i,j,cursum):
                pass

            pass

        pass

    def testFindSumInArrayAllSubsets(self,vsum,varray):
        '''
        find all subsets in varray that sums to vsum. if none, return none
        '''
        pass

    def testFindProductInArrayFirst(self,vproduct,varray):
        '''
        find first subset in varray that results in product value. if none, return none
        '''

    def testFindProductInArrayAllSubsets(self,vproduct,varray):
        '''
        find all subset in varray that results in product value. if none, return none
        '''

    def ordered_setlist_from_list(self, list) -> list:
        s = set(list)
        l = list(dict.fromkeys(s).keys())
        return l

    def test_quicksort(self):

        def partition_key(list,l,r) -> int:
            return (l + (r-l)/2)
            #return (l+r+1)/2
            '''
            difference between l+(r-l)/2 vs (l+r)/2
            l+(r-l)/2                5+(10-5)/2=5+5/2=7
            l+(r-l+1)/2              5+(10-5+1)/2=5+6/2=8            
            (l+r)/2                  (5+10)/2=7
            (l+r+1)/2                (5+10+1)/2=8
            '''

        def partition_swap(list,lp,rp) -> None:
            i = partition_key(list,l,r)
            partition_val = list[i]
            while(lp < rp):
                while(list[lp] < partition_val): lp += 1
                while(list[rp] > partition_val): rp -= 1
                if(lp >= rp): return rp
                swap(list,lp,rp)
            return rp

        def swap(list,l,r) -> None:
            x = list[l]
            list[l] = list[r]
            list[r] = x

    def test_quickselect(self):
        '''
        this is quicksort, but you stop at the desired index
        '''
        def partition_key(list,l,r) -> int:
            return (r-l)/2

        def partition_swap(list,lp,rp,idx_stop) -> None:
            i = partition_key(list,l,r)
            partition_val = list[i]
            while(lp < rp):
                while(list[lp] < partition_val): lp += 1
                while(list[rp] > partition_val): rp -= 1
                if(lp >= rp): return rp
                swap(list,lp,rp)
            return rp

        def swap(list,l,r) -> None:
            x = list[l]
            list[l] = list[r]
            list[r] = x

    def testCombination(self):
        perfctr = 0
        vdbg = False

        def dbg(s):
            nonlocal vdbg
            if vdbg:
                p(s)

        def incperfctr():
            nonlocal perfctr
            perfctr += 1

        def getperfctr():
            nonlocal perfctr
            return perfctr

        def quick_calc(list,k):
            # c(n,k) == n!/k!(n-k)!
            d = {}
            for v in list:
                if v in d: d[v] += 1
                else:      d[v] = 1
            n = len(d)
            v = math.factorial(n) / (math.factorial(k) * math.factorial(n-k))
            return int(v)

        def combination(l,k,tmpi,i,doprint=False):
            incperfctr()
            if getperfctr() > 1000:  return

            if len(tmpi) == k:
                if doprint: p('out: {}'.format(tmpi))
                return 1
            if i >= len(l): return 0

            cnt = 0
            for j in range(i,len(l)):
                tmpo = tmpi + l[j]
                dbg('{}:{}'.format(getperfctr(),tmpo))
                cnt += combination(l,k,tmpo,j+1,doprint)

            return cnt

        def t0():
            l0 = '12345'
            cnt0 = combination(l0,3,'',0,False)
            cnt1 = quick_calc(l0,3)
            assert cnt0 == cnt1

        def t1():
            l0 = '1223445'

        t0()

        p('testCombination pass')

    def testPermutation(self):
        perfctr = 0
        dbg = False

        def dbg(s):
            nonlocal dbg
            if dbg:
                p(s)

        def incperfctr():
            nonlocal perfctr
            perfctr += 1

        def getperfctr():
            nonlocal perfctr
            return perfctr

        def quick_calc(list,k):
            # p(n,k) == n!/(n-k)!
            # ordering matters but do not repeat chosen ones
            # if repetition, then it's just k^n, which is not this case
            d = {}
            for v in list:
                if v in d: d[v] += 1
                else:      d[v] = 1
            n = len(list)
            v = math.factorial(n) / math.factorial(n-k)
            return int(v)

        def permutation(l,k,tmpi,s,doprint=False):
            incperfctr()
            if getperfctr() > 1000:  return

            if len(tmpi) == k:
                if doprint: p('out: {}'.format(tmpi))
                return 1

            cnt = 0

            for j in range(0,len(l)):
                if j in s: continue
                s.add(j)
                tmpo = tmpi + l[j]
                #dbg('{}:{}'.format(getperfctr(),tmpo))
                cnt += permutation(l,k,tmpo,s,doprint)
                s.discard(j)

            return cnt

        def t0():
            l0 = '12345'
            cnt0 = permutation(l0,3,'',set(),False)
            cnt1 = quick_calc(l0,3)
            assert cnt0 == cnt1

        def t1():
            l0 = '1223445'

        t0()

        p('testPermutation pass')

    # heapq implementation
    '''
    heapq implementation

    00 01 02 03 04 05 06 07 08 09 10 11 12
    00 0L 0R 1L 1R 2L 2R 3L 3R 4L 4R 5L 5R

        child idx L = idx * 2 + 1
        child idx R = idx * 2 + 2
            0 -> 0*2+1,0*2+2 == 1,2
            1 -> 1*2+1,1*2+2 == 3,4
            2 -> 2*2+1,2*2+2 == 5,6
            3 -> 3*2+1,3*2+2 == 7,8

        parent idx = UPPER(idx / 2) - 1
            12/2-1 = 5
            11/2-1 = 5
            10/2-1 = 4
             9/2-1 = 4
    '''
    class _HeapQ:
        def __init__(self, is_max=False):
            self.is_max = is_max
            self.q = []

        def push(self, v):
            self.q.append(v)
            self.swim(self.q, len(self.q)-1)

        def pop(self):
            size = self.size()
            if size == 0:
                return None
            v = self.q[0]
            self.q[0] = self.q[size-1]
            del self.q[size-1]
            self.sink(self.q, 0)
            return v

        def swap(self, q, srci, dsti):
            v = q[srci]
            q[srci] = q[dsti]
            q[dsti] = v

        '''
        if minheap, swap with smaller of left or right child
        if maxheap, swap with larger of left or right child
        '''
        def sink(self, q, idx):
            size = self.size()
            idxl = idx*2+1
            idxr = idx*2+2
            if(self.is_max == False):
                if(idxr < size):
                    if(q[idxl] < q[idxr]):
                        self.swap(q, idx, idxl)
                        self.sink(q, idxl)
                    else:
                        self.swap(q, idx, idxr)
                        self.sink(q, idxr)
                elif(idxl < size):
                    if(q[idxl] < q[idx]):
                        self.swap(q, idx, idxl)
            else:
                if(idxr < size):
                    if(q[idxl] > q[idxr]):
                        self.swap(q, idx, idxl)
                        self.sink(q, idxl)
                    else:
                        self.swap(q, idx, idxr)
                        self.sink(q, idxr)
                elif(idxl < size):
                    if(q[idxl] > q[idx]):
                        self.swap(q, idx, idxl)

        '''
        if minheap, swap with parent if parent > current
        if maxheap, swap with parent if parent < current
        '''
        def swim(self, q, idx):
            if(idx == 0):
                return
            size = self.size()
            idxp = math.ceil(idx*1.0/2)-1
            if(self.is_max == False):
                if(q[idx] < q[idxp]):
                    self.swap(q, idx, idxp)
                    self.swim(q, idxp)
            else:
                if(q[idx] > q[idxp]):
                    self.swap(q, idx, idxp)
                    self.swim(q, idxp)

        def size(self):
            return len(self.q)

    def testHeapQueue(self):

        def _t0():
            hq = _HeapQ()
            hq.push(5)
            hq.push(6)
            hq.push(4)
            hq.push(7)
            hq.push(3)
            l = []
            while(hq.size() > 0):
                l.append(hq.pop())
            assert l == [3,4,5,6,7]
            p('pass heapq t0')

        def _t1():
            hq = _HeapQ(True)
            hq.push(5)
            hq.push(6)
            hq.push(4)
            hq.push(7)
            hq.push(3)
            l = []
            while(hq.size() > 0):
                l.append(hq.pop())
            assert l == [7,6,5,4,3]
            p('pass heapq t1')

        def _t():
            _t0()
            _t1()

        _t()

    class pair:
        def __init__(self, v1, v2):
            self.v1 = v1
            self.v2 = v2
        def get1(self):
            return self.v1
        def get2(self):
            return self.v2
        def __eq__(self,other):
            return self.v1 == other.v1
        def __lt__(self,other):
            return self.v1 < other.v1
        def __gt__(self,other):
            return self.v1 > other.v1

    def test_merge_sort(self):
        def t0():
            ctr = 0
            l = [[],[],[]]
            maxcols = 5
            maxrows = 3
            for i in range(maxcols):
                for j in range(maxrows):
                    p = ut.pair(ctr,j)
                    ctr += 1
                    l[j].append(p)
            r = [list(map(lambda x: x.v1,l[0])),list(map(lambda x: x.v1,l[1])),list(map(lambda x: x.v1,l[2]))]
            assert  len(l) == maxrows and r == [[0,3,6,9,12],[1,4,7,10,13],[2,5,8,11,14]]

            act = []
            for p in l[0]: act.append(p.get1())
            assert act == [0,3,6,9,12]
            q = ut._HeapQ()
            q.push(l[0][0])
            q.push(l[1][0])
            q.push(l[2][0])
            ctrs = [1,1,1]
            r = []
            while(q.size() != 0):
                p = q.pop()
                r.append(p.v1)
                if(ctrs[p.v2] < maxcols):
                    q.push(l[p.v2][ctrs[p.v2]])
                    ctrs[p.v2] += 1
            assert r == [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]

        t0()
        p('passed test_merge_sort')     # named conflict with pv if it was named p

    def test_binary_search(self):
        class _Node:
            def __init__(self,v,l=None,r=None):
                self.v = v
                self.l = l
                self.r = r
            def setlc(self,l):
                self.l = l
            def setrc(self,r):
                self.r = r
            def getlc(self):
                return self.l
            def getrc(self):
                return self.r
            def getv(self):
                return self.v

        class _BinarySearchTree:
            def __init__(self):
                self.r = None
            def get_root(self):
                return self.r
            def add(self, v):
                pass
            def get(self, v):
                pass

    def main(self):
        self.testCombination()
        self.testPermutation()
        self.test_merge_sort()
        p('main passed')

if __name__ == "__main__":
    unittest.main()
import unittest
import queue
import math
import collections
import enum
import time
import random
import utils.myutils
import typing
import logging

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

def set_logger():
    fh = logging.FileHandler('logging_output.log')
    fh.setLevel(logging.DEBUG)

    # log formatter is optional         time          appname    level space align
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-10s - line:%(lineno)-5s - %(message)s')
    log_formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)-5s - %(message)s')
    fh.setFormatter(log_formatter)

    logger = logging.getLogger('unittest_algos')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)

set_logger()

class CTR:
    def __init__(self): self.v = 0
    def inc(self,v=1): self.v += v
    def get(self): return self.v
    def set(self,v): self.v = v
    def dec(self,v=1): self.v -= v

def p(s):
    global global_output_to_file_
    global global_fh_
    if(global_output_to_file_):
        if(global_fh_ is None):
            global_fh_ = open('output_debug.log','w')
        global_fh_.write(s + '\n')
    else:
        print(s)

class Utils:
    def __init__(self, seed=0):
        self.charset_lc = 'abcdefghijklkmnopqrstuvwxyz'
        self.charset_uc = self.charset_lc.upper()
        self.charset_n  = '0123456789'
        self.charset_h  = '0123456789ABCDEF'
        self.charset_alphanum = self.charset_lc + self.charset_n
        pass
    def get_non_visited_set(self, set_target:set, set_visited:set) -> set:
        s = set()
        for v in set_target:
            if v not in set_visited:
                s.add(v)
        return s
    def get_non_visited_list(self, set_target:set, set_visited:set) -> list:
        s = self.get_non_visited_set(set_target,set_visited)
        l = list(s)
    def get_random_from_set(self, set_target:set, set_exclude:set, num_select:int, allow_select_resize:bool=False, allow_repetition=False) -> list:
        list_nonvisited = list(self.get_non_visited_set(set_target, set_exclude))
        sz = len(list_nonvisited)
        if sz < num_select:
            if allow_select_resize:
                num_select = sz
            else:
                assert sz >= num_select
        result = []
        s = set()
        max_loop = 1000
        for i in range(num_select):
            if allow_repetition:
                result.append(list_nonvisited[self.rand(0,sz)])
            else:
                for j in range(max_loop+1):
                    assert j != max_loop
                    rand_idx = self.rand(0,sz)
                    if(rand_idx >= len(list_nonvisited)):
                        assert rand_idx < len(list_nonvisited)
                    v = list_nonvisited[rand_idx]
                    if v not in s:
                        s.add(v)
                        break
        if not allow_repetition:
            assert len(s) == num_select
            result = list(s)
        return result
    def swap(self, l, i, j):
        v = l[i]
        l[i] = l[j]
        l[j] = v
    def shuffle(self, l:list,num_shuffles=3) -> list:
        result = l.copy()
        sz = len(result)
        for cnt in range(num_shuffles):
            for i in range(sz):
                self.swap(result, i, rand(0,sz))
        return result
    def rand_str(self, num:int, charset:str=None) -> str:
        if charset is None:
            charset = self.charset_alphanum
        sz = len(charset)
        l_idx = self.rand_list(0,sz,True)
        s = []
        for i in l_idx:
            s.append(charset[i])
        result = ''.join(s)
        return result
    def rand(self, min:int,max:int) -> int: # [min,max)
        if min == max: return min
        return random.randrange(min,max)
    def randint(self,min:int,max:int) -> int: # [min,max]
        if min == max: return min
        return random.randint(min,max)
    def rand_list(self, min:int,max:int,num:int,allow_repetition=False) -> list:
        sz = max - min + 1
        assert num < sz
        l = []
        s = set()
        max_loop = 100
        for i in range(num):
            if allow_repetition:
                l.append(random.randint(min,max))
            else:
                for j in range(max_loop+1):
                    assert j != max_loop
                    v = random.randint(min,max)
                    if v not in s:
                        v.add(s)
                        break
        if not allow_repetition:
            assert len(s) == num
            l = list(s)
        return l
class Pair:
    def __init__(self, v1, v2):
        this.v1 = v1
        this.v2 = v2

class GNode:
    ID = 0
    def __init__(self,v=None):
        self.id = GNode.ID
        self.v = v
        self.vertices = {}  # dst_id:weight
        GNode.ID += 1
    def get_vertices(self,is_copy=False):
        if is_copy:
            return self.vertices.copy()
        return self.vertices
    def get_v(self):
        return self.v
    def get_id(self):
        return self.id
    def add_edge(self,dst_id:int,weight=0):
        self.vertices[dst_id] = weight
    def get_global_id(self):
        return GNode.ID
    @staticmethod
    def reset_id(v:int=0):
        GNode.ID = v

class GraphNode(GNode):
    def __init__(self,v=None,name=None):
        super.__init__(v)
        self.name = name

class Graph:
    class DType(enum.Enum):
        DIRECTED = 0
        UNDIRECTED = 1
        MIXED = 2

    def __init__(self):
        self.all_nodes = {} # map of all_nodes[id] = GNode
        self.u = Utils()

    def get_all_nodes_map(self,is_copy=False):
        if is_copy:
            return self.all_nodes.copy()
        return self.all_nodes

    def add_edge_to_ids(self, src_id:int, dst_id:int, weight=0, is_directed=True):
        nodes = self.get_all_nodes_map()
        if src_id not in nodes or dst_id not in nodes:
            return
        self.add_edge_to_nodes(nodes[src_id],nodes[dst_id],weight,is_directed)
        pass

    def add_edge_to_nodes(self, src_node: GNode, dst_node: GNode, weight=0, is_directed=True):
        if src_node is None or dst_node is None:
            return
        src_node.add_edge(dst_node.get_id(),weight)
        if not is_directed:
            dst_node.add_edge(src_node.get_id(),weight)

    def make_random_graph(self, num_nodes:int, directed_type:DType, min_edges:int, max_edges:int, min_weight:int, max_weight:int) -> dict:
        '''
        directed_type:
            0 directed only
            1 bidirectionaly only
            2 mixed directed and bidirectional

        num_edges == [min_edges,max_edges]
        '''
        u = self.u
        GNode.reset_id()
        nodes = {}
        for i in range(num_nodes):
            node = GNode('v.{:03}'.format(i))
            nodes[i] = node
        set_target = set(nodes.keys())
        for i in range(num_nodes):
            src_node = nodes[i]
            src_id = i
            num_edges = u.randint(min_edges,max_edges)
            dst_ids = u.get_random_from_set(set_target, set([src_id]), num_edges)
            for dst_id in dst_ids:
                w = u.randint(min_weight,max_weight)
                src_node.add_edge(dst_id,w)
                dst_node = nodes[dst_id]
                if directed_type == Graph.DType.UNDIRECTED:
                    dst_node.add_edge(src_id,w)
                    pass
                elif directed_type == Graph.DType.MIXED:
                    if u.randint(0,1) == 1:
                        w = u.randint(min_weight,max_weight)
                        dst_node.add_edge(src_id,w)
        return nodes

    def set_graph(self, nodes:dict):    # nodes must be nodes[id] = GNode map
        self.all_nodes = nodes.copy()

    def print_graph_summary(self):
        '''
        print this sort of format:

        id1 id2 id3 id4 id5
          |   |   |   |   |
          |   |   |   |   +-- all outbound ids and weights
          |   |   |   +------ all outbound ids and weights
          |   |   +---------- all outbound ids and weights
          |   +-------------- all outbound ids and weights
          +------------------ all outbound ids and weights
        '''
        p('---- print_graph_summary: num_nodes:{}'.format(len(self.all_nodes)))
        width = 3
        horizontal_line = '---'
        nodes = self.get_all_nodes_map()
        list_node_ids = list(nodes.keys())
        sz_ids = len(list_node_ids)
        buffered_lines = {}
        line = ''
        for id in list_node_ids:
            line += f"{id:{width}} "
        buffered_lines[0] = line
        bar = '|'
        cross = '+'
        line = ''
        for j in range(sz_ids):
            line += f"{bar:>{width}} "
        buffered_lines[1] = line

        for i in range(sz_ids):
            line = ''
            line_num = sz_ids - i + 1
            for j in range(i):
                line += f"{bar:>{width}} "
            line += f"{cross:>{width}}"
            for j in range(sz_ids-i):
                line += f"{horizontal_line}-"
            id = list_node_ids[i]
            node = nodes[id]
            vertices = node.get_vertices()
            buffered_vertices = ''
            is_first = True
            for vertex_id, vertex_weight in vertices.items():
                if is_first:
                    buffered_vertices += '({})'.format(vertex_id)
                    is_first = False
                else:
                    buffered_vertices += ',({})'.format(vertex_id)
            line += '{}'.format(buffered_vertices)
            buffered_lines[line_num] = line
        sorted_lines = sorted(buffered_lines)
        for line_num in sorted_lines:
            #p('{:3}: {}'.format(line_num,buffered_lines[line_num]))
            p('{}'.format(buffered_lines[line_num]))
        p('\n')
        p('\n')
        p('\n')

    def run_prims_mst(self):
        nodes = self.get_all_nodes_map()
        visited_node_ids = set()
        non_visited_node_ids = nodes.keys()
        for node_id,node in nodes.items():
            pass


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

    def tearDown(self) -> None:
        #    p('teardown')
        pass

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
        #p('pass test_increasing_val')

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
        #p('pass testSlidingWindowMax')


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

    def testFindSumInArrayAllSubsets(self):
        '''
        find all subsets in varray that sums to vsum. if none, return none
        vsum,varray
        '''
        pass

    def testFindProductInArrayFirst(self):
        '''
        find first subset in varray that results in product value. if none, return none
        vproduct,varray
        '''

    def testFindProductInArrayAllSubsets(self):
        '''
        find all subset in varray that results in product value. if none, return none
        vproduct,varray
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

        #p('testCombination pass')

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

        #p('testPermutation pass')

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
            hq = ut._HeapQ()
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
            hq = ut._HeapQ(True)
            hq.push(5)
            hq.push(6)
            hq.push(4)
            hq.push(7)
            hq.push(3)
            l = []
            while(hq.size() > 0):
                l.append(hq.pop())
            assert l == [7,6,5,4,3]
            #p('pass heapq t1')

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
        #p('passed test_merge_sort')     # named conflict with pv if it was named p

    def test_trapping_rain_water(self):
        class trap:
            '''
            i   0 1 2 3 4 5 6 7 8 9
            -----------------------
            h   5 7 9 4 6 5 8 3 4 7
            -----------------------

            time    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0
            lptr    0 1
            lmax    0 1
            lstack  -
            rptr    9
            rmax    9
            rstack  -
            total


            '''
            def calculate1(self, l):
                stackl = []
                stackr = []
                len = len(l)

    def test_stack_list(self):
        class stack_ops:
            def get_less_equal_current_left2right(self,l):
                q = [0]
                a = []
                while(len(q) != 0):
                    i = q[-1] + 1
                    if(i >= len(l)): break
                    while(len(q) != 0 and l[q[-1]] <= l[i]):
                        a.append(l[q.pop()])
                    q.append(i)
                return a
            def get_less_equal_current_right2left(self,l):
                q = [len(l)-1]
                a = []
                while(len(q) != 0):
                    i = q[-1] - 1
                    if(i < 0): break
                    while(len(q) != 0 and q[-1] <= l[i]):
                        a.append(l[q.pop()])
                    q.append(i)
                return a
            # local maxes are local peaks, meaning its left <= cur
            def get_local_maxes_left2right(self,l):
                q = [0]
                a = []
                while(len(q) != 0):
                    i = q[-1] + 1
                    if(i >= len(l)): break
                    if(l[i] >= q[-1]):
                        a.append(l[q.pop()])
                return a
            def sum_both_directions(self,l):
                al,ar = [0 for i in range(len(l))],[0 for i in range(len(l))]
                sum = 0
                for i in range(0,len(l),1):
                    sum += l[i]
                    al[i] = sum
                sum = 0
                for i in range(len(l)-1,-1,-1):
                    sum += l[i]
                    ar[i] = sum
                return al,ar
            def sum_both_directions_diff(self,l):
                al,ar = self.sum_both_directions(l)
                a = list(map(lambda x,y: int(math.fabs(x-y)), al,ar))
                return a
            def sum_both_directions_sum(self,l):
                al,ar = self.sum_both_directions(l)
                a = list(map(lambda x,y: x+y, al,ar))
                return a
            def sum_list(self,l):
                a = [l[0]]
                for i in range(1,len(l)):
                    a.append(a[i-1]+l[i])
                return a

        test = stack_ops()

        l = [50,30,60,40,50,20]
        a = test.get_less_equal_current_left2right(l)
        assert a == [30,50,40]

        l = [50,30,60,40,30,70,20]
        a = test.get_less_equal_current_left2right(l)
        assert a == [30,50,30,40,60]

        l = [10,20,30,40]
        a = test.get_less_equal_current_left2right(l)
        assert a == [10,20,30]

        l = [40,30,20,10]
        a = test.get_less_equal_current_left2right(l)
        assert a == []

        l = [1,2,3,4,5]
        al,ar = test.sum_both_directions(l)
        assert al == [ 1, 3, 6,10,15] and \
               ar == [15,14,12, 9, 5]

        a = test.sum_both_directions_diff([1,2,3,4,5])
        assert a == [14,11,6,1,10]

        a = test.sum_both_directions_sum([1,2,3,4,5])
        assert a == [16,17,18,19,20]

        a = test.sum_list([1,2,3,4,5,6,7])
        assert a == [1,3,6,10,15,21,28]
        assert (a[6]-a[2]) == (7+6+5+4)

        #p('pass test_stack_list')

    def test_max_product_subarray(self):
        def max_product_subarray_1(l):
            cmin = 0
            cmax = 0
            res = 0
            for v in l:
                t = min(v,min(cmin*v,cmax*v))
                cmax = max(v,max(cmin*v,cmax*v))
                res = max(res,cmax)
                cmin = t
            return res
        def max_product_subarray_2(l):
            prd = 1
            a = []
            for i in range(l):
                prd *= l[i]
                a.append(prd)
            min = None
            max = None

    def test_longest_consecutive_sequence(self):
        # return index of longest consecutive sequence, eg 5,6,3,4,5,6,3,4,5 -> 3,4,5,6 -> 2
        def longest_consecutive_sequence(l):
            if(len(l) <= 1): return 0
            max = 0
            curi = 0
            for i in range(1,len(l)):
                if((i-curi) > max):
                    max = curi
                if(l[i-1]+1 != l[i]):
                    curi = i
            return max
        def t0():
            assert longest_consecutive_sequence([5]) == 0
            assert longest_consecutive_sequence([5,6,3,4,5,6,3,4,5]) == 2
            assert longest_consecutive_sequence([1,2,3,1,2,3,4,1,2,3,4,5]) == 7
        t0()
        #p('passed test_longest_consecutive_sequence')

    def test_find_all_anagrams_in_string(self):
        def dict_meets_min_criteria(d_exp,d_act):
            if(len(d_exp) != len(d_act)): return False
            for k,v in d_act.items():
                if(k not in d_exp): return False
                if(v < d_exp[k]): return False
            return True
        def find_all_anagrams_in_string(s, pat):
            # return all pairs of starting index,ending index of anagram of pat in string s
            # one way is sliding window and use map to cover all the values in pat
            l = []
            i = 0
            j = 0
            pat_cnt = 0

            d_exp = {}
            # populate the expected map
            for c in pat:
                if c in d_exp:  d_exp[c] += 1
                else:           d_exp[c] = 0
            d = {}
            for c in d:         d[c] = 0
            j = 0
            for i in range(s):
                if s[i] in d:
                    d[s[i]] += 1
                    if(dict_meets_min_criteria(d_exp, d)):
                        l.append([j,i])
                        # now try to reduce window, temporarily remove next matching char from dict
                        # and see if still meet min criteria. keep doing until not meet criteria
                        k = j
                        while(k < i):
                            k += 1
                            # finish code here
            return l
        def t0():
            pass
        t0()

    def test_largest_rectangle_in_histogram(self):
        def largest_rectangle_1(l):
            pass
        def t0():
            pass
        t0()

    def testBinarySearchTreeOperations(self):
        class BSTNode:
            def __init__(self,k:str,v,l=None,r=None):
                self.k = k
                self.v = v
                self.lc = l
                self.rc = r

        class BinarySearchTree:

            def __init__(self):
                self.r = None
                self.allow_overwrite = False
                self.min = None
                self.max = None

            def addVal(self, k:str, v=None):
                n = BSTNode(k,v)
                if k < self.min:        self.min = k
                if k > self.max:        self.max = k
                addNode(n,self.r)

            def addNode(self, n:BSTNode,p:BSTNode=None):
                if self.r is None:
                    assert p is None
                    self.r = n
                elif n.k < p.k:
                    if p.l is None:     p.l = n
                    else:               addNode(n,p.l)
                elif n.k > p.k:
                    if p.r is None:     p.r = n
                    else:               addNode(n,p.r)
                else:
                    assert self.allow_overwrite
                    p.v = n.v           # same key gets overwritten

            def getNode(self, k) -> BSTNode:
                result = self._getNode(k, self.r, '')
                if result is None:      return None
                return result[0]

            # getNodePath returns tuple for node and its current path
            def getNodePath(self, k) -> BSTNode:
                return self._getNode(k, self.r, '')

            def _getNode(self, k:str, n:BSTNode=None, path:str=None) -> BSTNode:
                if n is None:           return None
                path += '/' + n.k
                if k == n.k:            return (n,path)
                if k < n.k:             return _getNode(k,n.l,path)
                return _getNode(k,n.r,path)

            def getNodesByVal(self, v) -> dict:
                return self._getNodesByValFromRange(v,self.min,self.max)

            def getNodesByValFromRange(self,v,min:str,max:str) -> dict:
                results = {}
                self._getNodesByValFromRange(v,min,max,self.r,results,'')
                return results

            def preprocessTuples(self,listTuples:list) -> list:
                results = listTuples
                return results

            '''
            tuple is (v,minkey,maxkey)
            '''
            def getNodesByValFromTuples(self,listTuples:list) -> dict:
                results = {}
                mergedTuples = self.preprocessTuples(listTuples)
                for t in mergedTuples:
                    assert len(t) == 3
                    d = self.getNodesByValFromRange(t[0],t[1],t[2],'')
                    results.update(d)
                return results

            '''
            tuple is (minkey,maxkey)
            '''
            def getNodesByValFromListRange(self,v,listRanges:list) -> dict:
                results = {}
                for p in listRanges:
                    assert isinstance(p,Pair)
                    d = self.getNodesByValFromRange(v,p.v1,p.v2,'')
                    results.update(d)
                return results

            def _getNodesByValFromRanges(self,mapTuples:dict,n:BSTNode,results:dict,path:str):
                pass

            def _getNodesByValFromRange(self,listTuples:list,n:BSTNode,results:dict,path:str):
                '''
                what if you change this to map?
                '''
                if n is None:           return
                path += '/' + n.k
                newTuples = []
                removedTuples = []
                for tuple in listTuples:
                    if tuple.min <= n.k and tuple.max <= max:
                        if tuple.v == v:
                            if path not in results:
                                results[path] = n
                        newTuples.append(tuple)
                    else:
                        removedTuples.append(tuple)
                if len(newTuples) > 0:
                    self._getNodesByValFromRange(newTuples,n.l,results,path)
                    self._getNodesByValFromRange(newTuples,n.r,results,path)


            def _getNodesByValFromRange(self,v,min:str,max:str,n:BSTNode,results:dict,path:str):
                if n is None:           return
                path += '/' + n.k
                if min <= n.k and n.k <= max:
                    if n.v == v:
                        if path in results:
                            return
                        results[path] = n
                if min < n.k:
                    self._getNodesByValFromRange(v,min,max,n.l,results,path)
                if n.k < max:
                    self._getNodesByValFromRange(v,min,max,n.r,results,path)

            def getNodesByValFromStartKeys(self,v,k1:str,k2:str) -> dict:
                t1 = self.getNodePath(k1)
                t2 = self.getNodePath(k2)
                results = {}
                if t1 is not None:
                    self._getNodesByValFromRange(v,self.min,self.max,t1[0],results,t1[1])
                if t2 is not None:
                    self._getNodesByValFromRange(v,self.min,self.max,t2[0],results,t2[1])
                return results
        pass

    def test_stable_match(self):
        class Role(enum.Enum):
            REQUESTER       = 1
            ACKNOWLEDGER    = 2
            MEDIATOR        = 3
        class MatchType(enum.Enum):
            MATCH_PREF      = 1
        class Thing:
            def __init__(self, id: str, role: Role):
                self.id = id
                self.role = role
                self.pref_id = None
                self.pref_list = []
                self.rejected_set = set()
                self.match_id = None
                self.round = 0
        class StableMatch:
            def __init__(self, num_reqs: int, num_acks: int, num_pref_reqs: int, num_pref_acks: int):
                self.reqs = set()
                self.acks = set()
                self.utils = Utils()
                self.pctr = 0
                self.pctr_rounds = 0
                self.num_pref_reqs = num_pref_reqs
                self.num_pref_acks = num_pref_acks
                self.match_map = {}
                self.map = {}
                ctr = 0
                for i in range(num_reqs):
                    id = "name.r.{:02}".format(ctr)
                    t = Thing(id, Role.REQUESTER)
                    self.reqs.add(t)
                    self.map[t.id] = t
                    ctr += 1
                for i in range(num_acks):
                    id = "name.a.{:02}".format(ctr)
                    t = Thing(id, Role.ACKNOWLEDGER)
                    self.acks.add(t)
                    self.map[t.id] = t
                    ctr += 1
                self.make_pref_lists_for_available()
            def make_pref_lists_for_available(self):
                # make a random prioritized preference list for each requester and acknowledger
                reqs = self.get_available_req_set()
                acks = self.get_available_ack_set()
                for t in reqs:
                    t.pref_list = self.utils.get_random_from_set(acks,{t},self.num_pref_reqs,allow_select_resize=True)
                for t in acks:
                    t.pref_list = self.utils.get_random_from_set(reqs,{t},self.num_pref_acks,allow_select_resize=True)
                return
            def get_available_req_set(self) -> set:
                return self.get_available_set(False)
            def get_available_ack_set(self) -> set:
                return self.get_available_set(True)
            def get_available_set(self, is_ack_set: bool) -> set:
                s = set()
                if is_ack_set:
                    s = self.acks
                else:
                    s = self.reqs
                available = set()
                for t in s:
                    if t.match_id is None:
                        available.add(t)
                return available
            def get_num_available(self, is_ack_set: bool) -> int:
                cnt = 0
                s = set()
                if is_ack_set:
                    s = self.acks
                else:
                    s = self.reqs
                for t in s:
                    if t.match_id is None:
                        cnt += 1
                return cnt
            def print_matches(self):
                if(len(self.match_map) == 0):
                    return
                set_visited = set()
                err_list = []
                ctr = 0
                for k,v in self.match_map.items():
                    if k in set_visited:
                        continue
                    #p('{:3}: {} <=> {}'.format(ctr, k,v.id))
                    ctr += 1
                    #assert v.id in self.map
                    if v.match_id != k:
                        err_list.append('k:{} v.id:{} v.match_id:{}'.format(k,v.id,v.match_id))
                    set_visited.add(k)
                    set_visited.add(v.id)
                for err in err_list:
                    p('error: {}'.format(err))
                p("")
            def do_match(self, match_type: MatchType=MatchType.MATCH_PREF):
                self.pctr = 0
                self.pctr_rounds = 0
                if match_type == MatchType.MATCH_PREF:
                    self.do_match_MATCH_PREF()
                self.print_matches()
                #p('num_rounds:{} perf_ctr:{}'.format(self.pctr_rounds, self.pctr))

            def do_match_MATCH_PREF(self):
                num_rounds = self.num_pref_reqs
                reqs = self.get_available_req_set()
                acks = self.get_available_ack_set()
                self.make_pref_lists_for_available()
                for round in range(num_rounds):
                    self.pctr_rounds += 1
                    # for each req, get its round preference, see if it's match with ack's pref.
                    for req in reqs:
                        if round >= len(req.pref_list):
                            continue
                        if req.match_id is not None:
                            continue
                        ack = req.pref_list[round]
                        if ack.match_id is not None:
                            continue
                        # for the ack, if req is preferred from prev->cur rounds, choose the req
                        for i in range(round+1):
                            if req.id == ack.pref_list[i].id:
                                ack.match_id = req.id
                                req.match_id = ack.id
                                self.match_map[req.id] = ack
                                self.match_map[ack.id] = req
                            self.pctr += 1
                # at this point, get all the non-matched and repeat
                num_available_reqs = self.get_num_available(False)
                num_available_acks = self.get_num_available(True)
                if num_available_reqs == 0 or num_available_acks == 0:
                    return
                assert self.pctr < 1_000_000
                assert self.pctr_rounds < 1000
                self.do_match_MATCH_PREF()

        def t0():
            thing1 = Thing('name1', Role.REQUESTER)
            thing2 = Thing('name2', Role.ACKNOWLEDGER)
            assert thing1.id == 'name1'
            assert thing1.role == Role.REQUESTER
            assert thing2.id == 'name2'
            assert thing2.role == Role.ACKNOWLEDGER
        def t1(num_req,num_ack,num_pref):
            algos = StableMatch(num_req,num_ack,num_pref,num_pref)
            algos.do_match()
            #p('num_reqs: {} num_acks: {} num_rounds: {} perfctr: {}'
            #  .format(len(algos.reqs), len(algos.acks), algos.pctr_rounds, algos.pctr))
        #p('----------')
        t1(20,20,3)
        #p('----------')
        t1(20,20,10)
        #p('----------')
        t1(20,20,20)

    def test_interleave_with_errors(self):
        myutils = utils.myutils.my_utils()
        charset = 'abcdef'
        def do_interleave(s1,s2):
            s3 = ''
            i = 0
            j = 0
            while i < len(s1) or j < len(s2):
                if i < len(s1) and j < len(s2):
                    if bool(random.getrandbits(1)):
                        s3 += s1[i]
                        i += 1
                    else:
                        s3 += s2[j]
                        j += 1
                elif i < len(s1):
                    s3 += s1[i]
                    i += 1
                elif j < len(s2):
                    s3 += s2[j]
                    j += 1
            return s3

        '''
        inject n from charset into string s
        '''
        def inject_rand_chars(s,charset,num):
            rand_str = myutils.rand_str(num,charset)
            set_positions = set(myutils.rand_list(0,len(s),num,False))
            result = ''
            j = 0
            for i in range(len(s)):
                if i in set_positions:
                    result += rand_str[j]
                    j += 1
                result += s[i]
            return result

        def is_interleave_with_errors_iterative(s1,s2,s3):
            if (len(s1)+len(s2) < len(s3)) or (len(s1)+len(s2) > len(s3 + 2)):
                return False
            dp = {(0,0):True}
            for i in range(len(s1)+1):
                for j in range(len(s2)+1):
                    if i != 0 and j != 0:
                        dp[(i,j)] = False
                    if i > 0 and dp.get((i-1,j), False) and (s1[i-1] == s3[i+j-1] or s1[i-1] == s3[i+j] or s1[i-1] == s3[i+j+1]):
                        dp[(i,j)] = True
                    if j > 0 and dp.get((i,j-1), False) and (s2[j-1] == s3[i+j-1] or s2[j-1] == s3[i+j] or s2[j-1] == s3[i+j+1]):
                        dp[(i,j)] = True
            return dp[(len(s1), len(s2))]

        def is_interleave_with_no_errors(s1,s2,s3):
            def is_interleave_1(s1,s2,s3,i1,i2,i3):
                if(i1 == len(s1) and i2 == len(s2) and i3 == len(s3)):
                    return True
                result = False
                if(i1 < len(s1) and s1[i1] == s3[i3]):
                    result |= is_interleave_1(s1,s2,s3,i1+1,i2,i3+1)
                if(i2 < len(s2) and s2[i2] == s3[i3]):
                    result |= is_interleave_1(s1,s2,s3,i1,i2+1,i3+1)
                return result
            return is_interleave_1(s1,s2,s3,0,0,0)

        def reference_is_interleave_with_errors_recursive(s1,s2,s3,max_num_errors):
            def is_interleave_with_errors_indexed(s1,s2,s3,i1,i2,i3,memo,num_errors,max_num_errors):
                if (i1,i2) in memo:
                    return memo[(i1,i2)]
                if i1 == len(s1) and i2 == len(s2) and i3 == len(s3):
                    return num_errors < max_num_errors
                if i3 == len(s3):
                    return False
                result = False
                if i1 < len(s1) and s1[i1] == s3[i3]:
                    result |= is_interleave_with_errors_indexed(s1,s2,s3,i1+1,i2,i3+1,memo,num_errors,max_num_errors)
                if i2 < len(s2) and s2[i2] == s3[i3]:
                    result |= is_interleave_with_errors_indexed(s1,s2,s3,i1,i2+1,i3+1,memo,num_errors,max_num_errors)
                if not result:
                    result |= is_interleave_with_errors_indexed(s1,s2,s3,i1,i2,i3+1,memo,num_errors+1,max_num_errors)
                memo[(i1,i2)] = result
                return result

            def is_interleave_with_errors_sliced(s1,s2,s3,memo,num_errors,max_num_errors):
                if s1 == s2 == s3:
                    return True
                if (i1,i2) in memo:
                    return memo[(i1,i2)]
                if i1 == len(s1) and i2 == len(s2) and i3 == len(s3):
                    return num_errors < max_num_errors
                if i3 == len(s3):
                    return False
                result = False
                if i1 < len(s1) and s1[i1] == s3[i3]:
                    result |= is_interleave_with_errors_sliced(s1[1:],s2,s3[1:],memo,num_errors,max_num_errors)
                if i2 < len(s2) and s2[i2] == s3[i3]:
                    result |= is_interleave_with_errors_sliced(s1,s2[1:],s3[1:],memo,num_errors,max_num_errors)
                if not result:
                    result |= is_interleave_with_errors_sliced(s1,s2,s3[1:],memo,num_errors+1,max_num_errors)
                memo[(i1,i2)] = result
                return result

            memo = {}
            return is_interleave_with_errors_indexed(s1,s2,s3,0,0,0,memo,0,max_num_errors)

        def t0():
            for i in range(1000):
                s1 = myutils.rand_str(20,charset)
                s2 = myutils.rand_str(20,charset)
                s3 = do_interleave(s1,s2)
                num_errors = myutils.rand(0,3)
                s3_errors = inject_rand_chars(s3,charset,num_errors)
                result = is_interleave_with_errors_iterative(s1,s2,s3_errors)
                if not result:
                    p('not work: {},{}={:10} (original:{})'.format(s1,s2,s3_errors,s3))
                else:
                    continue
                    p('yes work: {},{}={:10} (original:{})'.format(s1,s2,s3_errors,s3))

            p('pass')
        def t_negative_cases():
            for i in range(100):
                s1 = myutils.rand_str(20,charset)
                s2 = myutils.rand_str(20,charset)
                s2_shuffled = myutils.shuffle_string(s2)
                s3 = do_interleave(s1,s2_shuffled)
                num_errors = myutils.rand(0,1)
                num_errors = 0
                s3_errors = inject_rand_chars(s3,charset,num_errors)
                result = is_interleave_with_errors_iterative(s1,s2,s3_errors)
                if not result:
                    #p('not work: {},{}={:10} (original:{})'.format(s1,s2,s3_errors,s3))
                    pass
                else:
                    continue
                    p('yes work: {},{}={:10} (original:{})'.format(s1,s2,s3_errors,s3))

            p('pass')
        def test_no_errors():
            for i in range(100):
                s1 = myutils.rand_str(4,charset)
                s2 = myutils.rand_str(4,charset)
                s3 = do_interleave(s1,s2)
                result = is_interleave_with_no_errors(s1,s2,s3)
                if not result:
                    p('not work: {},{}={:10}'.format(s1,s2,s3))
                else:
                    continue
                    p('yes work: {},{}={:10}'.format(s1,s2,s3))

            p('pass')
        test_no_errors()
        #t_negative_cases()

    def print_matrix(self, matrix, colx, rowy):
        sz_box = len(colx) + 1
        # print by row
        for i in range(colx):
            for j in range(rowy):
                pass

    def test_longest_common_subsequence(self):
        def t0():
            '''
            s1 feddcbedcafhfgghefcijab
            s2 aefgdbecfgdchfeibjhe

                f e d d c b e d c a f h f g g h e f c i j a b
            a                     1                       1
            e     1                             2
            f   1                   2   2         3
            g                             3 3
            d       2 2       2
            b
            e
            c
            f
            g
            d
            c
            h
            f
            e
            i
            b
            j
            h
            e

            basically when there is match, increment from max of [i-1,j],[i-1,j-1],[i,j-1]
            this value propagates all the way to the end of each row, and eventually
            the last col of last row
            '''
            pass
        t0()

    def test_longest_common_substring(self):
        '''
        k common substring
        generalized suffix tree
        dynamic programming O(mn)
        '''

        def dp(s1:str,s2:str) -> typing.Tuple[int,int]: # return of s1 indices beg and end
            idx_max_beg = 0
            idx_max_end = 0
            idx_cur_beg = 0
            idx_cur_end = 0
            sz1 = len(s1)
            sz2 = len(s2)
            for i in range(sz1):
                for j in range(sz2):
                    if s1[i] == s2[j]:
                        pass
                    else:
                        pass
            return None

        def brute(s1:str,s2:str) -> tuple: # return of s1 indices beg and end
            idx_max_beg = None
            idx_max_end = None
            idx_cur_beg = None
            idx_cur_end = None
            s1i = None
            s1j = None
            s2i = None
            s2j = None
            sz1 = len(s1)
            sz2 = len(s2)
            for i in range(sz1):
                for j in range(sz2):
                    if s1[i] == s2[j]:
                        idx_cur_beg = j
                        idx_cur_end = j
                    else:
                        idx_cur_beg = None
                        idx_cur_end = None
            return (idx_max_beg,idx_max_end)

        def t0():
            '''
                longest common substring

                a b c a b c d d e f g a b c d e f g a b c
            d   0 0 0 0 0 0 1 1 0 0 0 0 0 0 1
            e   0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 2
            f   0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 3
            g   0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 4
            h
            i
            a   1 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1
            b   0 2 0 0 2 0 0 0 0 0 0 0 2 0 0 0 0 0 0 2
            c   0 0 3 0 0 3 0 0 0 0 0 0 0 3 0 0 0 0 0 0 3
            b   0 1 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1
            c       2     2               2             2
            d               3 1             3
            e                   2             4
            f                     3             5
            g                       4             6
            h
            a   1     1               1             1
            b     2     2               2             2
            c       3     3               3             3

            '''
            s1 = 'abcabcddefgabcdefgabc'
            s2 = 'defghiabcbcdefghabc'
            (s1i,s2i) = brute(s1,s2)
            #assert s3 == 'cdefgh'
            pass

        t0()

    def test_suffix_tree(self):
        '''
        Node,SuffixTree
            this implementation has char->node mapping, which can lead to false positives
        NodeMultiSet,SuffixTreeMultiSet:
            this implementation has char->set of nodes, which should not lead to false positives,
            but leads to long runtimes
        '''
        class NodeMultiSet:
            ID = 0
            def __init__(self, v=None):
                self._id = Node.ID
                self._v = v
                self._c = {}
                Node.ID += 1
            def get_v(self):
                return self._v
            def get_children_multiset(self) -> dict:
                return self._c
            def get_children_of_key(self,key) -> set:
                children = self.get_children_multiset()
                if key not in children:
                    return None
                set_children = children[key]
                return set_children
            def add_child(self,key,child):
                children = self.get_children()
                if key not in children:
                    children[key] = set()
                children_of_key = children[key]
                children_of_key.add(child)
            def reset(self):
                self._v = None
                self._c = {}
        class Node:
            ID = 0
            def __init__(self, v=None):
                self._id = Node.ID
                self._v = v
                self._c = {}
                Node.ID += 1
                self._indices = set()
            def get_v(self):
                return self._v
            def set_v(self, v):
                self._v = v
            def add_index(self, idx):
                self._indices.add(idx)
            def is_in_index(self, idx):
                return idx in self._indices
            def get_indices(self) -> set:
                result = self._indices.copy()
                return result
            def get_children(self) -> dict:
                return self._c
            def get_children_vals(self) -> list:
                l = []
                for c,child in self._c.items():
                    l.append(c)
                return l
            def set_child(self,key,child):
                children = self.get_children()
                children[key] = child
            def reset(self):
                self._v = None
                self._c = {}
                self._indices = set()
            def get_node_summary(self):
                s = ''
                for k,child in self._c.items():
                    v = child._v
                    if v is None:
                        v = ' '
                    if s == '':
                        s = '(id,v):({:2},{}) '.format(child._id,v)
                    else:
                        s = '{}; (id,v):({:2},{})'.format(s,child._id,v)
                v = self._v
                if v is None:
                    v = ' '
                s = ('SUMMARY: id:{:2}; v:{}; children:{}'.format(self._id,v,s))
                return s
        class SuffixTreeMultiSet:
            def __init__(self):
                self.r = Node()
            def get_root(self) -> Node:
                return self.r
            def clear(self):
                self.r = None
            def make_suffix_tree(self,s:str,parent:Node=None):
                if s is None or len(s) == 0:
                    return
                pass
            def is_substring(self,s:str,n:Node=None) -> bool:
                if s is None or len(s) == 0:
                    return False;
                if n is None:
                    n = self.get_root()
                pass
        class SuffixTree:
            def __init__(self):
                self.r = Node()
            def get_root(self) -> Node:
                return self.r
            def clear(self):
                self.r = None
            def make_suffix_tree(self,s:str,parent:Node=None):
                if s is None or len(s) == 0:
                    return
                c = s[0]
                root = self.get_root()
                if parent is None:
                    parent = root
                root_children = root.get_children()
                if c not in root_children:
                    root_children[c] = Node(c)
                child = root_children[c]
                parent_children = parent.get_children()
                if c not in parent_children:
                    parent_children[c] = child
                p('s: {:20} parent: {}; root: {}'.format(s,parent.get_node_summary(),root.get_node_summary()))
                self.make_suffix_tree(s[1:],child)
            def is_substring(self,s:str,n:Node=None) -> bool:
                if s is None or len(s) == 0:
                    return False;
                if n is None:
                    n = self.get_root()
                c = s[0]
                if c not in n._c:
                    return False
                child = n._c[c]
                s = s[1:]
                if len(s) == 0:
                    return True
                return self.is_substring(s,child)
            def make_suffix_tree_indexed(self,s:str,i:int=0,parent:Node=None):
                if s is None or i >= len(s):
                    return
                c = s[i]
                root = self.get_root()
                if parent is None:
                    parent = root
                root_children = root.get_children()
                if c not in root_children:
                    root_children[c] = Node(c)
                child = root_children[c]
                child.add_index(i)
                parent_children = parent.get_children()
                if c not in parent_children:
                    parent_children[c] = child
                #p('s: {:20} parent: {}; root: {}'.format(s,parent.get_node_summary(),root.get_node_summary()))
                self.make_suffix_tree_indexed(s,i+1,child)
            def is_substring_indexed(self,s:str,i:int=0,offset:int=0,n:Node=None) -> bool:
                if s is None or i >= len(s):
                    return False
                if n is None:
                    n = self.get_root()
                c = s[i]
                children = n.get_children()
                if c not in children:
                    return False
                child = children[c]
                # if first iteration, go through all indices of the starting character (0)
                # else continue only with the given path. do not branch to all indices
                if(i == 0):
                    indices = child.get_indices()
                    for index in indices:
                        match = self.is_substring_indexed(s,i+1,index,child)
                        if match:
                            return True
                    return False
                else:
                    if not child.is_in_index(i+offset):
                        return False
                    if (i+1) == len(s):
                        return True
                    return self.is_substring_indexed(s,i+1,offset,child)
            def is_substring_indexed_1(self,s:str,i:int=0,indices:set=None,n:Node=None) -> bool:
                if s is None or i >= len(s):
                    return False
                if n is None:
                    n = self.get_root()
                c = s[i]
                children = n.get_children()
                if c not in children:
                    return False
                child = children[c]
                # if first iteration, go through all indices of the starting character (0)
                # else continue only with the given path. do not branch to all indices
                if(i == 0):
                    indices = child.get_indices() # this is a copy
                    return self.is_substring_indexed_1(s,i+1,indices,child)
                else:
                    indices_to_remove = set()
                    for index in indices:
                        if not child.is_in_index(index + i):
                            indices_to_remove.add(index)
                    for index in indices_to_remove:
                        indices.remove(index)
                    if len(indices) == 0:
                        return False
                    if (i+1) == len(s):
                        return True
                    return self.is_substring_indexed_1(s,i+1,indices,child)
            def get_all_suffixes(self,s:str):
                '''
                this runs into:
                circular traversal/no termination
                '''
                pass
        def t0():
            s = 'abcdefghijklmnopqrstuvwxyz0123456789'
            stree = SuffixTree()
            stree.make_suffix_tree(s)
            assert stree.is_substring('bcb') == False
            assert stree.is_substring('hijl') == False
            assert stree.is_substring('hijkl') == True
            assert stree.is_substring('abd') == False
            assert stree.is_substring('abc') == True
            assert stree.is_substring('789') == True
        def t1():
            s = 'abracadabra'
            stree = SuffixTree()
            stree.make_suffix_tree(s)
            assert stree.is_substring('cadabr') == True
            assert stree.is_substring('belly') == False
            assert stree.is_substring('cadabro') == False
        def t3():
            stree = SuffixTree()
            stree.make_suffix_tree('abracadabra')
            stree.make_suffix_tree('this is a general suffix tree implementation')
        def t4():
            s = 'caberacadabro'
            stree = SuffixTree()
            stree.make_suffix_tree(s)
            assert stree.is_substring('abro') == True
            assert stree.is_substring('aber') == True
            assert stree.is_substring('abero') == True # false positive
        def t5():
            s = 'abacacbc'
            stree = SuffixTree()
            stree.make_suffix_tree(s)
            assert stree.is_substring('cabc') == True
            assert stree.is_substring('abac') == True
            assert stree.is_substring('abca') == True # false positive
        def t6():
            r = Node()
            na = Node('a')
            nb = Node('b')
            nc = Node('c')
            children = r.get_children()
            children['a'] = na
            children = r.get_children()
            children['b'] = nb
            children = r.get_children()
            children['c'] = nc
            children = r.get_children()
            assert len(children) == 3
        def t7():
            #     .   . . .
            #    0000000000111
            #    0123456789012
            s = 'caberacadabro'
            stree = SuffixTree()
            stree.make_suffix_tree_indexed(s)
            assert stree.is_substring_indexed('abro') == True
            assert stree.is_substring_indexed('aber') == True
            assert stree.is_substring_indexed('abero') == False
            assert stree.is_substring_indexed('abra') == False
            pass
        def t8():
            #     .   . . .
            #    0000000000111
            #    0123456789012
            s = 'caberacadabro'
            stree = SuffixTree()
            stree.make_suffix_tree_indexed(s)
            assert stree.is_substring_indexed_1('abro') == True
            assert stree.is_substring_indexed_1('aber') == True
            assert stree.is_substring_indexed_1('abero') == False
            assert stree.is_substring_indexed_1('abra') == False
            assert stree.is_substring_indexed_1('cadob') == False
            pass
        #t0()
        t8()

    def test_needleman_wunsch(self):
        '''
        edit distances with scoring preference to obtain highest scoring sequence
        '''
        pass

    def test_edit_distance(self):
        def edit_distance(s1,s2):
            # this needs to be verified, not verified
            sz_s1 = len(s1)
            sz_s2 = len(s2)
            d = [[0 for j in range(sz_s2)] for i in range(sz_s1)]
            for i in range(sz_s1):
                for j in range(sz_s2):
                    cost = 0
                    if s1[i-1] != s2[j-1]:
                        cost = 1
                    d[i][j] = min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+cost)
            min_distance = d[sz_s1-1][sz_s2-1]
            return min_distance

        def t0():
            '''
                k i t t e n
            s   1 2 3 4 5 6
            i   2 1 2 3 4 5
            t   3 2 1 2 3 4
            t   4 3 2 1
            i
            n
            g

                k i t t e n
            k
            i
            t
            e
            r

            '''
            pass
        pass

    def test_kmp_algos(self):
        pass

    def test_boyer_moore_algos(self):
        pass

    def test_raita_algos(self):
        pass

    def test_stack(self):
        pass

    def test_skip_grams(self):
        pass

    def test_n_grams(self):
        '''
        all possible substrings of length N that are contained in string
        1-gram
        2-gram
        3-gram
        4-gram
        5-gram
        '''
        pass

    def test_bayes_theorem_examples(self):
        '''
        P(A|B) = P(B|A)P(A)/P(B)

        '''
        pass

    def test_combinatorics_permutations_and_combinations(self):
        '''
        permutation:
            k permutations of n: n!/(n-k)!
            permutation with repetition: k^n
            permutation with multiset: n!/(m1!m2!m3!)
        combination
            n!/(k!(n-k)!)
        multiset:
            (n+k-1)!/(k!(n-1)!)     eg combos with 2,2,2,3,3,4,4

            permutation multiset:
                if n is total items and mX num of each type
                (n!)/(m1!m2!m3!)
                    1,1,2,2,3,3
                    5!/(2!2!2!) = 120/8=15
                    6!/(2!2!2!) = 720/8=90

            combination multiset:
                if n is num of types of items (not the number of items in each type) and choose k
                (n+k-1)!/(k!(n-1)!)
                    1,1,2,2,3,3
                    (3+3-1)!/(3!2!) = 5!/(3!2!) = 10
        '''
        def string_to_multiset_map(s:str) -> dict:
            d = {}
            for c in s:
                if c not in d:
                    d[c] = 0
                d[c] += 1
            return d
        def get_all_permutations_multiset(s:str,sz:int) -> dict:
            multiset_map = string_to_multiset_map(s)
            permutations = {}
            get_all_permutations_multiset_(multiset_map,sz,'',permutations)
            return permutations
        def get_all_permutations_multiset_(multiset_map:dict,sz:int,tmp_str:str,permutations:dict):
            sz_tmp = len(tmp_str)
            if sz_tmp != 0:
                if sz_tmp not in permutations:
                    permutations[sz_tmp] = []
                permutations[sz_tmp].append(tmp_str)
            if sz_tmp == sz:
                return
            for k in multiset_map.keys():
                v = multiset_map[k]
                if v != 0:
                    multiset_map[k] -= 1
                    get_all_permutations_multiset_(multiset_map,sz,tmp_str+k,permutations)
                    multiset_map[k] += 1
        def get_all_combinations_multiset(s:str,sz:int) -> dict:
            multiset_map = string_to_multiset_map(s)
            combinations = {}
            key_list = list(multiset_map.keys())
            get_all_combinations_multiset_(multiset_map,key_list,0,sz,'',combinations)
            return combinations
        def get_all_combinations_multiset_(multiset_map:dict,key_list:list,idx:int,sz:int,tmp_str:str,combinations:dict) -> dict:
            sz_tmp = len(tmp_str)
            if sz_tmp != 0:
                if sz_tmp not in combinations:
                    combinations[sz_tmp] = []
                combinations[sz_tmp].append(tmp_str)
            if sz_tmp == sz:
                return
            for i in range(idx,len(key_list)):
                key = key_list[i]
                count = multiset_map[key]
                new_str = tmp_str
                for j in range(count):
                    new_str = new_str + key
                    get_all_combinations_multiset_(multiset_map,key_list,i+1,sz,new_str,combinations)

        def get_all_permutations(s:str,sz:int) -> dict:
            permutations = {}
            visited = set()
            get_all_permutations_(s,sz,'',visited,permutations)
            return permutations
        def get_all_permutations_(s:str,sz:int,tmp_string:str,visited:set,permutations:dict):
            sz_tmp = len(tmp_string)
            if sz_tmp != 0:
                if sz_tmp not in permutations:
                    permutations[sz_tmp] = []
                permutations[sz_tmp].append(tmp_string)
            if sz_tmp == sz:
                return
            for j in range(len(s)):
                if j not in visited:
                    visited.add(j)
                    get_all_permutations_(s,sz,tmp_string+s[j],visited,permutations)
                    visited.remove(j)
        def get_all_combinations(s:str,sz:int) -> set:
            combinations = {}
            get_all_combinations_(s,sz,'',0,combinations)
            return combinations
        def get_all_combinations_(s:str,sz:int,tmp_string:str,i:int,combinations:dict):
            sz_tmp = len(tmp_string)
            if sz_tmp != 0:
                if sz_tmp not in combinations:
                    combinations[sz_tmp] = []
                combinations[sz_tmp].append(tmp_string)
            if i >= len(s) or sz_tmp >= sz:
                return
            for j in range(i,len(s),1):
                get_all_combinations_(s,sz,tmp_string+s[j],j+1,combinations)
            pass
        def print_map_of_list_stats(d:dict):
            for k,l in d.items():
                p('numchar: {:3}: {}'.format(k,l))
                sorted_str_map = {}
                for v in l:
                    vsorted = ''.join(sorted(v))
                    if vsorted not in sorted_str_map:
                        sorted_str_map[vsorted] = []
                    sorted_str_map[vsorted].append(v)
                for vsorted,sublist in sorted_str_map.items():
                    p('vsorted key:{} vals:{}'.format(vsorted,sublist))
        def t0():
            s = '12345'
            results = get_all_combinations(s,len(s))
            #p('combinations\n')
            for k,l in results.items():
                l = sorted(l)
                setv = set(l)
                setv = sorted(setv)
                #p('list: {:2}: num_entries: {:4}  {}'.format(k,len(l),l))
                #p('set:  {:2}: num_entries: {:4}  {}'.format(k,len(setv),setv))
                assert l == setv
            #p('\npermutations\n')
            results = get_all_permutations(s,len(s))
            for k,l in results.items():
                l = sorted(l)
                setv = set(l)
                setv = sorted(setv)
                #p('list: {:2}: num_entries: {:4}  {}'.format(k,len(l),l))
                #p('set:  {:2}: num_entries: {:4}  {}'.format(k,len(setv),setv))
                assert l == setv
            #p('\n')
        def t1():
            # multiset
            s = '112233'
            results = get_all_combinations_multiset(s,len(s))
            #p('combinations multiset\n')
            for k,l in results.items():
                l = sorted(l)
                setv = set(l)
                setv = sorted(setv)
                #p('list: {:2}: num_entries: {:4}  {}'.format(k,len(l),l))
                #p('set:  {:2}: num_entries: {:4}  {}'.format(k,len(setv),setv))
                assert l == setv
            #print_map_of_list_stats(results)
            #p('\npermutations multiset\n')
            results = get_all_permutations_multiset(s,len(s))
            for k,l in results.items():
                l = sorted(l)
                setv = set(l)
                setv = sorted(setv)
                #p('list: {:2}: num_entries: {:4}  {}'.format(k,len(l),l))
                #p('set:  {:2}: num_entries: {:4}  {}'.format(k,len(setv),setv))
                assert l == setv
            #print_map_of_list_stats(results)
            p('\n')
        t0()
        t1()

    def test_fibonacci_heap(self):
        pass

    def test_tries(self):
        pass

    def test_k_d_tree(self):
        pass

    def test_make_random_words(self):
        l = []
        for i in range(100):
            l.append(utils.myutils.my_utils.make_random_word(3))
        '''
        for n in l:
            p(n)
        '''
    def test_graph_make_graph(self):
        g = Graph()
        d = g.make_random_graph(7,Graph.DType.DIRECTED, 1,4,1,1)
        g.set_graph(d)
        g.print_graph_summary()

    def test_graph_min_spanning_tree(self):
        pass

    def test_count_dfs(self):
        class CTR:
            def __init__(self):
                self.ctr = 0
        def loop_3_var(i,j,k,imax,jmax,kmax,ctr):
            if i < imax:
                loop_3_var(i+1,j,k,imax,jmax,kmax,ctr)
            if j < jmax:
                loop_3_var(i,j+1,k,imax,jmax,kmax,ctr)
            #if k < kmax:
            #    loop_3_var(i,j,k+1,imax,jmax,kmax,ctr)
            p('{}:{}'.format(i,j))
            ctr.ctr += 1
        def loop_2_var_if_else(i,j,imax,jmax,ctr):
            if i >= imax and j >= jmax:
                return
            if i < imax:
                loop_2_var_if_else(i+1,j,imax,jmax,ctr)
            elif j < jmax:
                loop_2_var_if_else(i,j+1,imax,jmax,ctr)
            p('{}:{}'.format(i,j))
            ctr.ctr += 1
        def loop_2_var(i,j,imax,jmax,ctr):
            if (i + j) == (imax + jmax):
                return
            if i >= imax and j >= jmax:
                return
            if i < imax:
                loop_2_var(i+1,j,imax,jmax,ctr)
            if j < jmax:
                loop_2_var(i,j+1,imax,jmax,ctr)
            ctr.ctr += 1
        def t0():
            ctr = CTR()
            assert ctr.ctr == 0
            loop_3_var(0,0,0,5,5,5,ctr)
            assert 10 == 10
        def t1():
            ctr = CTR()
            loop_2_var_if_else(0,0,5,5,ctr)
            assert ctr.ctr == 10
        def t2():
            ctr = CTR()
            loop_2_var(0,0,5,5,ctr)
            assert ctr.ctr == 671
        t2()

    def test_print_cards(self):
        '''
        organize the cards of 5 based on:
        - sum value of 5 cards
        - is same suit
        - is sequenced
        - is 3 of one value and 2 of another value
        - is 4 of one value
        - is same suit and sequenced

        C(x,y) = x!/y!(x-y)!
        P(x,y) = x!/(x-y)!
        card odds:
        C(x,y) is combination(x,y), not permutation(x,y)
        royal flush: C(4,1) = 4
        straight flush (exclude royal flush): C(10,1)C(4,1) - C(4,1)
            1,2,3,4,5,6,7,8,9,10,J,Q,K
                    1 2 3 4 5  6 7 8 9
            1-5,2-6,3-7,4-8,5-9,6-10,7-J,8-Q,9-K
            it is not C(9,1)C(4,1) because you eliminate any of 1-5,2-6,etc, include 10,J,Q,K,1
        four of a kind: C(13,1)C(12,1)C(4,1)
        full house: (C(4,3)C(13,1))(C(4,2)C(12,1))
        flush (exclude royal and straight): C(13,5)C(4,1) - C(10,1)C(4,1)
        straight (exclude royal and straight flush): POW(C(4,1),5)C(10,1) - C(4,1)C(10,1)
        three of a kind: C(4,3)C(13,1)POW(C(4,1),2)C(12,2)
        two pair: POW(C(4,2),2)C(13,2)C(4,1)C(11,1)
        one pair: C(4,2)C(13,1)POW(C(4,1),3)C(12,3)
        no pair: (C(13,5)-10)(POW(C(4,1),5)-4)
                (13!/5!(13-5)!-10)(POW((4!/3!),5)-4)
                (13*12*11*10*9/120 - 10)(4*4*4*4*4-5) = (1287-10)(1024-4) = 1277*1020
        total: C(52,5) = 2,598,960
        '''
        class Card:
            def __init__(self,val,suit):
                self.val = val
                self.suit = suit
        num_decks = 2
        d = {}

    def test_choose(self):
        '''
        test choose(n,k) = n!/(n-k)!   == permutation
        with repetition is k^n
        with multiset is: n!/(m1!m2!m3!) where m1,m2,m3 is number of types of m1,m2,m3
        '''
        def choose_math(n,k):
            num = math.factorial(n)
            den = math.factorial(n-k)
            res = num/den
            return res
        def choose_loop(n,k):
            num = 1
            for i in range(n,0,-1): # [n,0)
                num *= i
            den = 1
            for i in range(n-k,0,-1): # [n-k,0)
                den *= i
            res = num/den
            return res
        def choose(n,k) -> int:
            v = choose_math(n,k)
            return v
    def main(self):
        p('main passed')

if __name__ == "__main__":
    unittest.main() # not ut.main()!

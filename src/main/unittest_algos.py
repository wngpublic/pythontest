import unittest
import queue
import heapq
import math
import collections
import enum
import time
import random
import utils.myutils
import typing
import logging
import json
import hashlib
import struct
import binascii
import numpy
import random
import scipy
import copy
#from __future__ import annotations

'''
python3 -m unittest unittests.ut.test_list
or
python3 unittest_algos.py ut.test_list
or alias pythonut ut.test_something 
pythonut unittest_algos.ut.main
where pythonut='python3 -m unittest'

pythonut unittest_algos.ut.main

python -m unittest unittest_algos.ut.test_<methodname>

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
        if isinstance(s,list):
            print(s)
        elif isinstance(s,set):
            print(s)
        elif isinstance(s,dict):
            print(s)
        else:
            print(s)

def print_array(s,is_double_space=False):
    sz_s = len(s)
    numbers = []
    result = sz_s
    while result != 0:
        remainder = int(result % 10)
        numbers.append(remainder)
        result -= remainder
        result = int(result/10)
    numbers.reverse()
    starting_ten = 10**(len(numbers)-1)
    buf = []
    for i in range(len(numbers)):
        buf.append([])
        print_v = 0
        ctr = 0
        for j in range(sz_s):
            if j != 0 and j % starting_ten == 0:
                print_v = (print_v + 1) % 10
            buf[i].append(str(print_v))
        starting_ten = int(starting_ten/10)
    l = []
    for i in range(sz_s):
        l.append('-')
    buf.append(l)
    buf.append(s)
    debug = True
    if debug:
        for line in buf:
            if is_double_space:
                p(' '.join(line))
            else:
                p(''.join(line))

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
                self.swap(result, i, random.randint(0,sz-1))
        return result
    def rand_str(self, num:int, charset:str=None) -> str:
        if charset is None:
            charset = self.charset_alphanum
        sz = len(charset)-1
        l_idx = self.rand_list(0,sz,num,True)
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
        #sz = max - min + 1
        #assert num < sz
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
                        s.add(v)
                        break
        if not allow_repetition:
            assert len(s) == num
            l = list(s)
        return l
class Pair:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

class Container:
    def __init__(self,obj=None):
        self.obj = obj
    def get(self):
        return self.obj
    def set(self,obj):
        self.obj = obj

class LLN:
    ID = 0
    def __init__(self,v = None, pp = None, np = None, lp=None, rp=None, parentp=None, lo=None, hi=None, min=None, max=None):
        self.v = v
        self.np = np
        self.pp = pp
        self.lp = lp
        self.rp = rp
        self.parentp = parentp
        self.lo = lo
        self.hi = hi
        self.min = min
        self.max = max
        self.id = LLN.ID
        LLN.ID += 1
    def get_id(self):
        return self.id
    def set_lo(self,lo):
        self.lo = lo
        return self
    def set_hi(self,hi):
        self.hi = hi
        return self
    def set_max(self,max):
        self.max = max
        return self
    def set_min(self,min):
        self.min = min
        return self
    def set_lp(self,lp):
        self.lp = lp
        return self
    def set_rp(self,rp):
        self.rp = rp
        return self
    def set_np(self,np):
        self.np = np
        return self
    def set_pp(self,pp):
        self.pp = pp
        return self
    def set_v(self,v):
        self.v = v
        return self
    def get_lo(self):
        return self.lo
    def get_hi(self):
        return self.hi
    def get_max(self):
        return self.max
    def get_min(self):
        return self.min
    def get_lp(self):
        return self.lp
    def get_rp(self):
        return self.rp
    def get_np(self):
        return self.np
    def get_pp(self):
        return self.pp
    def get_v(self):
        return self.v
    def print_vals(self,id=False,v=False,lo=False,hi=False,min=False,max=False):
        s = self.get_print_vals(id,v,lo,hi,min,max)
        print(s)
    def get_print_vals(self,id=False,v=False,lo=False,hi=False,min=False,max=False):
        s = '{'
        populated = False
        if id:
            s += 'id:{}'.format(self.id)
            populated = True
        if v:
            s = s + (',' if populated else '') + 'v:{}'.format(self.v)
            populated = True
        if lo:
            s = s + (',' if populated else '') + 'lo:{}'.format(self.lo)
            populated = True
        if hi:
            s = s + (',' if populated else '') + 'hi:{}'.format(self.hi)
            populated = True
        if min:
            s = s + (',' if populated else '') + 'min:{}'.format(self.min)
            populated = True
        if max:
            s = s + (',' if populated else '') + 'max:{}'.format(self.max)
            populated = True
        s += '}'
        return s

    @staticmethod
    def convert_num_2_lln(v): # -> LLN: cannot return self type in 3.6
        h = LLN()
        n = h
        t = v
        while t != 0:
            m = t % 10
            n.set_v(m)
            t = int((t - m)/10)
            if t != 0:
                newN = LLN()
                n.set_np(newN)
                n = newN
        return h
    @staticmethod
    def convert_lln_2_num(n) -> int:
        t = n
        s = 0
        b10 = 1
        while t != None:
            v = t.get_v() * b10
            s += v
            b10 = b10 * 10
            t = t.get_np()
        return s
    @staticmethod
    def reverse_lln(n): # -> LLN: cannot return self type in 3.6
        '''
        a->b->c->d
        d->c->b->a

        a->b
        a->N
        t = b->n
        b->a
        '''
        tmp = n
        pp = None
        while tmp != None:
            np = tmp.get_np()
            tmp.set_np(pp)
            pp = tmp
            tmp = np
        return pp


class IntervalTree:
    '''
    i:lo/hi input lo/hi
    n:lo/hi node  lo/hi

    -   no merge
                      ilo------ihi
        nlo------nhi
    -   merge candidate
                 ilo------ihi
        nlo------nhi
    -   merge candidate
            ilo------ihi
        nlo------nhi
    -   merge candidate
            ilo------ihi
        nlo--------------nhi
    -   merge candidate
        ilo--------------ihi
            nlo------nhi
    -   merge candidate
        ilo------ihi
            nlo------nhi
    -   merge candidate
        ilo------ihi
                 nlo------nhi
    -   no merge
        ilo------ihi
                     nlo------nhi
    '''

    def __init__(self):
        self.r = None

    def get_root(self):
        return self.r

    def get_preorder(self):
        def get_preorder_(n,l):
            if n != None:
                l.append(n)
                get_preorder_(n.get_lp(),l)
                get_preorder_(n.get_rp(),l)
        l = []
        get_preorder_(self.r,l)
        return l

    def get_inorder(self):
        def get_inorder_(n,l):
            if n != None:
                get_inorder_(n.get_lp(),l)
                l.append(n)
                get_inorder_(n.get_rp(),l)
        l = []
        get_inorder_(self.r,l)
        return l

    def get_postorder(self):
        def get_postorder_(n,l):
            if n != None:
                get_postorder_(n.get_lp(),l)
                get_postorder_(n.get_rp(),l)
                l.append(n)
        l = []
        get_postorder_(self.r,l)
        return l

    def add(self,lo,hi,do_merge=False):
        def add_merge_(lo,hi,n):
            if n == None:
                return
            if n.get_lo() == lo and n.get_hi() == hi:
                return
            if n.get_max() < hi:
                n.set_max(hi)
            if n.get_min() > lo:
                n.set_min(lo)
            if (hi+1) < n.get_lo() or n.get_hi() < (lo-1):
                if hi < n.get_lo():
                    if n.get_lp() == None:
                        nn = LLN(lo=lo,hi=hi,min=lo,max=hi)
                        n.set_lp(nn)
                    else:
                        add_merge_(lo,hi,n.get_lp())
                if n.get_hi() < lo:
                    if n.get_rp() == None:
                        nn = LLN(lo=lo,hi=hi,min=lo,max=hi)
                        n.set_rp(nn)
                    else:
                        add_merge_(lo,hi,n.get_rp())
            else:
                if lo < n.get_lo():
                    n.set_lo(lo)
                if n.get_hi() < hi:
                    n.set_hi(hi)
        def add_(lo,hi,n):
            if n == None:
                return
            if n.get_lo() == lo and n.get_hi() == hi:
                return
            if n.get_max() < hi:
                n.set_max(hi)
            if n.get_min() > lo:
                n.set_min(lo)
            if   n.get_lo() <= lo:
                if n.get_rp() == None:
                    nn = LLN(lo=lo,hi=hi,min=lo,max=hi)
                    n.set_rp(nn)
                else:
                    add_(lo,hi,n.get_rp())
            else:
                if n.get_lp() == None:
                    nn = LLN(lo=lo,hi=hi,min=lo,max=hi)
                    n.set_lp(nn)
                else:
                    add_(lo,hi,n.get_lp())
        if self.r == None:
            self.r = LLN(lo=lo,hi=hi,min=lo,max=hi)
            return
        if do_merge:
            add_merge_(lo,hi,self.r)
        else:
            add_(lo,hi,self.r)

    def find_first_overlap(self,v):
        def find_first_overlap_(self,v,n):
            if n == None:
                return None
            if n.get_lo() <= v and v <= n.get_hi():
                return n
            if n.get_lo() < lo:
                return find_first_overlap_(v,n.get_rp())
            return find_first_overlap_(v,n.get_lp())
        if self.r == None:
            return None
        return find_first_overlap_(v,self.r)

    def find_all_overlap(self,v):
        def find_all_overlap_(self,v,n,l):
            if n == None:
                return
            if n.get_lo() <= v and v <= n.get_hi():
                l.append(n)
            if n.get_min() <= v:
                find_all_overlap_(v,n.get_lp(),l)
            if v <= n.get_max():
                find_all_overlap_(v,n.get_rp(),l)
        l = []
        if self.r != None:
            find_all_overlap_(v,self.r,l)
        return l

    def find_range_all_overlap(self,lo,hi):
        def find_range_all_overlap_(self,lo,hi,n,l):
            if n == None:
                return
            if not (n.get_hi() < lo or hi < n.get_lo()):
                l.append(n)
            if n.get_min() <= lo:
                find_range_all_overlap_(lo,hi,n.get_lp(),l)
            if hi <= n.get_max():
                find_range_all_overlap_(lo,hi,n.get_rp(),l)
        l = []
        if self.r != None:
            find_range_all_overlap_(lo,hi,self.r,l)
        return l

class GNode:
    '''
    GNode is generic class for
    binary tree ops with lc,rc, parent
    also for generic nodes with weighted edges
    '''
    ID = 0
    def __init__(self,v=None):
        self.id = GNode.ID
        self.k = None
        self.v = v
        self.lc = None
        self.rc = None
        self.p = None
        self.vertices = {}          # dst_id:weight dst_id and weight
        self.vertices2nodes = {}    # dst_id:node   dst_id and node
        GNode.ID += 1
    def get_k(self):
        return self.k
    def set_k(self,k):
        self.k = k
        return self
    def get_lc(self):
        return self.lc
    def set_lc(self,lc):
        self.lc = lc
        return self
    def get_rc(self):
        return self.rc
    def set_rc(self,rc):
        self.rc = rc
        return self
    def get_p(self):
        return self.p
    def set_p(self,p):
        self.p = p
        return self
    def get_v(self):
        return self.v
    def set_v(self,v):
        self.v = v
        return self
    def get_id(self):
        return self.id
    def get_vertices(self,is_copy=False):
        if is_copy:
            return self.vertices.copy()
        return self.vertices
    def get_vertices2nodes(self,is_copy=False): # returns dict[node]=weight
        if is_copy:
            return self.vertices2nodes.copy()
        return self.vertices2nodes
    def add_edge(self,dst_node,weight=1):
        self.add_edge_to_node(dst_node,weight)
        self.vertices[dst_id] = weight
        return self
    def add_edge_to_node(self,dst_node,weight=1):
        self.vertices2nodes[dst_node] = weight
        self.vertices[dst_node.get_id()] = weight
        return self
    def get_edge_to_node(self,dst_node):
        if dst_node in self.vertices2nodes:
            return self.vertices2nodes[dst_node]
        return None
    def add_edge_to_node_bilateral(self,dst_node,weight=1):
        self.add_edge_to_node(dst_node,weight)
        dst_node.add_edge_to_node(self,weight)
        return self
    def get_global_id(self):
        return GNode.ID
    @staticmethod
    def reset_id(v:int=0):
        GNode.ID = v
    def print_node(self,id=False,k=False,v=False,vertex_id=False,vertex_weight=False):
        s = self.get_print_node(id,k,v,vertex_id,vertex_weight)
        print(s)
    def get_print_node(self,id=False,k=False,v=False,vertex_id=False,vertex_weight=False):
        s = '{'
        populated = False
        if id:
            s += 'id:{}'.format(self.id)
            populated = True
        if k:
            s = s + (',' if populated else '') + 'k:{}'.format(self.k)
            populated = True
        if v:
            s = s + (',' if populated else '') + 'v:{}'.format(self.v)
            populated = True
        if vertex_id:
            s = s + (',' if populated else '') + 'vertex_id:{}'.format(self.vertices.keys())
            populated = True
        if vertex_weight:
            s = s + (',' if populated else '') + 'vertex_weight:{}'.format(self.vertices.values())
            populated = True
        s += '}'
        return s

class gnode(GNode):
    def __init__(self,v=None):
        super.__init__(v)

class GraphNode(GNode):
    def __init__(self,v=None,name=None):
        super.__init__(v)
        self.name = name

class Graph:
    '''
    Graph is a collection of GNode. Each node knows about connections
    to peer nodes; Graph does not know about all the connections, only the existing GNodes

    Here are methods

    Graph.DType: DIRECTED, UNDIRECTED, MIXED
    add_node(node)
    get_all_nodes_map(is_copy=False)->{node_id:GNode}
    add_edge_to_ids(src_id,dst_id,weight=1,is_directed=True)
    add_edge_to_nodes(src_node,dst_node,weight=1,is_directed=True)
    get_all_sources()
    is_cyclic(nsrc=None,ndst=None)
    make_random_graph(num_nodes,directed_type,min_edges,max_edges,min_weight,max_weight)->{id:GNode}
    set_graph(dict)
    print_graph_summary()
    run_prims_mst()
    '''
    class DType(enum.Enum):
        DIRECTED = 0
        UNDIRECTED = 1
        MIXED = 2

    def __init__(self):
        self.all_nodes = {} # map of all_nodes[id] = GNode
        self.u = Utils()

    def add_node(self,node=None):
        if node == None:
            node = GNode()
        if node.get_id() not in self.all_nodes:
            self.all_nodes[node.get_id()] = node

    def get_all_nodes_map(self,is_copy=False):
        if is_copy:
            return self.all_nodes.copy()
        return self.all_nodes

    def add_edge_to_ids(self, src_id:int, dst_id:int, weight=1, is_directed=True):
        nodes = self.get_all_nodes_map()
        if src_id not in nodes or dst_id not in nodes:
            return
        self.add_edge_to_nodes(nodes[src_id],nodes[dst_id],weight,is_directed)

    def add_edge_to_nodes(self, src_node: GNode, dst_node: GNode, weight=1, is_directed=True):
        if src_node is None or dst_node is None:
            return
        src_node.add_edge_to_node(dst_node,weight)
        if not is_directed:
            dst_node.add_edge_to_node(src_node,weight)

    def make_random_graph(self,
                          num_nodes:int,
                          directed_type:DType,
                          min_edges:int,
                          max_edges:int,
                          min_weight:int,
                          max_weight:int) -> dict:
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
                src_node.add_edge_to_node(nodes[dst_id],w)
                dst_node = nodes[dst_id]
                if directed_type == Graph.DType.UNDIRECTED:
                    dst_node.add_edge_to_node(nodes[src_id],w)
                    pass
                elif directed_type == Graph.DType.MIXED:
                    if u.randint(0,1) == 1:
                        w = u.randint(min_weight,max_weight)
                        dst_node.add_edge_to_node(nodes[src_id],w)
        return nodes

    def set_graph(self, nodes:dict):    # nodes must be nodes[id] = GNode map
        self.all_nodes = nodes.copy()

    def get_all_sources(self):
        dictNodeInboundNodes = {}   # node:set

        for id,n in self.all_nodes.items():
            if n not in dictNodeInboundNodes:
                dictNodeInboundNodes[n] = set()
            for dstnode,weight in n.get_vertices2nodes(False).items():
                if dstnode not in dictNodeInboundNodes:
                    dictNodeInboundNodes[dstnode] = set()
                dictNodeInboundNodes[dstnode].add(n)

        sourceNodes = set()
        for n,inbound in dictNodeInboundNodes.items():
            if len(inbound) == 0:
                sourceNodes.add(n)

        return sourceNodes

    def is_cyclic(self):
        def is_cyclic_(nsrc,ndst,set_visited):
            if nsrc == None:
                return None
            if nsrc in set_visited:
                return nsrc
            if nsrc == ndst:
                return None
            set_visited.add(nsrc)
            for n,weight in nsrc.get_vertices2nodes(False).items():
                cyclic_node = is_cyclic_(n,ndst,set_visited)
                if cyclic_node != None:
                    return cyclic_node
            set_visited.remove(nsrc)

            return None
        '''
        for each source node
            is a node revisited for a single path?
            is a node revisited from any source path?
        '''
        sourceNodes = self.get_all_sources()
        for nsrc in sourceNodes:
            set_visited = set()
            ndst = None
            cyclic_node = is_cyclic_(nsrc,ndst,set_visited)
            if cyclic_node != None:
                return cyclic_node
        return None

    def get_all_topologies(self) -> list:
        '''
        return list of list of paths from any source to any sink,
        return list[list[GNode]]
        '''
        def get_all_topologies_(nsrc,visited,ll,l):
            if nsrc == None:
                return False
            if nsrc in visited:
                return True
            visited.add(nsrc)
            l.append(nsrc)
            dst_nodes = nsrc.get_vertices2nodes(False)
            if len(dst_nodes) == 0:
                ll.append(l.copy())
            else:
                for ndst in dst_nodes.keys():
                    if get_all_topologies_(ndst,visited,ll,l):
                        return True
            l.pop()
            visited.remove(nsrc)

        ll = []
        srcnodes = self.get_all_sources()
        for src in srcnodes:
            visited = set()
            l = []
            if get_all_topologies_(src,visited,ll,l):
                return None
        debug = False
        if debug:
            for l in ll:
                print('-------------------------')
                for n in l:
                    n.print_node(id=True)
        return ll

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

class GraphSamples:
    def __init__(self):
        pass
    @staticmethod
    def get_graph_0():
        '''
        0     4
        |     |
        +-+-+ |
        | +-+-+
        1 2 3
        | | |
        +-+ +-+
          | | |
          5 6 7
          | | |
          +-+ |
          | | |
          8 9 A
        '''
        g = Graph()
        GNode.reset_id(0)
        num_nodes = 11
        d = {}
        for i in range(num_nodes):
            n = GNode()
            d[n.get_id()] = n
            g.add_node(n)
        g.add_edge_to_nodes(d[0],d[1])
        g.add_edge_to_nodes(d[0],d[2])
        g.add_edge_to_nodes(d[0],d[3])
        g.add_edge_to_nodes(d[4],d[2])
        g.add_edge_to_nodes(d[4],d[3])
        g.add_edge_to_nodes(d[1],d[5])
        g.add_edge_to_nodes(d[2],d[5])
        g.add_edge_to_nodes(d[3],d[6])
        g.add_edge_to_nodes(d[3],d[7])
        g.add_edge_to_nodes(d[5],d[8])
        g.add_edge_to_nodes(d[5],d[9])
        g.add_edge_to_nodes(d[6],d[8])
        g.add_edge_to_nodes(d[6],d[9])
        g.add_edge_to_nodes(d[7],d[10])
        return g

    @staticmethod
    def get_graph_1():
        '''
        0     4
        |     |
        +-+-+ |
        | +-+-+
        | | +---+
        1 2 3   |
        | | |   |
        +-+ +-+ |
          | | | |
          5 6 7 |
          | +---+
          +-+
          | |
          8 9
        '''
        g = Graph()
        GNode.reset_id(0)
        num_nodes = 10
        d = {}
        for i in range(num_nodes):
            n = GNode()
            d[n.get_id()] = n
            g.add_node(n)
        g.add_edge_to_nodes(d[0],d[1])
        g.add_edge_to_nodes(d[0],d[2])
        g.add_edge_to_nodes(d[0],d[3])
        g.add_edge_to_nodes(d[4],d[2])
        g.add_edge_to_nodes(d[4],d[3])
        g.add_edge_to_nodes(d[1],d[5])
        g.add_edge_to_nodes(d[2],d[5])
        g.add_edge_to_nodes(d[3],d[6])
        g.add_edge_to_nodes(d[3],d[7])
        g.add_edge_to_nodes(d[5],d[8])
        g.add_edge_to_nodes(d[5],d[9])
        g.add_edge_to_nodes(d[6],d[8])
        g.add_edge_to_nodes(d[6],d[9])
        g.add_edge_to_nodes(d[6],d[3])
        return g

    @staticmethod
    def get_graph_2():
        '''

        0           4
        |           |
        +---+---+   |
        |   +---+---+
        1   2   3
        |   |   |
        +---+   +---+
            |   |   |
            5   6   7
            |   |   |
            | +-+ +-+
            | | | | |
            8 | 9 | A
            | |   |
            +-+   |
            |     |
            |     |
            B     C

        '''
        g = Graph()
        GNode.reset_id(0)
        num_nodes = 13
        d = {}
        for i in range(num_nodes):
            n = GNode()
            d[n.get_id()] = n
            g.add_node(n)
        g.add_edge_to_nodes(d[0],d[1])
        g.add_edge_to_nodes(d[0],d[2])
        g.add_edge_to_nodes(d[0],d[3])
        g.add_edge_to_nodes(d[4],d[2])
        g.add_edge_to_nodes(d[4],d[3])
        g.add_edge_to_nodes(d[1],d[5])
        g.add_edge_to_nodes(d[2],d[5])
        g.add_edge_to_nodes(d[3],d[6])
        g.add_edge_to_nodes(d[3],d[7])
        g.add_edge_to_nodes(d[5],d[8])
        g.add_edge_to_nodes(d[6],d[9])
        g.add_edge_to_nodes(d[6],d[11])
        g.add_edge_to_nodes(d[7],d[10])
        g.add_edge_to_nodes(d[7],d[12])
        g.add_edge_to_nodes(d[8],d[11])
        return g



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
        self.utils = Utils()

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
            #p('pass heapq t0')

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

    def test_find_string_suffix_tree(self):
        '''
        ukkonen construction
        '''
        class snode:
            def __init__(self,val=None):
                self.children = {}
                self.val = val
                self.has_terminal = False
            def get_has_terminal(self):
                return self.has_terminal
            def set_has_terminal(self, has_terminal):
                self.has_terminal = has_terminal
            def set_val(self,val):
                self.val = val
            def get_val(self):
                return self.val
            def get_node(self,c):
                if c not in self.children:
                    return None
                return self.children[c]
            def get_children(self):
                l = list(self.children.values())
                return l
            def add_node(self,c,node):
                self.children[c] = node
            def set_node(self,c,node):
                self.children[c] = node

        class trie_compressed:
            def __init__(self):
                self.r = snode()
            def reset(self):
                self.r = snode()
            def construct(self, s):
                self.r = self._construct(s,self.r)
            def _construct(self,s,n):
                pass
            def get_last_matching_index(self,s1,s2):
                # returns last index that matches, None if no match
                i = 0
                while i < len(s1) and i < len(s2):
                    if s1[i] != s2[i]:
                        break
                    i += 1
                return None if i == 0 else (i - 1)
            def find(self,s):
                if s == None:
                    return False
                n = self.r.get_node(s[0])
                return self._find(s,n)
            def _find(self,s,n):
                if len(s) == 0 or n == None:
                    return False
                v = n.get_val()
                i = self.get_last_matching_index(s,v)
                if i == None:
                    return False
                substring = s[i+1:]
                if len(substring) == 0:
                    return True
                if len(v) != (i+1):
                    return False
                child = n.get_node(substring[0])
                return self._find(substring,child)
            def get_all_words(self):
                l = []
                self._get_all_words(self.r,l,'')
                return l
            def _get_all_words(self,n,l,word):
                if n == None:
                    return
                substring = n.get_val()
                if substring != None and len(substring) != 0:
                    word += substring
                if n.get_has_terminal():
                    l.append(word)
                children = n.get_children()
                if children == None:
                    return
                for child in children:
                    self._get_all_words(child,l,word)

        class suffix_tree_ukkonen(trie_compressed):
            def __init__(self):
                super().__init__()
            def construct_suffix_tree(self,s):
                sz_s = len(s)
                for i in range(sz_s):
                    substring = s[i:]
                    self.construct(substring)

        def t1():
            t = suffix_tree_ukkonen()
            li = ['banana','barn','apple','applet']
            for word in li:
                t.construct_suffix_tree(word)
            l = t.get_all_words()
            set_words = set(l)
            exp = {
                'banana','anana','nana','ana','na','a',
                'barn','arn','rn','n',
                'applet','pplet','plet','let','et','t',
                'apple','pple','ple','le','e'
            }
            assert set_words == exp

        def test():
            try:
                t1()
            except Exception as e:
                raise e
        test()

    def test_run_length_encoding(self):
        def run_length_encode(s):
            p   = None
            c   = None
            cnt = 0
            li  = []
            for i in range(len(s)):
                c = s[i]
                if c != p:
                    if cnt != 0:
                        li.append(cnt)
                        ic = ord(p)
                        li.append(ic)
                    cnt = 1
                else:
                    cnt += 1
                p = c
            if cnt != 0:
                li.append(cnt)
                ic = ord(c)
                li.append(ic)
            res = bytearray(li)
            return res
        def run_length_decode(ba):
            ls = []
            i = 0
            while i < len(ba):
                cnt = ba[i]
                i  += 1
                ic  = ba[i]
                i  += 1
                c   = chr(ic)
                v   = c * cnt
                ls.append(v)
            s = ''.join(ls)
            return s
        def t0():   # string compression with run length encoding
            '''
                      61  31  3        9
            '''
            s = 'aaaaaabaaabaaabbbbbbbbb'
            bs = bytearray([ord(c) for c in s])
            assert bs == bytearray(b'\x61\x61\x61\x61\x61\x61\x62\x61\x61\x61\x62\x61\x61\x61\x62\x62\x62\x62\x62\x62\x62\x62\x62')
            ba = run_length_encode(s)
            rs = run_length_decode(ba)
            assert s == rs
            assert ba == bytearray(b'\x06\x61\x01\x62\x03\x61\x01\x62\x03\x61\x09\x62')
        try:
            t0()
        except Exception as e:
            raise e

    def test_lzw(self):
        pass

    def test_huffman(self):
        '''
        encode:
        1. get frequency dict of the data to be encoded, eg count of each char
        2. each char is leaf node with count
        3. use priority queue, min heap to choose 2 smallest values and construct a parent node of those 2,
           record the sum count of those two min leafs
        4. if next min leaf count > constructed node count, then create a new parent
           with these nodes (min1,min2,parent of min1+min2,min3. otherwise, recursively construct
           min pairs until the next min leaf count > any of the constructed sums
        5. this is repeated until only 1 leaf remaining on heap. at this point, there is a huffman tree.
        6. this means the heaviest values use the least bit of encoding.
        7. when constructing compressed data, each level represents 1 bit added, eg
           root is null
           L1L = 0,                    L1R = 1
           L2LL = 0, L2LR = 1,    L2RL = 0, L2RR = 1

           so then encoding is 10 for L2RL if it is a leaf
           how to prevent ambiguity? must satisfy prefix rule, which results in uniquely decodeable leaf.
           this means no leaf is a prefix of another leaf.
        8. now encode the data by using the tree to each each leaf node, which hopefully has less
           encoding than the char encoding.

        decode:
        1. read from the huffman tree
        2. read in the input sequence and decode each variable sequence of 1 and 0 to reach leaf.
           then start all over.


        '''
        class node:
            ID = 0
            def __init__(self,k,v):
                self.id_ = node.ID
                self.k_ = k
                self.v_ = v
                self.l_ = None
                self.r_ = None
                node.ID += 1
            def reset(self):
                node.ID = 0
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
            '''
            the __lt__,__eq__,__gt__ are needed for tiebreaker values
            the use case is when insert into heapq, the key value is equal, and so
            node needs to be compared. if node needs to be compared, then comparison
            method is needed. 
            
            only __lt__ needs to be implemented
            def __eq__(self, other):
                if other == None:
                    return False
                if self.k() == None:
                    return True
                return self.k() == other.k()
            def __gt__(self, other):
                if other == None:
                    return True
                if self.k() == None:
                    return False
                return self.k() > other.k()

            '''
            def __lt__(self, other):
                if other == None:
                    return False
                if self.k() == None:
                    return True
                return self.k() < other.k()

        def intarray_to_bytearray(ia):
            ba = bytearray()
            ctr = 0
            b = 0
            cnt_total = 0
            for i in ia:
                assert (i == 0 or i == 1)
                ctr += 1
                b = (b << 0x1) | (i & 0x1)
                if ctr % 8 == 0:
                    ba.append(b)
                    ctr = 0
                cnt_total += 1
            if ctr != 0:
                ba.append(b)
            return (cnt_total,ba)
        def bytearray_to_intarray(ba,cnt_total):
            ia = []
            ctr = 0
            for b in ba:
                for i in range(8):
                    if ctr >= cnt_total:
                        break
                    i = b & 0x1
                    ia.append(i)
                    b = b >> 1
                    ctr += 1
                if ctr >= cnt_total:
                    break
            return ia

        def huffman_build_tree(s):
            d = {}

            for c in s:
                if c not in d:
                    d[c] = 0
                d[c] += 1

            ln = [node(k,v) for k,v in d.items()]       # make a node of each k,v

            hq = []
            for n in ln:
                heapq.heappush(hq,(int(n.v()),n))

            while(len(hq) > 0):
                n1 = heapq.heappop(hq)[1]
                if len(hq) == 0:
                    nr = n1
                    break
                n2 = heapq.heappop(hq)[1]
                n = node(None,n1.v()+n2.v())
                n.l(n1 if n1.v() < n2.v() else n2)
                n.r(n1 if n1.v() >= n2.v() else n2)
                heapq.heappush(hq,(int(n.v()),n))

            return nr

        def huffman_build_tree_2(s):
            d = {}

            for c in s:
                if c not in d:
                    d[c] = 0
                d[c] += 1

            ln = [node(k,v) for k,v in d.items()]       # make a node of each k,v

            hqleaves = []
            for n in ln:
                heapq.heappush(hqleaves,(int(n.v(),n)))

            hq = []

            while(len(hqleaves) > 0):
                n1 = heapq.heappop(hqleaves)[1]
                if len(hqleaves) == 0:
                    n = node(None,n1.v())
                    n.l(n1)
                    heapq.heappush(hq,(int(n.v()),n))
                    break
                n2 = heapq.heappop(hqleaves)[1]
                n = node(None,n1.v()+n2.v())
                n.l(n1 if n1.v() < n2.v() else n2)
                n.r(n1 if n1.v() >= n2.v() else n2)
                heapq.heappush(hq,(int(n.v()),n))

            nr = None
            while(len(hq) > 0):
                n1 = heapq.heappop(hq)
                if len(hq) == 0:
                    nr = n1
                    break
                n2 = heapq.heappop(hq)
                n  = node(None,n1.v()+n2.v())
                n.l(n1 if n1.v() < n2.v() else n2)
                n.r(n1 if n1.v() >= n2.v() else n2)
                heapq.heappush(hq,(int(n.v()),n))

            return nr

        def huffman_build_dict_char_to_bin_array(n,d,s,v):
            if n == None:
                return
            if v != None:
                s += v
            if n.k() != None:
                d[n.k()] = s
            else:
                huffman_build_dict_char_to_bin_array(n.l(),d,s,'0')
                huffman_build_dict_char_to_bin_array(n.r(),d,s,'1')

        # returns string of 1s and 0s, which can be passed to binary converter
        def huffman_encode_from_tree(s,d,nr):
            result = ''
            for c in s:
                result += d[c]
            return result

        def huffman_decode_from_binary_string(s,root):
            if s == None or len(s) == 0:
                return

            sz_s = len(s)
            l = []
            i = 0

            while i < sz_s:
                last_i = i
                cnt = 0
                n = root
                while True:
                    if n.k() != None:
                        l.append(n.k())
                        break
                    b = s[i]
                    n = n.l() if b == '0' else n.r()
                    cnt += 1
                    i += 1
                    if cnt > 1000:
                        raise Exception('max_depth for char decode {}'.format(last_i))
                if i >= sz_s:
                    break

            result = ''.join(l)
            return result

        def bytearray_to_str_binary(ba):
            # reserve first 4 bytes for length of string, max of 4G
            ctr = 0
            ctr = ba[0]
            ctr = (ctr << 8) | ba[1]
            ctr = (ctr << 16) | ba[2]
            ctr = (ctr << 24) | ba[3]


            ctr_max = ctr
            bctr = 4
            s = ''
            i = 0
            while i < ctr_max:
                b = ba[bctr]
                for j in range(8):
                    v = (b >> (7-j)) & 0x1
                    v = '0' if v == 0 else '1'
                    s += v
                    i += 1
                    if i >= ctr_max:
                        break
                bctr += 1
            return s

        def str_binary_to_bytearray(s):
            # reserve first 4 bytes for length of string, max of 4G
            ba = bytearray()
            ba.append(0)
            ba.append(0)
            ba.append(0)
            ba.append(0)
            ctr = 0
            bctr = 0
            b = 0
            for c in s:
                v = 0 if c == '0' else 1
                b = (b << 1) | (v & 1)
                ctr += 1
                bctr += 1
                if bctr % 8 == 0:
                    ba.append(b)
                    b = 0
                    bctr = 0
            ba[0] = (ctr >> 24) & 0xff
            ba[1] = (ctr >> 16) & 0xff
            ba[2] = (ctr >> 8) & 0xff
            ba[3] = (ctr >> 0) & 0xff
            return ba

        def serialize_huffman_tree_node(nr):
            pass

        def deserialize_huffman_tree_string(s):
            pass

        def huffman_encode(s):
            nr = huffman_build_tree(s)
            d  = {}
            huffman_build_dict_char_to_bin_array(nr,d,'',None)
            encoded_string = huffman_encode_from_tree(s,d,nr)
            ba = str_binary_to_bytearray(encoded_string)
            return (d,nr,ba)

        def huffman_decode(s,nr):
            decoded_s = huffman_decode_from_binary_string(encoded_string,nr)
            return decoded_s

        def t0():
            s = 'abcbababcabcabcabbcabcabacbababc'
            #s = 'abcbababcabcabcabbcabcabacbabcbacbabcabcbaccccabc'
            huffman_encode(s)
            pass

        def t1():
            '''
            s   = abcbababcabcabcabbca
            b   = 0
            c   = 10
            a   = 11
            s   =  a b  c b  a b  a b  c  a b  c  a b  c  a b b  c  a
            sb  = 11 0 10 0 11 0 11 0 10 11 0 10 11 0 10 11 0 0 10 11
                 '11 0 10 0 11 0 11 0 10 11 0 10 11 0 10 11 0 0 10 11'
            '''
            s = 'abcbababcabcabcabbca'
            s = 'abnassbnabnbababasbabababbansabnabna'
            s = 'abnassbnabnbababasbabababbansabnabnasbasnbanwbansbanabnabnbanabnasbb'+\
                'ansbansbnabsnabnsbnanbsnabsnabsnabnbababanbanabnababababbbabababbnsbansban'+\
                'ansbansbnabsnabnsbnanbsnabsnabsnabnbababanbanabnababababbbabababbnsbansban'
            nr = huffman_build_tree(s)
            d  = {}
            huffman_build_dict_char_to_bin_array(nr,d,'',None)
            encoded_string = huffman_encode_from_tree(s,d,nr)
            decoded_s = huffman_decode_from_binary_string(encoded_string,nr)
            assert decoded_s == s
            sz_s = len(s)
            sz_b = int(len(encoded_string)/8)+1
            #print('encoded bytes: {} string bytes:{}'.format(sz_b,sz_s))
        try:
            t1()
        except Exception as e:
            raise e

    def test_hash(self):
        def rolling_hash_1(substring, next_char, hash_val):
            '''
            construction of 5,3,8,6
            5                           5
            (5*10)+3                    5*10   + 3
            ((5*10)+3)*10+8             5*10^2 + 3*10^1 + 8
            (((5*10)+3)*10+8)*10+6      5*10^3 + 3*10^2 + 8*10^1 + 6

            remove LH 5, add RH 7
            ((5*10^3 + 3*10^2 + 8*10^1 + 6) - 5*10^(len(S)-1))*10 + 7
            3*10^3 + 8*10^2 + 6*10^1 + 7*10^0

            ------------------------------------------------------
            construction from 2,5,3,8  add 6
            2*10^3 + 5*10^2 + 3*10^1 + 8*10^0
            5*10^2 + 3*10^1 + 8*10^0                // substract 2*10^3
            (5*10^2 + 3*10^1 + 8*10^0)*10
            5*10^3 + 3*10^2 + 8*10^1
            5*10^3 + 3*10^2 + 8*10^1 + 6
            '''

            prime = 65449 # 101
            base  = 256

            sz_s = len(substring)

            if next_char == None and hash_val == None:
                h = 0
                for i in range(sz_s):
                    c = substring[i]
                    v = ord(c)
                    h = h*base%prime
                    h += v
                return h
            else:
                c_p = substring[0]
                v = ord(c_p)
                v = v*pow(base,sz_s-1)%prime
                h = hash_val - v
                h = h*base%prime
                v = ord(next_char)
                h += v
                return h
        def test_single():
            s   = 'abcdef'
            p   = 'bcde'
            ss  = 'abcd'
            hv1 = rolling_hash_1(p,None,None)
            hv2 = rolling_hash_1(ss,None,None)
            hv3 = rolling_hash_1(ss,'e',hv2)
            assert hv3 == hv1
        def test_basic_0():
            debug = False
            s = 'abcdefghijklmnopqrstuvwxyz'
            l = []
            sz_ss = 5
            sz_s = len(s)
            ss = s[:sz_ss]
            hashval = None
            next_char = None
            for i in range(sz_ss,sz_s,1):
                hashval = rolling_hash_1(ss,next_char,hashval)
                l.append(hashval)
                if next_char != None:
                    ss = ss[1:] + next_char
                next_char = s[i]
            if debug:
                print(l)
        def test_uniqueness_1():
            debug = False
            charset   = 'abcdefghij'
            utils     = self.utils
            sz_s = 1000
            s = utils.rand_str(sz_s,charset)
            d_s = {}
            d_h = {}
            sz_ss = 5
            ss = s[:sz_ss]
            hv = None
            nc = None
            for i in range(sz_ss,sz_s,1):
                nhv = rolling_hash_1(ss,nc,hv)
                if nc != None:
                    ss = ss[1:] + nc
                if ss not in d_s:
                    d_s[ss] = 0
                d_s[ss] += 1
                if nhv not in d_h:
                    d_h[nhv] = []
                d_h[nhv].append(ss)
                nc = s[i]
                hv = nhv
            if debug:
                print('--------------d_string')
                ctr_u = 0
                ctr_d = 0
                for k,v in d_s.items():
                    if v > 1:
                        print('ss:{} cnt:{}'.format(k,v))
                        ctr_d += 1
                    else:
                        ctr_u += 1
                print('ss: unique: {} duplicate:{}'.format(ctr_u, ctr_d))
                print('--------------d_hash')
                ctr_u = 0
                ctr_d = 0
                for k,v in d_h.items():
                    if len(v) > 1:
                        print('hv:{} ss:{}'.format(k,v))
                        ctr_d += 1
                    else:
                        ctr_u += 1
                print('ss: unique: {} duplicate:{}'.format(ctr_u, ctr_d))

        #test_basic_0()
        #test_uniqueness_1()
        test_single()

    def test_prime_number_generator(self):
        def sieve_of_eratosthenes(max) -> list:
            if max >= 0xffff_ffff_ffff_ffff:
                raise Exception
            l = [True for i in range(max)]
            for i in range(2,max,1):
                if l[i]:
                    for j in range(2,max,1):
                        v = i*j
                        if v >= max:
                            break
                        l[v] = False
            primes = []
            for i in range(max):
                if l[i]:
                    primes.append(i)
            return primes
        '''
        0, 1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
        59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 
        131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 
        197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 
        271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 
        353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 
        433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 
        509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 
        601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 
        677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 
        769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 
        859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 
        953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 
        1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 
        1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 
        1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 
        1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 
        1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 
        1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 
        1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 
        1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663,
        1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 
        1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 
        1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 
        1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011, 
        2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089, 
        2099, 2111, 2113, 2129, 2131, 2137, 2141, 2143, 2153, 2161, 2179, 
        2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 
        2281, 2287, 2293, 2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 
        2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423, 
        2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 
        2543, 2549, 2551, 2557, 2579, 2591, 2593, 2609, 2617, 2621, 2633, 
        2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687, 2689, 2693, 2699, 
        2707, 2711, 2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777, 
        2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843, 2851, 2857, 
        2861, 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 
        2963, 2969, 2971, 2999, 3001, 3011, 3019, 3023, 3037, 3041, 3049, 
        3061, 3067, 3079, 3083, 3089, 3109, 3119, 3121, 3137, 3163, 3167, 
        3169, 3181, 3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251, 3253, 
        3257, 3259, 3271, 3299, 3301, 3307, 3313, 3319, 3323, 3329, 3331, 
        3343, 3347, 3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413, 3433, 
        3449, 3457, 3461, 3463, 3467, 3469, 3491, 3499, 3511, 3517, 3527, 
        3529, 3533, 3539, 3541, 3547, 3557, 3559, 3571, 3581, 3583, 3593, 
        3607, 3613, 3617, 3623, 3631, 3637, 3643, 3659, 3671, 3673, 3677, 
        3691, 3697, 3701, 3709, 3719, 3727, 3733, 3739, 3761, 3767, 3769, 
        3779, 3793, 3797, 3803, 3821, 3823, 3833, 3847, 3851, 3853, 3863, 
        3877, 3881, 3889, 3907, 3911, 3917, 3919, 3923, 3929, 3931, 3943, 
        3947, 3967, 3989, 4001, 4003, 4007, 4013, 4019, 4021, 4027, 4049, 
        4051, 4057, 4073, 4079, 4091, 4093, 4099, 4111, 4127, 4129, 4133, 
        4139, 4153, 4157, 4159, 4177, 4201, 4211, 4217, 4219, 4229, 4231, 
        4241, 4243, 4253, 4259, 4261, 4271, 4273, 4283, 4289, 4297, 4327, 
        4337, 4339, 4349, 4357, 4363, 4373, 4391, 4397, 4409, 4421, 4423, 
        4441, 4447, 4451, 4457, 4463, 4481, 4483, 4493, 4507, 4513, 4517, 
        4519, 4523, 4547, 4549, 4561, 4567, 4583, 4591, 4597, 4603, 4621, 
        4637, 4639, 4643, 4649, 4651, 4657, 4663, 4673, 4679, 4691, 4703, 
        4721, 4723, 4729, 4733, 4751, 4759, 4783, 4787, 4789, 4793, 4799, 
        4801, 4813, 4817, 4831, 4861, 4871, 4877, 4889, 4903, 4909, 4919, 
        4931, 4933, 4937, 4943, 4951, 4957, 4967, 4969, 4973, 4987, 4993, 
        4999, 5003, 5009, 5011, 5021, 5023, 5039, 5051, 5059, 5077, 5081, 
        5087, 5099, 5101, 5107, 5113, 5119, 5147, 5153, 5167, 5171, 5179, 
        5189, 5197, 5209, 5227, 5231, 5233, 5237, 5261, 5273, 5279, 5281, 
        5297, 5303, 5309, 5323, 5333, 5347, 5351, 5381, 5387, 5393, 5399, 
        5407, 5413, 5417, 5419, 5431, 5437, 5441, 5443, 5449, 5471, 5477, 
        5479, 5483, 5501, 5503, 5507, 5519, 5521, 5527, 5531, 5557, 5563, 
        5569, 5573, 5581, 5591, 5623, 5639, 5641, 5647, 5651, 5653, 5657, 
        5659, 5669, 5683, 5689, 5693, 5701, 5711, 5717, 5737, 5741, 5743, 
        5749, 5779, 5783, 5791, 5801, 5807, 5813, 5821, 5827, 5839, 5843, 
        5849, 5851, 5857, 5861, 5867, 5869, 5879, 5881, 5897, 5903, 5923, 
        5927, 5939, 5953, 5981, 5987, 6007, 6011, 6029, 6037, 6043, 6047, 
        6053, 6067, 6073, 6079, 6089, 6091, 6101, 6113, 6121, 6131, 6133, 
        6143, 6151, 6163, 6173, 6197, 6199, 6203, 6211, 6217, 6221, 6229, 
        6247, 6257, 6263, 6269, 6271, 6277, 6287, 6299, 6301, 6311, 6317, 
        6323, 6329, 6337, 6343, 6353, 6359, 6361, 6367, 6373, 6379, 6389, 
        6397, 6421, 6427, 6449, 6451, 6469, 6473, 6481, 6491, 6521, 6529, 
        6547, 6551, 6553, 6563, 6569, 6571, 6577, 6581, 6599, 6607, 6619, 
        6637, 6653, 6659, 6661, 6673, 6679, 6689, 6691, 6701, 6703, 6709, 
        6719, 6733, 6737, 6761, 6763, 6779, 6781, 6791, 6793, 6803, 6823, 
        6827, 6829, 6833, 6841, 6857, 6863, 6869, 6871, 6883, 6899, 6907, 
        6911, 6917, 6947, 6949, 6959, 6961, 6967, 6971, 6977, 6983, 6991, 
        6997, 7001, 7013, 7019, 7027, 7039, 7043, 7057, 7069, 7079, 7103, 
        7109, 7121, 7127, 7129, 7151, 7159, 7177, 7187, 7193, 7207, 7211, 
        7213, 7219, 7229, 7237, 7243, 7247, 7253, 7283, 7297, 7307, 7309, 7321, 7331, 7333, 7349, 7351, 7369, 7393, 7411, 7417, 7433, 7451, 
        7457, 7459, 7477, 7481, 7487, 7489, 7499, 7507, 7517, 7523, 7529, 7537, 7541, 7547, 7549, 7559, 7561, 7573, 7577, 7583, 7589, 7591, 
        7603, 7607, 7621, 7639, 7643, 7649, 7669, 7673, 7681, 7687, 7691, 7699, 7703, 7717, 7723, 7727, 7741, 7753, 7757, 7759, 7789, 7793, 
        7817, 7823, 7829, 7841, 7853, 7867, 7873, 7877, 7879, 7883, 7901, 7907, 7919, 7927, 7933, 7937, 7949, 7951, 7963, 7993, 8009, 8011, 
        8017, 8039, 8053, 8059, 8069, 8081, 8087, 8089, 8093, 8101, 8111, 8117, 8123, 8147, 8161, 8167, 8171, 8179, 8191, 8209, 8219, 8221, 
        8231, 8233, 8237, 8243, 8263, 8269, 8273, 8287, 8291, 8293, 8297, 8311, 8317, 8329, 8353, 8363, 8369, 8377, 8387, 8389, 8419, 8423, 
        8429, 8431, 8443, 8447, 8461, 8467, 8501, 8513, 8521, 8527, 8537, 8539, 8543, 8563, 8573, 8581, 8597, 8599, 8609, 8623, 8627, 8629, 
        8641, 8647, 8663, 8669, 8677, 8681, 8689, 8693, 8699, 8707, 8713, 8719, 8731, 8737, 8741, 8747, 8753, 8761, 8779, 8783, 8803, 8807, 
        8819, 8821, 8831, 8837, 8839, 8849, 8861, 8863, 8867, 8887, 8893, 8923, 8929, 8933, 8941, 8951, 8963, 8969, 8971, 8999, 9001, 9007, 
        9011, 9013, 9029, 9041, 9043, 9049, 9059, 9067, 9091, 9103, 9109, 9127, 9133, 9137, 9151, 9157, 9161, 9173, 9181, 9187, 9199, 9203, 
        9209, 9221, 9227, 9239, 9241, 9257, 9277, 9281, 9283, 9293, 9311, 9319, 9323, 9337, 9341, 9343, 9349, 9371, 9377, 9391, 9397, 9403, 
        9413, 9419, 9421, 9431, 9433, 9437, 9439, 9461, 9463, 9467, 9473, 9479, 9491, 9497, 9511, 9521, 9533, 9539, 9547, 9551, 9587, 9601, 
        9613, 9619, 9623, 9629, 9631, 9643, 9649, 9661, 9677, 9679, 9689, 9697, 9719, 9721, 9733, 9739, 9743, 9749, 9767, 9769, 9781, 9787, 
        9791, 9803, 9811, 9817, 9829, 9833, 9839, 9851, 9857, 9859, 9871, 9883, 9887, 9901, 9907, 9923, 9929, 9931, 9941, 9949, 9967, 9973, 
        10007, 10009, 10037, 10039, 10061, 10067, 10069, 10079, 10091, 10093, 
        10099, 10103, 10111, 10133, 10139, 10141, 10151, 10159, 10163, 10169, 10177, 10181, 10193, 10211, 10223, 10243, 10247, 10253, 10259, 10267, 
        10271, 10273, 10289, 10301, 10303, 10313, 10321, 10331, 10333, 10337, 10343, 10357, 10369, 10391, 10399, 10427, 10429, 10433, 10453, 10457, 
        10459, 10463, 10477, 10487, 10499, 10501, 10513, 10529, 10531, 10559, 10567, 10589, 10597, 10601, 10607, 10613, 10627, 10631, 10639, 10651, 
        10657, 10663, 10667, 10687, 10691, 10709, 10711, 10723, 10729, 10733, 10739, 10753, 10771, 10781, 10789, 10799, 10831, 10837, 10847, 10853, 
        10859, 10861, 10867, 10883, 10889, 10891, 10903, 10909, 10937, 10939, 10949, 10957, 10973, 10979, 10987, 10993, 11003, 11027, 11047, 11057, 
        11059, 11069, 11071, 11083, 11087, 11093, 11113, 11117, 11119, 11131, 11149, 11159, 11161, 11171, 11173, 11177, 11197, 11213, 11239, 11243, 
        11251, 11257, 11261, 11273, 11279, 11287, 11299, 11311, 11317, 11321, 11329, 11351, 11353, 11369, 11383, 11393, 11399, 11411, 11423, 11437, 
        11443, 11447, 11467, 11471, 11483, 11489, 11491, 11497, 11503, 11519, 11527, 11549, 11551, 11579, 11587, 11593, 11597, 11617, 11621, 11633, 
        11657, 11677, 11681, 11689, 11699, 11701, 11717, 11719, 11731, 11743, 11777, 11779, 11783, 11789, 11801, 11807, 11813, 11821, 11827, 11831, 
        11833, 11839, 11863, 11867, 11887, 11897, 11903, 11909, 11923, 11927, 11933, 11939, 11941, 11953, 11959, 11969, 11971, 11981, 11987, 12007, 
        12011, 12037, 12041, 12043, 12049, 12071, 12073, 12097, 12101, 12107, 12109, 12113, 12119, 12143, 12149, 12157, 12161, 12163, 12197, 12203, 
        12211, 12227, 12239, 12241, 12251, 12253, 12263, 12269, 12277, 12281, 12289, 12301, 12323, 12329, 12343, 12347, 12373, 12377, 12379, 12391, 
        12401, 12409, 12413, 12421, 12433, 12437, 12451, 12457, 12473, 12479, 12487, 12491, 12497, 12503, 12511, 12517, 12527, 12539, 
        12541, 12547, 12553, 12569, 12577, 12583, 12589, 12601, 12611, 12613, 12619, 12637, 12641, 12647, 12653, 12659, 12671, 12689, 
        12697, 12703, 12713, 12721, 12739, 12743, 12757, 12763, 12781, 12791, 12799, 12809, 12821, 12823, 12829, 12841, 12853, 12889, 
        12893, 12899, 12907, 12911, 12917, 12919, 12923, 12941, 12953, 12959, 12967, 12973, 12979, 12983, 13001, 13003, 13007, 13009, 
        13033, 13037, 13043, 13049, 13063, 13093, 13099, 13103, 13109, 13121, 13127, 13147, 13151, 13159, 13163, 13171, 13177, 13183, 
        13187, 13217, 13219, 13229, 13241, 13249, 13259, 13267, 13291, 13297, 13309, 13313, 13327, 13331, 13337, 13339, 13367, 13381, 
        13397, 13399, 13411, 13417, 13421, 13441, 13451, 13457, 13463, 13469, 13477, 13487, 13499, 13513, 13523, 13537, 13553, 13567, 
        13577, 13591, 13597, 13613, 13619, 13627, 13633, 13649, 13669, 13679, 13681, 13687, 13691, 13693, 13697, 13709, 13711, 13721, 13723, 
        13729, 13751, 13757, 13759, 13763, 13781, 13789, 13799, 13807, 13829, 13831, 13841, 13859, 13873, 13877, 13879, 13883, 13901, 13903, 
        13907, 13913, 13921, 13931, 13933, 13963, 13967, 13997, 13999, 14009, 14011, 14029, 14033, 14051, 14057, 14071, 14081, 14083, 14087, 
        14107, 14143, 14149, 14153, 14159, 14173, 14177, 14197, 14207, 14221, 14243, 14249, 14251, 14281, 14293, 14303, 14321, 14323, 14327, 
        14341, 14347, 14369, 14387, 14389, 14401, 14407, 14411, 14419, 14423, 14431, 14437, 14447, 14449, 14461, 14479, 14489, 14503, 14519, 
        14533, 14537, 14543, 14549, 14551, 14557, 14561, 14563, 14591, 14593, 14621, 14627, 14629, 14633, 14639, 14653, 14657, 14669, 14683, 14699, 14713, 14717, 
        14723, 14731, 14737, 14741, 14747, 14753, 14759, 14767, 14771, 14779, 14783, 14797, 14813, 14821, 14827, 14831, 14843, 14851, 14867, 14869, 14879, 14887, 
        14891, 14897, 14923, 14929, 14939, 14947, 14951, 14957, 14969, 14983, 15013, 15017, 15031, 15053, 15061, 15073, 15077, 15083, 15091, 15101, 15107, 15121, 
        15131, 15137, 15139, 15149, 15161, 15173, 15187, 15193, 15199, 15217, 15227, 15233, 15241, 15259, 15263, 15269, 15271, 15277, 15287, 15289, 15299, 15307, 
        15313, 15319, 15329, 15331, 15349, 15359, 15361, 15373, 15377, 15383, 15391, 15401, 15413, 15427, 15439, 15443, 15451, 15461, 15467, 15473, 15493, 15497, 
        15511, 15527, 15541, 15551, 15559, 15569, 15581, 15583, 15601, 15607, 15619, 15629, 15641, 15643, 15647, 15649, 15661, 15667, 15671, 15679, 15683, 15727, 
        15731, 15733, 15737, 15739, 15749, 15761, 15767, 15773, 15787, 15791, 15797, 15803, 15809, 15817, 15823, 15859, 15877, 15881, 15887, 15889, 15901, 15907, 
        15913, 15919, 15923, 15937, 15959, 15971, 15973, 15991, 16001, 16007, 16033, 16057, 16061, 16063, 16067, 16069, 16073, 16087, 16091, 16097, 16103, 16111, 
        16127, 16139, 16141, 16183, 16187, 16189, 16193, 16217, 16223, 16229, 16231, 16249, 16253, 16267, 16273, 16301, 16319, 16333, 16339, 16349, 16361, 16363, 
        16369, 16381, 16411, 16417, 16421, 16427, 16433, 16447, 16451, 16453, 16477, 16481, 16487, 16493, 16519, 16529, 16547, 16553, 16561, 16567, 16573, 16603, 
        16607, 16619, 16631, 16633, 16649, 16651, 16657, 16661, 16673, 16691, 16693, 16699, 16703, 16729, 16741, 16747, 16759, 16763, 16787, 16811, 16823, 16829, 
        16831, 16843, 16871, 16879, 16883, 16889, 16901, 16903, 16921, 16927, 16931, 16937, 16943, 16963, 16979, 16981, 16987, 16993, 17011, 17021, 17027, 17029, 
        17033, 17041, 17047, 17053, 17077, 17093, 17099, 17107, 17117, 17123, 17137, 17159, 17167, 17183, 17189, 17191, 17203, 17207, 17209, 17231, 17239, 17257, 
        17291, 17293, 17299, 17317, 17321, 17327, 17333, 17341, 17351, 17359, 17377, 17383, 17387, 17389, 17393, 17401, 17417, 17419, 17431, 17443, 17449, 17467, 
        17471, 17477, 17483, 17489, 17491, 17497, 17509, 17519, 17539, 17551, 17569, 17573, 17579, 17581, 17597, 17599, 17609, 17623, 17627, 17657, 17659, 17669, 
        17681, 17683, 17707, 17713, 17729, 17737, 17747, 17749, 17761, 17783, 17789, 17791, 17807, 17827, 17837, 17839, 17851, 17863, 17881, 17891, 17903, 17909, 
        

        '''
        primes = sieve_of_eratosthenes(0xffff)
        # p(primes)

    def test_find_string_rabin_karp(self):
        def rolling_hash_2(substring, next_char, hash_val):
            prime = 65449
            base  = 256
            sz_s = len(substring)
            h = 0
            if next_char == None and hash_val == None:
                for i in range(sz_s):
                    h = h*base%prime
                    h = h+ord(substring[i])
            else:
                v = (ord(substring[0]))*pow(base,sz_s-1)%prime
                h = (hash_val - v)*base%prime
                h = h+ord(next_char)
            return h
        def rolling_hash(substring, next_char, hash_val):
            prime = 65449
            base  = 256
            sz_s = len(substring)
            h = 0
            if next_char == None and hash_val == None:
                for i in range(sz_s):
                    h = h*base%prime
                    v = ord(substring[i])
                    h = h+v
            else:
                v = ord(substring[0])
                v = v*pow(base,sz_s-1)%prime
                h = hash_val - v
                h = h*base%prime
                v = ord(next_char)
                h = h+v
            return h
        def hash(s, next_char=None, hash=None):
            return rolling_hash(s, next_char, hash)
        def string_cmp(s1,s2):
            sz_s1 = len(s1)
            sz_s2 = len(s2)
            if sz_s1 != sz_s2:
                return False
            for i in range(sz_s1):
                if s1[i] != s2[i]:
                    return False
            return True
        def rabin_karp(s,p):
            ph = hash(p)
            sz_p = len(p)
            sz_s = len(s)
            substr = s[:sz_p]
            next_c = None
            hash_v = None
            for i in range(sz_p,sz_s,1):
                hash_v = rolling_hash(substr,next_c,hash_v)
                if next_c != None:
                    substr = substr[1:] + next_c
                next_c = s[i]
                if hash_v == ph:
                    if string_cmp(p,substr):
                        return i
            return None
        def t_single():
            s         = 'bbdbfccdcdbbfba'
            p         =     'fccdc'
            v         = rabin_karp(s,p)
            assert v != None
        def t_single_negative():
            s         = 'bbdbfccdcdbbfba'
            p         =     'fccdx'
            v         = rabin_karp(s,p)
            assert v == None
        def t0():
            num_cases = 100
            charset   = 'abcdef'
            utils     = self.utils
            sz_s      = 30
            sz_p      = 5
            try:
                for i in range(num_cases):
                    s         = utils.rand_str(sz_s,charset)
                    j         = utils.rand(0,sz_s-sz_p)
                    p         = s[j:j+sz_p]
                    v         = rabin_karp(s,p)
                    if v == None:
                        print('p:{} s:{}'.format(p,s))
                    assert v != None
            except Exception:
                raise
        t0()
        t_single_negative()
        t_single()
    def test_find_string_compressed_trie(self):
        class snode:
            def __init__(self,val=None):
                self.children = {}
                self.val = val
                self.has_terminal = False
            def get_has_terminal(self):
                return self.has_terminal
            def set_has_terminal(self, has_terminal):
                self.has_terminal = has_terminal
            def set_val(self,val):
                self.val = val
            def get_val(self):
                return self.val
            def get_node(self,c):
                if c not in self.children:
                    return None
                return self.children[c]
            def get_children(self):
                l = list(self.children.values())
                return l
            def add_node(self,c,node):
                self.children[c] = node
            def set_node(self,c,node):
                self.children[c] = node

        class trie_compressed:
            def __init__(self):
                self.r = snode()
            def reset(self):
                self.r = snode()
            def construct(self, s):
                self.r = self._construct(s,self.r)
            def _construct(self,s,n):
                '''
                split rules:

                s       bbbcc
                c       bbbbc

                current state:
                node    a->bbbbc->cd
                                ->ef

                s traverses, splits bbbbc to bbb,bc

                next state:
                node    a->bbb->bc->cd$
                                  ->ef$
                              ->cc$

                '''
                if len(s) == 0:
                    return n
                if n == None:
                    node = snode(s)
                    node.set_has_terminal(True)
                    return node

                c = s[0]
                if n != self.r:
                    v = n.get_val()
                    sz_s = len(s)-1
                    sz_v = len(v)-1
                    i = self.get_last_matching_index(s,v)
                    '''
                    assert 1 <= i <= sz_s && (i < sz_v || i == sz_v || i > sz_v)
                    assert NEVER i > sz_s
                    if i == sz_s: assert i <= sz_v # i is never i > sz_v
                    if i < sz_s: assert (i < sz_v || i == sz_v || i > sz_v)
                    '''
                    if i == sz_s:
                        if      i < sz_v:
                            str_p1_v = v[:i+1]
                            str_p2_v = v[i+1:]
                            node = snode(str_p1_v)
                            node.set_has_terminal(True)
                            n.set_val(str_p2_v)
                            node.set_node(str_p2_v[0],n)
                            return node
                    else:
                        '''
                        assert NOT i > sz_s, so this should cover only i < sz_s
                        if i == sz_v then split current node
                        if i < sz_v then split incoming s and current node
                        if i > sz_v: this shouldnt happen
                        '''
                        if      i == sz_v:
                            str_p1_s = s[:i+1]
                            str_p2_s = s[i+1:]
                            node = self._construct(str_p2_s,n.get_node(str_p2_s[0]))
                            n.set_node(str_p2_s[0],node)
                        elif    i < sz_v:
                            str_p1_s = s[:i+1]
                            str_p2_s = s[i+1:]
                            str_p1_v = v[:i+1]
                            str_p2_v = v[i+1:]

                            node = n
                            node.set_val(str_p2_v)
                            n = snode(str_p1_v)
                            n.set_node(str_p2_v[0],node)

                            node_s = snode(str_p2_s)
                            node_s.set_has_terminal(True)
                            n.set_node(str_p2_s[0],node_s)
                else:
                    node = self._construct(s,n.get_node(c))
                    n.set_node(c,node)
                return n

            def get_last_matching_index(self,s1,s2):
                # returns last index that matches, None if no match
                i = 0
                while i < len(s1) and i < len(s2):
                    if s1[i] != s2[i]:
                        break
                    i += 1
                return None if i == 0 else (i - 1)
            def find(self,s):
                if s == None:
                    return False
                n = self.r.get_node(s[0])
                return self._find(s,n)
            def _find(self,s,n):
                if len(s) == 0 or n == None:
                    return False
                v = n.get_val()
                i = self.get_last_matching_index(s,v)
                if i == None:
                    return False
                substring = s[i+1:]
                if len(substring) == 0:
                    return True
                if len(v) != (i+1):
                    return False
                child = n.get_node(substring[0])
                return self._find(substring,child)
            def get_all_words(self):
                l = []
                self._get_all_words(self.r,l,'')
                return l
            def _get_all_words(self,n,l,word):
                if n == None:
                    return
                substring = n.get_val()
                if substring != None and len(substring) != 0:
                    word += substring
                if n.get_has_terminal():
                    l.append(word)
                children = n.get_children()
                if children == None:
                    return
                for child in children:
                    self._get_all_words(child,l,word)

        class suffix_tree(trie_compressed):
            def __init__(self):
                super().__init__()
            def construct_suffix_tree(self,s):
                sz_s = len(s)
                for i in range(sz_s):
                    substring = s[i:]
                    self.construct(substring)
        def t0():
            t = trie_compressed()
            t.construct('banana')
            t.construct('barn')
            t.construct('b')
            t.construct('bs')
            t.construct('monkey')
            t.construct('apple')
            t.construct('key')
            t.construct('ban')
            t.construct('app')
            t.construct('money')
            t.construct('applet')
            t.construct('applets')
            '''
            ROOT-+-b-+-a-+-n-+-ana$
                 |   |   |   +-$
                 |   |   |
                 |   |   +-rn$
                 |   +-$
                 |   |
                 |   +-s$
                 |
                 +-mon-+-key$
                 |     |
                 |     +-ey$
                 |
                 +-app-+-l-+-e$
                 |     |   |
                 |     |   +-let-+-$
                 |     |         |
                 |     +-$       +-s$
                 |
                 +-key$
        
            R---b---a---n---ana$
                         ---$
                     ---rn$
                 ---$
                 ---s$
             ---mon---key$
                   ---ey$
             ---app---l---e#
                   ---$
                       ---let---$
                             ---s$
             ---key$
            '''
            l = t.get_all_words()
            set_words = set(l)
            assert set_words == {'banana','barn','b','bs','monkey','apple','key','ban','app','money','applet','applets'}
            r = t.find('ana')
            assert r == False
            r = t.find('bar')
            assert r == True
            r = t.find('ap')
            assert r == True
            r = t.find('apple')
            assert r == True
            r = t.find('bana')
            assert r == True

        def t1():
            '''

            '''
            t = suffix_tree()
            li = ['banana','barn','apple','applet']
            for word in li:
                t.construct_suffix_tree(word)
            l = t.get_all_words()
            set_words = set(l)
            exp = {
                'banana','anana','nana','ana','na','a',
                'barn','arn','rn','n',
                'applet','pplet','plet','let','et','t',
                'apple','pple','ple','le','e'
            }
            assert set_words == exp

        def test():
            try:
                t0()
                t1()
            except Exception as e:
                raise e
        test()


    def test_find_string_trie(self):
        class snode:
            def __init__(self,val=None):
                self.children = {}
                self.val = None
                self.has_terminal = False
            def get_has_terminal(self):
                return self.has_terminal
            def set_has_terminal(self, has_terminal):
                self.has_terminal = has_terminal
            def set_val(self,val):
                self.val = val
            def get_val(self):
                return self.val
            def get_node(self,c):
                if c not in self.children:
                    return None
                return self.children[c]
            def add_node_from_val(self,val):
                if val not in self.children:
                    self.children[val] = snode(val)
            def add_node(self,c,node):
                self.children[c] = node
        class trie:
            def __init__(self):
                self.r = snode()
            def reset(self):
                self.r = snode()
            def construct(self, s):
                return self._construct(s,len(s),0,self.r)
            def _construct(self,s,sz,i,n):
                if i == sz:
                    child = n.get_node('$')
                    if child == None:
                        child = snode('$')
                        n.add_node('$',child)
                    return
                c = s[i]
                child = n.get_node(c)
                if child == None:
                    child = snode(c)
                    n.add_node(c,child)
                self._construct(s,sz,i+1,child)
            def find(self,s):
                return self._find(s,len(s),0,self.r)
            def _find(self,s,sz,i,n):
                if i > sz or n == None:
                    return None
                if i == sz:
                    return n.get_node('$')
                child = n.get_node(s[i])
                return self._find(s,sz,i+1,child)

        def t0_trie():
            t = trie()
            t.construct('banana')
            t.construct('barn')
            t.construct('monkey')
            t.construct('apple')
            t.construct('key')
            t.construct('ban')
            t.construct('app')
            t.construct('money')
            t.construct('applet')
            r = t.find('ana')
            assert r == None
            r = t.find('barn')
            assert r != None
            r = t.find('applet')
            assert r != None
            r = t.find('apple')
            assert r != None
        t0_trie()

    def test_find_string_suffix_tree(self):
        '''
        have to process the whole text. but after that, you can search any text
        '''
        class suffixnode:
            def __init__(self,c=None,position=None):
                if c != None:
                    self.c = c
                self.set_position = set()       # all the positions where this character exists in text
                if position != None:
                    self.set_position.add(position)
                self.dict_children = {}         # all the child nodes of c->node
            def getc(self):
                return self.c
            def addindex(self,i):
                self.set_postion.add(i)
            def addindices(self,i_set):
                self.set_position.update(i_set)
            def getindex(self,i):
                return i in self.set_position
            def getindices(self,modifiable=True):
                if modifiable:
                    return self.set_position
                return self.set_position.copy()
            def addchildnode(self,node):
                c = node.getc()
                set_indices = node.getindices()
                if c not in self.dict_children:
                    self.dict_children[c] = node
                else:
                    child = self.dict_children[c]
                    child.addindices(set_indices)
            def addchild(self,c,i):
                if c not in self.dict_children:
                    self.dict_children[c] = suffixnode(c,i)
                else:
                    child = self.dict_children[c]
                    if not child.getindex(i):
                        child.addindex(i)
                return self.dict_children[c]
            def getchild(self,c,i=None):
                if c not in self.dict_children:
                    return None
                child = self.dict_children[c]
                if i != None and not child.getindex(i):
                    return None
                return child
        class suffixtree1:
            def __init__(self):
                self.r = suffixnode()
            def reset(self):
                self.r = None
            def construct(self, s, i=0, node=None):
                sz_s = len(s)
                if i >= sz_s:
                    return
                if node == None:
                    node = self.r
                child = node.getchild(s[i])
                if child == None:
                    node.addchild(s[i],i)
                    child = node.getchild(s[i])
                else:
                    child.addindex(i)
                self.construct(s,i+1,child)
            def find(self, s, find_all=True, i=0, j=0, node=None):
                # return the start index in text where s is found, else None
                if node == None:
                    node = self.r
                if i == len(s):
                    return j-len(s)
                child = node.getchild(s[i])
                if child == None:
                    return None
                indices = child.getindices()
                if i == 0:
                    results = []
                    for index in indices:
                        result = self.find(s,i+1,index,child)
                        if result != None:
                            results.append(result)
                            if find_all == False:
                                return results
                else:
                    if j not in indices:
                        return None
                    return self.find(s,i+1,j+1,child)
                return None
        def t0():
            st = suffixtree1()
            st.construct('the cat in the hat lives with a mouse in the house of a man with a pan who likes eating ham')
            results = st.find('with') #this is broken
            #assert len(results) == 2
            return
        class snode:
            def __init__(self,is_leaf=False,val=None):
                self.is_leaf = is_leaf
                self.children = {}
                self.val = None
            def set_is_leaf(self,is_leaf):
                self.is_leaf = is_leaf
            def get_is_leaf(self):
                return self.is_leaf
            def set_val(self,val):
                self.val = val
            def get_val(self):
                return self.val
            def get_all_nodes(self):
                return self.children.values()
            def get_node(self,c):
                if self.is_leaf or c not in self.children:
                    return None
                return self.children[c]
            def add_node(self,node):
                v = node.get_val()
                # what if already existing?
                if v not in self.children:
                    self.children[v] = node
        class trie:
            def __init__(self):
                self.r = snode()
            def reset(self):
                self.r = snode()
            def construct(self, s):
                sz = len(s)
            def _construct(self,s,sz,i,n):
                if i == sz:
                    child = n.get_node('$')
                    if child == None:
                        child = snode(True,'$')
                        n.add_node(child)
                    return
                c = s[i]
                child = n.get_node(c)
                if child == None:
                    child = snode(False,c)
                    n.add_node(child)
                self._construct(s,sz,i+1,child)
            def find(self,s):
                sz = len(s)
                return self._find(s,sz,0,self.r)
            def _find(self,s,sz,i,n):
                if i > sz or n == None:
                    return None
                if i == sz:
                    return n.get_node('$')
                child = n.get_node(s[i])
                return self._find(s,sz,i+1,child)
        class stree:
            def __init__(self):
                self.r = snode()
            def reset(self):
                self.r = snode()
            def construct(self, s):
                sz = len(s)
                for i in range(sz):
                    substr = s[i:]
                    self._construct(substr,0,self.r)
            def _construct(self,s,i,n):
                sz = len(s)
                if i >= sz:
                    return
                c = s[i]
                n.get_node(c)
                if n == None:
                    # split if not empty
                    pass

        t0()

    def test_find_string_kmp(self):
        pctr = 0

        def get_perf_ctr():
            nonlocal pctr
            return pctr
        def find_string_1(s,pat):
            nonlocal pctr
            '''
            this is brute force
            for(i = 0; i < sz_s;)
                if first char of pat match, then check
                else inc
            '''
            pctr = 0
            # brute
            sz_s = len(s)
            sz_p = len(pat)
            i = 0
            while i < sz_s:
                pctr += 1
                j = i
                if s[j] == pat[0]:
                    found = True
                    for m in range(1,sz_p):
                        pctr += 1
                        if (j+m) >= sz_s or m >= sz_p:
                            break
                        cs = s[j+m]
                        cp = pat[m]
                        if s[j+m] != pat[m]:
                            found = False
                            break
                    if found:
                        return i
                i = i+1
            return None

        def find_string_1_1(s,pat):
            nonlocal pctr
            '''
            this is brute force
            for(i = 0; i < sz_s;)
                if first and last chras of pat match, then check
                else inc
            '''
            pctr = 0
            sz_s = len(s)
            sz_p = len(pat)
            i = 0
            while i < sz_s:
                pctr += 1
                j = i
                # match the first and last char
                if s[j] == pat[0] and (j+sz_p-1) < sz_s and s[j+sz_p-1] == pat[sz_p-1]:
                    found = True
                    for m in range(1,sz_p):
                        pctr += 1
                        if s[j+m] != pat[m]:
                            found = False
                            break
                    if found:
                        return i
                i = i+1
            return None

        def find_string_2(s,p,debug=False):
            '''
            for(i = 0; i < sz_s;)
                if first and last chars of pat match, then check
                    keep idx of first char in s that matches pat[0] after this condition
                if mismatch
                    if there is matching first char
                        set i to that matching first char idx
                    else
                        set i to at least +1 or where mismatch was
            '''
            nonlocal pctr
            debug_is_double_space=True
            pctr = 0
            # have idx ptr that points to next matching first char, and skip
            sz_s = len(s)
            sz_p = len(p)
            i = 0
            m = 0

            if debug:
                print('p:            {}'.format(p))
                print('s:            {}'.format(s))
                print('')

            while i < sz_s:
                pctr += 1
                j = i
                m = 0
                idx_next_match_0_char_offset = None

                if debug:
                    print('j:{} m:{}'.format(j,m))
                    print_array(s,debug_is_double_space)
                    space   = '  ' if debug_is_double_space else ' '
                    nospace = ' '  if debug_is_double_space else ''
                    t = space * (j-m)
                    print(t + nospace.join(p))
                    arrow = '' if j == 0 else space * (j)
                    print(arrow + '|\n')

                # match the first and last char
                if s[j] == p[0] and (j+sz_p-1) < sz_s and s[j+sz_p-1] == p[sz_p-1]:
                    found = True
                    for m in range(1,sz_p):
                        pctr += 1
                        # find first char in s that matches p[0],
                        # which can be used to jump to next offset if fail match

                        if debug:
                            print('j:{} m:{}'.format(j,m))
                            print_array(s,debug_is_double_space)
                            space   = '  ' if debug_is_double_space else ' '
                            nospace = ' ' if debug_is_double_space else ''
                            t = space * (j)
                            print(t + nospace.join(p))
                            arrow = '' if (j+m) == 0 else space * (j+m)
                            print(arrow + '|\n')

                        if s[j+m] == p[0] and idx_next_match_0_char_offset is not None:
                            idx_next_match_0_char_offset = m
                        if s[j+m] != p[m]:
                            found = False
                            break
                    if found:
                        return i
                if idx_next_match_0_char_offset is not None:
                    i = i + idx_next_match_0_char_offset
                else:
                    # if no prefix match at all, just go to next idx
                    if m != 0:
                        i += m
                    else:
                        i += 1
            return None

        def find_string_3(s,pat):
            nonlocal pctr
            pctr = 0
            '''
            for(i = 0; i < sz_s;)
                if first and last chars of pat match, then check
                    keep idx of first char in s that matches pat[0] after this condition
                    keep matching offset
                if mismatch
                    if there is matching first char
                        set i to that matching first char idx + matching offset
                    else
                        set i to at least +1 or where mismatch was
            '''
            sz_s = len(s)
            sz_p = len(pat)
            i = 0
            i_pat = 0
            debug = False
            while i < sz_s:
                pctr += 1
                j = i
                idx_next_match_0_char_offset = None
                prefix_offset = 0
                # match the first and last char
                if debug: print('i:{:2} s:{} p:{}'.format(i,s,pat))
                if s[j] == pat[0] and (j+sz_p-1) < sz_s and s[j+sz_p-1] == pat[sz_p-1]:
                    if debug: print('i:{:2} s[{}] == pat[0] ({}) s:{} p:{}'.format(i,j,pat[0],s,pat))
                    found = True
                    for m in range(1,sz_p):
                        pctr += 1
                        # find first char in s that matches pat[0],
                        # which can be used to jump to next offset if fail match
                        if debug: print('i:{:2} s[{}+{}] = {} pat[{}] = {} idx_next_match_0_char_offset:{} prefix_offset:{}'.format(i,j,m,s[j+m],m,pat[m],idx_next_match_0_char_offset,prefix_offset))
                        if idx_next_match_0_char_offset is not None:
                            if s[j+m] == pat[m] and (prefix_offset+idx_next_match_0_char_offset) == m:
                                prefix_offset += 1
                        if s[j+m] == pat[0] and idx_next_match_0_char_offset is None:
                            idx_next_match_0_char_offset = m
                            prefix_offset = 1
                        if s[j+m] != pat[m]:
                            found = False
                            break
                    if found:
                        return i
                if idx_next_match_0_char_offset is not None:
                    if debug: print('i:{:2} idx_next_match_0_char_offset:{} prefix_offset:{}'.format(i,idx_next_match_0_char_offset,prefix_offset))
                    i += idx_next_match_0_char_offset
                    i += prefix_offset      # this is i offset, different from offset and where to start comparing. this can lead to wrong comparisons!
                else:
                    i += 1
            return None

        def find_string_4(s,pat):
            nonlocal pctr
            pctr = 0
            '''
            NOT currently working
            
            for(i = 0; i < sz_s;)
                if first and last chars of pat match, then check
                    keep idx of first char in s that matches pat[0] after this condition
                    keep matching offset
                if mismatch
                    if there is matching first char
                        set i to that matching first char idx + matching offset
                    else
                        set i to at least +1 or where mismatch was
            '''
            sz_s = len(s)
            sz_p = len(pat)
            i = 0
            i_pat = 0
            debug = False
            while i < sz_s:
                pctr += 1
                j = i
                idx_next_match_0_char_offset = None
                prefix_offset = 0
                # match the first and last char
                if debug: print('i:{:2} s:{} p:{}'.format(i,s,pat))
                if s[j] == pat[0] and (j+sz_p-1) < sz_s and s[j+sz_p-1] == pat[sz_p-1] and s[j+i_pat] == pat[i_pat]:
                    if debug: print('i:{:2} s[{}] == pat[0] ({}) s:{} p:{}'.format(i,j,pat[0],s,pat))
                    found = True
                    for m in range(i_pat,sz_p):
                        pctr += 1
                        # find first char in s that matches pat[0],
                        # which can be used to jump to next offset if fail match
                        if debug: print('i:{:2} s[{}+{}] = {} pat[{}] = {} idx_next_match_0_char_offset:{} prefix_offset:{}'.format(i,j,m,s[j+m],m,pat[m],idx_next_match_0_char_offset,prefix_offset))
                        if idx_next_match_0_char_offset is not None:
                            if s[j+m] == pat[m] and (prefix_offset+idx_next_match_0_char_offset) == m:
                                prefix_offset += 1
                        if s[j+m] == pat[0] and idx_next_match_0_char_offset is None:
                            idx_next_match_0_char_offset = m
                            prefix_offset = 1
                        if s[j+m] != pat[m]:
                            found = False
                            break
                    if found:
                        return i
                if idx_next_match_0_char_offset is not None:
                    if debug: print('i:{:2} idx_next_match_0_char_offset:{} prefix_offset:{}'.format(i,idx_next_match_0_char_offset,prefix_offset))
                    i += idx_next_match_0_char_offset
                    i_pat = prefix_offset
                else:
                    i += 1
                    i_pat = 0
            return None

        def find_string_kmp(s,p,debug=False):
            nonlocal pctr
            debug_is_double_space=True
            pctr = 0
            flag = False
            sz_s = len(s)
            sz_p = len(p)
            l_table_prefix = construct_kmp_table(p)
            i_s = 0     # index of string
            i_p = 0     # index of pat
            i_t = 0
            if debug:
                print('prefix_table: {}'.format(''.join([str(i) for i in l_table_prefix])))
                print('p:            {}'.format(p))
                print('s:            {}'.format(s))
                print('')
            while i_s < sz_s and i_p < sz_p:
                pctr += 1
                if debug:
                    c_s = s[i_s]
                    c_p = p[i_p]
                    idx_prefix = 0 if i_p == 0 else l_table_prefix[i_p-1]
                    print('s[{}]={} p[{}]={} t={} next_prefix={}'.format(i_s,c_s,i_p,c_p,i_t,idx_prefix))
                    print_array(s,debug_is_double_space)
                    t = ' ' * (i_s-i_p)
                    if debug_is_double_space:
                        print(t + t + ' '.join(p))
                        arrow = '' if i_s == 0 else '  ' * (i_s)
                        arrow += '|'
                        print(arrow)
                    else:
                        print(t + ''.join(p))
                        arrow = '' if i_s == 0 else ' ' * (i_s)
                        arrow += '|'
                        print(arrow)

                    print('\n')

                if s[i_s] != p[i_p]:
                    '''
                    if i_t != 0:
                        i_p = i_t
                    else:
                        if i_p != 0:
                            i_p = l_table_prefix[i_p-1]
                        else:
                            i_s += 1
                    '''
                    '''
                    if i_p != 0:
                        i_p = l_table_prefix[i_p-1]
                    else:
                        i_s += 1
                    '''
                    if i_p != 0:
                        i_p = l_table_prefix[i_p-1]
                        #i_p = l_table_prefix[i_t] if i_p == 0 else i_p
                    else:
                        i_s += 1
                    i_t = 0
                    if debug:
                        print('next compare starts at i_s:{} i_p:{}'.format(i_s,i_p))
                        print('\n')

                else:
                    i_p += 1
                    i_s += 1
                    i_t += 1
            if i_p == sz_p:
                return i_s-sz_p
            return None

        def construct_kmp_table(s) -> list:
            prefix_table = []
            sz_s = len(s)
            offset = 0
            for i in range(sz_s):
                if i == 0:
                    prefix_table.append(0)
                elif s[i] == s[offset]:
                    offset += 1
                    prefix_table.append(offset)
                else:
                    # this part should look at backward index for first matching, then +1
                    # for now, resetting it to 0 is a performance hit
                    offset = 0
                    if s[i] == s[offset]:
                        offset += 1
                    prefix_table.append(offset)
            return prefix_table

        def test_str_1():
            '''
            #    000000000011111111112222222222
            #    012345678901234567890123456789
            s = 'cefefcefgcegcefghcefgcefghicef'
            p = 'cefghi'
                 cef
                      cefg
                          ce
                             cefgh
                                  cefg
                                      cefghi
            '''

            #    000000000011111111112222222222
            #    012345678901234567890123456789
            nonlocal pctr
            s = 'cefefcefgcegcefghcefgcefghicef'
            p =                      'cefghi'
            r = find_string_1(s,p)
            print('ctr {}'.format(pctr))
            assert r == 21
            r = find_string_1_1(s,p)
            print('ctr {}'.format(pctr))
            assert r == 21
            r = find_string_2(s,p)
            print('ctr {}'.format(pctr))
            assert r == 21
            r = find_string_3(s,p)
            print('ctr {}'.format(pctr))
            assert r == 21

        def test_str_2():
            '''
            #    000000000011111111112222222
            #    012345678901234567890123456
            s = 'aabbaabbaabcaaabbccaabbbbcc'
            p =               'abbcca'

            '''
            nonlocal pctr
            s = 'aabbaabbaabcaaabbccaabbbbcc'
            p =               'abbcca'
            r = find_string_1(s,p)
            print('ctr {}'.format(pctr))
            assert r == 14
            r = find_string_1_1(s,p)
            print('ctr {}'.format(pctr))
            assert r == 14
            r = find_string_2(s,p)
            print('ctr {}'.format(pctr))
            assert r == 14
            r = find_string_3(s,p)
            print('ctr {}'.format(pctr))
            assert r == 14

        def test_str_3():
            '''
            #    000000000011111111112222222
            #    012345678901234567890123456
            s = 'aabbaabbaabcaaabbccaabbbbcc'
            p =               'abbccab'

            '''
            nonlocal pctr
            s = 'aabbaabbaabcaaabbccaabbbbcc'
            p =               'abbccb'
            r = find_string_kmp(s,p)
            r = find_string_1(s,p)
            print('ctr {}'.format(pctr))
            assert r == None
            r = find_string_1_1(s,p)
            print('ctr {}'.format(pctr))
            assert r == None
            r = find_string_2(s,p)
            print('ctr {}'.format(pctr))
            assert r == None
            r = find_string_3(s,p)
            print('ctr {}'.format(pctr))
            assert r == None

        def test_str_4():
            '''
            #    000000000011111111112222222222333333
            #    012345678901234567890123456789012345
            s = 'aaabaaabaaabaabaaabaabaaabaababaaaba'
            p =                       'aaabaababa'

            worksheet:
            prefix
                 0123456789
                 aaabaababa
                 0120123401

            #    0000000000 1111111111 2222222222 333333
            #    0123456789 0123456789 0123456789 012345
            s = 'aaabaaabaa abaabaaaba abaaabaaba baaaba'   p_idx_mismatch  p_shift_val     next_idx_p
            p =  aaabaababa
                 aaabaa|                                    6               2               i+(6-2)=i+4
                     aaabaa|                                6               2               i+(6-2)=i+4
                         aa abaaba|                         8               0               i+(8-0)=i+8
                                  aa|                       2               1               i+(2-1)=i+1
                                   a|                       1               0
                                    a
                                     a a|                   2               1
                                       a|
                                        |
                                         aaabaaba ba
                does this always work?? this shift p by next_idx_p is weird
                the trick is to shift p relative to s[i], but never move i (of s) backward.
            '''
            nonlocal pctr
            s = 'aabbaabbaabcaaabbccaabbbbcc'
            p =               'abbccb'
            s = 'aaabaaabaaabaabaaabaabaaabaababaaaba'
            p = 'aaabaababa'

            r = find_string_1(s,p)
            assert r != None

            r = find_string_kmp(s,p)
            assert r != None

        def test_kmp():
            debug = False
            if debug:
                print('-------------------------------------------------')

            s = 'aabbaabbaabcaaabbccaabbbbcc'
            p =               'abbccb'
            r = find_string_kmp(s,p,False)
            assert r == None

            s = 'aabbaabbaabcaaabbccaabbbbcc'
            p =               'abbcca'
            r = find_string_kmp(s,p,False)
            assert r != None

            s = 'aababaabababaababbbaaabababaabaabaabababaaababaabaaabaaa'
            p =                                           'ababaabaaab'
            r = find_string_kmp(s,p,False)
            assert r != None

            s = 'aababaabababaababbbaaabababaabaabaabababaaababaabaaabaaa'
            p =                                           'ababaabaaabb'
            r = find_string_kmp(s,p,False)
            assert r == None

            s = 'abedaadcaadcadbabaedacbcedeee'
            p =          'adcadbabae'
            r = find_string_kmp(s,p,False)
            assert r == 9

            s = 'ceaebabaabdaadcbaeaabcbacd'
            p =       'baabdaadcb'
            r = find_string_kmp(s,p,False)
            assert r != None

            s = 'cdcaaaaaaddebbeabcdeaabdb'
            p =      'aaaaddebbe'
            r = find_string_kmp(s,p,False)
            assert r != None

            s = 'cbededdeddeeebddcbeaa'
            p =       'deddeeebdd'
            r = find_string_kmp(s,p,False)
            assert r != None

            s = 'aaaaaaaaaaaaaaaaaaaaaaaabbaaaaaaaaaaaa'
            p =             'aaaaaaaaaaaabbaaaaaa'
            r = find_string_kmp(s,p,False)
            assert r != None

            '''
            s = ''
            p =      ''
            r = find_string_kmp(s,p,True)
            assert r != None
            '''

        def test_single_case():
            s = 'aaaaaaaaaaaaaaaaaaaaaaaabbaaaaaaaaaaaa'
            p =             'aaaaaaaaaaaabbaaaaaa'
            s = 'aababaabababaababbbaaabababaabaabaabababaaababaabaaabaaa'
            p =                                           'ababaabaaab'
            r0 = find_string_kmp(s,p,False)
            p0 = get_perf_ctr()
            assert r0 != None
            r1 = find_string_1(s,p)
            p1 = get_perf_ctr()
            assert r1 != None
            r2 = find_string_2(s,p,False)
            p2 = get_perf_ctr()
            assert r2 != None
            #print('pctr[0,1,2] = [{},{},{}]'.format(p0,p1,p2))

        def test_kmp_random_positive():
            num_cases = 1000
            sz_s = 100
            sz_p = 10
            charset   = 'abcdef'
            utils     = self.utils
            res_pctr  = []
            try:
                for i in range(num_cases):
                    s = utils.rand_str(sz_s,charset)
                    j = utils.rand(0,sz_s-sz_p)
                    p = s[j:j+10]
                    r = find_string_kmp(s,p)
                    if r != j:
                        print('case:{} mismatch: expected match at j:{} r:{}'.format(i,j,r))
                        print('')
                        print_array(s)
                        print('')
                        print_array(p)
                        print('')
                        r = find_string_kmp(s,p,True)

                    assert r == j
                    pctr_val = get_perf_ctr()
                    res_pctr.append(pctr_val)
            except Exception as e:
                raise e
            #print('pctr_val {}'.format(res_pctr))
            return


        def test_kmp_random_negative():
            num_cases = 100
            pass

        def test_compare_performance():
            num_cases = 1000
            sz_s      = 100
            sz_p      = 10
            charset   = 'abcdef'
            utils     = self.utils
            res_pctr  = []
            data_in   = []
            for i in range(num_cases):
                s       = utils.rand_str(sz_s,charset)
                j       = utils.rand(0,sz_s-sz_p)
                p       = s[j:j+sz_p]
                tup = (s,p,j)
                data_in.append(tup)

            pctr_out  = []

            try:
                i = 0
                for tup in data_in:
                    s = tup[0]
                    p = tup[1]
                    j = tup[2]

                    r1 = find_string_kmp(s,p)
                    p1 = get_perf_ctr()
                    r2 = find_string_1(s,p)
                    p2 = get_perf_ctr()
                    r3 = find_string_1_1(s,p)
                    p3 = get_perf_ctr()
                    r4 = find_string_2(s,p)
                    p4 = get_perf_ctr()
                    r5 = find_string_3(s,p)
                    p5 = get_perf_ctr()

                    tup_pctr = (p1,p2,p3,p4,p5)
                    res_pctr.append(tup_pctr)

                    if r1 != j:
                        print('case:{} mismatch: expected match at j:{} r:{}'.format(i,j,r1))
                        print('')
                        print_array(s)
                        print('')
                        print_array(p)
                        print('')
                        r = find_string_kmp(s,p,True)

                    assert r1 == j
                    print('r[1,2,3,4,5] = [{},{},{},{},{}]'.format(r1,r2,r3,r4,r5))
                    if r1 == r2 and r1 == r3 and r1 == r4 and r1 == r5:
                        pctr_out.append(tup_pctr)
                    '''
                    if not (r1 == r2 and r1 == r3 and r1 == r4 and r1 == r5):
                        print('r[1,2,3,4,5] = [{},{},{},{},{}]'.format(r1,r2,r3,r4,r5))
                    assert r1 == r2 and r1 == r3 and r1 == r4 and r1 == r5
                    '''
                    i += 1
                # get pctr average
                sum_list = [0,0,0,0,0]
                avg_list = [0,0,0,0,0]
                sz_list = len(pctr_out)
                for tup in pctr_out:
                    for k in range(len(tup)):
                        sum_list[k] += tup[k]
                for k in range(len(sum_list)):
                    avg_list[k] = sum_list[k]/sz_list
                    avg_list[k] = round(avg_list[k],2)
                print('avg perfctr: {}'.format(avg_list))

            except Exception as e:
                raise e
            #print('pctr_val {}'.format(res_pctr))
            return

        def test_main_string_find():
            '''
            test_str_1()
            p('\n')
            test_str_2()
            p('\n')
            test_str_3()
            p('\n')
            test_str_4()
            p('\n')
            test_kmp_random_positive()
            test_compare_performance()
            test_kmp()
            '''
            test_single_case()


        test_main_string_find()

    def test_printarray(self):
        def _printarray(s):
            sz_s = len(s)
            numbers = []
            result = sz_s
            # 0 0-9
            # 1 10-99
            # 2 100-999
            # ...
            while result != 0:
                remainder = int(result % 10)
                numbers.append(remainder)
                result -= remainder
                result /= 10
            numbers.reverse()
            starting_ten = 10**(len(numbers)-1)
            # ...
            # 0 100-999
            # 1 10-99
            # 2 0-9
            buf = []
            for i in range(len(numbers)):
                buf.append([])
                print_v = 0
                ctr = 0
                for j in range(sz_s):
                    if j != 0 and j % starting_ten == 0:
                        print_v = (print_v + 1) % 10
                    buf[i].append(str(print_v))
                #starting_ten = starting_ten/10 if starting_ten > 10 else 10
                starting_ten = starting_ten/10
            debug = True
            if debug:
                for line in buf:
                    p(' '.join(line))
                p(' '.join(s))
        _printarray('abcdefghijklmnopqrstuvwxyz01234567890abcdefghijklmnopqrstuvwxyz01234567890abcdefghijklmnopqrstuvwxyz01234567890abcdefghijklmnopqrstuvwxyz01234567890')

    def test_k_dimension_search(self):
        class k_node:
            def __init__(self,tup):
                self.sz = len(tup)
                self.tup = tup
                self.lchildren = [None for i in range(self.sz)]
                self.rchildren = [None for i in range(self.sz)]
            def getdimval(self,dimension):
                if self.sz <= dimension:
                    return None
                return self.tup[dimension]
            def getdimchild(self,dimension,is_left):
                if self.sz <= dimension:
                    return None
                if is_left:
                    return self.lchildren[dimension]
                return self.rchildren[dimension]
            def gettuple(self):
                return self.tup
            def setdimchild(self,dimension,child_k_node,is_left):
                if self.sz <= dimension:
                    raise Exception('wrong dimension k_node: {}'.format(dimension))
                if is_left:
                    self.lchildren[dimension] = child_k_node
                else:
                    self.rchildren[dimension] = child_k_node
            def calculate_distance(self,tup):
                return self.calculate_unweighted_distance(tup)
            def calculate_unweighted_distance(self,tup):
                res = 0
                for v1,v2 in (tup,self.tup):
                    res += (v1-v2) ** 2
                res = math.sqrt(res)
                return res
        class k_dimension_tree:
            '''
            this assume rigid dimensions, where all points must have k-dimensions, that are non nullable

            we want operations such as get all elements where tuple[k-dim] < x. does this mean
            we need k roots and insert into k trees? seems pretty bad
            - balance
            - remove
            - nearest neighbor search

            insertion rotates along k axis, such that each level, the comparison axis is n modulo k
            '''
            def __init__(self,num_dimensions):
                self.r = None
                self.ndim = num_dimensions
            def add_point(self, tup):
                if len(tup) != self.ndim:
                    raise Exception('wrong dimension for tuple: {}'.format(len(tup)))
                self.r = self.i_add_point(tup,self.r,0)
            def i_add_point(self, tup, node, level):
                if node == None:
                    newnode = k_node(tup)
                    return newnode
                dim = level % self.ndim
                vcurr = tup[dim]
                vnode = node.getdimval(dim)
                childnode = None
                is_left = True
                if vcurr < vnode:
                    is_left = True
                else:
                    is_left = False
                childnode = node.getdimchild(dim,is_left)
                retnode = self.i_add_point(tup,childnode,level+1)
                node.setdimchild(dim,retnode,is_left)
                return node
            def get_point(self, tup):
                if len(tup) != self.ndim:
                    raise Exception('wrong dimension for tuple: {}'.format(len(tup)))
                return self.i_get_point(tup, self.r, 0)
            def i_get_point(self, tup, node, level):
                if node == None:
                    return None
                if tup == node.gettuple():
                    return node
                dim = level % self.ndim
                is_left = True
                vcurr = tup[dim]
                vnode = node.getdimval(dim)
                if vcurr < vnode:
                    is_left = True
                else:
                    is_left = False
                childnode = node.getdimchild(dim, is_left)
                return self.i_get_point(tup,childnode,level+1)


        def test_3vector():
            a_points = [
                (5,5,5),
                (3,5,8),
                (7,2,4),
                (8,8,8),
                (2,2,2)
            ]
            kdt = k_dimension_tree(3)
            for p in a_points:
                kdt.add_point(p)
            p = kdt.get_point((7,2,4))
            assert p != None
            p = kdt.get_point((3,2,1))
            assert p == None


        test_3vector()

    def test_calculate_all_distances_of_points(self):
        ap = [
            (5,2),(5,8),(3,6),(3,4),(2,8),(3,7),(7,3)
        ]
        map = {}  # d[tupsrc][tupdst] = distance
        for p1 in ap:
            k1 = ','.join(str(v) for v in p1)
            map[k1] = {}
            for p2 in ap:
                if p1 == p2: continue
                dist = 0
                for x,y in zip(p1,p2):
                    dist += (x-y)**2
                dist = math.sqrt(dist)
                dist = round(dist,1)
                k2 = ','.join(str(v) for v in p2)
                map[k1][k2] = str(dist)
        debug = True
        if debug:
            for k,v in map.items():
                p('{} = {}'.format(k,json.dumps(v)))
            #vjson = json.dumps(map)
            #p(vjson)

        ap = [
            (5,2,3),(5,8,2),(3,6,5),(3,4,3),(2,8,7),(3,7,6),(7,3,2)
        ]
        map = {}  # d[tupsrc][tupdst] = distance
        for p1 in ap:
            k1 = ','.join(str(v) for v in p1)
            map[k1] = {}
            for p2 in ap:
                if p1 == p2: continue
                dist = 0
                for x,y in zip(p1,p2):
                    dist += (x-y)**2
                dist = round(math.sqrt(dist),1)
                k2 = ','.join(str(v) for v in p2)
                map[k1][k2] = str(dist)
        debug = True
        if debug:
            for k,v in map.items():
                p('{} = {}'.format(k,json.dumps(v)))
            #vjson = json.dumps(map)
            #p(vjson)


        pass

    def test_find_all_points_within_rectangle_2d(self):
        '''
        in 2d space, find all points within a given rectangle
        '''
        pass

    def test_minmax_diff_in_bst(self):
        '''
        within BST, find the first min diff between any two node vals
        within BST, find the first max diff between any two node vals
        '''
        pass

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
            def __lt__(self,other):
                return self.v < other.v
            def __gt__(self,other):
                return self.v > other.v
            def __eq__(self, other):
                return self.v == other.v

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

            def add(self, v, n=None):
                if(n is None):
                    if(self.r is None): self.r = _Node(v)
                    return
                if(v < n.v):
                    if(n.l is None): n.l = _Node(v)
                    else:            add(v,n.l)
                else:
                    if(n.r is None): n.r = _Node(v)
                    else:            add(v,n.r)
                return add(v, self.r)
            def get(self, v, n=None):
                if(n is None):
                    if(self.r is None): return None
                    return get(v,self.r)
                if(n.v == v): return n
                if(n.v < v): return get(v,n.l)
                return get(v,n.r)

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
    def test_interleave(self):
        def interleave(s1,s2,stringval:str,results:list):
            if len(s1) == 0 and len(s2) == 0:
                if len(stringval) != 0:
                    results.append(stringval)
                return
            if stringval is None:
                stringval = ''
            if len(s1) > 0:
                interleave(s1[1:],s2,stringval+s1[0:1],results)
            if len(s2) > 0:
                interleave(s1,s2[1:],stringval+s2[0:1],results)
        def do_print(s1,s2,l:list):
            sz = len(l)
            p('s1:{},s2:{}'.format(s1,s2))
            for i in range(sz):
                p('{:3}:{}'.format(i,l[i]))
        def t0():
            results = []
            s1 = '0123'
            s2 = '4567'
            interleave(s1,s2,None,results)
            #do_print(s1,s2,results)
        t0()

    def test_dices(self):
        def all_dice_combos_2(d1,d2,result):
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

        def edit_distance_recursive(s1,s2):
            # not verified yet
            def edrec(s1,s2,i1,i2,cost,mem):

                key = '{},{}'.format(i1,i2)
                #if key in mem:
                #    return mem[key]

                if i1 == len(s1) and i2 == len(s2):
                    mem[key] = cost
                    return cost
                if i1 >= len(s1):
                    cost = cost + len(s2) - i2
                    mem[key] = cost
                    return cost
                if i2 >= len(s2):
                    cost = cost + len(s1) - i1
                    mem[key] = cost
                    return cost
                if s1[i1] == s2[i2]:
                    return edrec(s1,s2,i1+1,i2+1,cost,mem)

                c1 = edrec(s1,s2,i1+1,i2,cost+1,mem)
                c2 = edrec(s1,s2,i1,i2+1,cost+1,mem)
                c3 = edrec(s1,s2,i1+1,i2+1,cost+1,mem)

                cost = min(c1,c2,c3)
                mem[key] = cost
                return cost

            mem = {}
            min = edrec(s1,s2,0,0,0,mem)
            return min

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

            s1 = 'kiterider'
            s2 = 'taxidriver'
            d = edit_distance_recursive(s1,s2)

            s1 = 'kiterider'
            s2 = 'kindriver'
            d = edit_distance_recursive(s1,s2)

            s1 = 'kiterider'
            s2 = 'niterivers'
            d = edit_distance_recursive(s1,s2)

            s1 = 'kiteriders'
            s2 = 'niteriver'
            d = edit_distance_recursive(s1,s2)

            s1 = 'kiterider'
            s2 = 'niterider'
            d = edit_distance_recursive(s1,s2)

            s1 = 'kniterider'
            s2 = 'kiterider'
            d = edit_distance_recursive(s1,s2)

            s1 = 'kiterider'
            s2 = 'kniterider'
            d = edit_distance_recursive(s1,s2)

            s1 = 'gnatrider'
            s2 = 'knitrider'
            d = edit_distance_recursive(s1,s2)

            s1 = 'kiteriders'
            s2 = 'niterider'
            d = edit_distance_recursive(s1,s2)

            return
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
        #g.print_graph_summary()

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
    def test_trapping_rainwater_2d(self):
        pass

    def test_largest_rectangle_in_histogram(self):
        pass

    def test_palindromic_substrings(self):
        pass

    def test_top_k_frequent_elements(self):
        pass

    def test_knapsack(self):
        pass

    def test_text_justification(self):
        '''
        dp is considered smart brute force, but still brute force,
        because trying all possible combinations in an efficient way

        in dp, you basically need to find all splits/combos of words
        and minimize the space for each line, minus the last line.
        '''

        class container:
            def __init__(self, min=None):
                self.min = min
                self.ll = None
            def set_list_2d(self,ll):
                self.ll = copy.deepcopy(ll)
            def get_list_2d(self):
                return self.ll
            def set_min_score(self, min):
                self.min = min
            def get_min_score(self):
                return self.min

        def score_matrix(list_words,ll,max_width,include_last_row=False):
            num_rows = 0
            for row in ll:
                if len(row) == 0:
                    break
                num_rows += 1
            if not include_last_row:
                num_rows -= 1

            total_num_spaces = 0
            for row in ll:
                num_chars = 0
                for idx_word in row:
                    num_chars += len(list_words[idx_word])
                num_spaces = max_width - num_chars
                total_num_spaces += num_spaces
            return total_num_spaces

        def greedy_strategy(list_words,max_width):
            llwords = [[] for i in range(len(list_words))]
            ctr = container()
            greedy_strategy_(list_words,max_width,llwords,0,0,ctr)
            return

        def greedy_strategy_(list_words,max_width,llwords,i,irow,ctr):
            '''
            high level plan:
                for each word
                    if word length + current width < max:
                        add the word to current row
                        recursive call with the next row
                    else
                        recursive call with next row
                at the end of this, check if matrix was already calculated
                if not, then calculate the min score
            '''
            sz = len(list_words)
            width = 0

            for j in range(i,sz):
                word = list_words[j]
                tmp_width = width + len(word)
                if tmp_width < max_width:
                    llwords[irow].append(word)
                    width = tmp_width
                else:
                    greedy_strategy_(list_words,max_width,llwords,j,irow+1)
            total_num_spaces = score_matrix(list_words,llwords,max_width)
            if ctr.get_min_score() == None or ctr.get_min_score() > total_num_spaces:
                ctr.set_min_score(total_num_spaces)
                ctr.set_list_2d(llwords)

        def greedy_strategy_iterative_(list_words,max_width,llwords):
            ctr = container
            sz = len(list_words)
            sz_width = 0
            i_row = 0

            for i in range(sz):
                sz_word = len(list_words[i])
                if (sz_width + sz_word) >= max_width:
                    pass

                for j in range(j,sz):
                    pass
            pass

        def dp_bottom_up(list_words,width):
            pass

        def dp_top_down(list_words,max_width):
            list_list_placement = [[] for i in range(len(list_words))]
            dp = {}
            row = 0
            row_width = 80
            ctr = container(max_width*len(list_words))
            dp_top_down_(list_words,max_width,row,list_list_placement,dp,ctr)

        def dp_top_down_(list_words,max_width,list_idx,row,list_list_placement,dp,ctr):
            sz = len(list_words)
            for j in range(list_idx,sz):
                width = 0
                row_entries = list_list_placement[row]
                for entry in row_entries:
                    width += len(entry)
                if width >= max_width:
                    dp_top_down_(list_words,max_width,j,row+1,list_list_placement,dp,ctr)
                if (width + len(list_words[j])) < max_width:
                    list_list_placement[row].append(list_words[j])
                key = ','.join(list_list_placement[row])
                if key not in dp:
                    dp[key] = True
                    dp_top_down_(list_words,max_width,j+1,row+1,list_list_placement,dp,ctr)
            sum_spaces = 0
            num_rows = len(list_list_placement)
            num_rows = (num_rows - 1) if num_rows > 1 else num_rows # dont count the last row
            for i in range(num_rows):
                row_data = list_list_placement[i]
                sum_space_row = max_width
                for word in row_data:
                    sum_space_row -= len(word)
                sum_spaces += sum_space_row
            if sum_spaces < ctr.min:
                ctr.min = sum_spaces
        def t0():
            num_words = 1000
            sz_min = 1
            sz_max = 10
        pass

    def test_parenthesization(self):
        pass


    def test_enumeration(self):
        '''
        - list all possibilities of 5 over 5 rows
        -
            [0],[1],[2],[3],[4]
            [0],[1],[2],[3,4],[]
            [0],[1],[2,3],[4],[]
            [0],[1],[2,3,4],[],[]
            [0],[1,2],[3],[4],[]
            [0],[1,2],[3,4],[],[]
            [0],[1,2,3],[4],[],[]
            [0],[1,2,3,4],[],[],[]

            [0,1],[2],[3],[4],[]
            [0,1],[2],[3,4],[],[]
            [0,1],[2,3],[4],[],[]
            [0,1],[2,3,4],[],[],[]

            [0,1,2],[3],[4],[],[]
            [0,1,2],[3,4],[],[],[]

            [0,1,2,3],[4],[],[],[]

            [0,1,2,3,4],[],[],[],[]

        - list all possibilities of 7 items over 7 rows
        -
            [0],[1],[2],[3],[4],[5],[6]
            [0],[1],[2],[3],[4],[5,6],[]
            [0],[1],[2],[3],[4,5],[6],[]
            [0],[1],[2],[3],[4,5,6],[],[]
            [0],[1],[2],[3,4],[5],[6],[]
            [0],[1],[2],[3,4],[5,6],[],[]
            [0],[1],[2],[3,4,5],[6],[],[]
            [0],[1],[2],[3,4,5,6],[],[],[]
            [0],[1],[2,3],[4],[5],[6],[]
            [0],[1],[2,3],[4],[5,6],[],[]
            [0],[1],[2,3],[4,5],[6],[],[]
            [0],[1],[2,3],[4,5,6],[],[],[]
            [0],[1],[2,3,4],[5],[6],[],[]
            [0],[1],[2,3,4],[5,6],[],[],[]
            [0],[1],[2,3,4,5],[6],[],[],[]
            [0],[1],[2,3,4,5,6],[],[],[],[]
            [0],[1,2],[3],[4],[5],[6],[]
            [0],[1,2],[3],[4],[5,6],[],[]
            [0],[1,2],[3],[4,5],[6],[],[]
            [0],[1,2],[3],[4,5,6],[],[],[]
            [0],[1,2],[3,4],[5],[6],[],[]
            [0],[1,2],[3,4],[5,6],[],[],[]
            [0],[1,2],[3,4,5],[6],[],[],[]
            [0],[1,2],[3,4,5,6],[],[],[],[]
            [],[],[],[],[],[],[]
            [],[],[],[],[],[],[]
        '''

        def enumerate_list_recursive(n):
            def enumlistrec(ll_collection,ll,n,i):
                if i >= n:
                    ll_collection.append(copy.deepcopy(ll))
                    return
                row = []
                ll.append(row)
                for j in range(i,n):
                    row.append(j)
                    enumlistrec(ll_collection,ll,n,j+1)
                del ll[len(ll)-1]
            ll_collection = []
            ll = []
            enumlistrec(ll_collection,ll,n,0)
            return ll_collection

        def enumerate_list_iterative(n):
            ll_collection = []
            ll = []
            for i in range(n):
                row = []
                ll.append(row)
                for j in range(j,n):
                    pass
                ll_collection.append(copy.deepcopy(ll))
                del ll[len(ll)-1]
            return ll_collection

        def t0():
            ll_collection = enumerate_list_recursive(7)
            debug = True
            if debug:
                for collection in ll_collection:
                    p(collection)
                p('num collections: {}'.format(len(ll_collection)))
        t0()

    def test_fibonacci(self):
        '''
                      1
                    2   2
                   3  4  3
                 4  7   7  4
               5  11 14  11  5
              6 16 25  25  16 6


                      1
                    1   1
                  1   2   1
                1   3   3   1
              1   4   6   4   1
            1   5   10 10   5   1
          1   6  15  20  15   6   1

            0 1 1 2 3 5 8 13 21 34 55

        '''
        def fib1(n):
            '''
            0 1 1 2 3 5 8 13 21 34 55
            '''
            l = [1,1]
            for i in range(1,n-1):
                s = l[i] + l[i-1]
                l.append(s)
            return l

        def fib2(num_levels):
            '''
                      1
                    2   2
                   3  4  3
                 4  7   7  4
               5  11 14  11  5
              6 16 25  25  16 6

            '''
            l = [[1]]
            for i in range(1,num_levels):
                lnew = []
                lnew.append(i+1)
                lprv = l[i-1]
                for j in range(1,len(lprv)):
                    sum = lprv[j-1] + lprv[j]
                    lnew.append(sum)
                lnew.append(i+1)
                l.append(lnew)
            return l

        def fib3(num_levels):
            '''
                      1
                    1   1
                  1   2   1
                1   3   3   1
              1   4   6   4   1
            1   5   10 10   5   1
          1   6  15  20  15   6   1

            '''
            l = [[1]]
            for i in range(1,num_levels):
                lnew = []
                lnew.append(1)
                lprv = l[i-1]
                for j in range(1,len(lprv)):
                    sum = lprv[j-1] + lprv[j]
                    lnew.append(sum)
                lnew.append(1)
                l.append(lnew)
            return l

        def fib(n):
            sum = 0
            for i in range(n):
                sum += i

        def t0():
            sz = 10
            l = fib1(sz)
            assert l == [1,1,2,3,5,8,13,21,34,55]
            assert len(l) == sz
            return

        def t1():
            sz = 9
            l2 = fib2(sz)
            assert len(l2) == sz
            lexp2 = [
                           [1],
                          [2,2],
                         [3,4,3],
                        [4,7,7,4],
                      [5,11,14,11,5],
                     [6,16,25,25,16,6],
                    [7,22,41,50,41,22,7],
                  [8,29,63,91,91,63,29,8],
                [9,37,92,154,182,154,92,37,9]
            ]
            assert lexp2 == l2

            l3 = fib3(sz)
            assert len(l3) == sz
            lexp3 = [
                        [1],
                       [1,1],
                      [1,2,1],
                     [1,3,3,1],
                    [1,4,6,4,1],
                   [1,5,10,10,5,1],
                  [1,6,15,20,15,6,1],
                 [1,7,21,35,35,21,7,1],
                [1,8,28,56,70,56,28,8,1]
            ]
            assert l3 == lexp3
            return

        #t0()
        t1()

    def test_distribution(self):
        def test_uniform_concat():
            '''
            distribution of concatenating 1,2,3 combos
            <class 'dict'>: {
                0: 322,
                1: 350,
                2: 339,
                3: 317,
                4: 355,
                5: 319,
                6: 341,
                7: 309,
                8: 325,
                9: 356,
                }
            summing 2 numbers results in normal distribution
            <class 'dict'>: {
                0:  30,
                1:  77,
                2:  101,
                3:  131,
                4:  158,
                5:  204,
                6:  243,
                7:  242,
                8:  277,
                9:  348,
                10: 309,
                11: 266,
                12: 228,
                13: 206,
                14: 165,
                15: 138,
                16: 108,
                17: 72,
                18: 30
                }

            <class 'dict'>: {
                0:  1,
                1:  13,
                2:  20,
                3:  33,
                4:  47,
                5:  67,
                6:  114,
                7:  108,
                8:  144,
                9:  160,
                10: 212,
                11: 239,
                12: 240,
                13: 242,
                14: 238,
                15: 252,
                16: 222,
                17: 219,
                18: 173,
                19: 167,
                20: 124,
                21: 96,
                22: 89,
                23: 53,
                24: 35,
                25: 14,
                26: 9,
                27: 2,
                }
            '''
            num_samples = 10000
            lo=0
            hi=10
            results = numpy.random.randint(lo,hi,num_samples) # [lo,hi)
            l = [i for i in results]
            d0 = {}     # no concat distribution
            d1 = {}     # add 2 distro
            d2 = {}     # add 3 distro

            v = [0,0,0]
            j = 0
            for i in l:
                v[j] = i
                j += 1
                if j >= 3:
                    v0 = v[0]
                    v1 = v0 + v[1]
                    v2 = v1 + v[2]
                    if v0 not in d0:
                        d0[v0] = 0
                    if v1 not in d1:
                        d1[v1] = 0
                    if v2 not in d2:
                        d2[v2] = 0
                    d0[v0] += 1
                    d1[v1] += 1
                    d2[v2] += 1
                    j = 0
                    v = [0,0,0]
            return
        def test_normal_dist():
            '''
            std deviation of 1 with locus 10 has this sort of dist:
            <class 'dict'>: {
                13: 1,
                12: 23,
                11: 139,
                10: 331,
                9: 341,
                8: 146,
                7: 16,
                6: 3
                }
            '''
            loc = 10
            deviation = 1
            num_samples = 1000
            samples = numpy.random.normal(loc,deviation,num_samples)
            lf = [round(f,3) for f in samples]
            li = [int(f) for f in lf]
            d = {}
            for i in li:
                if i not in d:
                    d[i] = 0
                d[i] += 1
            assert abs(0 - numpy.mean(lf)) < 1
        def test_uniform_dist():
            '''
            <class 'dict'>: {
                0: 98,
                1: 106,
                2: 99,
                3: 104,
                4: 86,
                5: 88,
                6: 104,
                7: 101,
                8: 107,
                9: 107,
            }
            '''
            num_samples = 1000
            lo=0
            hi=10
            results = numpy.random.randint(lo,hi,num_samples) # [lo,hi)
            l = [i for i in results]
            d = {}
            for i in l:
                if i not in d:
                    d[i] = 0
                d[i] += 1
            for i in l:
                assert lo <= i and i <= hi
        def test():
            #test_normal_dist()
            #test_uniform_dist()
            test_uniform_concat()
        test()

    def test_min_window_substring(self):
        '''
        given string s and pattern t, find min window in s where all chars of t appear,
        in complexity O(s)

        if no such window, return ''
        '''
        def algos(s,t):
            szs = len(s)
            szt = len(t)
            d = { }
            count_uniques = 0
            idxs = 0
            minpair = None
            for c in t:
                d[c] = 0
            for i in range(szs):
                c = s[i]
                if c not in d:
                    continue
                d[c] += 1
                if d[c] == 1:
                    count_uniques += 1
                else:
                    # can this be trimmed?
                    while idxs <= i:
                        c1 = s[idxs]
                        if c1 not in d:
                            idxs += 1
                        elif d[c1] > 1:
                            idxs += 1
                            d[c1] -= 1
                        else:
                            break
                if count_uniques == szt:
                    if minpair == None:
                        minpair = [idxs,i]
                    else:
                        szcur = i - idxs + 1
                        szmin = minpair[1] - minpair[0] + 1
                        if szcur < szmin:
                            minpair = [idxs,i]
            if minpair == None or minpair[0] == minpair[1]:
                return ''
            return minpair
        def t():
            #    0         1
            #    0 2 4 6 8 0 2
            s = 'ADOBECODEBANC'
            t = 'ABC'
            v = algos(s,t)
            assert v == [9,12]
            pass
        t()
    def test_integer_to_roman(self):

        def i2r(ival):
            '''
            I       1
            V       5
            X       10
            L       50
            C       100
            D       500
            M       1000

            valid 1-3999

            1   I
            2   II
            3   III
            4   IV
            5   V
            6   VI
            7   VII
            8   VIII
            9   IX
            10  X
            11  XI
            12  XII
            13  XIII
            14  XIV
            15  XV
            16  XVI
            17  XVII
            18  XVIII
            19  XIX
            20  XX
            - evaluate 9
                IX
            - evaluate 78
                LXXVIII
            - evaluate 99
                XCIX    99 = (100-10) + (10-1)
            - evaluate 3999
                3999 = MMMCMXCIX
                     = 3000 + (1000-100) + (100-10) + (10-1)
                     = 3000 + 900        + 90       + 9

            eval left to right or right to left?
            '''

            def long_calculate(ival):
                s = ''
                base10 = 10
                while ival != 0:
                    mval = ival % base10
                    ival = ival - mval
                    if base10 == 10:
                        if mval == 1: s = 'I'
                        if mval == 2: s = 'II'
                        if mval == 3: s = 'III'
                        if mval == 4: s = 'IV'
                        if mval == 5: s = 'V'
                        if mval == 6: s = 'VI'
                        if mval == 7: s = 'VII'
                        if mval == 8: s = 'VIII'
                        if mval == 9: s = 'IX'
                    elif base10 == 100:
                        if mval == 10: s = 'X' + s
                        if mval == 20: s = 'XX' + s
                        if mval == 30: s = 'XXX' + s
                        if mval == 40: s = 'XL' + s
                        if mval == 50: s = 'L' + s
                        if mval == 60: s = 'LX' + s
                        if mval == 70: s = 'LXX' + s
                        if mval == 80: s = 'LXXX' + s
                        if mval == 90: s = 'XC' + s
                    elif base10 == 1000:
                        if mval == 100: s = 'C' + s
                        if mval == 200: s = 'CC' + s
                        if mval == 300: s = 'CCC' + s
                        if mval == 400: s = 'CD' + s
                        if mval == 500: s = 'D' + s
                        if mval == 600: s = 'DC' + s
                        if mval == 700: s = 'DCC' + s
                        if mval == 800: s = 'DCCC' + s
                        if mval == 900: s = 'CM' + s
                    elif base10 == 10000:
                        if mval == 1000: s = 'M' + s
                        if mval == 2000: s = 'MM' + s
                        if mval == 3000: s = 'MMM' + s
                    base10 = base10 * 10
                return s
            def short_calc(ival):
                def base10_to_r(mval,i,j,k):
                    if mval == 1: return '{}'.format(i)
                    if mval == 2: return '{}{}'.format(i,i)
                    if mval == 3: return '{}{}{}'.format(i,i,i)
                    if mval == 4: return '{}{}'.format(i,j)
                    if mval == 5: return '{}'.format(j)
                    if mval == 6: return '{}{}'.format(j,i)
                    if mval == 7: return '{}{}{}'.format(j,i,i)
                    if mval == 8: return '{}{}{}{}'.format(j,i,i,i)
                    if mval == 9: return '{}{}'.format(i,k)
                    return ''
                s = ''
                base10 = 10
                while ival != 0:
                    mval = ival % base10
                    ival = ival - mval
                    if base10 == 10:
                        s = base10_to_r(mval,'I','V','X')
                    elif base10 == 100:
                        mval = mval / 10
                        s = base10_to_r(mval,'X','L','C') + s
                    elif base10 == 1000:
                        mval = mval / 100
                        s = base10_to_r(mval,'C','D','M') + s
                    elif base10 == 10000:
                        mval = mval / 1000
                        s = base10_to_r(mval,'M','','') + s
                    base10 = base10 * 10
                return s
            s = short_calc(ival)
            return s
        def r2i(s):
            '''
            I       1
            V       5
            X       10
            L       50
            C       100
            D       500
            M       1000

            valid 1-3999

            1   I
            2   II
            3   III
            4   IV
            5   V
            6   VI
            7   VII
            8   VIII
            9   IX
            10  X
            11  XI
            12  XII
            13  XIII
            14  XIV
            15  XV
            16  XVI
            17  XVII
            18  XVIII
            19  XIX
            20  XX
            - evaluate 9
                IX
            - evaluate 78
                LXXVIII
            - evaluate 99
                XCIX    99 = (100-10) + (10-1)
            - evaluate 3999
                3999 = MMMCMXCIX
                     = 3000 + (1000-100) + (100-10) + (10-1)
                     = 3000 + 900        + 90       + 9

            eval left to right or right to left?
            '''
            d = {
                'I':1,
                'V':5,
                'X':10,
                'L':50,
                'C':100,
                'D':500,
                'M':1000
            }
            ival = 0
            p = None
            sz = len(s)
            # no rules validation here!
            for i in range(sz):
                c = s[i]
                if (p != None):
                    if d[p] < d[c]:
                        v = d[c] - d[p]
                        ival += v
                        p = None
                    else:
                        ival += d[p]
                        if (i == (sz-1)):
                            ival += d[c]
                        p = c
                else:
                    if (i == (sz-1)):
                        ival += d[c]
                    p = c
            return ival
        def t():
            v = i2r(3999)
            assert v == 'MMMCMXCIX'
            v = i2r(78)
            assert v == 'LXXVIII'
            v = i2r(1991)
            assert v == 'MCMXCI'
            v = i2r(1994)
            assert v == 'MCMXCIV'
            i = r2i('MMMCMXCIX')
            assert i == 3999
            i = r2i('LXXVIII')
            assert i == 78
            i = r2i('CXLI')
            assert i == 141
            i = r2i('MCMXCI')
            assert i == 1991
            i = r2i('MCMXCIV')
            assert i == 1994
        t()

    def test_interval_tree(self):
        def t0():
            bst = IntervalTree()
            lp = [[5,8],[15,18],[1,3],[7,9],[1,3],[19,23],[3,4],[2,6]]
            for p in lp:
                lo = p[0]
                hi = p[1]
                bst.add(lo,hi,do_merge=False)
            l = bst.get_inorder()
            for i in range(len(l)):
                n = l[i]
                n.print_vals(lo=True,hi=True)
        def t1():
            bst = IntervalTree()
            lp = [[5,8],[15,18],[1,3],[7,9],[1,3],[19,23],[3,4],[2,6]]
            lpsorted = [[1,3],[1,3],[2,6],[3,4],[5,8],[7,9],[15,18],[19,23]]
            lpmerged = [[1,9],[15,23]]
            for p in lp:
                lo = p[0]
                hi = p[1]
                bst.add(lo,hi,do_merge=True)
            l = bst.get_inorder()
            for i in range(len(l)):
                n = l[i]
                n.print_vals(lo=True,hi=True)
        t0()
        p('---------')
        t1()

    def test_intersecting_lines(self):
        def get_intersecting_lines_sweep_lines(n):
            pass
        def t0():
            pass
        t0()

    def test_binary_search(self):
        def binary_search_recursive(v,listval,l,r):
            if l > r:
                return None
            m = int((l+r+1)/2)
            if listval[m] == v:
                return m
            if listval[m] < v:
                return binary_search_recursive(v,listval,m+1,r)
            return binary_search_recursive(v,listval,l,m-1)
        def binary_search_iterative(v,listval):
            l = 0
            r = len(listval)

            while(l <= r):
                pass
            return None
        def t0():
            pass
        pass

    def test_basic_sort(self):
        '''
        put valmid at right edge
        then iterate idxleft:idxright. whenever val > valmid,
        shift valmid leftward and put val to val's place.
        at end of iteration, all elements smaller than valmid should be left
        and all elements bigger than valmid should be right. to
        handle equal values, then there has to be a group shift left for
        midval
        '''
        def swap(l,src,dst):
            v = l[src]
            l[src] = l[dst]
            l[dst] = v
        def partition_elements(l,il,ir):
            if ir <= il:
                return
            im = int((ir+il+1)/2)
            vm = l[im]
            swap(l,im,ir)
            til = il
            tir = ir
            while til < tir:
                if l[til] > vm:
                    l[tir] = l[til]
                    tir -= 1
                    l[til] = l[tir]
                    l[tir] = vm
                else:
                    til += 1
            partition_elements(l,il,tir-1)
            partition_elements(l,tir,ir)
        def partition_elements_with_duplicates(l,il,ir):
            '''
                0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 3
                0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0
                -------------------------------
                11122333456667889
                39431626835781621
                [3,9,4,3,1,6,2,6,8,3,5,7,8,1,6,2,1]

                partition and swap repeated starting from bottom up

                0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 3
                0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0
                -------------------------------
                39431626835781621
                L       M       R   calculate M and swap all elements left and right with 3 groups
                                    X<VM,X==VM,X>VM
                39431626835781621   orig -> swap VM to R
                        |       |
                39431626135781628   now do X<VM,X==VM,X>VM
                3               8   cmp no change
                 9              8   start shift swap
                 2             89   end shift swap
                  4            8    cmp no change
                   3           8    cmp no change
                    1          8    cmp no change
                     6         8    cmp no change
                      2        8    cmp no change
                       6       8    cmp no change
                        1      8    cmp no change
                         3     8    cmp no change
                          5    8    cmp no change
                           7   8    cmp no change
                            8  8    start shift swap
                            6 88    end shift swap
                             188    cmp no change
                32431626135761889   end this iteration, split evaluate
                0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 3
                0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0
                -------------------------------
                L       RL      R
                324316261           partition 0
                         35761889   partition 1
                |   M   |           got midpoint, now swap to R and do X<VM,X==VM,X>VM
                324316261
                3       1           cmp start shift swap
                6      13           end shift swap, cmp start swap
                2     163           cmp end shift swap, cmp start swap
                6    1263           cmp end shift swap, cmp start swap
                1   16263           cmp end shift swap, cmp start swap
                3  116263           cmp end shift swap, cmp start swap
                4 1146263           cmp end shift swap, cmp start swap
                211446263           cmp start shift swap


                this method is wrong because you have to again sort partition 1
                you were supposed to recursively go down by the partition value, not midpoint

                and the mistake was doing split, eval partition 0 by partition. the right thing was
                1. get top level midpoint, and do comparison with VM, then split recursively at
                   resulting V as R and L+1 for recursive partitions. let's try this again


                0 0 0 0 0 1 1 1 1
                0 2 4 6 8 0 2 4 6
                -----------------
                11122333456667889

                39431626835781621
                L       M       R   start cmp swap now instead of earlier partition then cmp
                        1       8   swap VM to right and start iterative cmp
                3               8   cmp no change
                 9              8   cmp start swap
                 2             89   cmp end swap
                 24316261357   89   cmp no changes
                            8  89   cmp start swap
                            6 889   cmp end swap
                             1889   cmp no change
                32431626135761889   complete sequence, now recurse at VM begin
                L            RL R   partition 0 and partition 1
                32431626135761      (0+13+1)/2 = 7 midpoint, do swap and start cmp
                L      M     R
                       6     1      start cmp, VM = 6
                32431621135766
                32431               cmp no change
                     6       6      start swap
                     6      66      end swap, start swap
                     7     666      end swap, start swap
                     5    6667      end swap
                     52113          complete sequence, no recurse at VM begin
                32431521136667
                L        RL  R      (0+9+1)/2 = 5 midpoint idx = VM 5
                3243152113
                     5   3          swap and start with VM = 5
                3243132115
                324313211           cmp no changes, recurse, so R partition is not recursable
                0 0 0 0 0 1 1 1 1
                0 2 4 6 8 0 2 4 6
                -----------------
                L       R           (0+8+1)/2=4
                L   M   R           VM = 1, swap and start cmp
                324313211
                    1   1
                3       1           swap start
                1      13           swap end, swap start
                2     113           swap end, swap start
                3    1123           swap end, swap start
                1   11323           swap end, swap start
                3  111323           swap end, swap start
                4 1113323           swap end, swap start
                211143323           swap end, swap start
                111243323           complete sequence, recurse at VM 1, so no left recurse
                   243323
                0 0 0 0 0 1 1 1 1
                0 2 4 6 8 0 2 4 6
                -----------------
                   L    R           (3+8+1)/2 = 6, VM = 3
                   243323
                      3 3           start cmp
                   2    3
                    4   3           start swap
                    2  34           end swap
                     3 3            start swap
                     3334           end swap, end sequence, recurse
                   223334           at this point, when recursing to the others, they are sorted
                  |      |   |889
                  |      |6667
                  |      5
                111
                11122333456667889   here is end result of merging each of the partitions
            '''
            if ir <= il:
                return
            im = int((il+ir+1)/2)
            vm = l[im]
            tl = il
            tr = ir
            idxMEnd = tr
            duplicate_detected = False

            #p('VMI = {} VM = {}'.format(im,vm))
            #p('VMI SWAP BEFORE: {}'.format(l))
            swap(l,im,ir)
            #p('VMI SWAP AFTER : {}'.format(l))
            while tl < tr:
                if l[tl] < l[tr]:
                    tl += 1
                elif l[tl] == l[tr]:
                    tr -= 1
                    #p('before =:        {}'.format(l))
                    swap(l,tl,tr)
                    #p('after  =:        {}'.format(l))
                    duplicate_detected = True
                else:
                    #p('before >:        {}'.format(l))
                    if duplicate_detected:
                        tr -= 1
                        swap(l,tl,tr)
                        swap(l,tr,idxMEnd)
                        idxMEnd -= 1
                    else:
                        swap(l,tl,tr-1)
                        swap(l,tr-1,tr)
                        tr -= 1
                        idxMEnd = tr
                    #p('after  >:        {}'.format(l))
            if duplicate_detected:
                partition_elements_with_duplicates(l,il,tr-1)
                partition_elements_with_duplicates(l,idxMEnd+1,ir)
            else:
                partition_elements_with_duplicates(l,il,tr-1)
                partition_elements_with_duplicates(l,tr,ir)

        def t_noduplicates():
            lo = [i for i in range(10)]
            lo = self.utils.shuffle(lo)
            li = lo.copy()
            partition_elements(li,0,len(li)-1)
            assert li == [0,1,2,3,4,5,6,7,8,9]

            li = lo.copy()
            partition_elements_with_duplicates(li,0,len(li)-1)
            assert li == [0,1,2,3,4,5,6,7,8,9]

        def t_duplicates():
            l = [3,9,4,3,1,6,2,6,8,3,5,7,8,1,6,2,1]
            partition_elements_with_duplicates(l,0,len(l)-1)
            assert l == [1,1,1,2,2,3,3,3,4,5,6,6,6,7,8,8,9]
        t_noduplicates()
        t_duplicates()

    def test_sort_quicksort(self):
        pass

    def test_k_sort(self):
        pass

    def test_graph_acyclic_vs_cyclic(self):
        def test_cyclic_0():
            g = GraphSamples.get_graph_0()
            set_src_nodes = g.get_all_sources()
            cyclic_node   = g.is_cyclic()
            assert cyclic_node == None

        def test_cyclic_1():
            g = GraphSamples.get_graph_1()
            set_src_nodes = g.get_all_sources()
            cyclic_node   = g.is_cyclic()
            assert cyclic_node != None


        test_cyclic_0()
        test_cyclic_1()

    def test_topological_sort(self):
        def t0():
            g = GraphSamples.get_graph_0()
            ll = g.get_all_topologies()
            assert len(ll) == 12

            '''
            12 possible paths
            0 1 5 8
            0 1 5 9
            0 2 5 8
            0 2 5 9
            0 3 6 8
            0 3 6 9
            0 3 7 10
            4 2 5 8
            4 2 5 9
            4 3 6 8
            4 3 6 9
            4 3 7 10
            '''
        def t1():
            g = GraphSamples.get_graph_2()
            ll = g.get_all_topologies()
            assert len(ll) == 11
            '''
            0 1 5 8 11
            0 2 5 8 11
            0 3 6 11
            0 3 6 9
            0 3 7 10
            0 3 7 12
            4 2 5 8 11
            4 3 6 11
            4 3 6 9
            4 3 7 10
            4 3 7 12
            '''
        t0()
        t1()

    def test_merge_intervals(self):
        def merge_intervals_bst(lpairs):
            '''
            given list of pair segments [x,y), merge overlapping segments

            you cannot use interval tree to merge intervals because the pairs
            are unsorted. this means you might update the parent node with merge,
            but children node that should have merged, did not merge

            you still have to use a sorted list to merge
            '''
            bst = IntervalTree()
            for pair in lpairs:
                lo = pair[0]
                hi = pair[1]
                bst.add(lo,hi,do_merge=True)
            l = bst.get_inorder()
            return l
        def merge_intervals_list(lpairs):
            lsorted = sorted(lpairs,key = lambda x: x[0]) # sort by lo
            prv = None
            lmerged = []
            for pair in lsorted:
                if prv == None:
                    lmerged.append([pair[0],pair[1]])
                    prv = pair
                else:
                    if prv[0] <= pair[0] and pair[0] <= (prv[1]+1):
                        lmerged[len(lmerged)-1][1] = pair[1]
                        prv = lmerged[len(lmerged)-1]
                    else:
                        lmerged.append([pair[0],pair[1]])
                        prv = pair
            return lmerged
        def t0():
            lpairs = [[1,3],[2,6],[8,10],[15,18]]
            l = merge_intervals_bst(lpairs)
            for i in range(len(l)):
                n = l[i]
                n.print_vals(lo=True,hi=True)
        def t1():
            lpairs = [[1,3],[2,6],[8,10],[15,18]]
            l = merge_intervals_list(lpairs)
            for i in range(len(l)):
                print(l[i])
        t1()

    def test_LLN_functions(self):
        e = 12345
        n = LLN.convert_num_2_lln(e)
        a = LLN.convert_lln_2_num(n)
        assert a == 12345
        nr = LLN.reverse_lln(n)
        ar = LLN.convert_lln_2_num(nr)
        assert ar == 54321
        nrr = LLN.reverse_lln(nr)
        arr = LLN.convert_lln_2_num(nrr)
        assert a == 12345


    def test_add_two_numbers_reverse_linked(self):
        def add_xy_reverse_linked_list(ll0:LLN, ll1:LLN) -> LLN:
            '''
            input: ll0, ll1 where ll0/1 are reverse linked lists. add ll0 + ll1
            out:  ll2
                    eg 6->5->4 + 4->5->6->1 => 456 + 1654 = 2110 => 0->1->1->2
            '''
            ll2 = LLN()
            t0 = ll0
            t1 = ll1
            t2 = ll2
            carry = 0
            while t0 != None or t1 != None:
                v = carry
                if t0 != None:
                    v += t0.get_v()
                    t0 = t0.get_np()
                if t1 != None:
                    v += t1.get_v()
                    t1 = t1.get_np()
                carry = 1 if v >= 10 else 0
                t2.set_v(v)
                if carry != 0 or t0 != None or t1 != None:
                    tmp = LLN()
                    t2.set_np(tmp)
                    t2 = tmp
            return ll2
        def t0():
            pass
        t0()

    def main(self):
        p('main passed')

if __name__ == "__main__":
    unittest.main() # not ut.main()!



'''
s1  0123
s2  4567

interleave values:
combination tree

0 1 2 3 4 5 6 7
    4 2 3 5 6 7
      5 
  4 1 2 3 5 6 7
    
4 0 1 2 3 5 6 7
  5 0 1 2 3 6 7
    

'''


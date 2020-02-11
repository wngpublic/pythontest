#!/usr/local/bin/python3

import sys
import os
import os.path
import getopt
import fileinput
import subprocess
import re
import string
import copy
import math
import calendar
import cmd
import collections
from collections import OrderedDict
from collections import deque
import urllib.request as url
import pathlib
from src.main import myclasses
from src.algos import algos
import json
import unittest
import argparse
from src.main import gossip
import abc
import gzip
import multiprocessing
from src.main import asynciotests
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
import argparse

global_output_to_file_ = False
global_fh_ = None
global_debug_level_ = 0

def p(s):
    global global_output_to_file_
    global global_fh_
    print(s)
    if(global_output_to_file_):
        if(global_fh_ is None):
            global_fh_ = open('output_debug.log','w')
        global_fh_.write(s + '\n')

def set_debug_level(debuglevel):
    global global_debug_level_
    global_debug_level_ = debuglevel

def d(s,debuglevel=1):
    global global_debug_level_
    if(global_debug_level_ == 0):
        return
    if(global_debug_level_ < debuglevel):
        return
    p(s)

class TestAlgos:
    def __init__(self):
        pass

    @staticmethod
    def test_catalon(size):
        '''
        6
        (
          ()
            ()(
              ()()
                ()()(
                  ()()()    O
                ()())       X
              ()((
                ()(()
                  ()(())    O
                ()(((       X
            ())             X
          ((
            (()
              (())
                (())(
                  (())()    O
                  (())((    X
                (()))       X
              (()(
                (()()
                  (()())    O
                  (()()(    X
                (()((       X
            (((
              ((((          X
              ((()
                ((()(       X
                ((())
                  ((())(    X
                  ((()))    O
        '''
        def dfss1(s, l, lp, c, size):
            if c == ')':
                if len(s) == 0: return False
                p = s.pop()
                if p == ')':
                    s.append(')')
                    return False
                if p == '(':
                    l.append(')')
            else:
                s.append('(')
                l.append('(')

            if len(l) == size:
                if(len(s) == 0): lp.append(''.join(l))
                return True

            if dfss1(s,l,lp,'(',size):
                l.pop()
            if dfss1(s,l,lp,')',size):
                l.pop()
            return True

        def dfss(s, l, lp, c, size):
            s = s.copy()
            l = l.copy()
            if c == ')':
                if len(s) == 0: return
                p = s.pop()
                if p == ')':
                    s.append(')')
                    return
                if p == '(':
                    l.append(')')
            else:
                s.append('(')
                l.append('(')

            if len(l) == size:
                if(len(s) == 0): lp.append(''.join(l))
                return

            dfss(s,l,lp,'(',size)
            dfss(s,l,lp,')',size)

        def testdfss(size):
            if size % 2 != 0: return
            s = []
            l = []
            lp = []
            dfss(s, l,lp,'(', size)     # works
            #dfss1(s, l,lp,'(', size)

            for i in range(len(lp)):
                p('{:3} {}'.format(i, lp[i]))
            # validate
            set1 = set()
            for i in range(len(lp)):
                if lp[i] in set1:
                    p('{} duplicate in set'.format(lp[i]))
                    assert False
                set1.add(lp[i])

        testdfss(6)
        p('pass test_catalon')
        pass

    def testCatchRainwater3d(self, a, r, i, j, pv):
        max = len(a)

        if i < 0 or i >= max or j < 0 or j >= max:
            return

        cv = r[i][j]

        if(cv != -1 or cv > pv):
            return

        if(r[i][j] >= a[i][j]):
            pass

        self.testCatchRainwater3d(a, r, i-1, j-1, cv)
        self.testCatchRainwater3d(a, r, i-1, j,   cv)
        self.testCatchRainwater3d(a, r, i-1, j+1, cv)

        self.testCatchRainwater3d(a, r, i+1, j+1, cv)
        self.testCatchRainwater3d(a, r, i+1, j,   cv)
        self.testCatchRainwater3d(a, r, i+1, j-1, cv)

        self.testCatchRainwater3d(a, r, i,   j+1, cv)
        self.testCatchRainwater3d(a, r, i,   j-1, cv)

    def testCatchRainwater3d(self):
        max = 5
        a = [
            [7,8,7,7,6],
            [8,4,5,3,7],
            [7,3,4,3,8],
            [8,5,6,7,9],
            [8,4,5,8,8]
        ]
        r = [[-1 for i in range(max)] for j in range(max)]
        for i in range(max):
            for j in range(max):
                self.testCatchRainwater3d(a, r, i, j, None)


    def test(self, argv):
        '''
        '''
        TestAlgos.test_catalon(5)
        pass

def maintestalgos():
    global global_fh_
    t = TestAlgos()
    parser = argparse.ArgumentParser()
    parser.add_argument('-debuglevel', type=int, help='debuglevel 0-5')
    parser.add_argument('-tc', help='-tc with methodname')
    args = parser.parse_args()
    if(args.debuglevel is not None):
        set_debug_level(args.debuglevel)
    d(args)
    if(args.tc is not None):
        methodname = args.tc
        getattr(t, methodname)()
    else:
        t.test(None)
    if(global_fh_ is not None):
        global_fh_.close()

maintestalgos()
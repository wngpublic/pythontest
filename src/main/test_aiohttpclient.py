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

def p(s):
    print(s)

class TestAioHttpClient:
    def __init__(self):
        self.tsem = threading.Semaphore(value=4)
        self.asem = asyncio.Semaphore(value=4)

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

    def process_test(self, methodname):
        result = getattr(self, methodname)()

        #if(methodname == 'test_thread_semaphore'):
        #    self.test_thread_semaphore()
        #if(methodname == 'test_asyncio_semaphore'):
        #    self.test_asyncio_semaphore()

    def process(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-test', type=str, help='test methodname')
        parser.add_argument('-url', help='url')
        parser.add_argument('-num', type=int, help='num types to call url')
        args = parser.parse_args()
        tbeg = time.time_ns()
        if args.test is not None:
            self.process_test(args.test)
        tend = time.time_ns()
        tdif = (tend - tbeg)/1_000_000
        p('\ncompleted. time diff {} ms'.format(tdif))


t = TestAioHttpClient()
t.process()



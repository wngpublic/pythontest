#!/usr/local/bin/python3
import asyncio
import time
import concurrent.futures
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import random
import threading
import queue
from enum import Enum
import aiohttp
import argparse
import sys

def p(s):
    print(s)

class SYNCTYPE1(Enum):
    SYNC = 0,
    ASYNC = 1

class AsyncIOTests:
    #
    # cases to try:
    # IO bound cases:
    #   submit 5 tasks at a time into 2 thread pool, and allow them to finish
    #   before submitting the next 5 tasks.
    #
    #   continuously submit 5 tasks into 2 thread pool, to limit memory and cpu
    #
    #   in same above cases, block the thread from switching
    #
    #   in same above cases, do not block thread from switching
    #
    def __init__(self):
        self.threadPoolExecutor = ThreadPoolExecutor(2)
        self.processPoolExecutor = ProcessPoolExecutor(2)
        self.tsem = threading.Semaphore(value=4)
        self.asem = asyncio.Semaphore(value=4)
        pass

    async def foo1(self):
        print('start foo 1')
        await asyncio.sleep(1)
        print('end   foo 1')

    async def foo2(self):
        print('start foo 2')
        await asyncio.sleep(1)
        print('end   foo 2')

    async def asyncfoo1foo2(self):
        t = [self.foo1(), self.foo2()]
        await asyncio.gather(*t)

    def foo1foo2(self):
        asyncio.run(self.asyncfoo1foo2())

    def foo1sleep(self, id, ms):
        t = ms / 1000
        p('start id %3d for %d ms' % (id, ms))
        time.sleep(t)
        p('end   id %3d for %d ms' % (id, ms))

    async def foo2sleep(self, id, ms):
        t = ms / 1000
        p('start id %3d for %d ms' % (id, ms))
        await asyncio.sleep(t)
        p('end   id %3d for %d ms' % (id, ms))

    def test_sleep1(self):
        asyncio.run(self.foo2sleep(2,200))
        self.foo1sleep(1,100)

    def test_task_submit_sync(self):
        exe = futures.ThreadPoolExecutor(3)
        l = []
        for i in range(5):
            future = exe.submit(self.foo1sleep, i, 100)
            l.append(future)
        ctr = 0
        for future in futures.as_completed(l):
            ctr += 1

    def futureBlocking(self, id, ms):
        t = ms / 1000
        #p('start id %3d for %d ms' % (id, ms))
        time.sleep(t)
        #p('end   id %3d for %d ms' % (id, ms))

    def futureBlockingReturn(self, id, ms):
        t = ms / 1000
        #p('start id %3d for %d ms' % (id, ms))
        time.sleep(t)
        #p('end   id %3d for %d ms' % (id, ms))
        return id

    def testExecutorPoolsAndFutures1(self):
        num_runs = 8
        sleep_ms = 50
        set = {0,1,2,3,4,5,6,7}

        p('start run 1')
        ctr = 0
        lfutures = []
        for i in range(num_runs):
            future = self.threadPoolExecutor.submit(self.futureBlocking, i, sleep_ms)
            lfutures.append(future)
        for future in concurrent.futures.as_completed(lfutures):
            assert future.result() == None
            ctr += 1
        assert ctr == num_runs

        # this is the same as above, as_completed, result
        p('start run 2')
        ctr = 0
        lfutures = []
        for i in range(num_runs):
            future = self.threadPoolExecutor.submit(self.futureBlocking, i, sleep_ms)
            lfutures.append(future)
        for future in lfutures:
            assert future.result() == None
            ctr += 1
        assert ctr == num_runs

        # this is the same as above, as_completed, result
        p('start run 3')
        lfutures = []
        for i in range(num_runs):
            future = self.threadPoolExecutor.submit(self.futureBlocking, i, sleep_ms)
            lfutures.append(future)
        results = concurrent.futures.wait(lfutures)
        assert len(results.done) == num_runs
        assert len(results.not_done) == 0

        p('start run 4')
        ctr = 0
        lfutures = []
        for i in range(num_runs):
            future = self.threadPoolExecutor.submit(self.futureBlockingReturn, i, sleep_ms)
            lfutures.append(future)
        for future in lfutures:
            assert future.result() in set
            ctr += 1
        assert ctr == num_runs

        p('start run 5')
        ctr = 0
        lfutures = []
        for i in range(num_runs):
            future = self.threadPoolExecutor.submit(self.futureBlockingReturn, i, sleep_ms)
            lfutures.append(future)
        for future in concurrent.futures.as_completed(lfutures): # any order
            assert future.result() in set
            ctr += 1
        assert ctr == num_runs

        p('start run 6')
        ctr = 0
        lfutures = []
        for i in range(num_runs):
            future = self.threadPoolExecutor.submit(self.futureBlockingReturn, i, sleep_ms)
            lfutures.append(future)
        #results = concurrent.futures.wait(lfutures,timeout=60,return_when=futures.ALL_COMPLETED) # wait for all
        results = concurrent.futures.wait(lfutures,return_when=futures.ALL_COMPLETED) # wait for all
        assert len(results.done) == num_runs
        assert len(results.not_done) == 0
        lresults = []
        for result in results.done:
            assert result.result() in set
            lresults.append(result.result())

        p('these results not in order for 2 thread pool with 8 tasks!')
        #for result in lresults:
        #    p(result)

        p('\ndone testExecutorPoolsAndFutures1\n')

    async def test_task_submit_async(self):
        exe = futures.ThreadPoolExecutor(3)
        loop = asyncio.new_event_loop()
        l = []
        for i in range(5):
            future = loop.run_in_executor(exe, self.foo2sleep, i, 100)
            l.append(future)
        results = await asyncio.gather(*l)
        ctr = 0
        for future in futures.as_completed(l):
            ctr += 1

    def thread_consume(self, num_consume, q, qresult):
        for i in range(num_consume):
            qresult.put(q.get())

    def thread_produce(self, num_produce, start_idx, q):
        for i in range(start_idx, start_idx + num_produce):
            q.put(i)

    def test_queue(self):
        queue_unsafe = asyncio.Queue(8)    # blocking not thread safe queue
        queue_safe = queue.Queue(5)
        q = queue_safe
        qresult = queue.Queue()
        num_produce = 200
        num_threads_consume = 2
        num_threads_produce = 2
        num_consume = int(num_produce / num_threads_consume)
        delta = int(num_produce/num_threads_produce)

        lthreads = []
        for i in range(num_threads_consume):
            t = threading.Thread(target=self.thread_consume, args=(num_consume, q, qresult))
            t.setDaemon(True)
            lthreads.append(t)
        for i in range(num_threads_produce):
            t = threading.Thread(target=self.thread_produce, args=(delta, i * delta, q))
            lthreads.append(t)

        for t in lthreads:
            t.start()
        [t.join() for t in lthreads]

        assert qresult.qsize() == num_produce
        l = []
        while not qresult.empty():
            l.append(qresult.get())
        assert len(l) == num_produce

        # check that producer to consumer are all unique
        l_sorted = sorted(l)
        cmp = 0
        for v in l_sorted:
            assert v == cmp
            cmp += 1
        p('done test_queue')

    # a sleep just blocks the thread, does not hand off control
    # each time anticipated IO event occurs, yield/await and hand off control
    async def test_sync_vs_async_handoff_sync_vs_async_version(self, synctype1, id, sleep_ms):
        sleep_s = sleep_ms / 1000
        tbeg = time.time_ns()
        if synctype1 == SYNCTYPE1.SYNC:
            p('sleep beg id: {} sync {}'.format(id, sleep_ms))
            time.sleep(sleep_s) # this is not awaitable!
        if synctype1 == SYNCTYPE1.ASYNC:
            p('sleep beg id: {} async {}'.format(id, sleep_ms))
            await asyncio.sleep(sleep_s)
        tend = time.time_ns()
        tdiff_ms = int((tend - tbeg)/1_000_000)
        p('sleep end id: {} elapsed_time_ms {}'.format(id, tdiff_ms))
        return id

    async def test_sync_vs_async_handoff_caller(self, synctype1, id, retval, sleep_ms=None):
        if sleep_ms is None:
            sleep_ms = random.randint(1000,2000)
        p('test_sync_vs_async_handoff_caller beg {}'.format(id))
        await self.test_sync_vs_async_handoff_sync_vs_async_version(synctype1, id, sleep_ms)
        p('test_sync_vs_async_handoff_caller end {}'.format(id))
        return retval

    def test_sync_vs_async_handoff_wrapper(self, num_tasks, synctype1):
        try:
            lfutures = []
            for id in range(num_tasks):
                '''
                ensure_future(task) schedules in loop, but does not run.
                use run_until_complete(task) or loop.run_forever() to start running
                keep in mind loop.run_forever() is blocking forever
                
                don't call both ensure_future(task) AND loop.run_until_complete(task) or
                you'll run into error because some tasks will have already been scheduled
                use 
                    ensure_future(task) AND loop.run_until_complete(future) 
                    but NOT
                    ensure_future(task) AND loop.run_until_complete(task)
                '''
                lfutures.append(asyncio.ensure_future(self.test_sync_vs_async_handoff_caller(synctype1, id, random.randint(0,99), 1000)))
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(lfutures))
            for future in lfutures:
                p('result {}'.format(future.result()))
        except Exception as e:
            print(e)
        finally:
            pass
            #loop.close()

    def test_asyncio_gather(self, num_tasks):
        '''
        run blocking vs non blocking performance using gather
        :param num_tasks:
        :return:
        '''
        #futures = [long_task(i) for i in inputs]
        #results = await asyncio.gather(*futures)
        try:
            pass
        except Exception as e:
            print(e)
        finally:
            pass

        pass

    def test_create_task(self, num_tasks):
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(self.test_sync_vs_async_handoff_caller(SYNCTYPE1.ASYNC, 10, 20, 100))
        except Exception as e:
            pass
        finally:
            pass

    def test_multiprocessing_pool(self, num_processes):
        try:
            executor = ProcessPoolExecutor(4)
            pass
        except Exception as e:
            pass
        finally:
            pass

    async def test_tasks_1_wrapper(self):
        tasks = [self.test_sync_vs_async_handoff_sync_vs_async_version(SYNCTYPE1.ASYNC, 1, 10),
                 self.test_sync_vs_async_handoff_sync_vs_async_version(SYNCTYPE1.ASYNC, 2, 10)]
        await asyncio.gather(*tasks)

    def test_tasks_1(self):
        asyncio.run(self.test_tasks_1_wrapper())

    # demos asyncio.sleep vs time.sleep, where asyncio passes control to event_loop and time does not
    def test_sync_vs_async_handoff(self):
        try:
            loop = asyncio.get_event_loop()

            tbeg = time.time_ns()
            self.test_sync_vs_async_handoff_wrapper(5, SYNCTYPE1.SYNC)
            tend = time.time_ns()
            tms = int((tend - tbeg)/1_000_000)
            p('tdiff ms: {} sync version'.format(tms))

            p('-----------------------------')

            tbeg = time.time_ns()
            self.test_sync_vs_async_handoff_wrapper(5, SYNCTYPE1.ASYNC)
            tend = time.time_ns()
            tms = int((tend - tbeg)/1_000_000)
            p('tdiff ms: {} async version'.format(tms))
            p('-----------------------------')

        finally:
            loop.close()
            p('done')

    def test_wrapper(self):
        #self.test_sleep1()
        #self.test_task_submit_sync()
        #self.test_task_submit_async()
        #self.testExecutorPoolsAndFutures1()
        #self.test_queue()
        self.test_sync_vs_async_handoff()
        #self.test_tasks_1()

    def test(self):
        ns1 = time.time_ns()

        self.test_wrapper()

        ns2 = time.time_ns()
        diff_ms = (ns2 - ns1)/1_000_000
        print('done AsyncIOTests %d ms' % diff_ms)

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
        #self.test_sleep1()
        #self.test_task_submit_sync()
        #self.test_task_submit_async()
        #self.testExecutorPoolsAndFutures1()
        #self.test_queue()
        #self.test_tasks_1()
        '''
        if(methodname == 'test_sync_vs_async_handoff'):
            self.test_sync_vs_async_handoff()
        if(methodname == 'test_thread_semaphore'):
            self.test_thread_semaphore()
        if(methodname == 'test_asyncio_semaphore'):
            self.test_asyncio_semaphore()
        '''

        result = getattr(self, methodname)()

    def process(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-test', type=str, help='test methodname')
        args = parser.parse_args()
        tbeg = time.time_ns()
        if args.test is not None:
            self.process_test(args.test)
        else:
            sys.exit('./script -test <methodname>')
        tend = time.time_ns()
        tdif = (tend - tbeg)/1_000_000
        p('\ncompleted. time diff {} ms'.format(tdif))

t = AsyncIOTests()
t.process()
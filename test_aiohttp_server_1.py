#!/usr/local/bin/python3

from aiohttp import web
import asyncio
import random
import requests
import sys
from aiohttp import ClientSession
from aiohttp import web
from itertools import islice

'''
hello, this aiohttp stuff is copied from examples online about large 
number of concurrent and limited requests with aiohttp
'''

async def handle(request):
    await asyncio.sleep(random.randint(0, 3))
    return web.Response(text="Hello, World!")

async def init(loop):
    app = web.Application()
    app.router.add_route('GET', '/{name}', handle)
    #app.router.add_get('/{name}', handle)
    return await loop.create_server(
        app.make_handler(), '127.0.0.1', 8080)

def run_server():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()

def run_client():
    url = "http://localhost:8080/{}"
    for i in range(int(sys.argv[1])):
        requests.get(url.format(i)).text

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()

async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)

async def run(session, r):
    limit = 1000
    url = "http://localhost:8080/{}"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(limit)
    for i in range(r):
        # pass Semaphore and session to every GET request
        task = asyncio.ensure_future(bound_fetch(sem, url.format(i), session))
        tasks.append(task)
    responses = asyncio.gather(*tasks)
    await responses

def run_client_session():
    loop = asyncio.get_event_loop()
    with ClientSession() as session:
        loop.run_until_complete(asyncio.ensure_future(run(session, int(sys.argv[1]))))


def limited_as_completed(coros, limit):
    futures = [
        asyncio.ensure_future(c)
        for c in islice(coros, 0, limit)
    ]
    async def first_to_finish():
        while True:
            await asyncio.sleep(0)
            for f in futures:
                if f.done():
                    futures.remove(f)
                    try:
                        newf = next(coros)
                        futures.append(
                            asyncio.ensure_future(newf))
                    except StopIteration as e:
                        pass
                    return f.result()
    while len(futures) > 0:
        yield first_to_finish()

async def print_when_done(tasks):
    limit = 1000
    for res in limited_as_completed(tasks, limit):
        await res

def _on_task_done(self, task):
    self._tasks.remove(task)
    self._semaphore.release()

def p(s):
    print(s)

def run_client_session_2():
    r = int(sys.argv[1])
    url = "http://localhost:8080/{}"
    loop = asyncio.get_event_loop()
    with ClientSession() as session:
        coros = (fetch(url.format(i), session) for i in range(r))
        loop.run_until_complete(print_when_done(coros))
    loop.close()

def main(argv):
    if len(argv) == 0:
        p('no args for test_aiohttp_server_1')
        return
    if argv[0] == 'server':
        p('run server')
        run_server()
    elif argv[0] == 'client':
        p('run client')
        run_client()
    pass

main(sys.argv[1:])


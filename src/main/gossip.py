#!/usr/local/bin/python3

import random

def p(s):
    print(s)

class ACtr:
    id = 0
    @staticmethod
    def getAndInc():
        v = ACtr.id
        ACtr.id += 1
        return v
    @staticmethod
    def reset():
        ACtr.id = 0

class MyNodeGossip:
    def resetTables(self):
        self.ns = {}
        self.ns['g'] = set()
        self.ns['b'] = set()
        self.cs = {}
        self.cs['g'] = set()
        self.cs['b'] = set()
        self.cs['g'].add(self.id)
        self.changeset = {}
        self.changeset['g'] = set()
        self.changeset['b'] = set()

    def __init__(self,router=None,fanout=2,ttl=3):
        self.id = ACtr.getAndInc()
        self.name = '{}_{}'.format('name',self.id)
        self.router = router
        self.fanout = fanout
        self.isDisconnected = False
        self.ttl = ttl
        self.ttlcur = self.ttl
        self.resetTables()

    def addnodeid(self,id):
        self.ns['g'].add(id)

    def randint(self,max):
        return random.randint(0,max) # [0,max] not [0,max)

    def p(self):
        p(self.getinfo())

    def getinfo(self):
        s = 'ID:{:>2} '.format(self.id)
        if len(self.cs['g']) == 0:
            s += 'G: {} '.format(None)
        else:
            s += 'G: {} '.format(self.cs['g'])
        if len(self.cs['b']) == 0:
            s += 'B: {} '.format(None)
        else:
            s += 'B: {} '.format(self.cs['b'])
        return s

    def updateCS(self):
        if self.isDisconnected:
            return
        self.changeset['g'].clear()
        self.changeset['b'].clear()
        for id in self.ns['b']:
            if id not in self.cs['b'] or id in self.cs['g']:
                self.changeset['b'].add(id)
            if id in self.cs['g']:
                self.cs['g'].remove(id)
            self.cs['b'].add(id)
        for id in self.ns['g']:
            if id not in self.cs['g'] or id in self.cs['b']:
                self.changeset['g'].add(id)
            if id in self.cs['b']:
                self.cs['b'].remove(id)
            self.cs['g'].add(id)
        self.ns['g'].clear()
        self.ns['b'].clear()

    def getrandomnodes(self):
        targets = set()
        # for fanout times, choose from good or bad set
        lg = list(self.cs['g'])
        lb = list(self.cs['b'])
        for i in range(0,self.fanout):
            id = None
            if self.randint(1) % 2 == 0 and len(lb) != 0:
                id = lb[self.randint(len(lb)-1)]
            if id is None and len(lg) != 0:
                idtmp = lg[self.randint(len(lg)-1)]
                if idtmp != self.id:
                    id = idtmp
            if id is not None:
                targets.add(id)
        return targets

    def resetIfDisconnectedTTL(self):
        if self.isDisconnected:
            if self.ttlcur > 0:
                self.ttlcur -= 1
                if self.ttlcur <= 0:
                    sg = self.cs['b'].copy()
                    sb = self.cs['g'].copy()
                    self.resetTables()
                    for id in sg:
                        self.cs['b'].add(id)
                    for id in sb:
                        self.cs['b'].add(id)
                    self.cs['b'].remove(self.id)
                    self.cs['g'].add(self.id)
            return True
        return False

    # call update nodes from random nodes
    def ping(self, usechangeset=True):
        if self.resetIfDisconnectedTTL():
            return
        srcsetdata = {}
        if usechangeset:
            srcsetdata['b'] = self.changeset['b'].copy()
            srcsetdata['g'] = self.changeset['g'].copy()
        else:
            srcsetdata['b'] = self.cs['b'].copy()
            srcsetdata['g'] = self.cs['g'].copy()

        ids = self.getrandomnodes()

        for id in ids:
            data = self.router.routeGetData(idsrc=self.id, iddst=id, srcsetdata=srcsetdata, usechangeset=usechangeset)
            #p('{:>2} pinged {:>2}, tx:{}  rx:{}'.format(self.id, id, srcsetdata, data))
            if data is None:
                self.ns['b'].add(id)
                if id in self.ns['g']:
                    self.ns['g'].remove(id)
            else:
                for k in data['g']:
                    self.ns['g'].add(k)
                for k in data['b']:
                    self.ns['b'].add(k)
                if id in self.ns['b']:
                    self.ns['b'].remove(id)

        # resolve conflicts
        itemsToRemove = []
        for id in self.ns['g']:
            if id in self.ns['b']:
                itemsToRemove.append(id)

        for id in itemsToRemove:
            self.ns['g'].remove(id)

    def pinged(self,idsrc,srcsetdata,usechangeset=True):
        if self.resetIfDisconnectedTTL():
            return None

        d = {}
        if usechangeset:
            d['g'] = self.changeset['g'].copy()
            d['b'] = self.changeset['b'].copy()
            d['g'].add(self.id)
        else:
            d['g'] = self.cs['g'].copy()
            d['b'] = self.cs['b'].copy()

        self.ns['g'].add(idsrc)
        for g in srcsetdata['g']:
            self.ns['g'].add(g)
        for g in srcsetdata['b']:
            if g != self.id:
                self.ns['b'].add(g)
        # resolve conflicts
        itemsToRemove = []
        for id in self.ns['g']:
            if id in self.ns['b']:
                itemsToRemove.append(id)

        for id in itemsToRemove:
            self.ns['g'].remove(id)

        return d

    def disconnect(self):
        self.isDisconnected = True

    def connect(self):
        self.isDisconnected = False
        self.ttlcur = self.ttl


class Router:
    def __init__(self):
        self.d = {}

    def setNodes(self, dnodes):
        self.d = dnodes

    def routeGetData(self, idsrc, iddst, srcsetdata, usechangeset):
        if idsrc not in self.d or iddst not in self.d:
            return None
        ndst = self.d.get(iddst)
        return ndst.pinged(idsrc,srcsetdata, usechangeset)

    def step(self):
        pass

class Gossip:
    def __init__(self, numnodes, fanout, ttl):
        self.d = {}
        self.router = Router()

        d = {}
        for i in range(0, numnodes):
            n = MyNodeGossip(router=self.router,fanout=fanout, ttl=ttl)
            self.d[n.id] = {}
            self.d[n.id]['obj'] = n
            self.d[n.id]['state'] = True
            self.d[n.id]['tschange'] = 0
            d[n.id] = n
        self.ts = 0

        self.router.setNodes(d)

    def getNodes(self):
        d = {}
        for k,v in self.d.items():
            d[k] = v['obj']
        return d

    def connectAll(self):
        keys = self.d.keys()
        for k,v in self.d.items():
            v['obj'].resetTables()
            for key in keys:
                v['obj'].addnodeid(key)
            v['obj'].updateCS()

    def p(self):
        p('TS:{} '.format(self.ts))
        for k,v in self.d.items():
            s = 'id:{:>2} state:{} '.format(k,v['state'])
            s += v['obj'].getinfo()
            p(s)
        if self.isConsistentState():
            p('isConsistentState 1')
        else:
            p('inConsistentState 0')

    def isConsistentState(self):
        sidg = set()
        sidb = set()
        for k,v in self.d.items():
            if v['state']:
                sidg.add(k)
            else:
                sidb.add(k)
        # for each good node, compare its good/bad keys with reference set
        for k,v in self.d.items():
            if not v['state']:
                continue
            n = v['obj']
            if len(n.cs['g']) != len(sidg) or len(n.cs['b']) != len(sidb):
                return False
            for key in n.cs['g']:
                if key not in sidg:
                    return False
            for key in n.cs['b']:
                if key not in sidb:
                    return False
        return True

    def setConnectState(self,id,isConnected=True):
        if id not in self.d:
            return
        d = self.d[id]
        p('setConnectState {} isConnected {}'.format(id, isConnected))
        d['state'] = isConnected
        if isConnected:
            d['obj'].connect()
        else:
            d['obj'].disconnect()
        d['tschange'] = self.ts

    def cycle(self):
        for k,v in self.d.items():
            v['obj'].ping()
        for k,v in self.d.items():
            v['obj'].updateCS()
        self.ts += 1

class TestGossip:
    @staticmethod
    def runcheckcycles(gossip,maxloops):
        ctr = 0
        for i in range(0,maxloops):
            gossip.cycle()
            #gossip.p()
            ctr += 1
            if gossip.isConsistentState():
                break
        assert gossip.isConsistentState()
        p('took {:>2} cycles to get to consistent state'.format(ctr))
    @staticmethod
    def test1():
        numnodes = 15
        maxloops = 100
        ACtr.reset()
        gossip = Gossip(numnodes=numnodes,fanout=2,ttl=3)
        d = gossip.getNodes()
        keys = d.keys()
        for i in range(0,numnodes):
            assert i in d

        gossip.connectAll()
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(1,False)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(1,True)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(1,False)
        gossip.setConnectState(8,False)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(1,True)
        gossip.setConnectState(8,True)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(1,False)
        gossip.setConnectState(8,False)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(5,False)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(1,True)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(5,True)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(3,False)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(8,True)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(3,True)
        TestGossip.runcheckcycles(gossip,maxloops)

        p('gossip passed')
    @staticmethod
    def test2():
        numnodes = 15
        maxloops = 100
        ACtr.reset()
        gossip = Gossip(numnodes=numnodes,fanout=2,ttl=3)
        d = gossip.getNodes()
        keys = d.keys()
        for i in range(0,numnodes):
            assert i in d

        gossip.connectAll()
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(1,False)
        gossip.cycle()
        gossip.setConnectState(1,True)
        gossip.cycle()
        gossip.cycle()
        gossip.setConnectState(1,False)
        gossip.cycle()
        gossip.cycle()
        gossip.setConnectState(1,True)
        gossip.cycle()
        gossip.setConnectState(1,False)
        gossip.cycle()
        gossip.cycle()
        gossip.cycle()
        gossip.cycle()
        gossip.setConnectState(1,True)
        gossip.cycle()
        gossip.setConnectState(1,False)
        gossip.cycle()
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(1,True)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(1,False)
        gossip.setConnectState(8,False)
        gossip.cycle()
        gossip.cycle()
        gossip.setConnectState(1,True)
        gossip.cycle()
        gossip.cycle()
        gossip.setConnectState(1,False)
        TestGossip.runcheckcycles(gossip,maxloops)

        gossip.setConnectState(1,True)
        gossip.setConnectState(8,True)
        TestGossip.runcheckcycles(gossip,maxloops)


        p('gossip passed')
    @staticmethod
    def test():
        TestGossip.test1()
        TestGossip.test2()


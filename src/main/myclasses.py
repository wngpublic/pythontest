#!/usr/local/bin/python3

import sys
import os
import os.path
import getopt
import argparse
import fileinput
import random
import re
import string
import copy
import math
import threading
import collections
import time
import urllib.request as url
import json
import requests
import copy
import time
import datetime
import xml.etree.ElementTree
import subprocess
import hashlib
import base64

def p(v):
    print(v)

class ClassTest1:
    def __init__(self):
        self.v1 = 10
        self.v2 = 20
        self.v3 = 'hello there'
    def getV1(self):
        return self.v1
    def getV3(self):
        return self.v3
    def setV1(self, v1):
        self.v1 = v1
    def hello(self):
        print('hello {0}'.format('wayne'))


class Myutils:
    def __init__(self):
        self.charset = {
            'lun'   : 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
            'l'     : 'abcdefghijklmnopqrstuvwxyz',
            'u'     : 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'ln'    : 'abcdefghijklmnopqrstuvwxyz0123456789',
            'h'     : 'abcdef0123456789',
            'n'     : '0123456789'
        }
        pass

    def readfile(self, filename):
        v = ''
        try:
            filehandle = open(filename, 'r')
            for line in filehandle:
                v = v + line
            filehandle.close()
        except Exception as e:
            print(e)
        finally:
            filehandle.close()
        return v

    def writefile(self, filename, value):
        try:
            filehandle = open(filename, 'a')
            filehandle.write('\n')
            filehandle.write(value)
            filehandle.close()
        except Exception as e:
            print(e)
        finally:
            filehandle.close()

    def getRandString(self, sz, charsettype='ln'):
        charset = self.charset.get(charsettype)
        if charset is None:
            return None
        maxcharset = len(charset)-1
        v = ''
        for i in range(0,sz):
            idx = random.randint(0,maxcharset)
            v += charset[idx]
        return v

    def getRandNum(self, min, max):
        return random.randint(min,max)

    # choose numselect items from array, exclude setexclude. return None if unavail
    @staticmethod
    def choose(array,numselect,setexclude):
        if array is None or not isinstance(array, list):
            return None
        if setexclude is not None and not isinstance(setexclude, set):
            return None
        if numselect < 1:
            return None
        if setexclude is not None:
            sz = len(setexclude)
            total = sz + numselect
            if total > len(array):
                return None
        else:
            if numselect >= len(array):
                return None
        l = array.copy()
        random.shuffle(l)
        ret = set()
        ctr = 0
        for v in l:
            if setexclude is not None and v in setexclude:
                continue
            ret.add(v)
            ctr += 1
            if ctr >= numselect:
                break
        return ret

    @staticmethod
    def getTimeCurMillis():
        t = time.time()
        return int(round(t * 1000))

    def getDatetimeMicro(self):
        t = datetime.datetime.now()
        return t.microsecond

    @staticmethod
    def getJsonFromString(input):
        v = json.loads(input)
        return v

    @staticmethod
    def getFileJSON(filename):
        if not os.path.isfile(filename):
            raise ValueError('is not filename {0}'.format(filename))
        try:
            filehandle = open(filename, 'r')
            lines = filehandle.readlines()
            filehandle.close()
            sjson = ''.join(lines)
            vjson = json.loads(sjson)
            return vjson
        except Exception as e:
            p(e)
            return None
        finally:
            filehandle.close()

    @staticmethod
    def getStringXML(s):
        root = xml.etree.ElementTree.fromstring(s)
        return root

    @staticmethod
    def getFileXML(filename):
        if not os.path.isfile(filename):
            raise ValueError('is not filename {0}'.format(filename))
        try:
            tree = xml.etree.ElementTree.parse(filename)
            root = tree.getroot()
            return root
        except Exception as e:
            p(e)
            return None

    @staticmethod
    def prettyXML(root):
        proc = subprocess.Popen(
            ['xmllint','--format','/dev/stdin'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        (out,outerr) = proc.communicate(root)
        out = out.decode('utf-8')
        return out

    @staticmethod
    def parseXML(root):
        xmlStr = xml.etree.ElementTree.tostring(root)
        xmlPretty = Myutils.prettyXML(xmlStr)
        p('------------------')
        p('{0}'.format(xmlPretty))
        p('------------------')
        for e in root.iter():
            tag = e.tag
            text = e.text
            attrib = e.attrib
            if text is not None:
                text = text.strip()
                if len(text) == 0:
                    text = None
            if attrib is not None:
                if len(attrib) == 0:
                    attrib = None
            if text is not None and attrib is not None:
                p('TAG:{0},TEXT:{1},ATTRIB:{2}'.format(tag,text,attrib))
            elif text is not None:
                p('TAG:{0},TEXT:{1}'.format(tag,text))
            elif attrib is not None:
                p('TAG:{0},ATTRIB:{1}'.format(tag,attrib))
            else:
                p('TAG:{0}'.format(tag))
        pass


    @staticmethod
    def jsondiff(json1=None, json2=None, prefix='', printStats=False, printKeysOnly=False):
        returnVal = True
        try:
            if isinstance(json1, list):
                # does not evaluate out of order lists!
                if not isinstance(json2, list):
                    if printStats:
                        if printKeysOnly:
                            p('diff list mismatch @{0}'.format(prefix))
                        else:
                            p('diff list mismatch @{0}\n{1}\n!=\n{2}'.format(prefix,json1,json2))
                    returnVal = False
                if len(json1) != len(json2):
                    if printStats:
                        if printKeysOnly:
                            p('diff list mismatch @{0}'.format(prefix))
                        else:
                            p('diff @{0}\n{1}\n!=\n{2}\n'.format(prefix,json1,json2))
                    returnVal = False
                for i in range(0, len(json1)):
                    k1 = json1[i]
                    k2 = json2[i]
                    if not Myutils.jsondiff(json1=k1,json2=k2,prefix=prefix + '/' + str(i),printStats=printStats,printKeysOnly=printKeysOnly):
                        returnVal = False
            elif isinstance(json1, dict):
                if not isinstance(json2, dict):
                    if printStats:
                        if printKeysOnly:
                            p('diff list mismatch @{0}'.format(prefix))
                        else:
                            p('diff dict mismatch @{0}\n{1}\n!=\n{2}'.format(prefix,json1,json2))
                    returnVal = False
                if len(json1) != len(json2):
                    if printStats:
                        if printKeysOnly:
                            p('diff list mismatch @{0}'.format(prefix))
                        else:
                            p('diff @{0}\n{1}\n!=\n{2}\n'.format(prefix,json1,json2))
                    returnVal = False
                for k1 in json1:
                    newprefix = prefix + '/' + k1
                    if k1 not in json2:
                        if printStats:
                            if printKeysOnly:
                                p('diff list mismatch @{0}'.format(newprefix))
                            else:
                                p('diff @{0}\n{1}\n!=\n{2}\n'.format(newprefix,json1,json2))
                        returnVal = False
                    if not Myutils.jsondiff(json1[k1],json2[k1],prefix=newprefix,printStats=printStats,printKeysOnly=printKeysOnly):
                        returnVal = False
            else:
                if json1 != json2:
                    if printStats:
                        if printKeysOnly:
                            p('diff @{0}'.format(prefix))
                        else:
                            p('diff @{0}\n{1}\n!=\n{2}\n'.format(prefix,json1,json2))
                    returnVal = False
        except Exception as e:
            p(e)
            returnVal = False

        return returnVal

    @staticmethod
    def traverseDict(prefix, vjson, printStats=False):
        objtype = 0
        if isinstance(vjson, list):
            objtype = 1
        elif isinstance(vjson, dict):
            objtype = 2

        i = 0
        for k in vjson:
            if objtype == 1:
                key = k
                strval = str(i)
            elif objtype == 2:
                key = vjson[k]
                strval = k
            try:
                if isinstance(key, list):
                    if printStats:
                        p('is list {0}'.format(key))
                    Myutils.traverseDict(prefix + strval + '.', key, printStats)
                elif isinstance(key, dict):
                    if printStats:
                        p('is dict {0}'.format(key))
                    Myutils.traverseDict(prefix + strval + '.', key, printStats)
                else:
                    if objtype == 1:
                        if printStats:
                            p('is terminal value {0} = {1}'.format(k, key))
                    else:
                        if printStats:
                            p('is terminal value {0}'.format(key))
            except Exception as e:
                p(e)
            i += 1

    @staticmethod
    def traverseDictOld(prefix, vjson, printStats=False):
        if isinstance(vjson, list):
            i = 0
            for i in range(0, len(vjson)):
                k = vjson[i]
                if isinstance(k, list):
                    if printStats:
                        p('l is list {0}'.format(k))
                    Myutils.traverseDict(prefix + str(i) + '.', k, printStats)
                elif isinstance(k, dict):
                    if printStats:
                        p('l is dict {0}'.format(k))
                    Myutils.traverseDict(prefix + str(i) + '.', k, printStats)
                else:
                    if printStats:
                        p('l is terminal value {0}'.format(k))
                i += 1
        elif isinstance(vjson, dict):
            for k in vjson:
                if isinstance(vjson[k], list):
                    if printStats:
                        p('d is list {0}'.format(k))
                    Myutils.traverseDict(prefix + k + '.', vjson[k], printStats)
                elif isinstance(vjson[k], dict):
                    if printStats:
                        p('d is dict {0}'.format(k))
                    Myutils.traverseDict(prefix + k + '.', vjson[k], printStats)
                else:
                    if printStats:
                        p('d is terminal value  {0} = {1}'.format(k,vjson[k]))
        else:
            for k in vjson:
                if printStats:
                    p('e is value {0} {1}'.format(prefix, k))


    @staticmethod
    def jsonsubtreediff(jsonv, printStats=None):
        pass

    @staticmethod
    def hashSHA256(data):
        data_hashed = hashlib.sha256(data.encode()).hexdigest()
        return data_hashed

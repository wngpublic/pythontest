#!/usr/local/bin/python3
import argparse
import sys
import os

def p(s):
    print(s)

class TestReadWriteFile:
    def __init__(self):
        pass
    def file_exists(self, f):
        return False if f is None or not os.path.exists(f) else True
    def process(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-fi', help='input file')
        parser.add_argument('-fo', help='output file')
        parser.add_argument('-append', action='store_true', help='if output file exists, append to it')
        parser.add_argument('-debug', action='store_true', help='output to std')
        args = parser.parse_args()

        filei = args.fi
        fileo = args.fo
        debug = args.debug
        appendmode = args.append

        if(filei is None):
            sys.exit('use: script.py -fi <input> -fo <output> -append -debug')
        if not self.file_exists(filei):
            sys.exit('file {} does not exist'.format(filei))

        fo = None
        if(fileo is not None):
            fo = open(fileo, 'a') if(self.file_exists(fileo) and appendmode) else open(fileo, 'w')

        fi = open(filei, 'r')
        lines = fi.readlines()
        for line in lines:
            line = line.strip('\n')
            if(debug):
                p(line)
            if fo:
                fo.write(line + '\n')

        fi.close()
        if(fo is not None):
            fo.close()
            p('finished reading {} and writing to {}'.format(filei, fileo))
        else:
            p('finished reading {}'.format(filei))

test = TestReadWriteFile()
test.process()
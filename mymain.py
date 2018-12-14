#!/usr/local/bin/python3

import testcases
import signal

def p(s):
    print(s)

class Main:
    def __init__(self):
        pass
    def main(self):
        t = testcases.Tests()
        try:
            t.test()
        except Exception as e:
            p('ERROR: ' + e.args[0])

Main().main()

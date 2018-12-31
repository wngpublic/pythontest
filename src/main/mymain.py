#!/usr/local/bin/python3

from src.main import testcases
import sys
import time

def p(s):
    print(s)

class Main:
    def __init__(self):
        pass
    def main(self, argv):
        try:
            nsbeg = time.time_ns()
            testcases.Tests().test(argv)
        except KeyboardInterrupt:
            p('KeyboardInterrupt detected! Killing!')
        except Exception as e:
            p('ERROR: ' + e.args[0])
        finally:
            nsend = time.time_ns()
            diff_ms = (nsend - nsbeg)/1_000_000
            p('finished. time elapsed: {} ms'.format(diff_ms))

Main().main(sys.argv[1:])

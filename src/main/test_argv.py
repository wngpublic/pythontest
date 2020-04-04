import sys
import re

def parse_argv(argv):
    if len(argv) == 1:
        assert len(argv[1:]) == 0
    print('[{}], [{}]'.format(argv[0],argv[1:]))

argv = sys.argv
parse_argv(argv)
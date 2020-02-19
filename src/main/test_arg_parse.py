#!/usr/local/bin/python3
import argparse

class TestArgParse:
    def __init__(self):
        pass
    def p(self, s):
        print(s)
    def hello(self, name=None):
        self.p('hello {0}'.format(name))
    def test(self):
        self.hello('hi')
    def processOptionalArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-o',   '--out',    action='store_true',  help='show out, stores as true')
        parser.add_argument('-o1',  '--out1',   action='store_true',  help='show out1, stores as true')
        parser.add_argument('-of',  '--outf',   action='store_false', help='show out1, stores as false, true if not exist')
        parser.add_argument('-o2',  '--out2',                         help='show out2, stores as value')
        parser.add_argument('-o3',                                    help='show o3, stores as value')
        parser.add_argument('-o4',                                    help='show o4, stores as value')
        parser.add_argument('-o5',              type=int,             help='show o5, stores as int')
        parser.add_argument('-l2',              nargs=2,              help='l2 takes 2 args')

        parser.add_argument('req1', type=int,                         help='required position1 req1 is type int')
        parser.add_argument('req2', type=str,                         help='required position2 req2 is type str')
        args,unknown = parser.parse_known_args()
        msg = ''
        if args.out == True:
            msg += '-o was used; '
        if args.out1 == True:
            msg += '--out1 was used; '
        if args.out2 is not None:
            msg += '--out2 was used; '
        if args.o3 is not None:
            msg += '-o3 was used {}; '.format(args.o3)
        if args.o4 is not None:
            msg += '-o4 was used; '
        if args.o5 is not None:
            msg += '-o5 was used; '
        if args.l2 is not None:
            a = args.l2
            msg += 'l2 vals: (arg0={} arg1={})'.format(a[0], a[1])
        self.p(args)
        self.p(unknown)
        self.p('\nprinting req1={}, req2={} msg: {}'.format(args.req1, args.req2, msg))

test = TestArgParse()
test.processOptionalArgs()

'''

./test_arg_parse.py -o1 123 345 -o2 he -o3 abab
./test_arg_parse.py -o1 123 blah -o2 he -o3 abab
./test_arg_parse.py -o1 123 "blah" -o2 he -o3 abab
./test_arg_parse.py -o1 123 "blah" -o2 he -o3 abab -l2 a1 a2

'''

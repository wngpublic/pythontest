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
        '''
        usage: test_arg_parse.py [-h] [-o] [-o1] [-of] [-o2 OUT2] [-o3 O3] [-o4 O4]
                         [-o5 O5] [-l2 L2 L2]
                         req1 req2 req3 req4

        python3 test_arg_parse.py 10 hi -o -o1 -o2 someval -req3 20 -l2 val1 val2
        "10" and "hi" are req1 and req2, REQUIRED POSITIONAL vals
        -o and -o1 dont use args because they are flags only
        '''
        parser = argparse.ArgumentParser()
        # optional, no arg needed, if -o present, args.out is true, there is no store_true var
        parser.add_argument('-o',   '--out',    action='store_true',  help='show out, stores as true')
        # out1 is the formal name, so when accessing, it's args.out1, not args.o1
        parser.add_argument('-o1',  '--out1',   action='store_true',  help='show out1, stores as true')
        parser.add_argument('-of',  '--outf',   action='store_false', help='show out1, stores as false, true if not exist')
        # optional, -o2 someval, if -o2 is not specified, args.out2 is None
        parser.add_argument('-o2',  '--out2',                         help='show out2, stores as value')
        parser.add_argument('-o3',                                    help='show o3, stores as value')
        parser.add_argument('-o4',                                    help='show o4, stores as value')
        parser.add_argument('-o5',              type=int,             help='show o5, stores as int')
        parser.add_argument('-l2',              nargs=2,              help='l2 takes 2 args')

        # no dash means required, use it like: python3 test_arg_parse.py 10 hi
        #                            NOT like: python3 test_arg_parse.py -req1 10 -req2 hi
        parser.add_argument('req1', type=int,                         help='required position1 req1 is type int')
        parser.add_argument('req2', type=str,                         help='required position2 req2 is type str')
        # dash means optional with default of 100
        parser.add_argument('-req3', type=int, default=100,           help='option req3 is type int')
        parser.add_argument('-req4', type=str, default='blah',        help='option req4 is type str')
        args,unknown = parser.parse_known_args()
        msg = ''
        msg += 'o {}; '.format(args.out)
        msg += 'out1: {}; '.format(args.out1)
        msg += 'out2: {}; '.format(args.out2)
        msg += 'o3: {}; '.format(args.o3)
        msg += 'o4: {}; '.format(args.o4)
        msg += 'o5: {}; '.format(args.o5)
        if args.l2 is not None:
            a = args.l2
            msg += 'l2 vals: (arg0={} arg1={})'.format(a[0], a[1])
        self.p('{},{}'.format(args,unknown))
        self.p('\nprinting req1:{}, req2:{} req3:{}, req4:{} others:{} unknown:{}'
               .format(args.req1, args.req2, args.req3, args.req4, msg, unknown))

test = TestArgParse()
test.processOptionalArgs()

'''

./test_arg_parse.py -o1 123 345 -o2 he -o3 abab
./test_arg_parse.py -o1 123 blah -o2 he -o3 abab
./test_arg_parse.py -o1 123 "blah" -o2 he -o3 abab
./test_arg_parse.py -o1 123 "blah" -o2 he -o3 abab -l2 a1 a2

'''

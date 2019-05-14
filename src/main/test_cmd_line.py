#!/usr/local/bin/python3

from .testcases import Tests

'''
.testcases import Tests does not work as dir(module)
fix it
'''
def p(s):
    print(s)
class test_cmd_line:
    def cmd_line_input(self, argv):
        def parse_cmd_line_input(s, h):
            def print_methods(h):
                for k,v in h.items():
                    p('{:2} {}'.format(k,v))
            if(s is None or len(s) == 0):
                print_methods(h)
            elif(s == 'q' or s == 'quit'):
                return False
            elif(s == '?'):
                print_methods(h)
            elif(s.isdigit()):
                i = int(s)
                if(i in h):
                    p('exec {}'.format(h[i]))
                    getattr(self, h[i])()
            return True
        def get_function_map():
            l = dir(Tests)
            l_functions = [ m for m in dir(Tests) if self.is_callable_user_defined(m)]
            #l_functions = [ m for m in dir(self) if self.is_callable_user_defined(m)]
            h = {}
            for i in range(len(l_functions)):
                h[i] = l_functions[i]
            return h
        h = get_function_map()
        for i in range(0,1000):
            s = input('prompt> ')
            if not parse_cmd_line_input(s, h):
                break
        p('quitting cmd_line_input')
def main():
    test_cmd_line().cmd_line_input(argv=None)

main()
import unittest

'''
python3 -m unittest testutcases.UTCases.test_helloworld1
'''

global_debug_level_ = 0  # 0 to 5. 0 = off, 1 = highest, 5 = lowest
global_output_to_file_ = False
global_fh_ = None

def p(s):
    global global_output_to_file_
    global global_fh_
    if(global_output_to_file_):
        if(global_fh_ is None):
            global_fh_ = open('output_debug.log','w')
        global_fh_.write(s + '\n')
    else:
        print(s)

class UTCases(unittest.TestCase):
    def setUp(self):
        p('setup')

    def tearDown(self) -> None:
        p('teardown')

    def test_helloworld1(self):
        p('hello world 1')
        assert True
        self.assertEqual(1,1)

    @unittest.expectedFailure
    def test_helloworld2(self):
        p('hello world 2')
        assert False

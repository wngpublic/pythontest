import numpy
import random
import scipy
import unittest
import matplotlib.pyplot as plt
import time

def p(s):
    print(s)

class ut(unittest.TestCase):
    '''
    __init__ is overridden
    def __init__(self):
        pass
    '''
    def test_random_normal(self):
        def dist1():
            samples = numpy.random.normal(0,0.1,100)
            assert len(samples) == 100
            l = []
            for f in samples:
                rounded = round(f,3)
                l.append(rounded)
            assert len(l) == 100
            assert abs(0 - numpy.mean(l)) < 0.1
        def dist2():
            samples = numpy.random.normal(10,1,100)
            assert len(samples) == 100
            l = []
            for f in samples:
                rounded = round(f,3)
                l.append(rounded)
            assert len(l) == 100
            mean = numpy.mean(l)
            assert abs(10 - mean) < 1
            stddev = numpy.std(l)
            assert abs(stddev) < 1.1
        def d3():
            '''
            # 3-sigma rule: 68-95-99.7 (empirical) for 1,2,3 standard deviation
            # 68% of all samples lie within 1 standard deviations of mean
            # 95% of all samples lie within 2 standard deviations of mean

            observations with std_dev

            std_dev range   pct%
            0.5     48      2
                    49:50   96
                    51      2
            1.0     47      2
                    28      14
                    49:50   68
                    51      12
                    52      2
            1.5     46      1
                    47      6
                    48      16
                    49      24
                    50      26
                    51      16
                    52      8
                    53      1
            2.0     45      1
                    46      4
                    47      10
                    48      17
                    49      21
                    50      17
                    51      15
                    52      7
                    53      5
                    54      2
            3.0     43      2
                    45      6
                    46      7
                    47      10
                    48      11
                    49      11
                    50      13
                    51      10
                    52      11
                    53      7
                    54      4
                    55      3
                    56      2
            '''

            for multiplier in range(1,8):
                std_deviation = 0.5 * multiplier
                mean = 50
                size = 1000
                samples = numpy.random.normal(mean,std_deviation,size)
                l = [int(f) for f in samples]
                d = {}
                for v in l:
                    if v not in d:
                        d[v] = 0
                    d[v] += 1
                sorted_keys = sorted(d.keys())
                p('standard_deviation:{}'.format(std_deviation))
                for k in sorted_keys:
                    p('{:2} = {:.2f} = {}'.format(k,d[k]/1000.0,d[k]))
        def d4():
            # uniform dist of [0,1)
            size = 1000
            samples = numpy.random.random_sample(size)
            l = [int(10*f) for f in samples]
            d = {}
            for v in l:
                if v not in d:
                    d[v] = 0
                d[v] += 1
            sorted_keys = sorted(d.keys())
            for k in sorted_keys:
                p('{:2} = {:.2f} = {}'.format(k,d[k]/1000.0,d[k]))
            time.sleep(1)
        def d5():
            # multivariate normal distribution
            pass
        d3()
        time.sleep(1)
        pass

if __name__ == "__main__":
    unittest.main() # not ut.main()!

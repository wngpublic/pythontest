import numpy
import random
import scipy
import unittest
import time
import matplotlib.pyplot as pyplot

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
        def dist2a():
            mean = 1000
            sigma = 50
            numsamples = 100
            samples = []
            for i in range(numsamples):
                v = random.normalvariate(mean,sigma)
                samples.append(v)
            assert len(samples) == numsamples
            l = []
            for f in samples:
                rounded = round(f,3)
                l.append(rounded)
            assert len(l) == numsamples
            calc_mean = numpy.mean(l)
            assert abs(calc_mean - mean) < sigma
            stddev = numpy.std(l)
            calc_stddev = mean + sigma/mean
            assert abs(stddev) < calc_stddev
            print_distribtion(l,do_round=True)

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
        def print_distribtion(l,do_round=True):
            d = {}
            for v in l:
                if do_round:
                    v = int(v)
                if v not in d:
                    d[v] = 0
                d[v] += 1
            sorted_keys = sorted(d.keys())
            for k in sorted_keys:
                p('{:2} = {:.2f} = {}'.format(k,d[k]/1000.0,d[k]))

        dist2a()
        #d3()

        time.sleep(1)
        pass
    def test_random(self):
        sz = 20
        l1 = numpy.random.randint(low=0,high=10,size=sz)            # [low,high)
        l2 = numpy.random.random_integers(low=0,high=10,size=sz)    # [low,high]
        l3 = numpy.random.uniform(size=sz)
        l4 = numpy.random.normal(size=sz)
        l5 = numpy.random.random_sample(size=sz)                    # [0.0,1.0) floats
        l6 = numpy.random.random(size=sz)                           # [0.0,1.0) floats
        l7 = numpy.random.sample(size=sz)                           # [0.0,1.0) floats
        l8 = numpy.random.rand(3,2)                                 # 3 rows, 2 elements per row
        la = [0,1,2,3,4,5,6,7,8,9]
        lb = la.copy()
        numpy.random.shuffle(lb)                                    # in place shuffle
        lc = numpy.random.permutation(la)
        assert len(l1) == 20
    def test_matplotlib_line(self):
        x = numpy.random.randint(0,10,8)
        y = [2,6,1,4,8,7,9,5]
        pyplot.plot(x,y)
        pyplot.show()
    def test_matplotlib_bar(self):
        x = numpy.random.randint(0,10,8)
        y = [2,6,1,4,8,7,9,5]
        pyplot.bar(x,y)
        pyplot.show()
    def test_matplotlib_scatter(self):
        x = numpy.random.randint(0,10,8)
        y = [2,6,1,4,8,7,9,5]
        pyplot.hist(y)
        pyplot.show()
    def test_matplotlib_histogram(self):
        x = numpy.random.randint(0,10,8)
        y = [2,6,1,4,8,7,9,5]
        pyplot.scatter(x,y)
        pyplot.show()
    def test_matplotlib_multiline(self):
        x1 = [2,3,4,5,6,7,8,9]
        y1 = [2,6,1,4,8,7,9,5]
        pyplot.plot(x1,y1,label='line-1')

        x2 = [2,3,4,5,6,7,8,9]
        y2 = [8,3,9,1,4,6,3,7]
        pyplot.plot(x2,y2,label='line-2')

        x2 = [2,3,4,5,6,7,8,9]
        y2 = [2,4,5,7,5,4,3,1]
        pyplot.plot(x2,y2,label='line-3')

        pyplot.title('multi lines')
        pyplot.legend()
        pyplot.show()

if __name__ == "__main__":
    unittest.main() # not ut.main()!


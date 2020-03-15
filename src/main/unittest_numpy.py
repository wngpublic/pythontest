import numpy
import random
import scipy
import unittest
import matplotlib.pyplot as plt

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
        dist2()

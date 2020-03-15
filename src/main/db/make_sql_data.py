import re
import json
import random
import enum
import sys
import unittest
import utils.myutils

def p(s):
    print(s)

class ut(unittest.TestCase):
    '''
    def __init__(self):
        pass
    __init__ gets overridden, so dont define it
    '''

    def test_make_receipt_table_1(self):
        products = {
            'apples':{
                'product_type':'food',
                'product_subtype':'fruit',
                'avg_price':1.00,
                'variation':0.50,
                'is_bulkable':True,
                'is_manufactued':False
            },
            'bananas':{
                'product_type':'food',
                'product_subtype':'fruit',
                'avg_price':2.00,
                'variation':0.50,
                'is_bulkable':True,
                'is_manufactued':False
            },
            'milk':{
                'product_type':'food',
                'product_subtype':'dairy',
                'avg_price':5.00,
                'variation':1.50,
                'is_bulkable':True,
                'is_manufactued':False
            },
            'coffee':{
                'product_type':'food',
                'product_subtype':'beverage',
                'avg_price':7.00,
                'variation':5.00,
                'is_bulkable':True,
                'is_manufactued':False
            },
            'tea':{
                'product_type':'food',
                'product_subtype':'beverage',
                'avg_price':4.00,
                'variation':4.00,
                'is_bulkable':True,
                'is_manufactued':False
            },
            'socks':{
                'product_type':'fashion',
                'product_subtype':'clothes',
                'avg_price':8.00,
                'variation':5.00,
                'is_bulkable':True,
                'is_manufactued':True
            },
            'shirts':{
                'product_type':'fashion',
                'product_subtype':'clothes',
                'avg_price':20.00,
                'variation':20.00,
                'is_bulkable':True,
                'is_manufactued':True
            },
            'sunglasses':{
                'product_type':'fashion',
                'product_subtype':'accessories',
                'avg_price':30.00,
                'variation':30.00,
                'is_bulkable':True,
                'is_manufactued':True
            },
            'phone':{
                'product_type':'electronics',
                'product_subtype':'communications',
                'avg_price':500.00,
                'avg_price':200.00,
                'is_bulkable':False,
                'is_manufactued':True
            },
            'laptop':{
                'product_type':'electronics',
                'product_subtype':'productivity',
                'avg_price':1000.00,
                'avg_price':2000.00,
                'is_bulkable':False,
                'is_manufactued':True
            }
        }

#!/usr/bin/python3

import random

def p(s):
    print(s)

#------------------------------------------------------
# map layout
#   goods_id:
#     soaps: int
#   goods
#     soaps
#     textiles: []
#   cost_adjustment
#     countries
#       country_id: float
#     goods
#       soaps: int
#       fruits: int
#   companies
#     company_id: {id,govid,name,address_id,domainname,country_id}
#------------------------------------------------------
class sql_data_generator:
    COSTADJ = 'cost_adjustment'
    GOODS = 'goods'
    GOODSID = 'goods_id'

    def __init__(self):
        self._m = {}
        self.init_goods()

    def init_goods(self):
        def init_set():
            s = set()
            s.add('soaps')
            s.add('cleaners')
            s.add('office')
            s.add('home')
            s.add('services_tech')
            s.add('services_law')
            s.add('shirts')
            s.add('pants')
            s.add('shoes')
            s.add('jackets')
            s.add('fruits')
            s.add('vegetables')
            s.add('meats')
            s.add('grains')
            s.add('truck')
            s.add('bike')
            s.add('sedan')

            m = {}
            ctr = 0
            for item in s:
                m[item] = ctr
                ctr = ctr + 1
            self._m[self.GOODSID] = m
            return m
        def new_company(id,govid,name,address_id,domainname,country_id):
            m = {}
            m['id']         = id
            m['govid']      = govid
            m['name']       = name
            m['address_id'] = address_id
            m['domainname'] = domainname
            m['country_id'] = country_id
            return m

        def init_goods():
            m = {}

            m['soaps'] = ['soaps']
            m['cleaners'] = ['cleaners']
            m['office'] = ['office']
            m['textiles'] = ['shirts','pants','shoes','jackets']
            m['home'] = ['home']
            m['foods'] = ['fruits','vegetables','meats','grains']
            m['cars'] = ['bike','truck','sedan']
            m['services_tech'] = ['services_tech']
            m['services_law'] = ['services_law']

            self._m[self.GOODS] = m

            m = {}
            m['countries'] = {}
            m['countries'][0] = 1.0
            m['countries'][1] = 1.5
            m['countries'][2] = 0.5
            m['countries'][3] = 2.0

            m[self.GOODS] = {}
            for product in self._m[self.GOODSID].keys():
                m[self.GOODS][product] = random.randint(1,1000)

            self._m[self.COSTADJ] = m

        def init_companies_fixed():
            m = {}
            e = new_company(0,0,"company0",1,"company0.C01",1)
            m[e['id']] = e
            e = new_company(1,1,"company1",2,"company1.C01",1)
            m[e['id']] = e
            e = new_company(2,0,"company0",1,"company0.C02",2)
            m[e['id']] = e
            e = new_company(3,1,"company1",2,"company1.C02",2)
            m[e['id']] = e
            e = new_company(4,0,"company0",1,"company0.C03",3)
            m[e['id']] = e
            e = new_company(5,1,"company1",2,"company1.C03",3)
            m[e['id']] = e
            e = new_company(6,2,"company2",3,"company2.C03",3)
            m[e['id']] = e
            e = new_company(7,3,"company3",4,"company3.C03",3)
            m[e['id']] = e
            e = new_company(8,0,"company0",1,"company0.C00",0)
            m[e['id']] = e
            e = new_company(9,1,"company1",2,"company1.C00",0)
            m[e['id']] = e

            self._m['companies'] = m

        init_set()
        init_companies_fixed()
        init_goods()

    def pop_goods(self):
        m = self._m
        results = []
        # populate table for products available
        results.append('CREATE TABLE products (gid integer primary key autoincrement, id integer, name text, category text);')
        for product_category, products in m[self.GOODS].items():
            for product in products:
                results.append('insert into products (id, name, category) values ({}, "{}", "{}");'
                               .format(self._m[self.GOODSID][product], product, product_category))
        # populate table for cost for each product by company
        results.append(
            'CREATE TABLE products_prices (gid integer primary key autoincrement,' + \
            'id integer, name text, product_id integer, company_id integer, price real);')
        ctr = 0
        for company_id,company_tuple in m['companies'].items():
            country_id = company_tuple['country_id']
            country_adjust = m[self.COSTADJ]['countries'][country_id]
            for product_category, products in m[self.GOODS].items():
                for product in products:
                    is_covered = random.randint(0,10) <= 7
                    if(not is_covered): continue
                    # each company has strength/weakness in specific good
                    company_adjust = random.uniform(0.5,3.0)
                    cost_adjust = country_adjust * company_adjust
                    price = m[self.COSTADJ][self.GOODS][product]
                    final_price = cost_adjust * price
                    final_price = int(final_price)
                    results.append('insert into products_prices (id,name,product_id,company_id,price) values ' + \
                                   '({},"{}",{},{},{});'.format(ctr, product, self._m[self.GOODSID][product],company_id,final_price))
                    ctr = ctr + 1
        for line in results:
            p(line)

def testmain():
    t = sql_data_generator()
    t.pop_goods()

testmain()

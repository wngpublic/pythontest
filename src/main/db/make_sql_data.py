import re
import json
import random
import enum
import sys
import unittest
import myutils

def p(s):
    print(s)

class sql_data_maker:

    '''
    table0  cities
            id,state,city,base_zip
    table1  address
            address
            id,id_cities,street,address,unit,zip,id_address_type
    table2  entity_type
            id,entity_category,entity_type,entity_name
    table3  owner_of_address
            id,id_address,id_entity_buyer,id_entity_seller,purchase_price,purchase_date
    table4  entities
            id,namefirst,namelast,id_entity_type,start_date,end_date
    table5  inventory_catalog
            id,id_entity_type,id_address,msrp
    table6  inventory_receipts
            id,id_entity_from,id_entity_toe,id_address_from,id_address_to,purchase_price,qty,date
    table7  relationships
            id_src,id_dst,relationship_type


d_relationships:{
    id0:{
        S_ENTITY_RELATE_SIBLING: {id1,id2}, # not objects!
        S_ENTITY_RELATE_PARENT:  {id3,id4},
        S_ENTITY_RELATE_COUPLE:  {id5,id6},
        S_ENTITY_RELATE_CHILD:   {id7,id8}
    },
    id1:{
        S_ENTITY_RELATE_SIBLING: {id0,id2},
        S_ENTITY_RELATE_PARENT:  {id3,id4},
        S_ENTITY_RELATE_COUPLE:  {id6},
        S_ENTITY_RELATE_CHILD:   {id9,id10}
    },
}

d_entities:{
    id0:{
        S_ID:id,
        S_ENTITY_FIRSTNAME:str,
        S_ENTITY_LASTNAME:str,
        S_ENTITY_TYPE:leaf value of S_ENTITY_TYPE
    },
    id1:{
        S_ID:id,
        S_ENTITY_FIRSTNAME:str,
        S_ENTITY_LASTNAME:str,
        S_ENTITY_TYPE:leaf value of S_ENTITY_TYPE
    }
}


data
|
+---S_DATAKEY_STATES
    |
    +---STATE1
    |   |
    |   +---S_DATAKEY_CITIES
    |       |
    |       +---CITY1
    |       |   |
    |       |   +---S_KEY_CITY_BASE_ZIP:v
    |       |   |
    |       |   +---S_DATAKEY_STREETS
    |       |       |
    |       |       +---STREET1
    |       |       |   |
    |       |       |   +---S
    |       |       |   +---S_DATAKEY_ADDRS
    |       |       |       |
    |       |       |       +---ADDR1
    |       |       |       |   |
    |       |       |       |   +---S_DATAKEY_ADDR_ZIP:v
    |       |       |       |   +---S_DATAKEY_ADDR_NUM_ID:v
    |       |       |       |   +---S_DATAKEY_ADDR_UNIT_ID:v
    |       |       |       |   +---S_DATAKEY_ADDR_TYPE:v
    |       |       |       |
    |       |       |       +---ADDR2
    |       |       |
    |       |       +---STREET2
    |       |
    |       +---CITY2
    |
    +---STATE2

figure1: data layout

'''


    S_CAT_ADDR          = 'category_address'
    S_ADDR_RES          = 'resident'
    S_ADDR_RES_VIRT     = 'resident_virtual'
    S_ADDR_RES_LAND     = 'resident_land'
    S_ADDR_BUS          = 'business'
    S_RES_PRIM_LAND     = 'primary_land'
    S_RES_PRIM_VIRT     = 'primary_virtual'
    S_RES_SEC_LAND      = 'secondary_land'
    S_RES_SEC_VIRT      = 'secondary_virtual'
    S_BUS_PRV           = 'business_private'
    S_BUS_PUB           = 'business_public'
    S_CAT_CONSUME       = 'category_consume'
    S_CONSUME_FRUITS    = 'fruits'
    S_CONSUME_VEGS      = 'vegs'
    S_CONSUME_GRAINS    = 'grains'
    S_CONSUME_MEAT      = 'meat'
    S_CONSUME_DRINK     = 'drink'
    S_ZIP_INC_THRESHOLD = 20
    S_ZIP               = 'zip'
    S_STREET            = 'streetname'
    S_ADDR              = 'addr_num'
    S_ADDR_UNIT         = 'addr_unit_num'
    S_ADDR_TYPE         = 'addr_type'
    S_ADDRESSES         = 'addresses'

    S_ENTITY_RELATIONSHIP   = 'relationship'
    S_ENTITY_RELATE_SIBLING = 'sibling'
    S_ENTITY_RELATE_PARENT  = 'parent'
    S_ENTITY_RELATE_COUPLE  = 'couple'
    S_ENTITY_RELATE_CHILD   = 'child'
    S_ENTITY_FIRSTNAME      = 'firstname'
    S_ENTITY_LASTNAME       = 'lastname'
    S_ENTITY_START_DATE     = 'startdate'
    S_ENTITY_END_DATE       = 'enddate'
    S_ENTITY_MALE           = 'male'
    S_ENTITY_FEMALE         = 'female'
    S_ENTITY_OTHER          = 'other'
    S_ENTITY_TYPE           = 'entity_type'
    S_ENTITYT_PERSON        = 'entityt_person'
    S_ENTITYT_VIRTUAL       = 'entityt_virtual'
    S_ENTITYT_ANIMAL        = 'entityt_animal'
    S_ENTITYT_FARM_ANIMAL   = 'entityt_farm_animal'
    S_ENTITYT_HOUSE_ANIMAL  = 'entityt_house_animal'
    S_ENTITYT_WILD_ANIMAL   = 'entityt_wild_animal'
    S_BASE_ZIP              = 'base_zip'
    S_KEY_CITY_BASE_ZIP     = 'city_base_zip'
    S_DATAKEY_STATES        = 'states'
    S_DATAKEY_CITIES        = 'cities'
    S_DATAKEY_STREETS       = 'streets'
    S_DATAKEY_STREET_NAME   = 'street_name'
    S_DATAKEY_ADDRS         = 'addresses'
    S_DATAKEY_ADDR_UNITS    = 'address_units'
    S_DATAKEY_ADDR_ZIP      = 'zip'
    S_DATAKEY_ADDR_NUM_ID   = 'id_addr_num'
    S_DATAKEY_ADDR_UNIT_ID  = 'id_addr_unit'
    S_DATAKEY_ADDR_TYPE     = 'addr_type'
    S_ID                    = 'id'


    def __init__(self):
        self.entity_types                           = self.make_entity_type()
        self.data_entities                          = {
            self.S_ENTITYT_PERSON:{},
            self.S_ENTITYT_VIRTUAL:{},
            self.S_ENTITYT_ANIMAL:{}
        }
        self.data_relationships                     = {}
        self.data_addresses                         = {}
        self.min_address_per_street                 = 1
        self.max_address_per_street                 = 5
        self.address_starting_val                   = 10
        self.pct_chance_of_unit_if_has_virtual      = 50
        self.min_num_streets_threshold_for_units    = 2
        self.pct_has_units_in_city                  = 25
        self.pct_has_units_in_street                = 50
        self.pct_has_units_in_address               = 50
        self.min_unit_per_address                   = 2
        self.max_unit_per_address                   = 10
        self.min_num_people_per_state               = 50
        self.max_num_people_per_state               = 100
        self.max_num_person                         = 1000
        self.max_num_virtual                        = 200
        self.max_num_animal                         = 2000
        self.max_num_children_per_couple            = 6
        self.max_level_relationship_descendants     = 10
        self.num_original_descendants               = 20
        self.pct_carry_over_currgen_2_nextgen       = 20
        self.u = myutils.my_utils
        pass

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


    def make_names(self,min_syllables,max_syllables,consonants,vowels,num,allow_duplicates):
        num_possibilities = len(consonants)*len(vowels)*(max_syllables-min_syllables+1)
        if(not allow_duplicates and num_possibilities < num):
            raise Exception('ERROR make_state_names: num:{} < num_possibilities:{}'.format(num,num_possibilities))
        data = []
        data_set = set()
        max_attempts = 100_000
        ctr = 0
        while len(data) < num:
            num_syllables = myutils.my_utils.rand_int(min_syllables,max_syllables)
            name = myutils.my_utils.make_random_word_from_charset(consonants,vowels,num_syllables,False)
            if allow_duplicates or name not in data_set:
                data.append(name)
            ctr += 1
            if ctr > max_attempts:
                break
        return data
    def make_state_names(self,num):
        consonants = ['b','c','d','f','g']
        vowels = ['a','e','i','o']
        data = self.make_names(1,3,consonants,vowels,num,False)
        assert isinstance(data,list)
        return data
    def make_city_names(self,num):
        consonants = ['f','g','h','j','k']
        vowels = ['a','e','i','o']
        data = self.make_names(1,3,consonants,vowels,num,False)
        assert isinstance(data,list)
        return data
    def make_street_names(self,num):
        consonants = ['f','g','h','j','k']
        vowels = ['a','e','i','o']
        data = self.make_names(1,3,consonants,vowels,num,False)
        assert isinstance(data,list)
        return data
    def make_last_names(self,num):
        consonants = ['b','m','p']
        vowels = ['a','o']
        data = self.make_names(1,3,consonants,vowels,num,True)
        assert isinstance(data,list)
        return data
    def make_first_names(self,num):
        consonants = ['b','c','d','g','h','j']
        vowels = ['a','e','i','o']
        data = self.make_names(1,3,consonants,vowels,num,True)
        assert isinstance(data,list)
        return data
    def make_virtual_names(self,num):
        consonants = ['b','c','d','g','h','j']
        vowels = ['a','e']
        data = self.make_names(2,5,consonants,vowels,num,True)
        assert isinstance(data,list)
        return data
    def make_animal_names(self,num):
        consonants = ['g','m','p']
        vowels = ['a','o']
        data = self.make_names(1,3,consonants,vowels,num,True)
        assert isinstance(data,list)
        return data
    def make_table_cities(self,num_states,min_cities_per_state,max_cities_per_state):
        data = self.data_addresses
        states = self.make_state_names(num_states)
        base_zip = 10000
        d_states = {}
        data[self.S_DATAKEY_STATES] = d_states
        for state in states:
            d_states[state] = {}
            d_cities = {}
            d_states[state][self.S_DATAKEY_CITIES] = d_cities
            num_cities = myutils.my_utils.rand_int(min_cities_per_state,max_cities_per_state)
            cities = self.make_city_names(num_cities)
            offset = 0
            for city in cities:
                d_cities[city] = {}
                d_cities[city][self.S_DATAKEY_STREETS] = {}
                d_cities[city][self.S_KEY_CITY_BASE_ZIP] = base_zip + offset*10    # so each city can have max 10 zips
                offset += 1
            base_zip += 1000
        return data

    def make_entity_type(self):
        data = {}
        data[self.S_CAT_ADDR] = {
            self.S_ADDR_RES: {
                self.S_ADDR_RES_VIRT:[
                    self.S_RES_PRIM_VIRT,
                    self.S_RES_SEC_VIRT
                ],
                self.S_ADDR_RES_LAND:[
                    self.S_RES_PRIM_LAND,
                    self.S_RES_SEC_LAND
                ]
            },
            self.S_ADDR_BUS:[
                self.S_BUS_PRV,
                self.S_BUS_PUB
            ]
        }
        data[self.S_ENTITY_TYPE] = {
            self.S_ENTITYT_PERSON:  [self.S_ENTITY_FEMALE,self.S_ENTITY_MALE],
            self.S_ENTITYT_VIRTUAL: ['company','govt','club'],
            self.S_ENTITYT_ANIMAL:  {
                self.S_ENTITYT_FARM_ANIMAL: ['farmchicken','farmfish','farmlamb'],
                self.S_ENTITYT_HOUSE_ANIMAL: ['housecat','housedog'],
                self.S_ENTITYT_WILD_ANIMAL: ['wildcat','wilddog','wildbird','wildraccoon','wildfish']
            }
        }
        data[self.S_ENTITY_RELATIONSHIP] = [
            self.S_ENTITY_RELATE_SIBLING,
            self.S_ENTITY_RELATE_PARENT,
            self.S_ENTITY_RELATE_COUPLE,
            self.S_ENTITY_RELATE_CHILD
        ]
        data[self.S_CAT_CONSUME] = {
            self.S_CONSUME_FRUITS: ['apple','banana','orange'],
            self.S_CONSUME_VEGS:   ['tomato','carrot','onion','beans','potato'],
            self.S_CONSUME_GRAINS: ['rice','bread','lentil'],
            self.S_CONSUME_MEAT:   ['chicken','fish','lamb'],
            self.S_CONSUME_DRINK:  ['water','juice','tea','coffee','milk','wine']
        }
        return data

    def choose_type(self,list_path_keys,num_elements=1):
        def traverse_subpaths_extend_leafs(kvnode,leafs):
            if isinstance(kvnode,list):
                leafs.extend(kvnode)
            elif isinstance(kvnode,dict):
                for k,v in kvnode.items():
                    traverse_subpaths_extend_leafs(v,leafs)
        data = self.entity_types
        if not isinstance(list_path_keys,list) or list_path_keys == None:
            raise Exception('ERROR list_path_keys is not list or is null')
        for path in list_path_keys:
            if path not in data:
                raise Exception('ERROR choose_type:{} not in entity_types:{}'.format(path,data.keys()))
            data = data[path]
        leafs = []
        traverse_subpaths_extend_leafs(data,leafs)
        sz = len(leafs)
        res = []
        for ctr in range(num_elements):
            i = myutils.my_utils.rand_int(0,sz)
            res.append(leafs[i])
        return res

    def make_table_addresses(self, data, min_num_streets, max_num_streets):
        '''
        data input is dict and has figure1 layout in class description
        '''
        min_inc_val                         = 1
        max_inc_val                         = 10
        for state,cities in data[self.S_DATAKEY_STATES].items():
            for city,d_city in cities[self.S_DATAKEY_CITIES].items():
                num_streets                 = myutils.my_utils.rand_int(min_num_streets,max_num_streets)
                has_virtual                 = True if num_streets >= self.min_num_streets_threshold_for_units else False
                has_units_c                 = myutils.my_utils.rand_bool(self.pct_chance_of_unit_if_has_virtual)
                zip_val                     = d_city[self.S_KEY_CITY_BASE_ZIP]
                d_streets                   = {}
                d_city[self.S_DATAKEY_STREETS] = d_streets
                cnt_addr                    = 0
                street_names                = self.make_street_names(num_streets)
                for street_name in street_names:
                    street                  = {}
                    d_streets[street_name] = street
                    #d_streets[self.S_DATAKEY_STREET_NAME] = street
                    street[self.S_DATAKEY_STREET_NAME] = street_name
                    #d_streets[self.S_DATAKEY_STREET_NAME] = street_name
                    d_addresses             = {}
                    #d_streets[self.S_DATAKEY_ADDRS] = d_addresses
                    street[self.S_DATAKEY_ADDRS] = d_addresses
                    num_addresses           = myutils.my_utils.rand_int(self.min_address_per_street,self.max_address_per_street)
                    id_address_val          = self.address_starting_val
                    inc_val                 = myutils.my_utils.rand_int(min_inc_val,max_inc_val)            # address 100,105,110,...
                    pct_business            = myutils.my_utils.get_rand_pct(1,4) if has_units_c else 0   # 0,25,50,75,100
                    has_units_s             = myutils.my_utils.rand_bool(self.pct_has_units_in_street) if has_units_c else False
                    for i in range(num_addresses):
                        is_business         = myutils.my_utils.pct_is_true(pct_business)
                        addr_type           = self.choose_type([self.S_CAT_ADDR,self.S_ADDR_BUS]) if is_business else self.choose_type([self.S_CAT_ADDR,self.S_ADDR_RES])
                        has_unit_s          = myutils.my_utils.rand_bool(self.pct_has_units_in_address) if has_units_s else False
                        if addr_type[0] == self.S_RES_PRIM_LAND or addr_type[0] == self.S_RES_SEC_LAND:
                            has_unit_s      = False
                        address_obj         = {}
                        #address_obj[self.S_STREET] = street_name
                        address_obj[self.S_ZIP] = zip_val
                        if has_unit_s:
                            num_units = myutils.my_utils.rand_int(self.min_unit_per_address,self.max_unit_per_address)
                            d_address_units = {}
                            address_obj[self.S_DATAKEY_ADDR_UNITS] = d_address_units
                            address_obj[self.S_ADDR_TYPE] = addr_type[0]
                            d_addresses[id_address_val] = address_obj
                            #d_addresses[self.S_DATAKEY_ADDR_UNITS] = d_address_units
                            #d_addresses[id_address_val] = d_address_units
                            for id_address_unit in range(num_units):
                                id_address_unit += 1
                                address_unit_obj = address_obj.copy()
                                addr_type = self.choose_type([self.S_CAT_ADDR,self.S_ADDR_BUS]) if is_business else self.choose_type([self.S_CAT_ADDR,self.S_ADDR_RES,self.S_ADDR_RES_VIRT])
                                address_unit_obj[self.S_ADDR_TYPE] = addr_type[0]
                                address_unit_obj[self.S_ADDR_UNIT] = id_address_unit
                                #d_address_units[id_address_unit] = address_unit_obj
                                cnt_addr += 1
                        else:
                            address_obj[self.S_ADDR_TYPE] = addr_type[0]
                            d_addresses[id_address_val] = address_obj
                            cnt_addr += 1
                        id_address_val += inc_val
                    if cnt_addr > self.S_ZIP_INC_THRESHOLD:
                        zip_val += 1
                        cnt_addr = 1

        return data

    def make_table_entities(self):
        '''
        entities:{
            S_ENTITYT_PERSON: {
                id1:{
                    id,
                    namefirst,namelast,
                    id_entity_type (S_ENTITY_TYPE),
                    start_date: date
                    end_date: date
                },
                id2:{...},
                ...
            },
            S_ENTITYT_VIRTUAL: {
                ...
            },
            S_ENTITYT_ANIMAL: {
                ...
            },
        }
        '''

        data_entities = self.data_entities
        data_relationships = self.data_relationships

        self.make_people_and_relationships(data_entities[self.S_ENTITYT_PERSON],data_relationships)

        id = 0
        virtualnames = list(self.make_virtual_names(self.max_num_virtual))
        for virtualname in virtualnames:
            etype = self.choose_type([self.S_ENTITY_TYPE,self.S_ENTITYT_VIRTUAL])
            entity = {
                self.S_ID:id,
                self.S_ENTITY_FIRSTNAME:None,
                self.S_ENTITY_LASTNAME:virtualname,
                self.S_ENTITY_TYPE:etype[0]
            }
            data_entities[self.S_ENTITYT_VIRTUAL][id] = entity
            id += 1


        id = 0
        animal_names = list(self.make_animal_names(self.max_num_animal))
        for i in range(self.max_num_animal):
            etype = self.choose_type([self.S_ENTITY_TYPE,self.S_ENTITYT_ANIMAL])
            name = None
            if etype[0] in self.entity_types[self.S_ENTITY_TYPE][self.S_ENTITYT_ANIMAL][self.S_ENTITYT_HOUSE_ANIMAL]:
                name = animal_names[i]
            entity = {
                self.S_ID:id,
                self.S_ENTITY_FIRSTNAME:name,
                self.S_ENTITY_LASTNAME:None,
                self.S_ENTITY_TYPE:etype[0]
            }
            data_entities[self.S_ENTITYT_ANIMAL][id] = entity
            id += 1
        return (data_entities,data_relationships)

    def make_people_and_relationships(self, dentities, drelationships):

        def init_relationship_id(drelationship,id):
            if id not in drelationship:
                drelationship[id] = {
                    self.S_ENTITY_RELATE_SIBLING:[],
                    self.S_ENTITY_RELATE_PARENT:[],
                    self.S_ENTITY_RELATE_COUPLE:[],
                    self.S_ENTITY_RELATE_CHILD:[]
                }

        def make_asymmetrical_relationship(e0,e1,keyid,key0to1,key1to0,drelationships):
            init_relationship_id(drelationships,e0[keyid])
            init_relationship_id(drelationships,e1[keyid])
            drelationships[e0[keyid]][key0to1].append(e1[keyid])
            drelationships[e1[keyid]][key1to0].append(e0[keyid])

        def make_symmetrical_relationship(e0,e1,keyid,key,drelationships):
            make_asymmetrical_relationship(e0,e1,keyid,key,key,drelationships)

        def match_simple(l_entity_males,l_entity_females,drelationships,allow_overlap=True):
            keyid = self.S_ID
            key = self.S_ENTITY_RELATE_COUPLE
            lm_unmatched = []
            lf_unmatched = []
            for m,f in zip(l_entity_males,l_entity_females):
                make_symmetrical_relationship(m,f,keyid,key,drelationships)

            szm = len(l_entity_males)
            szf = len(l_entity_females)
            if szm == szf or not allow_overlap:
                return
            elif szm < szf:
                for i in range(szm,szf):
                    f = l_entity_females[i]
                    m = self.u.choose_obj_from(l_entity_males)
                    make_symmetrical_relationship(m,f,keyid,key,drelationships)
            else:
                for i in range(szf,szm):
                    m = l_entity_males[i]
                    f = self.u.choose_obj_from(l_entity_females)
                    make_symmetrical_relationship(m,f,keyid,key,drelationships)

        # return (listfemale,listmale) from entities
        def get_m_f(entities):
            lm = []
            lf = []
            st = self.S_ENTITY_TYPE
            sm = self.S_ENTITY_MALE
            sf = self.S_ENTITY_FEMALE
            for e in entities:
                if      e[st] == sm:
                    lm.append(e)
                elif    e[st] == sf:
                    lf.append(e)
            return (lf,lm)

        def make_children(arrayid,f,dentities,drelationships):
            scouple     = self.S_ENTITY_RELATE_COUPLE
            schild      = self.S_ENTITY_RELATE_CHILD
            sparent     = self.S_ENTITY_RELATE_PARENT
            ssibling    = self.S_ENTITY_RELATE_SIBLING
            sid         = self.S_ID
            smale       = self.S_ENTITY_MALE
            stype       = self.S_ENTITY_TYPE
            slname      = self.S_ENTITY_LASTNAME
            sfname      = self.S_ENTITY_FIRSTNAME
            lmaleids    = []

            # choose random male
            for id in drelationships[f[sid]][scouple]:
                if dentities[id][stype] == smale:
                    lmaleids.append(id)
            idm             = self.u.choose_obj_from(lmaleids)
            m               = dentities[idm]
            lastname        = self.u.choose_obj_from([f[slname],m[slname]])
            num_children    = self.u.rand_int(0,self.max_num_children_per_couple)
            firstnames      = self.make_first_names(num_children)
            lchildren       = []
            for i in range(num_children):
                etype       = self.choose_type([self.S_ENTITY_TYPE,self.S_ENTITYT_PERSON])
                entity      = { sid:arrayid[0], sfname:firstnames[i], slname:lastname, stype:etype[0] }
                lchildren.append(entity)
                dentities[entity[sid]] = entity
                arrayid[0]  += 1
                if arrayid[0] >= self.max_num_person:
                    break

            # make relationships
            for i in range(len(lchildren)):
                child = lchildren[i]
                make_asymmetrical_relationship(m,child,sid,schild,sparent,drelationships)
                make_asymmetrical_relationship(f,child,sid,schild,sparent,drelationships)
                for j in range(i,len(lchildren)):
                    sibling = lchildren[j]
                    if child[sid] == sibling[sid]:
                        continue
                    make_symmetrical_relationship(child,sibling,sid,ssibling,drelationships)

            return lchildren

        def make_people_relationships(arrayid,dentities,drelationships):
            lcurrgen = list(dentities.values())
            while arrayid[0] < self.max_num_person:
                (lf,lm) = get_m_f(lcurrgen)
                if len(lf) == 0 or len(lm) == 0:
                    return  # no more generations!
                match_simple(lm,lf,drelationships,True)
                lnextgen = []
                for f in lf:
                    lchildren = make_children(arrayid,f,dentities,drelationships)
                    lnextgen.extend(lchildren)
                maxcarryover = int(len(lcurrgen)*self.pct_carry_over_currgen_2_nextgen/100)
                if maxcarryover > 0:
                    numcarryover = self.u.rand_int(0,maxcarryover)
                    if numcarryover > 0:
                        carryover = self.u.choose_objs_from(lcurrgen,numcarryover)
                        if len(carryover) != 0:
                            lnextgen.extend(carryover)
                lcurrgen = lnextgen

        def make_people_origin(arrayid,dentities):
            lastnames = self.make_last_names(self.num_original_descendants)
            firstnames = self.make_first_names(self.num_original_descendants)
            l_m = []
            l_f = []

            for ln,fn in zip(lastnames,firstnames):
                etype = self.choose_type([self.S_ENTITY_TYPE,self.S_ENTITYT_PERSON])
                entity = {
                    self.S_ID:arrayid[0],
                    self.S_ENTITY_FIRSTNAME:fn,
                    self.S_ENTITY_LASTNAME:ln,
                    self.S_ENTITY_TYPE:etype[0]
                }
                if etype[0] == self.S_ENTITY_FEMALE:
                    l_f.append(entity)
                elif etype[0] == self.S_ENTITY_MALE:
                    l_m.append(entity)
                dentities[arrayid[0]] = entity
                arrayid[0] += 1
                if arrayid[0] >= self.max_num_person:
                    break

            if len(l_f) == 0:
                assert len(l_f) != 0
            if len(l_m) == 0:
                assert len(l_m) != 0


        id = 0
        arrayid = [id]
        make_people_origin(arrayid,dentities)
        make_people_relationships(arrayid,dentities,drelationships)
        return

    def make_inventory_catalog(self, data_geo):
        return

    def make_transaction_receipts(self, data_geo, data_entities, data_inventory):
        return


    def recurse_entity_types_old(self,d,level,category,subcat0,subcat1,patharraybuf,tentryarraybuf,detype2id,arrayid):
        if isinstance(d,dict):
            for k,v in d.items():
                patharraybuf.append(k)
                if k in detype2id:
                    assert k not in detype2id
                detype2id[k] = arrayid[0]
                if level == 0:
                    tentryarraybuf.append('insert into entity_types(id,category,value) values({},"{}","{}")'
                                          .format(arrayid[0],k,k))
                    arrayid[0] += 1
                    self.recurse_entity_types(v,level+1,k,None,None,patharraybuf,tentryarraybuf,detype2id,arrayid)
                elif level == 1:
                    fullpathval = ','.join(patharraybuf)
                    tentryarraybuf.append('insert into entity_types(id,category,subcat0,fullpath,value) values({},"{}","{}","{}","{}")'
                                          .format(arrayid[0],category,k,fullpathval,k))
                    arrayid[0] += 1
                    self.recurse_entity_types(v,level+1,category,k,None,patharraybuf,tentryarraybuf,detype2id,arrayid)
                else:
                    fullpathval = ','.join(patharraybuf)
                    cur_subcat1 = subcat1 if subcat1 is not None else k
                    tentryarraybuf.append('insert into entity_types(id,category,subcat0,subcat1,fullpath,value) values({},"{}","{}","{}","{}","{}")'
                                          .format(arrayid[0],category,subcat0,cur_subcat1,fullpathval,k))
                    arrayid[0] += 1
                    self.recurse_entity_types(v,level+1,category,subcat0,subcat1,patharraybuf,tentryarraybuf,detype2id,arrayid)
                patharraybuf.pop()
        elif isinstance(d,list):
            for v in d:
                fullpathval = ','.join(patharraybuf)
                if v in detype2id:
                    assert v not in detype2id
                detype2id[v] = arrayid[0]
                if level == 0:
                    tentryarraybuf.append('insert into entity_types(id,category,fullpath,value) values({},"{}","{}","{}")'
                                          .format(arrayid[0],category,fullpathval,v))
                    arrayid[0] += 1
                elif level == 1:
                    tentryarraybuf.append('insert into entity_types(id,category,subcat0,fullpath,value) values({},"{}","{}","{}","{}")'
                                          .format(arrayid[0],category,subcat0,fullpathval,v))
                    arrayid[0] += 1
                else:
                    tentryarraybuf.append('insert into entity_types(id,category,subcat0,subcat1,fullpath,value) values({},"{}","{}","{}","{}","{}")'
                                          .format(arrayid[0],category,subcat0,subcat1,fullpathval,v))
                    arrayid[0] += 1
        else:
            raise Exception('ERROR unrecognized format in make_sql_tables for d: {}'.format(d))

    def recurse_entity_types(self,d,level,category,subcat0,subcat1,patharraybuf,tentryarraybuf,detype2id,arrayid):
        if isinstance(d,dict):
            for k,v in d.items():
                patharraybuf.append(k)
                if k in detype2id:
                    assert k not in detype2id
                detype2id[k] = arrayid[0]
                fullpath = None
                if len(patharraybuf) != 0:
                    fullpath = ','.join(patharraybuf)
                    tentryarraybuf.append('insert into entity_types(id,value,fullpath) values({},"{}","{}");'.format(arrayid[0],k,fullpath))
                else:
                    tentryarraybuf.append('insert into entity_types(id,value) values({},"{}");'.format(arrayid[0],k))
                arrayid[0] += 1
                self.recurse_entity_types(v,level+1,k,None,None,patharraybuf,tentryarraybuf,detype2id,arrayid)
                patharraybuf.pop()
        elif isinstance(d,list):
            for v in d:
                fullpathval = ','.join(patharraybuf)
                if v in detype2id:
                    assert v not in detype2id
                detype2id[v] = arrayid[0]
                tentryarraybuf.append('insert into entity_types(id,value,fullpath) values({},"{}","{}");'.format(arrayid[0],v,fullpathval))
                arrayid[0] += 1

        else:
            raise Exception('ERROR unrecognized format in make_sql_tables for d: {}'.format(d))


    def make_sql_tables(self, do_print=True):

        # entity_type
        detype2id = {}
        id = 0
        arrayid = [id]
        entity_types = self.entity_types
        tentitytypes = []
        #tentitytypes.append('create table entity_types(id integer primary key, category text, subcat0 text, subcat1 text, fullpath text, value text)')
        tentitytypes.append('create table entity_types(id integer primary key, value text, fullpath text);')
        self.recurse_entity_types(entity_types,0,None,None,None,[],tentitytypes,detype2id,arrayid)

        print('-------------------ENTITY_TYPES')
        for line in tentitytypes:
            print(line)


        # cities and addresses
        tcities = []
        tcities.append('create table cities(id integer primary key, state text, city text, base_zip integer);')
        taddress = []
        taddress.append('create table addresses(id integer primary key autoincrement, id_city integer, street text, address_id integer, unit integer, zip integer, id_type);')
        data_addresses = self.data_addresses
        idcity = 0
        for statename,stateval in data_addresses[self.S_DATAKEY_STATES].items():
            for cityname,cityval in stateval[self.S_DATAKEY_CITIES].items():
                tcities.append('insert into cities(id,state,city,base_zip) values("{}","{}","{}",{});'
                               .format(idcity,statename,cityname,cityval[self.S_KEY_CITY_BASE_ZIP]))
                for streetname,streetval in cityval[self.S_DATAKEY_STREETS].items():
                    for addressname,addressval in streetval[self.S_DATAKEY_ADDRS].items():
                        if self.S_DATAKEY_ADDR_UNITS in addressval:
                            for unitid,unitval in addressval[self.S_DATAKEY_ADDR_UNITS].items():
                                try:
                                    address_id  = addressname # addressval[self.S_DATAKEY_ADDR_NUM_ID]
                                    unit        = addressval[self.S_DATAKEY_ADDR_UNIT_ID] # if self.S_DATAKEY_ADDR_UNIT_ID in addressval else None
                                    zip         = addressval[self.S_DATAKEY_ADDR_ZIP]
                                    id_type     = addressval[self.S_DATAKEY_ADDR_TYPE]
                                    taddress.append('insert into addresses(id_city,street,address_id,unit,zip,id_type) values({},"{}",{},{},{},"{}");'
                                                    .format(idcity,streetname,address_id,unit,zip,id_type))
                                    #if unit == None:
                                    #    taddress.append('insert into addresses(id_city,street,address_id,zip,id_type) values("{}","{}","{}","{}","{}")'
                                    #                    .format(idcity,streetname,address_id,zip,id_type))
                                    #else:
                                    #    taddress.append('insert into addresses(id_city,street,address_id,unit,zip,id_type) values("{}","{}","{}","{}","{}","{}")'
                                    #                    .format(idcity,streetname,address_id,unit,zip,id_type))
                                except Exception as e:
                                    p('ERROR: {}'.format(e))
                        else:
                            try:
                                address_id  = addressname # addressval[self.S_DATAKEY_ADDR_NUM_ID]
                                #unit        = addressval[self.S_DATAKEY_ADDR_UNIT_ID] if self.S_DATAKEY_ADDR_UNIT_ID in addressval else None
                                zip         = addressval[self.S_DATAKEY_ADDR_ZIP]
                                id_type     = addressval[self.S_DATAKEY_ADDR_TYPE]
                                taddress.append('insert into addresses(id_city,street,address_id,zip,id_type) values({},"{}",{},{},"{}");'
                                                .format(idcity,streetname,address_id,zip,id_type))
                                #if unit == None:
                                #    taddress.append('insert into addresses(id_city,street,address_id,zip,id_type) values("{}","{}","{}","{}","{}")'
                                #                .format(idcity,streetname,address_id,zip,id_type))
                                #else:
                                #    taddress.append('insert into addresses(id_city,street,address_id,unit,zip,id_type) values("{}","{}","{}","{}","{}","{}")'
                                #                    .format(idcity,streetname,address_id,unit,zip,id_type))
                            except Exception as e:
                                p('ERROR: {}'.format(e))
                idcity += 1
        print('-------------------CITIES')
        for line in tcities:
            print(line)
        print('-------------------ADDRESSES')
        for line in taddress:
            print(line)

        # entities
        data_entities = self.data_entities
        tentities = []
        tentities.append('create table entities(gid integer primary key, id_entity_category integer, id integer, firstname text, lastname text, id_entity_type, startdate date, enddate date);')
        for entity_category,entities in data_entities.items():
            id_entity_category = detype2id[entity_category]
            for k,v in entities.items():
                try:
                    id = v[self.S_ID]
                    firstname = v[self.S_ENTITY_FIRSTNAME] if self.S_ENTITY_FIRSTNAME in v else None
                    lastname = v[self.S_ENTITY_LASTNAME] if self.S_ENTITY_LASTNAME in v else None
                    entity_type = v[self.S_ENTITY_TYPE]
                    startdate = v[self.S_ENTITY_START_DATE] if self.S_ENTITY_START_DATE in v else None
                    enddate = v[self.S_ENTITY_END_DATE] if self.S_ENTITY_END_DATE in v else None
                    keys = ['id_entity_category','id']
                    values = [id_entity_category,id]
                    if firstname is not None:
                        keys.append('firstname')
                        values.append('"{}"'.format(firstname))
                    if lastname is not None:
                        keys.append('lastname')
                        values.append('"{}"'.format(lastname))
                    keys.append('id_entity_type')
                    values.append('"{}"'.format(entity_type))
                    strkeys = ','.join(keys)
                    aryvals = ['{}'.format(v) for v in values]
                    strvals = ','.join(aryvals)
                    tentities.append('insert into entities({}) values({});'.format(strkeys,strvals))
                except Exception as e:
                    p(e)
        print('-------------------ENTITIES')
        for line in tentities:
            print(line)

        # entity_relationships
        data_relationships = self.data_relationships
        trelationships = []
        trelationships.append('create table relationships(gid integer primary key, id_src, id_dst, id_relationship_type);')
        for idsrc,relationships in data_relationships.items():
            for relationship_type,array_iddst in relationships.items():
                id_relationship_type = detype2id[relationship_type]
                for iddst in array_iddst:
                    trelationships.append('insert into relationships(id_src,id_dst,id_relationship_type) values ({},{},{});'.format(idsrc,iddst,id_relationship_type))

        print('-------------------RELATIONSHIPS')
        for line in trelationships:
            print(line)

class ut(unittest.TestCase):
    '''
    def __init__(self):
        pass
    __init__ gets overridden, so dont define it
    '''
    def test_generate_db_data(self):

        def construct_database_0():
            t = sql_data_maker()
            data = t.make_table_cities(num_states=10,min_cities_per_state=2,max_cities_per_state=6)
            #print('\n')
            etypes = t.choose_type([sql_data_maker.S_CAT_ADDR,sql_data_maker.S_ADDR_RES],5)
            #print(etypes)
            #print('\n')
            etypes = t.choose_type([sql_data_maker.S_CAT_CONSUME,sql_data_maker.S_CONSUME_GRAINS],5)
            #print(etypes)
            t.make_table_addresses(data,3,8)
            json_val = json.dumps(data,indent=4,sort_keys=True)
            print(json_val)
            return

        def test_make_table_entities():
            t = sql_data_maker()
            t.num_original_descendants = 10
            t.max_num_person  = 500
            t.max_num_virtual = 100
            t.max_num_animal  = 1000

            data = t.make_table_cities(num_states=10,min_cities_per_state=5,max_cities_per_state=10)
            t.make_table_addresses(data,min_num_streets=3,max_num_streets=10)

            (entities,relationships) = t.make_table_entities()

            json_val = json.dumps(entities,indent=4,sort_keys=True)
            #print('----------------------entities')
            #print(json_val)

            json_val = json.dumps(relationships,indent=4,sort_keys=True)
            #print('----------------------relationships')
            #print(json_val)

            t.make_sql_tables()
            return

        #construct_database_0()
        test_make_table_entities()


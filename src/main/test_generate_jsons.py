import unittest
from .generate_multiple_jsons import TKEYS
from .generate_multiple_jsons import TVALS
from .generate_multiple_jsons import Row
from .generate_multiple_jsons import GenerateInheritedDicts

'''
UI view:

tags_affected:  
    tag_key     tag_value       
    <blank>     <blank>         add_button
                                add_another_button
    
    // example 1:
    //
    // tag_key  tag_value       
    // -------  ---------
    // env      beta            add_button
    // region   US              add_button
    // <blank>  <blank>         add_another_button
    //
    // apply change on beta/US/<all_children_of_US>
    //
    // --------------------------------------------------
    //
    // example 2:
    //
    // tag_key  tag_value       
    // -------  ---------
    // env      beta            add_button
    // cluster  CLUSTER_A       add_button
    // <blank>  <blank>         add_another_button
    //
    // apply change on only CLUSTER_A of beta/<all_regions>/<all_children_of_region>/CLUSTER_A
    //
    //
    // for single hierarchy, specify the full tag hierarchy, so keep adding buttons
    // to span across hierarchies, specify only the relevant root tag or tags

keyname_search -> searchable select of available keys from key/value payload

<table> shows all rules active for this key, and the tags_affected, so user doesnt duplicate.
        this is retrieved via jquery/ajax dynamically

optional subkey_path shows up if keyname is a dictionary -> javascript validate this is valid path

operations:
    operation_tuple:

        operation -> add|delete|substitute|override
        
        value_to_change -> javascript validate this is valid list,scalar,or dictionary
            // add means add to a list or dictionary
            // delete means delete from a list or dictionary
            // substitute is only for scalar value to replace, same as override with single value
            // override means entirely replace the existing value
            //

    add_another_operation_button
        // if you want to add another operation tuple, eg you can have any combo of add,delete,sub, etc

    // example 1
    //
    // this adds 2 operations: add and delete to a key k2, which is a dictionary. the operations are
    // applied on key k2's subkey_path of k210/k311, which is a list
    //
    // keyname_search
    //   k2
    //
    // optional subkey_path
    //   k210/k311          k2/k210/k311 is a list in this example
    //
    // operation 1
    //   operation
    //     delete
    //
    //   value_to_change
    //     [10,20,25]       if 10,20,25 are in value, remove those values. 
    //                      all children of this tag_value (eg region:US) also have 10,20,25 removed, 
    //                      unless a child tag_value adds 10,20,25 back in (eg region:US subcluster:SUB_CLUSTER_ABC)
    //
    // operation 2
    //   operation
    //     add
    //
    //   value_to_replace
    //     [11,30]          add 11,30 to list. 
    //                      all children of this tag_value (eg region:US) also have 11,30 added, 
    //                      unless a child tag_value deletes 11,30 (eg region:US subcluster:SUB_CLUSTER_ABC)




next button -> next page displays the diff and the hierarchies that will be modified and a
    "are you sure" button to confirm changeset

--------------------------------------------------

--------------------------------------------------

example basefile-1.json

{
    "filename": null,
    "group_subtree": {
        "t0a": {
            "filename": "basename1-1.json",
            "group_subtree": {
                "t1a": {
                    "filename": "basename1-1.json",
                    "group_subtree": {
                        "t2a": {
                            "filename": "basename1-8.json",
                            "group_subtree": {
                                "t3a": {
                                    "filename": "basename1-9.json",
                                    "group_subtree": {},
                                    "path": "t0a/t1a/t2a/t3a"
                                }
                            },
                            "path": "t0a/t1a/t2a"
                        },
                        "t2b": {
                            "filename": "basename1-10.json",
                            "group_subtree": {
                                "t3a": {
                                    "filename": "basename1-12.json",
                                    "group_subtree": {},
                                    "path": "t0a/t1a/t2b/t3a"
                                },
                                "t3b": {
                                    "filename": "basename1-11.json",
                                    "group_subtree": {},
                                    "path": "t0a/t1a/t2b/t3b"
                                }
                            },
                            "path": "t0a/t1a/t2b"
                        },
                        "t2c": {
                            "filename": "basename1-13.json",
                            "group_subtree": {
                                "t3a": {
                                    "filename": "basename1-15.json",
                                    "group_subtree": {},
                                    "path": "t0a/t1a/t2c/t3a"
                                },
                                "t3c": {
                                    "filename": "basename1-14.json",
                                    "group_subtree": {},
                                    "path": "t0a/t1a/t2c/t3c"
                                }
                            },
                            "path": "t0a/t1a/t2c"
                        }
                    },
                    "path": "t0a/t1a"
                },
                "t1b": {
                    "filename": "basename1-1.json",
                    "group_subtree": {
                        "t2a": {
                            "filename": "basename1-2.json",
                            "group_subtree": {},
                            "path": "t0a/t1b/t2a"
                        },
                        "t2b": {
                            "filename": "basename1-3.json",
                            "group_subtree": {
                                "t3a": {
                                    "filename": "basename1-5.json",
                                    "group_subtree": {},
                                    "path": "t0a/t1b/t2b/t3a"
                                },
                                "t3b": {
                                    "filename": "basename1-4.json",
                                    "group_subtree": {},
                                    "path": "t0a/t1b/t2b/t3b"
                                }
                            },
                            "path": "t0a/t1b/t2b"
                        },
                        "t2c": {
                            "filename": "basename1-6.json",
                            "group_subtree": {
                                "t3c": {
                                    "filename": "basename1-7.json",
                                    "group_subtree": {},
                                    "path": "t0a/t1b/t2c/t3c"
                                }
                            },
                            "path": "t0a/t1b/t2c"
                        }
                    },
                    "path": "t0a/t1b"
                }
            },
            "path": "t0a"
        }
    },
    "path": "basename1"
}

--------------------------------------------------

example of payload for consumption:

{
    "k1v": 10,
    "k2v": 50,
    "k3a": [
        1,
        2,
        3,
        100,
        220
    ],
    "k4a": [
        4,
        7,
        8
    ],
    "k5m": {
        "km1v": 10,
        "km2a": [
            10,
            11,
            12
        ],
        "km3m": {
            "k3.1": 100,
            "k3.2": 200
        }
    },
    "k6m": {
        "km1v": 40,
        "km2a": [
            20,
            21,
            22
        ],
        "km3m": {
            "k3.1": 300,
            "k3.2": 400
        }
    }
}

--------------------------------------------------

example output of intermediate tree

{
    E.RJSONNAME: {
        // JSON BASENAME
        json_basename1: {
            // STAGE
            E.RTAGH1: {
                stageval1: {
                    default: {
                        rows: [row,row,row]
                    },
                    E.RTAGH2: {
                        tagh2key1: {
                            default: {
                                rows: [row,row,row]
                            },
                            E.RTAGH3: {}
                        },
                        tagh2key2: {
                            default: {
                                rows: []
                            },
                            E.RTAGH3: {
                                tagh3key1: {
                                    default: {
                                        rows: [row,row,row]
                                    },
                                    E.RTAGH4: {}
                                }
                            }
                        }
                    }
                },
                stageval2: {
                    default: {
                        rows: [row,row,row]
                    },
                    E.RTAGH2: {
                        tagh2key1: {
                            default: {
                                rows: [row,row,row]
                            },
                            E.RTAGH3: {}
                        },
                        tagh2key2: {
                            default: {
                                rows: []
                            },
                            E.RTAGH3: {
                                default: {
                                    rows: []
                                },
                                tagh3key1: {
                                    default: {
                                        rows: [row,row,row]
                                    },
                                    E.RTAGH4: {}
                                }
                            }
                        }
    
                    ]
                },
                ...
            }
        },
        json_basename2: {
        }
    }
}

{
    tagh1val1: {
        default: jsonfile1.json,            // json for this tagval
        tagh2val1: {
            default: jsonfile2.json         // json for this tagval
        },
        tagh2val2: {
                                            // no json for this tagval because no overrides, use parent json
            tagh3val1: {
                default: jsonfile3.json     // json for this tagval, which is same tagval across all tagh2 levels
            }
        },
        tagh2val3: {
            default: jsonfile4.json,        // json for this tagval
            tagh3val1: {
                default: jsonfile5.json     // json for this tagval, same across all tagh2 + some overrides, hence not jsonfile3.json
            },
            tagh3val2: {
                default: jsonfile6.json
            }
        },
        tagh2val4: {
            tagh3val1: {
                default: jsonfile3.json     // json for this tagval, same as default for tagh2, hence jsonfile3.json
            }
        }
    }
}

'''

class Test_generate_multiple_json(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_generate_multiple_json, self).__init__(*args, **kwargs)
        self.generator = GenerateInheritedDicts()

    def get_tag_hierarchy_values_case_1(self):
        tag_hierarchy_values = {
            TKEYS.TAGKBASE: {'basename1'},
            TKEYS.TAGK0 : {'t0a'},
            TKEYS.TAGK1 : {'t1a','t1b'},
            TKEYS.TAGK2 : {'t2a','t2b','t2c'},
            TKEYS.TAGK3 : {'t3a','t3b','t3c'},
            TKEYS.TAGK4 : {'t4a','t4b'}
        }
        return tag_hierarchy_values


    def populate_row_vectors_case1(self):
        rows = []
        rows.append(Row('k1v',10,dict_tags={TKEYS.TAGK0:'t0a'}))
        rows.append(Row('k2v',20,dict_tags={TKEYS.TAGK0:'t0a'}))
        rows.append(Row('k3a',[1,2,3],dict_tags={TKEYS.TAGK0:'t0a'}))
        rows.append(Row('k4a',[4,5,6],dict_tags={TKEYS.TAGK0:'t0a'}))
        rows.append(Row('k5m',{
            'km1v':10,
            'km2a':[10,11,12],
            'km3m':{'k3.1':100,'k3.2':200}},dict_tags={TKEYS.TAGK0:'t0a'}))
        rows.append(Row('k6m',{
            'km1v':40,
            'km2a':[20,21,22],
            'km3m':{'k3.1':300,'k3.2':400}},dict_tags={TKEYS.TAGK0:'t0a'}))

        # expect k2v = 30
        rows.append(Row('k2v',dict_tags={TKEYS.TAGK1:'t1a',TKEYS.TAGK2:'t2a'},dict_ops={TKEYS.OPSUB:30}))
        # expect k2v = 30
        rows.append(Row('k2v',dict_tags={TKEYS.TAGK2:'t2b'},dict_ops={TKEYS.OPSUB:40}))
        # expect k2v = 50
        rows.append(Row('k2v',dict_tags={TKEYS.TAGK2:'t2b',TKEYS.TAGK3:'t3a'},dict_ops={TKEYS.OPSUB:50}))
        # expect k2v = 50 hard override
        rows.append(Row('k2v',dict_tags={TKEYS.TAGK2:'t2c'},dict_ops={TKEYS.OPOVR:50}))
        # t2a adds.
        # expect 4ka = 4,5,6,7,8
        rows.append(Row('k4a',dict_tags={TKEYS.TAGK2:'t2a'},dict_ops={TKEYS.OPADD:[7,8]}))
        # t2b adds 7,8, removes 5,6,10 if exists.
        # expect 4ka = 4,7,8
        rows.append(Row('k4a',dict_tags={TKEYS.TAGK2:'t2b'},dict_ops={TKEYS.OPADD:[7,8],TKEYS.OPDEL:[5,6,10]}))
        # t2b.t3b adds 9,10, but vsub from parent removes 10. removes 4 from t2b profile
        # expect 4ka = 7,8,9
        rows.append(Row('k4a',dict_tags={TKEYS.TAGK2:'t2b',TKEYS.TAGK3:'t3b'},dict_ops={TKEYS.OPADD:[9,10],TKEYS.OPDEL:[4]}))
        # expect 4ka = 4,5,6,20,21,22
        rows.append(Row('k4a',dict_tags={TKEYS.TAGK2:'t2c',TKEYS.TAGK3:'t3c'},dict_ops={TKEYS.OPADD:[20,21,22]}))
        # always overrides whatever is parent in this case
        # expect 4ka =  {}
        #rows.append(Row('k4a',{},tagh2='t2d'))
        rows.append(Row('k4a',dict_tags={TKEYS.TAGK2:'t2d'},dict_ops={TKEYS.OPOVR:[]}))
        # always overrides whatever is parent in this case
        # expect 4ka =  7,8 hard override
        rows.append(Row('k4a',dict_tags={TKEYS.TAGK2:'t2d',TKEYS.TAGK3:'t3a'},dict_ops={TKEYS.OPOVR:[7,8]}))
        # expect k6m = {
        #             'k1v':50,
        #             'k2a':[22,30,31,32],
        #             'k3m':{'k3.1':300,'k3.2':500}}
        rows.append(Row('k6m',dict_tags={TKEYS.TAGK2:'t2a'},subkey_path='km1v',dict_ops={TKEYS.OPSUB:50}))
        rows.append(Row('k6m',dict_tags={TKEYS.TAGK2:'t2a'},subkey_path='km2a',dict_ops={TKEYS.OPADD:[30,31,32],TKEYS.OPDEL:[20,21]}))
        rows.append(Row('k6m',dict_tags={TKEYS.TAGK2:'t2a'},subkey_path='km3m/k3.2',dict_ops={TKEYS.OPSUB:500}))
        rows.append(Row('k3a',dict_tags={TKEYS.TAGK1:'t1a',TKEYS.TAGK3:'t3a'},dict_ops={TKEYS.OPADD:[100,220]}))

        return rows

    def populate_row_vectors_case2(self):
        rows = []
        rows.append(Row('k1v',10,dict_tags={TKEYS.TAGK0:'t0a'}))
        rows.append(Row('k2v',20,dict_tags={TKEYS.TAGK0:'t0a'}))
        rows.append(Row('k3a',[1,2,3],dict_tags={TKEYS.TAGK0:'t0a'}))
        rows.append(Row('k4a',[4,5,6],dict_tags={TKEYS.TAGK0:'t0a'}))
        rows.append(Row('k5m',{
            'km1v':10,
            'km2a':[10,11,12],
            'km3m':{'k3.1':100,'k3.2':200}},dict_tags={TKEYS.TAGK0:'t0a'}))
        rows.append(Row('k6m',{
            'km1v':40,
            'km2a':[20,21,22],
            'km3m':{'k3.1':300,'k3.2':400}},dict_tags={TKEYS.TAGK0:'t0a'}))
        rows.append(Row('k4a',dict_tags={TKEYS.TAGK2:'t2b'},dict_ops={TKEYS.OPADD:[7,8],TKEYS.OPDEL:[5,6,10]}))
        rows.append(Row('k4a',dict_tags={TKEYS.TAGK2:'t2b',TKEYS.TAGK3:'t3b'},dict_ops={TKEYS.OPADD:[9,10],TKEYS.OPDEL:[4]}))
        rows.append(Row('k4a',dict_tags={TKEYS.TAGK2:'t1a',TKEYS.TAGK3:'t3c'},dict_ops={TKEYS.OPADD:[20,21,22]}))
        return rows

    def test_next_tag_key(self):
        tag_key_order_list = TVALS.TAG_KEY_ORDER

        row = Row('k2v',dict_tags={TKEYS.TAGK1:'t1a',TKEYS.TAGK2:'t2a'},dict_ops={TKEYS.OPSUB:30})
        next_tag_key = self.generator.get_next_tag_key_from_row(row,tag_key_order_list)
        assert next_tag_key == TKEYS.TAGK1
        next_tag_key = self.generator.get_next_tag_key_from_row(row,tag_key_order_list,next_tag_key)
        assert next_tag_key == TKEYS.TAGK2

        row = Row('k2v',dict_tags={TKEYS.TAGK1:'t1a',TKEYS.TAGK3:'t3a'},dict_ops={TKEYS.OPSUB:30})
        next_tag_key = self.generator.get_next_tag_key_from_row(row,tag_key_order_list)
        assert next_tag_key == TKEYS.TAGK1
        next_tag_key = self.generator.get_next_tag_key_from_row(row,tag_key_order_list,next_tag_key)
        assert next_tag_key == TKEYS.TAGK3

    def test_generate_tree_from_dict_hierarchy(self):
        dict_hierarchy = {
            TKEYS.TAGKBASE:{
                'basename2':{
                    TKEYS.TAGK0:{
                        't0a':{
                            TKEYS.TAGK1:{
                                't1a':{
                                    TKEYS.TAGK2:{
                                        't2a':{
                                            TKEYS.TAGK3:{
                                                't3a':{},
                                                't3b':{}
                                            }
                                        }
                                    }
                                },
                                't1b':{
                                    TKEYS.TAGK2:{
                                        't2a':{
                                            TKEYS.TAGK3:{
                                                't3a':{},
                                                't3b':{
                                                    TKEYS.TAGK4:{
                                                        't4a':{},
                                                        't4b':{}
                                                    }
                                                }
                                            }
                                        },
                                        't2b':{
                                            TKEYS.TAGK3:{
                                                't3a':{}
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        't0b':{
                            TKEYS.TAGK1:{
                                't1a':{}
                            }
                        }
                    }
                }
            }
        }
        try:
            tag_order_list = [TKEYS.TAGKBASE,TKEYS.TAGK0,TKEYS.TAGK1,TKEYS.TAGK2,TKEYS.TAGK3,TKEYS.TAGK4]
            tree = self.generator.generate_tree_from_dict_hierarchy(dict_hierarchy,tag_order_list)
            return
        except Exception as e:
            raise e
    def test_process_rows_to_jsons2(self):
        tags = self.get_tag_hierarchy_values_case_1()
        rows = self.populate_row_vectors_case2()
        flag = False
        try:
            result = self.generator.process_rows_to_files(rows,tags,TVALS.TAG_KEY_ORDER)
            assert result != None
        except Exception as e:
            flag = True
        return

    def test_process_rows_to_jsons3(self):
        tags = self.get_tag_hierarchy_values_case_1()
        rows = self.populate_row_vectors_case1()
        flag = False
        try:
            result = self.generator.process_rows_to_files(rows,tags,TVALS.TAG_KEY_ORDER)
            assert result != None
        except Exception as e:
            flag = True
        return


    def test_basic1(self):
        pass

if __name__ == "__main__":
    unittest.main()





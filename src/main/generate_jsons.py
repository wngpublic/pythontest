import json
import copy
import os

class TKEYS:
    TAGKBASE        = 'tag_base'
    TAGK0           = 'tag_key_0'
    TAGK1           = 'tag_key_1'
    TAGK2           = 'tag_key_2'
    TAGK3           = 'tag_key_3'
    TAGK4           = 'tag_key_4'
    TAGK5           = 'tag_key_5'
    TAGK6           = 'tag_key_6'
    TAGK7           = 'tag_key_7'

    KEY             = 'key'
    VAL             = 'val'
    VALTYPE         = 'val_type'
    LIST            = 'list'
    DICT            = 'dict'
    SET             = 'set'
    SCALAR          = 'scalar'
    OBJECT          = 'object'

    OPADD           = 'add'
    OPDEL           = 'del'
    OPSUB           = 'sub'
    OPOVR           = 'override'

    GROUP_TAGS      = 'group_tags'
    GROUP_ROWS      = 'group_rows'
    GROUP_OPS       = 'group_ops'
    GROUP_SUBTREE   = 'group_subtree'

    TAGS            = 'tags'

    ID              = 'id'
    PATH            = 'path'
    PATH_LIST       = 'path_list'
    SUBKEY_PATH     = 'subkey_path'
    TAGGROUPOPS     = 'tag_ops'
    FILENAME        = 'filename'
    FULL_PAYLOAD    = 'full_payload'
    VERSION         = 'version'

    IS_MODIFIED     = 'is_modified'
    IS_ACTIVE       = 'is_active'

class TVALS:
    TAG_KEY_ORDER   = [TKEYS.TAGK0,TKEYS.TAGK1,TKEYS.TAGK2,TKEYS.TAGK3,TKEYS.TAGK4,TKEYS.TAGK5,TKEYS.TAGK6,TKEYS.TAGK7]

class util:
    @staticmethod
    def get_edata_type(value):
        if value == None:
            return None
        if isinstance(value,list):
            return TKEYS.LIST
        if isinstance(value,dict):
            return TKEYS.DICT
        if isinstance(value,set):
            return TKEYS.SET
        return TKEYS.OBJECT

class Row:
    GID = 0

    def __init__(self,
                 key,                       # key name of value, not tag_key hierarchy name
                 val=None,
                 subkey_path=None,          # specify if modify key is dict and modify subkey
                 basename='basename1',
                 dict_tags={},              # tag_key associated with this key
                 dict_ops={},
                 isactive=True):
        self.id = Row.GID
        Row.GID += 1

        self.key                = key
        self.val                = val
        self.valtype            = util.get_edata_type(val)
        self.subkey_path = subkey_path    # keypath is split by delimiter / to get to correct hierarchy
        self.basename           = basename
        self.dict_tags          = dict_tags
        self.dict_ops           = dict_ops
        self.isactive           = isactive
        self.is_override        = False if(len(dict_tags) == 0 or
                                           (len(dict_tags) == 1 and TKEYS.TAGK0 in dict_tags)) \
            else True

        self.map = {
            TKEYS.ID            : self.id,
            TKEYS.KEY           : self.key,
            TKEYS.VAL           : self.val,
            TKEYS.VALTYPE       : self.valtype,
            TKEYS.SUBKEY_PATH   : self.subkey_path,
            TKEYS.TAGKBASE      : self.basename,
            TKEYS.GROUP_TAGS    : self.dict_tags,
            TKEYS.GROUP_OPS     : self.dict_ops,
            TKEYS.IS_ACTIVE     : self.isactive
        }

    def get_row_map(self):
        return self.map

    def to_string(self):
        return f"id:{self.id} key:{self.key} val:{self.val} keypath:{self.subkey_path}"


class GenerateInheritedDicts:
    ID = 1
    VERSION = 1
    VERSION_FILENAME = 1

    def __init__(self):
        self.keypath_delimiter = '/'
        self.cur_id = self.get_next_id()
        self.tag_order_dict = TVALS.TAG_KEY_ORDER
        self.filename_suffix = '.json'
        self.tree = None

    def get_next_id(self):
        id = GenerateInheritedDicts.ID
        GenerateInheritedDicts.ID += 1
        return id

    def get_version_id(self,do_increment=False):
        id = GenerateInheritedDicts.VERSION
        if do_increment == True:
            GenerateInheritedDicts.VERSION += 1
        return id

    def get_next_version_filename_id(self):
        v = GenerateInheritedDicts.VERSION_FILENAME
        GenerateInheritedDicts.VERSION_FILENAME += 1
        return v

    def get_next_version_id(self):
        self.get_version_id(True)
        return self.get_version_id()

    def set_keypath_delimiter(self,delimiter):
        self.keypath_delimiter = delimiter

    def get_next_tag_key_from_ordered_list(self,cur_tag_key,tag_key_order_list):
        last_visited_idx = 0
        if cur_tag_key == None:
            return tag_key_order_list[0]
        sz = len(tag_key_order_list)
        for i in range(last_visited_idx,sz):
            if cur_tag_key == tag_key_order_list[i]:
                if (i+1) < sz:
                    return tag_key_order_list[i+1]
                else:
                    return None
        return None

    def get_next_tag_key_from_row(self,row,tag_key_order_list,cur_tag_key=None):
        sz = len(tag_key_order_list)
        row_tags = row.get_row_map()[TKEYS.GROUP_TAGS]
        idx = None

        if cur_tag_key == None:
            for i in range(sz):
                if tag_key_order_list[i] in row_tags:
                    return tag_key_order_list[i]
            return None

        next_tag_key = cur_tag_key
        for i in range(sz):
            if next_tag_key == tag_key_order_list[i]:
                idx = i+1
                break

        if idx == None:
            return None
        for i in range(idx,sz):
            if tag_key_order_list[i] in row_tags:
                return tag_key_order_list[i]
        return None

    def generate_tree_info_structure(self,path=None,filename=None,version=None,modified=None):
        node = {
            TKEYS.PATH:path,
            TKEYS.FILENAME:filename,
            TKEYS.GROUP_SUBTREE:{},
            #TKEYS.IS_MODIFIED:None
        }
        return node

    def generate_tree_file_structure(self,path=None,tag_key=None,tag_val=None,version=None):
        updated_version = version if version != None else self.get_version_id(True)
        node = {
            TKEYS.ID:self.get_next_id(),
            TKEYS.GROUP_TAGS:{},
            TKEYS.PATH:path,
            TKEYS.FILENAME:None,
            TKEYS.FULL_PAYLOAD:None,
            TKEYS.TAGKBASE:tag_val,
            TKEYS.GROUP_SUBTREE:{},
            TKEYS.VERSION:updated_version,
            TKEYS.IS_MODIFIED:False
        }
        if tag_key != None and tag_val != None:
            node[TKEYS.GROUP_TAGS][tag_key] = tag_val
        return node

    def generate_general_tag_node_structure(self,path=None,tag_key=None,tag_val=None):
        node = {
            TKEYS.ID:self.get_next_id(),
            TKEYS.PATH:path,
            TKEYS.GROUP_TAGS:{},
            TKEYS.GROUP_ROWS:[],
            TKEYS.GROUP_SUBTREE:{}
        }
        if tag_key != None and tag_val != None:
            node[TKEYS.GROUP_TAGS][tag_key] = tag_val
        return node

    '''

    this is used as template tree. use this tree to put the rows of
    data into the correct hierarchy, where rows may be repeated.

    after putting rows of data into this hiearchy, create a new tree
    with inherited/modified values for each subtree node
    :param dict_tags:
        {
            TKEYS.TAGKBASE:'jsonbase1',
            TKEYS.TAGK0: [v0,v1],
            TKEYS.TAGK1: [v10,v11,v12],
            TKEYS.TAGK2: [v20,v21,v22],
            TKEYS.TAGK3: [v30,v31,v32],
            TKEYS.TAGK4: [v40,v41,v42],
        }
    :return:
        {
            'basename1':{
                TKEYS.ID = <id>,
                TKEYS.PATH = 'hierarchy string value',
                // dict
                TKEYS.GROUP_TAGS:{
                    TKEYS.TAGKBASE:'...'
                },
                // list
                TKEYS.GROUP_NODES:[row1,row2,...],
                TKEYS.GROUP_SUBTREE:{
                    v0:{
                        TKEYS.ID = <id>,
                        TKEYS.PATH = 'hierarchy string value',
                        TKEYS.GROUP_TAGS:{TKEYS.TAGK0:'...'},
                        TKEYS.GROUP_NODES:[row1,row2,...],
                        TKEYS.GROUP_SUBTREE:{
                            v10:{
                                TKEYS.ID = <id>,
                                TKEYS.PATH = 'hierarchy string value',
                                TKEYS.GROUP_TAGS:{TKEYS.TAGK1:'...'},
                                TKEYS.GROUP_NODES:[row1,row2,...],
                                TKEYS.GROUP_SUBTREE:{
                                    v20:{
                                        TKEYS.ID = <id>,
                                        TKEYS.PATH = 'hierarchy string value',
                                        TKEYS.GROUP_TAGS:{TKEYS.TAGK2:'...'},
                                        TKEYS.GROUP_NODES:[row1,row2,...],
                                        TKEYS.GROUP_SUBTREE:{
                                            v30:{
                                                ...
                                            },
                                            v31:{
                                            }
                                        }
                                    },
                                    v21:{
                                        ...
                                    }
                                }
                            },
                            v11:{
                                ...
                            }
                        }
                    }
                }
            }
        }

    '''
    def generate_general_tag_tree(self,dict_tags,tag_key_order_list):
        def generate_tag_tree(dict_tags,tree,tag_key_order_list,subpath=[],idx_tag_key_order_list=0):
            try:
                sz = len(tag_key_order_list)
                if idx_tag_key_order_list >= sz:
                    return
                tag_key_from_order_list = tag_key_order_list[idx_tag_key_order_list]
                if tag_key_from_order_list not in dict_tags:
                    return
                for tag_val in dict_tags[tag_key_from_order_list]:
                    subpath.append(tag_val)
                    path = self.keypath_delimiter.join(subpath)
                    tree[TKEYS.GROUP_SUBTREE][tag_val] = self.generate_general_tag_node_structure(
                        path=path,tag_key=tag_key_from_order_list,tag_val=tag_val)
                    generate_tag_tree(dict_tags,tree[TKEYS.GROUP_SUBTREE][tag_val],tag_key_order_list,subpath,idx_tag_key_order_list+1)
                    subpath.pop()
            except Exception as e:
                raise e
            finally:
                return

        def generate_tag_tree_base(dict_tags,tree):
            tag_bases = dict_tags[TKEYS.TAGKBASE]
            for tag_base in tag_bases:
                tree[tag_base] = self.generate_general_tag_node_structure(tag_base,TKEYS.TAGKBASE,tag_base)

        tree = {}
        generate_tag_tree_base(dict_tags,tree)
        for basenames,subtree in tree.items():
            generate_tag_tree(dict_tags,subtree,tag_key_order_list)
        return tree

    def generate_tree_from_dict_hierarchy(self,dict_hierarchy,tag_key_order_list):
        def generate_tree(dict_hierarchy,tree,tag_key_order_list,subpath=[],idx_tag_key=0):
            for tag_key,subtree_hierarchy in dict_hierarchy.items():
                assert tag_key in tag_key_order_list
                for tag_value,subtree_tree in subtree_hierarchy.items():
                    subpath.append(tag_value)
                    path = self.keypath_delimiter.join(subpath)
                    tree[tag_value] = self.generate_general_tag_node_structure(
                        path=path,tag_key=tag_key,tag_val=tag_value)
                    generate_tree(
                        dict_hierarchy[tag_key][tag_value],
                        tree[tag_value][TKEYS.GROUP_SUBTREE],
                        tag_key_order_list,
                        subpath,
                        idx_tag_key+1)
                    subpath.pop()
        tree = {}
        generate_tree(dict_hierarchy,tree,tag_key_order_list)
        return tree



    def put_row_in_tag_tree(self,
                                 row,
                                 tree,
                                 tag_key_order_list,
                                 idx_tag_key_order_list=0,
                                 row_tag_key_to_match=None):
        sz = len(tag_key_order_list)
        if idx_tag_key_order_list >= sz:
            return
        tag_key_from_order_list = tag_key_order_list[idx_tag_key_order_list]
        rowmap = row.get_row_map()
        rowtags_dict = rowmap[TKEYS.GROUP_TAGS]

        # if no tags in row, put it in top level of tree
        if idx_tag_key_order_list == 0 and len(rowtags_dict) == 0:
            tree[TKEYS.GROUP_ROWS].append(row)
            return

        # find the next row tag key to match with current tree view
        cur_row_tag_key_to_match = row_tag_key_to_match if row_tag_key_to_match != None else \
            self.get_next_tag_key_from_row(row,tag_key_order_list)
        if cur_row_tag_key_to_match == None:
            return

        # if current tag key is not in current level, traverse to all elements in next level til match
        if(cur_row_tag_key_to_match not in tree[TKEYS.GROUP_TAGS]):
            if(len(tree[TKEYS.GROUP_SUBTREE]) == 0):
                return
            for subtree_key,subtree in tree[TKEYS.GROUP_SUBTREE].items():
                self.put_row_in_tag_tree(
                    row,
                    subtree,
                    tag_key_order_list,
                    idx_tag_key_order_list+1,
                    cur_row_tag_key_to_match)
            return

        # if next tag key matches current level
        cur_row_tag_val_to_match = rowtags_dict[cur_row_tag_key_to_match]
        tree_tag_val = tree[TKEYS.GROUP_TAGS][cur_row_tag_key_to_match]
        if(cur_row_tag_val_to_match != tree_tag_val):
            return

        # put in current view only if row is last key in hierarchy
        next_row_tag_key_to_match = self.get_next_tag_key_from_row(row,tag_key_order_list,cur_row_tag_key_to_match)
        if next_row_tag_key_to_match == None:
            tree[TKEYS.GROUP_ROWS].append(row)
            return

        for subtree_key,subtree in tree[TKEYS.GROUP_SUBTREE].items():
            self.put_row_in_tag_tree(
                row,
                subtree,
                tag_key_order_list,
                idx_tag_key_order_list+1,
                next_row_tag_key_to_match)

        return

    def populate_rows_to_tag_tree(self,rows,tree,tag_key_order_list):
        for row in rows:
            rowmap = row.get_row_map()
            try:
                if rowmap[TKEYS.IS_ACTIVE] == False:
                    continue
                rowmap = row.get_row_map()
                basename = rowmap[TKEYS.TAGKBASE]
                assert basename in tree
                self.put_row_in_tag_tree(row,tree[basename],tag_key_order_list)
            except Exception as e:
                raise e
        return

    def generate_tree_hierarchy_with_rows(self,rows,dict_tags,tag_key_order_list):
        try:
            tree_rows = self.generate_general_tag_tree(dict_tags,tag_key_order_list)
            self.populate_rows_to_tag_tree(rows,tree_rows,tag_key_order_list)
            return tree_rows
        except Exception as e:
            raise e

    def get_reference_to_map_keypath(self,input_map,keypath_string):
        '''
        returns reference to subpath of a dict payload

        :param input_map: the dict payload
        :param keypath_string: the keypath to the key:value of input_map, delimited by keypath_delimiter
        :return:  returns subkey_name,parent of input_map[subkey_name]

        if input_map = {
            k1:{
                k2:{
                    k3:{
                        k4:{
                            k5:v5
                        }
                    }
                }
            }
        }

        and keypath_string = k1/k2/k3/k4, return
        k4,the payload at input_map[k1][k2][k3], which is:
        {
            k4:{
                k5:v5
            }
        }
        '''
        if keypath_string == None:
            return None
        keypath_array = keypath_string.split(self.keypath_delimiter)

        parent_key = None
        subpath = input_map
        last_key = None
        for k in keypath_array:
            if k not in subpath:
                string_map_val = json.dumps(input_map)
                raise Exception('path not exist in map for keypath_array {} for input_map: {}'.format(keypath_array,string_map_val))
            parent_key = subpath
            subpath = subpath[k]
            last_key = k
        return (last_key,parent_key)

    def evaluate_row_default_val(self,key,row,input_value):
        rowmap = row.get_row_map()
        result = input_value
        if rowmap[TKEYS.VAL] != None:
            result = rowmap[TKEYS.VAL]
        return result


    def evaluate_row_rules_on_value_override_val(self,key,row,input_value):
        rowmap = row.get_row_map()
        if TKEYS.OPOVR not in rowmap[TKEYS.GROUP_OPS]:
            return input_value
        data_row = rowmap[TKEYS.GROUP_OPS][TKEYS.OPOVR]
        dtype_val = util.get_edata_type(input_value)
        dtype_row = util.get_edata_type(data_row)
        result = input_value

        if input_value == None:
            result = data_row
        else:
            if dtype_val != dtype_row:
                raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))
            result = data_row

        return result

    def evaluate_row_rules_on_value_override_add(self,key,row,input_value):
        rowmap = row.get_row_map()
        if TKEYS.OPADD not in rowmap[TKEYS.GROUP_OPS]:
            return input_value
        data_row = rowmap[TKEYS.GROUP_OPS][TKEYS.OPADD]
        dtype_val = util.get_edata_type(input_value)
        dtype_row = util.get_edata_type(data_row)
        result = input_value

        if dtype_val == TKEYS.LIST:
            if dtype_row != dtype_val:
                raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))
            result = result.copy()
            for v in data_row:
                if v not in result:
                    result.append(v)
        elif dtype_val == TKEYS.SET:
            if dtype_row != dtype_val:
                raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))
            result = result.copy()
            for v in data_row:
                result.add(v)
        elif dtype_val == TKEYS.DICT:
            keypath = rowmap[TKEYS.SUBKEY_PATH]
            if keypath != None:
                result = copy.deepcopy(result)
                (leaf_key,subpath) = self.get_reference_to_map_keypath(result,keypath)
                dtype_subpath = util.get_edata_type(subpath[leaf_key])
                if dtype_subpath != dtype_row:
                    raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))
                if dtype_row == TKEYS.LIST:
                    for v in data_row:
                        subpath[leaf_key].append(v)
                elif dtype_row == TKEYS.SET:
                    for v in data_row:
                        subpath[leaf_key].add(v)
                elif dtype_row == TKEYS.DICT:
                    for k,v in data_row.items():
                        subpath[leaf_key][k] = v
                else:
                    subpath[leaf_key] = data_row
            elif dtype_row == TKEYS.DICT:
                result = data_row
            else:
                raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))
        elif dtype_row == TKEYS.OBJECT:
            result = data_row
        return result

    def evaluate_row_rules_on_value_override_del(self,key,row,input_value):
        rowmap = row.get_row_map()
        if TKEYS.OPDEL not in rowmap[TKEYS.GROUP_OPS]:
            return input_value
        data_row = rowmap[TKEYS.GROUP_OPS][TKEYS.OPDEL]
        dtype_val = util.get_edata_type(input_value)
        dtype_row = util.get_edata_type(data_row)
        result = input_value

        if dtype_val == TKEYS.LIST:
            if dtype_row != dtype_val:
                raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))
            result = result.copy()
            for v in data_row:
                if v in result:
                    result.remove(v)
        elif dtype_val == TKEYS.SET:
            if dtype_row != dtype_val:
                raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))
            result = result.copy()
            for v in data_row:
                if v in result:
                    result.remove(v)
        elif dtype_val == TKEYS.DICT:
            keypath = rowmap[TKEYS.SUBKEY_PATH]
            if keypath != None:
                result = copy.deepcopy(result)
                (leaf_key,subpath) = self.get_reference_to_map_keypath(result,keypath)
                dtype_subpath = util.get_edata_type(subpath[leaf_key])
                if dtype_subpath != dtype_row:
                    raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))
                if dtype_row == TKEYS.LIST:
                    for v in data_row:
                        if v in subpath[leaf_key]:
                            subpath[leaf_key].remove(v)
                elif dtype_row == TKEYS.SET:
                    for v in data_row:
                        if v in subpath[leaf_key]:
                            subpath[leaf_key].remove(v)
                elif dtype_row == TKEYS.DICT:
                    for k,v in data_row.items():
                        if k in subpath[leaf_key]:
                            subpath[leaf_key].pop(v)
                else:
                    subpath[leaf_key] = data_row
            elif dtype_row == TKEYS.DICT:
                result = data_row
            else:
                raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))
        elif dtype_row == TKEYS.OBJECT:
            if data_row == result:
                result = None

        return result

    def evaluate_row_rules_on_value_override_sub(self,key,row,input_value):
        rowmap = row.get_row_map()
        if TKEYS.OPSUB not in rowmap[TKEYS.GROUP_OPS]:
            return input_value
        data_row = rowmap[TKEYS.GROUP_OPS][TKEYS.OPSUB]
        dtype_val = util.get_edata_type(input_value)
        dtype_row = util.get_edata_type(data_row)
        result = input_value

        if dtype_row == TKEYS.SET or dtype_row == TKEYS.LIST:
            raise Exception('cannot substitute set or arrayfor rowmap:{} and value:{}'.format(row.to_string(),input_value))
        if dtype_val == TKEYS.DICT:
            keypath = rowmap[TKEYS.SUBKEY_PATH]
            if keypath != None:
                result = copy.deepcopy(result)
                (leaf_key,subpath) = self.get_reference_to_map_keypath(result,keypath)
                dtype_subpath = util.get_edata_type(subpath[leaf_key])
                if dtype_subpath != dtype_row:
                    raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))
                subpath[leaf_key] = data_row
            elif dtype_row == TKEYS.DICT:
                result = data_row
            else:
                raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))
        elif dtype_row == TKEYS.OBJECT:
            result = data_row
        else:
            if dtype_val != None and dtype_val != TKEYS.DICT and dtype_row != dtype_val:
                raise Exception('data type mismatch for rowmap:{} and value:{}'.format(row.to_string(),input_value))

        return result

    def apply_row_rules_on_cur_value(self,key,row,parent_value):
        result = parent_value

        rowmap = row.get_row_map()
        try:
            flag = False
            if key == 'k3a':
                flag = True
            result = self.evaluate_row_default_val(key,row,result)
            result = self.evaluate_row_rules_on_value_override_val(key,row,result)
            result = self.evaluate_row_rules_on_value_override_add(key,row,result)
            result = self.evaluate_row_rules_on_value_override_del(key,row,result)
            result = self.evaluate_row_rules_on_value_override_sub(key,row,result)
        except Exception as e:
            raise e
        return result

    def write_payload_to_file(self,filename,dict_payload,dir='tmp'):
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename_final = '{}/{}'.format(dir,filename)
        with open(filename_final,'w') as fw:
            json_pretty = json.dumps(dict_payload,indent=4,sort_keys=True)
            fw.write(json_pretty)

    def evaluate_rows_in_subtree(self,tree_rows,parent_tree_files,tree_files,tag_key_order_list):
        try:
            tree_dict_modified = {}
            parent_tree_dict = {} if(parent_tree_files == None or len(parent_tree_files)==0) else parent_tree_files[TKEYS.FULL_PAYLOAD]

            tree_files[TKEYS.GROUP_TAGS] = tree_rows[TKEYS.GROUP_TAGS].copy()
            tree_files[TKEYS.PATH] = tree_rows[TKEYS.PATH]

            if(parent_tree_files == None or len(parent_tree_files) == 0):
                parent_tree_files = tree_files
            else:
                tree_files[TKEYS.TAGKBASE] = parent_tree_files[TKEYS.TAGKBASE]

            for row in tree_rows[TKEYS.GROUP_ROWS]:
                try:
                    rowmap = row.get_row_map()
                    rowkey = rowmap[TKEYS.KEY]
                    cur_value_of_key = None
                    if (rowkey in tree_dict_modified):
                        cur_value_of_key = tree_dict_modified[rowkey]
                    elif (rowkey in parent_tree_dict):
                        cur_value_of_key = parent_tree_dict[rowkey]
                    evaluated_value_of_key_after_row_ops = self.apply_row_rules_on_cur_value(rowkey,row,cur_value_of_key)
                    tree_dict_modified[rowkey] = evaluated_value_of_key_after_row_ops
                except Exception as e:
                    raise e

            # if tree is modified, then copy immediate parent's payload to current subtree.
            # then in current tree view, overwrite copied parent values with subtree_override_vals
            if(len(tree_dict_modified) == 0):
                tree_files[TKEYS.FULL_PAYLOAD] = parent_tree_dict    # reference only
                if(len(parent_tree_dict) != 0):
                    version = parent_tree_files[TKEYS.VERSION] if(TKEYS.VERSION in parent_tree_files) else \
                        self.get_version_id(True)
                    tree_files[TKEYS.FILENAME] = parent_tree_files[TKEYS.FILENAME] if parent_tree_files[TKEYS.FILENAME] != None else \
                        '{}-{}{}'.format(
                            tree_files[TKEYS.TAGKBASE],
                            version,
                            self.filename_suffix)
            else:
                tree_files[TKEYS.FULL_PAYLOAD] = {k:v for k,v in parent_tree_dict.items()}
                for k,v in tree_dict_modified.items():
                    tree_files[TKEYS.FULL_PAYLOAD][k] = v            # override only modified keys
                tree_files[TKEYS.IS_MODIFIED] = True
                version = self.get_next_version_id()
                version_filename = self.get_next_version_filename_id()
                tree_files[TKEYS.VERSION] = version
                tree_files[TKEYS.FILENAME] = '{}-{}{}'.format(
                    tree_files[TKEYS.TAGKBASE],
                    version_filename,
                    self.filename_suffix)

                self.write_payload_to_file(tree_files[TKEYS.FILENAME],tree_files[TKEYS.FULL_PAYLOAD])

            # evaluate subtrees
            for tag_value,subtree in tree_rows[TKEYS.GROUP_SUBTREE].items():
                tree_files[TKEYS.GROUP_SUBTREE][tag_value] = self.generate_tree_file_structure()
                subtree_file = tree_files[TKEYS.GROUP_SUBTREE][tag_value]
                self.evaluate_rows_in_subtree(subtree,tree_files,subtree_file,tag_key_order_list)

            tree_files[TKEYS.FULL_PAYLOAD] = {}     # clean up memory
        except Exception as e:
            raise e

        return

    def reduce_tree_info_redundancy(self,tree_files):
        do_not_delete = {}
        do_not_delete_this_subtree = False
        for key,subtree in tree_files[TKEYS.GROUP_SUBTREE].items():
            status = self.reduce_tree_info_redundancy(subtree)
            do_not_delete[key] = status
            if(status == True):
                do_not_delete_this_subtree = True
        keys_to_delete = []
        for key,subtree in tree_files[TKEYS.GROUP_SUBTREE].items():
            if(do_not_delete[key] == True):
                continue
            if(subtree[TKEYS.IS_MODIFIED] == False):
                keys_to_delete.append(key)
            else:
                do_not_delete_this_subtree = True
        for key in keys_to_delete:
            tree_files[TKEYS.GROUP_SUBTREE].pop(key)
        return do_not_delete_this_subtree


    def write_tree_info_to_file(self,tree_files,basename,dir='tmp'):
        def write_tree_files_to_tree_info(tree_files,tree_info):
            tree_info[TKEYS.PATH] = tree_files[TKEYS.PATH]
            tree_info[TKEYS.FILENAME] = tree_files[TKEYS.FILENAME]
            #tree_info[TKEYS.IS_MODIFIED] = tree_files[TKEYS.IS_MODIFIED]
            for tag_val,tree_files_subtree in tree_files[TKEYS.GROUP_SUBTREE].items():
                tree_info[TKEYS.GROUP_SUBTREE][tag_val] = self.generate_tree_info_structure()
                write_tree_files_to_tree_info(tree_files_subtree,tree_info[TKEYS.GROUP_SUBTREE][tag_val])
            return
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename_final = '{}/{}-info{}'.format(dir,basename,self.filename_suffix)
        tree_info = self.generate_tree_info_structure(tree_files[TKEYS.PATH],filename_final,tree_files[TKEYS.VERSION])
        write_tree_files_to_tree_info(tree_files,tree_info)

        with open(filename_final,'w') as fw:
            json_pretty = json.dumps(tree_info,indent=4,sort_keys=True)
            fw.write(json_pretty)
        return tree_info

    def evaluate_rows_in_tree_base(self,tree_rows,tag_key_order_list):
        tree_files = {}

        for basename,subtree in tree_rows.items():
            assert basename == subtree[TKEYS.PATH]
            try:
                tree_files[basename] = self.generate_tree_file_structure(path=basename,tag_key=TKEYS.TAGKBASE,tag_val=basename)
                assert tree_files[basename][TKEYS.TAGKBASE] != None
                self.evaluate_rows_in_subtree(tree_rows[basename],{},tree_files[basename],tag_key_order_list)
                self.reduce_tree_info_redundancy(tree_files[basename])
                tree_info = self.write_tree_info_to_file(tree_files[basename],basename)
            except Exception as e:
                raise e
        return tree_files

    def print_tree_rows(self,tree_rows):
        return

    def print_tree_files(self,tree_files):
        return

    def process_tree_hierarchy_to_files(self,tree_rows,tag_key_order_list):
        tree_files = self.evaluate_rows_in_tree_base(tree_rows,tag_key_order_list)
        return tree_files

    def process_rows_to_files(self,rows,dict_tags,tag_key_order_list):
        tree_rows = self.generate_tree_hierarchy_with_rows(rows,dict_tags,tag_key_order_list)
        tree_files = self.process_tree_hierarchy_to_files(tree_rows,tag_key_order_list)
        return tree_files

    def process_rows_to_files_with_defined_tree(self,rows,tree,tag_key_order_list):
        self.populate_rows_to_tag_tree(rows,tree,tag_key_order_list)
        tree_files = self.process_tree_hierarchy_to_files(tree,tag_key_order_list)
        return tree_files
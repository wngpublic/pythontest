import random
import enum

class my_utils:
    class DISTRIBUTION_ENUM(enum.Enum):                     # just use scipy
        UNIFORM = 1
        BELL_CURVE = 2

    charset_lc          = 'abcdefghijklkmnopqrstuvwxyz'
    charset_uc          = charset_lc.upper()                # reference to class variable
    charset_num         = '0123456789'
    charset_hex         = '0123456789ABCDEF'
    charset_alphanum    = charset_lc + charset_num
    charset_special     = '!@#$%^&*(){}[]|;:<>,.?-_+='
    charset_math        = '%&-+*/'
    common_consonants   = ['b','c','d','f','g','h','j','k','l','m','n','p','r','s','t','w']
    common_vowels       = ['a','e','i','o','u']
    silent_endings      = {
        'a':['s'],
        'b':['e','s'],
        'c':['k','e','s'],
        'd':['e','s'],
        'e':['s'],
        'f':['e','s'],
        'g':['e','h','s'],
        'h':[],
        'i':['s'],
        'j':['e'],
        'k':['c','e'],
        'l':['e','s'],
        'm':['n','e','s'],
        'n':['e','s'],
        'o':['s'],
        'p':['e','s'],
        'r':['e','s'],
        's':['e','s','t'],
        't':['e','s'],
        'u':['s'],
        'w':['e','s']
    }
    ascii_map_hex           = {
        ' ':0x20,
        '!':0x21,
        '"':0x22,
        '#':0x23,
        '$':0x24,
        '%':0x25,
        '&':0x26,
        '\'':0x27,
        '(':0x28,
        ')':0x29,
        '*':0x2A,
        '+':0x2B,
        ',':0x2C,
        '-':0x2D,
        '.':0x2E,
        '/':0x2F,
        ':':0x3A,
        ';':0x3B,
        '<':0x3C,
        '=':0x3D,
        '>':0x3E,
        '?':0x3F,
        '@':0x40,
        '[':0x5B,
        '\\':0x5C,
        ']':0x5D,
        '^':0x5E,
        '_':0x5F,
        '`':0x60,
        '{':0x7B,
        '|':0x7C,
        '}':0x7D,
        '~':0x7E
    }
    ascii_map = {k:'%{:02}'.format(v) for k,v in ascii_map_hex.items()}

    ascii_map_hex_inverted = {v:k for k,v in ascii_map_hex.items()}
    ascii_map_inverted = {'%{:02}'.format(k):v for k,v in ascii_map_hex_inverted.items()}


    def __init__(self):
        pass

    def get(self,x):
        return x

    @staticmethod
    def swap(l:list, i:int, j:int) -> None:
        v = l[i]
        l[i] = l[j]
        l[j] = v

    @staticmethod
    def shuffle(l:list,num_shuffles=3) -> list:
        result = l.copy()
        sz = len(result)
        for cnt in range(num_shuffles):
            for i in range(sz):
                my_utils.swap(result, i, my_utils.rand(0,sz))
        return result

    @staticmethod
    def shuffle_string(s:str,num_shuffles=3)-> str:
        l = list(s)
        r = my_utils.shuffle(l,num_shuffles)
        result = ''.join(r)
        return result

    '''
    - start with either
        - 1 consonant
            - add 1 or 2 vowels
            - repeat 1 consonant or end
        - 1 vowel
            - go to consonant
    '''
    @staticmethod
    def make_random_word(num_syllables=2)-> str:
        s = ''
        consonants = my_utils.common_consonants
        vowels = my_utils.common_vowels
        len_con = len(consonants)
        len_vow = len(vowels)
        last_is_vowel = False
        for i in range(num_syllables):
            if my_utils.rand_bool():
                s += consonants[my_utils.rand(0,len_con)]
                s += vowels[my_utils.rand(0,len_vow)]
                if my_utils.rand_bool():
                    s += vowels[my_utils.rand(0,len_vow)]
                last_is_vowel = True
            else:
                if last_is_vowel:
                    s += consonants[my_utils.rand(0,len_con)]
                s += vowels[my_utils.rand(0,len_vow)]
                s += consonants[my_utils.rand(0,len_con)]
                last_is_vowel = False
            if (i+1) == num_syllables and not last_is_vowel:
                if my_utils.rand_bool():
                    c = consonants[my_utils.rand(0,len_con)]
                    l_silent_endings = my_utils.silent_endings[c]
                    if len(l_silent_endings) != 0:
                        s += l_silent_endings[my_utils.rand(0,len(l_silent_endings))]

        return s

    @staticmethod
    def inject_random_errors_string(s:str,charset:str,num_errors:int) -> str:
        result = ''.join(my_utils.inject_random_errors_list(list(s),charset,num_errors))
        return result

    @staticmethod
    def inject_random_errors_list(l:list,charset:list,num_errors:int) -> list:
        sz = len(l)
        rand_set = set(my_utils.rand_list(0,sz,num_errors,False))
        result = []
        for i in range(sz):
            if i in rand_set:
                c = my_utils.rand_str(1,charset)
                result.append(c)
            result.append(l[i])
        return result

    @staticmethod
    def random_swap(s:str,num_swaps:int) -> str:
        l = list(s)
        result = ''.join(my_utils.random_swap_list(l,num_swaps))
        return result

    '''
    random swap. 
    first, characterize the different characters by making map of char -> list of index
    then randomly choose two unique chars from map and swap random index in each group. 
    there is option to not repeat same index by keeping a set of used indices
    '''
    @staticmethod
    def random_swap_list(l:list,num_swaps:int,allow_reusable_index:bool=True) -> list:
        result = l.copy()
        d = {}
        used_indices = set()
        for i in range(l):
            c = l[i]
            if c not in d:
                d[c] = []
            d[c].append(i)

        list_chars = list(d.keys())
        sz_list_chars = len(list_chars)

        for i in range(num_swaps):
            list_pair_swap = my_utils.rand_list(0,sz_list_chars,2)
            assert len(list_pair_swap) == 2
            # choose index in each of pairs to swap
            list_index_char_0 = d[list_chars[list_pair_swap[0]]]
            list_index_char_1 = d[list_chars[list_pair_swap[1]]]
            idx_char_0 = my_utils.rand(0,len(list_index_char_0))
            idx_char_1 = my_utils.rand(0,len(list_index_char_1))
            my_utils.swap(result,idx_char_0,idx_char_1)
        
        return result


    @staticmethod
    def mutate_string(s:str,charset:str,num_mutations:int) -> str:
        l = list(s)
        result = ''.join(my_utils.mutate_list(l,num_mutations))
        return result

    @staticmethod
    def mutate_list(l:list,charset:list,num_mutations:int) -> list:
        sz = len(l)
        rand_set = set(my_utils.rand_list(0,sz,num_mutations,False))
        result = []
        for i in range(sz):
            if i in rand_set:
                c = my_utils.rand_str(1,charset)
                result.append(c)
            result.append(l[i])
        return result

    '''
    return set_target - set_visited
    '''
    @staticmethod
    def get_non_visited_set(set_target:set, set_visited:set) -> set:
        s = set()
        for v in set_target:
            if v not in set_visited:
                s.add(v)
        return s

    '''
    return set_target - set_visited
    '''
    @staticmethod
    def get_non_visited_list(set_target:set, set_visited:set) -> list:
        s = my_utils.get_non_visited_set(set_target,set_visited)
        l = list(s)

    @staticmethod
    def rand_str(num:int, charset:str=None) -> str:
        if charset is None:
            charset = my_utils.charset_alphanum
        sz = len(charset)
        l_idx = my_utils.rand_list(0,sz,num,True)
        s = []
        for i in l_idx:
            s.append(charset[i])
        result = ''.join(s)
        return result

    @staticmethod
    def rand_bool()->bool:
        return random.getrandbits(1)                # bool(val) also works

    @staticmethod
    def rand_int(min:int,max:int)->int:             # randint is [min,max], randrange is [min,max)
        return my_utils.rand(min,max)

    @staticmethod
    def rand(min:int,max:int) -> int:
        return random.randrange(min,max)            # randint is [min,max], randrange is [min,max)

    '''
    s can be string, list, set, tuple, etc
    '''
    @staticmethod
    def rand_sample_over_sequence(s,k) -> list:
        l = random.sample(s, k)
        return l

    '''
    get rand values from [min,max)
    '''
    @staticmethod
    def rand_list(min:int,max:int,num:int,allow_repetition=False) -> list:
        def rand_list_1(min:int,max:int,num:int,allow_repetition=False) -> list:
            sz = max - min
            if not allow_repetition:
                assert num <= sz
            l = []
            s = set()
            max_loop = 100
            for i in range(num):
                if allow_repetition:
                    l.append(random.randrange(min,max))
                else:
                    for j in range(max_loop):
                        v = random.randint(min,max)     # randint is [min,max], randrange is [min,max)
                        if v not in s:
                            s.add(v)
                            break
                        else:
                            if (j + 1) == max_loop:
                                assert False
            if not allow_repetition:
                assert len(s) == num
                l = list(s)
            return l
        def rand_list_sample_range(min:int,max:int,num:int,allow_repetition=False) -> list:
            l = random.sample(range(min,max), num)
            return l
        def rand_list_loop(min:int,max:int,num:int,allow_repetition=False) -> list:
            l = [random.randrange(min,max) for i in range(num)]     # generate list of random int
            return l
        def rand_list_2(min:int,max:int,num:int,allow_repetition=False) -> list:
            if not allow_repetition:
                return rand_list_1(min,max,num,allow_repetition)
            #l = rand_list_sample_range(min,max,num,allow_repetition)
            l = rand_list_loop(min,max,num,allow_repetition)
            return l
        return rand_list_2(min,max,num,allow_repetition)

    @staticmethod
    def get_ascii_encoding(l:list, set_exclude:set) -> list:
        result = []
        for c in l:
            if c in set_exclude or c not in my_utils.ascii_map:
                result.append(c)
            else:
                result.append('%{:02}'.format(my_utils.ascii_map[c]))
        return result

    @staticmethod
    def get_ascii_decoding(l:list) -> list:
        result = []
        for c in l:
            # if c is like %\d{2} then it might be in map
            if c in my_utils.ascii_map:
                pass
            else:
                pass
        return result

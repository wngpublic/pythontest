#!/usr/local/bin/python3

def p(s):
    print(s)

class algos_geometry:
    def __init__(self):
        pass

    '''
    SEPARATOR------------------------------------------------------------------
    '''
    class matrix:
        def __init__(self):
            self.rows = []
        def add_row(self, row):
            if len(self.rows) != 0:
                assert len(self.rows[0]) == len(row)
            self.rows.append(row)
        def size(self):
            return len(self.rows),len(self.rows[0])
        def print(self):
            [p(row) for row in self.rows]

    def test_matrix(self):
        def test1():
            matrix = algos_geometry.matrix()
            matrix.add_row([1,2,3])
            matrix.add_row([4,5,6])
            matrix.add_row([7,8,9])
            matrix.add_row([10,11,12])
            numrows,numcols=matrix.size()
            assert numrows == 4 and numcols == 3
        def test2():
            matrix = algos_geometry.matrix()
            matrix.add_row([1,2,3])
            flag = False
            try:
                matrix.add_row([4,5,6,7])
            except Exception as e:
                flag = True
            assert flag
        def inner_main():
            test1()
            test2()

        inner_main()

    '''
    SEPARATOR------------------------------------------------------------------
    '''
    class tree_node:
        _static_tree_node_id_ctr = 0

        @staticmethod
        def inc_static_ctr():
            algos_geometry.tree_node._static_tree_node_id_ctr += 1

        def __init__(self, **kwargs):
            self._l = kwargs.get('l',None)
            self._r = kwargs.get('r',None)
            self._v = kwargs.get('v',None)
            self._iv = kwargs.get('id',None)
            if self._iv is None:
                self._id = algos_geometry.tree_node._static_tree_node_id_ctr
                algos_geometry.tree_node.inc_static_ctr()

        def l(self, l=None):
            if l is not None:
                self._l = l
            return self._l

        def r(self, r=None):
            if r is not None:
                self._r = r
            return self._r

        def v(self, v=None):
            if v is not None:
                self._v = v
            return self._v

        def id(self, id=None):
            if id is not None:
                self._id = id
            return self._id

        def p(self):
            p('id:{};v:{}'.format(self._id, self._v))

    class binary_tree:
        def __init__(self):
            self.root = None
        def l(self, n):
            pass

    def test_binary_tree(self):
        def test_binary_node():
            n1 = algos_geometry.tree_node()
            n1.v(1)
            n2 = algos_geometry.tree_node(v=42)
            n3 = algos_geometry.tree_node(v=84)
            n4 = algos_geometry.tree_node(v=10,l=n2,r=n3)
            n1.l(n4)
            assert n1 is not None and n1.v() == 1
            assert n1.l() is not None and n1.l() == n4
            assert n4.v() == 10
            assert n4.r() is not None and n4.r() == n3 and n4.r().v() == 84
            assert n4.l() is not None and n4.l() == n2 and n4.l().v() == 42
            assert n1.id() == 0 and n2.id() == 1 and n3.id() == 2 and n4.id() == 3

        test_binary_node()

    '''
    SEPARATOR------------------------------------------------------------------
    '''
    class rubic:
        '''
                        4 4 4
                        4 4 4
                        4 4 4

                0 0 0   1 1 1   2 2 2   3 3 3
                0 0 0   1 1 1   2 2 2   3 3 3
                0 0 0   1 1 1   2 2 2   3 3 3

                        5 5 5
                        5 5 5
                        5 5 5

        all actions taken from side 0 and side 1.
        '''

        class Side:
            def __init__(self, v):
                self.matrix = [[v] * 3 for i in range(3)]

            def get(self):
                return self.matrix

            def is_match(self):
                m = self.matrix
                for i in range(len(m)):
                    for j in range(len(m[i])):
                        if m[i][j] != m[0][0]:
                            return False
                return True

        def __init__(self):
            self._sides = [algos_geometry.rubic.Side(i) for i in range(6)]

        def p(self):
            pass

    def test_rubic(self):
        def test_side():
            v = 2
            side = algos_geometry.rubic.Side(v)
            m = side.get()
            assert len(m) == 3
            assert len(m[0]) == 3
            for i in range(len(m)):
                for j in range(len(m[i])):
                    assert m[i][j] == v

        def test_inner_main():
            test_side()
        test_inner_main()

    '''
    SEPARATOR------------------------------------------------------------------
    '''

    '''
    SEPARATOR------------------------------------------------------------------
    '''

    '''
    SEPARATOR------------------------------------------------------------------
    '''

    '''
    SEPARATOR------------------------------------------------------------------
    '''

    '''
    SEPARATOR------------------------------------------------------------------
    '''

    '''
    SEPARATOR------------------------------------------------------------------
    '''
    def test(self):
        pass

class algos:
    def __init__(self):
        pass

    def test(self):
        '''
        algos_geometry().test_matrix()
        algos_geometry().test_binary_tree()
        '''
        algos_geometry().test_rubic()
        p('test algos done')

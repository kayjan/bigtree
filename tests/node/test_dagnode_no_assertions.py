import unittest
from unittest.mock import patch

import pytest

from bigtree.node import basenode, dagnode, node


@patch("bigtree.node.dagnode.ASSERTIONS", "")
class TestDAGNodeNoAssertions(unittest.TestCase):
    def setUp(self):
        """
        Tree should have structure
        a >> b
        b >> c
        b >> d
        c >> e
        c >> f
        e >> f
        f >> g
        d >> e
        """
        self.a = dagnode.DAGNode(name="a", age=90)
        self.b = dagnode.DAGNode(name="b", age=65)
        self.c = dagnode.DAGNode(name="c", age=60)
        self.d = dagnode.DAGNode(name="d", age=40)
        self.e = dagnode.DAGNode(name="e", age=35)
        self.f = dagnode.DAGNode(name="f", age=38)
        self.g = dagnode.DAGNode(name="g", age=10)
        self.h = dagnode.DAGNode(name="h", age=6)

        self.nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g]

    def tearDown(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None

    def test_set_parents_none_parent_error(self):
        # TypeError: 'NoneType' object is not iterable
        self.c.parents = [self.a]
        parents = None
        with pytest.raises(TypeError):
            self.c.parents = parents

    def test_set_children_none_children_error(self):
        # TypeError: 'NoneType' object is not iterable
        children = None
        with pytest.raises(TypeError):
            self.g.children = children

    def test_set_parents_type_error(self):
        # TypeError: 'int' object is not iterable
        parents = 1
        with pytest.raises(TypeError):
            self.a.parents = parents

        # AttributeError: 'int' object has no attribute '_DAGNode__children'
        parent = 1
        with pytest.raises(AttributeError):
            self.a.parents = [parent]

        # AttributeError: 'BaseNode' object has no attribute '_DAGNode__parents'
        parent = basenode.BaseNode()
        with pytest.raises(AttributeError):
            self.a.parents = [parent]

        # AttributeError: 'Node' object has no attribute '_DAGNode__parents'
        parent = node.Node("a")
        with pytest.raises(AttributeError):
            self.a.parents = [parent]

    def test_set_parents_loop_error(self):
        # No error without assertion
        self.a.parents = [self.a]

        # No error without assertion
        self.b.parents = [self.a]
        self.c.parents = [self.b]
        self.a.parents = [self.c]

    def test_set_duplicate_parent_error(self):
        # No error without assertion
        self.a.parents = [self.b, self.b]

    def test_set_children_type_error(self):
        # TypeError: 'int' object is not iterable
        children = 1
        with pytest.raises(TypeError):
            self.a.children = children

        # AttributeError: 'int' object has no attribute '_DAGNode__parents'
        children = 1
        with pytest.raises(AttributeError):
            self.a.children = [self.b, children]

        # AttributeError: 'BaseNode' object has no attribute '_DAGNode__parents'
        children = basenode.BaseNode()
        with pytest.raises(AttributeError):
            self.a.children = [children]

        # AttributeError: 'Node' object has no attribute '_DAGNode__parents'
        children = node.Node("a")
        with pytest.raises(AttributeError):
            self.a.children = [children]

    def test_set_children_loop_error(self):
        # No error without assertion
        self.a.children = [self.b, self.a]

        # No error without assertion
        self.a.children = [self.b, self.c]
        self.c.children = [self.d, self.e, self.f]
        self.f.children = [self.a]

    def test_set_duplicate_children_error(self):
        # No error without assertion
        self.a.children = [self.b, self.b]

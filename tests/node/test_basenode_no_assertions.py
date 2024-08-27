import unittest
from unittest.mock import patch

import pytest

from bigtree.node import basenode


@patch("bigtree.node.basenode.ASSERTIONS", "")
class TestBaseNodeNoAssertions(unittest.TestCase):
    def setUp(self):
        """
        Tree should have structure
        a (age=90)
        |-- b (age=65)
        |   |-- d (age=40)
        |   +-- e (age=35)
        |       |-- g (age=10)
        |       +-- h (age=6)
        +-- c (age=60)
            +-- f (age=38)
        """
        self.a = basenode.BaseNode(name="a", age=90)
        self.b = basenode.BaseNode(name="b", age=65)
        self.c = basenode.BaseNode(name="c", age=60)
        self.d = basenode.BaseNode(name="d", age=40)
        self.e = basenode.BaseNode(name="e", age=35)
        self.f = basenode.BaseNode(name="f", age=38)
        self.g = basenode.BaseNode(name="g", age=10)
        self.h = basenode.BaseNode(name="h", age=6)

    def tearDown(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None

    def test_set_children_none_parent_error(self):
        # TypeError: 'NoneType' object is not iterable
        children = None
        with pytest.raises(TypeError):
            self.h.children = children

    def test_set_parent_type_error(self):
        # AttributeError: 'int' object has no attribute '_BaseNode__children'
        parent = 1
        with pytest.raises(AttributeError):
            self.a.parent = parent

    def test_set_parent_loop_error(self):
        # No error without assertion
        self.a.parent = self.a

        # No error without assertion
        self.b.parent = self.a
        self.c.parent = self.b
        self.a.parent = self.c

    def test_set_children_type_error(self):
        # AttributeError: 'int' object has no attribute '_BaseNode__children'
        children = 1
        with pytest.raises(AttributeError):
            self.a.children = [self.b, children]

        # AttributeError: 'NoneType' object has no attribute 'parent'
        children = None
        with pytest.raises(AttributeError):
            self.a.children = [self.b, children]

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

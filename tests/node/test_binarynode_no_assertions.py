import unittest
from unittest.mock import patch

import pytest

from bigtree.node.basenode import BaseNode
from bigtree.node.binarynode import BinaryNode
from bigtree.node.node import Node
from bigtree.utils.exceptions import TreeError


@patch("bigtree.node.binarynode.ASSERTIONS", "")
class TestBinaryNodeNoAssertions(unittest.TestCase):
    def setUp(self):
        self.a = BinaryNode(1)
        self.b = BinaryNode(2)
        self.c = BinaryNode(3)
        self.d = BinaryNode(4)
        self.e = BinaryNode(5)
        self.f = BinaryNode(6)
        self.g = BinaryNode(7)
        self.h = BinaryNode(8)

    def tearDown(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None

    def test_set_parent_type_error(self):
        # AttributeError: 'int' object has no attribute '_BinaryNode__children'
        parent = 1
        with pytest.raises(AttributeError):
            self.a.parent = parent

        # AttributeError: 'BaseNode' object has no attribute '_BinaryNode__children'
        parent = BaseNode()
        with pytest.raises(AttributeError):
            self.a.parent = parent

        # AttributeError: 'Node' object has no attribute '_BinaryNode__children'
        parent = Node("a")
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
        # AttributeError: 'int' object has no attribute 'parent'
        children = 1
        with pytest.raises(AttributeError):
            self.a.children = [self.b, children]

        # No error without assertion
        children = BaseNode()
        self.a.children = [children, None]

        # bigtree.utils.exceptions.TreeError: 'NoneType' object has no attribute '_BinaryNode__children'
        children = Node("a")
        with pytest.raises(TreeError):
            self.a.children = [children, None]

    def test_set_children_loop_error(self):
        # No error without assertion
        self.a.children = [self.b, self.a]

        # No error without assertion
        self.a.children = [self.b, self.c]
        self.c.children = [self.d, self.e]
        self.e.children = [self.a, self.f]

    def test_set_duplicate_children_error(self):
        # No error without assertion
        self.a.children = [self.b, self.b]

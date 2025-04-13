import unittest
from itertools import combinations

import pytest

from bigtree.node import node
from bigtree.tree import parsing
from bigtree.utils import exceptions, iterators
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
    assert_tree_structure_basenode_self,
)
from tests.node.test_node import (
    assert_tree_structure_node_root,
    assert_tree_structure_node_self,
)
from tests.test_constants import Constants


class TestParsing(unittest.TestCase):
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
        self.a = node.Node("a", age=90)
        self.b = node.Node("b", age=65)
        self.c = node.Node("c", age=60)
        self.d = node.Node("d", age=40)
        self.e = node.Node("e", age=35)
        self.f = node.Node("f", age=38)
        self.g = node.Node("g", age=10)
        self.h = node.Node("h", age=6)

        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

    def tearDown(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None

    def test_get_path(self):
        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_root(self.a)
        assert_tree_structure_node_self(self)

        expected_paths = [
            ["a", "b"],
            ["a", "b", "d"],
            ["a", "b", "e"],
            ["a", "b", "e", "g"],
            ["a", "b", "e", "h"],
            ["a", "c"],
            ["a", "c", "f"],
            ["b", "d"],
            ["b", "e"],
            ["b", "e", "g"],
            ["b", "e", "h"],
            ["b", "a", "c"],
            ["b", "a", "c", "f"],
            ["d", "b", "e"],
            ["d", "b", "e", "g"],
            ["d", "b", "e", "h"],
            ["d", "b", "a", "c"],
            ["d", "b", "a", "c", "f"],
            ["e", "g"],
            ["e", "h"],
            ["e", "b", "a", "c"],
            ["e", "b", "a", "c", "f"],
            ["g", "e", "h"],
            ["g", "e", "b", "a", "c"],
            ["g", "e", "b", "a", "c", "f"],
            ["h", "e", "b", "a", "c"],
            ["h", "e", "b", "a", "c", "f"],
            ["c", "f"],
        ]
        for node_pair, expected_path in zip(
            combinations(list(iterators.preorder_iter(self.a)), 2), expected_paths
        ):
            actual_path = [
                _node.node_name
                for _node in parsing.get_path(node_pair[0], (node_pair[1]))
            ]
            assert (
                actual_path == expected_path
            ), f"Wrong path for {node_pair}, expected {expected_path}, received {actual_path}"

    def test_get_path_same_node(self):
        for _node in iterators.preorder_iter(self.a):
            actual_path = [
                _node1.node_name for _node1 in parsing.get_path(_node, _node)
            ]
            expected_path = [_node.node_name]
            assert (
                actual_path == expected_path
            ), f"Wrong path for {_node}, expected {expected_path}, received {actual_path}"

    def test_get_path_type_error(self):
        source = node.Node("a")
        destination = 2
        with pytest.raises(TypeError) as exc_info:
            parsing.get_path(source, destination)
        assert str(exc_info.value) == Constants.ERROR_NODE_GOTO_TYPE.format(
            type="BaseNode", input_type=type(destination)
        )

    def test_get_path_different_tree_error(self):
        source = node.Node("a")
        destination = self.a
        with pytest.raises(exceptions.TreeError) as exc_info:
            parsing.get_path(source, destination)
        assert str(exc_info.value) == Constants.ERROR_NODE_GOTO_SAME_TREE.format(
            a=source, b=destination
        )

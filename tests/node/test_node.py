import unittest

import pytest

from bigtree.node.node import Node
from bigtree.utils.exceptions import LoopError, TreeError
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root_attr,
    assert_tree_structure_basenode_root_generic,
    assert_tree_structure_basenode_self,
)


class TestNode(unittest.TestCase):
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
        self.a = Node("a", age=90)
        self.b = Node("b", age=65)
        self.c = Node("c", age=60)
        self.d = Node("d", age=40)
        self.e = Node("e", age=35)
        self.f = Node("f", age=38)
        self.g = Node("g", age=10)
        self.h = Node("h", age=6)

    def tearDown(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None

    def test_empty_node_name(self):
        with pytest.raises(TreeError):
            Node()

    def test_set_parent(self):
        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.f.parent = self.c
        self.g.parent = self.e
        self.h.parent = self.e

        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_root_generic(self.a)
        assert_tree_structure_node_self(self)

    def test_set_parent_constructor(self):
        self.a = Node(name="a", age=90)
        self.b = Node(name="b", age=65, parent=self.a)
        self.c = Node(name="c", age=60, parent=self.a)
        self.d = Node(name="d", age=40, parent=self.b)
        self.e = Node(name="e", age=35, parent=self.b)
        self.f = Node(name="f", age=38, parent=self.c)
        self.g = Node(name="g", age=10, parent=self.e)
        self.h = Node(name="h", age=6, parent=self.e)

        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_root_generic(self.a)
        assert_tree_structure_node_self(self)

    def test_set_parent_duplicate(self):
        # Set parent again
        self.b.parent = self.a
        self.b.parent = self.a

    def test_set_parent_duplicate_constructor(self):
        # Set parent again
        self.a = Node(name="a", age=90)
        self.b = Node(name="b", age=65, parent=self.a)
        self.b.parent = self.a

    def test_set_parent_sep_root(self):
        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.f.parent = self.c
        self.g.parent = self.e
        self.h.parent = self.e
        self.a.sep = "\\"

        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_self_sep(self)

    def test_set_parent_sep_child(self):
        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.f.parent = self.c
        self.g.parent = self.e
        self.h.parent = self.e
        self.h.sep = "\\"

        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_self_sep(self)

    def test_set_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_root_generic(self.a)
        assert_tree_structure_node_self(self)

    def test_set_children_constructor(self):
        self.h = Node(name="h", age=6)
        self.g = Node(name="g", age=10)
        self.f = Node(name="f", age=38)
        self.e = Node(name="e", age=35, children=[self.g, self.h])
        self.d = Node(name="d", age=40)
        self.c = Node(name="c", age=60, children=[self.f])
        self.b = Node(name="b", age=65, children=[self.d, self.e])
        self.a = Node(name="a", age=90, children=[self.b, self.c])

        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_root_generic(self.a)
        assert_tree_structure_node_self(self)

    def test_set_children_duplicate(self):
        # Set child again
        self.a.children = [self.b]
        self.a.children = [self.b]

    def test_set_children_duplicate_constructor(self):
        # Set child again
        self.a = Node("a", children=[self.b])
        self.a.children = [self.b]

    def test_error_set_parent_same_path(self):
        self.a = Node("a")
        self.b = Node("b", parent=self.a)
        self.c = Node("b")
        with pytest.raises(TreeError):
            self.c.parent = self.a

    def test_error_set_parent_constructor_same_path(self):
        self.a = Node("a")
        self.b = Node("b", parent=self.a)
        with pytest.raises(TreeError):
            self.c = Node("b", parent=self.a)

    def test_error_set_children_same_path(self):
        self.a = Node("a")
        self.b = Node("b")
        self.c = Node("b")
        with pytest.raises(TreeError):
            self.a.children = [self.b, self.c]

    def test_error_set_children_constructor_same_path(self):
        self.c = Node("b")
        self.b = Node("b")
        with pytest.raises(TreeError):
            self.a = Node("a", children=[self.b, self.c])

    def test_error_set_children_multiple_same_path(self):
        self.a = Node("a")
        self.b = Node("b")
        self.c = Node("b")
        self.d = Node("c")
        self.e = Node("c")
        with pytest.raises(TreeError) as exc_info:
            self.a.children = [self.b, self.c, self.d, self.e]
        assert (
            str(exc_info.value)
            == "Error: Duplicate node with same path\nAttempting to add nodes same path /a/b and /a/c"
        )

    def test_error_set_parent(self):
        # Error: wrong type
        with pytest.raises(TypeError):
            self.a.parent = 1

        # Error: set self as parent
        with pytest.raises(LoopError):
            self.a.parent = self.a

        # Error: set descendant as parent
        with pytest.raises(LoopError):
            self.b.parent = self.a
            self.c.parent = self.b
            self.a.parent = self.c

    def test_error_set_children(self):
        # Error: wrong type
        with pytest.raises(TypeError):
            self.a.children = [self.b, 1]

        # Error: set self as child
        with pytest.raises(LoopError):
            self.a.children = [self.b, self.a]

        # Error: set ancestor as child
        with pytest.raises(LoopError):
            self.a.children = [self.b, self.c]
            self.c.children = [self.d, self.e, self.f]
            self.f.children = [self.a]

        # Error: duplicate child
        with pytest.raises(TreeError):
            self.a.children = [self.b, self.b]


def assert_tree_structure_node_root_generic(root):
    # Test path_name
    expected = "/a"
    actual = root.path_name
    assert actual == expected, f"Node should have path {expected}, but path is {actual}"


def assert_tree_structure_node_self(self):
    nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

    # Test path_name
    expected_ans = [
        "/a",
        "/a/b",
        "/a/c",
        "/a/b/d",
        "/a/b/e",
        "/a/c/f",
        "/a/b/e/g",
        "/a/b/e/h",
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = node.path_name
        assert (
            actual == expected
        ), f"Node should have path {expected}, but path is {actual}"


def assert_tree_structure_node_root_sep(root):
    # Test path_name
    expected = "\\a"
    actual = root.path_name
    assert actual == expected, f"Node should have path {expected}, but path is {actual}"


def assert_tree_structure_node_self_sep(self):
    nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

    # Test path_name
    expected_ans = [
        "\\a",
        "\\a\\b",
        "\\a\\c",
        "\\a\\b\\d",
        "\\a\\b\\e",
        "\\a\\c\\f",
        "\\a\\b\\e\\g",
        "\\a\\b\\e\\h",
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = node.path_name
        assert (
            actual == expected
        ), f"Node should have path {expected}, but path is {actual}"

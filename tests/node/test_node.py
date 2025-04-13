import unittest

import pytest

from bigtree.node import node
from bigtree.utils import exceptions, iterators
from tests.conftest import assert_print_statement
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
    assert_tree_structure_basenode_self,
)
from tests.test_constants import Constants


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
        self.a = node.Node("a", age=90)
        self.b = node.Node("b", age=65)
        self.c = node.Node("c", age=60)
        self.d = node.Node("d", age=40)
        self.e = node.Node("e", age=35)
        self.f = node.Node("f", age=38)
        self.g = node.Node("g", age=10)
        self.h = node.Node("h", age=6)

    def tearDown(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None

    def test_empty_node_name_error(self):
        with pytest.raises(exceptions.TreeError) as exc_info:
            node.Node("")
        assert str(exc_info.value) == Constants.ERROR_NODE_NAME

    def test_set_parent(self):
        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.f.parent = self.c
        self.g.parent = self.e
        self.h.parent = self.e

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_root(self.a)
        assert_tree_structure_node_self(self)

    def test_set_parent_constructor(self):
        self.a = node.Node(name="a", age=90)
        self.b = node.Node(name="b", age=65, parent=self.a)
        self.c = node.Node(name="c", age=60, parent=self.a)
        self.d = node.Node(name="d", age=40, parent=self.b)
        self.e = node.Node(name="e", age=35, parent=self.b)
        self.f = node.Node(name="f", age=38, parent=self.c)
        self.g = node.Node(name="g", age=10, parent=self.e)
        self.h = node.Node(name="h", age=6, parent=self.e)

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_root(self.a)
        assert_tree_structure_node_self(self)

    def test_set_parent_duplicate(self):
        # Set parent again
        self.b.parent = self.a
        self.b.parent = self.a
        assert list(self.a.children) == [self.b]
        assert self.b.parent == self.a

    def test_set_parent_duplicate_constructor(self):
        # Set parent again
        self.a = node.Node(name="a", age=90)
        self.b = node.Node(name="b", age=65, parent=self.a)
        self.b.parent = self.a
        assert list(self.a.children) == [self.b]
        assert self.b.parent == self.a

    def test_set_parent_sep_different_error(self):
        b = node.Node("b", sep="\\")
        self.b.parent = self.a
        path = "/a/b"
        with pytest.raises(exceptions.TreeError) as exc_info:
            b.parent = self.a
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_PARENT_PATH.format(
            path=path
        )

    def test_set_parent_sep_root(self):
        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.f.parent = self.c
        self.g.parent = self.e
        self.h.parent = self.e
        self.a.sep = "\\"

        assert_tree_structure_basenode_root(self.a)
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

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_self_sep(self)

    def test_set_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_root(self.a)
        assert_tree_structure_node_self(self)

    def test_set_children_constructor(self):
        self.h = node.Node(name="h", age=6)
        self.g = node.Node(name="g", age=10)
        self.f = node.Node(name="f", age=38)
        self.e = node.Node(name="e", age=35, children=[self.g, self.h])
        self.d = node.Node(name="d", age=40)
        self.c = node.Node(name="c", age=60, children=[self.f])
        self.b = node.Node(name="b", age=65, children=[self.d, self.e])
        self.a = node.Node(name="a", age=90, children=[self.b, self.c])

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_root(self.a)
        assert_tree_structure_node_self(self)

    def test_set_children_duplicate(self):
        self.a.children = [self.b]
        self.a.children = [self.b]

    def test_set_children_duplicate_constructor(self):
        self.a = node.Node("a", children=[self.b])
        self.a.children = [self.b]

    def test_set_children_sep_different_error(self):
        b = node.Node("b", sep="\\")
        path = "/a/b"
        with pytest.raises(exceptions.TreeError) as exc_info:
            self.a.children = [self.b, b]
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_CHILDREN_PATH.format(
            path=path
        )

    def test_set_parent_same_path_error(self):
        self.a = node.Node("a")
        self.b = node.Node("b", parent=self.a)
        self.c = node.Node("b")
        path = "/a/b"
        with pytest.raises(exceptions.TreeError) as exc_info:
            self.c.parent = self.a
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_PARENT_PATH.format(
            path=path
        )

    def test_set_parent_constructor_same_path_error(self):
        self.a = node.Node("a")
        self.b = node.Node("b", parent=self.a)
        path = "/a/b"
        with pytest.raises(exceptions.TreeError) as exc_info:
            self.c = node.Node("b", parent=self.a)
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_PARENT_PATH.format(
            path=path
        )

    def test_set_children_same_path_error(self):
        self.a = node.Node("a")
        self.b = node.Node("b")
        self.c = node.Node("b")
        path = "/a/b"
        with pytest.raises(exceptions.TreeError) as exc_info:
            self.a.children = [self.b, self.c]
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_CHILDREN_PATH.format(
            path=path
        )

    def test_set_children_constructor_same_path_error(self):
        self.c = node.Node("b")
        self.b = node.Node("b")
        path = "/a/b"
        with pytest.raises(exceptions.TreeError) as exc_info:
            self.a = node.Node("a", children=[self.b, self.c])
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_CHILDREN_PATH.format(
            path=path
        )

    def test_set_children_multiple_same_path_error(self):
        self.a = node.Node("a")
        self.b = node.Node("b")
        self.c = node.Node("b")
        self.d = node.Node("c")
        self.e = node.Node("c")
        path = "/a/b and /a/c"
        with pytest.raises(exceptions.TreeError) as exc_info:
            self.a.children = [self.b, self.c, self.d, self.e]
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_CHILDREN_PATH.format(
            path=path
        )

    def test_set_parent_error(self):
        parent = 1
        with pytest.raises(TypeError) as exc_info:
            self.a.parent = parent
        assert str(exc_info.value) == Constants.ERROR_NODE_PARENT_TYPE_NONE.format(
            type="BaseNode", input_type=type(parent)
        )

        with pytest.raises(exceptions.LoopError) as exc_info:
            self.a.parent = self.a
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_PARENT

        with pytest.raises(exceptions.LoopError) as exc_info:
            self.b.parent = self.a
            self.c.parent = self.b
            self.a.parent = self.c
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_ANCESTOR

    def test_set_children_error(self):
        children = 1
        with pytest.raises(TypeError) as exc_info:
            self.a.children = [self.b, children]
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE.format(
            type="BaseNode", input_type=type(children)
        )

        with pytest.raises(exceptions.LoopError) as exc_info:
            self.a.children = [self.b, self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_CHILD

        with pytest.raises(exceptions.LoopError) as exc_info:
            self.a.children = [self.b, self.c]
            self.c.children = [self.d, self.e, self.f]
            self.f.children = [self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_DESCENDANT

        with pytest.raises(exceptions.TreeError) as exc_info:
            self.a.children = [self.b, self.b]
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_CHILD

    def test_path_name_int(self):
        b = node.Node(1, parent=self.a)
        assert b.path_name == "/a/1"


def assert_tree_structure_node_root(
    root,
    a="/a",
    b="/a/b",
    c="/a/c",
    d="/a/b/d",
    e="/a/b/e",
    f="/a/c/f",
    g="/a/b/e/g",
    h="/a/b/e/h",
):
    # Test path_name
    expected_attrs = [a, b, d, e, g, h, c, f]
    for _node, expected in zip(iterators.preorder_iter(root), expected_attrs):
        actual = _node.get_attr("path_name")
        assert actual == expected, f"Node path should be {expected}, but it is {actual}"


def assert_tree_structure_node_self(self):
    nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

    # Test accessing with square bracket (__getitem__)
    assert (
        self.a["b"] == self.b
    ), f"Accessor method not returning correct for node {self.a} for {self.b}"
    assert (
        self.a["c"] == self.c
    ), f"Accessor method not returning correct for node {self.a} for {self.c}"
    assert (
        self.a["b"]["d"] == self.d
    ), f"Accessor method not returning correct for node {self.a} for {self.d}"

    # Test deletion of children with square bracket (__delitem__)
    assert len(self.a.children) == 2, f"Before deletion: error in {self.a.children}"
    del self.a["c"]
    assert len(self.a.children) == 1, f"After deletion: error in {self.a.children}"
    self.c.parent = self.a
    assert (
        len(self.a.children) == 2
    ), f"Revert after deletion: error in {self.a.children}"

    # Test deletion of non-existent children with square bracket (__delitem__)
    assert len(self.a.children) == 2, f"Before deletion: error in {self.a.children}"
    del self.a["d"]
    assert len(self.a.children) == 2, f"After deletion: error in {self.a.children}"

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
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.path_name
        assert (
            actual == expected
        ), f"Node should have path {expected}, but path is {actual}"

    # Test show()
    expected_str = (
        "a\n"
        "├── b\n"
        "│   ├── d\n"
        "│   └── e\n"
        "│       ├── g\n"
        "│       └── h\n"
        "└── c\n"
        "    └── f\n"
    )
    assert_print_statement(
        self.a.show,
        expected_str,
    )

    expected_str = (
        "a\n"
        "|-- b\n"
        "|   |-- d\n"
        "|   `-- e\n"
        "|       |-- g\n"
        "|       `-- h\n"
        "`-- c\n"
        "    `-- f\n"
    )
    assert_print_statement(
        self.a.show,
        expected_str,
        style="ansi",
    )

    # Test hshow()
    expected_str = (
        "           ┌─ d\n"
        "     ┌─ b ─┤     ┌─ g\n"
        "─ a ─┤     └─ e ─┤\n"
        "     │           └─ h\n"
        "     └─ c ─── f\n"
    )
    assert_print_statement(
        self.a.hshow,
        expected_str,
    )

    # Test vshow()
    expected_str = (
        "             ┌───┐        \n"
        "             │ a │        \n"
        "             └─┬─┘        \n"
        "       ┌───────┴───────┐  \n"
        "     ┌─┴─┐           ┌─┴─┐\n"
        "     │ b │           │ c │\n"
        "     └─┬─┘           └─┬─┘\n"
        "  ┌────┴────┐          │  \n"
        "┌─┴─┐     ┌─┴─┐      ┌─┴─┐\n"
        "│ d │     │ e │      │ f │\n"
        "└───┘     └─┬─┘      └───┘\n"
        "         ┌──┴───┐         \n"
        "       ┌─┴─┐  ┌─┴─┐       \n"
        "       │ g │  │ h │       \n"
        "       └───┘  └───┘       \n"
    )
    assert_print_statement(
        self.a.vshow,
        expected_str,
    )


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
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.path_name
        assert (
            actual == expected
        ), f"Node should have path {expected}, but path is {actual}"

import unittest
from itertools import combinations

import pytest

from bigtree.node.node import Node
from bigtree.utils.exceptions import LoopError, TreeError
from bigtree.utils.iterators import preorder_iter
from tests.conftest import assert_print_statement
from tests.constants import Constants
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
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

    def test_empty_node_name_error(self):
        with pytest.raises(TreeError) as exc_info:
            Node()
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
        self.a = Node(name="a", age=90)
        self.b = Node(name="b", age=65, parent=self.a)
        self.c = Node(name="c", age=60, parent=self.a)
        self.d = Node(name="d", age=40, parent=self.b)
        self.e = Node(name="e", age=35, parent=self.b)
        self.f = Node(name="f", age=38, parent=self.c)
        self.g = Node(name="g", age=10, parent=self.e)
        self.h = Node(name="h", age=6, parent=self.e)

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
        self.a = Node(name="a", age=90)
        self.b = Node(name="b", age=65, parent=self.a)
        self.b.parent = self.a
        assert list(self.a.children) == [self.b]
        assert self.b.parent == self.a

    def test_set_parent_sep_different_error(self):
        b = Node("b", sep="\\")
        self.b.parent = self.a
        path = "/a/b"
        with pytest.raises(TreeError) as exc_info:
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
        self.h = Node(name="h", age=6)
        self.g = Node(name="g", age=10)
        self.f = Node(name="f", age=38)
        self.e = Node(name="e", age=35, children=[self.g, self.h])
        self.d = Node(name="d", age=40)
        self.c = Node(name="c", age=60, children=[self.f])
        self.b = Node(name="b", age=65, children=[self.d, self.e])
        self.a = Node(name="a", age=90, children=[self.b, self.c])

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)
        assert_tree_structure_node_root(self.a)
        assert_tree_structure_node_self(self)

    def test_set_children_duplicate(self):
        self.a.children = [self.b]
        self.a.children = [self.b]

    def test_set_children_duplicate_constructor(self):
        self.a = Node("a", children=[self.b])
        self.a.children = [self.b]

    def test_set_children_sep_different_error(self):
        b = Node("b", sep="\\")
        path = "/a/b"
        with pytest.raises(TreeError) as exc_info:
            self.a.children = [self.b, b]
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_CHILDREN_PATH.format(
            path=path
        )

    def test_set_parent_same_path_error(self):
        self.a = Node("a")
        self.b = Node("b", parent=self.a)
        self.c = Node("b")
        path = "/a/b"
        with pytest.raises(TreeError) as exc_info:
            self.c.parent = self.a
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_PARENT_PATH.format(
            path=path
        )

    def test_set_parent_constructor_same_path_error(self):
        self.a = Node("a")
        self.b = Node("b", parent=self.a)
        path = "/a/b"
        with pytest.raises(TreeError) as exc_info:
            self.c = Node("b", parent=self.a)
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_PARENT_PATH.format(
            path=path
        )

    def test_set_children_same_path_error(self):
        self.a = Node("a")
        self.b = Node("b")
        self.c = Node("b")
        path = "/a/b"
        with pytest.raises(TreeError) as exc_info:
            self.a.children = [self.b, self.c]
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_CHILDREN_PATH.format(
            path=path
        )

    def test_set_children_constructor_same_path_error(self):
        self.c = Node("b")
        self.b = Node("b")
        path = "/a/b"
        with pytest.raises(TreeError) as exc_info:
            self.a = Node("a", children=[self.b, self.c])
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_CHILDREN_PATH.format(
            path=path
        )

    def test_set_children_multiple_same_path_error(self):
        self.a = Node("a")
        self.b = Node("b")
        self.c = Node("b")
        self.d = Node("c")
        self.e = Node("c")
        path = "/a/b and /a/c"
        with pytest.raises(TreeError) as exc_info:
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

        with pytest.raises(LoopError) as exc_info:
            self.a.parent = self.a
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_PARENT

        with pytest.raises(LoopError) as exc_info:
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

        with pytest.raises(LoopError) as exc_info:
            self.a.children = [self.b, self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_CHILD

        with pytest.raises(LoopError) as exc_info:
            self.a.children = [self.b, self.c]
            self.c.children = [self.d, self.e, self.f]
            self.f.children = [self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_DESCENDANT

        with pytest.raises(TreeError) as exc_info:
            self.a.children = [self.b, self.b]
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_CHILD

    def test_path_name_int(self):
        b = Node(1, parent=self.a)
        assert b.path_name == "/a/1"

    def test_go_to(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

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
            combinations(list(preorder_iter(self.a)), 2), expected_paths
        ):
            actual_path = [_node.name for _node in node_pair[0].go_to(node_pair[1])]
            assert (
                actual_path == expected_path
            ), f"Wrong path for {node_pair}, expected {expected_path}, received {actual_path}"

    def test_go_to_same_node(self):
        for node in preorder_iter(self.a):
            actual_path = [_node.name for _node in node.go_to(node)]
            expected_path = [node.name]
            assert (
                actual_path == expected_path
            ), f"Wrong path for {node}, expected {expected_path}, received {actual_path}"

    def test_go_to_type_error(self):
        a = Node("a")
        destination = 2
        with pytest.raises(TypeError) as exc_info:
            a.go_to(destination)
        assert str(exc_info.value) == Constants.ERROR_NODE_GOTO_TYPE.format(
            type="BaseNode", input_type=type(destination)
        )

    def test_go_to_different_tree_error(self):
        source = Node("a")
        destination = self.a
        with pytest.raises(TreeError) as exc_info:
            source.go_to(destination)
        assert str(exc_info.value) == Constants.ERROR_NODE_GOTO_SAME_TREE.format(
            a=source, b=destination
        )


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
    expected = "/a"
    actual = root.path_name
    assert actual == expected, f"Node should have path {expected}, but path is {actual}"

    # Test age attribute
    expected_attrs = [a, b, d, e, g, h, c, f]
    for node, expected in zip(preorder_iter(root), expected_attrs):
        actual = node.get_attr("path_name")
        assert actual == expected, f"Node path should be {expected}, but it is {actual}"


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

    # Test show
    expected_str = """a\n├── b\n│   ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f\n"""
    assert_print_statement(
        self.a.show,
        expected_str,
    )

    expected_str = """a\n|-- b\n|   |-- d\n|   `-- e\n|       |-- g\n|       `-- h\n`-- c\n    `-- f\n"""
    assert_print_statement(
        self.a.show,
        expected_str,
        style="ansi",
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
    for node, expected in zip(nodes, expected_ans):
        actual = node.path_name
        assert (
            actual == expected
        ), f"Node should have path {expected}, but path is {actual}"

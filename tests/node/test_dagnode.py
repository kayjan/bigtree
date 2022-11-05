import copy
import unittest

import pandas as pd
import pytest

from bigtree.node.dagnode import DAGNode
from bigtree.node.node import Node
from bigtree.utils.exceptions import LoopError, TreeError
from bigtree.utils.iterators import dag_iterator
from tests.conftest import assert_print_statement


class TestDAGNode(unittest.TestCase):
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
        self.a = DAGNode(name="a", age=90)
        self.b = DAGNode(name="b", age=65)
        self.c = DAGNode(name="c", age=60)
        self.d = DAGNode(name="d", age=40)
        self.e = DAGNode(name="e", age=35)
        self.f = DAGNode(name="f", age=38)
        self.g = DAGNode(name="g", age=10)
        self.h = DAGNode(name="h", age=6)

    def tearDown(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None

    def test_from_dict(self):
        self.a = DAGNode().from_dict({"name": "a", "age": 90})
        self.b = DAGNode().from_dict({"name": "b", "age": 65})
        self.c = DAGNode().from_dict({"name": "c", "age": 60})
        self.d = DAGNode().from_dict({"name": "d", "age": 40})
        self.e = DAGNode().from_dict({"name": "e", "age": 35})
        self.f = DAGNode().from_dict({"name": "f", "age": 38})
        self.g = DAGNode().from_dict({"name": "g", "age": 10})
        self.h = DAGNode().from_dict({"name": "h", "age": 6})

        self.c.parents = [self.a, self.b]
        self.d.parents = [self.a, self.c]
        self.e.parents = [self.d]
        self.f.parents = [self.c, self.d]
        self.g.parents = [self.c]
        self.h.parents = [self.g]

        assert_dag_structure_self(self)
        assert_dag_structure_root(self.a)

    def test_set_parent_error(self):
        with pytest.raises(ValueError) as exc_info:
            self.c.parent = self.a
        assert str(exc_info.value).startswith("Attempting to set `parent` attribute")

        with pytest.raises(ValueError) as exc_info:
            self.c = DAGNode("b", parent=self.a)
        assert str(exc_info.value).startswith("Attempting to set `parent` attribute")

        with pytest.raises(ValueError) as exc_info:
            self.c.parent
        assert str(exc_info.value).startswith("Attempting to access `parent` attribute")

    def test_set_parents(self):
        self.c.parents = [self.a, self.b]
        self.d.parents = [self.a, self.c]
        self.e.parents = [self.d]
        self.f.parents = [self.c, self.d]
        self.g.parents = [self.c]
        self.h.parents = [self.g]

        assert_dag_structure_self(self)
        assert_dag_structure_root(self.a)

    def test_set_parents_rshift(self):
        self.a >> self.c
        self.a >> self.d
        self.b >> self.c
        self.c >> self.d
        self.c >> self.f
        self.c >> self.g
        self.d >> self.e
        self.d >> self.f
        self.g >> self.h

        assert_dag_structure_self(self)
        assert_dag_structure_root(self.a)

    def test_set_parents_lshift(self):
        self.c << self.a
        self.d << self.a
        self.c << self.b
        self.d << self.c
        self.f << self.c
        self.g << self.c
        self.e << self.d
        self.g << self.d
        self.h << self.g

    def test_set_parents_constructor(self):
        self.a = DAGNode(name="a", age=90)
        self.b = DAGNode(name="b", age=65)
        self.c = DAGNode(name="c", age=60, parents=[self.a, self.b])
        self.d = DAGNode(name="d", age=40, parents=[self.a, self.c])
        self.e = DAGNode(name="e", age=35, parents=[self.d])
        self.f = DAGNode(name="f", age=38, parents=[self.c, self.d])
        self.g = DAGNode(name="g", age=10, parents=[self.c])
        self.h = DAGNode(name="h", age=6, parents=[self.g])

        assert_dag_structure_self(self)
        assert_dag_structure_root(self.a)

    def test_set_parents_none_parent(self):
        self.c.parents = [self.a]
        with pytest.raises(TypeError):
            self.c.parents = None

    def test_set_parent_duplicate(self):
        # Set parent again
        self.c.parents = [self.a]
        self.c.parents = [self.a]

    def test_set_parent_duplicate_constructor(self):
        # Set parent again
        self.a = DAGNode(name="a", age=90)
        self.c = DAGNode(name="c", age=60, parents=[self.a])
        self.c.parents = [self.a]

    def test_set_children(self):
        self.a.children = [self.c, self.d]
        self.b.children = [self.c]
        self.c.children = [self.d, self.f, self.g]
        self.d.children = [self.e, self.f]
        self.g.children = [self.h]

        assert_dag_structure_self(self)
        assert_dag_structure_root(self.a)

    def test_set_children_constructor(self):
        self.h = DAGNode(name="h", age=6)
        self.g = DAGNode(name="g", age=10, children=[self.h])
        self.f = DAGNode(name="f", age=38)
        self.e = DAGNode(name="e", age=35)
        self.d = DAGNode(name="d", age=40)
        self.c = DAGNode(name="c", age=60)
        self.b = DAGNode(name="b", age=65)
        self.a = DAGNode(name="a", age=90, children=[self.c, self.d])
        self.c.children = [self.d, self.f, self.g]
        self.b.children = [self.c]
        self.d.children = [self.e, self.f]

        assert_dag_structure_self(self)
        assert_dag_structure_root(self.a)

    def test_set_children_none_children(self):
        with pytest.raises(TypeError):
            self.g.children = None

    def test_set_children_duplicate(self):
        # Set child again
        self.a.children = [self.c]
        self.a.children = [self.c]

    def test_set_children_duplicate_constructor(self):
        # Set child again
        self.a = DAGNode(children=[self.c])
        self.a.children = [self.c]

    def test_deep_copy_set_children(self):
        self.c.parents = [self.a, self.b]
        self.d.parents = [self.a, self.c]
        self.e.parents = [self.d]
        self.f.parents = [self.c, self.d]
        self.g.parents = [self.c]
        self.h.parents = [self.g]

        a2 = self.a.copy()
        assert (
            len(list(a2.children)) == 2
        ), f"Expected 2 children, received {len(a2.children)}"

    def test_shallow_copy_set_children(self):
        self.a.children = [self.c, self.d]
        self.b.children = [self.c]
        self.c.children = [self.d, self.f, self.g]
        self.d.children = [self.e, self.f]
        self.g.children = [self.h]

        a2 = copy.copy(self.a)
        assert (
            len(list(a2.children)) == 2
        ), f"Expected 2 child, received {len(list(a2.children))}"
        assert (
            a2.children[0] == self.c or a2.children[1] == self.c
        ), "Shallow copy does not copy child nodes"

    def test_error_set_parent_type_error(self):
        # Error: wrong type
        with pytest.raises(TypeError):
            self.a.parents = 1

        # Error: wrong type
        with pytest.raises(TypeError):
            self.a.parents = [1]

        # Error: wrong type
        with pytest.raises(TypeError):
            self.a.parents = [Node("a"), Node("b")]

    def test_error_set_parent_loop_error(self):
        # Error: set self as parent
        with pytest.raises(LoopError):
            self.a.parents = [self.a]

        # Error: set descendant as parent
        with pytest.raises(LoopError):
            self.b.parents = [self.a]
            self.c.parents = [self.b]
            self.a.parents = [self.c]

    def test_error_set_parent_exception(self):
        # Error: duplicate child
        with pytest.raises(TreeError):
            self.a.parents = [self.b, self.b]

    def test_error_set_children_type_error(self):
        # Error: wrong type
        with pytest.raises(TypeError):
            self.a.children = 1

        with pytest.raises(TypeError):
            self.a.children = [self.b, 1]

        # Error: wrong type
        with pytest.raises(TypeError):
            self.a.children = [Node("a"), Node("b")]

    def test_error_set_children_loop_error(self):
        # Error: set self as child
        with pytest.raises(LoopError):
            self.a.children = [self.b, self.a]

        # Error: set ancestor as child
        with pytest.raises(LoopError):
            self.a.children = [self.b, self.c]
            self.c.children = [self.d, self.e, self.f]
            self.f.children = [self.a]

    def test_error_set_children_exception(self):
        # Error: duplicate child
        with pytest.raises(TreeError):
            self.a.children = [self.b, self.b]

    def assert_tree_structure_basenode_root_attr(root):
        # Test describe()
        expected = [("age", 90), ("name", "a")]
        actual = root.describe(exclude_prefix="_")
        assert (
            actual == expected
        ), f"Node description should be {expected}, but it is {actual}"


def assert_dag_structure_self(self):
    """
    Tree should have structure
    a >> c
    a >> d
    b >> c
    c >> d
    c >> f
    c >> g
    d >> e
    g >> h
    """
    nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

    # Test parent
    expected_ans = [
        [],
        [],
        [self.a, self.b],
        [self.a, self.c],
        [self.d],
        [self.c, self.d],
        [self.c],
        [self.g],
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = list(node.parents)
        assert set(id(_node) for _node in actual) == set(
            id(_node) for _node in expected
        ), f"Parents of {node} is wrong, expected {expected}, received {actual}"

    # Test children
    expected_ans = [
        [self.c, self.d],
        [self.c],
        [self.d, self.f, self.g],
        [self.e, self.f],
        [],
        [],
        [self.h],
        [],
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = list(node.children)
        assert set(id(_node) for _node in actual) == set(
            id(_node) for _node in expected
        ), f"Children of {node} is wrong, expected {expected}, received {actual}"

    # Test ancestors
    expected_ans = [
        [],
        [],
        [self.a, self.b],
        [self.a, self.b, self.c],
        [self.a, self.b, self.c, self.d],
        [self.a, self.b, self.c, self.d],
        [self.a, self.b, self.c],
        [self.a, self.b, self.c, self.g],
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = list(node.ancestors)
        assert set(id(_node) for _node in actual) == set(
            id(_node) for _node in expected
        ), f"Ancestors of {node} is wrong, expected {expected}, received {actual}"

    # Test descendants
    expected_ans = [
        [self.c, self.d, self.e, self.f, self.g, self.h],
        [self.c, self.d, self.e, self.f, self.g, self.h],
        [self.d, self.e, self.f, self.g, self.h],
        [self.e, self.f],
        [],
        [],
        [self.h],
        [],
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = list(node.descendants)
        assert (
            actual == expected
        ), f"Descendants of {node} is wrong, expected {expected}, received {actual}"

    # Test siblings
    expected_ans = [
        (),
        (),
        (self.d,),
        (self.c, self.f, self.g),
        (self.f,),
        (self.d, self.g, self.e),
        (self.d, self.f),
        (),
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = node.siblings
        assert (
            actual == expected
        ), f"Siblings of {node} is wrong, expected {expected}, received {actual}"

    # Test node_name
    expected_ans = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for node, expected in zip(nodes, expected_ans):
        actual = node.node_name
        assert (
            actual == expected
        ), f"node_name of {node} is wrong, expected {expected}, received {actual}"

    # Test is_root
    expected_ans = [True, True, False, False, False, False, False, False]
    for node, expected in zip(nodes, expected_ans):
        actual = node.is_root
        assert (
            actual == expected
        ), f"is_root of {node} is wrong, expected {expected}, received {actual}"

    # Test is_leaf
    expected_ans = [False, False, False, False, True, True, False, True]
    for node, expected in zip(nodes, expected_ans):
        actual = node.is_leaf
        assert (
            actual == expected
        ), f"is_leaf of {node} is wrong, expected {expected}, received {actual}"

    # Test describe()
    expected_ans = [
        [("age", 90), ("name", "a")],
        [("age", 65), ("name", "b")],
        [("age", 60), ("name", "c")],
        [("age", 40), ("name", "d")],
        [("age", 35), ("name", "e")],
        [("age", 38), ("name", "f")],
        [("age", 10), ("name", "g")],
        [("age", 6), ("name", "h")],
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = node.describe(exclude_prefix="_")
        assert (
            actual == expected
        ), f"Node description should be {expected}, but it is {actual}"

    # Test get_attr()
    expected_ans = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for node, expected in zip(nodes, expected_ans):
        actual = node.get_attr("name")
        assert (
            actual == expected
        ), f"Node attribute should be {expected}, but it is {actual}"

    expected = None
    for node in nodes:
        actual = node.get_attr("something")
        assert (
            actual == expected
        ), f"Node attribute should be {expected}, but it is {actual}"

    # Test __repr__
    expected_ans = [
        "DAGNode(a, age=90)\n",
        "DAGNode(b, age=65)\n",
        "DAGNode(c, age=60)\n",
        "DAGNode(d, age=40)\n",
        "DAGNode(e, age=35)\n",
        "DAGNode(f, age=38)\n",
        "DAGNode(g, age=10)\n",
        "DAGNode(h, age=6)\n",
    ]
    for node, expected in zip(nodes, expected_ans):
        assert_print_statement(print, expected, node)

    # Test set_attrs()
    attrs = [1, 2, 3, 4, 5, 6, 7, 8]
    for node, expected in zip(nodes, attrs):
        node.set_attrs({"index": expected})
        actual = node.get_attr("index")
        assert (
            actual == expected
        ), f"Node attribute should be {expected}, but it is {actual}"


def assert_dag_structure_root(dag):
    expected = [
        ("a", "c"),
        ("a", "d"),
        ("b", "c"),
        ("c", "d"),
        ("c", "f"),
        ("c", "g"),
        ("d", "e"),
        ("d", "f"),
        ("g", "h"),
    ]
    actual = [
        (parent.node_name, child.node_name) for parent, child in dag_iterator(dag)
    ]
    len_expected = 9
    len_actual = len(actual)
    for relation in actual:
        if relation[1] in ["a", "b"]:
            len_expected = 11
            assert pd.isnull(relation[0]), f"Expected\n{relation}\nReceived\n{actual}"
        else:
            assert relation in expected, f"Expected\n{relation}\nReceived\n{actual}"
    assert (
        len_expected == len_actual
    ), f"Expected\n{len_expected}\nReceived\n{len_actual}"


def assert_dag_structure_attr_root(dag):
    expected_dict = {
        "a": 90,
        "b": 65,
        "c": 60,
        "d": 40,
        "e": 35,
        "f": 38,
        "g": 10,
        "h": 6,
    }
    for parent, child in dag_iterator(dag):
        expected = expected_dict[parent.node_name]
        actual = parent.age
        assert (
            expected == actual
        ), f"For {parent}, expected\n{expected}\nReceived\n{actual}"

        expected = expected_dict[child.node_name]
        actual = child.age
        assert (
            expected == actual
        ), f"For {child}, expected\n{expected}\nReceived\n{actual}"

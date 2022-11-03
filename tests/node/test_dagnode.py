import copy
import unittest

import pytest

from bigtree.node.dagnode import DAGNode
from bigtree.node.node import Node
from bigtree.utils.exceptions import LoopError, TreeError
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

    def tearDown(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None

    def test_from_dict(self):
        self.a = DAGNode().from_dict({"name": "a", "age": 90})
        self.b = DAGNode().from_dict({"name": "b", "age": 65})
        self.c = DAGNode().from_dict({"name": "c", "age": 60})
        self.d = DAGNode().from_dict({"name": "d", "age": 40})
        self.e = DAGNode().from_dict({"name": "e", "age": 35})
        self.f = DAGNode().from_dict({"name": "f", "age": 38})
        self.g = DAGNode().from_dict({"name": "g", "age": 10})
        self.h = DAGNode().from_dict({"name": "h", "age": 6})

        self.b.parents = [self.a]
        self.c.parents = [self.b]
        self.d.parents = [self.b]
        self.e.parents = [self.c, self.d]
        self.f.parents = [self.c, self.e]
        self.g.parents = [self.f]

        assert_tree_structure_dag_self(self)

    def test_set_parent_error(self):
        with pytest.raises(ValueError) as exc_info:
            self.b.parent = self.a
        assert str(exc_info.value).startswith("Attempting to set `parent` attribute")

        with pytest.raises(ValueError) as exc_info:
            self.b = DAGNode("b", parent=self.a)
        assert str(exc_info.value).startswith("Attempting to set `parent` attribute")

        with pytest.raises(ValueError) as exc_info:
            self.b.parent
        assert str(exc_info.value).startswith("Attempting to access `parent` attribute")

    def test_set_parents(self):
        self.b.parents = [self.a]
        self.c.parents = [self.b]
        self.d.parents = [self.b]
        self.e.parents = [self.c, self.d]
        self.f.parents = [self.c, self.e]
        self.g.parents = [self.f]

        assert_tree_structure_dag_self(self)

    def test_set_parents_rshift(self):
        self.a >> self.b
        self.b >> self.c
        self.b >> self.d
        self.c >> self.e
        self.c >> self.f
        self.e >> self.f
        self.f >> self.g
        self.d >> self.e

        assert_tree_structure_dag_self(self)

    def test_set_parents_lshift(self):
        self.b << self.a
        self.c << self.b
        self.d << self.b
        self.e << self.c
        self.e << self.d
        self.f << self.c
        self.f << self.e
        self.g << self.f

    def test_set_parents_constructor(self):
        self.a = DAGNode(name="a", age=90)
        self.b = DAGNode(name="b", age=65, parents=[self.a])
        self.c = DAGNode(name="c", age=60, parents=[self.b])
        self.d = DAGNode(name="d", age=40, parents=[self.b])
        self.e = DAGNode(name="e", age=35, parents=[self.c, self.d])
        self.f = DAGNode(name="f", age=38, parents=[self.c, self.e])
        self.g = DAGNode(name="g", age=10, parents=[self.f])

        assert_tree_structure_dag_self(self)

    def test_set_parents_none_parent(self):
        self.b.parents = [self.a]
        with pytest.raises(TypeError):
            self.b.parents = None

    def test_set_parent_duplicate(self):
        # Set parent again
        self.b.parents = [self.a]
        self.b.parents = [self.a]

    def test_set_parent_duplicate_constructor(self):
        # Set parent again
        self.a = DAGNode(name="a", age=90)
        self.b = DAGNode(name="b", age=65, parents=[self.a])
        self.b.parents = [self.a]

    def test_set_children(self):
        self.a.children = [self.b]
        self.b.children = [self.c, self.d]
        self.c.children = [self.e, self.f]
        self.d.children = [self.e]
        self.e.children = [self.f]
        self.f.children = [self.g]
        self.g.children = []

        assert_tree_structure_dag_self(self)

    def test_set_children_constructor(self):
        self.g = DAGNode(name="g", age=10, children=[])
        self.f = DAGNode(name="f", age=38, children=[self.g])
        self.e = DAGNode(name="e", age=35, children=[self.f])
        self.d = DAGNode(name="d", age=40, children=[self.e])
        self.c = DAGNode(name="c", age=60, children=[self.e, self.f])
        self.b = DAGNode(name="b", age=65, children=[self.c, self.d])
        self.a = DAGNode(name="a", age=90, children=[self.b])

        assert_tree_structure_dag_self(self)

    def test_set_children_none_children(self):
        with pytest.raises(TypeError):
            self.g.children = None

    def test_set_children_duplicate(self):
        # Set child again
        self.a.children = [self.b]
        self.a.children = [self.b]

    def test_set_children_duplicate_constructor(self):
        # Set child again
        self.a = DAGNode(children=[self.b])
        self.a.children = [self.b]

    def test_deep_copy_set_children(self):
        self.b.parents = [self.a]
        self.c.parents = [self.b]
        self.d.parents = [self.b]
        self.e.parents = [self.c, self.d]
        self.f.parents = [self.c, self.e]
        self.g.parents = [self.f]

        a2 = self.a.copy()
        assert (
            len(list(a2.children)) == 1
        ), f"Expected 2 children, received {len(a2.children)}"

    def test_shallow_copy_set_children(self):
        self.a.children = [self.b]
        self.b.children = [self.c, self.d]
        self.c.children = [self.e, self.f]
        self.d.children = [self.e]
        self.e.children = [self.f]
        self.f.children = [self.g]
        self.g.children = []

        a2 = copy.copy(self.a)
        assert (
            len(list(a2.children)) == 1
        ), f"Expected 1 child, received {len(list(a2.children))}"
        assert (
            a2.children[0] == self.b or a2.children[1] == self.b
        ), "Shallow copy does not copy child nodes"
        assert len(list(a2.children)) == 1, "Shallow copy does not copy child nodes"

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


def assert_tree_structure_dag_self(self):
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
    nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g]

    # Test parent
    expected_ans = [
        [],
        [self.a],
        [self.b],
        [self.b],
        [self.c, self.d],
        [self.c, self.e],
        [self.f],
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = list(node.parents)
        assert set(id(_node) for _node in actual) == set(
            id(_node) for _node in expected
        ), f"Parents of {node} is wrong, expected {expected}, received {actual}"

    # Test children
    expected_ans = [
        [self.b],
        [self.c, self.d],
        [self.e, self.f],
        [self.e],
        [self.f],
        [self.g],
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
        [self.a],
        [self.a, self.b],
        [self.a, self.b],
        [self.a, self.b, self.c, self.d],
        [self.a, self.b, self.c, self.d, self.e],
        [self.a, self.b, self.c, self.d, self.e, self.f],
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = list(node.ancestors)
        assert set(id(_node) for _node in actual) == set(
            id(_node) for _node in expected
        ), f"Ancestors of {node} is wrong, expected {expected}, received {actual}"

    # Test descendants
    expected_ans = [
        [self.b, self.c, self.e, self.f, self.g, self.d],
        [self.c, self.e, self.f, self.g, self.d],
        [self.e, self.f, self.g],
        [self.e, self.f, self.g],
        [self.f, self.g],
        [self.g],
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
        (self.c,),
        (self.f,),
        (self.e,),
        (),
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = node.siblings
        assert (
            actual == expected
        ), f"Siblings of {node} is wrong, expected {expected}, received {actual}"

    # Test node_name
    expected_ans = ["a", "b", "c", "d", "e", "f", "g"]
    for node, expected in zip(nodes, expected_ans):
        actual = node.node_name
        assert (
            actual == expected
        ), f"node_name of {node} is wrong, expected {expected}, received {actual}"

    # Test is_root
    expected_ans = [True, False, False, False, False, False, False]
    for node, expected in zip(nodes, expected_ans):
        actual = node.is_root
        assert (
            actual == expected
        ), f"is_root of {node} is wrong, expected {expected}, received {actual}"

    # Test is_leaf
    expected_ans = [False, False, False, False, False, False, True]
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
    ]
    for node, expected in zip(nodes, expected_ans):
        assert_print_statement(print, expected, node)

    # Test set_attrs()
    attrs = [1, 2, 3, 4, 5, 6, 7]
    for node, expected in zip(nodes, attrs):
        node.set_attrs({"index": expected})
        actual = node.get_attr("index")
        assert (
            actual == expected
        ), f"Node attribute should be {expected}, but it is {actual}"

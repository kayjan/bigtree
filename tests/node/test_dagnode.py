import copy
import unittest
from itertools import combinations

import pandas as pd
import pytest

from bigtree.node.basenode import BaseNode
from bigtree.node.dagnode import DAGNode
from bigtree.node.node import Node
from bigtree.utils.exceptions import LoopError, TreeError
from bigtree.utils.iterators import dag_iterator
from tests.conftest import assert_print_statement
from tests.test_constants import Constants


class DAGNode2(DAGNode):
    def _DAGNode__post_assign_parents(self, new_parents):
        if self.get_attr("val"):
            raise Exception("Custom error assigning parent")
        for parent in new_parents:
            if parent.get_attr("val"):
                raise Exception(
                    f"Custom error assigning parent, new children {new_parents}"
                )


class DAGNode3(DAGNode):
    def _DAGNode__post_assign_children(self, new_children):
        if self.get_attr("val"):
            raise Exception("Custom error assigning children")
        for child in new_children:
            if child.get_attr("val"):
                raise Exception(
                    f"Custom error assigning children, new children {new_children}"
                )


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

    def test_from_dict(self):
        self.a = DAGNode.from_dict({"name": "a", "age": 90})
        self.b = DAGNode.from_dict({"name": "b", "age": 65})
        self.c = DAGNode.from_dict({"name": "c", "age": 60})
        self.d = DAGNode.from_dict({"name": "d", "age": 40})
        self.e = DAGNode.from_dict({"name": "e", "age": 35})
        self.f = DAGNode.from_dict({"name": "f", "age": 38})
        self.g = DAGNode.from_dict({"name": "g", "age": 10})
        self.h = DAGNode.from_dict({"name": "h", "age": 6})

        self.c.parents = [self.a, self.b]
        self.d.parents = [self.a, self.c]
        self.e.parents = [self.d]
        self.f.parents = [self.c, self.d]
        self.g.parents = [self.c]
        self.h.parents = [self.g]

        assert_dag_structure_self(self)
        assert_dag_structure_root(self.a)

    def test_set_parent_error(self):
        with pytest.raises(AttributeError) as exc_info:
            self.c.parent = self.a
        assert str(exc_info.value) == Constants.ERROR_NODE_SET_PARENT_ATTR

        with pytest.raises(AttributeError) as exc_info:
            self.c = DAGNode("b", parent=self.a)
        assert str(exc_info.value) == Constants.ERROR_NODE_SET_PARENT_ATTR

        with pytest.raises(AttributeError) as exc_info:
            self.c.parent
        assert str(exc_info.value) == Constants.ERROR_NODE_GET_PARENT_ATTR

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

    def test_set_parents_none_parent_error(self):
        self.c.parents = [self.a]
        parents = None
        with pytest.raises(TypeError) as exc_info:
            self.c.parents = parents
        assert str(exc_info.value) == Constants.ERROR_DAGNODE_PARENTS_TYPE.format(
            input_type=type(parents)
        )

    def test_set_parent_reassign(self):
        self.a.children = [self.b, self.c]
        self.d.children = [self.e]
        self.b.parents = [self.d]
        assert list(self.a.children) == [
            self.b,
            self.c,
        ], f"Node a children, expected {[self.c]}, received {self.a.children}"
        assert list(self.d.children) == [
            self.e,
            self.b,
        ], f"Node d children, expected {[self.e, self.b]}, received {self.d.children}"
        assert list(self.b.parents) == [
            self.a,
            self.d,
        ], f"Node b parents, expected {[self.a, self.d]}, received {self.b.parents}"

    def test_set_parent_duplicate(self):
        self.c.parents = [self.a]
        self.c.parents = [self.a]
        assert list(self.a.children) == [self.c]
        assert list(self.c.parents) == [self.a]

    def test_set_parent_duplicate_constructor(self):
        self.a = DAGNode(name="a", age=90)
        self.c = DAGNode(name="c", age=60, parents=[self.a])
        self.c.parents = [self.a]
        assert list(self.a.children) == [self.c]
        assert list(self.c.parents) == [self.a]

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

    def test_set_children_none_children_error(self):
        children = None
        with pytest.raises(TypeError) as exc_info:
            self.g.children = children
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE.format(
            type="Iterable", input_type=type(children)
        )

    def test_set_children_reassign(self):
        self.a.children = [self.c]
        self.b.parents = [self.a]
        self.d.children = [self.e, self.b]
        assert list(self.a.children) == [
            self.c,
            self.b,
        ], f"Node a children, expected {[self.c]}, received {self.a.children}"
        assert list(self.d.children) == [
            self.e,
            self.b,
        ], f"Node d children, expected {[self.e, self.b]}, received {self.d.children}"
        assert list(self.b.parents) == [
            self.a,
            self.d,
        ], f"Node b parents, expected {[self.a, self.d]}, received {self.b.parents}"

    def test_set_children_duplicate(self):
        self.a.children = [self.c]
        self.a.children = [self.c]

    def test_set_children_duplicate_constructor(self):
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

    def test_set_parents_type_error(self):
        parents = 1
        with pytest.raises(TypeError) as exc_info:
            self.a.parents = parents
        assert str(exc_info.value) == Constants.ERROR_DAGNODE_PARENTS_TYPE.format(
            input_type=type(parents)
        )

        parent = 1
        with pytest.raises(TypeError) as exc_info:
            self.a.parents = [parent]
        assert str(exc_info.value) == Constants.ERROR_NODE_PARENT_TYPE.format(
            type="DAGNode", input_type=type(parent)
        )

        parent = BaseNode()
        with pytest.raises(TypeError) as exc_info:
            self.a.parents = [parent]
        assert str(exc_info.value) == Constants.ERROR_NODE_PARENT_TYPE.format(
            type="DAGNode", input_type=type(parent)
        )

        parent = Node("a")
        with pytest.raises(TypeError) as exc_info:
            self.a.parents = [parent]
        assert str(exc_info.value) == Constants.ERROR_NODE_PARENT_TYPE.format(
            type="DAGNode", input_type=type(parent)
        )

    def test_set_parents_loop_error(self):
        with pytest.raises(LoopError) as exc_info:
            self.a.parents = [self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_PARENT

        with pytest.raises(LoopError) as exc_info:
            self.b.parents = [self.a]
            self.c.parents = [self.b]
            self.a.parents = [self.c]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_ANCESTOR

    def test_set_duplicate_parent_error(self):
        with pytest.raises(TreeError) as exc_info:
            self.a.parents = [self.b, self.b]
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_PARENT

    def test_set_children_mutable_list(self):
        children_list = [self.c, self.d]
        self.a.children = children_list
        children_list.pop()
        actual_children = self.a.children
        expected_children = (self.c, self.d)
        assert (
            actual_children == expected_children
        ), f"Expected {expected_children}, Received {actual_children}"

    def test_set_children_iterable(self):
        self.a.children = (self.c, self.d)
        self.b.children = {self.c}
        self.c.children = (self.d, self.f, self.g)
        self.d.children = {self.e: 0, self.f: 0}
        self.g.children = {self.h}

        assert_dag_structure_self(self)
        assert_dag_structure_root(self.a)

    def test_set_children_type_error(self):
        children = 1
        with pytest.raises(TypeError) as exc_info:
            self.a.children = children
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE.format(
            type="Iterable", input_type=type(children)
        )

        children = 1
        with pytest.raises(TypeError) as exc_info:
            self.a.children = [self.b, children]
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE.format(
            type="DAGNode", input_type=type(children)
        )

        children = BaseNode()
        with pytest.raises(TypeError) as exc_info:
            self.a.children = [children]
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE.format(
            type="DAGNode", input_type=type(children)
        )

        children = Node("a")
        with pytest.raises(TypeError) as exc_info:
            self.a.children = [children]
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE.format(
            type="DAGNode", input_type=type(children)
        )

    def test_set_children_loop_error(self):
        with pytest.raises(LoopError) as exc_info:
            self.a.children = [self.b, self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_CHILD

        with pytest.raises(LoopError) as exc_info:
            self.a.children = [self.b, self.c]
            self.c.children = [self.d, self.e, self.f]
            self.f.children = [self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_DESCENDANT

    def test_set_duplicate_children_error(self):
        with pytest.raises(TreeError) as exc_info:
            self.a.children = [self.b, self.b]
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_CHILD

    @staticmethod
    def test_rollback_set_parents():
        a = DAGNode2(name="a", age=90)
        b = DAGNode2(name="b", age=65)
        c = DAGNode2(name="c", age=60)
        d = DAGNode2(name="d", age=40)
        e = DAGNode2(name="e", age=35)
        f = DAGNode2(name="f", age=38)
        g = DAGNode2(name="g", age=10)
        h = DAGNode2(name="h", age=6)
        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        f.set_attrs({"val": 1})
        with pytest.raises(TreeError) as exc_info:
            f.parents = [a, h]
        assert str(exc_info.value) == "Custom error assigning parent"

        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        assert not d.parents, f"Expected Node d parent to be None, received {d.parents}"
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert list(child.parents) == [
                        parent
                    ], f"Node {child} parent, expected {parent}, received {child.parents}"

    @staticmethod
    def test_rollback_set_parents_no_parents():
        a = DAGNode2(name="a", age=90)
        b = DAGNode2(name="b", age=65)
        c = DAGNode2(name="c", age=60)
        d = DAGNode2(name="d", age=40)
        e = DAGNode2(name="e", age=35)
        f = DAGNode2(name="f", age=38)
        g = DAGNode2(name="g", age=10)
        h = DAGNode2(name="h", age=6)
        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        d.set_attrs({"val": 1})
        with pytest.raises(TreeError) as exc_info:
            d.parents = [a, h]
        assert str(exc_info.value) == "Custom error assigning parent"

        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        assert not d.parents, f"Expected Node d parent to be None, received {d.parents}"
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert list(child.parents) == [
                        parent
                    ], f"Node {child} parent, expected {parent}, received {child.parents}"

    @staticmethod
    def test_rollback_set_parents_null_parents():
        a = DAGNode2(name="a", age=90)
        b = DAGNode2(name="b", age=65)
        c = DAGNode2(name="c", age=60)
        d = DAGNode2(name="d", age=40)
        e = DAGNode2(name="e", age=35)
        f = DAGNode2(name="f", age=38)
        g = DAGNode2(name="g", age=10)
        h = DAGNode2(name="h", age=6)
        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        f.set_attrs({"val": 1})
        with pytest.raises(TreeError) as exc_info:
            f.parents = []
        assert str(exc_info.value) == "Custom error assigning parent"

        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        assert not d.parents, f"Expected Node d parent to be None, received {d.parents}"
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert list(child.parents) == [
                        parent
                    ], f"Node {child} parent, expected {parent}, received {child.parents}"

    @staticmethod
    def test_rollback_set_parents_reassign():
        a = DAGNode2(name="a", age=90)
        b = DAGNode2(name="b", age=65)
        c = DAGNode2(name="c", age=60)
        d = DAGNode2(name="d", age=40)
        e = DAGNode2(name="e", age=35)
        f = DAGNode2(name="f", age=38)
        g = DAGNode2(name="g", age=10)
        h = DAGNode2(name="h", age=6)
        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        f.set_attrs({"val": 1})
        with pytest.raises(TreeError) as exc_info:
            f.parents = [h]
        assert str(exc_info.value) == "Custom error assigning parent"

        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        assert not d.parents, f"Expected Node d parent to be None, received {d.parents}"
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert list(child.parents) == [
                        parent
                    ], f"Node {child} parent, expected {parent}, received {child.parents}"

    @staticmethod
    def test_rollback_set_children():
        a = DAGNode3(name="a", age=90)
        b = DAGNode3(name="b", age=65)
        c = DAGNode3(name="c", age=60)
        d = DAGNode3(name="d", age=40)
        e = DAGNode3(name="e", age=35)
        f = DAGNode3(name="f", age=38)
        g = DAGNode3(name="g", age=10)
        h = DAGNode3(name="h", age=6)
        i = DAGNode3(name="i")
        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        b.set_attrs({"val": 1})
        with pytest.raises(TreeError) as exc_info:
            a.children = [b, c, d, g, i, f]
        assert str(exc_info.value).startswith("Custom error assigning children, ")
        assert not len(
            list(i.parents)
        ), f"Node i parent, expected None, received {i.parents}"

        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert list(child.parents) == [
                        parent
                    ], f"Node {child} parent, expected {parent}, received {child.parents}"

    @staticmethod
    def test_rollback_set_children_null_children():
        a = DAGNode3(name="a", age=90)
        b = DAGNode3(name="b", age=65)
        c = DAGNode3(name="c", age=60)
        d = DAGNode3(name="d", age=40)
        e = DAGNode3(name="e", age=35)
        f = DAGNode3(name="f", age=38)
        g = DAGNode3(name="g", age=10)
        h = DAGNode3(name="h", age=6)
        i = DAGNode3(name="i")
        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        a.set_attrs({"val": 1})
        with pytest.raises(TreeError) as exc_info:
            a.children = []
        assert str(exc_info.value) == "Custom error assigning children"
        assert not len(
            list(i.parents)
        ), f"Node i parent, expected None, received {i.parents}"

        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert list(child.parents) == [
                        parent
                    ], f"Node {child} parent, expected {parent}, received {child.parents}"

    @staticmethod
    def test_rollback_set_children_reassign():
        a = DAGNode3(name="a", age=90)
        b = DAGNode3(name="b", age=65)
        c = DAGNode3(name="c", age=60)
        d = DAGNode3(name="d", age=40)
        e = DAGNode3(name="e", age=35)
        f = DAGNode3(name="f", age=38)
        g = DAGNode3(name="g", age=10)
        h = DAGNode3(name="h", age=6)
        i = DAGNode3(name="i")
        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        b.set_attrs({"val": 1})
        with pytest.raises(TreeError) as exc_info:
            a.children = [b, c, d]
        assert str(exc_info.value).startswith("Custom error assigning children, ")
        assert not len(
            list(i.parents)
        ), f"Node i parent, expected None, received {i.parents}"

        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert list(child.parents) == [
                        parent
                    ], f"Node {child} parent, expected {parent}, received {child.parents}"

    def test_go_to(self):
        self.a >> self.b
        self.b >> self.c
        self.b >> self.d
        self.c >> self.e
        self.c >> self.f
        self.e >> self.f
        self.f >> self.g
        self.d >> self.e

        expected_paths = [
            [["a", "b"]],
            [["a", "b", "c"]],
            [["a", "b", "d"]],
            [["a", "b", "c", "e"], ["a", "b", "d", "e"]],
            [
                ["a", "b", "c", "e", "f"],
                ["a", "b", "c", "f"],
                ["a", "b", "d", "e", "f"],
            ],
            [
                ["a", "b", "c", "e", "f", "g"],
                ["a", "b", "c", "f", "g"],
                ["a", "b", "d", "e", "f", "g"],
            ],
            [["b", "c"]],
            [["b", "d"]],
            [["b", "c", "e"], ["b", "d", "e"]],
            [["b", "c", "e", "f"], ["b", "c", "f"], ["b", "d", "e", "f"]],
            [
                ["b", "c", "e", "f", "g"],
                ["b", "c", "f", "g"],
                ["b", "d", "e", "f", "g"],
            ],
            None,
            [["c", "e"]],
            [["c", "e", "f"], ["c", "f"]],
            [["c", "e", "f", "g"], ["c", "f", "g"]],
            [["d", "e"]],
            [["d", "e", "f"]],
            [["d", "e", "f", "g"]],
            [["e", "f"]],
            [["e", "f", "g"]],
            [["f", "g"]],
        ]
        for node_pair, expected_path in zip(
            combinations(self.nodes, 2), expected_paths
        ):
            if not expected_path:
                with pytest.raises(TreeError) as exc_info:
                    node_pair[0].go_to(node_pair[1])
                assert str(exc_info.value) == Constants.ERROR_NODE_GOTO.format(
                    node=node_pair[1]
                )
            else:
                actual_path = [
                    [_node.name for _node in _path]
                    for _path in node_pair[0].go_to(node_pair[1])
                ]
                assert (
                    actual_path == expected_path
                ), f"Wrong path for {node_pair}, expected {expected_path}, received {actual_path}"

    def test_go_to_same_node(self):
        self.a >> self.b
        self.b >> self.c
        self.b >> self.d
        self.c >> self.e
        self.c >> self.f
        self.e >> self.f
        self.f >> self.g
        self.d >> self.e

        for node in self.nodes:
            actual_path = [
                [_node2.name for _node2 in _node] for _node in node.go_to(node)
            ]
            expected_path = [[node.name]]
            assert (
                actual_path == expected_path
            ), f"Wrong path for {node}, expected {expected_path}, received {actual_path}"

    def test_go_to_type_error(self):
        destination = 2
        with pytest.raises(TypeError) as exc_info:
            self.a.go_to(destination)
        assert str(exc_info.value) == Constants.ERROR_NODE_GOTO_TYPE.format(
            type="DAGNode", input_type=type(destination)
        )

    def test_go_to_different_tree_error(self):
        a = DAGNode("a")
        with pytest.raises(TreeError) as exc_info:
            a.go_to(self.a)
        assert str(exc_info.value) == Constants.ERROR_NODE_GOTO.format(node=self.a)


def assert_dag_structure_root(dag):
    """Test tree structure"""
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


def assert_dag_structure_root_attr(dag):
    """Test tree structure with age attributes"""
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
            actual == expected
        ), f"For {parent}, expected\n{expected}\nReceived\n{actual}"

        expected = expected_dict[child.node_name]
        actual = child.age
        assert (
            actual == expected
        ), f"For {child}, expected\n{expected}\nReceived\n{actual}"


def assert_dag_structure_self(self):
    """Test tree structure with self object
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


def assert_dag_child_attr(dag, parent_name, child_name, child_attr, child_value):
    """Test tree attributes"""
    for parent, child in dag_iterator(dag):
        if parent.name == parent_name and child.name == child_name:
            expected = child_value
            actual = child.get_attr(child_attr)
            assert actual == expected, f"Expected {expected}, received {actual}"

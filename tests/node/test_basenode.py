import copy
import unittest

import matplotlib.pyplot as plt
import pytest

from bigtree.node import basenode
from bigtree.tree import helper
from bigtree.utils import exceptions, iterators
from tests.conftest import assert_print_statement
from tests.test_constants import Constants


class BaseNode2(basenode.BaseNode):
    def _BaseNode__post_assign_parent(self, new_parent):
        if new_parent is not None:
            if new_parent.get_attr("val"):
                raise Exception(
                    f"Custom error assigning parent, new parent {new_parent} and children are {new_parent.children}"
                )
        elif self.get_attr("val"):
            raise Exception("Custom error assigning parent")


class BaseNode3(basenode.BaseNode):
    def _BaseNode__post_assign_children(self, new_children):
        if self.get_attr("val"):
            raise Exception("Custom error assigning children")
        for child in new_children:
            if child.get_attr("val"):
                raise Exception(
                    f"Custom error assigning children, new children {new_children}"
                )


class TestBaseNode(unittest.TestCase):
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

    def test_from_dict(self):
        self.a = basenode.BaseNode.from_dict({"name": "a", "age": 90})
        self.b = basenode.BaseNode.from_dict({"name": "b", "age": 65})
        self.c = basenode.BaseNode.from_dict({"name": "c", "age": 60})
        self.d = basenode.BaseNode.from_dict({"name": "d", "age": 40})
        self.e = basenode.BaseNode.from_dict({"name": "e", "age": 35})
        self.f = basenode.BaseNode.from_dict({"name": "f", "age": 38})
        self.g = basenode.BaseNode.from_dict({"name": "g", "age": 10})
        self.h = basenode.BaseNode.from_dict({"name": "h", "age": 6})

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
        assert_print_statement(print, "BaseNode(age=90, name=a)\n", self.a)

    def test_set_parents_error(self):
        with pytest.raises(AttributeError) as exc_info:
            self.b.parents = [self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_SET_PARENTS_ATTR

        with pytest.raises(AttributeError) as exc_info:
            self.b = basenode.BaseNode(parents=[self.a])
        assert str(exc_info.value) == Constants.ERROR_NODE_SET_PARENTS_ATTR

        with pytest.raises(AttributeError) as exc_info:
            self.b.parents
        assert str(exc_info.value) == Constants.ERROR_NODE_GET_PARENTS_ATTR

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

    def test_set_parent_sort(self):
        self.h.parent = self.e
        self.g.parent = self.e
        self.f.parent = self.c
        self.e.parent = self.b
        self.d.parent = self.b
        self.c.parent = self.a
        self.b.parent = self.a

        self.a.sort(key=lambda x: x.name)
        self.b.sort(key=lambda x: x.name)
        self.e.sort(key=lambda x: x.name)
        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_parent_rshift(self):
        self.a >> self.b
        self.a >> self.c
        self.b >> self.d
        self.b >> self.e
        self.c >> self.f
        self.e >> self.g
        self.e >> self.h

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_parent_lshift(self):
        self.b << self.a
        self.c << self.a
        self.d << self.b
        self.e << self.b
        self.f << self.c
        self.g << self.e
        self.h << self.e

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_parent_constructor(self):
        self.a = basenode.BaseNode(name="a", age=90)
        self.b = basenode.BaseNode(name="b", age=65, parent=self.a)
        self.c = basenode.BaseNode(name="c", age=60, parent=self.a)
        self.d = basenode.BaseNode(name="d", age=40, parent=self.b)
        self.e = basenode.BaseNode(name="e", age=35, parent=self.b)
        self.f = basenode.BaseNode(name="f", age=38, parent=self.c)
        self.g = basenode.BaseNode(name="g", age=10, parent=self.e)
        self.h = basenode.BaseNode(name="h", age=6, parent=self.e)

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_parent_null_parent(self):
        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.f.parent = self.c
        self.g.parent = self.e
        self.h.parent = self.e

        dummy = basenode.BaseNode()
        dummy.parent = self.h
        assert list(self.h.children) == [dummy]

        dummy.parent = None
        assert not len(list(self.h.children))

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_parent_reassign(self):
        self.a.children = [self.b, self.c]
        self.d.children = [self.e]
        self.b.parent = self.d
        assert list(self.a.children) == [
            self.c
        ], f"Node a children, expected {[self.c]}, received {self.a.children}"
        assert list(self.d.children) == [
            self.e,
            self.b,
        ], f"Node d children, expected {[self.e, self.b]}, received {self.d.children}"
        assert (
            self.b.parent == self.d
        ), f"Node b parent, expected {self.d}, received {self.b.parent}"

    def test_set_parent_duplicate(self):
        self.b.parent = self.a
        self.b.parent = self.a
        assert list(self.a.children) == [self.b]
        assert self.b.parent == self.a

    def test_set_parent_duplicate_constructor(self):
        self.a = basenode.BaseNode(name="a", age=90)
        self.b = basenode.BaseNode(name="b", age=65, parent=self.a)
        self.b.parent = self.a
        assert list(self.a.children) == [self.b]
        assert self.b.parent == self.a

    def test_set_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_append(self):
        self.a.children = [self.b]
        self.b.children = [self.d]
        self.e.children = [self.g, self.h]
        self.a.append(self.c)
        self.b.append(self.e)
        self.c.append(self.f)

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_extend(self):
        self.a.children = [self.b]
        self.b.children = [self.d]
        self.c.children = [self.f]

        self.a.extend([self.c])
        self.b.extend([self.e])
        self.e.extend([self.g, self.h])

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_sort(self):
        self.a.children = [self.c, self.b]
        self.b.children = [self.e, self.d]
        self.c.children = [self.f]
        self.e.children = [self.h, self.g]

        self.a.sort(key=lambda x: x.name)
        self.b.sort(key=lambda x: x.name)
        self.e.sort(key=lambda x: x.name)
        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_constructor(self):
        self.h = basenode.BaseNode(name="h", age=6)
        self.g = basenode.BaseNode(name="g", age=10)
        self.f = basenode.BaseNode(name="f", age=38)
        self.e = basenode.BaseNode(name="e", age=35, children=[self.g, self.h])
        self.d = basenode.BaseNode(name="d", age=40)
        self.c = basenode.BaseNode(name="c", age=60, children=[self.f])
        self.b = basenode.BaseNode(name="b", age=65, children=[self.d, self.e])
        self.a = basenode.BaseNode(name="a", age=90, children=[self.b, self.c])

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_null_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

        dummy = basenode.BaseNode()
        self.h.children = [dummy]
        assert dummy.parent == self.h
        self.h.children = []

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_null_parent(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

        dummy = basenode.BaseNode()
        self.h.children = [dummy]
        assert dummy.parent == self.h
        dummy.parent.children = []

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_none_parent_error(self):
        children = None
        with pytest.raises(TypeError) as exc_info:
            self.h.children = children
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE.format(
            type="List or Tuple or Set", input_type=type(children)
        )

    def test_set_children_reassign(self):
        self.a.children = [self.c]
        self.b.parent = self.a
        self.d.children = [self.e, self.b]
        assert list(self.a.children) == [
            self.c
        ], f"Node a children, expected {[self.c]}, received {self.a.children}"
        assert list(self.d.children) == [
            self.e,
            self.b,
        ], f"Node d children, expected {[self.e, self.b]}, received {self.d.children}"
        assert (
            self.b.parent == self.d
        ), f"Node b parent, expected {self.d}, received {self.b.parent}"

    def test_set_children_duplicate(self):
        self.a.children = [self.b]
        self.a.children = [self.b]
        assert list(self.a.children) == [self.b]
        assert self.b.parent == self.a

    def test_set_children_duplicate_constructor(self):
        self.a = basenode.BaseNode(children=[self.b])
        self.a.children = [self.b]
        assert list(self.a.children) == [self.b]
        assert self.b.parent == self.a

    def test_deep_copy_set_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

        a2 = self.a.copy()
        assert (
            len(a2.children) == 2
        ), f"Expected 2 children, received {len(a2.children)}"
        assert (
            not a2.children[0] == self.b and not a2.children[1] == self.b
        ), "Copy does not copy child nodes"
        assert not a2.children == [self.b, self.c], "Copy does not copy child nodes"
        assert_tree_structure_basenode_root(a2)
        assert_tree_structure_basenode_root_attr(a2)

    def test_shallow_copy_set_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

        a2 = copy.copy(self.a)
        assert (
            len(a2.children) == 2
        ), f"Expected 2 children, received {len(a2.children)}"
        assert (
            a2.children[0] == self.b or a2.children[1] == self.b
        ), "Shallow copy does not copy child nodes"
        assert a2.children == (self.b, self.c), "Shallow copy does not copy child nodes"
        assert_tree_structure_basenode_root(a2)
        assert_tree_structure_basenode_root_attr(a2)

    def test_set_parent_type_error(self):
        parent = 1
        with pytest.raises(TypeError) as exc_info:
            self.a.parent = parent
        assert str(exc_info.value) == Constants.ERROR_NODE_PARENT_TYPE_NONE.format(
            type="BaseNode", input_type=type(parent)
        )

    def test_set_parent_loop_error(self):
        with pytest.raises(exceptions.LoopError) as exc_info:
            self.a.parent = self.a
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_PARENT

        with pytest.raises(exceptions.LoopError) as exc_info:
            self.b.parent = self.a
            self.c.parent = self.b
            self.a.parent = self.c
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_ANCESTOR

    def test_set_children_mutable_list(self):
        children_list = [self.b, self.c, self.d]
        self.a.children = children_list
        children_list.pop()
        actual_children = self.a.children
        expected_children = (self.b, self.c, self.d)
        assert (
            actual_children == expected_children
        ), f"Expected {expected_children}, Received {actual_children}"

    def test_set_children_iterable(self):
        self.a.children = (self.b, self.c)
        self.b.children = [self.d, self.e]
        self.c.children = {self.f}
        self.e.children = (self.g, self.h)

        assert_tree_structure_basenode_root(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_type_error(self):
        children = 1
        with pytest.raises(TypeError) as exc_info:
            self.a.children = [self.b, children]
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE.format(
            type="BaseNode", input_type=type(children)
        )

        children = None
        with pytest.raises(TypeError) as exc_info:
            self.a.children = [self.b, children]
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE.format(
            type="BaseNode", input_type=type(children)
        )

    def test_set_children_loop_error(self):
        with pytest.raises(exceptions.LoopError) as exc_info:
            self.a.children = [self.b, self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_CHILD

        with pytest.raises(exceptions.LoopError) as exc_info:
            self.a.children = [self.b, self.c]
            self.c.children = [self.d, self.e, self.f]
            self.f.children = [self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_DESCENDANT

    def test_set_duplicate_children_error(self):
        with pytest.raises(exceptions.TreeError) as exc_info:
            self.a.children = [self.b, self.b]
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_CHILD

    def test_rollback_set_parent(self):
        a = helper.clone_tree(self.a, BaseNode2)
        b = helper.clone_tree(self.b, BaseNode2)
        c = helper.clone_tree(self.c, BaseNode2)
        d = helper.clone_tree(self.d, BaseNode2)
        e = helper.clone_tree(self.e, BaseNode2)
        f = helper.clone_tree(self.f, BaseNode2)
        g = helper.clone_tree(self.g, BaseNode2)
        h = helper.clone_tree(self.h, BaseNode2)
        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        a.set_attrs({"val": 1})
        with pytest.raises(exceptions.TreeError) as exc_info:
            f.parent = a
        assert str(exc_info.value).startswith("Custom error assigning parent, ")

        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        assert not d.parent, f"Expected Node d parent to be None, received {d.parent}"
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_parent_no_parent(self):
        a = helper.clone_tree(self.a, BaseNode2)
        b = helper.clone_tree(self.b, BaseNode2)
        c = helper.clone_tree(self.c, BaseNode2)
        d = helper.clone_tree(self.d, BaseNode2)
        e = helper.clone_tree(self.e, BaseNode2)
        f = helper.clone_tree(self.f, BaseNode2)
        g = helper.clone_tree(self.g, BaseNode2)
        h = helper.clone_tree(self.h, BaseNode2)
        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        a.set_attrs({"val": 1})
        with pytest.raises(exceptions.TreeError) as exc_info:
            d.parent = a
        assert str(exc_info.value).startswith("Custom error assigning parent, ")

        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        assert not d.parent, f"Expected Node d parent to be None, received {d.parent}"
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_parent_null_parent(self):
        a = helper.clone_tree(self.a, BaseNode2)
        b = helper.clone_tree(self.b, BaseNode2)
        c = helper.clone_tree(self.c, BaseNode2)
        d = helper.clone_tree(self.d, BaseNode2)
        e = helper.clone_tree(self.e, BaseNode2)
        f = helper.clone_tree(self.f, BaseNode2)
        g = helper.clone_tree(self.g, BaseNode2)
        h = helper.clone_tree(self.h, BaseNode2)
        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        d.set_attrs({"val": 1})
        with pytest.raises(exceptions.TreeError) as exc_info:
            d.parent = None
        assert str(exc_info.value) == "Custom error assigning parent"

        expected_a_children = [b, c]
        expected_h_children = [e, f, g]
        assert not d.parent, f"Expected Node d parent to be None, received {d.parent}"
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_parent_reassign(self):
        a = helper.clone_tree(self.a, BaseNode2)
        b = helper.clone_tree(self.b, BaseNode2)
        c = helper.clone_tree(self.c, BaseNode2)
        d = helper.clone_tree(self.d, BaseNode2)
        e = helper.clone_tree(self.e, BaseNode2)
        f = helper.clone_tree(self.f, BaseNode2)
        g = helper.clone_tree(self.g, BaseNode2)
        h = helper.clone_tree(self.h, BaseNode2)
        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        a.set_attrs({"val": 1})
        with pytest.raises(exceptions.TreeError) as exc_info:
            b.parent = a
        assert str(exc_info.value).startswith("Custom error assigning parent, ")

        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_children(self):
        a = helper.clone_tree(self.a, BaseNode3)
        b = helper.clone_tree(self.b, BaseNode3)
        c = helper.clone_tree(self.c, BaseNode3)
        d = helper.clone_tree(self.d, BaseNode3)
        e = helper.clone_tree(self.e, BaseNode3)
        f = helper.clone_tree(self.f, BaseNode3)
        g = helper.clone_tree(self.g, BaseNode3)
        h = helper.clone_tree(self.h, BaseNode3)
        i = BaseNode3(name="i")
        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        g.set_attrs({"val": 1})
        with pytest.raises(exceptions.TreeError) as exc_info:
            a.children = [b, c, d, g, i, f]
        assert str(exc_info.value).startswith("Custom error assigning children, ")
        assert not i.parent, f"Node i parent, expected {None}, received {i.parent}"

        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_children_null_children(self):
        a = helper.clone_tree(self.a, BaseNode3)
        b = helper.clone_tree(self.b, BaseNode3)
        c = helper.clone_tree(self.c, BaseNode3)
        d = helper.clone_tree(self.d, BaseNode3)
        e = helper.clone_tree(self.e, BaseNode3)
        f = helper.clone_tree(self.f, BaseNode3)
        g = helper.clone_tree(self.g, BaseNode3)
        h = helper.clone_tree(self.h, BaseNode3)
        i = BaseNode3(name="i")
        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        a.set_attrs({"val": 1})
        with pytest.raises(exceptions.TreeError) as exc_info:
            a.children = []
        assert str(exc_info.value) == "Custom error assigning children"
        assert not i.parent, f"Node i parent, expected {None}, received {i.parent}"

        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_children_reassign(self):
        a = helper.clone_tree(self.a, BaseNode3)
        b = helper.clone_tree(self.b, BaseNode3)
        c = helper.clone_tree(self.c, BaseNode3)
        d = helper.clone_tree(self.d, BaseNode3)
        e = helper.clone_tree(self.e, BaseNode3)
        f = helper.clone_tree(self.f, BaseNode3)
        g = helper.clone_tree(self.g, BaseNode3)
        h = helper.clone_tree(self.h, BaseNode3)
        i = BaseNode3(name="i")
        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        a.children = expected_a_children
        h.children = expected_h_children
        b.set_attrs({"val": 1})
        with pytest.raises(exceptions.TreeError) as exc_info:
            a.children = [b, c, d]
        assert str(exc_info.value).startswith("Custom error assigning children, ")
        assert not i.parent, f"Node i parent, expected {None}, received {i.parent}"

        expected_a_children = [b, c, d]
        expected_h_children = [e, f, g]
        for parent, children in zip([a, h], [expected_a_children, expected_h_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_plot(self):
        self.a.children = [self.b, self.c]
        fig = self.a.plot()
        assert isinstance(fig, plt.Figure)

    def test_plot_with_reingold_tilford(self):
        from bigtree.utils.plot import reingold_tilford

        self.a.children = [self.b, self.c]
        reingold_tilford(self.a)
        fig = self.a.plot()
        assert isinstance(fig, plt.Figure)


def assert_tree_structure_basenode_root(root):
    """Test tree structure (i.e., ancestors, descendants, leaves, siblings, etc.)"""
    # Test ancestors
    expected = 0
    actual = len(list(root.ancestors))
    assert (
        actual == expected
    ), f"Node {root} should have {expected} ancestors, but it has {actual} ancestors"

    # Test descendants
    expected = 7
    actual = len(list(root.descendants))
    assert (
        actual == expected
    ), f"Node {root} should have {expected} descendants, but it has {actual} descendants"

    # Test leaves
    expected = 4
    actual = len(list(root.leaves))
    assert (
        actual == expected
    ), f"Node {root} should have {expected} leaves, but it has {actual} leaves"

    # Test siblings
    expected = ()
    actual = root.siblings
    assert (
        actual == expected
    ), f"Node {root} should have {expected} siblings, but it has {actual} siblings"

    # Test left_sibling
    expected = None
    actual = root.left_sibling
    assert (
        actual == expected
    ), f"Node {root} should have {expected} left sibling, but it has {actual} left sibling"

    # Test right_sibling
    expected = None
    actual = root.right_sibling
    assert (
        actual == expected
    ), f"Node {root} should have {expected} right sibling, but it has {actual} right sibling"

    # Test node_path
    expected = 1
    actual = len(list(root.node_path))
    assert (
        actual == expected
    ), f"Node {root} should have {expected} nodes in node path, but it has {actual} nodes"

    # Test is_root
    expected = True
    actual = root.is_root
    assert (
        actual == expected
    ), f"Node {root} is_root should be {expected}, but it is {actual}"

    # Test is_leaf
    expected = False
    actual = root.is_leaf
    assert (
        actual == expected
    ), f"Node {root} is_leaf should be {expected}, but it is {actual}"

    # Test root
    expected = root
    actual = root.root
    assert (
        actual == expected
    ), f"Node {root} root should be {expected}, but it is {actual}"

    # Test depth
    expected = 1
    actual = root.depth
    assert (
        actual == expected
    ), f"Node {root} should be nested to {expected} levels, but it has {actual} levels"

    # Test max_depth
    expected = 4
    actual = root.max_depth
    assert (
        actual == expected
    ), f"Node {root} max_depth should be {expected}, but it is {actual}"

    # Test get_attr()
    expected = "a"
    actual = root.get_attr("name")
    assert (
        actual == expected
    ), f"Node attribute should be {expected}, but it is {actual}"

    expected = None
    actual = root.get_attr("something")
    assert (
        actual == expected
    ), f"Node attribute should be {expected}, but it is {actual}"


def assert_tree_structure_basenode_root_attr(
    root,
    a=("a", 90),
    b=("b", 65),
    c=("c", 60),
    d=("d", 40),
    e=("e", 35),
    f=("f", 38),
    g=("g", 10),
    h=("h", 6),
):
    """Test tree structure with age attributes"""
    # Test describe()
    expected = {("age", a[1]), ("name", a[0])}
    actual = set(root.describe(exclude_prefix="_"))
    assert (
        actual == expected
    ), f"Node description should be {expected}, but it is {actual}"

    # Test age attribute
    expected_attrs = [a, b, d, e, g, h, c, f]
    for node, expected in zip(iterators.preorder_iter(root), expected_attrs):
        actual = node.get_attr("name"), node.get_attr("age")
        assert (
            actual == expected
        ), f"Node name and age should be {expected}, but it is {actual}"


def assert_tree_structure_customnode_root_attr(
    root,
    a=("a", 90),
    b=("b", 65),
    c=("c", 60),
    d=("d", 40),
    e=("e", 35),
    f=("f", 38),
    g=("g", 10),
    h=("h", 6),
):
    """Test tree structure with age attributes"""
    # Test describe()
    expected = {("custom_field", a[1]), ("custom_field_str", a[0]), ("name", a[0])}
    actual = set(root.describe(exclude_prefix="_"))
    assert (
        actual == expected
    ), f"Node description should be {expected}, but it is {actual}"

    # Test age attribute
    expected_attrs = [a, b, d, e, g, h, c, f]
    for node, expected in zip(iterators.preorder_iter(root), expected_attrs):
        actual = node.get_attr("custom_field_str"), node.get_attr("custom_field")
        assert (
            actual == expected
        ), f"Node custom_field_str and custom_field should be {expected}, but it is {actual}"


def assert_tree_structure_basenode_self(self):
    """Test tree structure with self object"""
    nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

    # Test iteration (__iter__)
    expected = [self.b, self.c]
    actual = [child for child in self.a]
    assert (
        actual == expected
    ), f"Node {self.a} should have {expected} children when iterated, but it has {actual}"

    # Test contains (__contains__)
    assert self.b in self.a, f"Check if {self.a} contains {self.b}, expected True"
    assert self.d not in self.a, f"Check if {self.a} contains {self.d}, expected False"

    # Test ancestors
    expected_ans = [0, 1, 1, 2, 2, 2, 3, 3]
    for node, expected in zip(nodes, expected_ans):
        actual = len(list(node.ancestors))
        assert (
            actual == expected
        ), f"Node {node} should have {expected} ancestors, but it has {actual} ancestors"

    # Test descendants
    expected_ans = [7, 4, 1, 0, 2, 0, 0, 0]
    for node, expected in zip(nodes, expected_ans):
        actual = len(list(node.descendants))
        assert (
            actual == expected
        ), f"Node {node} should have {expected} descendants, but it has {actual} descendants"

    # Test leaves
    expected_ans = [4, 3, 1, 1, 2, 1, 1, 1]
    for node, expected in zip(nodes, expected_ans):
        actual = len(list(node.leaves))
        assert (
            actual == expected
        ), f"Node {node} should have {expected} leaves, but it has {actual} leaves"

    # Test siblings
    expected_ans = [
        (),
        (self.c,),
        (self.b,),
        (self.e,),
        (self.d,),
        (),
        (self.h,),
        (self.g,),
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = node.siblings
        assert (
            actual == expected
        ), f"Node {node} should have {expected} siblings, but it has {actual} siblings"

    # Test left_sibling
    expected_ans = [None, None, self.b, None, self.d, None, None, self.g]
    for node, expected in zip(nodes, expected_ans):
        actual = node.left_sibling
        assert (
            actual == expected
        ), f"Node {node} should have {expected} left sibling, but it has {actual} left sibling"

    # Test right_sibling
    expected_ans = [None, self.c, None, self.e, None, None, self.h, None]
    for node, expected in zip(nodes, expected_ans):
        actual = node.right_sibling
        assert (
            actual == expected
        ), f"Node {node} should have {expected} right sibling, but it has {actual} right sibling"

    # Test node_path
    expected_ans = [1, 2, 2, 3, 3, 3, 4, 4]
    for node, expected in zip(nodes, expected_ans):
        actual = len(list(node.node_path))
        assert (
            actual == expected
        ), f"Node {node} should have {expected} nodes in node path, but it has {actual} nodes"

    # Test is_root
    expected_ans = [True, False, False, False, False, False, False, False]
    for node, expected in zip(nodes, expected_ans):
        actual = node.is_root
        assert (
            actual == expected
        ), f"Node {node} is_root should be {expected}, but it is {actual}"

    # Test is_leaf
    expected_ans = [False, False, False, True, False, True, True, True]
    for node, expected in zip(nodes, expected_ans):
        actual = node.is_leaf
        assert (
            actual == expected
        ), f"Node {node} is_leaf should be {expected}, but it is {actual}"

    # Test root
    for node in nodes:
        actual = node.root
        assert (
            actual == nodes[0]
        ), f"Node {node} root should be {expected}, but it is {actual}"

    # Test diameter
    expected_ans = [5, 3, 1, 0, 2, 0, 0, 0]
    for node, expected in zip(nodes, expected_ans):
        actual = node.diameter
        assert (
            actual == expected
        ), f"Node {node} diameter should be {expected}, but it is {actual}"

    # Test depth
    expected_ans = [1, 2, 2, 3, 3, 3, 4, 4]
    for node, expected in zip(nodes, expected_ans):
        actual = node.depth
        assert (
            actual == expected
        ), f"Node {node} should be nested to {expected} levels, but it has {actual} levels"

    # Test max_depth
    expected = 4
    for node in nodes:
        actual = node.max_depth
        assert (
            actual == expected
        ), f"Node {node} max_depth should be {expected}, but it is {actual}"

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

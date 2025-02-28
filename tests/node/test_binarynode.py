import unittest

import pytest

from bigtree.node import basenode, binarynode, node
from bigtree.tree import export, helper
from bigtree.utils import exceptions
from tests.conftest import assert_print_statement
from tests.test_constants import Constants


class BinaryNode2(binarynode.BinaryNode):
    def _BinaryNode__post_assign_parent(self, new_parent):
        if new_parent is not None:
            if new_parent.val == 100:
                raise Exception(
                    f"Custom error assigning parent, new parent {new_parent} and children are {new_parent.children}"
                )
        elif self.val == 100:
            raise Exception("Custom error assigning parent")


class BinaryNode3(binarynode.BinaryNode):
    def _BinaryNode__post_assign_children(self, new_children):
        if self.val == 100:
            raise Exception("Custom error assigning children")
        for child in new_children:
            if child and child.val == 100:
                raise Exception(
                    f"Custom error assigning children, new children {new_children}"
                )


class TestBinaryNode(unittest.TestCase):
    def setUp(self):
        self.a = binarynode.BinaryNode(1)
        self.b = binarynode.BinaryNode(2)
        self.c = binarynode.BinaryNode(3)
        self.d = binarynode.BinaryNode(4)
        self.e = binarynode.BinaryNode(5)
        self.f = binarynode.BinaryNode(6)
        self.g = binarynode.BinaryNode(7)
        self.h = binarynode.BinaryNode(8)

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
        self.a = binarynode.BinaryNode.from_dict({"name": 1})
        self.b = binarynode.BinaryNode.from_dict({"name": 2})
        self.c = binarynode.BinaryNode.from_dict({"name": 3})
        self.d = binarynode.BinaryNode.from_dict({"name": 4})
        self.e = binarynode.BinaryNode.from_dict({"name": 5})
        self.f = binarynode.BinaryNode.from_dict({"name": 6})
        self.g = binarynode.BinaryNode.from_dict({"name": 7})
        self.h = binarynode.BinaryNode.from_dict({"name": 8})

        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.c.children = []
        self.c.left = self.f
        self.g.parent = self.c
        self.d.children = []
        self.d.children = [None, self.h]

        assert_binarytree_structure_self(self)
        assert_print_statement(print, "BinaryNode(name=1, val=1)\n", self.a)
        assert (
            self.a.node_name == "1"
        ), f"Node name is wrong, expected 1, received {self.a.node_name}"
        assert (
            self.a.val == 1
        ), f"Node val is wrong, expected 1, received {self.a.node_name}"
        self.h.children = []
        assert not self.h.left, f"Expected {None}, received {self.h.left}"
        assert not self.h.right, f"Expected {None}, received {self.h.right}"
        self.a.sep = "\\"
        assert (
            self.b.path_name == "\\1\\2"
        ), f"Expected \\1\\2, received {self.b.path_name}"

    def test_from_dict_str(self):
        self.a = binarynode.BinaryNode.from_dict({"name": "abc"})
        self.b = binarynode.BinaryNode.from_dict({"name": "2"})
        self.c = binarynode.BinaryNode.from_dict({"name": "3"})
        self.d = binarynode.BinaryNode.from_dict({"name": "4"})
        self.e = binarynode.BinaryNode.from_dict({"name": "5"})
        self.f = binarynode.BinaryNode.from_dict({"name": "6"})
        self.g = binarynode.BinaryNode.from_dict({"name": "7"})
        self.h = binarynode.BinaryNode.from_dict({"name": "8"})

        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.c.children = []
        self.c.left = self.f
        self.g.parent = self.c
        self.d.children = []
        self.d.children = [None, self.h]

        assert_print_statement(print, "BinaryNode(name=abc, val=abc)\n", self.a)
        assert (
            self.a.node_name == "abc"
        ), f"Node name is wrong, expected abc, received {self.a.node_name}"
        assert (
            self.a.val == "abc"
        ), f"Node val is wrong, expected abc, received {self.a.node_name}"
        self.h.children = []
        assert not self.h.left, f"Expected {None}, received {self.h.left}"
        assert not self.h.right, f"Expected {None}, received {self.h.right}"
        self.a.sep = "\\"
        assert (
            self.b.path_name == "\\abc\\2"
        ), f"Expected \\abc\\2, received {self.b.path_name}"

    def test_set_parents_error(self):
        with pytest.raises(AttributeError) as exc_info:
            self.b.parents = [self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_SET_PARENTS_ATTR

        with pytest.raises(AttributeError) as exc_info:
            self.b = binarynode.BinaryNode(1, parents=[self.a])
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
        self.g.parent = self.c
        self.d.children = [None, self.h]

        assert_binarytree_structure_self(self)

    def test_set_parent_3_parent_error(self):
        self.b.parent = self.a
        self.c.parent = self.a
        with pytest.raises(exceptions.TreeError) as exc_info:
            self.d.parent = self.a
        assert str(exc_info.value).endswith("already has 2 children")

    def test_set_parent_children_insert(self):
        self.a.children = [None, None]
        self.b.parent = self.a
        self.c.parent = self.a
        self.b.children = [self.d, None]
        self.e.parent = self.b
        self.c.children = [None, self.g]
        self.f.parent = self.c
        self.d.children = [None, self.h]

        assert_binarytree_structure_self(self)

    def test_set_parent_sort(self):
        self.c.parent = self.a
        self.b.parent = self.a
        self.e.parent = self.b
        self.d.parent = self.b
        self.g.parent = self.c
        self.f.parent = self.c
        self.d.children = [None, self.h]

        self.a.sort(key=lambda x: x.val)
        self.b.sort(key=lambda x: x.val)
        self.c.sort(key=lambda x: x.val)
        self.d.sort(key=lambda x: x.val)
        self.e.sort(key=lambda x: x.val)
        self.f.sort(key=lambda x: x.val)
        self.g.sort(key=lambda x: x.val)
        self.h.sort(key=lambda x: x.val)
        assert_binarytree_structure_self(self)

    def test_set_parent_rshift(self):
        self.a >> self.b
        self.a >> self.c
        self.b >> self.d
        self.b >> self.e
        self.c >> self.f
        self.c >> self.g
        self.d.children = [None, self.h]

        assert_binarytree_structure_self(self)

    def test_set_parent_lshift(self):
        self.b << self.a
        self.c << self.a
        self.d << self.b
        self.e << self.b
        self.f << self.c
        self.g << self.c
        self.d.children = [None, self.h]

        assert_binarytree_structure_self(self)

    def test_set_parent_constructor(self):
        self.a = binarynode.BinaryNode(1)
        self.b = binarynode.BinaryNode(2, parent=self.a)
        self.c = binarynode.BinaryNode(3, parent=self.a)
        self.d = binarynode.BinaryNode(4, parent=self.b)
        self.e = binarynode.BinaryNode(5, parent=self.b)
        self.f = binarynode.BinaryNode(6, parent=self.c)
        self.g = binarynode.BinaryNode(7, parent=self.c)
        self.h = binarynode.BinaryNode(8)
        self.d.children = [None, self.h]

        assert_binarytree_structure_self(self)

    def test_set_parent_null_parent(self):
        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.f.parent = self.c
        self.g.parent = self.c
        self.d.children = [None, self.h]

        dummy = binarynode.BinaryNode(100)
        dummy.parent = self.h
        assert list(self.h.children) == [dummy, None]

        dummy.parent = None
        assert_binarytree_structure_self(self)

    def test_set_parent_reassign(self):
        self.a.children = [self.b, self.c]
        self.b.parent = self.d
        assert not self.a.left, f"Node a left, expected None, received {self.a.left}"
        assert (
            self.a.right == self.c
        ), f"Node a right, expected {self.c}, received {self.a.right}"
        assert (
            self.d.left == self.b
        ), f"Node d left, expected {self.b}, received {self.d.left}"
        assert not self.d.right, f"Node d right, expected None, received {self.d.right}"

    def test_set_parent_reassign_right(self):
        self.a.children = [self.b, self.c]
        self.e.parent = self.d
        self.b.parent = self.d
        assert not self.a.left, f"Node a left, expected None, received {self.a.left}"
        assert (
            self.a.right == self.c
        ), f"Node a right, expected {self.c}, received {self.a.right}"
        assert (
            self.d.left == self.e
        ), f"Node d left, expected {self.e}, received {self.d.left}"
        assert (
            self.d.right == self.b
        ), f"Node d right, expected {self.b}, received {self.d.right}"

    def test_set_parent_duplicate(self):
        self.b.parent = self.a
        self.b.parent = self.a
        assert list(self.a.children) == [self.b, None]
        assert self.b.parent == self.a

    def test_set_parent_duplicate_constructor(self):
        self.a = binarynode.BinaryNode(1)
        self.b = binarynode.BinaryNode(2, parent=self.a)
        self.b.parent = self.a
        assert list(self.a.children) == [self.b, None]
        assert self.b.parent == self.a

    def test_set_left_and_right(self):
        self.a.left = self.b
        self.a.right = self.c
        self.b.left = self.d
        self.b.right = self.e
        self.c.left = self.f
        self.c.right = self.g
        self.d.right = self.h

        assert_binarytree_structure_self(self)

    def test_set_left_and_right_constructor(self):
        self.h = binarynode.BinaryNode(8)
        self.g = binarynode.BinaryNode(7)
        self.f = binarynode.BinaryNode(6)
        self.e = binarynode.BinaryNode(5)
        self.d = binarynode.BinaryNode(4, right=self.h)
        self.c = binarynode.BinaryNode(3, left=self.f, right=self.g)
        self.b = binarynode.BinaryNode(2, left=self.d, right=self.e)
        self.a = binarynode.BinaryNode(1, left=self.b, right=self.c)

        assert_binarytree_structure_self(self)

    def test_set_left_and_right_and_children_constructor(self):
        self.h = binarynode.BinaryNode(8)
        self.g = binarynode.BinaryNode(7)
        self.f = binarynode.BinaryNode(6)
        self.e = binarynode.BinaryNode(5)
        self.d = binarynode.BinaryNode(4, right=self.h, children=[None, self.h])
        self.c = binarynode.BinaryNode(
            3, left=self.f, right=self.g, children=[self.f, self.g]
        )
        self.b = binarynode.BinaryNode(
            2, left=self.d, right=self.e, children=[self.d, self.e]
        )
        self.a = binarynode.BinaryNode(
            1, left=self.b, right=self.c, children=[self.b, self.c]
        )

        assert_binarytree_structure_self(self)

    def test_set_left_and_right_and_children_constructor_error(self):
        with pytest.raises(ValueError) as exc_info:
            self.a = binarynode.BinaryNode(
                1, left=self.b, right=self.c, children=[self.c]
            )
        assert str(exc_info.value) == Constants.ERROR_BINARYNODE_CHILDREN_LENGTH

        left = self.b
        right = self.c
        children = [self.d, self.c]
        with pytest.raises(ValueError) as exc_info:
            self.a = binarynode.BinaryNode(1, left=left, right=right, children=children)
        assert str(exc_info.value) == Constants.ERROR_BINARYNODE_LEFT_CHILDREN.format(
            left=left, children=children
        )

        left = self.b
        right = self.c
        children = [self.b, self.d]
        with pytest.raises(ValueError) as exc_info:
            self.a = binarynode.BinaryNode(1, left=left, right=right, children=children)
        assert str(exc_info.value) == Constants.ERROR_BINARYNODE_RIGHT_CHILDREN.format(
            right=right, children=children
        )

    def test_set_left_and_right_duplicate(self):
        self.a = binarynode.BinaryNode(1, left=self.b, right=self.c)
        self.a.left = self.b
        self.a.right = self.c
        assert list(self.a.children) == [self.b, self.c]
        assert self.b.parent == self.a
        assert self.c.parent == self.a

    def test_set_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f, self.g]
        self.d.children = [None, self.h]

        assert_binarytree_structure_self(self)

    def test_set_children_3_children_error(self):
        with pytest.raises(ValueError) as exc_info:
            self.a.children = [self.b, self.c, self.d]
        assert str(exc_info.value) == Constants.ERROR_BINARYNODE_CHILDREN_LENGTH

    def test_set_children_sort(self):
        self.a.children = [self.c, self.b]
        self.b.children = [self.e, self.d]
        self.c.children = [self.g, self.f]
        self.d.children = [None, self.h]

        self.a.sort(key=lambda x: x.val)
        self.b.sort(key=lambda x: x.val)
        self.c.sort(key=lambda x: x.val)
        self.d.sort(key=lambda x: x.val)
        self.e.sort(key=lambda x: x.val)
        self.f.sort(key=lambda x: x.val)
        self.g.sort(key=lambda x: x.val)
        self.h.sort(key=lambda x: x.val)
        assert_binarytree_structure_self(self)

    def test_set_children_constructor(self):
        self.h = binarynode.BinaryNode(8)
        self.g = binarynode.BinaryNode(7)
        self.f = binarynode.BinaryNode(6)
        self.e = binarynode.BinaryNode(5)
        self.d = binarynode.BinaryNode(4, children=[None, self.h])
        self.c = binarynode.BinaryNode(3, children=[self.f, self.g])
        self.b = binarynode.BinaryNode(2, children=[self.d, self.e])
        self.a = binarynode.BinaryNode(1, children=[self.b, self.c])

        assert_binarytree_structure_self(self)

    def test_set_children_null_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f, self.g]
        self.d.children = [None, self.h]

        dummy = binarynode.BinaryNode(100)
        self.h.children = [dummy, None]
        assert dummy.parent == self.h
        self.h.children = []

        assert_binarytree_structure_self(self)

    def test_set_children_null_parent(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f, self.g]
        self.d.children = [None, self.h]

        dummy = binarynode.BinaryNode(100)
        self.h.children = [dummy, None]
        assert dummy.parent == self.h
        dummy.parent.children = []

        assert_binarytree_structure_self(self)

    def test_set_children_none_parent_error(self):
        children = None
        with pytest.raises(TypeError) as exc_info:
            self.h.children = children
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE.format(
            type="List or Tuple or Set", input_type=type(children)
        )

    def test_set_children_reassign(self):
        self.a.children = [self.b, self.c]
        self.d.children = [self.b, None]
        assert not self.a.left, f"Node a left, expected None, received {self.a.left}"
        assert (
            self.a.right == self.c
        ), f"Node a right, expected {self.c}, received {self.a.right}"
        assert (
            self.d.left == self.b
        ), f"Node d left, expected {self.b}, received {self.d.left}"
        assert not self.d.right, f"Node d right, expected None, received {self.d.right}"

    def test_set_children_reassign_right(self):
        self.a.children = [self.b, self.c]
        self.d.children = [self.e, self.b]
        assert not self.a.left, f"Node a left, expected None, received {self.a.left}"
        assert (
            self.a.right == self.c
        ), f"Node a right, expected {self.c}, received {self.a.right}"
        assert (
            self.d.left == self.e
        ), f"Node d left, expected {self.e}, received {self.d.left}"
        assert (
            self.d.right == self.b
        ), f"Node d right, expected {self.b}, received {self.d.right}"

    def test_set_children_duplicate(self):
        self.a.children = [self.b, None]
        self.a.children = [self.b, None]
        assert list(self.a.children) == [self.b, None]
        assert self.b.parent == self.a

    def test_set_children_duplicate_constructor(self):
        self.a = binarynode.BinaryNode(1, children=[self.b, None])
        self.a.children = [self.b, None]
        assert list(self.a.children) == [self.b, None]
        assert self.b.parent == self.a

    def test_deep_copy_set_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f, self.g]
        self.d.children = [None, self.h]

        a2 = self.a.copy()
        assert (
            len(a2.children) == 2
        ), f"Expected 2 children, received {len(a2.children)}"
        assert (
            not a2.children[0] == self.b and not a2.children[1] == self.b
        ), "Copy does not copy child nodes"
        assert not a2.children == [self.b, self.c], "Copy does not copy child nodes"
        assert_binarytree_structure_root(a2)

    def test_set_parent_type_error(self):
        parent = 1
        with pytest.raises(TypeError) as exc_info:
            self.a.parent = parent
        assert str(exc_info.value) == Constants.ERROR_NODE_PARENT_TYPE_NONE.format(
            type="BinaryNode", input_type=type(parent)
        )

        parent = basenode.BaseNode()
        with pytest.raises(TypeError) as exc_info:
            self.a.parent = parent
        assert str(exc_info.value) == Constants.ERROR_NODE_PARENT_TYPE_NONE.format(
            type="BinaryNode", input_type=type(parent)
        )

        parent = node.Node("a")
        with pytest.raises(TypeError) as exc_info:
            self.a.parent = parent
        assert str(exc_info.value) == Constants.ERROR_NODE_PARENT_TYPE_NONE.format(
            type="BinaryNode", input_type=type(parent)
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

    def test_set_children_type_error(self):
        children = self.b
        with pytest.raises(TypeError) as exc_info:
            self.a.children = children
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE.format(
            type="List or Tuple or Set", input_type=type(children)
        )

        children = 1
        with pytest.raises(TypeError) as exc_info:
            self.a.children = [self.b, children]
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE_NONE.format(
            type="BinaryNode", input_type=type(children)
        )

        children = basenode.BaseNode()
        with pytest.raises(TypeError) as exc_info:
            self.a.children = [children, None]
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE_NONE.format(
            type="BinaryNode", input_type=type(children)
        )

        children = node.Node("a")
        with pytest.raises(TypeError) as exc_info:
            self.a.children = [children, None]
        assert str(exc_info.value) == Constants.ERROR_NODE_CHILDREN_TYPE_NONE.format(
            type="BinaryNode", input_type=type(children)
        )

    def test_set_children_length_error(self):
        with pytest.raises(ValueError) as exc_info:
            self.a.children = [self.b]
        assert str(exc_info.value) == Constants.ERROR_BINARYNODE_CHILDREN_LENGTH

    def test_set_children_loop_error(self):
        with pytest.raises(exceptions.LoopError) as exc_info:
            self.a.children = [self.b, self.a]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_CHILD

        with pytest.raises(exceptions.LoopError) as exc_info:
            self.a.children = [self.b, self.c]
            self.c.children = [self.d, self.e]
            self.e.children = [self.a, self.f]
        assert str(exc_info.value) == Constants.ERROR_NODE_LOOP_DESCENDANT

    def test_set_duplicate_children_error(self):
        with pytest.raises(exceptions.TreeError) as exc_info:
            self.a.children = [self.b, self.b]
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_CHILD

    def test_rollback_set_parent(self):
        a = helper.clone_tree(self.a, BinaryNode2)
        b = helper.clone_tree(self.b, BinaryNode2)
        c = helper.clone_tree(self.c, BinaryNode2)
        d = helper.clone_tree(self.d, BinaryNode2)
        e = helper.clone_tree(self.e, BinaryNode2)
        f = helper.clone_tree(self.f, BinaryNode2)
        expected_a_children = [None, c]
        expected_b_children = [d, e]
        expected_f_children = [None, b]
        a.children = expected_a_children
        b.children = expected_b_children
        f.children = expected_f_children
        a.val = 100
        with pytest.raises(exceptions.TreeError) as exc_info:
            b.parent = a
        assert str(exc_info.value).startswith("Custom error assigning parent, ")

        expected_a_children = [None, c]
        expected_b_children = [d, e]
        expected_f_children = [None, b]
        for parent, children in zip(
            [a, b, f], [expected_a_children, expected_b_children, expected_f_children]
        ):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_parent_no_parent(self):
        a = helper.clone_tree(self.a, BinaryNode2)
        b = helper.clone_tree(self.b, BinaryNode2)
        c = helper.clone_tree(self.c, BinaryNode2)
        d = helper.clone_tree(self.d, BinaryNode2)
        e = helper.clone_tree(self.e, BinaryNode2)
        f = helper.clone_tree(self.f, BinaryNode2)
        g = helper.clone_tree(self.g, BinaryNode2)
        expected_a_children = [None, c]
        expected_b_children = [d, e]
        expected_f_children = [None, b]
        a.children = expected_a_children
        b.children = expected_b_children
        f.children = expected_f_children
        a.val = 100
        with pytest.raises(exceptions.TreeError) as exc_info:
            g.parent = a
        assert str(exc_info.value).startswith("Custom error assigning parent, ")

        expected_a_children = [None, c]
        expected_b_children = [d, e]
        expected_f_children = [None, b]
        assert not g.parent, f"Node g parent, expected None, received {g.parent}"
        for parent, children in zip(
            [a, b, f], [expected_a_children, expected_b_children, expected_f_children]
        ):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_parent_null_parent(self):
        a = helper.clone_tree(self.a, BinaryNode2)
        b = helper.clone_tree(self.b, BinaryNode2)
        c = helper.clone_tree(self.c, BinaryNode2)
        d = helper.clone_tree(self.d, BinaryNode2)
        e = helper.clone_tree(self.e, BinaryNode2)
        f = helper.clone_tree(self.f, BinaryNode2)
        g = helper.clone_tree(self.g, BinaryNode2)
        expected_a_children = [None, c]
        expected_b_children = [d, e]
        expected_f_children = [None, b]
        a.children = expected_a_children
        b.children = expected_b_children
        f.children = expected_f_children
        g.val = 100
        with pytest.raises(exceptions.TreeError) as exc_info:
            g.parent = None
        assert str(exc_info.value) == "Custom error assigning parent"

        expected_a_children = [None, c]
        expected_b_children = [d, e]
        expected_f_children = [None, b]
        assert not g.parent, f"Node g parent, expected None, received {g.parent}"
        for parent, children in zip(
            [a, b, f], [expected_a_children, expected_b_children, expected_f_children]
        ):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_parent_reassign(self):
        a = helper.clone_tree(self.a, BinaryNode2)
        b = helper.clone_tree(self.b, BinaryNode2)
        c = helper.clone_tree(self.c, BinaryNode2)
        d = helper.clone_tree(self.d, BinaryNode2)
        e = helper.clone_tree(self.e, BinaryNode2)
        f = helper.clone_tree(self.f, BinaryNode2)
        expected_a_children = [None, c]
        expected_b_children = [d, e]
        expected_f_children = [None, b]
        a.children = expected_a_children
        b.children = expected_b_children
        f.children = expected_f_children
        a.val = 100
        with pytest.raises(exceptions.TreeError) as exc_info:
            c.parent = a
        assert str(exc_info.value).startswith("Custom error assigning parent, ")

        expected_a_children = [None, c]
        expected_b_children = [d, e]
        expected_f_children = [None, b]
        for parent, children in zip(
            [a, b, f], [expected_a_children, expected_b_children, expected_f_children]
        ):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_children(self):
        a = helper.clone_tree(self.a, BinaryNode3)
        b = helper.clone_tree(self.b, BinaryNode3)
        c = helper.clone_tree(self.c, BinaryNode3)
        d = helper.clone_tree(self.d, BinaryNode3)
        e = helper.clone_tree(self.e, BinaryNode3)
        f = helper.clone_tree(self.f, BinaryNode2)
        expected_a_children = [b, c]
        expected_b_children = [d, e]
        a.children = expected_a_children
        b.children = expected_b_children
        f.val = 100
        with pytest.raises(exceptions.TreeError) as exc_info:
            a.children = [d, f]
        assert str(exc_info.value).startswith("Custom error assigning children, ")

        expected_a_children = [b, c]
        expected_b_children = [d, e]
        assert not f.parent, f"Node f parent, expected {None}, received {f.parent}"

        for parent, children in zip([a, b], [expected_a_children, expected_b_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_children_no_children(self):
        a = helper.clone_tree(self.a, BinaryNode3)
        b = helper.clone_tree(self.b, BinaryNode3)
        c = helper.clone_tree(self.c, BinaryNode3)
        d = helper.clone_tree(self.d, BinaryNode3)
        e = helper.clone_tree(self.e, BinaryNode3)
        f = helper.clone_tree(self.f, BinaryNode2)
        expected_a_children = [b, c]
        expected_b_children = [d, e]
        a.children = expected_a_children
        b.children = expected_b_children
        a.val = 100
        with pytest.raises(exceptions.TreeError) as exc_info:
            a.children = []
        assert str(exc_info.value) == "Custom error assigning children"

        expected_a_children = [b, c]
        expected_b_children = [d, e]
        assert not f.parent, f"Node f parent, expected {None}, received {f.parent}"

        for parent, children in zip([a, b], [expected_a_children, expected_b_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_children_null_children(self):
        a = helper.clone_tree(self.a, BinaryNode3)
        b = helper.clone_tree(self.b, BinaryNode3)
        e = helper.clone_tree(self.e, BinaryNode3)
        f = helper.clone_tree(self.f, BinaryNode2)
        expected_a_children = [b, None]
        expected_b_children = [None, e]
        a.children = expected_a_children
        b.children = expected_b_children
        f.val = 100
        with pytest.raises(exceptions.TreeError) as exc_info:
            a.children = [e, f]
        assert str(exc_info.value).startswith("Custom error assigning children, ")

        expected_a_children = [b, None]
        expected_b_children = [None, e]
        assert not f.parent, f"Node f parent, expected {None}, received {f.parent}"

        for parent, children in zip([a, b], [expected_a_children, expected_b_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"

    def test_rollback_set_children_reassign(self):
        a = helper.clone_tree(self.a, BinaryNode3)
        b = helper.clone_tree(self.b, BinaryNode3)
        c = helper.clone_tree(self.c, BinaryNode3)
        d = helper.clone_tree(self.d, BinaryNode3)
        e = helper.clone_tree(self.e, BinaryNode3)
        expected_a_children = [b, c]
        expected_b_children = [d, e]
        a.children = expected_a_children
        b.children = expected_b_children
        b.val = 100
        with pytest.raises(exceptions.TreeError) as exc_info:
            a.children = [b, c]
        assert str(exc_info.value).startswith("Custom error assigning children, ")

        expected_a_children = [b, c]
        expected_b_children = [d, e]

        for parent, children in zip([a, b], [expected_a_children, expected_b_children]):
            assert (
                list(parent.children) == children
            ), f"Node {parent} children, expected {children}, received {parent.children}"
            for child in children:
                if child:
                    assert (
                        child.parent == parent
                    ), f"Node {child} parent, expected {parent}, received {child.parent}"


def assert_binarytree_structure_root(root):
    """Test tree structure"""
    a = root
    b, c = a.children
    d, e = b.children
    f, g = c.children
    _, h = d.children

    class Sample:
        pass

    self = Sample()
    self.a = a
    self.b = b
    self.c = c
    self.d = d
    self.e = e
    self.f = f
    self.g = g
    self.h = h
    assert_binarytree_structure_self(self)


def assert_binarytree_structure_self(self):
    """Test tree structure with self object"""
    nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

    # Test parent
    expected_ans = [None, self.a, self.a, self.b, self.b, self.c, self.c, self.d]
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.parent
        assert actual == expected, f"Expected parent {expected}, received {actual}"

    # Test children
    expected_ans = [
        [self.b, self.c],
        [self.d, self.e],
        [self.f, self.g],
        [None, self.h],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
    ]
    for _node, expected in zip(nodes, expected_ans):
        actual = list(_node.children)
        assert actual == expected, f"Expected children {expected}, received {actual}"

    # Test left
    expected_ans = [self.b, self.d, self.f, None, None, None, None, None]
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.left
        assert actual == expected, f"Expected left {expected}, received {actual}"

    # Test right
    expected_ans = [self.c, self.e, self.g, self.h, None, None, None, None]
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.right
        assert actual == expected, f"Expected right {expected}, received {actual}"

    # Test ancestors
    expected_ans = [0, 1, 1, 2, 2, 2, 2, 3]
    for _node, expected in zip(nodes, expected_ans):
        actual = len(list(_node.ancestors))
        assert (
            actual == expected
        ), f"Node {_node} should have {expected} ancestors, but it has {actual} ancestors"

    # Test descendants
    expected_ans = [7, 3, 2, 1, 0, 0, 0, 0]
    for _node, expected in zip(nodes, expected_ans):
        actual = len(list(_node.descendants))
        assert (
            actual == expected
        ), f"Node {_node} should have {expected} descendants, but it has {actual} descendants"

    # Test leaves
    expected_ans = [4, 2, 2, 1, 1, 1, 1, 1]
    for _node, expected in zip(nodes, expected_ans):
        actual = len(list(_node.leaves))
        assert (
            actual == expected
        ), f"Node {_node} should have {expected} leaves, but it has {actual} leaves"

    # Test siblings
    expected_ans = [
        (),
        (self.c,),
        (self.b,),
        (self.e,),
        (self.d,),
        (self.g,),
        (self.f,),
        (None,),
    ]
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.siblings
        assert (
            actual == expected
        ), f"Node {_node} should have {expected} siblings, but it has {actual} siblings"

    # Test left_sibling
    expected_ans = [None, None, self.b, None, self.d, None, self.f, None]
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.left_sibling
        assert (
            actual == expected
        ), f"Node {_node} should have {expected} left sibling, but it has {actual} left sibling"

    # Test right_sibling
    expected_ans = [None, self.c, None, self.e, None, self.g, None, None]
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.right_sibling
        assert (
            actual == expected
        ), f"Node {_node} should have {expected} right sibling, but it has {actual} right sibling"

    # Test node_path
    expected_ans = [1, 2, 2, 3, 3, 3, 3, 4]
    for _node, expected in zip(nodes, expected_ans):
        actual = len(list(_node.node_path))
        assert (
            actual == expected
        ), f"Node {_node} should have {expected} nodes in node path, but it has {actual} nodes"

    # Test is_root
    expected_ans = [True, False, False, False, False, False, False, False]
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.is_root
        assert (
            actual == expected
        ), f"Node {_node} is_root should be {expected}, but it is {actual}"

    # Test is_leaf
    expected_ans = [False, False, False, False, True, True, True, True]
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.is_leaf
        assert (
            actual == expected
        ), f"Node {_node} is_leaf should be {expected}, but it is {actual}"

    # Test root
    for _node in nodes:
        actual = _node.root
        assert (
            actual == nodes[0]
        ), f"Node {_node} root should be {expected}, but it is {actual}"

    # Test depth
    expected_ans = [1, 2, 2, 3, 3, 3, 3, 4]
    for self, expected in zip(nodes, expected_ans):
        actual = self.depth
        assert (
            actual == expected
        ), f"Node {node} should be nested to {expected} levels, but it has {actual} levels"

    # Test max_depth
    expected = 4
    for _node in nodes:
        actual = _node.max_depth
        assert (
            actual == expected
        ), f"Node {_node} max_depth should be {expected}, but it is {actual}"

    # Test describe()
    expected_ans = [
        [("name", "1"), ("val", 1)],
        [("name", "2"), ("val", 2)],
        [("name", "3"), ("val", 3)],
        [("name", "4"), ("val", 4)],
        [("name", "5"), ("val", 5)],
        [("name", "6"), ("val", 6)],
        [("name", "7"), ("val", 7)],
        [("name", "8"), ("val", 8)],
    ]
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.describe(exclude_prefix="_")
        assert (
            actual == expected
        ), f"Node description should be {expected}, but it is {actual}"

    # Test get_attr()
    expected_ans = [1, 2, 3, 4, 5, 6, 7, 8]
    for _node, expected in zip(nodes, expected_ans):
        actual = _node.get_attr("val")
        assert actual == expected, f"Expected right {expected}, received {actual}"


def assert_binarytree_structure_root2(root):
    """Test tree structure"""
    a = root
    b, c = a.children
    d, e = b.children
    f, g = c.children
    h, _ = d.children

    expected_str = (
        "                 ┌─ 8\n"
        "           ┌─ 4 ─┤\n"
        "     ┌─ 2 ─┤     └─\n"
        "─ 1 ─┤     └─ 5\n"
        "     │     ┌─ 6\n"
        "     └─ 3 ─┤\n"
        "           └─ 7\n"
    )
    assert_print_statement(
        export.hprint_tree,
        expected_str,
        tree=root,
    )

    expected_str = (
        "                ┌───┐            \n"
        "                │ 1 │            \n"
        "                └─┬─┘            \n"
        "          ┌───────┴───────┐      \n"
        "        ┌─┴─┐           ┌─┴─┐    \n"
        "        │ 2 │           │ 3 │    \n"
        "        └─┬─┘           └─┬─┘    \n"
        "     ┌────┴─────┐      ┌──┴───┐  \n"
        "   ┌─┴─┐      ┌─┴─┐  ┌─┴─┐  ┌─┴─┐\n"
        "   │ 4 │      │ 5 │  │ 6 │  │ 7 │\n"
        "   └─┬─┘      └───┘  └───┘  └───┘\n"
        "  ┌──┴───┐                       \n"
        "┌─┴─┐  ┌─┴─┐                     \n"
        "│ 8 │  │   │                     \n"
        "└───┘  └───┘                     \n"
    )
    assert_print_statement(
        export.vprint_tree,
        expected_str,
        tree=root,
    )

    class Sample:
        pass

    self = Sample()
    self.a = a
    self.b = b
    self.c = c
    self.d = d
    self.e = e
    self.f = f
    self.g = g
    self.h = h
    assert_binarytree_structure_self2(self)


def assert_binarytree_structure_self2(self):
    """Test tree structure with self object"""
    nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

    # Test parent
    expected_parent = [None, self.a, self.a, self.b, self.b, self.c, self.c, self.d]
    for _node, expected in zip(nodes, expected_parent):
        actual = _node.parent
        assert actual == expected, f"Expected parent {expected}, received {actual}"

    # Test children
    expected_children = [
        [self.b, self.c],
        [self.d, self.e],
        [self.f, self.g],
        [self.h, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
    ]
    for _node, expected in zip(nodes, expected_children):
        actual = list(_node.children)
        assert actual == expected, f"Expected children {expected}, received {actual}"

    # Test left
    expected_left = [self.b, self.d, self.f, self.h, None, None, None, None]
    for _node, expected in zip(nodes, expected_left):
        actual = _node.left
        assert actual == expected, f"Expected left {expected}, received {actual}"

    # Test right
    expected_right = [self.c, self.e, self.g, None, None, None, None, None]
    for _node, expected in zip(nodes, expected_right):
        actual = _node.right
        assert actual == expected, f"Expected right {expected}, received {actual}"

    # Test get_attr()
    expected_val = [1, 2, 3, 4, 5, 6, 7, 8]
    for _node, expected in zip(nodes, expected_val):
        actual = _node.get_attr("val")
        assert actual == expected, f"Expected attribute {expected}, received {actual}"

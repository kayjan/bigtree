import unittest

import pytest

from bigtree import LoopError, TreeError
from bigtree.node.bnode import BNode
from bigtree.tree.helper import clone_tree
from tests.conftest import assert_print_statement


class BNode2(BNode):
    def _BNode__post_assign_parent(self, new_parent):
        if new_parent is not None:
            if new_parent.val == 100:
                raise Exception(
                    f"Custom error assigning parent, new parent {new_parent} and children are {new_parent.children}"
                )


class BNode3(BNode):
    def _BNode__post_assign_children(self, new_children):
        for child in new_children:
            if child and child.val == 100:
                raise Exception(
                    f"Custom error assigning children, new children {new_children}"
                )


class TestBNode(unittest.TestCase):
    def setUp(self):
        self.a = BNode(1)
        self.b = BNode(2)
        self.c = BNode(3)
        self.d = BNode(4)
        self.e = BNode(5)
        self.f = BNode(6)
        self.g = BNode(7)
        self.h = BNode(8)

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
        self.a = BNode.from_dict({"name": 1})
        self.b = BNode.from_dict({"name": 2})
        self.c = BNode.from_dict({"name": 3})
        self.d = BNode.from_dict({"name": 4})
        self.e = BNode.from_dict({"name": 5})
        self.f = BNode.from_dict({"name": 6})
        self.g = BNode.from_dict({"name": 7})
        self.h = BNode.from_dict({"name": 8})

        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.c.children = []
        self.c.left = self.f
        self.g.parent = self.c
        self.d.children = []
        self.d.children = [None, self.h]

        assert_btree_structure_self(self)
        assert_print_statement(print, "BNode(name=1, val=1)\n", self.a)
        assert (
            self.a.node_name == "1"
        ), f"Node name is wrong, expected 1, received {self.a.node_name}"
        assert (
            self.a.val == 1
        ), f"Node name is wrong, expected 1, received {self.a.node_name}"
        self.h.children = []
        assert not self.h.left, f"Expected {None}, received {self.h.left}"
        assert not self.h.right, f"Expected {None}, received {self.h.right}"
        self.a.sep = "\\"
        assert (
            self.b.path_name == "\\1\\2"
        ), f"Expected \\1\\2, received {self.b.path_name}"

    def test_set_parent_error(self):
        with pytest.raises(ValueError) as exc_info:
            self.b.parents = [self.a]
        assert str(exc_info.value).startswith("Attempting to set `parents` attribute")

        with pytest.raises(ValueError) as exc_info:
            self.b = BNode(1, parents=[self.a])
        assert str(exc_info.value).startswith("Attempting to set `parents` attribute")

        with pytest.raises(ValueError) as exc_info:
            self.b.parents
        assert str(exc_info.value).startswith(
            "Attempting to access `parents` attribute"
        )

    def test_set_parent_3_parent_error(self):
        self.b.parent = self.a
        self.c.parent = self.a
        with pytest.raises(TreeError) as exc_info:
            self.d.parent = self.a
        assert str(exc_info.value).endswith("already has 2 children")

    def test_set_parent(self):
        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.f.parent = self.c
        self.g.parent = self.c
        self.d.children = [None, self.h]

        assert_btree_structure_self(self)

    def test_set_parent_children_insert(self):
        self.a.children = [None, None]
        self.b.parent = self.a
        self.c.parent = self.a
        self.b.children = [self.d, None]
        self.e.parent = self.b
        self.c.children = [None, self.g]
        self.f.parent = self.c
        self.d.children = [None, self.h]

        assert_btree_structure_self(self)

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
        assert_btree_structure_self(self)

    def test_set_parent_rshift(self):
        self.a >> self.b
        self.a >> self.c
        self.b >> self.d
        self.b >> self.e
        self.c >> self.f
        self.c >> self.g
        self.d.children = [None, self.h]

        assert_btree_structure_self(self)

    def test_set_parent_lshift(self):
        self.b << self.a
        self.c << self.a
        self.d << self.b
        self.e << self.b
        self.f << self.c
        self.g << self.c
        self.d.children = [None, self.h]

        assert_btree_structure_self(self)

    def test_set_parent_constructor(self):
        self.a = BNode(1)
        self.b = BNode(2, parent=self.a)
        self.c = BNode(3, parent=self.a)
        self.d = BNode(4, parent=self.b)
        self.e = BNode(5, parent=self.b)
        self.f = BNode(6, parent=self.c)
        self.g = BNode(7, parent=self.c)
        self.h = BNode(8)
        self.d.children = [None, self.h]

        assert_btree_structure_self(self)

    def test_set_parent_null_parent(self):
        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.f.parent = self.c
        self.g.parent = self.c
        self.d.children = [None, self.h]

        dummy = BNode(100)
        dummy.parent = self.h
        assert list(self.h.children) == [dummy, None]

        dummy.parent = None
        assert_btree_structure_self(self)

    def test_set_parent_duplicate(self):
        # Set parent again
        self.b.parent = self.a
        self.b.parent = self.a
        assert list(self.a.children) == [self.b, None]
        assert self.b.parent == self.a

    def test_set_parent_duplicate_constructor(self):
        # Set parent again
        self.a = BNode(1)
        self.b = BNode(2, parent=self.a)
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

        assert_btree_structure_self(self)

    def test_set_left_and_right_constructor(self):
        self.h = BNode(8)
        self.g = BNode(7)
        self.f = BNode(6)
        self.e = BNode(5)
        self.d = BNode(4, right=self.h)
        self.c = BNode(3, left=self.f, right=self.g)
        self.b = BNode(2, left=self.d, right=self.e)
        self.a = BNode(1, left=self.b, right=self.c)

        assert_btree_structure_self(self)

    def test_set_left_and_right_and_children_constructor(self):
        self.h = BNode(8)
        self.g = BNode(7)
        self.f = BNode(6)
        self.e = BNode(5)
        self.d = BNode(4, right=self.h, children=[None, self.h])
        self.c = BNode(3, left=self.f, right=self.g, children=[self.f, self.g])
        self.b = BNode(2, left=self.d, right=self.e, children=[self.d, self.e])
        self.a = BNode(1, left=self.b, right=self.c, children=[self.b, self.c])

        assert_btree_structure_self(self)

    def test_set_left_and_right_and_children_constructor_error(self):
        with pytest.raises(ValueError) as exc_info:
            self.a = BNode(1, left=self.b, right=self.c, children=[self.c])
        assert str(exc_info.value).startswith("Children input must have length 2")

        with pytest.raises(ValueError) as exc_info:
            self.a = BNode(1, left=self.b, right=self.c, children=[self.d, self.c])
        assert str(exc_info.value).startswith(
            "Attempting to set both left and children with mismatched values"
        )

        with pytest.raises(ValueError) as exc_info:
            self.a = BNode(1, left=self.b, right=self.c, children=[self.b, self.d])
        assert str(exc_info.value).startswith(
            "Attempting to set both right and children with mismatched values"
        )

    def test_set_left_and_right_duplicate(self):
        # Set parent again
        self.a = BNode(1, left=self.b, right=self.c)
        self.a.left = self.b
        self.a.right = self.c
        assert list(self.a.children) == [self.b, self.c]
        assert self.b.parent == self.a
        assert self.c.parent == self.a

    def test_set_children_3_children_error(self):
        with pytest.raises(ValueError) as exc_info:
            self.a.children = [self.b, self.c, self.d]
        assert str(exc_info.value) == "Children input must have length 2"

    def test_set_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f, self.g]
        self.d.children = [None, self.h]

        assert_btree_structure_self(self)

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
        assert_btree_structure_self(self)

    def test_set_children_constructor(self):
        self.h = BNode(8)
        self.g = BNode(7)
        self.f = BNode(6)
        self.e = BNode(5)
        self.d = BNode(4, children=[None, self.h])
        self.c = BNode(3, children=[self.f, self.g])
        self.b = BNode(2, children=[self.d, self.e])
        self.a = BNode(1, children=[self.b, self.c])

        assert_btree_structure_self(self)

    def test_set_children_null_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f, self.g]
        self.d.children = [None, self.h]

        dummy = BNode(100)
        self.h.children = [dummy, None]
        assert dummy.parent == self.h
        self.h.children = []

        assert_btree_structure_self(self)

    def test_set_children_null_parent(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f, self.g]
        self.d.children = [None, self.h]

        dummy = BNode(100)
        self.h.children = [dummy, None]
        assert dummy.parent == self.h
        dummy.parent.children = []

        assert_btree_structure_self(self)

    def test_set_children_none_parent(self):
        with pytest.raises(TypeError):
            self.h.children = None

    def test_set_children_duplicate(self):
        # Set child again
        self.a.children = [self.b, None]
        self.a.children = [self.b, None]
        assert list(self.a.children) == [self.b, None]
        assert self.b.parent == self.a

    def test_set_children_duplicate_constructor(self):
        # Set child again
        self.a = BNode(1, children=[self.b, None])
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
        assert_btree_structure_root(a2)

    def test_error_set_parent_type_error(self):
        # Error: wrong type
        with pytest.raises(TypeError):
            self.a.parent = 1

    def test_error_set_parent_loop_error(self):
        # Error: set self as parent
        with pytest.raises(LoopError):
            self.a.parent = self.a

        # Error: set descendant as parent
        with pytest.raises(LoopError):
            self.b.parent = self.a
            self.c.parent = self.b
            self.a.parent = self.c

    def test_error_set_children_type_error(self):
        # Error: wrong type
        with pytest.raises(TypeError):
            self.a.children = [self.b, 1]

    def test_error_set_children_length_error(self):
        # Error: wrong type
        with pytest.raises(ValueError) as exc_info:
            self.a.children = [self.b]
        assert str(exc_info.value).startswith("Children input must have length 2")

    def test_error_set_children_loop_error(self):
        # Error: set self as child
        with pytest.raises(LoopError):
            self.a.children = [self.b, self.a]

        # Error: set ancestor as child
        with pytest.raises(LoopError):
            self.a.children = [self.b, self.c]
            self.c.children = [self.d, self.e]
            self.e.children = [self.a, self.f]

    def test_error_set_children_exception(self):
        # Error: duplicate child
        with pytest.raises(TreeError):
            self.a.children = [self.b, self.b]

    def test_rollback_setting_parent(self):
        a = clone_tree(self.a, BNode2)
        b = clone_tree(self.b, BNode2)
        c = clone_tree(self.c, BNode2)
        d = clone_tree(self.d, BNode2)
        e = clone_tree(self.e, BNode2)
        f = clone_tree(self.f, BNode2)
        expected_a_children = [None, c]
        expected_b_children = [d, e]
        expected_f_children = [None, b]
        a.children = expected_a_children
        b.children = expected_b_children
        f.children = expected_f_children
        a.val = 100
        with pytest.raises(TreeError) as exc_info:
            b.parent = a
        assert str(exc_info.value).startswith("Custom error assigning parent")
        assert b.parent == f, f"Node b parent, expected {f}, received {b.parent}"
        assert (
            list(a.children) == expected_a_children
        ), f"Node a children, expected {expected_a_children}, received {a.children}"
        for child in expected_a_children:
            assert (
                child.parent == a
            ), f"Node {child} parent, expected {a}, received {child.parent}"
        assert (
            list(b.children) == expected_b_children
        ), f"Node b children, expected {expected_b_children}, received {list(b.children)}"
        for child in expected_b_children:
            assert (
                child.parent == b
            ), f"Node {child} parent, expected {a}, received {child.parent}"
        assert (
            list(f.children) == expected_f_children
        ), f"Node f children, expected {expected_f_children}, received {list(f.children)}"
        for child in expected_f_children:
            if child:
                assert (
                    child.parent == f
                ), f"Node {child} parent, expected {f}, received {child.parent}"

    def test_rollback_setting_children(self):
        a = clone_tree(self.a, BNode3)
        b = clone_tree(self.b, BNode3)
        c = clone_tree(self.c, BNode3)
        d = clone_tree(self.d, BNode3)
        e = clone_tree(self.e, BNode3)
        f = clone_tree(self.f, BNode2)
        expected_a_children = [b, c]
        expected_b_children = [d, e]
        a.children = expected_a_children
        b.children = expected_b_children
        f.val = 100
        with pytest.raises(TreeError) as exc_info:
            a.children = [d, f]
        expected_a_children = [b, c]
        assert str(exc_info.value).startswith("Custom error assigning children")
        assert b.parent == a, f"Node b parent, expected {a}, received {b.parent}"
        assert c.parent == a, f"Node c parent, expected {a}, received {c.parent}"
        assert d.parent == b, f"Node d parent, expected {b}, received {d.parent}"
        assert e.parent == b, f"Node e parent, expected {b}, received {e.parent}"
        assert not f.parent, f"Node f parent, expected {None}, received {f.parent}"
        assert (
            list(a.children) == expected_a_children
        ), f"Node a children, expected {expected_a_children}, received {a.children}"
        for child in expected_a_children:
            assert (
                child.parent == a
            ), f"Node {child} parent, expected {a}, received {child.parent}"
        assert (
            list(b.children) == expected_b_children
        ), f"Node b children, expected {expected_b_children}, received {list(b.children)}"
        for child in expected_b_children:
            assert (
                child.parent == b
            ), f"Node {child} parent, expected {a}, received {child.parent}"


def assert_btree_structure_self(self):
    nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

    # Test parent
    expected_ans = [None, self.a, self.a, self.b, self.b, self.c, self.c, self.d]
    for node, expected in zip(nodes, expected_ans):
        actual = node.parent
        assert expected == actual, f"Expected parent {expected}, received {actual}"

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
    for node, expected in zip(nodes, expected_ans):
        actual = list(node.children)
        assert expected == actual, f"Expected children {expected}, received {actual}"

    # Test left
    expected_ans = [self.b, self.d, self.f, None, None, None, None, None]
    for node, expected in zip(nodes, expected_ans):
        actual = node.left
        assert expected == actual, f"Expected left {expected}, received {actual}"

    # Test right
    expected_ans = [self.c, self.e, self.g, self.h, None, None, None, None]
    for node, expected in zip(nodes, expected_ans):
        actual = node.right
        assert expected == actual, f"Expected right {expected}, received {actual}"

    # Test ancestors
    expected_ans = [0, 1, 1, 2, 2, 2, 2, 3]
    for node, expected in zip(nodes, expected_ans):
        actual = len(list(node.ancestors))
        assert (
            actual == expected
        ), f"Node {node} should have {expected} ancestors, but it has {actual} ancestors"

    # Test descendants
    expected_ans = [7, 3, 2, 1, 0, 0, 0, 0]
    for node, expected in zip(nodes, expected_ans):
        actual = len(list(node.descendants))
        assert (
            actual == expected
        ), f"Node {node} should have {expected} descendants, but it has {actual} descendants"

    # Test leaves
    expected_ans = [4, 2, 2, 1, 1, 1, 1, 1]
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
        (self.g,),
        (self.f,),
        (None,),
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = node.siblings
        assert (
            actual == expected
        ), f"Node {node} should have {expected} siblings, but it has {actual} siblings"

    # Test left_sibling
    expected_ans = [None, None, self.b, None, self.d, None, self.f, None]
    for node, expected in zip(nodes, expected_ans):
        actual = node.left_sibling
        assert (
            actual == expected
        ), f"Node {node} should have {expected} left sibling, but it has {actual} left sibling"

    # Test right_sibling
    expected_ans = [None, self.c, None, self.e, None, self.g, None, None]
    for node, expected in zip(nodes, expected_ans):
        actual = node.right_sibling
        assert (
            actual == expected
        ), f"Node {node} should have {expected} right sibling, but it has {actual} right sibling"

    # Test node_path
    expected_ans = [1, 2, 2, 3, 3, 3, 3, 4]
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
    expected_ans = [False, False, False, False, True, True, True, True]
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

    # Test depth
    expected_ans = [1, 2, 2, 3, 3, 3, 3, 4]
    for self, expected in zip(nodes, expected_ans):
        actual = self.depth
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
        [("name", "1"), ("val", 1)],
        [("name", "2"), ("val", 2)],
        [("name", "3"), ("val", 3)],
        [("name", "4"), ("val", 4)],
        [("name", "5"), ("val", 5)],
        [("name", "6"), ("val", 6)],
        [("name", "7"), ("val", 7)],
        [("name", "8"), ("val", 8)],
    ]
    for node, expected in zip(nodes, expected_ans):
        actual = node.describe(exclude_prefix="_")
        assert (
            actual == expected
        ), f"Node description should be {expected}, but it is {actual}"

    # Test get_attr()
    expected_ans = [1, 2, 3, 4, 5, 6, 7, 8]
    for node, expected in zip(nodes, expected_ans):
        actual = node.get_attr("val")
        assert expected == actual, f"Expected right {expected}, received {actual}"


def assert_btree_structure_root(root):
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
    assert_btree_structure_self(self)


def assert_btree_structure_self2(self):
    nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

    # Test parent
    expected_parent = [None, self.a, self.a, self.b, self.b, self.c, self.c, self.d]
    for node, expected in zip(nodes, expected_parent):
        actual = node.parent
        assert expected == actual, f"Expected parent {expected}, received {actual}"

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
    for node, expected in zip(nodes, expected_children):
        actual = list(node.children)
        assert expected == actual, f"Expected children {expected}, received {actual}"

    # Test left
    expected_left = [self.b, self.d, self.f, self.h, None, None, None, None]
    for node, expected in zip(nodes, expected_left):
        actual = node.left
        assert expected == actual, f"Expected left {expected}, received {actual}"

    # Test right
    expected_right = [self.c, self.e, self.g, None, None, None, None, None]
    for node, expected in zip(nodes, expected_right):
        actual = node.right
        assert expected == actual, f"Expected right {expected}, received {actual}"

    # Test get_attr()
    expected_val = [1, 2, 3, 4, 5, 6, 7, 8]
    for node, expected in zip(nodes, expected_val):
        actual = node.get_attr("val")
        assert expected == actual, f"Expected attribute {expected}, received {actual}"


def assert_btree_structure_root2(root):
    a = root
    b, c = a.children
    d, e = b.children
    f, g = c.children
    h, _ = d.children

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
    assert_btree_structure_self2(self)

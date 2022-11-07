import copy
import unittest

import pytest

from bigtree import BaseNode
from bigtree.utils.exceptions import LoopError, TreeError
from tests.conftest import assert_print_statement


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
        self.a = BaseNode(name="a", age=90)
        self.b = BaseNode(name="b", age=65)
        self.c = BaseNode(name="c", age=60)
        self.d = BaseNode(name="d", age=40)
        self.e = BaseNode(name="e", age=35)
        self.f = BaseNode(name="f", age=38)
        self.g = BaseNode(name="g", age=10)
        self.h = BaseNode(name="h", age=6)

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
        self.a = BaseNode().from_dict({"name": "a", "age": 90})
        self.b = BaseNode().from_dict({"name": "b", "age": 65})
        self.c = BaseNode().from_dict({"name": "c", "age": 60})
        self.d = BaseNode().from_dict({"name": "d", "age": 40})
        self.e = BaseNode().from_dict({"name": "e", "age": 35})
        self.f = BaseNode().from_dict({"name": "f", "age": 38})
        self.g = BaseNode().from_dict({"name": "g", "age": 10})
        self.h = BaseNode().from_dict({"name": "h", "age": 6})

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
        assert_print_statement(print, "BaseNode(age=90, name=a)\n", self.a)

    def test_set_parent_error(self):
        with pytest.raises(ValueError) as exc_info:
            self.b.parents = [self.a]
        assert str(exc_info.value).startswith("Attempting to set `parents` attribute")

        with pytest.raises(ValueError) as exc_info:
            self.b = BaseNode(parents=[self.a])
        assert str(exc_info.value).startswith("Attempting to set `parents` attribute")

        with pytest.raises(ValueError) as exc_info:
            self.b.parents
        assert str(exc_info.value).startswith(
            "Attempting to access `parents` attribute"
        )

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

    def test_set_parent_rshift(self):
        self.a >> self.b
        self.a >> self.c
        self.b >> self.d
        self.b >> self.e
        self.c >> self.f
        self.e >> self.g
        self.e >> self.h

        assert_tree_structure_basenode_root_generic(self.a)
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

        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_parent_constructor(self):
        self.a = BaseNode(name="a", age=90)
        self.b = BaseNode(name="b", age=65, parent=self.a)
        self.c = BaseNode(name="c", age=60, parent=self.a)
        self.d = BaseNode(name="d", age=40, parent=self.b)
        self.e = BaseNode(name="e", age=35, parent=self.b)
        self.f = BaseNode(name="f", age=38, parent=self.c)
        self.g = BaseNode(name="g", age=10, parent=self.e)
        self.h = BaseNode(name="h", age=6, parent=self.e)

        assert_tree_structure_basenode_root_generic(self.a)
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

        dummy = BaseNode()
        dummy.parent = self.h
        dummy.parent = None

        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_parent_duplicate(self):
        # Set parent again
        self.b.parent = self.a
        self.b.parent = self.a

    def test_set_parent_duplicate_constructor(self):
        # Set parent again
        self.a = BaseNode(name="a", age=90)
        self.b = BaseNode(name="b", age=65, parent=self.a)
        self.b.parent = self.a

    def test_set_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_constructor(self):
        self.h = BaseNode(name="h", age=6)
        self.g = BaseNode(name="g", age=10)
        self.f = BaseNode(name="f", age=38)
        self.e = BaseNode(name="e", age=35, children=[self.g, self.h])
        self.d = BaseNode(name="d", age=40)
        self.c = BaseNode(name="c", age=60, children=[self.f])
        self.b = BaseNode(name="b", age=65, children=[self.d, self.e])
        self.a = BaseNode(name="a", age=90, children=[self.b, self.c])

        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_null_children(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

        dummy = BaseNode()
        self.h.children = [dummy]
        self.h.children = []

        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_null_parent(self):
        self.a.children = [self.b, self.c]
        self.b.children = [self.d, self.e]
        self.c.children = [self.f]
        self.e.children = [self.g, self.h]

        dummy = BaseNode()
        self.h.children = [dummy]
        dummy.parent.children = []
        assert_tree_structure_basenode_root_generic(self.a)
        assert_tree_structure_basenode_root_attr(self.a)
        assert_tree_structure_basenode_self(self)

    def test_set_children_none_parent(self):
        with pytest.raises(TypeError):
            self.h.children = None

    def test_set_children_duplicate(self):
        # Set child again
        self.a.children = [self.b]
        self.a.children = [self.b]

    def test_set_children_duplicate_constructor(self):
        # Set child again
        self.a = BaseNode(children=[self.b])
        self.a.children = [self.b]

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
        assert_tree_structure_basenode_root_generic(a2)
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
        assert_tree_structure_basenode_root_generic(a2)
        assert_tree_structure_basenode_root_attr(a2)

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


def assert_tree_structure_basenode_root_generic(root):
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

    # Test get_attribute()
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


def assert_tree_structure_basenode_root_attr(root):
    # Test describe()
    expected = [("age", 90), ("name", "a")]
    actual = root.describe(exclude_prefix="_")
    assert (
        actual == expected
    ), f"Node description should be {expected}, but it is {actual}"


def assert_tree_structure_basenode_self(self):
    nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

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

    # Test depth
    expected_ans = [1, 2, 2, 3, 3, 3, 4, 4]
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

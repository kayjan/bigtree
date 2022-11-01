import unittest

import pytest

from bigtree.node.node import Node
from bigtree.tree.modify import copy_or_shift_logic
from bigtree.tree.search import find_path
from bigtree.utils.exceptions import NotFoundError, TreeError
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root_attr,
    assert_tree_structure_basenode_root_generic,
)
from tests.node.test_node import assert_tree_structure_node_root_generic


class TestCopyOrShiftNodes(unittest.TestCase):
    def setUp(self):
        """
        Tree should have structure
        a
        |-- b
        |   |-- d
        |   +-- e
        |       |-- g
        |       +-- h
        +-- c
            +-- f
        """
        a = Node(name="a", age=90)
        b = Node(name="b", age=65)
        c = Node(name="c", age=60)
        d = Node(name="d", age=40)
        e = Node(name="e", age=35)
        f = Node(name="f", age=38)
        g = Node(name="g", age=10)
        h = Node(name="h", age=6)

        b.parent = a
        c.parent = a
        d.parent = a
        e.parent = a
        f.parent = a
        g.parent = a
        h.parent = a

        self.root = a

    def tearDown(self):
        self.root = None

    def test_copy_or_shift_nodes(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        copy_or_shift_logic(self.root, from_paths, to_paths)
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_copy_or_shift_nodes_invalid_type(self):
        with pytest.raises(ValueError) as exc_info:
            copy_or_shift_logic(self.root, {}, [])
        assert str(exc_info.value).startswith("Invalid type")

    def test_copy_or_shift_nodes_unequal_length(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d"]
        with pytest.raises(ValueError) as exc_info:
            copy_or_shift_logic(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Paths are different length")

    def test_copy_or_shift_nodes_invalid_paths(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/e", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        with pytest.raises(ValueError) as exc_info:
            copy_or_shift_logic(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Unable to assign")

    def test_copy_or_shift_nodes_invalid_from_paths(self):
        from_paths = ["i"]
        to_paths = ["a/b/i"]
        with pytest.raises(NotFoundError) as exc_info:
            copy_or_shift_logic(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Unable to find from_path")

    def test_copy_or_shift_nodes_invalid_to_paths(self):
        from_paths = ["d"]
        to_paths = ["aa/b/d"]
        with pytest.raises(NotFoundError) as exc_info:
            copy_or_shift_logic(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Unable to find to_path")

    def test_copy_or_shift_nodes_create_intermediate_path(self):
        from_paths = ["d"]
        to_paths = ["a/b/c/d"]
        copy_or_shift_logic(self.root, from_paths, to_paths)
        assert self.root.max_depth == 4, "Shift did not create a tree of depth 4"

    def test_copy_or_shift_nodes_sep_undefined(self):
        from_paths = ["\\d", "\\e", "\\g", "\\h", "\\f"]
        to_paths = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        with pytest.raises(ValueError) as exc_info:
            copy_or_shift_logic(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Unable to assign from_path")

    def test_copy_or_shift_nodes_sep(self):
        from_paths = ["\\d", "\\e", "\\g", "\\h", "\\f"]
        to_paths = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        copy_or_shift_logic(self.root, from_paths, to_paths, sep="\\")
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_copy_or_shift_nodes_copy_node(self):
        from_paths = ["d"]
        to_paths = ["a/b/c/d"]
        copy_or_shift_logic(self.root, from_paths, to_paths, copy=True)
        assert self.root.max_depth == 4, "Shift did not create a tree of depth 4"
        assert find_path(self.root, "a/d"), "Original node is not there"
        assert find_path(self.root, "a/b/c/d"), "Copied node is not there"

    def test_copy_or_shift_nodes_skippable(self):
        from_paths = ["i", "d", "e", "g", "h", "f"]
        to_paths = ["a/c/f/i", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        with pytest.raises(NotFoundError):
            copy_or_shift_logic(self.root, from_paths, to_paths)

        copy_or_shift_logic(self.root, from_paths, to_paths, skippable=True)
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_copy_or_shift_nodes_delete_and_overriding_error(self):
        new_aa = Node("aa", parent=self.root)
        new_d = Node("d")
        new_d.parent = new_aa
        from_paths = ["/a/d", "aa/d", "e", "g", "h", "f", "a/aa"]
        to_paths = ["a/b/d", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f", None]
        with pytest.raises(TreeError):
            copy_or_shift_logic(self.root, from_paths, to_paths)

    def test_copy_or_shift_nodes_delete_and_overriding(self):
        new_aa = Node("aa", parent=self.root)
        new_d = Node("d")
        new_d.parent = new_aa
        from_paths = ["/a/d", "aa/d", "e", "g", "h", "f", "a/aa"]
        to_paths = ["a/b/d", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f", None]
        copy_or_shift_logic(self.root, from_paths, to_paths, overriding=True)
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_copy_or_shift_nodes_merge_children_change_levels(self):
        new_aa = Node("aa", parent=self.root)
        new_bb = Node("bb", parent=new_aa)
        new_cc = Node("cc")
        new_cc.parent = new_bb

        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        copy_or_shift_logic(self.root, from_paths, to_paths)

        from_paths = ["aa/bb"]
        to_paths = ["/a/bb"]
        copy_or_shift_logic(self.root, from_paths, to_paths, merge_children=True)
        assert len(list(self.root.children)) == 4
        assert find_path(self.root, "a/cc"), "Node children not merged"
        assert not len(
            list(find_path(self.root, "a/aa").children)
        ), "Node parent not deleted"

    def test_copy_or_shift_nodes_merge_children_same_level(self):
        new_aa = Node("aa", parent=self.root)
        new_bb = Node("bb", parent=new_aa)
        new_cc = Node("cc")
        new_cc.parent = new_bb

        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        copy_or_shift_logic(self.root, from_paths, to_paths)

        from_paths = ["aa"]
        to_paths = ["/a/aa"]
        copy_or_shift_logic(self.root, from_paths, to_paths, merge_children=True)
        assert len(list(self.root.children)) == 3
        assert find_path(self.root, "a/bb"), "Node children not merged"

    def test_copy_or_shift_nodes_shift_same_node(self):
        from_paths = ["d"]
        to_paths = ["a/d"]
        with pytest.raises(TreeError) as exc_info:
            copy_or_shift_logic(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Attempting to shift the same node")

    def test_copy_or_shift_nodes_tree_to_tree(self):
        root_other = Node("a", age=90)
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        copy_or_shift_logic(
            self.root, from_paths, to_paths, copy=True, to_tree=root_other
        )
        assert_tree_structure_basenode_root_generic(root_other)
        assert_tree_structure_basenode_root_attr(root_other)
        assert_tree_structure_node_root_generic(root_other)
        assert self.root.max_depth == 2, "Copying changes original tree"

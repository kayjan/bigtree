import unittest

import pytest

from bigtree.node.node import Node
from bigtree.tree.export import print_tree
from bigtree.tree.modify import copy_nodes, copy_nodes_from_tree_to_tree, shift_nodes
from bigtree.tree.search import find_name, find_path
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

    def test_shift_nodes(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths)
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_shift_nodes_invalid_type(self):
        with pytest.raises(ValueError) as exc_info:
            shift_nodes(self.root, {}, [])
        assert str(exc_info.value).startswith("Invalid type")

    def test_shift_nodes_unequal_length(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d"]
        with pytest.raises(ValueError) as exc_info:
            shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Paths are different length")

    def test_shift_nodes_invalid_paths(self):
        from_paths = ["d"]
        to_paths = ["a/b/e"]
        with pytest.raises(ValueError) as exc_info:
            shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Unable to assign")

    def test_shift_nodes_invalid_from_paths(self):
        from_paths = ["i"]
        to_paths = ["a/b/i"]
        with pytest.raises(NotFoundError) as exc_info:
            shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Unable to find from_path")

    def test_shift_nodes_invalid_to_paths(self):
        from_paths = ["d"]
        to_paths = ["aa/b/d"]
        with pytest.raises(NotFoundError) as exc_info:
            shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Unable to find to_path")

    def test_shift_nodes_create_intermediate_path(self):
        from_paths = ["d"]
        to_paths = ["a/b/c/d"]
        shift_nodes(self.root, from_paths, to_paths)
        assert self.root.max_depth == 4, "Shift did not create a tree of depth 4"

    def test_shift_nodes_sep_undefined(self):
        from_paths = ["\\d", "\\e", "\\g", "\\h", "\\f"]
        to_paths = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        with pytest.raises(ValueError) as exc_info:
            shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Unable to assign from_path")

    def test_shift_nodes_sep(self):
        from_paths = ["\\d", "\\e", "\\g", "\\h", "\\f"]
        to_paths = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        shift_nodes(self.root, from_paths, to_paths, sep="\\")
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_copy_nodes_copy_node(self):
        from_paths = ["d"]
        to_paths = ["a/b/c/d"]
        copy_nodes(self.root, from_paths, to_paths)
        assert self.root.max_depth == 4, "Shift did not create a tree of depth 4"
        assert find_path(self.root, "a/d"), "Original node is not there"
        assert find_path(self.root, "a/b/c/d"), "Copied node is not there"

    def test_shift_nodes_skippable(self):
        from_paths = ["i", "d", "e", "g", "h", "f"]
        to_paths = ["a/c/f/i", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        with pytest.raises(NotFoundError):
            shift_nodes(self.root, from_paths, to_paths)

        shift_nodes(self.root, from_paths, to_paths, skippable=True)
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_shift_nodes_delete_and_overriding_error(self):
        new_aa = Node("aa", parent=self.root)
        new_d = Node("d")
        new_d.parent = new_aa
        from_paths = ["/a/d", "aa/d", "e", "g", "h", "f", "a/aa"]
        to_paths = ["a/b/d", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f", None]
        with pytest.raises(TreeError):
            shift_nodes(self.root, from_paths, to_paths)

    def test_shift_nodes_delete_and_overriding(self):
        new_aa = Node("aa", parent=self.root)
        new_d = Node("d", age=1)
        new_d.parent = new_aa
        from_paths = ["/a/d", "aa/d", "e", "g", "h", "f", "a/aa"]
        to_paths = ["a/b/d", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f", None]
        shift_nodes(self.root, from_paths, to_paths, overriding=True)
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root, d=("d", 1))
        assert_tree_structure_node_root_generic(self.root)

    def test_shift_nodes_merge_children(self):
        new_aa = Node("aa", parent=self.root)
        new_bb = Node("bb", parent=new_aa)
        new_cc = Node("cc", age=1)
        new_cc.parent = new_bb

        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["aa/bb"]
        to_paths = ["/a/bb"]
        shift_nodes(self.root, from_paths, to_paths, merge_children=True)
        assert len(list(self.root.children)) == 4
        assert find_path(self.root, "a/cc"), "Node children not merged"
        assert (
            find_path(self.root, "a/cc").get_attr("age") == 1
        ), f"Merged children not overridden, {print_tree(self.root)}"
        assert not len(
            list(find_path(self.root, "a/aa").children)
        ), "Node parent not deleted"

    def test_shift_nodes_merge_children_non_overriding(self):
        new_aa = Node("aa", parent=self.root)
        new_bb = Node("bb", parent=new_aa)
        new_cc = Node("cc", age=1)
        new_cc.parent = new_bb
        bb2 = Node("bb")
        cc2 = Node("cc2")
        bb2.parent = self.root
        cc2.parent = bb2

        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["aa/bb"]
        to_paths = ["/a/bb"]
        shift_nodes(self.root, from_paths, to_paths, merge_children=True)
        assert len(list(self.root.children)) == 4
        assert find_path(
            self.root, "a/bb/cc"
        ), "Node children not merged, new children not present"
        assert find_path(
            self.root, "a/bb/cc2"
        ), "Node children not merged, original children overridden"
        assert (
            find_path(self.root, "a/bb/cc").get_attr("age") == 1
        ), f"Merged children not overridden, {print_tree(self.root)}"
        assert not len(
            list(find_path(self.root, "a/aa").children)
        ), "Node parent not deleted"

    def test_shift_nodes_merge_children_non_overriding_error(self):
        new_aa = Node("aa", parent=self.root)
        new_bb = Node("bb", parent=new_aa)
        new_cc = Node("cc", age=1)
        new_cc.parent = new_bb
        bb2 = Node("bb")
        cc2 = Node("cc")
        bb2.parent = self.root
        cc2.parent = bb2

        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["aa/bb"]
        to_paths = ["/a/bb"]
        with pytest.raises(TreeError):
            shift_nodes(self.root, from_paths, to_paths, merge_children=True)

    def test_shift_nodes_merge_children_overriding(self):
        new_aa = Node("aa", parent=self.root)
        new_bb = Node("bb", parent=new_aa)
        new_cc = Node("cc", age=1)
        new_cc.parent = new_bb
        bb2 = Node("bb")
        cc2 = Node("cc2")
        bb2.parent = self.root
        cc2.parent = bb2

        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/aa/bb"]
        to_paths = ["/a/bb"]
        shift_nodes(
            self.root, from_paths, to_paths, overriding=True, merge_children=True
        )
        assert (
            len(list(self.root.children)) == 4
        ), f"Node children not merged, {print_tree(self.root)}"
        assert find_path(
            self.root, "a/bb/cc"
        ), "Node children not merged, new children not present"
        assert not find_path(
            self.root, "a/bb/cc2"
        ), "Node children not merged, original children not overridden"
        assert (
            find_path(self.root, "a/bb/cc").get_attr("age") == 1
        ), f"Merged children not overridden, {print_tree(self.root)}"
        assert not len(
            list(find_path(self.root, "a/aa").children)
        ), "Node parent not deleted"

    def test_shift_nodes_overriding(self):
        new_aa = Node("aa", parent=self.root)
        new_bb = Node("bb", parent=new_aa)
        new_cc = Node("cc", age=1)
        new_cc.parent = new_bb
        bb2 = Node("bb")
        cc2 = Node("cc2")
        bb2.parent = self.root
        cc2.parent = bb2

        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/aa/bb"]
        to_paths = ["/a/bb"]
        shift_nodes(
            self.root,
            from_paths,
            to_paths,
            overriding=True,
        )
        assert (
            len(list(self.root.children)) == 4
        ), f"Node children not merged, {print_tree(self.root)}"
        assert find_path(
            self.root, "a/bb/cc"
        ), "Node children not merged, new children not present"
        assert not find_path(
            self.root, "a/bb/cc2"
        ), "Node children not merged, original children not overridden"
        assert (
            find_path(self.root, "a/bb/cc").get_attr("age") == 1
        ), f"Merged children not overridden, {print_tree(self.root)}"
        assert not len(
            list(find_path(self.root, "a/aa").children)
        ), "Node parent not deleted"

    def test_shift_nodes_same_node_error(self):
        from_paths = ["d"]
        to_paths = ["a/d"]
        with pytest.raises(TreeError) as exc_info:
            shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith("Attempting to shift the same node")

    def test_shift_nodes_same_node_merge_children(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["b"]
        to_paths = ["b"]
        shift_nodes(self.root, from_paths, to_paths, merge_children=True)
        assert len(list(self.root.children)) == 3, "Node b is not removed"
        assert not find_path(self.root, "a/b"), "Node b is not removed"
        assert find_path(self.root, "a/c"), "Node c is gone"
        assert find_path(self.root, "a/d"), "Node d parent is not Node a"
        assert find_path(self.root, "a/e"), "Node e parent is not Node a"

    def test_shift_nodes_merge_and_delete_children(self):
        from_paths = ["d", "e", "g", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths)

        h2 = Node("h", age=6)
        h2.children = [Node("i"), Node("j")]
        h = find_name(self.root, "h")
        h2.parent = h
        from_paths = ["a/h"]
        to_paths = ["a/b/e/h"]
        shift_nodes(
            self.root, from_paths, to_paths, merge_children=True, delete_children=True
        )
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_shift_nodes_delete_children(self):
        g = find_name(self.root, "g")
        h = find_name(self.root, "h")
        g.children = [Node("i"), Node("j")]
        h.children = [Node("i"), Node("j")]
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths, delete_children=True)
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_copy_nodes_from_tree_to_tree(self):
        root_other = Node("a", age=90)
        from_paths = ["b", "c", "d", "e", "f", "g", "h"]
        to_paths = ["a/b", "a/c", "a/b/d", "a/b/e", "a/c/f", "a/b/e/g", "a/b/e/h"]
        copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=root_other,
            from_paths=from_paths,
            to_paths=to_paths,
        )
        assert_tree_structure_basenode_root_generic(root_other)
        assert_tree_structure_basenode_root_attr(root_other)
        assert_tree_structure_node_root_generic(root_other)
        assert self.root.max_depth == 2, "Copying changes original tree"

    def test_copy_nodes_from_tree_to_tree_reversed(self):
        root_other = Node("a", age=90)
        from_paths = ["b", "c", "d", "e", "f", "g", "h"][::-1]
        to_paths = ["a/b", "a/c", "a/b/d", "a/b/e", "a/c/f", "a/b/e/g", "a/b/e/h"][::-1]
        with pytest.raises(TreeError) as exc_info:
            copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=root_other,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert "already exists and unable to override" in str(exc_info.value)

    def test_copy_nodes_from_tree_to_tree_merge_children(self):
        from_paths = ["e", "g", "h"]
        to_paths = ["a/bb/e", "a/bb/e/g", "a/bb/e/h"]
        shift_nodes(self.root, from_paths, to_paths)

        root_other = Node("a", age=90)
        b = Node("b", age=65, parent=root_other)
        d = Node("d", age=40)
        d.parent = b
        c = Node("c", age=60, parent=root_other)
        f = Node("f", age=38)
        f.parent = c
        from_paths = ["a/bb"]
        to_paths = ["a/b/bb"]
        copy_nodes_from_tree_to_tree(
            self.root,
            root_other,
            from_paths,
            to_paths,
            merge_children=True,
        )
        assert_tree_structure_basenode_root_generic(root_other)
        assert_tree_structure_basenode_root_attr(root_other)
        assert_tree_structure_node_root_generic(root_other)

    def test_copy_nodes_from_tree_to_tree_merge_children_non_overriding(self):
        from_paths = ["e", "g", "h"]
        to_paths = ["a/b/e", "a/b/e/g", "a/b/e/h"]
        shift_nodes(self.root, from_paths, to_paths)

        root_other = Node("a", age=90)
        b = Node("b", age=65, parent=root_other)
        d = Node("d", age=40)
        d.parent = b
        c = Node("c", age=60, parent=root_other)
        f = Node("f", age=38)
        f.parent = c
        from_paths = ["a/b"]
        to_paths = ["a/b"]
        copy_nodes_from_tree_to_tree(
            self.root,
            root_other,
            from_paths,
            to_paths,
            merge_children=True,
        )
        assert_tree_structure_basenode_root_generic(root_other)
        assert_tree_structure_basenode_root_attr(root_other)
        assert_tree_structure_node_root_generic(root_other)

    def test_copy_nodes_from_tree_to_tree_merge_children_non_overriding_error(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths)

        root_other = Node("a", age=90)
        c = Node("c", parent=root_other)
        f = Node("f")
        f.parent = c
        from_paths = ["a/c"]
        to_paths = ["a/c"]
        with pytest.raises(TreeError):
            copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                from_paths=from_paths,
                to_paths=to_paths,
                merge_children=True,
                to_tree=root_other,
            )

    def test_copy_nodes_from_tree_to_tree_merge_children_overriding(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/bb/d", "a/bb/e", "a/bb/e/g", "a/bb/e/h", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths)

        root_other = Node("a", age=90)
        b = Node("b", age=65)
        c = Node("c", age=1, parent=root_other)
        b.parent = root_other
        f = Node("f")
        f.parent = c
        from_paths = ["a/bb", "a/c"]
        to_paths = ["a/b/bb", "a/c"]
        assert find_path(root_other, "a/b").get_attr("age") == 65
        assert find_path(root_other, "a/c").get_attr("age") == 1

        copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            from_paths=from_paths,
            to_paths=to_paths,
            merge_children=True,
            overriding=True,
            to_tree=root_other,
        )
        assert_tree_structure_basenode_root_generic(root_other)
        assert_tree_structure_basenode_root_attr(root_other)
        assert_tree_structure_node_root_generic(root_other)

    def test_copy_nodes_from_tree_to_tree_overriding(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        shift_nodes(self.root, from_paths, to_paths)

        root_other = Node("a", age=90)
        b = Node("b", age=1)
        c = Node("c", age=1, parent=root_other)
        b.parent = root_other
        f = Node("f")
        f.parent = c
        from_paths = ["a/b", "a/c"]
        to_paths = ["a/b", "a/c"]
        assert find_path(root_other, "a/b").get_attr("age") == 1
        assert find_path(root_other, "a/c").get_attr("age") == 1

        copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            from_paths=from_paths,
            to_paths=to_paths,
            overriding=True,
            to_tree=root_other,
        )
        assert_tree_structure_basenode_root_generic(root_other)
        assert_tree_structure_basenode_root_attr(root_other)
        assert_tree_structure_node_root_generic(root_other)

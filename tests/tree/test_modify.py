import unittest

import pytest

from bigtree.node import node
from bigtree.tree import export, modify, search
from bigtree.utils import exceptions
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
)
from tests.node.test_node import assert_tree_structure_node_root
from tests.test_constants import Constants


class TestCopyNodes(unittest.TestCase):
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

        Tree root should have structure
        a
        ├── b
        ├── c
        ├── d
        ├── e
        ├── f
        ├── g
        └── h

        Tree root_other should have structure
        aa
        ├── b
        ├── c
        ├── d
        ├── e
        ├── f
        ├── g
        └── h

        Tree root_overriding should have structure
        a
        ├── aa
        │   └── bb
        │       └── cc
        │           └── dd
        └── bb
            └── cc2
        """
        a = node.Node(name="a", age=90)
        b = node.Node(name="b", age=65)
        c = node.Node(name="c", age=60)
        d = node.Node(name="d", age=40)
        e = node.Node(name="e", age=35)
        f = node.Node(name="f", age=38)
        g = node.Node(name="g", age=10)
        h = node.Node(name="h", age=6)

        b.parent = a
        c.parent = a
        d.parent = a
        e.parent = a
        f.parent = a
        g.parent = a
        h.parent = a

        self.root = a

        aa = node.Node(name="aa", age=90)
        b = node.Node(name="b", age=65)
        c = node.Node(name="c", age=60)
        d = node.Node(name="d", age=40)
        e = node.Node(name="e", age=35)
        f = node.Node(name="f", age=38)
        g = node.Node(name="g", age=10)
        h = node.Node(name="h", age=6)

        b.parent = aa
        c.parent = aa
        d.parent = aa
        e.parent = aa
        f.parent = aa
        g.parent = aa
        h.parent = aa

        self.root_other = aa

        root_overriding = node.Node("a")
        new_aa = node.Node("aa", parent=root_overriding)
        new_bb = node.Node("bb", parent=new_aa)
        new_cc = node.Node("cc", age=1, parent=new_bb)
        new_dd = node.Node("dd", age=2)
        new_dd.parent = new_cc
        bb2 = node.Node("bb")
        cc2 = node.Node("cc2")
        bb2.parent = root_overriding
        cc2.parent = bb2
        self.root_overriding = root_overriding

    def tearDown(self):
        self.root = None

    def test_copy_nodes(self):
        from_paths = ["d"]
        to_paths = ["a/b/c/d"]
        modify.copy_nodes(self.root, from_paths, to_paths)
        assert self.root.max_depth == 4, "Shift did not create a tree of depth 4"
        assert search.find_path(self.root, "a/d"), "Original node is not there"
        assert search.find_path(self.root, "a/b/c/d"), "Copied node is not there"

    def test_copy_nodes_invalid_type_error(self):
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes(self.root, {}, [])
        assert str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_TYPE

    def test_copy_nodes_unequal_length_error(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes(self.root, from_paths, to_paths)
        assert str(
            exc_info.value
        ) == Constants.ERROR_MODIFY_PARAM_DIFFERENT_PATH_LENGTH.format(
            n1=len(from_paths), n2=len(to_paths)
        )

    def test_copy_nodes_invalid_paths_error(self):
        from_paths = ["d"]
        to_paths = ["a/b/e"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith(Constants.ERROR_MODIFY_PATH_MISMATCH)

    def test_copy_nodes_invalid_from_paths_error(self):
        from_path = "i"
        from_paths = [from_path]
        to_paths = ["a/b/i"]
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            modify.copy_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_FROM_PATH_NOT_FOUND.format(
            from_path=from_path
        )

    def test_copy_nodes_invalid_to_paths_error(self):
        from_paths = ["d"]
        to_paths = ["aa/b/d"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_TO_PATH

    def test_copy_nodes_create_intermediate_path(self):
        from_paths = ["d"]
        to_paths = ["a/b/c/d"]
        modify.copy_nodes(self.root, from_paths, to_paths)
        assert self.root.max_depth == 4, "Shift did not create a tree of depth 4"

    def test_copy_nodes_delete_error(self):
        from_paths = ["d"]
        to_paths = [None]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_DELETE_AND_COPY

        from_paths = ["d"]
        to_paths = [""]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_DELETE_AND_COPY

    # sep
    def test_copy_nodes_leading_sep(self):
        from_paths = ["/d", "e", "g", "/h", "/f"]
        to_paths = ["/a/b/d", "a/b/e", "/a/b/e/g", "a/b/e/h", "/a/c/f"]
        modify.copy_nodes(self.root, from_paths, to_paths)

        # Delete original nodes
        from_paths = ["/a/d", "/a/e", "/a/g", "/a/h", "/a/f"]
        to_paths = [None, None, None, None, None]
        modify.shift_nodes(self.root, from_paths, to_paths)

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_copy_nodes_trailing_sep(self):
        from_paths = ["d", "e/", "g/", "h", "f/"]
        to_paths = ["a/b/d", "a/b/e/", "a/b/e/g/", "a/b/e/h/", "a/c/f"]
        modify.copy_nodes(self.root, from_paths, to_paths)

        # Delete original nodes
        from_paths = ["/a/d", "/a/e", "/a/g", "/a/h", "/a/f"]
        to_paths = [None, None, None, None, None]
        modify.shift_nodes(self.root, from_paths, to_paths)

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_copy_nodes_sep_error(self):
        from_paths = ["\\d", "\\e", "\\g", "\\h", "\\f"]
        to_paths = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith(Constants.ERROR_MODIFY_PATH_MISMATCH)

    def test_copy_nodes_sep(self):
        from_paths = ["\\d", "\\e", "\\g", "\\h", "\\f"]
        to_paths = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        modify.copy_nodes(self.root, from_paths, to_paths, sep="\\")

        # Delete original nodes
        from_paths = ["\\a\\d", "\\a\\e", "\\a\\g", "\\a\\h", "\\a\\f"]
        to_paths = [None, None, None, None, None]
        modify.shift_nodes(self.root, from_paths, to_paths, sep="\\")

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_copy_nodes_sep_different(self):
        # Delete intermediate nodes
        from_paths = ["\\a\\b", "\\a\\c", "\\a\\e"]
        to_paths = [None, None, None]
        modify.shift_nodes(self.root, from_paths, to_paths, sep="\\")

        # Create intermediate nodes
        from_paths = ["\\d", "\\g", "\\h", "\\f"]
        to_paths = ["a\\b\\d", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        modify.copy_nodes(self.root, from_paths, to_paths, sep="\\")

        # Delete original nodes
        from_paths = ["\\a\\d", "\\a\\g", "\\a\\h", "\\a\\f"]
        to_paths = [None, None, None, None]
        modify.shift_nodes(self.root, from_paths, to_paths, sep="\\")

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    # skippable
    def test_copy_nodes_skippable_error(self):
        from_path = "i"
        from_paths = [from_path, "d", "e", "g", "h", "f"]
        to_paths = ["a/c/f/i", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            modify.copy_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_FROM_PATH_NOT_FOUND.format(
            from_path=from_path
        )

        modify.copy_nodes(self.root, from_paths, to_paths, skippable=True)

        # Delete original nodes
        from_paths = ["a/d", "a/e", "a/g", "a/h", "a/f"]
        to_paths = [None, None, None, None, None]
        modify.shift_nodes(self.root, from_paths, to_paths)

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # overriding
    def test_copy_nodes_overriding_error(self):
        to_path = "a/b/d"
        new_aa = node.Node("aa", parent=self.root)
        new_d = node.Node("d")
        new_d.parent = new_aa
        from_paths = ["/a/d", "aa/d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.copy_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_OVERRIDING.format(
            to_path=to_path
        )

    def test_copy_nodes_overriding(self):
        new_aa = node.Node("aa", parent=self.root)
        new_d = node.Node("d", age=1)
        new_d.parent = new_aa
        from_paths = ["/a/d", "aa/d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.copy_nodes(self.root, from_paths, to_paths, overriding=True)

        # Delete original nodes
        from_paths = ["a/aa", "a/d", "a/e", "a/g", "a/h", "a/f"]
        to_paths = [None, None, None, None, None, None]
        modify.shift_nodes(self.root, from_paths, to_paths)

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root, d=("d", 1))
        assert_tree_structure_node_root(self.root)

    def test_copy_nodes_overriding_manual_check(self):
        from_paths = ["a/aa/bb"]
        to_paths = ["/a/bb"]
        modify.copy_nodes(
            self.root_overriding,
            from_paths,
            to_paths,
            overriding=True,
        )
        assert (
            len(list(self.root_overriding.children)) == 2
        ), f"Node children not merged, {export.print_tree(self.root_overriding)}"
        assert search.find_path(
            self.root_overriding, "/a/bb/cc"
        ), "Node children not merged, new children not present"
        assert not search.find_path(
            self.root_overriding, "/a/bb/cc2"
        ), "Node children not merged, original children not overridden"
        assert (
            search.find_path(self.root_overriding, "/a/bb/cc").get_attr("age") == 1
        ), f"Merged children not overridden, {export.print_tree(self.root_overriding)}"
        assert len(
            list(search.find_path(self.root_overriding, "/a/aa").children)
        ), "Children of node parent deleted (not copied)"

    # merge_children
    def test_copy_nodes_merge_children(self):
        from_paths = ["aa/bb/cc"]
        to_paths = ["/a/cc"]
        modify.copy_nodes(
            self.root_overriding, from_paths, to_paths, merge_children=True
        )
        assert len(list(self.root_overriding.children)) == 3
        assert search.find_path(
            self.root_overriding, "a/dd"
        ), "Node children not merged"
        assert (
            search.find_path(self.root_overriding, "a/dd").get_attr("age") == 2
        ), f"Merged children not overridden, {export.print_tree(self.root_overriding)}"
        assert len(
            list(search.find_path(self.root_overriding, "a/aa/bb").children)
        ), "Children of node parent deleted (not copied)"

    def test_copy_nodes_merge_children_non_overriding(self):
        from_paths = ["aa/bb"]
        to_paths = ["/a/bb"]
        modify.copy_nodes(
            self.root_overriding, from_paths, to_paths, merge_children=True
        )
        assert len(list(self.root_overriding.children)) == 2
        assert search.find_path(
            self.root_overriding, "/a/bb/cc/dd"
        ), "Node children not merged"
        assert (
            search.find_path(self.root_overriding, "/a/bb/cc/dd").get_attr("age") == 2
        ), f"Merged children not overridden, {export.print_tree(self.root_overriding)}"
        assert len(
            list(search.find_path(self.root_overriding, "/a/aa").children)
        ), "Children of node parent deleted (not copied)"

    def test_copy_nodes_merge_children_non_overriding_error(self):
        bb = search.find_path(self.root_overriding, "/a/bb")
        cc = node.Node("cc")
        cc.parent = bb

        from_paths = ["aa/bb"]
        to_paths = ["/a/bb"]
        path = "/a/bb/cc"
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.copy_nodes(
                self.root_overriding, from_paths, to_paths, merge_children=True
            )
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_PARENT_PATH.format(
            path=path
        )

    def test_copy_nodes_same_node_error(self):
        from_paths = ["d"]
        to_paths = ["a/d"]
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.copy_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith(Constants.ERROR_MODIFY_SHIFT_SAME_NODE)

    def test_copy_nodes_same_node_merge_children(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["b"]
        to_paths = ["a/b"]
        modify.copy_nodes(self.root, from_paths, to_paths, merge_children=True)
        assert len(list(self.root.children)) == 3, "Node b is not removed"
        assert not search.find_path(self.root, "a/b"), "Node b is not removed"
        assert search.find_path(self.root, "a/c"), "Node c is gone"
        assert search.find_path(self.root, "a/d"), "Node d parent is not Node a"
        assert search.find_path(self.root, "a/e"), "Node e parent is not Node a"

    # merge_leaves
    def test_copy_nodes_merge_leaves(self):
        from_paths = ["a/aa/bb"]
        to_paths = ["/a/cc/bb"]
        modify.copy_nodes(self.root_overriding, from_paths, to_paths, merge_leaves=True)

        assert search.find_path(
            self.root_overriding, "a/aa/bb/cc"
        ), "a/aa/bb/cc path got removed"
        assert search.find_path(
            self.root_overriding, "a/aa/bb/cc/dd"
        ), "dd did not copy (old location not present)"
        assert search.find_path(
            self.root_overriding, "a/cc/dd"
        ), "dd did not shift (new location not present)"

    def test_copy_nodes_merge_leaves_non_overriding(self):
        from_paths = ["a/aa/bb"]
        to_paths = ["/a/bb"]
        modify.copy_nodes(self.root_overriding, from_paths, to_paths, merge_leaves=True)

        assert search.find_path(
            self.root_overriding, "a/aa/bb/cc"
        ), "a/aa/bb/cc path got removed"
        assert search.find_path(
            self.root_overriding, "a/aa/bb/cc/dd"
        ), "dd did not copy (old location not present)"
        assert search.find_path(
            self.root_overriding, "a/bb/dd"
        ), "dd did not shift (new location not present)"
        assert search.find_path(self.root_overriding, "a/bb/cc2"), "cc2 got replaced"

    def test_copy_nodes_merge_leaves_non_overriding_error(self):
        bb = search.find_path(self.root_overriding, "/a/bb")
        dd = node.Node("dd")
        dd.parent = bb

        from_paths = ["a/aa"]
        to_paths = ["/a/bb/aa"]
        path = "/a/bb/dd"
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.copy_nodes(
                self.root_overriding, from_paths, to_paths, merge_leaves=True
            )
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_PARENT_PATH.format(
            path=path
        )

    def test_copy_nodes_same_node_merge_leaves(self):
        a = node.Node("a", age=90)
        self.root_other.parent = a

        from_paths = ["a/aa/d", "a/aa/e", "a/aa/g", "a/aa/h", "a/aa/f"]
        to_paths = ["a/aa/b/d", "a/aa/b/e", "a/aa/b/e/g", "a/aa/b/e/h", "a/aa/c/f"]
        modify.shift_nodes(a, from_paths, to_paths)

        from_paths = ["a/aa"]
        to_paths = ["a/aa"]
        modify.copy_nodes(a, from_paths, to_paths, merge_leaves=True)

        assert [child.node_name for child in a.children] == [
            "aa",
            "d",
            "g",
            "h",
            "f",
        ], f"Tree has children {a.children}, expected ['aa', 'd', 'g', 'h', 'f']"
        assert search.find_path(a, "a/aa/b/d"), "a/aa/b/d path got removed"
        assert search.find_path(a, "a/aa/b/e/g"), "a/aa/b/e/g path got removed"
        assert search.find_path(a, "a/aa/b/e/h"), "a/aa/b/e/h path got removed"
        assert search.find_path(a, "a/aa/c/f"), "a/aa/c/f path got removed"

    # delete_children
    def test_copy_nodes_delete_children(self):
        g = search.find_name(self.root, "g")
        h = search.find_name(self.root, "h")
        g.children = [node.Node("i"), node.Node("j")]
        h.children = [node.Node("i"), node.Node("j")]
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.copy_nodes(self.root, from_paths, to_paths, delete_children=True)

        # Delete original nodes
        from_paths = ["a/d", "a/e", "a/g", "a/h", "a/f"]
        to_paths = [None, None, None, None, None]
        modify.shift_nodes(self.root, from_paths, to_paths)

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # merge_children, overriding
    def test_copy_nodes_merge_children_overriding(self):
        new_aa = node.Node("aa", parent=self.root)
        new_bb = node.Node("bb", parent=new_aa)
        new_cc = node.Node("cc", age=1)
        new_cc.parent = new_bb
        bb2 = node.Node("bb")
        cc2 = node.Node("cc2")
        bb2.parent = self.root
        cc2.parent = bb2

        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/aa/bb"]
        to_paths = ["/a/bb"]
        modify.copy_nodes(
            self.root, from_paths, to_paths, overriding=True, merge_children=True
        )
        assert (
            len(list(self.root.children)) == 4
        ), f"Node children not merged, {export.print_tree(self.root)}"
        assert search.find_path(
            self.root, "/a/bb/cc"
        ), "Node children not merged, new children not present"
        assert not search.find_path(
            self.root, "/a/bb/cc2"
        ), "Node children not merged, original children not overridden"
        assert (
            search.find_path(self.root, "/a/bb/cc").get_attr("age") == 1
        ), f"Merged children not overridden, {export.print_tree(self.root)}"
        assert len(
            list(search.find_path(self.root, "/a/aa").children)
        ), "Node parent deleted"

    # merge_leaves, overriding
    def test_copy_nodes_merge_leaves_overriding(self):
        new_aa = node.Node("aa", parent=self.root)
        new_bb = node.Node("bb", parent=new_aa)
        new_cc = node.Node("cc", age=1)
        new_cc.parent = new_bb
        bb2 = node.Node("bb")
        cc2 = node.Node("cc2")
        bb2.parent = self.root
        cc2.parent = bb2

        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/aa/bb"]
        to_paths = ["/a/bb"]
        modify.copy_nodes(
            self.root, from_paths, to_paths, overriding=True, merge_leaves=True
        )
        assert (
            len(list(self.root.children)) == 4
        ), f"Node children not merged, {export.print_tree(self.root)}"
        assert search.find_path(
            self.root, "/a/bb/cc"
        ), "Node children not merged, new children not present"
        assert not search.find_path(
            self.root, "/a/bb/cc2"
        ), "Node children not merged, original children not overridden"
        assert (
            search.find_path(self.root, "/a/bb/cc").get_attr("age") == 1
        ), f"Merged children not overridden, {export.print_tree(self.root)}"
        assert len(
            list(search.find_path(self.root, "/a/aa").children)
        ), "Node parent deleted"

    # merge_children, merge_leaves
    def test_copy_nodes_merge_children_and_leaf_error(self):
        a = node.Node("a", age=90)
        self.root_other.parent = a

        from_paths = ["a/aa/d", "a/aa/e", "a/aa/g", "a/aa/h", "a/aa/f"]
        to_paths = ["a/aa/b/d", "a/aa/b/e", "a/aa/b/e/g", "a/aa/b/e/h", "a/aa/c/f"]
        modify.shift_nodes(a, from_paths, to_paths)

        from_paths = ["a/aa"]
        to_paths = ["a/bb/aa"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes(
                a, from_paths, to_paths, merge_children=True, merge_leaves=True
            )
        assert (
            str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_MERGE_CHILDREN_OR_LEAVES
        )

    # merge_children, delete_children
    def test_copy_nodes_merge_children_and_delete_children(self):
        from_paths = ["d", "e", "g", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        h2 = node.Node("h", age=6)
        h2.children = [node.Node("i"), node.Node("j")]
        h = search.find_name(self.root, "h")
        h2.parent = h
        from_paths = ["a/h"]
        to_paths = ["a/b/e/h"]
        modify.copy_nodes(
            self.root, from_paths, to_paths, merge_children=True, delete_children=True
        )

        # Delete original nodes
        from_paths = ["a/h"]
        to_paths = [None]
        modify.shift_nodes(self.root, from_paths, to_paths)

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # merge_leaves, delete_children
    def test_copy_nodes_merge_leaves_and_delete_children(self):
        from_paths = ["d", "e", "g", "f", "h"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/c/f", "a/i/j/k/h"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/i"]
        to_paths = ["a/b/e/i"]
        modify.copy_nodes(
            self.root, from_paths, to_paths, merge_leaves=True, delete_children=True
        )
        i = search.find_path(self.root, "a/i")
        i.parent = None
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # with_full_path
    def test_copy_nodes_with_full_path(self):
        from_paths = ["a/d", "a/e", "a/g", "a/h", "a/f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.copy_nodes(self.root, from_paths, to_paths, with_full_path=True)

        # Delete original nodes
        from_paths = ["a/d", "a/e", "a/g", "a/h", "a/f"]
        to_paths = [None, None, None, None, None]
        modify.shift_nodes(self.root, from_paths, to_paths, with_full_path=True)

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_copy_nodes_with_full_path_error(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes(self.root, from_paths, to_paths, with_full_path=True)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_FULL_PATH


class TestShiftNodes(unittest.TestCase):
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

        Tree root should have structure
        a
        ├── b
        ├── c
        ├── d
        ├── e
        ├── f
        ├── g
        └── h

        Tree root_other should have structure
        aa
        ├── b
        ├── c
        ├── d
        ├── e
        ├── f
        ├── g
        └── h

        Tree root_overriding should have structure
        a
        ├── aa
        │   └── bb
        │       └── cc
        │           └── dd
        └── bb
            └── cc2
        """
        a = node.Node(name="a", age=90)
        b = node.Node(name="b", age=65)
        c = node.Node(name="c", age=60)
        d = node.Node(name="d", age=40)
        e = node.Node(name="e", age=35)
        f = node.Node(name="f", age=38)
        g = node.Node(name="g", age=10)
        h = node.Node(name="h", age=6)

        b.parent = a
        c.parent = a
        d.parent = a
        e.parent = a
        f.parent = a
        g.parent = a
        h.parent = a

        self.root = a

        aa = node.Node(name="aa", age=90)
        b = node.Node(name="b", age=65)
        c = node.Node(name="c", age=60)
        d = node.Node(name="d", age=40)
        e = node.Node(name="e", age=35)
        f = node.Node(name="f", age=38)
        g = node.Node(name="g", age=10)
        h = node.Node(name="h", age=6)

        b.parent = aa
        c.parent = aa
        d.parent = aa
        e.parent = aa
        f.parent = aa
        g.parent = aa
        h.parent = aa

        self.root_other = aa

        root_overriding = node.Node("a")
        new_aa = node.Node("aa", parent=root_overriding)
        new_bb = node.Node("bb", parent=new_aa)
        new_cc = node.Node("cc", age=1, parent=new_bb)
        new_dd = node.Node("dd", age=2)
        new_dd.parent = new_cc
        bb2 = node.Node("bb")
        cc2 = node.Node("cc2")
        bb2.parent = root_overriding
        cc2.parent = bb2
        self.root_overriding = root_overriding

    def tearDown(self):
        self.root = None

    def test_shift_nodes(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_shift_nodes_invalid_type_error(self):
        with pytest.raises(ValueError) as exc_info:
            modify.shift_nodes(self.root, {}, [])
        assert str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_TYPE

    def test_shift_nodes_unequal_length_error(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d"]
        with pytest.raises(ValueError) as exc_info:
            modify.shift_nodes(self.root, from_paths, to_paths)
        assert str(
            exc_info.value
        ) == Constants.ERROR_MODIFY_PARAM_DIFFERENT_PATH_LENGTH.format(
            n1=len(from_paths), n2=len(to_paths)
        )

    def test_shift_nodes_invalid_paths_error(self):
        from_paths = ["d"]
        to_paths = ["a/b/e"]
        with pytest.raises(ValueError) as exc_info:
            modify.shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith(Constants.ERROR_MODIFY_PATH_MISMATCH)

    def test_shift_nodes_invalid_from_paths_error(self):
        from_path = "i"
        from_paths = [from_path]
        to_paths = ["a/b/i"]
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            modify.shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_FROM_PATH_NOT_FOUND.format(
            from_path=from_path
        )

    def test_shift_nodes_invalid_to_paths_error(self):
        from_paths = ["d"]
        to_paths = ["aa/b/d"]
        with pytest.raises(ValueError) as exc_info:
            modify.shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_TO_PATH

    def test_shift_nodes_create_intermediate_path(self):
        from_paths = ["d"]
        to_paths = ["a/b/c/d"]
        modify.shift_nodes(self.root, from_paths, to_paths)
        assert self.root.max_depth == 4, "Shift did not create a tree of depth 4"

    # sep
    def test_shift_nodes_leading_sep(self):
        from_paths = ["/d", "e", "g", "/h", "/f"]
        to_paths = ["/a/b/d", "a/b/e", "/a/b/e/g", "a/b/e/h", "/a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_shift_nodes_trailing_sep(self):
        from_paths = ["d/", "e", "g/", "h", "f/"]
        to_paths = ["a/b/d/", "a/b/e", "a/b/e/g", "a/b/e/h/", "a/c/f/"]
        modify.shift_nodes(self.root, from_paths, to_paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_shift_nodes_sep_error(self):
        from_paths = ["\\d", "\\e", "\\g", "\\h", "\\f"]
        to_paths = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        with pytest.raises(ValueError) as exc_info:
            modify.shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith(Constants.ERROR_MODIFY_PATH_MISMATCH)

    def test_shift_nodes_sep(self):
        from_paths = ["\\d", "\\e", "\\g", "\\h", "\\f"]
        to_paths = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        modify.shift_nodes(self.root, from_paths, to_paths, sep="\\")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # skippable
    def test_shift_nodes_skippable_error(self):
        from_path = "i"
        from_paths = [from_path, "d", "e", "g", "h", "f"]
        to_paths = ["a/c/f/i", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            modify.shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_FROM_PATH_NOT_FOUND.format(
            from_path=from_path
        )

        modify.shift_nodes(self.root, from_paths, to_paths, skippable=True)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # overriding
    def test_shift_nodes_overriding_error(self):
        to_path = "a/b/d"
        new_aa = node.Node("aa", parent=self.root)
        new_d = node.Node("d")
        new_d.parent = new_aa
        from_paths = ["/a/d", "aa/d", "e", "g", "h", "f", "a/aa"]
        to_paths = ["a/b/d", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f", None]
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_OVERRIDING.format(
            to_path=to_path
        )

    def test_shift_nodes_overriding(self):
        new_aa = node.Node("aa", parent=self.root)
        new_d = node.Node("d", age=1)
        new_d.parent = new_aa
        from_paths = ["/a/d", "aa/d", "e", "g", "h", "f", "a/aa"]
        to_paths = ["a/b/d", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f", None]
        modify.shift_nodes(self.root, from_paths, to_paths, overriding=True)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root, d=("d", 1))
        assert_tree_structure_node_root(self.root)

    def test_shift_nodes_overriding_manual_check(self):
        from_paths = ["a/aa/bb"]
        to_paths = ["/a/bb"]
        modify.shift_nodes(
            self.root_overriding,
            from_paths,
            to_paths,
            overriding=True,
        )
        assert (
            len(list(self.root_overriding.children)) == 2
        ), f"Node children not merged, {export.print_tree(self.root_overriding)}"
        assert search.find_path(
            self.root_overriding, "a/bb/cc"
        ), "Node children not merged, new children not present"
        assert not search.find_path(
            self.root_overriding, "a/bb/cc2"
        ), "Node children not merged, original children not overridden"
        assert (
            search.find_path(self.root_overriding, "a/bb/cc").get_attr("age") == 1
        ), f"Merged children not overridden, {export.print_tree(self.root_overriding)}"
        assert not len(
            list(search.find_path(self.root_overriding, "a/aa").children)
        ), "Children of node parent not deleted"

    # merge_children
    def test_shift_nodes_merge_children(self):
        from_paths = ["aa/bb/cc"]
        to_paths = ["/a/cc"]
        modify.shift_nodes(
            self.root_overriding, from_paths, to_paths, merge_children=True
        )
        assert len(list(self.root_overriding.children)) == 3
        assert search.find_path(
            self.root_overriding, "a/dd"
        ), "Node children not merged"
        assert (
            search.find_path(self.root_overriding, "a/dd").get_attr("age") == 2
        ), f"Merged children not overridden, {export.print_tree(self.root_overriding)}"
        assert not len(
            list(search.find_path(self.root_overriding, "a/aa/bb").children)
        ), "Children of node parent not deleted"

    def test_shift_nodes_merge_children_non_overriding(self):
        from_paths = ["aa/bb"]
        to_paths = ["/a/bb"]
        modify.shift_nodes(
            self.root_overriding, from_paths, to_paths, merge_children=True
        )
        assert len(list(self.root_overriding.children)) == 2
        assert search.find_path(
            self.root_overriding, "a/bb/cc/dd"
        ), "Node children not merged"
        assert (
            search.find_path(self.root_overriding, "a/bb/cc/dd").get_attr("age") == 2
        ), f"Merged children not overridden, {export.print_tree(self.root_overriding)}"
        assert not len(
            list(search.find_path(self.root_overriding, "a/aa").children)
        ), "Children of node parent not deleted"

    def test_shift_nodes_merge_children_non_overriding_error(self):
        bb = search.find_path(self.root_overriding, "/a/bb")
        cc = node.Node("cc")
        cc.parent = bb

        from_paths = ["aa/bb"]
        to_paths = ["/a/bb"]
        path = "/a/bb/cc"
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.shift_nodes(
                self.root_overriding, from_paths, to_paths, merge_children=True
            )
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_PARENT_PATH.format(
            path=path
        )

    def test_shift_nodes_same_node_error(self):
        from_paths = ["d"]
        to_paths = ["a/d"]
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.shift_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith(Constants.ERROR_MODIFY_SHIFT_SAME_NODE)

    def test_shift_nodes_same_node_merge_children(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["b"]
        to_paths = ["a/b"]
        modify.shift_nodes(self.root, from_paths, to_paths, merge_children=True)
        assert len(list(self.root.children)) == 3, "Node b is not removed"
        assert not search.find_path(self.root, "a/b"), "Node b is not removed"
        assert search.find_path(self.root, "a/c"), "Node c is gone"
        assert search.find_path(self.root, "a/d"), "Node d parent is not Node a"
        assert search.find_path(self.root, "a/e"), "Node e parent is not Node a"

    # merge_leaves
    def test_shift_nodes_merge_leaves(self):
        from_paths = ["a/aa/bb"]
        to_paths = ["/a/cc/bb"]
        modify.shift_nodes(
            self.root_overriding, from_paths, to_paths, merge_leaves=True
        )

        assert search.find_path(
            self.root_overriding, "a/aa/bb/cc"
        ), "a/aa/bb/cc path got removed"
        assert not search.find_path(
            self.root_overriding, "a/aa/bb/cc/dd"
        ), "dd did not shift (old location still present)"
        assert search.find_path(
            self.root_overriding, "a/cc/dd"
        ), "dd did not shift (new location not present)"

    def test_shift_nodes_merge_leaves_non_overriding(self):
        from_paths = ["a/aa/bb"]
        to_paths = ["/a/bb"]
        modify.shift_nodes(
            self.root_overriding, from_paths, to_paths, merge_leaves=True
        )

        assert search.find_path(
            self.root_overriding, "a/aa/bb/cc"
        ), "a/aa/bb/cc path got removed"
        assert not search.find_path(
            self.root_overriding, "a/aa/bb/cc/dd"
        ), "dd did not shift (old location still present)"
        assert search.find_path(
            self.root_overriding, "a/bb/dd"
        ), "dd did not shift (new location not present)"
        assert search.find_path(self.root_overriding, "a/bb/cc2"), "cc2 got replaced"

    def test_shift_nodes_merge_leaves_non_overriding_error(self):
        bb = search.find_path(self.root_overriding, "/a/bb")
        dd = node.Node("dd")
        dd.parent = bb

        from_paths = ["a/aa"]
        to_paths = ["/a/bb/aa"]
        path = "/a/bb/dd"
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.shift_nodes(
                self.root_overriding, from_paths, to_paths, merge_leaves=True
            )
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_PARENT_PATH.format(
            path=path
        )

    def test_shift_nodes_same_node_merge_leaves(self):
        a = node.Node("a", age=90)
        self.root_other.parent = a

        from_paths = ["a/aa/d", "a/aa/e", "a/aa/g", "a/aa/h", "a/aa/f"]
        to_paths = ["a/aa/b/d", "a/aa/b/e", "a/aa/b/e/g", "a/aa/b/e/h", "a/aa/c/f"]
        modify.shift_nodes(a, from_paths, to_paths)

        from_paths = ["a/aa"]
        to_paths = ["a/aa"]
        modify.shift_nodes(a, from_paths, to_paths, merge_leaves=True)
        assert [child.node_name for child in a.children] == [
            "aa",
            "d",
            "g",
            "h",
            "f",
        ], f"Tree has children {a.children}, expected ['aa', 'd', 'g', 'h', 'f']"
        assert search.find_path(a, "a/aa/b/e"), "a/aa/b/e path got removed"
        assert search.find_path(a, "a/aa/c"), "a/aa/c path got removed"
        assert not len(
            search.find_path(a, "a/aa/b/e").children
        ), "Leaf nodes of a/aa/b/e did not get shifted"
        assert not len(
            search.find_path(a, "a/aa/c").children
        ), "Leaf nodes of a/aa/c did not get shifted"

    # delete_children
    def test_shift_nodes_delete_children(self):
        g = search.find_name(self.root, "g")
        h = search.find_name(self.root, "h")
        g.children = [node.Node("i"), node.Node("j")]
        h.children = [node.Node("i"), node.Node("j")]
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths, delete_children=True)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # merge_children, overriding
    def test_shift_nodes_merge_children_overriding(self):
        new_aa = node.Node("aa", parent=self.root)
        new_bb = node.Node("bb", parent=new_aa)
        new_cc = node.Node("cc", age=1)
        new_cc.parent = new_bb
        bb2 = node.Node("bb")
        cc2 = node.Node("cc2")
        bb2.parent = self.root
        cc2.parent = bb2

        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/aa/bb"]
        to_paths = ["/a/bb"]
        modify.shift_nodes(
            self.root, from_paths, to_paths, overriding=True, merge_children=True
        )
        assert (
            len(list(self.root.children)) == 4
        ), f"Node children not merged, {export.print_tree(self.root)}"
        assert search.find_path(
            self.root, "a/bb/cc"
        ), "Node children not merged, new children not present"
        assert not search.find_path(
            self.root, "a/bb/cc2"
        ), "Node children not merged, original children not overridden"
        assert (
            search.find_path(self.root, "a/bb/cc").get_attr("age") == 1
        ), f"Merged children not overridden, {export.print_tree(self.root)}"
        assert not len(
            list(search.find_path(self.root, "a/aa").children)
        ), "Node parent not deleted"

    # merge_leaves, overriding
    def test_shift_nodes_merge_leaves_overriding(self):
        new_aa = node.Node("aa", parent=self.root)
        new_bb = node.Node("bb", parent=new_aa)
        new_cc = node.Node("cc", age=1)
        new_cc.parent = new_bb
        bb2 = node.Node("bb")
        cc2 = node.Node("cc2")
        bb2.parent = self.root
        cc2.parent = bb2

        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/aa/bb"]
        to_paths = ["/a/bb"]
        modify.shift_nodes(
            self.root, from_paths, to_paths, overriding=True, merge_leaves=True
        )
        assert (
            len(list(self.root.children)) == 4
        ), f"Node children not merged, {export.print_tree(self.root)}"
        assert search.find_path(
            self.root, "a/bb/cc"
        ), "Node children not merged, new children not present"
        assert not search.find_path(
            self.root, "a/bb/cc2"
        ), "Node children not merged, original children not overridden"
        assert (
            search.find_path(self.root, "a/bb/cc").get_attr("age") == 1
        ), f"Merged children not overridden, {export.print_tree(self.root)}"
        assert len(
            list(search.find_path(self.root, "a/aa").children)
        ), "Node parent deleted"

    # merge_children, merge_leaves
    def test_shift_nodes_merge_children_and_leaf_error(self):
        a = node.Node("a", age=90)
        self.root_other.parent = a

        from_paths = ["a/aa/d", "a/aa/e", "a/aa/g", "a/aa/h", "a/aa/f"]
        to_paths = ["a/aa/b/d", "a/aa/b/e", "a/aa/b/e/g", "a/aa/b/e/h", "a/aa/c/f"]
        modify.shift_nodes(a, from_paths, to_paths)

        from_paths = ["a/aa"]
        to_paths = ["a/bb/aa"]
        with pytest.raises(ValueError) as exc_info:
            modify.shift_nodes(
                a, from_paths, to_paths, merge_children=True, merge_leaves=True
            )
        assert (
            str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_MERGE_CHILDREN_OR_LEAVES
        )

    # merge_children, delete_children
    def test_shift_nodes_merge_children_and_delete_children(self):
        from_paths = ["d", "e", "g", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        h2 = node.Node("h", age=6)
        h2.children = [node.Node("i"), node.Node("j")]
        h = search.find_name(self.root, "h")
        h2.parent = h
        from_paths = ["a/h"]
        to_paths = ["a/b/e/h"]
        modify.shift_nodes(
            self.root, from_paths, to_paths, merge_children=True, delete_children=True
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # merge_leaves, delete_children
    def test_shift_nodes_merge_leaves_and_delete_children(self):
        from_paths = ["d", "e", "g", "f", "h"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/c/f", "a/i/j/k/h"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/i"]
        to_paths = ["a/b/e/i"]
        modify.shift_nodes(
            self.root, from_paths, to_paths, merge_leaves=True, delete_children=True
        )
        i = search.find_path(self.root, "a/i")
        i.parent = None
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # with_full_path
    def test_shift_nodes_with_full_path(self):
        from_paths = ["a/d", "a/e", "a/g", "a/h", "a/f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths, with_full_path=True)

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_shift_nodes_with_full_path_error(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        with pytest.raises(ValueError) as exc_info:
            modify.shift_nodes(self.root, from_paths, to_paths, with_full_path=True)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_FULL_PATH


class TestShiftAndReplaceNodes(unittest.TestCase):
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

        Tree root should have structure
        a
        ├── b
        │   ├── c
        │   │   └── f
        │   ├── d
        │   └── ee
        ├── cc
        └── e
            ├── g
            └── h
        """
        a = node.Node(name="a", age=90)
        b = node.Node(name="b", age=65)
        cc = node.Node(name="cc", age=60)
        c = node.Node(name="c", age=60)
        d = node.Node(name="d", age=40)
        ee = node.Node(name="ee", age=35)
        e = node.Node(name="e", age=35)
        f = node.Node(name="f", age=38)
        g = node.Node(name="g", age=10)
        h = node.Node(name="h", age=6)

        b.parent = a
        cc.parent = a
        c.parent = b
        d.parent = b
        ee.parent = b
        e.parent = a
        f.parent = c
        g.parent = e
        h.parent = e

        self.root = a

    def tearDown(self):
        self.root = None

    def test_shift_and_replace_nodes(self):
        from_paths = ["/e", "/c"]
        to_paths = ["a/b/ee", "a/cc"]
        modify.shift_and_replace_nodes(self.root, from_paths, to_paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_shift_and_replace_nodes_invalid_type_error(self):
        with pytest.raises(ValueError) as exc_info:
            modify.shift_and_replace_nodes(self.root, {}, [])
        assert str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_TYPE

    def test_shift_and_replace_nodes_unequal_length_error(self):
        from_paths = ["/e", "/c"]
        to_paths = ["a/b/ee"]
        with pytest.raises(ValueError) as exc_info:
            modify.shift_and_replace_nodes(self.root, from_paths, to_paths)
        assert str(
            exc_info.value
        ) == Constants.ERROR_MODIFY_PARAM_DIFFERENT_PATH_LENGTH.format(
            n1=len(from_paths), n2=len(to_paths)
        )

    def test_shift_and_replace_nodes_invalid_from_paths_error(self):
        from_path = "i"
        from_paths = [from_path]
        to_paths = ["a/b/ee"]
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            modify.shift_and_replace_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_FROM_PATH_NOT_FOUND.format(
            from_path=from_path
        )

    def test_shift_and_replace_nodes_invalid_to_paths_error(self):
        from_paths = ["/e"]
        to_paths = ["aa/b/ee"]
        with pytest.raises(ValueError) as exc_info:
            modify.shift_and_replace_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_TO_PATH

    # sep
    def test_shift_and_replace_nodes_leading_sep(self):
        from_paths = ["/e", "/c"]
        to_paths = ["/a/b/ee", "/a/cc"]
        modify.shift_and_replace_nodes(self.root, from_paths, to_paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_shift_and_replace_nodes_trailing_sep(self):
        from_paths = ["/e/", "/c"]
        to_paths = ["a/b/ee", "a/cc/"]
        modify.shift_and_replace_nodes(self.root, from_paths, to_paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_shift_and_replace_nodes_sep_error(self):
        from_paths = ["\\e", "\\c"]
        to_paths = ["a\\b\\ee", "a\\cc"]
        with pytest.raises(ValueError) as exc_info:
            modify.shift_and_replace_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_TO_PATH

    def test_shift_and_replace_nodes_sep(self):
        from_paths = ["\\e", "\\c"]
        to_paths = ["a\\b\\ee", "a\\cc"]
        modify.shift_and_replace_nodes(self.root, from_paths, to_paths, sep="\\")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # skippable
    def test_shift_and_replace_nodes_skippable_error(self):
        from_path = "i"
        from_paths = [from_path, "/e/", "/c"]
        to_paths = ["a/b", "a/b/ee", "a/cc/"]
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            modify.shift_and_replace_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_FROM_PATH_NOT_FOUND.format(
            from_path=from_path
        )

        modify.shift_and_replace_nodes(self.root, from_paths, to_paths, skippable=True)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # same node
    def test_shift_and_replace_nodes_same_node_error(self):
        from_paths = ["/e/"]
        to_paths = ["a/e"]
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.shift_and_replace_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value).startswith(Constants.ERROR_MODIFY_REPLACE_SAME_NODE)

    # invalid to path
    def test_shift_and_replace_nodes_to_path_error(self):
        to_path = "a/ee"
        from_paths = ["/e/"]
        to_paths = [to_path]
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            modify.shift_and_replace_nodes(self.root, from_paths, to_paths)
        assert str(exc_info.value) == Constants.ERROR_MODIFY_TO_PATH_NOT_FOUND.format(
            to_path=to_path
        )

    # delete_children
    def test_shift_and_replace_nodes_delete_children(self):
        d = search.find_name(self.root, "d")
        h = search.find_name(self.root, "h")
        d.children = [node.Node("i"), node.Node("j")]
        h.children = [node.Node("d", age=40, children=[node.Node("k")])]
        from_paths = ["/e/", "/c"]
        to_paths = ["a/b/ee", "a/cc/"]
        modify.shift_and_replace_nodes(self.root, from_paths, to_paths)

        from_paths = ["h/d"]
        to_paths = ["a/b/d"]
        modify.shift_and_replace_nodes(
            self.root, from_paths, to_paths, delete_children=True
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # with_full_path
    def test_shift_and_replace_nodes_with_full_path(self):
        from_paths = ["a/e/", "a/b/c"]
        to_paths = ["a/b/ee", "a/cc"]
        modify.shift_and_replace_nodes(
            self.root, from_paths, to_paths, with_full_path=True
        )

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_shift_and_replace_nodes_with_full_path_error(self):
        from_paths = ["/e/", "a/b/c"]
        to_paths = ["a/b/ee", "a/cc"]
        with pytest.raises(ValueError) as exc_info:
            modify.shift_and_replace_nodes(
                self.root, from_paths, to_paths, with_full_path=True
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_FULL_PATH


class TestCopyNodesTwoTrees(unittest.TestCase):
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

        Tree root should have structure
        a [age=90]
        ├── b [age=65]
        ├── c [age=60]
        ├── d [age=40]
        ├── e [age=35]
        ├── f [age=38]
        ├── g [age=10]
        └── h [age=6]

        Tree root_other should have structure
        a [age=90]

        Tree root_other_full should have structure
        a [age=90]
        ├── b [age=65]
        │   └── d [age=40]
        └── c [age=60]
            └── f [age=38]

        Tree root_other_full_wrong should have structure
        a [age=90]
        ├── b [age=65]
        └── c [age=1]
            └── f
        """
        a = node.Node(name="a", age=90)
        b = node.Node(name="b", age=65)
        c = node.Node(name="c", age=60)
        d = node.Node(name="d", age=40)
        e = node.Node(name="e", age=35)
        f = node.Node(name="f", age=38)
        g = node.Node(name="g", age=10)
        h = node.Node(name="h", age=6)

        b.parent = a
        c.parent = a
        d.parent = a
        e.parent = a
        f.parent = a
        g.parent = a
        h.parent = a

        self.root = a

        root_other = node.Node("a", age=90)
        self.root_other = root_other

        root_other_full = node.Node("a", age=90)
        b = node.Node("b", age=65, parent=root_other_full)
        d = node.Node("d", age=40)
        d.parent = b
        c = node.Node("c", age=60, parent=root_other_full)
        f = node.Node("f", age=38)
        f.parent = c
        self.root_other_full = root_other_full

        root_other_full_wrong = node.Node("a", age=90)
        b = node.Node("b", age=65)
        b.parent = root_other_full_wrong
        c = node.Node("c", age=1, parent=root_other_full_wrong)
        f = node.Node("f")
        f.parent = c
        self.root_other_full_wrong = root_other_full_wrong

    def tearDown(self):
        self.root = None

    def test_copy_nodes_from_tree_to_tree(self):
        from_paths = ["b", "c", "d", "e", "f", "g", "h"]
        to_paths = ["a/b", "a/c", "a/b/d", "a/b/e", "a/c/f", "a/b/e/g", "a/b/e/h"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other,
            from_paths=from_paths,
            to_paths=to_paths,
        )
        assert_tree_structure_basenode_root(self.root_other)
        assert_tree_structure_basenode_root_attr(self.root_other)
        assert_tree_structure_node_root(self.root_other)
        assert self.root.max_depth == 2, "Copying changes original tree"

    def test_copy_nodes_from_tree_to_tree_reverse_error(self):
        to_path = "a/b/e"
        from_paths = ["b", "c", "d", "e", "f", "g", "h"][::-1]
        to_paths = ["a/b", "a/c", "a/b/d", "a/b/e", "a/c/f", "a/b/e/g", "a/b/e/h"][::-1]
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_OVERRIDING.format(
            to_path=to_path
        )

    def test_copy_nodes_from_tree_to_tree_invalid_type_error(self):
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths={},
                to_paths=[],
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_TYPE

    def test_copy_nodes_from_tree_to_tree_unequal_length_error(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(
            exc_info.value
        ) == Constants.ERROR_MODIFY_PARAM_DIFFERENT_PATH_LENGTH.format(
            n1=len(from_paths), n2=len(to_paths)
        )

    def test_copy_nodes_from_tree_to_tree_invalid_paths_error(self):
        from_paths = ["d"]
        to_paths = ["a/b/e"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value).startswith(Constants.ERROR_MODIFY_PATH_MISMATCH)

    def test_copy_nodes_from_tree_to_tree_invalid_from_paths_error(self):
        from_path = "i"
        from_paths = [from_path]
        to_paths = ["a/b/i"]
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_FROM_PATH_NOT_FOUND.format(
            from_path=from_path
        )

    def test_copy_nodes_from_tree_to_tree_invalid_to_paths_error(self):
        from_paths = ["d"]
        to_paths = ["aa/b/d"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_TO_PATH

    def test_copy_nodes_create_intermediate_path(self):
        from_paths = ["d"]
        to_paths = ["a/b/c/d"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other,
            from_paths=from_paths,
            to_paths=to_paths,
        )
        assert self.root_other.max_depth == 4, "Shift did not create a tree of depth 4"

    def test_copy_nodes_from_tree_to_tree_delete_error(self):
        from_paths = ["d"]
        to_paths = [None]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_DELETE_AND_COPY

        from_paths = ["d"]
        to_paths = [""]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_DELETE_AND_COPY

    # sep
    def test_copy_nodes_from_tree_to_tree_leading_sep(self):
        from_paths = ["/b", "c", "/d", "e", "g", "h", "f"]
        to_paths = [
            "/a/b",
            "a/c",
            "a/b/d",
            "/a/b/e",
            "a/b/e/g",
            "a/b/e/h",
            "a/c/f",
        ]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other,
            from_paths=from_paths,
            to_paths=to_paths,
        )

        assert_tree_structure_basenode_root(self.root_other)
        assert_tree_structure_basenode_root_attr(self.root_other)
        assert_tree_structure_node_root(self.root_other)

    def test_copy_nodes_from_tree_to_tree_different_sep(self):
        from_paths = ["b/", "c", "d/", "e", "g", "h", "f"]
        to_paths = [
            "a/b/",
            "a/c",
            "a/b/d",
            "a/b/e/",
            "a/b/e/g",
            "a/b/e/h",
            "a/c/f",
        ]
        self.root_other.sep = "\\"
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other,
            from_paths=from_paths,
            to_paths=to_paths,
        )
        self.root_other.sep = "/"

        assert_tree_structure_basenode_root(self.root_other)
        assert_tree_structure_basenode_root_attr(self.root_other)
        assert_tree_structure_node_root(self.root_other)

    def test_copy_nodes_from_tree_to_tree_trailing_sep(self):
        from_paths = ["b/", "c", "d/", "e", "g", "h", "f"]
        to_paths = [
            "a/b/",
            "a/c",
            "a/b/d",
            "a/b/e/",
            "a/b/e/g",
            "a/b/e/h",
            "a/c/f",
        ]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other,
            from_paths=from_paths,
            to_paths=to_paths,
        )

        assert_tree_structure_basenode_root(self.root_other)
        assert_tree_structure_basenode_root_attr(self.root_other)
        assert_tree_structure_node_root(self.root_other)

    def test_copy_nodes_from_tree_to_tree_sep_error(self):
        from_paths = ["\\d", "\\e", "\\g", "\\h", "\\f"]
        to_paths = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value).startswith(Constants.ERROR_MODIFY_PATH_MISMATCH)

    def test_copy_nodes_from_tree_to_tree_sep(self):
        from_paths = ["\\b", "\\c", "\\d", "\\e", "\\g", "\\h", "\\f"]
        to_paths = [
            "a\\b",
            "a\\c",
            "a\\b\\d",
            "a\\b\\e",
            "a\\b\\e\\g",
            "a\\b\\e\\h",
            "a\\c\\f",
        ]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other,
            from_paths=from_paths,
            to_paths=to_paths,
            sep="\\",
        )

        assert_tree_structure_basenode_root(self.root_other)
        assert_tree_structure_basenode_root_attr(self.root_other)
        assert_tree_structure_node_root(self.root_other)

    # skippable
    def test_copy_nodes_skippable_error(self):
        from_path = "i"
        from_paths = [from_path, "b", "c", "d", "e", "g", "h", "f"]
        to_paths = [
            "a/c/f/i",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/b/e/g",
            "a/b/e/h",
            "a/c/f",
        ]
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_FROM_PATH_NOT_FOUND.format(
            from_path=from_path
        )

        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other,
            from_paths=from_paths,
            to_paths=to_paths,
            skippable=True,
        )

        assert_tree_structure_basenode_root(self.root_other)
        assert_tree_structure_basenode_root_attr(self.root_other)
        assert_tree_structure_node_root(self.root_other)

    # overriding
    def test_copy_nodes_from_tree_to_tree_overriding_error(self):
        new_aa = node.Node("aa", parent=self.root)
        new_d = node.Node("d")
        new_d.parent = new_aa
        from_paths = ["/a/d", "aa/d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        to_path = "a/b/d"
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_OVERRIDING.format(
            to_path=to_path
        )

    def test_copy_nodes_from_tree_to_tree_overriding(self):
        new_aa = node.Node("aa", parent=self.root)
        new_d = node.Node("d", age=1)
        new_d.parent = new_aa
        from_paths = ["a/b", "a/c", "/a/d", "aa/d", "e", "g", "h", "f"]
        to_paths = [
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/d",
            "a/b/e",
            "a/b/e/g",
            "a/b/e/h",
            "a/c/f",
        ]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other,
            from_paths=from_paths,
            to_paths=to_paths,
            overriding=True,
        )
        assert_tree_structure_basenode_root(self.root_other)
        assert_tree_structure_basenode_root_attr(self.root_other, d=("d", 1))
        assert_tree_structure_node_root(self.root_other)

    def test_copy_nodes_from_tree_to_tree_overriding_manual_check(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/b", "a/c"]
        to_paths = ["a/b", "a/c"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other_full_wrong,
            from_paths=from_paths,
            to_paths=to_paths,
            overriding=True,
        )
        assert_tree_structure_basenode_root(self.root_other_full_wrong)
        assert_tree_structure_basenode_root_attr(self.root_other_full_wrong)
        assert_tree_structure_node_root(self.root_other_full_wrong)

    # merge_children
    def test_copy_nodes_from_tree_to_tree_merge_children(self):
        from_paths = ["e", "g", "h"]
        to_paths = ["a/bb/e", "a/bb/e/g", "a/bb/e/h"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/bb"]
        to_paths = ["a/b/bb"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other_full,
            from_paths=from_paths,
            to_paths=to_paths,
            merge_children=True,
        )
        assert_tree_structure_basenode_root(self.root_other_full)
        assert_tree_structure_basenode_root_attr(self.root_other_full)
        assert_tree_structure_node_root(self.root_other_full)

    def test_copy_nodes_from_tree_to_tree_merge_children_non_overriding(self):
        from_paths = ["e", "g", "h"]
        to_paths = ["a/b/e", "a/b/e/g", "a/b/e/h"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/b"]
        to_paths = ["a/b"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other_full,
            from_paths=from_paths,
            to_paths=to_paths,
            merge_children=True,
        )
        assert_tree_structure_basenode_root(self.root_other_full)
        assert_tree_structure_basenode_root_attr(self.root_other_full)
        assert_tree_structure_node_root(self.root_other_full)

    def test_copy_nodes_from_tree_to_tree_merge_children_non_overriding_error(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/c"]
        to_paths = ["a/c"]
        path = "/a/c/f"
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other_full,
                from_paths=from_paths,
                to_paths=to_paths,
                merge_children=True,
            )
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_PARENT_PATH.format(
            path=path
        )

    # merge_leaves
    def test_copy_nodes_from_tree_to_tree_merge_leaves(self):
        from_paths = ["a"]
        to_paths = ["a/b/a"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other,
            from_paths=from_paths,
            to_paths=to_paths,
            merge_leaves=True,
        )
        assert (
            self.root_other.max_depth == 3
        ), f"Depth is wrong, expected 3, received {self.root_other.depth}"
        assert [
            _node.node_name
            for _node in search.find_path(self.root_other, "a/b").children
        ] == [
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
        ], "Nodes are not copied"

    def test_copy_nodes_from_tree_to_tree_merge_leaves_non_overriding(self):
        from_paths = ["a/e", "a/g", "a/h"]
        to_paths = ["/a/b/e", "a/c/g", "a/c/h"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/b", "a/c"]
        to_paths = ["/a/b", "a/b/e/c"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other_full,
            from_paths=from_paths,
            to_paths=to_paths,
            merge_leaves=True,
        )
        assert_tree_structure_basenode_root(self.root_other_full)
        assert_tree_structure_basenode_root_attr(self.root_other_full)
        assert_tree_structure_node_root(self.root_other_full)

    def test_copy_nodes_from_tree_to_tree_merge_leaves_non_overriding_error(self):
        from_paths = ["a/d", "a/e", "a/g", "a/h"]
        to_paths = ["a/b/d", "/a/b/e", "a/c/g", "a/c/h"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/b", "a/c"]
        to_paths = ["/a/b", "a/b/e/c"]
        path = "/a/b/d"
        with pytest.raises(exceptions.TreeError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other_full,
                from_paths=from_paths,
                to_paths=to_paths,
                merge_leaves=True,
            )
        assert str(exc_info.value) == Constants.ERROR_NODE_SAME_PARENT_PATH.format(
            path=path
        )

    # delete_children
    def test_copy_nodes_from_tree_to_tree_delete_children(self):
        from_paths = ["a/b", "a/c", "a/d", "a/f"]
        to_paths = ["a/e/b", "a/e/b/c", "a/g/d", "a/h/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/e", "a/g", "a/h"]
        to_paths = ["/a/b/e", "a/b/e/g", "a/b/e/h"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other_full,
            from_paths=from_paths,
            to_paths=to_paths,
            delete_children=True,
        )
        assert_tree_structure_basenode_root(self.root_other_full)
        assert_tree_structure_basenode_root_attr(self.root_other_full)
        assert_tree_structure_node_root(self.root_other_full)

    # merge_children, overriding
    def test_copy_nodes_from_tree_to_tree_merge_children_overriding(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/bb/d", "a/bb/e", "a/bb/e/g", "a/bb/e/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/bb", "a/c"]
        to_paths = ["a/b/bb", "a/c"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other_full_wrong,
            from_paths=from_paths,
            to_paths=to_paths,
            merge_children=True,
            overriding=True,
        )
        assert_tree_structure_basenode_root(self.root_other_full_wrong)
        assert_tree_structure_basenode_root_attr(self.root_other_full_wrong)
        assert_tree_structure_node_root(self.root_other_full_wrong)

    # merge_leaves, overriding
    def test_copy_nodes_from_tree_to_tree_merge_leaves_overriding(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/bb/d", "a/bb/e", "a/cc/g", "a/cc/h", "a/c/f"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/bb", "a/cc", "a/c"]
        to_paths = ["a/b/bb", "a/b/e/cc", "a/c"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other_full_wrong,
            from_paths=from_paths,
            to_paths=to_paths,
            merge_leaves=True,
            overriding=True,
        )
        assert_tree_structure_basenode_root(self.root_other_full_wrong)
        assert_tree_structure_basenode_root_attr(self.root_other_full_wrong, c=("c", 1))
        assert_tree_structure_node_root(self.root_other_full_wrong)

    # merge_children, merge_leaves
    def test_copy_nodes_from_tree_to_tree_merge_children_and_leaf_error(self):
        from_paths = ["a"]
        to_paths = ["a"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other_full_wrong,
                from_paths=from_paths,
                to_paths=to_paths,
                merge_children=True,
                merge_leaves=True,
            )
        assert (
            str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_MERGE_CHILDREN_OR_LEAVES
        )

    # merge_children, delete_children
    def test_copy_nodes_from_tree_to_tree_merge_children_and_delete_children(self):
        from_paths = ["e", "/b", "g", "/c", "h", "d", "f"]
        to_paths = [
            "a/bb/e",
            "a/bb/e/b",
            "a/cc/g",
            "a/cc/g/c",
            "a/cc/h",
            "a/cc/h/d",
            "a/cc/h/f",
        ]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/bb", "a/cc"]
        to_paths = ["a/b/bb", "a/b/e/cc"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other_full,
            from_paths=from_paths,
            to_paths=to_paths,
            merge_children=True,
            delete_children=True,
        )
        assert_tree_structure_basenode_root(self.root_other_full)
        assert_tree_structure_basenode_root_attr(self.root_other_full)
        assert_tree_structure_node_root(self.root_other_full)

    # merge_leaves, delete_children
    def test_copy_nodes_from_tree_to_tree_merge_leaves_and_delete_children(self):
        from_paths = ["a/e", "a/g", "a/h"]
        to_paths = ["/a/b/e", "a/c/g", "a/c/h"]
        modify.shift_nodes(self.root, from_paths, to_paths)

        from_paths = ["a/b", "a/c"]
        to_paths = ["/a/b", "a/b/e/c"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other_full,
            from_paths=from_paths,
            to_paths=to_paths,
            merge_leaves=True,
            delete_children=True,
        )
        assert_tree_structure_basenode_root(self.root_other_full)
        assert_tree_structure_basenode_root_attr(self.root_other_full)
        assert_tree_structure_node_root(self.root_other_full)

    # with_full_path
    def test_copy_nodes_from_tree_to_tree_with_full_path(self):
        from_paths = ["a/b", "a/c", "a/d", "a/e", "a/f", "a/g", "a/h"]
        to_paths = ["a/b", "a/c", "a/b/d", "a/b/e", "a/c/f", "a/b/e/g", "a/b/e/h"]
        modify.copy_nodes_from_tree_to_tree(
            from_tree=self.root,
            to_tree=self.root_other,
            from_paths=from_paths,
            to_paths=to_paths,
            with_full_path=True,
        )
        assert_tree_structure_basenode_root(self.root_other)
        assert_tree_structure_basenode_root_attr(self.root_other)
        assert_tree_structure_node_root(self.root_other)

    def test_copy_nodes_from_tree_to_tree_with_full_path_error(self):
        from_paths = ["d", "e", "g", "h", "f"]
        to_paths = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_nodes_from_tree_to_tree(
                from_tree=self.root,
                to_tree=self.root_other,
                from_paths=from_paths,
                to_paths=to_paths,
                with_full_path=True,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_FULL_PATH


class TestCopyAndReplaceNodesTwoTrees(unittest.TestCase):
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

        Tree root should have structure
        a
        ├── b
        │   ├── d
        │   └── ee
        └── cc

        Tree root_other should have structure
        aa
        ├── c
        │   └── f
        └── e
            ├── g
            └── h
        """
        a = node.Node(name="a", age=90)
        b = node.Node(name="b", age=65)
        cc = node.Node(name="cc", age=60)
        d = node.Node(name="d", age=40)
        ee = node.Node(name="ee", age=35)

        b.parent = a
        cc.parent = a
        d.parent = b
        ee.parent = b

        self.root = a

        aa = node.Node(name="aa", age=90)
        cc = node.Node(name="c", age=60)
        ee = node.Node(name="e", age=35)
        ff = node.Node(name="f", age=38)
        gg = node.Node(name="g", age=10)
        hh = node.Node(name="h", age=6)

        cc.parent = aa
        ee.parent = aa
        ff.parent = cc
        gg.parent = ee
        hh.parent = ee

        self.root_other = aa

    def tearDown(self):
        self.root = None

    def test_copy_and_replace_nodes_from_tree_to_tree(self):
        from_paths = ["c", "e"]
        to_paths = ["a/cc", "a/b/ee"]
        modify.copy_and_replace_nodes_from_tree_to_tree(
            from_tree=self.root_other,
            to_tree=self.root,
            from_paths=from_paths,
            to_paths=to_paths,
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)
        assert len(self.root_other.children) == 2, "Copying changes original tree"

    def test_copy_and_replace_nodes_from_tree_to_tree_invalid_type_error(self):
        with pytest.raises(ValueError) as exc_info:
            modify.copy_and_replace_nodes_from_tree_to_tree(
                from_tree=self.root_other,
                to_tree=self.root,
                from_paths={},
                to_paths=[],
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_PARAM_TYPE

    def test_copy_and_replace_nodes_from_tree_to_tree_unequal_length_error(self):
        from_paths = ["e"]
        to_paths = ["a/cc", "a/b/ee"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_and_replace_nodes_from_tree_to_tree(
                from_tree=self.root_other,
                to_tree=self.root,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(
            exc_info.value
        ) == Constants.ERROR_MODIFY_PARAM_DIFFERENT_PATH_LENGTH.format(
            n1=len(from_paths), n2=len(to_paths)
        )

    def test_copy_and_replace_nodes_from_tree_to_tree_invalid_from_paths_error(self):
        from_path = "i"
        from_paths = [from_path]
        to_paths = ["a/cc"]
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            modify.copy_and_replace_nodes_from_tree_to_tree(
                from_tree=self.root_other,
                to_tree=self.root,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_FROM_PATH_NOT_FOUND.format(
            from_path=from_path
        )

    def test_copy_and_replace_nodes_from_tree_to_tree_invalid_to_paths_error(self):
        from_paths = ["c"]
        to_paths = ["aa/cc"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_and_replace_nodes_from_tree_to_tree(
                from_tree=self.root_other,
                to_tree=self.root,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_TO_PATH

    # sep
    def test_copy_and_replace_nodes_from_tree_to_tree_leading_sep(self):
        from_paths = ["/c", "/e"]
        to_paths = ["/a/cc", "/a/b/ee"]
        modify.copy_and_replace_nodes_from_tree_to_tree(
            from_tree=self.root_other,
            to_tree=self.root,
            from_paths=from_paths,
            to_paths=to_paths,
        )

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_copy_and_replace_nodes_from_tree_to_tree_different_sep(self):
        from_paths = ["c", "e"]
        to_paths = ["a/cc", "a/b/ee"]
        self.root_other.sep = "\\"
        modify.copy_and_replace_nodes_from_tree_to_tree(
            from_tree=self.root_other,
            to_tree=self.root,
            from_paths=from_paths,
            to_paths=to_paths,
        )
        self.root_other.sep = "/"

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_copy_and_replace_nodes_from_tree_to_tree_trailing_sep(self):
        from_paths = ["c", "e/"]
        to_paths = ["a/cc/", "a/b/ee"]
        modify.copy_and_replace_nodes_from_tree_to_tree(
            from_tree=self.root_other,
            to_tree=self.root,
            from_paths=from_paths,
            to_paths=to_paths,
        )

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_copy_and_replace_nodes_from_tree_to_tree_sep_error(self):
        from_paths = ["\\c", "\\e"]
        to_paths = ["a\\cc", "a\\b\\ee"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_and_replace_nodes_from_tree_to_tree(
                from_tree=self.root_other,
                to_tree=self.root,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_TO_PATH

    def test_copy_and_replace_nodes_from_tree_to_tree_sep(self):
        from_paths = ["\\c", "\\e"]
        to_paths = ["a\\cc", "a\\b\\ee"]
        modify.copy_and_replace_nodes_from_tree_to_tree(
            from_tree=self.root_other,
            to_tree=self.root,
            from_paths=from_paths,
            to_paths=to_paths,
            sep="\\",
        )

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # skippable
    def test_copy_and_replace_nodes_skippable_error(self):
        from_path = "i"
        from_paths = [from_path, "c", "e"]
        to_paths = ["a/cc", "a/cc", "a/b/ee"]
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            modify.copy_and_replace_nodes_from_tree_to_tree(
                from_tree=self.root_other,
                to_tree=self.root,
                from_paths=from_paths,
                to_paths=to_paths,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_FROM_PATH_NOT_FOUND.format(
            from_path=from_path
        )

        modify.copy_and_replace_nodes_from_tree_to_tree(
            from_tree=self.root_other,
            to_tree=self.root,
            from_paths=from_paths,
            to_paths=to_paths,
            skippable=True,
        )

        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # delete_children
    def test_copy_and_replace_nodes_from_tree_to_tree_delete_children(self):
        d = search.find_name(self.root, "d")
        d.children = [node.Node("i"), node.Node("j")]
        d = node.Node("d", age=40, children=[node.Node("k")])
        d.parent = self.root_other

        from_paths = ["c", "e"]
        to_paths = ["a/cc", "a/b/ee"]
        modify.copy_and_replace_nodes_from_tree_to_tree(
            self.root_other, self.root, from_paths, to_paths
        )

        from_paths = ["d"]
        to_paths = ["a/b/d"]
        modify.copy_and_replace_nodes_from_tree_to_tree(
            from_tree=self.root_other,
            to_tree=self.root,
            from_paths=from_paths,
            to_paths=to_paths,
            delete_children=True,
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    # with_full_path
    def test_copy_and_replace_nodes_from_tree_to_tree_with_full_path(self):
        from_paths = ["aa/c", "aa/e"]
        to_paths = ["a/cc", "a/b/ee"]
        modify.copy_and_replace_nodes_from_tree_to_tree(
            from_tree=self.root_other,
            to_tree=self.root,
            from_paths=from_paths,
            to_paths=to_paths,
            with_full_path=True,
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_copy_and_replace_nodes_from_tree_to_tree_with_full_path_error(self):
        from_paths = ["a/c", "aa/e"]
        to_paths = ["aa/cc/", "aa/b/ee"]
        with pytest.raises(ValueError) as exc_info:
            modify.copy_and_replace_nodes_from_tree_to_tree(
                from_tree=self.root_other,
                to_tree=self.root,
                from_paths=from_paths,
                to_paths=to_paths,
                with_full_path=True,
            )
        assert str(exc_info.value) == Constants.ERROR_MODIFY_INVALID_FULL_PATH

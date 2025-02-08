import unittest

import pytest

from bigtree.tree import construct, export
from bigtree.utils import exceptions
from tests.conftest import assert_print_statement
from tests.node.test_basenode import assert_tree_structure_basenode_root
from tests.node.test_node import (
    assert_tree_structure_node_root,
    assert_tree_structure_node_root_sep,
)
from tests.test_constants import Constants
from tests.tree.construct.conftest import NodeA


class TestListToTree(unittest.TestCase):
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
        self.path_list = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        self.path_list_full = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/f",
            "a/b/e/g",
            "a/b/e/h",
        ]

    def tearDown(self):
        self.path_list = None
        self.path_list_full = None

    def test_list_to_tree(self):
        root = construct.list_to_tree(self.path_list_full)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_leaves(self):
        root = construct.list_to_tree(self.path_list)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.list_to_tree([])
        assert str(exc_info.value) == Constants.ERROR_NODE_LIST_EMPTY.format(
            parameter="paths"
        )

    def test_list_to_tree_sep_leading(self):
        path_list = ["/a/b/d", "/a/b/e", "/a/b/e/g", "/a/b/e/h", "/a/c/f"]
        root = construct.list_to_tree(path_list)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_sep_trailing(self):
        path_list = ["a/b/d/", "a/b/e/", "a/b/e/g/", "a/b/e/h/", "a/c/f/"]
        root = construct.list_to_tree(path_list)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_sep_error(self):
        root1 = "a\\b\\d"
        root2 = "a\\b\\e"
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.list_to_tree(path_list)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )

    def test_list_to_tree_sep(self):
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        root = construct.list_to_tree(path_list, sep="\\")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root_sep(root)

    def test_list_to_tree_duplicate_node_error(self):
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/d",  # duplicate
            "a/b/e/g",
            "a/b/e/h",
        ]
        with pytest.raises(exceptions.DuplicatedNodeError) as exc_info:
            construct.list_to_tree(path_list, duplicate_name_allowed=False)
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_NAME.format(
            name="d"
        )

    def test_list_to_tree_duplicate_node(self):
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/d",  # duplicate
            "a/b/e/g",
            "a/b/e/h",
        ]
        root = construct.list_to_tree(path_list)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root, f="/a/c/d")

    def test_list_to_tree_node_type(self):
        root = construct.list_to_tree(self.path_list, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_different_root_error(self):
        root1 = "a"
        root2 = "b"
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/f",
            "a/b/e/g",
            "b/b/e/h",  # different root
        ]
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.list_to_tree(path_list)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )


class TestListToTreeByRelation(unittest.TestCase):
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
        self.relations = [
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("b", "e"),
            ("c", "f"),
            ("e", "g"),
            ("e", "h"),
        ]
        self.relations_reverse = [
            ("e", "g"),
            ("e", "h"),
            ("b", "d"),
            ("b", "e"),
            ("c", "f"),
            ("a", "b"),
            ("a", "c"),
        ]
        self.relations_switch = [
            ("h", "g"),
            ("h", "f"),
            ("g", "e"),
            ("g", "d"),
            ("g", "a"),
            ("f", "a"),
            ("d", "b"),
            ("d", "a"),
        ]

    def tearDown(self):
        self.relations = None

    def test_list_to_tree_by_relation(self):
        root = construct.list_to_tree_by_relation(self.relations)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_by_relation_reverse(self):
        root = construct.list_to_tree_by_relation(self.relations_reverse)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_by_relation_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.list_to_tree_by_relation([])
        assert str(exc_info.value) == Constants.ERROR_NODE_LIST_EMPTY.format(
            parameter="relations"
        )

    @staticmethod
    def test_list_to_tree_by_relation_duplicate_leaf_node():
        relations = [
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("b", "e"),
            ("b", "h"),
            ("c", "h"),
            ("e", "g"),
            ("e", "h"),
        ]
        root = construct.list_to_tree_by_relation(relations)
        expected = """a\n├── b\n│   ├── d\n│   ├── e\n│   │   ├── g\n│   │   └── h\n│   └── h\n└── c\n    └── h\n"""
        assert_print_statement(export.print_tree, expected, tree=root, style="const")

    @staticmethod
    def test_list_to_tree_by_relation_duplicate_intermediate_node_error():
        relations = [
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("b", "e"),
            ("c", "e"),
            ("c", "f"),
            ("e", "g"),  # duplicate parent
            ("e", "h"),  # duplicate parent
        ]
        with pytest.raises(ValueError) as exc_info:
            construct.list_to_tree_by_relation(relations)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DUPLICATED_INTERMEDIATE_NODE
        )

    @staticmethod
    def test_list_to_tree_by_relation_duplicate_intermediate_node_entry_error():
        relations = [
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("b", "e"),
            ("c", "e"),
            ("c", "f"),
            ("e", "g"),
            ("e", "g"),  # duplicate entry
            ("e", "h"),  # duplicate parent
        ]
        with pytest.raises(ValueError) as exc_info:
            construct.list_to_tree_by_relation(relations)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DUPLICATED_INTERMEDIATE_NODE
        )

    @staticmethod
    def test_list_to_tree_by_relation_duplicate_intermediate_node():
        relations = [
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("b", "e"),
            ("c", "e"),
            ("c", "f"),
            ("e", "g"),  # duplicate parent
            ("e", "h"),  # duplicate parent
        ]
        root = construct.list_to_tree_by_relation(relations, allow_duplicates=True)
        expected = (
            "a\n"
            "├── b\n"
            "│   ├── d\n"
            "│   └── e\n"
            "│       ├── g\n"
            "│       └── h\n"
            "└── c\n"
            "    ├── e\n"
            "    │   ├── g\n"
            "    │   └── h\n"
            "    └── f\n"
        )
        assert_print_statement(export.print_tree, expected, tree=root)

    def test_list_to_tree_by_relation_empty_parent(self):
        self.relations.append((None, "a"))
        root = construct.list_to_tree_by_relation(self.relations)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_list_to_tree_by_relation_one_tuple():
        root = construct.list_to_tree_by_relation([(None, "a")])
        assert root.max_depth == 1, "Max depth is wrong"
        assert root.node_name == "a", "Node name is wrong"

    def test_list_to_tree_by_relation_switch_order(self):
        root = construct.list_to_tree_by_relation(self.relations_switch)
        expected = (
            "h\n"
            "├── g\n"
            "│   ├── e\n"
            "│   ├── d\n"
            "│   │   ├── b\n"
            "│   │   └── a\n"
            "│   └── a\n"
            "└── f\n"
            "    └── a\n"
        )
        assert_print_statement(export.print_tree, expected, root)

    def test_list_to_tree_by_relation_switch_order_reverse(self):
        root = construct.list_to_tree_by_relation(self.relations_switch[::-1])
        expected = (
            "h\n"
            "├── f\n"
            "│   └── a\n"
            "└── g\n"
            "    ├── a\n"
            "    ├── d\n"
            "    │   ├── a\n"
            "    │   └── b\n"
            "    └── e\n"
        )
        assert_print_statement(export.print_tree, expected, root)

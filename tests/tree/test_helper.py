import pytest

from bigtree import print_tree
from bigtree.node.basenode import BaseNode
from bigtree.node.node import Node
from bigtree.tree.helper import clone_tree, get_tree_diff, prune_tree
from bigtree.utils.exceptions import NotFoundError, SearchError
from tests.conftest import assert_print_statement
from tests.constants import Constants
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
)


class TestCloneTree:
    @staticmethod
    def test_clone_tree_wrong_type_error():
        with pytest.raises(TypeError) as exc_info:
            clone_tree({}, Node)
        assert str(exc_info.value) == Constants.ERROR_NODE_TYPE.format(type="BaseNode")

    @staticmethod
    def test_clone_tree_basenode_node(tree_basenode):
        root_clone = clone_tree(tree_basenode, node_type=Node)
        assert isinstance(root_clone, Node), "Wrong type returned"
        assert_tree_structure_basenode_root(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)

    @staticmethod
    def test_clone_tree_node_basenode(tree_node):
        root_clone = clone_tree(tree_node, node_type=BaseNode)
        assert isinstance(root_clone, BaseNode), "Wrong type returned"
        assert_tree_structure_basenode_root(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)

    @staticmethod
    def test_clone_tree_basenode_custom(tree_basenode):
        class NodeA(Node):
            pass

        root_clone = clone_tree(tree_basenode, node_type=NodeA)
        assert isinstance(root_clone, NodeA), Constants.ERROR_CUSTOM_TYPE.format(
            type="NodeA"
        )
        assert_tree_structure_basenode_root(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)


class TestPruneTree:
    @staticmethod
    def test_prune_tree(tree_node):
        # Pruned tree is a/b/d, a/b/e/g, a/b/e/h
        tree_prune = prune_tree(tree_node, "a/b")

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 2
        assert len(tree_prune.children[0].children[0].children) == 0
        assert len(tree_prune.children[0].children[1].children) == 2

    @staticmethod
    def test_prune_tree_path_and_depth(tree_node):
        # Pruned tree is a/b/d, a/b/e (a/b/e/g, a/b/e/h pruned away)
        tree_prune = prune_tree(tree_node, "a/b", max_depth=3)

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 2
        assert len(tree_prune.children[0].children[0].children) == 0
        assert (
            len(tree_prune.children[0].children[1].children) == 0
        ), "Depth at 4 is not pruned away"

    @staticmethod
    def test_prune_tree_only_depth(tree_node):
        # Pruned tree is a/b, a/c (a/b/e/g, a/b/e/h, a/c/f pruned away)
        tree_prune = prune_tree(tree_node, max_depth=2)

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 2
        assert (
            len(tree_prune.children[0].children) == 0
        ), "Depth at 3 is not pruned away"
        assert (
            len(tree_prune.children[1].children) == 0
        ), "Depth at 3 is not pruned away"

    @staticmethod
    def test_prune_tree_second_child(tree_node):
        # Pruned tree is a/c/f
        tree_prune = prune_tree(tree_node, "a/c")

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 1

    @staticmethod
    def test_prune_tree_multiple_path_error(tree_node):
        dd = Node("d")
        dd.parent = tree_node.children[-1]
        with pytest.raises(SearchError) as exc_info:
            prune_tree(tree_node, "d")
        assert str(exc_info.value).startswith(
            Constants.ERROR_SEARCH_LESS_THAN_N_ELEMENT.format(count=1)
        )

    @staticmethod
    def test_prune_tree_nonexistant_path_error(tree_node):
        prune_path = "i"
        with pytest.raises(NotFoundError) as exc_info:
            prune_tree(tree_node, prune_path)
        assert str(exc_info.value) == Constants.ERROR_NODE_PRUNE_NOT_FOUND.format(
            prune_path=prune_path
        )

    @staticmethod
    def test_prune_tree_sep(tree_node):
        # Pruned tree is a/c/f
        tree_prune = prune_tree(tree_node, "a\\c", sep="\\")

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 1

    @staticmethod
    def test_prune_tree_sep_error(tree_node):
        prune_path = "a\\c"
        with pytest.raises(NotFoundError) as exc_info:
            prune_tree(tree_node, prune_path)
        assert str(exc_info.value) == Constants.ERROR_NODE_PRUNE_NOT_FOUND.format(
            prune_path=prune_path
        )

    @staticmethod
    def test_prune_tree_no_arg_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            prune_tree(tree_node)
        assert str(exc_info.value) == Constants.ERROR_NODE_PRUNE_ARGUMENT


class TestTreeDiff:
    @staticmethod
    def test_tree_diff(tree_node):
        other_tree_node = prune_tree(tree_node, "a/c")
        _ = Node("d", parent=other_tree_node)
        tree_only_diff = get_tree_diff(tree_node, other_tree_node, only_diff=True)
        expected_str = """a\n├── b\n│   ├── d (-)\n│   └── e\n│       ├── g (-)\n│       └── h (-)\n└── d (+)\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_only_diff)
        assert (
            tree_only_diff.max_depth == 4
        ), f"Expect max_depth to be 4, received {tree_only_diff.max_depth}"
        assert (
            len(list(tree_only_diff.children)) == 2
        ), f"Expect root to have 2 children, received {len(list(tree_only_diff.children))}"

    @staticmethod
    def test_tree_diff_all_diff(tree_node):
        other_tree_node = prune_tree(tree_node, "a/c")
        _ = Node("d", parent=other_tree_node)
        tree_diff = get_tree_diff(tree_node, other_tree_node, only_diff=False)
        expected_str = """a\n├── b\n│   ├── d (-)\n│   └── e\n│       ├── g (-)\n│       └── h (-)\n├── c\n│   └── f\n└── d (+)\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_diff)
        assert (
            tree_diff.max_depth == 4
        ), f"Expect max_depth to be 4, received {tree_diff.max_depth}"
        assert (
            len(list(tree_diff.children)) == 3
        ), f"Expect root to have 2 children, received {len(list(tree_diff.children))}"

    @staticmethod
    def test_tree_diff_same_tree(tree_node):
        expected = None
        actual = get_tree_diff(tree_node, tree_node, only_diff=True)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

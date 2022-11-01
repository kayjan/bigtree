import pytest

from bigtree.node.basenode import BaseNode
from bigtree.node.node import Node
from bigtree.tree.helper import clone_tree, get_tree_diff, prune_tree
from bigtree.utils.exceptions import NotFoundError, SearchError
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root_attr,
    assert_tree_structure_basenode_root_generic,
)


class TestCloneTree:
    @staticmethod
    def test_clone_tree_wrong_type():
        with pytest.raises(ValueError):
            clone_tree({}, Node)

    @staticmethod
    def test_clone_tree_basenode_node(tree_basenode):
        root_clone = clone_tree(tree_basenode, node_type=Node)
        assert isinstance(root_clone, Node), "Wrong type returned"
        assert_tree_structure_basenode_root_generic(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)

    @staticmethod
    def test_clone_tree_node_basenode(tree_node):
        root_clone = clone_tree(tree_node, node_type=BaseNode)
        assert isinstance(root_clone, BaseNode), "Wrong type returned"
        assert_tree_structure_basenode_root_generic(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)

    @staticmethod
    def test_clone_tree_basenode_custom(tree_basenode):
        class NodeA(Node):
            pass

        root_clone = clone_tree(tree_basenode, node_type=NodeA)
        assert isinstance(root_clone, NodeA), "Node type is not `NodeA`"
        assert_tree_structure_basenode_root_generic(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)


class TestPruneTree:
    @staticmethod
    def test_prune_tree(tree_node):
        # Pruned tree is a/c/f
        tree_prune = prune_tree(tree_node, "a/c")

        assert_tree_structure_basenode_root_generic(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 1

    @staticmethod
    def test_prune_tree_multiple_path(tree_node):
        dd = Node("d")
        dd.parent = tree_node.children[-1]
        with pytest.raises(SearchError):
            prune_tree(tree_node, "d")

    @staticmethod
    def test_prune_tree_nonexistant_path(tree_node):
        with pytest.raises(NotFoundError):
            prune_tree(tree_node, "i")

    @staticmethod
    def test_prune_tree_sep(tree_node):
        # Pruned tree is a/c/f
        tree_prune = prune_tree(tree_node, "a\\c", sep="\\")

        assert_tree_structure_basenode_root_generic(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 1

    @staticmethod
    def test_prune_tree_sep_wrong(tree_node):
        with pytest.raises(NotFoundError):
            prune_tree(tree_node, "a\\c")


class TestTreeDiff:
    @staticmethod
    def test_tree_diff(tree_node):
        other_tree_node = prune_tree(tree_node, "a/c")
        tree_only_diff = get_tree_diff(tree_node, other_tree_node, only_diff=True)
        assert (
            tree_only_diff.max_depth == 4
        ), f"Expect max_depth to be 4, received {tree_only_diff.max_depth}"
        assert (
            len(list(tree_only_diff.children)) == 1
        ), f"Expect root to have 1 children, received {len(list(tree_only_diff.children))}"

    @staticmethod
    def test_tree_diff_all_diff(tree_node):
        other_tree_node = prune_tree(tree_node, "a/c")
        tree_diff = get_tree_diff(tree_node, other_tree_node, only_diff=False)
        assert (
            tree_diff.max_depth == 4
        ), f"Expect max_depth to be 4, received {tree_diff.max_depth}"
        assert (
            len(list(tree_diff.children)) == 2
        ), f"Expect root to have 2 children, received {len(list(tree_diff.children))}"

    @staticmethod
    def test_tree_diff_same_tree(tree_node):
        expected = None
        actual = get_tree_diff(tree_node, tree_node, only_diff=True)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

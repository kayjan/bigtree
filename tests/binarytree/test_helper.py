from bigtree.node.node import Node
from bigtree.tree.export import print_tree
from bigtree.tree.helper import clone_tree, get_tree_diff, prune_tree
from tests.conftest import assert_print_statement


class TestCloneTree:
    @staticmethod
    def test_clone_tree_btree(binarytree_node):
        root_clone = clone_tree(binarytree_node, node_type=Node)
        assert isinstance(root_clone, Node), "Wrong type returned"
        expected_str = """1\n├── 2\n│   ├── 4\n│   │   └── 8\n│   └── 5\n└── 3\n    ├── 6\n    └── 7\n"""
        assert_print_statement(print_tree, expected_str, tree=binarytree_node)


class TestPruneTree:
    @staticmethod
    def test_prune_tree(binarytree_node):
        tree_prune = prune_tree(binarytree_node, "1/3/6")
        expected_str = """1\n└── 3\n    └── 6\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_prune)
        assert len(list(tree_prune.children)) == 2
        assert not list(tree_prune.children)[1]
        assert len(tree_prune.children[0].children) == 2
        assert not tree_prune.children[0].children[1]


class TestTreeDiff:
    @staticmethod
    def test_tree_diff(binarytree_node):
        other_tree_node = prune_tree(binarytree_node, "1/3")
        tree_only_diff = get_tree_diff(binarytree_node, other_tree_node, only_diff=True)
        expected_str = """1\n└── 2\n    ├── 4\n    │   └── 8 (-)\n    └── 5 (-)\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_only_diff)
        assert (
            tree_only_diff.max_depth == 4
        ), f"Expect max_depth to be 4, received {tree_only_diff.max_depth}"
        assert (
            len(list(tree_only_diff.children)) == 2
        ), f"Expect root to have 2 children, received {len(list(tree_only_diff.children))}"
        assert not list(tree_only_diff.children)[
            1
        ], f"Expect root second children to be None, received {list(tree_only_diff.children)}"

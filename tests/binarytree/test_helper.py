from bigtree.node import node
from bigtree.tree import export, helper
from tests.conftest import assert_print_statement


class TestCloneTree:
    @staticmethod
    def test_clone_tree(binarytree_node):
        root_clone = helper.clone_tree(binarytree_node, node_type=node.Node)
        assert isinstance(root_clone, node.Node), "Wrong type returned"
        expected_str = (
            "1\n"
            "├── 2\n"
            "│   ├── 4\n"
            "│   │   └── 8\n"
            "│   └── 5\n"
            "└── 3\n"
            "    ├── 6\n"
            "    └── 7\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=binarytree_node)


class TestPruneTree:
    @staticmethod
    def test_prune_tree(binarytree_node):
        # Pruned tree is 1/2/4/8
        tree_prune = helper.prune_tree(binarytree_node, "1/2/4")

        assert tree_prune.left.val == 2, "Check left child of tree_prune (depth 2)"
        assert not tree_prune.right, "Check right child of tree_prune (depth 2)"
        assert tree_prune.left.left.val == 4, "Check left child (depth 3)"
        assert not tree_prune.left.right, "Check right child (depth 3)"
        assert not tree_prune.left.left.left, "Check left child (depth 4)"
        assert tree_prune.left.left.right.val == 8, "Check right child (depth 4)"
        assert tree_prune.left.left.right.children == (
            None,
            None,
        ), "Check children (depth 5)"

    @staticmethod
    def test_prune_tree_exact(binarytree_node):
        # Pruned tree is 1/2/4
        tree_prune = helper.prune_tree(binarytree_node, "1/2/4", exact=True)

        assert tree_prune.left.val == 2, "Check left child of tree_prune (depth 2)"
        assert not tree_prune.right, "Check right child of tree_prune (depth 2)"
        assert tree_prune.left.left.val == 4, "Check left child (depth 3)"
        assert not tree_prune.left.right, "Check right child (depth 3)"
        assert tree_prune.left.left.children == (
            None,
            None,
        ), "Check children (depth 4)"

    @staticmethod
    def test_prune_tree_second_child(binarytree_node):
        # Pruned tree is 1/3/6, 1/3/7
        tree_prune = helper.prune_tree(binarytree_node, "1/3")

        assert not tree_prune.left, "Check left child of tree_prune (depth 2)"
        assert tree_prune.right.val == 3, "Check right child of tree_prune (depth 2)"
        assert tree_prune.right.left.val == 6, "Check left child (depth 3)"
        assert tree_prune.right.right.val == 7, "Check right child (depth 3)"
        assert tree_prune.right.left.children == (
            None,
            None,
        ), "Check children (depth 4)"
        assert tree_prune.right.right.children == (
            None,
            None,
        ), "Check children (depth 4)"

    @staticmethod
    def test_prune_tree_list(binarytree_node):
        # Pruned tree is 1/3/6, 1/3/7
        tree_prune = helper.prune_tree(binarytree_node, ["1/3/6", "1/3/7"])

        assert not tree_prune.left, "Check left child of tree_prune (depth 2)"
        assert tree_prune.right.val == 3, "Check right child of tree_prune (depth 2)"
        assert tree_prune.right.left.val == 6, "Check left child (depth 3)"
        assert tree_prune.right.right.val == 7, "Check right child (depth 3)"
        assert tree_prune.right.left.children == (
            None,
            None,
        ), "Check children (depth 4)"
        assert tree_prune.right.right.children == (
            None,
            None,
        ), "Check children (depth 4)"


class TestTreeDiff:
    @staticmethod
    def test_tree_diff(binarytree_node):
        other_tree_node = helper.prune_tree(binarytree_node, "1/3")
        tree_only_diff = helper.get_tree_diff(
            binarytree_node, other_tree_node, only_diff=True
        )
        expected_str = (
            "1\n"
            "└── 2 (-)\n"
            "    ├── 4 (-)\n"
            "    │   └── 8 (-)\n"
            "    └── 5 (-)\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_only_diff)

from bigtree.tree.studio.actions import ActionRenameNode
from tests.node.test_node import assert_tree_structure_node_root
from tests.tree.studio.test_utils import assert_textual_tree_structure


class TestActionRenameNode:
    @staticmethod
    def test_action_rename_node(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        assert len(list(b_node.children)) == 2
        ActionRenameNode(tree_tree, e_node, "e_new").run()
        # Check textual tree
        assert len(list(b_node.children)) == 2
        b_child = list(b_node.children)[-1]
        assert b_child.data["path_name"] == "/a/b/e_new"
        # Check bigtree tree
        assert len(tree_tree["b"].node.children) == 2
        assert tree_tree["b"].node.children[-1].name == "e_new"

    @staticmethod
    def test_action_rename_node_empty_value(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        ActionRenameNode(tree_tree, e_node, "").run()
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)

    @staticmethod
    def test_action_rename_node_empty_textual_node(tree_tree, textual_tree):
        ActionRenameNode(tree_tree, None, "e_new").run()
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)

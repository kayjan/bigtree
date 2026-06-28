from bigtree.tree.studio.actions import ActionDeleteNode
from tests.node.test_node import assert_tree_structure_node_root
from tests.tree.studio.test_utils import assert_textual_tree_structure


class TestActionDeleteNode:
    @staticmethod
    def test_action_delete_node(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        assert len(list(b_node.children)) == 2
        ActionDeleteNode(tree_tree, e_node).run()
        assert len(list(b_node.children)) == 1
        assert len(list(tree_tree["b"].node.children)) == 1

    @staticmethod
    def test_action_delete_node_empty_textual_node(tree_tree, textual_tree):
        ActionDeleteNode(tree_tree, None).run()
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)

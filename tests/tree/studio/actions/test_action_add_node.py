from bigtree.tree.studio.actions import ActionAddNode
from tests.node.test_node import assert_tree_structure_node_root
from tests.tree.studio.test_utils import assert_textual_tree_structure


class TestActionAddNode:
    @staticmethod
    def test_action_add_node(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        assert len(list(b_node.children)) == 2
        ActionAddNode(tree_tree, b_node, "b_child").run()
        # Check textual tree
        assert len(list(b_node.children)) == 3
        b_child = list(b_node.children)[-1]
        assert b_child.data["path_name"] == "/a/b/b_child"
        # Check bigtree tree
        assert len(tree_tree["b"].node.children) == 3
        assert tree_tree["b"].node.children[-1].name == "b_child"

    @staticmethod
    def test_action_add_node_empty_value(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        assert len(list(b_node.children)) == 2
        ActionAddNode(tree_tree, b_node, "").run()
        assert len(list(b_node.children)) == 2
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)

    @staticmethod
    def test_action_add_node_empty_textual_node(tree_tree, textual_tree):
        ActionAddNode(tree_tree, None, "b_child").run()
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)

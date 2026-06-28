import pytest

from bigtree.tree.studio.actions import ActionEditAttr
from tests.node.test_node import assert_tree_structure_node_root
from tests.test_constants import Constants
from tests.tree.studio.test_utils import assert_textual_tree_structure


class TestActionEditAttr:
    @staticmethod
    def test_action_edit_attr(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        ActionEditAttr(tree_tree, e_node, "age=35,age2=30").run()
        # Check textual tree
        assert e_node.data["path_name"] == "/a/b/e"
        # Check bigtree tree
        assert tree_tree["b"]["e"].node.age == 35
        assert tree_tree["b"]["e"].node.age2 == 30

    @staticmethod
    def test_action_edit_attr_str(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        ActionEditAttr(tree_tree, e_node, "age=35,person='alice'").run()
        # Check textual tree
        assert e_node.data["path_name"] == "/a/b/e"
        # Check bigtree tree
        assert tree_tree["b"]["e"].node.age == 35
        assert tree_tree["b"]["e"].node.person == "alice"

    @staticmethod
    def test_action_edit_update(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        ActionEditAttr(tree_tree, e_node, "age2=35").run()
        # Check textual tree
        assert e_node.data["path_name"] == "/a/b/e"
        # Check bigtree tree
        assert tree_tree["b"]["e"].node.age2 == 35

    @staticmethod
    def test_action_edit_attr_name(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        ActionEditAttr(tree_tree, e_node, "age=35,name='alice'").run()
        # Check textual tree
        assert e_node.data["path_name"] == "/a/b/alice"
        # Check bigtree tree
        assert tree_tree["b"]["alice"].node.age == 35
        assert tree_tree["b"]["alice"].node.name == "alice"
        assert tree_tree["b"]["alice"].node.node_name == "alice"

    @staticmethod
    def test_action_edit_attr_name_clash_with_sep(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        ActionEditAttr(tree_tree, e_node, "age=35,name='c/d'").run()
        # Check textual tree
        assert e_node.data["path_name"] == "/a/b/c/d"
        # Check bigtree tree
        assert tree_tree["b"]["c/d"].node.age == 35
        assert tree_tree["b"]["c/d"].node.name == "c/d"
        assert tree_tree["b"]["c/d"].node.node_name == "c/d"

    @staticmethod
    def test_action_edit_attr_node_name(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        ActionEditAttr(tree_tree, e_node, "age=35,node_name='alice'").run()
        # Check textual tree
        assert e_node.data["path_name"] == "/a/b/e"
        # Check bigtree tree
        assert tree_tree["b"]["e"].node.age == 35
        assert tree_tree["b"]["e"].node.name == "e"
        assert tree_tree["b"]["e"].node.node_name == "e"
        assert tree_tree["b"]["e"].node.__dict__["node_name"] == "alice"

    @staticmethod
    def test_action_edit_attr_error(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        with pytest.raises(ValueError) as exc_info:
            ActionEditAttr(tree_tree, e_node, "age=").run()
        assert str(exc_info.value).startswith(Constants.ERROR_STUDIO_EDIT_ATTR)

    @staticmethod
    def test_action_edit_node_empty_value(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        ActionEditAttr(tree_tree, e_node, "").run()
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)

    @staticmethod
    def test_action_edit_node_empty_textual_node(tree_tree, textual_tree):
        ActionEditAttr(tree_tree, None, "e_new").run()
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)

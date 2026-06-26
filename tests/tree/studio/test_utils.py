import pytest
from textual.widgets import Tree

import bigtree.tree.studio.utils as studio_utils
from tests.node.test_node import assert_tree_structure_node_root
from tests.test_constants import Constants


@pytest.fixture
def textual_tree(tree_tree):
    _textual_tree = Tree("test")
    studio_utils.populate_textual_tree(tree_tree, _textual_tree, max_depth=2)
    return _textual_tree


def assert_textual_tree_structure(textual_tree):
    assert textual_tree.root.data["path_name"] == "/a"
    b_node = list(textual_tree.root.children)[0]
    assert b_node.data["path_name"] == "/a/b"
    e_node = list(b_node.children)[-1]
    h_node = list(e_node.children)[1]
    assert e_node.data["path_name"] == "/a/b/e"
    assert h_node.data["path_name"] == "/a/b/e/h"


def test_populate_textual_tree(tree_tree, textual_tree):
    assert_textual_tree_structure(textual_tree)
    assert_tree_structure_node_root(tree_tree.node)
    assert textual_tree.root.data["path_name"] == tree_tree.node.path_name


def test_get_textual_node_path(textual_tree):
    assert studio_utils._get_textual_node_path(textual_tree.root) == "a"
    b_node = list(textual_tree.root.children)[0]
    e_node = list(b_node.children)[-1]
    assert studio_utils._get_textual_node_path(b_node) == "a/b"
    assert studio_utils._get_textual_node_path(e_node) == "a/b/e"


def test_get_corresponding_bt_node(tree_tree, textual_tree):
    b_node = list(textual_tree.root.children)[0]
    e_node = list(b_node.children)[-1]
    assert (
        studio_utils._get_corresponding_bt_node(tree_tree, b_node)
        == tree_tree["b"].node
    )
    assert (
        studio_utils._get_corresponding_bt_node(tree_tree, e_node)
        == tree_tree["b"]["e"].node
    )


def test_get_corresponding_textual_nodes(textual_tree):
    actual_nodes = studio_utils._get_corresponding_textual_nodes(
        textual_tree, ["/a/b", "/a/b/e"]
    )
    b_node = list(textual_tree.root.children)[0]
    e_node = list(b_node.children)[-1]
    assert set(actual_nodes) == {b_node, e_node}


def test_get_attr_bt_node(tree_tree, textual_tree):
    # Covers _get_corresponding_bt_node
    b_node = list(textual_tree.root.children)[0]
    e_node = list(b_node.children)[-1]
    assert studio_utils._get_attr_bt_node(tree_tree, b_node) == {"age": 65}
    assert studio_utils._get_attr_bt_node(tree_tree, e_node) == {"age": 35}


def test_update_details(tree_tree, textual_tree):
    # Covers _get_attr_bt_node, _get_corresponding_bt_node
    b_node = list(textual_tree.root.children)[0]
    e_node = list(b_node.children)[-1]
    assert (
        studio_utils.update_details(tree_tree, b_node)
        == "[b]Name:[/] b\n[b]Path:[/] /a/b\n\n[b]Attributes:[/]\nage: 65"
    )
    assert (
        studio_utils.update_details(tree_tree, e_node)
        == "[b]Name:[/] e\n[b]Path:[/] /a/b/e\n\n[b]Attributes:[/]\nage: 35"
    )


def test_expand_parents(textual_tree):
    b_node = list(textual_tree.root.children)[0]
    e_node = list(b_node.children)[-1]
    h_node = list(e_node.children)[1]
    assert textual_tree.root.is_expanded
    for _node in (b_node, e_node, h_node):
        assert not _node.is_expanded
    studio_utils.expand_parents(h_node)
    for _node in (textual_tree.root, b_node, e_node):
        assert _node.is_expanded
    assert not h_node.is_expanded


class TestActionAddNode:
    @staticmethod
    def test_action_add_node(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        assert len(list(b_node.children)) == 2
        studio_utils.action_add_node(tree_tree, b_node, "b_child")
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
        studio_utils.action_add_node(tree_tree, b_node, "")
        assert len(list(b_node.children)) == 2
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)

    @staticmethod
    def test_action_add_node_empty_textual_node(tree_tree, textual_tree):
        studio_utils.action_add_node(tree_tree, None, "b_child")
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)


class TestActionAddSibling:
    @staticmethod
    def test_action_add_sibling(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        assert len(list(b_node.children)) == 2
        studio_utils.action_add_sibling(tree_tree, e_node, "b_child")
        # Check textual tree
        assert len(list(b_node.children)) == 3
        b_child = list(b_node.children)[-1]
        assert b_child.data["path_name"] == "/a/b/b_child"
        # Check bigtree tree
        assert len(tree_tree["b"].node.children) == 3
        assert tree_tree["b"].node.children[-1].name == "b_child"

    @staticmethod
    def test_action_add_sibling_root_error(tree_tree, textual_tree):
        with pytest.raises(ValueError) as exc_info:
            studio_utils.action_add_sibling(tree_tree, textual_tree.root, "sample")
        assert str(exc_info.value) == Constants.ERROR_STUDIO_ADD_SIBLING

    @staticmethod
    def test_action_add_sibling_empty_value(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        assert len(list(b_node.children)) == 2
        studio_utils.action_add_sibling(tree_tree, e_node, "")
        assert len(list(b_node.children)) == 2
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)

    @staticmethod
    def test_action_add_sibling_empty_textual_node(tree_tree, textual_tree):
        studio_utils.action_add_sibling(tree_tree, None, "b_child")
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)


class TestActionDeleteNode:
    @staticmethod
    def test_action_delete_node(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        assert len(list(b_node.children)) == 2
        studio_utils.action_delete_node(tree_tree, e_node)
        assert len(list(b_node.children)) == 1
        assert len(list(tree_tree["b"].node.children)) == 1

    @staticmethod
    def test_action_delete_node_empty_textual_node(tree_tree, textual_tree):
        studio_utils.action_delete_node(tree_tree, None)
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)


class TestActionRenameNode:
    @staticmethod
    def test_action_rename_node(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        assert len(list(b_node.children)) == 2
        studio_utils.action_rename_node(tree_tree, e_node, "e_new")
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
        assert len(list(b_node.children)) == 2
        studio_utils.action_rename_node(tree_tree, e_node, "")
        assert len(list(b_node.children)) == 2
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)

    @staticmethod
    def test_action_rename_node_empty_textual_node(tree_tree, textual_tree):
        studio_utils.action_rename_node(tree_tree, None, "e_new")
        assert_textual_tree_structure(textual_tree)
        assert_tree_structure_node_root(tree_tree.node)

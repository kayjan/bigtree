import bigtree.tree.studio.utils as studio_utils
from tests.node.test_node import assert_tree_structure_node_root


def assert_textual_tree_structure(textual_tree):
    assert textual_tree.root.data["path_name"] == "/a"
    b_node = list(textual_tree.root.children)[0]
    assert b_node.data["path_name"] == "/a/b"
    e_node = list(b_node.children)[-1]
    h_node = list(e_node.children)[1]
    assert e_node.data["path_name"] == "/a/b/e"
    assert h_node.data["path_name"] == "/a/b/e/h"


def test_get_textual_node_path(textual_tree):
    assert studio_utils._get_textual_node_path(textual_tree.root) == ["a"]
    b_node = list(textual_tree.root.children)[0]
    e_node = list(b_node.children)[-1]
    assert studio_utils._get_textual_node_path(b_node) == ["a", "b"]
    assert studio_utils._get_textual_node_path(e_node) == ["a", "b", "e"]


def test_get_corresponding_bt_node(tree_tree, textual_tree):
    b_node = list(textual_tree.root.children)[0]
    e_node = list(b_node.children)[-1]
    assert (
        studio_utils.get_corresponding_bt_node(tree_tree, b_node) == tree_tree["b"].node
    )
    assert (
        studio_utils.get_corresponding_bt_node(tree_tree, e_node)
        == tree_tree["b"]["e"].node
    )


def test_get_attr_bt_node(tree_tree, textual_tree):
    # Covers _get_corresponding_bt_node
    b_node = list(textual_tree.root.children)[0]
    e_node = list(b_node.children)[-1]
    assert studio_utils.get_attr_bt_node(tree_tree, b_node) == {"age": 65}
    assert studio_utils.get_attr_bt_node(tree_tree, e_node) == {"age": 35}


def test_populate_textual_tree(tree_tree, textual_tree):
    assert_textual_tree_structure(textual_tree)
    assert_tree_structure_node_root(tree_tree.node)
    assert textual_tree.root.data["path_name"] == tree_tree.node.path_name


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


def test_select_edit_attr(tree_tree, textual_tree):
    # Covers _get_attr_bt_node
    b_node = list(textual_tree.root.children)[0]
    e_node = list(b_node.children)[-1]
    assert studio_utils.select_edit_attr(tree_tree, b_node) == "age=65"
    assert studio_utils.select_edit_attr(tree_tree, e_node) == "age=35"

from bigtree.tree.studio.actions.action_search import (
    ActionSearch,
    _get_corresponding_textual_nodes,
)


def test_get_corresponding_textual_nodes(textual_tree):
    actual_nodes = _get_corresponding_textual_nodes(textual_tree, ["/a/b", "/a/b/e"])
    b_node = list(textual_tree.root.children)[0]
    e_node = list(b_node.children)[-1]
    assert set(actual_nodes) == {b_node, e_node}


class TestActionSearch:
    @staticmethod
    def test_action_search(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        actual = ActionSearch(tree_tree, textual_tree, "e").run()
        assert actual == [e_node]

    @staticmethod
    def test_action_search_query_equal(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        actual = ActionSearch(tree_tree, textual_tree, "query:age==35").run()
        assert actual == [e_node]

    @staticmethod
    def test_action_search_query_like(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        actual = ActionSearch(tree_tree, textual_tree, 'query:name LIKE ".*e.*"').run()
        assert actual == [e_node]

    @staticmethod
    def test_action_search_name(tree_tree, textual_tree):
        b_node = list(textual_tree.root.children)[0]
        e_node = list(b_node.children)[-1]
        actual = ActionSearch(tree_tree, textual_tree, "name:.*e.*").run()
        assert actual == [e_node]

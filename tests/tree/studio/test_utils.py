from textual.widgets import Tree

from bigtree.tree import tree
from bigtree.tree.studio.utils import populate_textual_tree


def test_populate_textual_tree(tree_node):
    textual_tree = Tree("test")
    populate_textual_tree(tree.Tree(tree_node), textual_tree, max_depth=2)
    assert textual_tree.root.data["path_name"] == tree_node.path_name

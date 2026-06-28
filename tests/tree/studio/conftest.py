import pytest
from textual.widgets import Tree

import bigtree.tree.studio.utils as studio_utils


@pytest.fixture
def textual_tree(tree_tree):
    _textual_tree = Tree("test")
    studio_utils.populate_textual_tree(tree_tree, _textual_tree, max_depth=2)
    return _textual_tree

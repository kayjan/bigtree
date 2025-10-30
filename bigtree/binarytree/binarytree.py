from typing import Any

from bigtree._plugins import register_binarytree_plugins
from bigtree.node import binarynode
from bigtree.tree.tree import Tree


class BinaryTree(Tree):
    """
    BinaryTree wraps around BinaryNode class to provide a quick, intuitive, Pythonic API for

        * Construction with dataframe, dictionary, list, or string
        * Export to dataframe, dictionary, list, string, or images
        * Helper methods for cloning, pruning, getting tree diff
        * Query and Search methods to find one or more Nodes

    Do refer to the various modules respectively on the keyword parameters.
    """

    construct_kwargs: dict[str, Any] = dict(node_type=binarynode.BinaryNode)

    def __init__(self, root: binarynode.BinaryNode):
        super().__init__(root)


register_binarytree_plugins()

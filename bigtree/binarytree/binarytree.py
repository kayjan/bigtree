from typing import Any, Sequence

from bigtree.binarytree import construct
from bigtree.node import binarynode
from bigtree.tree.tree import Tree


class BinaryTree(Tree):
    """
    BinaryTree wraps around BinaryNode class to provide an intuitive, Pythonic API for
        - Quick construction of tree with dataframe, dictionary, list, or string
        - Quick export to dataframe, dictionary, list, string, or images

    Do refer to the various modules respectively on the keyword parameters.
    """

    construct_kwargs: dict[str, Any] = dict(node_type=binarynode.BinaryNode)

    def __init__(self, root: binarynode.BinaryNode):
        super().__init__(root)

    @classmethod
    def from_heapq_list(cls, heapq_list: Sequence[int], **kwargs: Any) -> "BinaryTree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.list_to_binarytree(heapq_list, **construct_kwargs)
        return cls(root_node)

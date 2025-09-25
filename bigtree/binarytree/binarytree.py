from typing import Any, Sequence

from bigtree.binarytree import construct
from bigtree.node import binarynode
from bigtree.tree.tree import Tree


class BinaryTree(Tree):
    """
    BinaryTree wraps around BinaryNode class to provide a quick, intuitive, Pythonic API for
        - Construction with dataframe, dictionary, list, or string
        - Export to dataframe, dictionary, list, string, or images
        - Helper methods for cloning, pruning, getting tree diff
        - Query and Search methods to find one or more Nodes


    Do refer to the various modules respectively on the keyword parameters.
    """

    construct_kwargs: dict[str, Any] = dict(node_type=binarynode.BinaryNode)

    def __init__(self, root: binarynode.BinaryNode):
        super().__init__(root)

    @classmethod
    def from_heapq_list(
        cls, heapq_list: Sequence[int], *args: Any, **kwargs: Any
    ) -> "BinaryTree":
        """See `list_to_binarytree` for full details.

        Accepts the same arguments as `list_to_binarytree`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.list_to_binarytree(heapq_list, *args, **construct_kwargs)
        return cls(root_node)

from typing import List, Type, TypeVar

from bigtree.node import binarynode
from bigtree.utils import assertions

__all__ = ["list_to_binarytree"]

T = TypeVar("T", bound=binarynode.BinaryNode)


def list_to_binarytree(
    heapq_list: List[int],
    node_type: Type[T] = binarynode.BinaryNode,  # type: ignore[assignment]
) -> T:
    """Construct tree from a list of numbers (int or float) in heapq format.

    Examples:
        >>> from bigtree import list_to_binarytree, tree_to_dot
        >>> nums_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> root = list_to_binarytree(nums_list)
        >>> root.show()
        1
        ├── 2
        │   ├── 4
        │   │   ├── 8
        │   │   └── 9
        │   └── 5
        │       └── 10
        └── 3
            ├── 6
            └── 7
        >>> graph = tree_to_dot(root, node_colour="gold")
        >>> graph.write_png("assets/construct_binarytree.png")

        ![Sample Binary Tree](https://github.com/kayjan/bigtree/raw/master/assets/construct_binarytree.png)

    Args:
        heapq_list: list containing integer node names, ordered in heapq fashion
        node_type: node type of tree to be created

    Returns:
        Binary node
    """
    assertions.assert_length_not_empty(heapq_list, "Input list", "heapq_list")

    root_node = node_type(heapq_list[0])
    node_list = [root_node]
    for idx, num in enumerate(heapq_list):
        if idx:
            parent_idx = int((idx + 1) / 2) - 1
            node = node_type(num, parent=node_list[parent_idx])
            node_list.append(node)
    return root_node

from typing import List, Type, Union

from bigtree.node.binarynode import BinaryNode


def list_to_binarytree(
    heapq_list: List[Union[int, float]], node_type: Type[BinaryNode] = BinaryNode
) -> BinaryNode:
    """Construct tree from list of numbers (int or float) in heapq format.

    >>> from bigtree import list_to_binarytree, print_tree, tree_to_dot
    >>> nums_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> root = list_to_binarytree(nums_list)
    >>> print_tree(root)
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
    >>> graph.write_png("assets/binarytree.png")

    .. image:: https://github.com/kayjan/bigtree/raw/master/assets/binarytree.png

    Args:
        heapq_list (List[Union[int, float]]): list containing integer node names, ordered in heapq fashion
        node_type (Type[BinaryNode]): node type of tree to be created, defaults to BinaryNode

    Returns:
        (BinaryNode)
    """
    if not len(heapq_list):
        raise ValueError("Input list does not contain any data, check `heapq_list`")

    root = node_type(heapq_list[0])
    node_list = [root]
    for idx, num in enumerate(heapq_list):
        if idx:
            if idx % 2:
                parent_idx = int((idx - 1) / 2)
            else:
                parent_idx = int((idx - 2) / 2)
            node = node_type(num, parent=node_list[parent_idx])
            node_list.append(node)
    return root

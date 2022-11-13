from typing import List, Type, Union

from bigtree.node.bnode import BNode


def list_to_btree(
    heapq_list: List[Union[int, float]], node_type: Type[BNode] = BNode
) -> BNode:
    """Construct tree from list of numbers (int or float) in heapq format.

    >>> from bigtree import list_to_btree, print_tree, tree_to_dot
    >>> nums_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> root = list_to_btree(nums_list)
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
    >>> graph.write_png("assets/btree.png")

    .. image:: https://github.com/kayjan/bigtree/raw/master/assets/btree.png

    Args:
        heapq_list (List[Union[int, float]]): list containing path strings
        node_type (Type[BNode]): node type of tree to be created, defaults to BNode

    Returns:
        (BNode)
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

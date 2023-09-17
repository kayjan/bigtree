from typing import Type, TypeVar, Union

from bigtree.node.basenode import BaseNode
from bigtree.node.binarynode import BinaryNode
from bigtree.node.node import Node
from bigtree.tree.construct import dataframe_to_tree
from bigtree.tree.export import tree_to_dataframe
from bigtree.tree.search import find_path
from bigtree.utils.exceptions import NotFoundError
from bigtree.utils.iterators import levelordergroup_iter

__all__ = ["clone_tree", "prune_tree", "get_tree_diff"]
BaseNodeT = TypeVar("BaseNodeT", bound=BaseNode)
BinaryNodeT = TypeVar("BinaryNodeT", bound=BinaryNode)
NodeT = TypeVar("NodeT", bound=Node)


def clone_tree(tree: BaseNode, node_type: Type[BaseNode]) -> BaseNode:
    """Clone tree to another `Node` type.
    If the same type is needed, simply do a tree.copy().

    >>> from bigtree import BaseNode, Node, clone_tree
    >>> root = BaseNode(name="a")
    >>> b = BaseNode(name="b", parent=root)
    >>> clone_tree(root, Node)
    Node(/a, )

    Args:
        tree (BaseNode): tree to be cloned, must inherit from BaseNode
        node_type (Type[BaseNode]): type of cloned tree

    Returns:
        (BaseNode)
    """
    if not isinstance(tree, BaseNode):
        raise TypeError("Tree should be of type `BaseNode`, or inherit from `BaseNode`")

    # Start from root
    root_info = dict(tree.root.describe(exclude_prefix="_"))
    root_node = node_type(**root_info)

    def recursive_add_child(_new_parent_node: BaseNode, _parent_node: BaseNode) -> None:
        for _child in _parent_node.children:
            if _child:
                child_info = dict(_child.describe(exclude_prefix="_"))
                child_node = node_type(**child_info)
                child_node.parent = _new_parent_node
                recursive_add_child(child_node, _child)

    recursive_add_child(root_node, tree.root)
    return root_node


def prune_tree(
    tree: Union[BinaryNodeT, NodeT],
    prune_path: str = "",
    sep: str = "/",
    max_depth: int = 0,
) -> Union[BinaryNodeT, NodeT]:
    """Prune tree by path or depth, returns the root of a *copy* of the original tree.

    For pruning by `prune_path`,
      All siblings along the prune path will be removed.
      Prune path name should be unique, can be full path, partial path (trailing part of path), or node name.

    For pruning by `max_depth`,
      All nodes that are beyond `max_depth` will be removed.

    Path should contain `Node` name, separated by `sep`.
      - For example: Path string "a/b" refers to Node("b") with parent Node("a").

    >>> from bigtree import Node, prune_tree
    >>> root = Node("a")
    >>> b = Node("b", parent=root)
    >>> c = Node("c", parent=b)
    >>> d = Node("d", parent=b)
    >>> e = Node("e", parent=root)
    >>> root.show()
    a
    ├── b
    │   ├── c
    │   └── d
    └── e

    >>> root_pruned = prune_tree(root, "a/b")
    >>> root_pruned.show()
    a
    └── b
        ├── c
        └── d

    >>> root_pruned = prune_tree(root, max_depth=2)
    >>> root_pruned.show()
    a
    ├── b
    └── e

    Args:
        tree (Union[BinaryNode, Node]): existing tree
        prune_path (str): prune path, all siblings along the prune path will be removed
        sep (str): path separator of `prune_path`
        max_depth (int): maximum depth of pruned tree, based on `depth` attribute, defaults to None

    Returns:
        (Union[BinaryNode, Node])
    """
    if not prune_path and not max_depth:
        raise ValueError("Please specify either `prune_path` or `max_depth` or both.")

    tree_copy = tree.copy()

    # Prune by path (prune bottom-up)
    if prune_path:
        prune_path = prune_path.replace(sep, tree.sep)
        child = find_path(tree_copy, prune_path)
        if not child:
            raise NotFoundError(
                f"Cannot find any node matching path_name ending with {prune_path}"
            )
        while child.parent:
            for other_children in child.parent.children:
                if other_children != child:
                    other_children.parent = None
            child = child.parent

    # Prune by depth (prune top-down)
    if max_depth:
        for depth, level_nodes in enumerate(levelordergroup_iter(tree_copy), 1):
            if depth == max_depth:
                for level_node in level_nodes:
                    del level_node.children
    return tree_copy


def get_tree_diff(tree: Node, other_tree: Node, only_diff: bool = True) -> Node:
    """Get difference of `tree` to `other_tree`, changes are relative to `tree`.

    (+) and (-) will be added relative to `tree`.
      - For example: (+) refers to nodes that are in `other_tree` but not `tree`.
      - For example: (-) refers to nodes that are in `tree` but not `other_tree`.

    Note that only leaf nodes are compared and have (+) or (-) indicators. Intermediate parent nodes are not compared.

    Function can return all original tree nodes and differences, or only the differences.

    >>> from bigtree import Node, get_tree_diff
    >>> root = Node("a")
    >>> b = Node("b", parent=root)
    >>> c = Node("c", parent=root)
    >>> d = Node("d", parent=b)
    >>> e = Node("e", parent=root)
    >>> root.show()
    a
    ├── b
    │   └── d
    ├── c
    └── e

    >>> root_other = Node("a")
    >>> b_other = Node("b", parent=root_other)
    >>> c_other = Node("c", parent=b_other)
    >>> d_other = Node("d", parent=root_other)
    >>> e_other = Node("e", parent=root_other)
    >>> root_other.show()
    a
    ├── b
    │   └── c
    ├── d
    └── e

    >>> tree_diff = get_tree_diff(root, root_other)
    >>> tree_diff.show()
    a
    ├── b
    │   ├── c (+)
    │   └── d (-)
    ├── c (-)
    └── d (+)

    >>> tree_diff = get_tree_diff(root, root_other, only_diff=False)
    >>> tree_diff.show()
    a
    ├── b
    │   ├── c (+)
    │   └── d (-)
    ├── c (-)
    ├── d (+)
    └── e

    Args:
        tree (Node): tree to be compared against
        other_tree (Node): tree to be compared with
        only_diff (bool): indicator to show all nodes or only nodes that are different (+/-), defaults to True

    Returns:
        (Node)
    """
    tree = tree.copy()
    other_tree = other_tree.copy()
    name_col = "name"
    path_col = "PATH"
    indicator_col = "Exists"

    data = tree_to_dataframe(tree, name_col=name_col, path_col=path_col, leaf_only=True)
    data_other = tree_to_dataframe(
        other_tree, name_col=name_col, path_col=path_col, leaf_only=True
    )
    data_both = data[[path_col, name_col]].merge(
        data_other[[path_col, name_col]], how="outer", indicator=indicator_col
    )

    data_both.loc[data_both[indicator_col] == "left_only", name_col] = (
        data_both[name_col] + " (-)"
    )
    data_both.loc[data_both[indicator_col] == "right_only", name_col] = (
        data_both[name_col] + " (+)"
    )

    if only_diff:
        data_both = data_both[data_both[indicator_col] != "both"]
    data_both = data_both.drop(columns=indicator_col).sort_values(path_col)
    if len(data_both):
        return dataframe_to_tree(data_both, node_type=tree.__class__)

from collections import deque
from typing import Any, Deque, Dict, List, Set, Type, TypeVar, Union

from bigtree.node.basenode import BaseNode
from bigtree.node.binarynode import BinaryNode
from bigtree.node.node import Node
from bigtree.tree.construct import add_dict_to_tree_by_path, dataframe_to_tree
from bigtree.tree.export import tree_to_dataframe
from bigtree.tree.search import find_path
from bigtree.utils.assertions import assert_tree_type
from bigtree.utils.exceptions import NotFoundError
from bigtree.utils.iterators import levelordergroup_iter

__all__ = ["clone_tree", "get_subtree", "prune_tree", "get_tree_diff"]
BaseNodeT = TypeVar("BaseNodeT", bound=BaseNode)
BinaryNodeT = TypeVar("BinaryNodeT", bound=BinaryNode)
NodeT = TypeVar("NodeT", bound=Node)


def clone_tree(tree: BaseNode, node_type: Type[BaseNodeT]) -> BaseNodeT:
    """Clone tree to another ``Node`` type.
    If the same type is needed, simply do a tree.copy().

    Examples:
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
    assert_tree_type(tree, BaseNode, "BaseNode")

    # Start from root
    root_info = dict(tree.root.describe(exclude_prefix="_"))
    root_node = node_type(**root_info)

    def _recursive_add_child(
        _new_parent_node: BaseNodeT, _parent_node: BaseNode
    ) -> None:
        """Recursively clone current node

        Args:
            _new_parent_node (BaseNode): cloned parent node
            _parent_node (BaseNode): parent node to be cloned
        """
        for _child in _parent_node.children:
            if _child:
                child_info = dict(_child.describe(exclude_prefix="_"))
                child_node = node_type(**child_info)
                child_node.parent = _new_parent_node
                _recursive_add_child(child_node, _child)

    _recursive_add_child(root_node, tree.root)
    return root_node


def get_subtree(
    tree: NodeT,
    node_name_or_path: str = "",
    max_depth: int = 0,
) -> NodeT:
    """Get subtree based on node name or node path, and/or maximum depth of tree.

    Examples:
        >>> from bigtree import Node, get_subtree
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

        Get subtree

        >>> root_subtree = get_subtree(root, "b")
        >>> root_subtree.show()
        b
        ├── c
        └── d

    Args:
        tree (Node): existing tree
        node_name_or_path (str): node name or path to get subtree, defaults to None
        max_depth (int): maximum depth of subtree, based on `depth` attribute, defaults to None

    Returns:
        (Node)
    """
    tree = tree.copy()

    if node_name_or_path:
        tree = find_path(tree, node_name_or_path)
        if not tree:
            raise ValueError(f"Node name or path {node_name_or_path} not found")

    if not tree.is_root:
        tree.parent = None

    if max_depth:
        tree = prune_tree(tree, max_depth=max_depth)
    return tree


def prune_tree(
    tree: Union[BinaryNodeT, NodeT],
    prune_path: Union[List[str], str] = "",
    exact: bool = False,
    sep: str = "/",
    max_depth: int = 0,
) -> Union[BinaryNodeT, NodeT]:
    """Prune tree by path or depth, returns the root of a *copy* of the original tree.

    For pruning by `prune_path`,

    - All siblings along the prune path will be removed.
    - If ``exact=True``, all descendants of prune path will be removed.
    - Prune path can be string (only one path) or a list of strings (multiple paths).
    - Prune path name should be unique, can be full path, partial path (trailing part of path), or node name.

    For pruning by `max_depth`,

    - All nodes that are beyond `max_depth` will be removed.

    Path should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a").

    Examples:
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

        Prune (default is keep descendants)

        >>> root_pruned = prune_tree(root, "a/b")
        >>> root_pruned.show()
        a
        └── b
            ├── c
            └── d

        Prune exact path

        >>> root_pruned = prune_tree(root, "a/b", exact=True)
        >>> root_pruned.show()
        a
        └── b

        Prune multiple paths

        >>> root_pruned = prune_tree(root, ["a/b/d", "a/e"])
        >>> root_pruned.show()
        a
        ├── b
        │   └── d
        └── e

        Prune by depth

        >>> root_pruned = prune_tree(root, max_depth=2)
        >>> root_pruned.show()
        a
        ├── b
        └── e

    Args:
        tree (Union[BinaryNode, Node]): existing tree
        prune_path (List[str] | str): prune path(s), all siblings along the prune path(s) will be removed
        exact (bool): prune path(s) to be exactly the path, defaults to False (descendants of the path are retained)
        sep (str): path separator of `prune_path`
        max_depth (int): maximum depth of pruned tree, based on `depth` attribute, defaults to None

    Returns:
        (Union[BinaryNode, Node])
    """
    if isinstance(prune_path, str):
        prune_path = [prune_path] if prune_path else []

    if not len(prune_path) and not max_depth:
        raise ValueError("Please specify either `prune_path` or `max_depth` or both.")

    tree_copy = tree.copy()

    # Prune by path (prune bottom-up)
    if len(prune_path):
        ancestors_to_prune: Set[Union[BinaryNodeT, NodeT]] = set()
        nodes_to_prune: Set[Union[BinaryNodeT, NodeT]] = set()
        for path in prune_path:
            path = path.replace(sep, tree.sep)
            child = find_path(tree_copy, path)
            if not child:
                raise NotFoundError(
                    f"Cannot find any node matching path_name ending with {path}"
                )
            nodes_to_prune.add(child)
            ancestors_to_prune.update(list(child.ancestors))

        if exact:
            ancestors_to_prune.update(nodes_to_prune)

        for node in ancestors_to_prune:
            for child in node.children:
                if (
                    child
                    and child not in ancestors_to_prune
                    and child not in nodes_to_prune
                ):
                    child.parent = None

    # Prune by depth (prune top-down)
    if max_depth:
        for depth, level_nodes in enumerate(levelordergroup_iter(tree_copy), 1):
            if depth == max_depth:
                for level_node in level_nodes:
                    del level_node.children
    return tree_copy


def get_tree_diff(
    tree: Node, other_tree: Node, only_diff: bool = True, attr_list: List[str] = []
) -> Node:
    """Get difference of `tree` to `other_tree`, changes are relative to `tree`.

    Compares the difference in tree structure (default), but can also compare tree attributes using `attr_list`.
    Function can return only the differences (default), or all original tree nodes and differences.

    Comparing tree structure:

    - (+) and (-) will be added to node name relative to `tree`.
    - For example: (+) refers to nodes that are in `other_tree` but not `tree`.
    - For example: (-) refers to nodes that are in `tree` but not `other_tree`.

    Examples:
        >>> # Create original tree
        >>> from bigtree import Node, get_tree_diff, list_to_tree
        >>> root = list_to_tree(["Downloads/Pictures/photo1.jpg", "Downloads/file1.doc", "Downloads/photo2.jpg"])
        >>> root.show()
        Downloads
        ├── Pictures
        │   └── photo1.jpg
        ├── file1.doc
        └── photo2.jpg

        >>> # Create other tree
        >>> root_other = list_to_tree(["Downloads/Pictures/photo1.jpg", "Downloads/Pictures/photo2.jpg", "Downloads/file1.doc"])
        >>> root_other.show()
        Downloads
        ├── Pictures
        │   ├── photo1.jpg
        │   └── photo2.jpg
        └── file1.doc

        >>> # Get tree differences
        >>> tree_diff = get_tree_diff(root, root_other)
        >>> tree_diff.show()
        Downloads
        ├── photo2.jpg (-)
        └── Pictures
            └── photo2.jpg (+)

        >>> tree_diff = get_tree_diff(root, root_other, only_diff=False)
        >>> tree_diff.show()
        Downloads
        ├── Pictures
        │   ├── photo1.jpg
        │   └── photo2.jpg (+)
        ├── file1.doc
        └── photo2.jpg (-)

        Comparing tree attributes

        - (~) will be added to node name if there are differences in tree attributes defined in `attr_list`.
        - The node's attributes will be a list of [value in `tree`, value in `other_tree`]

        >>> # Create original tree
        >>> root = Node("Downloads")
        >>> picture_folder = Node("Pictures", parent=root)
        >>> photo2 = Node("photo1.jpg", tags="photo1", parent=picture_folder)
        >>> file1 = Node("file1.doc", tags="file1", parent=root)
        >>> root.show(attr_list=["tags"])
        Downloads
        ├── Pictures
        │   └── photo1.jpg [tags=photo1]
        └── file1.doc [tags=file1]

        >>> # Create other tree
        >>> root_other = Node("Downloads")
        >>> picture_folder = Node("Pictures", parent=root_other)
        >>> photo1 = Node("photo1.jpg", tags="photo1-edited", parent=picture_folder)
        >>> photo2 = Node("photo2.jpg", tags="photo2-new", parent=picture_folder)
        >>> file1 = Node("file1.doc", tags="file1", parent=root_other)
        >>> root_other.show(attr_list=["tags"])
        Downloads
        ├── Pictures
        │   ├── photo1.jpg [tags=photo1-edited]
        │   └── photo2.jpg [tags=photo2-new]
        └── file1.doc [tags=file1]

        >>> # Get tree differences
        >>> tree_diff = get_tree_diff(root, root_other, attr_list=["tags"])
        >>> tree_diff.show(attr_list=["tags"])
        Downloads
        └── Pictures
            ├── photo1.jpg (~) [tags=('photo1', 'photo1-edited')]
            └── photo2.jpg (+)

    Args:
        tree (Node): tree to be compared against
        other_tree (Node): tree to be compared with
        only_diff (bool): indicator to show all nodes or only nodes that are different (+/-), defaults to True
        attr_list (List[str]): tree attributes to check for difference, defaults to empty list

    Returns:
        (Node)
    """
    other_tree.sep = tree.sep
    name_col = "name"
    path_col = "PATH"
    indicator_col = "Exists"

    data, data_other = (
        tree_to_dataframe(
            _tree,
            name_col=name_col,
            path_col=path_col,
            attr_dict={k: k for k in attr_list},
        )
        for _tree in (tree, other_tree)
    )

    # Check tree structure difference
    data_both = data[[path_col, name_col] + attr_list].merge(
        data_other[[path_col, name_col] + attr_list],
        how="outer",
        on=[path_col, name_col],
        indicator=indicator_col,
    )

    # Handle tree structure difference
    nodes_removed = list(data_both[data_both[indicator_col] == "left_only"][path_col])[
        ::-1
    ]
    nodes_added = list(data_both[data_both[indicator_col] == "right_only"][path_col])[
        ::-1
    ]
    for node_removed in nodes_removed:
        data_both[path_col] = data_both[path_col].str.replace(
            node_removed, f"{node_removed} (-)", regex=True
        )
    for node_added in nodes_added:
        data_both[path_col] = data_both[path_col].str.replace(
            node_added, f"{node_added} (+)", regex=True
        )

    # Check tree attribute difference
    path_changes_list_of_dict: List[Dict[str, Dict[str, Any]]] = []
    path_changes_deque: Deque[str] = deque([])
    for attr_change in attr_list:
        condition_diff = (
            (
                ~data_both[f"{attr_change}_x"].isnull()
                | ~data_both[f"{attr_change}_y"].isnull()
            )
            & (data_both[f"{attr_change}_x"] != data_both[f"{attr_change}_y"])
            & (data_both[indicator_col] == "both")
        )
        data_diff = data_both[condition_diff]
        if len(data_diff):
            tuple_diff = zip(
                data_diff[f"{attr_change}_x"], data_diff[f"{attr_change}_y"]
            )
            dict_attr_diff = [{attr_change: v} for v in tuple_diff]
            dict_path_diff = dict(list(zip(data_diff[path_col], dict_attr_diff)))
            path_changes_list_of_dict.append(dict_path_diff)
            path_changes_deque.extend(list(data_diff[path_col]))

    if only_diff:
        data_both = data_both[
            (data_both[indicator_col] != "both")
            | (data_both[path_col].isin(path_changes_deque))
        ]
    data_both = data_both[[path_col]]
    if len(data_both):
        tree_diff = dataframe_to_tree(data_both, node_type=tree.__class__)
        # Handle tree attribute difference
        if len(path_changes_deque):
            path_changes_list = sorted(path_changes_deque, reverse=True)
            name_changes_list = [
                {k: {"name": f"{k.split(tree.sep)[-1]} (~)"} for k in path_changes_list}
            ]
            path_changes_list_of_dict.extend(name_changes_list)
            for attr_change_dict in path_changes_list_of_dict:
                tree_diff = add_dict_to_tree_by_path(tree_diff, attr_change_dict)
        return tree_diff

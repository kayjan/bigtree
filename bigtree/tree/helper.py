from typing import Any, Dict, List, Set, Type, TypeVar, Union

from bigtree.node import basenode, binarynode, node
from bigtree.tree import construct, export, search
from bigtree.utils import assertions, exceptions, iterators

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pd = MagicMock()

__all__ = [
    "clone_tree",
    "get_subtree",
    "prune_tree",
    "get_tree_diff_dataframe",
    "get_tree_diff",
]
BaseNodeT = TypeVar("BaseNodeT", bound=basenode.BaseNode)
BinaryNodeT = TypeVar("BinaryNodeT", bound=binarynode.BinaryNode)
NodeT = TypeVar("NodeT", bound=node.Node)


def clone_tree(tree: basenode.BaseNode, node_type: Type[BaseNodeT]) -> BaseNodeT:
    """Clone tree to another ``Node`` type. If the same type is needed, simply do a tree.copy().

    Examples:
        >>> from bigtree import BaseNode, Node, clone_tree
        >>> root = BaseNode(name="a")
        >>> b = BaseNode(name="b", parent=root)
        >>> clone_tree(root, Node)
        Node(/a, )

    Args:
        tree: tree to be cloned, must inherit from BaseNode
        node_type: type of cloned tree

    Returns:
        Cloned tree of another Node type
    """
    assertions.assert_tree_type(tree, basenode.BaseNode, "BaseNode")

    # Start from root
    root_info = dict(tree.root.describe(exclude_prefix="_"))
    root_node = node_type(**root_info)

    def _recursive_add_child(
        _new_parent_node: BaseNodeT, _parent_node: basenode.BaseNode
    ) -> None:
        """Recursively clone current node

        Args:
            _new_parent_node: cloned parent node
            _parent_node: parent node to be cloned
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
    """Get subtree based on node name or node path, and/or maximum depth of tree. Subtrees are smaller trees with
    different root. Returns a copy of the tree; does not affect original tree.

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
        tree: existing tree
        node_name_or_path: node name or path to get subtree
        max_depth: maximum depth of subtree, based on `depth` attribute

    Returns:
        Subtree
    """
    tree_sep = tree.sep
    tree = tree.copy()

    if node_name_or_path:
        tree = search.find_path(tree, node_name_or_path)
        if not tree:
            raise ValueError(f"Node name or path {node_name_or_path} not found")

    if not tree.is_root:
        tree.parent = None

    if max_depth:
        tree = prune_tree(tree, max_depth=max_depth)

    # Assign original tree's sep to subtree
    tree.sep = tree_sep
    return tree


def prune_tree(
    tree: Union[BinaryNodeT, NodeT],
    prune_path: Union[List[str], str] = "",
    exact: bool = False,
    sep: str = "/",
    max_depth: int = 0,
) -> Union[BinaryNodeT, NodeT]:
    """Prune tree by path or depth. Pruned trees are smaller trees with same root. Returns a copy of the tree; does not
    affect original tree.

    For pruning by `prune_path`,

    - All siblings along the prune path will be removed. All descendants will be kept by default
    - If ``exact=True``, all descendants of prune path will be removed
    - Prune path can be string (only one path) or a list of strings (multiple paths)
    - Prune path name should be unique, can be full path, partial path (trailing part of path), or node name

    For pruning by `max_depth`,

    - All nodes that are beyond `max_depth` will be removed

    Path should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a")

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

        Prune tree

        >>> root_pruned = prune_tree(root, "a/b")
        >>> root_pruned.show()
        a
        └── b
            ├── c
            └── d

        Prune by exact path

        >>> root_pruned = prune_tree(root, "a/b", exact=True)
        >>> root_pruned.show()
        a
        └── b

        Prune by multiple paths

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
        tree: existing tree
        prune_path: prune path(s), all siblings along the prune path(s) will be removed
        exact: prune path(s) to be exactly the path and remove descendants
        sep: path separator of `prune_path`
        max_depth: maximum depth of pruned tree, based on `depth` attribute

    Returns:
        Pruned tree
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
            child = search.find_path(tree_copy, path)
            if not child:
                raise exceptions.NotFoundError(
                    f"Cannot find any node matching path_name ending with {path}"
                )
            nodes_to_prune.add(child)
            ancestors_to_prune.update(list(child.ancestors))

        if exact:
            ancestors_to_prune.update(nodes_to_prune)

        for _node in ancestors_to_prune:
            for child in _node.children:
                if (
                    child
                    and child not in ancestors_to_prune
                    and child not in nodes_to_prune
                ):
                    child.parent = None

    # Prune by depth (prune top-down)
    if max_depth:
        for depth, level_nodes in enumerate(
            iterators.levelordergroup_iter(tree_copy), 1
        ):
            if depth == max_depth:
                for level_node in level_nodes:
                    del level_node.children
    return tree_copy


@exceptions.optional_dependencies_pandas
def get_tree_diff_dataframe(
    tree: node.Node,
    other_tree: node.Node,
    only_diff: bool = True,
    detail: bool = False,
    aggregate: bool = False,
    attr_list: List[str] = [],
    fallback_sep: str = "/",
    name_col: str = "name",
    path_col: str = "path",
    parent_col: str = "parent",
    indicator_col: str = "Exists",
    old_suffix: str = "_old",
    new_suffix: str = "_new",
    suffix_col: str = "suffix",
) -> pd.DataFrame:
    """Get difference of `tree` to `other_tree`, changes are relative to `tree`. This function exports both trees to
    pandas DataFrame, merge them, and adds new suffix column to indicate the type of differences in both trees.

    # Comparing tree structure

    By default, suffix will be '+' and '-' for the tree differences, and np.nan for the others.

    - If `detail=True`, 'added' and 'moved to' will be used instead of '+', and 'removed' and 'moved from' will be used
        instead of '-'
    - If `aggregate=True`, suffix will only be indicated at the parent-level. This is useful when a subtree is shifted
        and we want the differences shown only at the top node

    # Compare tree attribute

    Attributes indicated in `attr_list` will be exported in the pandas DataFrame with suffixes representing attributes
    from `tree` and `other_tree` respectively.

    Examples:
        >>> # Create original tree
        >>> from bigtree import Node, get_tree_diff_dataframe, list_to_tree
        >>> root = list_to_tree(["Downloads/Pictures/photo1.jpg", "Downloads/file1.doc", "Downloads/Trip/photo2.jpg"])
        >>> root.show()
        Downloads
        ├── Pictures
        │   └── photo1.jpg
        ├── file1.doc
        └── Trip
            └── photo2.jpg

        >>> # Create other tree
        >>> root_other = list_to_tree(
        ...     ["Downloads/Pictures/photo1.jpg", "Downloads/Pictures/Trip/photo2.jpg", "Downloads/file1.doc", "Downloads/file2.doc"]
        ... )
        >>> root_other.show()
        Downloads
        ├── Pictures
        │   ├── photo1.jpg
        │   └── Trip
        │       └── photo2.jpg
        ├── file1.doc
        └── file2.doc

        Comparing tree structure

        >>> get_tree_diff_dataframe(root, root_other, detail=True)
                                          path        name     parent      Exists      suffix
        0                           /Downloads   Downloads       None        both         NaN
        1                  /Downloads/Pictures    Pictures  Downloads        both         NaN
        2             /Downloads/Pictures/Trip        Trip   Pictures  right_only    moved to
        3  /Downloads/Pictures/Trip/photo2.jpg  photo2.jpg       Trip  right_only    moved to
        4       /Downloads/Pictures/photo1.jpg  photo1.jpg   Pictures        both         NaN
        5                      /Downloads/Trip        Trip  Downloads   left_only  moved from
        6           /Downloads/Trip/photo2.jpg  photo2.jpg       Trip   left_only  moved from
        7                 /Downloads/file1.doc   file1.doc  Downloads        both         NaN
        8                 /Downloads/file2.doc   file2.doc  Downloads  right_only       added

    !!! note

        - tree and other_tree must have the same `sep` symbol, otherwise this will raise ValueError
        - If the `sep` symbol contains one of `+` / `-` / `~` character, a fallback sep will be used
        - Node names in tree and other_tree must not contain the `sep` (or fallback sep) symbol

    Args:
        tree: tree to be compared against
        other_tree: tree to be compared with
        only_diff: if aggregate and only_diff are True, child nodes that are moved from tree will be removed
        detail: by default, suffix column will display "+" and "-". If detail is True, suffix column will be more
            detailed, displaying "moved from" / "moved to" / "added" / "removed" instead
        aggregate: by default, all nodes that are different will have suffix specified. If aggregate is True,
            only parent-level node have suffixes and nodes that have different paths but same parent will not have suffix
        attr_list: tree attributes to retrieve from tree and other_tree
        fallback_sep: sep to fall back to if tree and other_tree has sep that clashes with symbols "+" / "-" / "~".
            All node names in tree and other_tree should not contain this fallback_sep
        name_col: name column of return dataframe, indicates the name of node
        path_col: path column of return dataframe, indicates the full path of node
        parent_col: parent column of return dataframe, indicates the parent name of node
        indicator_col: indicator column of return dataframe, indicates whether node appears in left_only, right_only
            or both tree
        old_suffix: suffix given to attributes from tree of return dataframe, relevant if attr_list is specified
        new_suffix: suffix given to attributes from other_tree of return dataframe, relevant if attr_list is specified
        suffix_col: suffix column of return dataframe, indicates the type of diff whether it is added, removed, or moved

    Returns:
        Dataframe of tree differences
    """
    if tree.sep != other_tree.sep:
        raise ValueError("`sep` must be the same for tree and other_tree")

    forbidden_sep_symbols = ["+", "-", "~"]
    if any(
        forbidden_sep_symbol in tree.sep
        for forbidden_sep_symbol in forbidden_sep_symbols
    ):
        tree.sep = fallback_sep
        other_tree.sep = fallback_sep

    data, data_other = (
        export.tree_to_dataframe(
            _tree,
            name_col=name_col,
            path_col=path_col,
            parent_col=parent_col,
            attr_dict={k: k for k in attr_list},
        )
        for _tree in (tree, other_tree)
    )

    # Combine both trees to compare
    data_combine = data[[path_col, name_col, parent_col] + attr_list].merge(
        data_other[[path_col, name_col, parent_col] + attr_list],
        how="outer",
        on=[path_col, name_col, parent_col],
        indicator=indicator_col,
        suffixes=(old_suffix, new_suffix),
    )
    data_compare = data_combine[[path_col, name_col, parent_col, indicator_col]]

    # If aggregate, drop differences where node parent remains the same
    if aggregate:
        data_compare = data_compare[
            (data_compare[indicator_col] == "left_only")
            | (data_compare[indicator_col] == "right_only")
        ].drop_duplicates(subset=[name_col, parent_col], keep=False)
        if only_diff:
            # If only_diff and aggregate, remove children under (moved from)
            data_combine = data_combine.sort_values(indicator_col, ascending=False)
            data_combine = data_combine[
                ~data_combine.duplicated(subset=[name_col, parent_col])
            ]  # keep right_only

    # Determine the type of shift in suffix column
    data_tree = data_compare[data_compare[indicator_col] == "left_only"]
    data_tree_other = data_compare[data_compare[indicator_col] == "right_only"]

    if detail:
        data_tree[suffix_col] = "removed"
        data_tree_other[suffix_col] = "added"

        if len(data_tree) and len(data_tree_other):
            # Check for moved from and moved to
            move_from_condition = data_tree[
                data_tree[name_col].isin(set(data_tree_other[name_col]))
            ]
            data_tree.loc[move_from_condition.index, suffix_col] = "moved from"
            move_to_condition = data_tree_other[
                data_tree_other[name_col].isin(set(data_tree[name_col]))
            ]
            data_tree_other.loc[move_to_condition.index, suffix_col] = "moved to"
    else:
        data_tree[suffix_col] = "-"
        data_tree_other[suffix_col] = "+"

    data_tree_diff = pd.merge(
        data_combine,
        pd.concat([data_tree, data_tree_other]),
        on=[path_col, name_col, parent_col, indicator_col],
        how="left",
    )
    return data_tree_diff


@exceptions.optional_dependencies_pandas
def get_tree_diff(
    tree: node.Node,
    other_tree: node.Node,
    only_diff: bool = True,
    detail: bool = False,
    aggregate: bool = False,
    attr_list: List[str] = [],
    fallback_sep: str = "/",
) -> node.Node:
    """Get difference of `tree` to `other_tree`, changes are relative to `tree`.

    Compares the difference in tree structure (default), but can also compare tree attributes using `attr_list`.
    Function can return only the differences (default), or all original tree nodes and differences.

    # Comparing tree structure

    - (+) and (-) will be added to node name relative to `tree`
    - For example: (+) refers to nodes that are in `other_tree` but not `tree`
    - For example: (-) refers to nodes that are in `tree` but not `other_tree`

    If `detail=True`, (added) and (moved to) will be used instead of (+), (removed) and (moved from) will be used
    instead of (-).

    If `aggregate=True`, differences (+)/(added)/(moved to) and (-)/(removed)/(moved from) will only be indicated at
    the parent-level. This is useful when a subtree is shifted, and we want the differences shown only at the top node.

    Examples:
        >>> # Create original tree
        >>> from bigtree import Node, get_tree_diff, list_to_tree
        >>> root = list_to_tree(["Downloads/Pictures/photo1.jpg", "Downloads/file1.doc", "Downloads/Trip/photo2.jpg"])
        >>> root.show()
        Downloads
        ├── Pictures
        │   └── photo1.jpg
        ├── file1.doc
        └── Trip
            └── photo2.jpg

        >>> # Create other tree
        >>> root_other = list_to_tree(
        ...     ["Downloads/Pictures/photo1.jpg", "Downloads/Pictures/Trip/photo2.jpg", "Downloads/file1.doc", "Downloads/file2.doc"]
        ... )
        >>> root_other.show()
        Downloads
        ├── Pictures
        │   ├── photo1.jpg
        │   └── Trip
        │       └── photo2.jpg
        ├── file1.doc
        └── file2.doc

        Comparing tree structure

        >>> tree_diff = get_tree_diff(root, root_other)
        >>> tree_diff.show()
        Downloads
        ├── Pictures
        │   └── Trip (+)
        │       └── photo2.jpg (+)
        ├── Trip (-)
        │   └── photo2.jpg (-)
        └── file2.doc (+)

        All differences

        >>> tree_diff = get_tree_diff(root, root_other, only_diff=False)
        >>> tree_diff.show()
        Downloads
        ├── Pictures
        │   ├── Trip (+)
        │   │   └── photo2.jpg (+)
        │   └── photo1.jpg
        ├── Trip (-)
        │   └── photo2.jpg (-)
        ├── file1.doc
        └── file2.doc (+)

        All differences with details

        >>> tree_diff = get_tree_diff(
        ...     root, root_other, only_diff=False, detail=True
        ... )
        >>> tree_diff.show()
        Downloads
        ├── Pictures
        │   ├── Trip (moved to)
        │   │   └── photo2.jpg (moved to)
        │   └── photo1.jpg
        ├── Trip (moved from)
        │   └── photo2.jpg (moved from)
        ├── file1.doc
        └── file2.doc (added)

        All differences with details on aggregated level

        >>> tree_diff = get_tree_diff(
        ...     root, root_other, only_diff=False, detail=True, aggregate=True
        ... )
        >>> tree_diff.show()
        Downloads
        ├── Pictures
        │   ├── Trip (moved to)
        │   │   └── photo2.jpg
        │   └── photo1.jpg
        ├── Trip (moved from)
        │   └── photo2.jpg
        ├── file1.doc
        └── file2.doc (added)

        Only differences with details on aggregated level

        >>> tree_diff = get_tree_diff(root, root_other, detail=True, aggregate=True)
        >>> tree_diff.show()
        Downloads
        ├── Pictures
        │   └── Trip (moved to)
        │       └── photo2.jpg
        ├── Trip (moved from)
        └── file2.doc (added)

        # Comparing tree attribute

        - (~) will be added to node name if there are differences in tree attributes defined in `attr_list`
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

        >>> # Get tree attribute differences
        >>> tree_diff = get_tree_diff(root, root_other, attr_list=["tags"])
        >>> tree_diff.show(attr_list=["tags"])
        Downloads
        └── Pictures
            ├── photo1.jpg (~) [tags=('photo1', 'photo1-edited')]
            └── photo2.jpg (+)

    !!! note

        - tree and other_tree must have the same `sep` symbol, otherwise this will raise ValueError
        - If the `sep` symbol contains one of `+` / `-` / `~` character, a fallback sep will be used
        - Node names in tree and other_tree must not contain the `sep` (or fallback sep) symbol

    Args:
        tree: tree to be compared against
        other_tree: tree to be compared with
        only_diff: indicator to show all nodes or only nodes that are different (+/-)
        detail: indicator to differentiate between different types of diff e.g., added or removed or moved
        aggregate: indicator to only add difference indicator to parent-level e.g., when shifting subtrees
        attr_list: tree attributes to check for difference
        fallback_sep: sep to fall back to if tree and other_tree has sep that clashes with symbols "+" / "-" / "~".
            All node names in tree and other_tree should not contain this fallback_sep

    Returns:
        Tree highlighting the difference between tree and other_tree
    """
    name_col = "name"
    path_col = "path"
    parent_col = "parent"
    indicator_col = "Exists"
    old_suffix = "_old"
    new_suffix = "_new"
    suffix_col = "suffix"

    data_diff_all = get_tree_diff_dataframe(
        tree,
        other_tree,
        only_diff,
        detail,
        aggregate,
        attr_list,
        fallback_sep,
        name_col,
        path_col,
        parent_col,
        indicator_col,
        old_suffix,
        new_suffix,
        suffix_col,
    )

    # Check tree structure difference
    data_diff = data_diff_all.dropna(subset=[suffix_col])
    path_to_suffix = dict(zip(data_diff[path_col], data_diff[suffix_col]))

    # Check tree attribute difference
    path_attr_diff: Dict[str, Dict[str, Any]] = {}
    if attr_list:
        data_both = data_diff_all[data_diff_all[indicator_col] == "both"]
        condition_attr_diff = (
            "("
            + ") | (".join(
                [
                    f"""(data_both["{attr}{old_suffix}"] != data_both["{attr}{new_suffix}"]) """
                    f"""& ~(data_both["{attr}{old_suffix}"].isnull() & data_both["{attr}{new_suffix}"].isnull())"""
                    for attr in attr_list
                ]
            )
            + ")"
        )
        data_attr_diff = data_both[eval(condition_attr_diff)]
        dict_attr_all = data_attr_diff.set_index(path_col).to_dict(orient="index")
        for path, node_attr in dict_attr_all.items():
            path_attr_diff[path] = {
                attr: (
                    node_attr[f"{attr}{old_suffix}"],
                    node_attr[f"{attr}{new_suffix}"],
                )
                for attr in attr_list
                if node_attr[f"{attr}{old_suffix}"] != node_attr[f"{attr}{new_suffix}"]
                and node_attr[f"{attr}{old_suffix}"]
                and node_attr[f"{attr}{new_suffix}"]
            }

    if only_diff:
        data_diff_all = data_diff_all[
            (data_diff_all[indicator_col] != "both")
            | (data_diff_all[path_col].isin(path_attr_diff.keys()))
        ]
    data_diff_all = data_diff_all[[path_col]].sort_values(path_col)
    if len(data_diff_all):
        tree_diff = construct.dataframe_to_tree(
            data_diff_all, node_type=tree.__class__, sep=tree.sep
        )
        # Handle tree structure difference
        for path in sorted(path_to_suffix, reverse=True):
            _node = search.find_full_path(tree_diff, path)
            _node.name += f""" ({path_to_suffix[path]})"""

        # Handle tree attribute difference
        if path_attr_diff:
            tree_diff = construct.add_dict_to_tree_by_path(tree_diff, path_attr_diff)
            for path in sorted(path_attr_diff, reverse=True):
                _node = search.find_full_path(tree_diff, path)
                _node.name += " (~)"
        return tree_diff

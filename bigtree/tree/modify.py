import logging
from typing import List, Optional

from bigtree.node.node import Node
from bigtree.tree.search import find_path
from bigtree.utils.exceptions import NotFoundError, TreeError

logger = logging.getLogger(__name__)


__all__ = [
    "shift_nodes",
    "copy_nodes",
    "copy_nodes_from_tree_to_tree",
    "copy_or_shift_logic",
]


def shift_nodes(
    tree: Node,
    from_paths: List[str],
    to_paths: List[str],
    sep: str = "/",
    skippable: bool = False,
    overriding: bool = False,
    merge_children: bool = False,
):
    """Shift nodes from `from_paths` to `to_paths` *in-place*.

    - Creates intermediate nodes if to path is not present
    - Able to skip nodes if from path is not found, defaults to False (from-nodes must be found; not skippable).
    - Able to override existing node if it exists, defaults to False (to-nodes must not exist; not overridden).
    - Able to merge children and remove intermediate parent node, defaults to False (nodes are shifted; not merged).

    For paths in `from_paths` and `to_paths`,
      - Path name can be with or without leading tree path separator symbol.
      - Path name can be partial path (trailing part of path) or node name.
      - Path name must be unique to one node.

    For paths in `to_paths`,
      - Can set to empty string or None to delete the path in `from_paths`.

    >>> from bigtree import Node, shift_nodes, print_tree
    >>> root = Node("a")
    >>> b = Node("b", parent=root)
    >>> c = Node("c", parent=root)
    >>> d = Node("d", parent=root)
    >>> print_tree(root)
    a
    |-- b
    |-- c
    `-- d

    >>> shift_nodes(root, ["a/c", "a/d"], ["a/b/c", "a/dummy/d"])
    >>> print_tree(root)
    a
    |-- b
    |   `-- c
    `-- dummy
        `-- d

    Args:
        tree (Node): tree to modify
        from_paths (list): original paths to shift nodes from
        to_paths (list): new paths to shift nodes to
        sep (str): path separator for input paths, applies to `from_path` and `to_path`
        skippable (bool): indicator to skip if from path is not found, defaults to False
        overriding (bool): indicator to override existing to path if there is clashes, defaults to False
        merge_children (bool): indicator to merge children and remove intermediate parent node, defaults to False
    """
    return copy_or_shift_logic(
        tree=tree,
        from_paths=from_paths,
        to_paths=to_paths,
        sep=sep,
        copy=False,
        skippable=skippable,
        overriding=overriding,
        merge_children=merge_children,
        to_tree=None,
    )  # pragma: no cover


def copy_nodes(
    tree: Node,
    from_paths: List[str],
    to_paths: List[str],
    sep: str = "/",
    skippable: bool = False,
    overriding: bool = False,
    merge_children: bool = False,
):
    """Copy nodes from `from_paths` to `to_paths` *in-place*.

    - Creates intermediate nodes if to path is not present
    - Able to skip nodes if from path is not found, defaults to False (from-nodes must be found; not skippable).
    - Able to override existing node if it exists, defaults to False (to-nodes must not exist; not overridden).
    - Able to merge children and remove intermediate parent node, defaults to False (nodes are shifted; not merged).

    For paths in `from_paths` and `to_paths`,
      - Path name can be with or without leading tree path separator symbol.
      - Path name can be partial path (trailing part of path) or node name.
      - Path name must be unique to one node.

    For paths in `to_paths`,
      - Can set to empty string or None to delete the path in `from_paths`.

    >>> from bigtree import Node, copy_nodes, print_tree
    >>> root = Node("a")
    >>> b = Node("b", parent=root)
    >>> c = Node("c", parent=root)
    >>> d = Node("d", parent=root)
    >>> print_tree(root)
    a
    |-- b
    |-- c
    `-- d

    >>> copy_nodes(root, ["a/c", "a/d"], ["a/b/c", "a/dummy/d"])
    >>> print_tree(root)
    a
    |-- b
    |   `-- c
    |-- c
    |-- d
    `-- dummy
        `-- d

    Args:
        tree (Node): tree to modify
        from_paths (list): original paths to shift nodes from
        to_paths (list): new paths to shift nodes to
        sep (str): path separator for input paths, applies to `from_path` and `to_path`
        skippable (bool): indicator to skip if from path is not found, defaults to False
        overriding (bool): indicator to override existing to path if there is clashes, defaults to False
        merge_children (bool): indicator to merge children and remove intermediate parent node, defaults to False
    """
    return copy_or_shift_logic(
        tree=tree,
        from_paths=from_paths,
        to_paths=to_paths,
        sep=sep,
        copy=True,
        skippable=skippable,
        overriding=overriding,
        merge_children=merge_children,
        to_tree=None,
    )  # pragma: no cover


def copy_nodes_from_tree_to_tree(
    from_tree: Node,
    to_tree: Node,
    from_paths: List[str],
    to_paths: List[str],
    sep: str = "/",
    skippable: bool = False,
    overriding: bool = False,
    merge_children: bool = False,
):
    """Copy nodes from `from_paths` to `to_paths` *in-place*.

    - Creates intermediate nodes if to path is not present
    - Able to skip nodes if from path is not found, defaults to False (from-nodes must be found; not skippable).
    - Able to override existing node if it exists, defaults to False (to-nodes must not exist; not overridden).
    - Able to merge children and remove intermediate parent node, defaults to False (nodes are shifted; not merged).

    For paths in `from_paths` and `to_paths`,
      - Path name can be with or without leading tree path separator symbol.
      - Path name can be partial path (trailing part of path) or node name.
      - Path name must be unique to one node.

    For paths in `to_paths`,
      - Can set to empty string or None to delete the path in `from_paths`.

    >>> from bigtree import Node, copy_nodes_from_tree_to_tree, print_tree
    >>> root = Node("a")
    >>> b = Node("b", parent=root)
    >>> c = Node("c", parent=root)
    >>> d = Node("d", parent=root)
    >>> print_tree(root)
    a
    |-- b
    |-- c
    `-- d

    >>> root_other = Node("aa")
    >>> copy_nodes_from_tree_to_tree(root, root_other, ["a/b", "a/c", "a/d"], ["aa/b", "aa/b/c", "aa/dummy/d"])
    >>> print_tree(root_other)
    aa
    |-- b
    |   `-- c
    `-- dummy
        `-- d

    Args:
        from_tree (Node): tree to copy nodes from
        to_tree (Node): tree to copy nodes to
        from_paths (list): original paths to shift nodes from
        to_paths (list): new paths to shift nodes to
        sep (str): path separator for input paths, applies to `from_path` and `to_path`
        skippable (bool): indicator to skip if from path is not found, defaults to False
        overriding (bool): indicator to override existing to path if there is clashes, defaults to False
        merge_children (bool): indicator to merge children and remove intermediate parent node, defaults to False
    """
    return copy_or_shift_logic(
        tree=from_tree,
        from_paths=from_paths,
        to_paths=to_paths,
        sep=sep,
        copy=True,
        skippable=skippable,
        overriding=overriding,
        merge_children=merge_children,
        to_tree=to_tree,
    )  # pragma: no cover


def copy_or_shift_logic(
    tree: Node,
    from_paths: List[str],
    to_paths: List[str],
    sep: str = "/",
    copy: bool = False,
    skippable: bool = False,
    overriding: bool = False,
    merge_children: bool = False,
    to_tree: Optional[Node] = None,
):
    """Shift or copy nodes from `from_paths` to `to_paths` *in-place*.

    - Creates intermediate nodes if to path is not present
    - Able to copy node, defaults to False (nodes are shifted; not copied).
    - Able to skip nodes if from path is not found, defaults to False (from-nodes must be found; not skippable)
    - Able to override existing node if it exists, defaults to False (to-nodes must not exist; not overridden)
    - Able to merge children and remove intermediate parent node, defaults to False (nodes are shifted; not merged)
    - Able to copy nodes from one tree to another tree, defaults to None (shifting/copying happens within same tree)

    For paths in `from_paths` and `to_paths`,
      - Path name can be with or without leading tree path separator symbol.
      - Path name can be partial path (trailing part of path) or node name.
      - Path name must be unique to one node.

    For paths in `to_paths`,
      - Can set to empty string or None to delete the path in `from_paths`.

    Args:
        tree (Node): tree to modify
        from_paths (list): original paths to shift nodes from
        to_paths (list): new paths to shift nodes to
        sep (str): path separator for input paths, applies to `from_path` and `to_path`
        copy (bool): indicator to copy node, defaults to False
        skippable (bool): indicator to skip if from path is not found, defaults to False
        overriding (bool): indicator to override existing to path if there is clashes, defaults to False
        merge_children (bool): indicator to merge children and remove intermediate parent node, defaults to False
        to_tree (Node): tree to copy to, defaults to None
    """
    if not (isinstance(from_paths, list) and isinstance(to_paths, list)):
        raise ValueError(
            "Invalid type, `from_paths` and `to_paths` should be list type"
        )
    if len(from_paths) != len(to_paths):
        raise ValueError(
            f"Paths are different length, input `from_paths` have {len(from_paths)} entries, "
            f"while output `to_paths` have {len(to_paths)} entries"
        )
    for from_path, to_path in zip(from_paths, to_paths):
        if to_path:
            if from_path.split(sep)[-1] != to_path.split(sep)[-1]:
                raise ValueError(
                    f"Unable to assign from_path {from_path} to to_path {to_path}\n"
                    f"Verify that `sep` is defined correctly for path\n"
                    f"Alternatively, check that `from_path` and `to_path` is reassigning the same node"
                )

    transfer_indicator = False
    node_type = tree.__class__
    tree_sep = tree.sep
    if to_tree:
        transfer_indicator = True
        node_type = to_tree.__class__
        tree_sep = to_tree.sep
    for from_path, to_path in zip(from_paths, to_paths):
        from_path = from_path.replace(sep, tree.sep)
        from_node = find_path(tree, from_path)

        # From node not found
        if not from_node:
            if not skippable:
                raise NotFoundError(
                    f"Unable to find from_path {from_path}\n"
                    f"Set `skippable` to True to skip shifting for nodes not found"
                )
            else:
                logger.info(f"Unable to find from_path {from_path}")

        # From node found
        else:
            # Node to be deleted
            if not to_path:
                to_node = None
            # Node to be copied/shifted
            else:
                to_path = to_path.replace(sep, tree_sep)
                if transfer_indicator:
                    to_node = find_path(to_tree, to_path)
                else:
                    to_node = find_path(tree, to_path)

                # To node found
                if to_node:
                    if merge_children:
                        continue
                    if from_node == to_node:
                        raise TreeError(
                            f"Attempting to shift the same node {from_node} back to the same position\n"
                            f"Check from path {from_path} and to path {to_path}"
                        )
                    if not overriding:
                        raise TreeError(
                            f"Path {to_path} already exists and unable to override\n"
                            f"Set `overriding` to True to perform overrides"
                        )
                    logger.info(f"Path {to_path} already exists and will be overridden")
                    parent = to_node.parent
                    to_node.parent = None
                    to_node = parent

                # To node not found
                else:
                    # Find parent node
                    to_path_list = to_path.split(tree_sep)
                    idx = 1
                    to_path_parent = tree_sep.join(to_path_list[:-idx])
                    if transfer_indicator:
                        to_node = find_path(to_tree, to_path_parent)
                    else:
                        to_node = find_path(tree, to_path_parent)

                    # Create intermediate parent node, if applicable
                    while (not to_node) & (idx + 1 < len(to_path_list)):
                        idx += 1
                        to_path_parent = sep.join(to_path_list[:-idx])
                        if transfer_indicator:
                            to_node = find_path(to_tree, to_path_parent)
                        else:
                            to_node = find_path(tree, to_path_parent)
                    if not to_node:
                        raise NotFoundError(
                            f"Unable to find to_path {to_path}\n"
                            f"Please specify valid path to shift node to"
                        )
                    for depth in range(len(to_path_list) - idx, len(to_path_list) - 1):
                        intermediate_child_node = node_type(to_path_list[depth])
                        intermediate_child_node.parent = to_node
                        to_node = intermediate_child_node

            # Reassign from_node to new parent
            if copy:
                logger.info(f"Copying {from_node} to {to_node}")
                from_node = from_node.copy()
            if merge_children:
                logger.info(f"Reassigning children from {from_node} to {to_node}")
                for children in list(from_node.children):
                    children.parent = to_node
                from_node.parent = None
            else:
                from_node.parent = to_node

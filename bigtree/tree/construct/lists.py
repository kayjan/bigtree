from __future__ import annotations

from collections import OrderedDict
from typing import List, Tuple, Type, TypeVar

from bigtree.node import node
from bigtree.tree.construct.dataframes import dataframe_to_tree_by_relation
from bigtree.tree.construct.strings import add_path_to_tree
from bigtree.utils import assertions, exceptions

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pd = MagicMock()

__all__ = [
    "list_to_tree",
    "list_to_tree_by_relation",
]

T = TypeVar("T", bound=node.Node)


def list_to_tree(
    paths: List[str],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[T] = node.Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from list of path strings.

    Path should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a")

    Path can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/"

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node

    Examples:
        >>> from bigtree import list_to_tree
        >>> path_list = ["a/b", "a/c", "a/b/d", "a/b/e", "a/c/f", "a/b/e/g", "a/b/e/h"]
        >>> root = list_to_tree(path_list)
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f

    Args:
        paths: list containing path strings
        sep: path separator for input `paths` and created tree
        duplicate_name_allowed: indicator if nodes with duplicate ``Node`` name is allowed
        node_type: node type of tree to be created

    Returns:
        Node
    """
    assertions.assert_length_not_empty(paths, "Path list", "paths")

    # Remove duplicates
    paths = list(OrderedDict.fromkeys(paths))

    # Construct root node
    root_name = paths[0].lstrip(sep).split(sep)[0]
    root_node = node_type(root_name)
    root_node.sep = sep

    for path in paths:
        add_path_to_tree(
            root_node, path, sep=sep, duplicate_name_allowed=duplicate_name_allowed
        )
    return root_node


@exceptions.optional_dependencies_pandas
def list_to_tree_by_relation(
    relations: List[Tuple[str, str]],
    allow_duplicates: bool = False,
    node_type: Type[T] = node.Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from list of tuple containing parent-child names.

    Root node is inferred when parent is empty, or when name appears as parent but not as child.

    Since tree is created from parent-child names, only names of leaf nodes may be repeated. Error will be thrown if
    names of intermediate nodes are repeated as there will be confusion. This error can be ignored by setting
    `allow_duplicates` to be True.

    Examples:
        >>> from bigtree import list_to_tree_by_relation
        >>> relations_list = [("a", "b"), ("a", "c"), ("b", "d"), ("b", "e"), ("c", "f"), ("e", "g"), ("e", "h")]
        >>> root = list_to_tree_by_relation(relations_list)
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f

    Args:
        relations: list containing tuple containing parent-child names
        allow_duplicates : allow duplicate intermediate nodes such that child node will be tagged to multiple parent nodes
        node_type: node type of tree to be created

    Returns:
        Node
    """
    assertions.assert_length_not_empty(relations, "Path list", "relations")

    relation_data = pd.DataFrame(relations, columns=["parent", "child"])
    return dataframe_to_tree_by_relation(
        relation_data,
        child_col="child",
        parent_col="parent",
        allow_duplicates=allow_duplicates,
        node_type=node_type,
    )

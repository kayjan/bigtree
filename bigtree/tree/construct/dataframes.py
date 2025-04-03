from __future__ import annotations

from typing import Any, Dict, List, Type, TypeVar

from bigtree.node import node
from bigtree.tree.construct.dictionaries import add_dict_to_tree_by_name
from bigtree.tree.construct.strings import add_path_to_tree
from bigtree.utils import assertions

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pd = MagicMock()

try:
    import polars as pl
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pl = MagicMock()

__all__ = [
    "add_dataframe_to_tree_by_path",
    "add_dataframe_to_tree_by_name",
    "add_polars_to_tree_by_path",
    "add_polars_to_tree_by_name",
    "dataframe_to_tree",
    "dataframe_to_tree_by_relation",
    "polars_to_tree",
    "polars_to_tree_by_relation",
]

T = TypeVar("T", bound=node.Node)


def add_dataframe_to_tree_by_path(
    tree: T,
    data: pd.DataFrame,
    path_col: str = "",
    attribute_cols: List[str] = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
) -> T:
    """Add nodes and attributes to tree *in-place*, return root of tree. Adds to existing tree from pandas DataFrame.

    `path_col` and `attribute_cols` specify columns for node path and attributes to add to existing tree. If columns are
    not specified, `path_col` takes first column and all other columns are `attribute_cols`

    - Only attributes in `attribute_cols` with non-null values will be added to the tree

    Path in path column should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a")
    - Path separator `sep` is for the input `path` and can differ from existing tree

    Path in path column can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/"

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node

    Examples:
        >>> import pandas as pd
        >>> from bigtree import add_dataframe_to_tree_by_path, Node
        >>> root = Node("a")
        >>> path_data = pd.DataFrame([
        ...     ["a", 90],
        ...     ["a/b", 65],
        ...     ["a/c", 60],
        ...     ["a/b/d", 40],
        ...     ["a/b/e", 35],
        ...     ["a/c/f", 38],
        ...     ["a/b/e/g", 10],
        ...     ["a/b/e/h", 6],
        ... ],
        ...     columns=["PATH", "age"]
        ... )
        >>> root = add_dataframe_to_tree_by_path(root, path_data)
        >>> root.show(attr_list=["age"])
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        │       ├── g [age=10]
        │       └── h [age=6]
        └── c [age=60]
            └── f [age=38]

    Args:
        tree: existing tree
        data: data containing node path and attribute information
        path_col: column of data containing `path_name` information, if not set, it will take the first column of data
        attribute_cols: columns of data containing node attribute information, if not set, it will take all columns of
            data except `path_col`
        sep: path separator for input `path_col`
        duplicate_name_allowed: indicator if nodes with duplicate ``Node`` name is allowed

    Returns:
        Node
    """
    assertions.assert_dataframe_not_empty(data)

    if not path_col:
        path_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(path_col)

    data = data[[path_col] + attribute_cols].copy()
    data[path_col] = data[path_col].str.lstrip(sep).str.rstrip(sep)
    assertions.assert_dataframe_no_duplicate_attribute(
        data, "path", path_col, attribute_cols
    )

    root_node = tree.root
    for row in data.to_dict(orient="index").values():
        node_attrs = assertions.filter_attributes(
            row, omit_keys=["name", path_col], omit_null_values=True
        )
        add_path_to_tree(
            root_node,
            row[path_col],
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    return root_node


def add_dataframe_to_tree_by_name(
    tree: T,
    data: pd.DataFrame,
    name_col: str = "",
    attribute_cols: List[str] = [],
) -> T:
    """Add attributes to existing tree *in-place*. Adds to existing tree from pandas DataFrame.

    `name_col` and `attribute_cols` specify columns for node name and attributes to add to existing tree. If columns are
    not specified, the first column will be taken as name column and all other columns as attributes.

    - Only attributes in `attribute_cols` with non-null values will be added to the tree
    - Input data node names that are not existing node names will be ignored. Note that if multiple nodes have the same
        name, attributes will be added to all nodes sharing same name

    Examples:
        >>> import pandas as pd
        >>> from bigtree import add_dataframe_to_tree_by_name, Node
        >>> root = Node("a")
        >>> b = Node("b", parent=root)
        >>> name_data = pd.DataFrame([
        ...     ["a", 90],
        ...     ["b", 65],
        ... ],
        ...     columns=["NAME", "age"]
        ... )
        >>> root = add_dataframe_to_tree_by_name(root, name_data)
        >>> root.show(attr_list=["age"])
        a [age=90]
        └── b [age=65]

    Args:
        tree: existing tree
        data: data containing node name and attribute information
        name_col: column of data containing `name` information, if not set, it will take the first column of data
        attribute_cols: column(s) of data containing node attribute information, if not set, it will take all columns
            of data except `path_col`

    Returns:
        Node
    """
    assertions.assert_dataframe_not_empty(data)

    if not name_col:
        name_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(name_col)

    assertions.assert_dataframe_no_duplicate_attribute(
        data, "name", name_col, attribute_cols
    )

    # Get attribute dict, remove null attributes
    name_attrs = (
        data.drop_duplicates(name_col)
        .set_index(name_col)[attribute_cols]
        .to_dict(orient="index")
    )
    name_attrs = {
        k1: {k2: v2 for k2, v2 in v1.items() if not assertions.isnull(v2)}
        for k1, v1 in name_attrs.items()
    }

    return add_dict_to_tree_by_name(tree, name_attrs)


def add_polars_to_tree_by_path(
    tree: T,
    data: pl.DataFrame,
    path_col: str = "",
    attribute_cols: List[str] = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
) -> T:
    """Add nodes and attributes to tree *in-place*, return root of tree. Adds to existing tree from polars DataFrame.

    `path_col` and `attribute_cols` specify columns for node path and attributes to add to existing tree. If columns are
    not specified, `path_col` takes first column and all other columns are `attribute_cols`

    - Only attributes in `attribute_cols` with non-null values will be added to the tree

    Path in path column should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a")
    - Path separator `sep` is for the input `path` and can differ from existing tree

    Path in path column can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/"

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node

    Examples:
        >>> import polars as pl
        >>> from bigtree import add_polars_to_tree_by_path, Node
        >>> root = Node("a")
        >>> path_data = pl.DataFrame([
        ...     ["a", 90],
        ...     ["a/b", 65],
        ...     ["a/c", 60],
        ...     ["a/b/d", 40],
        ...     ["a/b/e", 35],
        ...     ["a/c/f", 38],
        ...     ["a/b/e/g", 10],
        ...     ["a/b/e/h", 6],
        ... ],
        ...     schema=["PATH", "age"]
        ... )
        >>> root = add_polars_to_tree_by_path(root, path_data)
        >>> root.show(attr_list=["age"])
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        │       ├── g [age=10]
        │       └── h [age=6]
        └── c [age=60]
            └── f [age=38]

    Args:
        tree: existing tree
        data: data containing node path and attribute information
        path_col: column of data containing `path_name` information, if not set, it will take the first column of data
        attribute_cols: columns of data containing node attribute information, if not set, it will take all columns of
            data except `path_col`
        sep: path separator for input `path_col`
        duplicate_name_allowed: indicator if nodes with duplicate ``Node`` name is allowed

    Returns:
        Node
    """
    assertions.assert_dataframe_not_empty(data)

    if not path_col:
        path_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(path_col)

    data = data[[path_col] + attribute_cols]
    data = data.with_columns(
        [data[path_col].str.strip_chars_start(sep).str.strip_chars_end(sep)]
    )
    assertions.assert_dataframe_no_duplicate_attribute(
        data, "path", path_col, attribute_cols
    )

    root_node = tree.root
    for row_kwargs in data.to_dicts():
        node_attrs = assertions.filter_attributes(
            row_kwargs, omit_keys=["name", path_col], omit_null_values=True
        )
        add_path_to_tree(
            root_node,
            row_kwargs[path_col],
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    return root_node


def add_polars_to_tree_by_name(
    tree: T,
    data: pl.DataFrame,
    name_col: str = "",
    attribute_cols: List[str] = [],
) -> T:
    """Add attributes to existing tree *in-place*. Adds to existing tree from polars DataFrame.

    `name_col` and `attribute_cols` specify columns for node name and attributes to add to existing tree. If columns are
    not specified, the first column will be taken as name column and all other columns as attributes.

    - Only attributes in `attribute_cols` with non-null values will be added to the tree
    - Input data node names that are not existing node names will be ignored. Note that if multiple nodes have the same
        name, attributes will be added to all nodes sharing same name

    Examples:
        >>> import polars as pl
        >>> from bigtree import add_polars_to_tree_by_name, Node
        >>> root = Node("a")
        >>> b = Node("b", parent=root)
        >>> name_data = pl.DataFrame({
        ...     "NAME": ["a", "b"],
        ...     "age": [90, 65],
        ... })
        >>> root = add_polars_to_tree_by_name(root, name_data)
        >>> root.show(attr_list=["age"])
        a [age=90]
        └── b [age=65]

    Args:
        tree: existing tree
        data: data containing node name and attribute information
        name_col: column of data containing `name` information, if not set, it will take the first column of data
        attribute_cols: column(s) of data containing node attribute information, if not set, it will take all columns
            of data except `path_col`

    Returns:
        Node
    """
    assertions.assert_dataframe_not_empty(data)

    if not name_col:
        name_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(name_col)

    assertions.assert_dataframe_no_duplicate_attribute(
        data, "name", name_col, attribute_cols
    )

    # Get attribute dict, remove null attributes
    name_attrs = dict(
        data.unique(subset=[name_col])
        .select([name_col] + attribute_cols)
        .rows_by_key(key=name_col, named=True)
    )
    name_attrs = {
        k1: {k2: v2 for k2, v2 in v1[0].items() if not assertions.isnull(v2)}
        for k1, v1 in name_attrs.items()
    }

    return add_dict_to_tree_by_name(tree, name_attrs)


def dataframe_to_tree(
    data: pd.DataFrame,
    path_col: str = "",
    attribute_cols: List[str] = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[T] = node.Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from pandas DataFrame using path, return root of tree.

    `path_col` and `attribute_cols` specify columns for node path and attributes to construct tree. If columns are not
    specified, `path_col` takes first column and all other columns are `attribute_cols`.

    - Only attributes in `attribute_cols` with non-null values will be added to the tree

    Path in path column should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a")

    Path in path column can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/"

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node

    Examples:
        >>> import pandas as pd
        >>> from bigtree import dataframe_to_tree
        >>> path_data = pd.DataFrame([
        ...     ["a", 90],
        ...     ["a/b", 65],
        ...     ["a/c", 60],
        ...     ["a/b/d", 40],
        ...     ["a/b/e", 35],
        ...     ["a/c/f", 38],
        ...     ["a/b/e/g", 10],
        ...     ["a/b/e/h", 6],
        ... ],
        ...     columns=["PATH", "age"]
        ... )
        >>> root = dataframe_to_tree(path_data)
        >>> root.show(attr_list=["age"])
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        │       ├── g [age=10]
        │       └── h [age=6]
        └── c [age=60]
            └── f [age=38]

    Args:
        data: data containing path and node attribute information
        path_col: column of data containing `path_name` information, if not set, it will take the first column of data
        attribute_cols: columns of data containing node attribute information, if not set, it will take all columns of
            data except `path_col`
        sep: path separator of input `path_col` and created tree
        duplicate_name_allowed: indicator if nodes with duplicate ``Node`` name is allowed
        node_type: node type of tree to be created

    Returns:
        Node
    """
    assertions.assert_dataframe_not_empty(data)

    if not path_col:
        path_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(path_col)

    data = data[[path_col] + attribute_cols].copy()
    data[path_col] = data[path_col].str.lstrip(sep).str.rstrip(sep)
    assertions.assert_dataframe_no_duplicate_attribute(
        data, "path", path_col, attribute_cols
    )

    root_name = data[path_col].values[0].split(sep)[0]
    root_node_data = data[data[path_col] == root_name]
    if len(root_node_data):
        root_node_kwargs = list(
            root_node_data[attribute_cols].to_dict(orient="index").values()
        )[0]
        root_node_kwargs = assertions.filter_attributes(
            root_node_kwargs, omit_keys=["name", path_col], omit_null_values=True
        )
        root_node = node_type(root_name, **root_node_kwargs)
    else:
        root_node = node_type(root_name)

    for row in data.to_dict(orient="index").values():
        node_attrs = assertions.filter_attributes(
            row, omit_keys=["name", path_col], omit_null_values=True
        )
        add_path_to_tree(
            root_node,
            row[path_col],
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    root_node.sep = sep
    return root_node


def dataframe_to_tree_by_relation(
    data: pd.DataFrame,
    child_col: str = "",
    parent_col: str = "",
    attribute_cols: List[str] = [],
    allow_duplicates: bool = False,
    node_type: Type[T] = node.Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from pandas DataFrame using parent and child names, return root of tree.

    Root node is inferred when parent name is empty, or when name appears in parent column but not in child column.

    Since tree is created from parent-child names, only names of leaf nodes may be repeated. Error will be thrown if
    names of intermediate nodes are repeated as there will be confusion. This error can be ignored by setting
    `allow_duplicates` to be True.

    `child_col` and `parent_col` specify columns for child name and parent name to construct tree. `attribute_cols` specify
    columns for node attribute for child name. If columns are not specified, `child_col` takes first column, `parent_col`
    takes second column, and all other columns are `attribute_cols`.

    - Only attributes in `attribute_cols` with non-null values will be added to the tree

    Examples:
        >>> import pandas as pd
        >>> from bigtree import dataframe_to_tree_by_relation
        >>> relation_data = pd.DataFrame([
        ...     ["a", None, 90],
        ...     ["b", "a", 65],
        ...     ["c", "a", 60],
        ...     ["d", "b", 40],
        ...     ["e", "b", 35],
        ...     ["f", "c", 38],
        ...     ["g", "e", 10],
        ...     ["h", "e", 6],
        ... ],
        ...     columns=["child", "parent", "age"]
        ... )
        >>> root = dataframe_to_tree_by_relation(relation_data)
        >>> root.show(attr_list=["age"])
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        │       ├── g [age=10]
        │       └── h [age=6]
        └── c [age=60]
            └── f [age=38]

    Args:
        data: data containing path and node attribute information
        child_col: column of data containing child name information, if not set, it will take the first column of data
        parent_col: column of data containing parent name information, if not set, it will take the second column of data
        attribute_cols: columns of data containing node attribute information, if not set, it will take all columns of
            data except `child_col` and `parent_col`
        allow_duplicates: allow duplicate intermediate nodes such that child node will be tagged to multiple parent nodes
        node_type: node type of tree to be created

    Returns:
        Node
    """
    assertions.assert_dataframe_not_empty(data)

    if not child_col:
        child_col = data.columns[0]
    if not parent_col:
        parent_col = data.columns[1]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(child_col)
        attribute_cols.remove(parent_col)

    data = data[[child_col, parent_col] + attribute_cols].copy()
    if not allow_duplicates:
        assertions.assert_dataframe_no_duplicate_children(data, child_col, parent_col)

    # Infer root node
    root_names = set(data[data[parent_col].isnull()][child_col])
    root_names.update(set(data[parent_col]) - set(data[child_col]) - {None})
    if len(root_names) != 1:
        raise ValueError(
            f"Unable to determine root node\n"
            f"Possible root nodes: {sorted(list(root_names), key=lambda v: (isinstance(v, str), v))}"
        )
    root_name = list(root_names)[0]

    def _retrieve_attr(_row: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve node attributes from dictionary, remove parent and child column from dictionary.

        Args:
            _row: node attributes

        Returns:
            Attribute dictionary
        """
        node_attrs = assertions.filter_attributes(
            _row, omit_keys=[child_col, parent_col], omit_null_values=True
        )
        node_attrs["name"] = _row[child_col]
        return node_attrs

    def _recursive_add_child(parent_node: T) -> None:
        """Recursive add child to tree, given current node.

        Args:
            parent_node: parent node
        """
        child_rows = data[data[parent_col] == parent_node.node_name]

        for row in child_rows.to_dict(orient="index").values():
            child_node = node_type(**_retrieve_attr(row))
            child_node.parent = parent_node
            _recursive_add_child(child_node)

    # Create root node attributes
    root_row = data[data[child_col] == root_name]
    if len(root_row):
        row = list(root_row.to_dict(orient="index").values())[0]
        root_node = node_type(**_retrieve_attr(row))
    else:
        root_node = node_type(root_name)
    _recursive_add_child(root_node)
    return root_node


def polars_to_tree(
    data: pl.DataFrame,
    path_col: str = "",
    attribute_cols: List[str] = [],
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_type: Type[T] = node.Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from polars DataFrame using path, return root of tree.

    `path_col` and `attribute_cols` specify columns for node path and attributes to construct tree. If columns are not
    specified, `path_col` takes first column and all other columns are `attribute_cols`.

    - Only attributes in `attribute_cols` with non-null values will be added to the tree

    Path in path column should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a")

    Path in path column can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/"

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node

    Examples:
        >>> import polars as pl
        >>> from bigtree import polars_to_tree
        >>> path_data = pl.DataFrame([
        ...     ["a", 90],
        ...     ["a/b", 65],
        ...     ["a/c", 60],
        ...     ["a/b/d", 40],
        ...     ["a/b/e", 35],
        ...     ["a/c/f", 38],
        ...     ["a/b/e/g", 10],
        ...     ["a/b/e/h", 6],
        ... ],
        ...     schema=["PATH", "age"]
        ... )
        >>> root = polars_to_tree(path_data)
        >>> root.show(attr_list=["age"])
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        │       ├── g [age=10]
        │       └── h [age=6]
        └── c [age=60]
            └── f [age=38]

    Args:
        data: data containing path and node attribute information
        path_col: column of data containing `path_name` information, if not set, it will take the first column of data
        attribute_cols: columns of data containing node attribute information, if not set, it will take all columns of
            data except `path_col`
        sep: path separator of input `path_col` and created tree
        duplicate_name_allowed: indicator if nodes with duplicate ``Node`` name is allowed
        node_type: node type of tree to be created

    Returns:
        Node
    """
    assertions.assert_dataframe_not_empty(data)

    if not path_col:
        path_col = data.columns[0]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(path_col)

    data = data[[path_col] + attribute_cols]
    data = data.with_columns(
        [data[path_col].str.strip_chars_start(sep).str.strip_chars_end(sep)]
    )
    assertions.assert_dataframe_no_duplicate_attribute(
        data, "path", path_col, attribute_cols
    )

    root_name = data[path_col][0].split(sep)[0]
    root_node_data = data.filter(data[path_col] == root_name)
    if len(root_node_data):
        root_node_kwargs_list = root_node_data[attribute_cols].to_dicts()
        root_node_kwargs = root_node_kwargs_list[0] if root_node_kwargs_list else {}
        root_node_kwargs = assertions.filter_attributes(
            root_node_kwargs, omit_keys=["name", path_col], omit_null_values=True
        )
        root_node = node_type(root_name, **root_node_kwargs)
    else:
        root_node = node_type(root_name)

    for row in data.to_dicts():
        node_attrs = assertions.filter_attributes(
            row, omit_keys=["name", path_col], omit_null_values=True
        )
        add_path_to_tree(
            root_node,
            row[path_col],
            sep=sep,
            duplicate_name_allowed=duplicate_name_allowed,
            node_attrs=node_attrs,
        )
    root_node.sep = sep
    return root_node


def polars_to_tree_by_relation(
    data: pl.DataFrame,
    child_col: str = "",
    parent_col: str = "",
    attribute_cols: List[str] = [],
    allow_duplicates: bool = False,
    node_type: Type[T] = node.Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from polars DataFrame using parent and child names, return root of tree.

    Root node is inferred when parent name is empty, or when name appears in parent column but not in child column.

    Since tree is created from parent-child names, only names of leaf nodes may be repeated. Error will be thrown if
    names of intermediate nodes are repeated as there will be confusion. This error can be ignored by setting
    `allow_duplicates` to be True.

    `child_col` and `parent_col` specify columns for child name and parent name to construct tree. `attribute_cols` specify
    columns for node attribute for child name. If columns are not specified, `child_col` takes first column, `parent_col`
    takes second column, and all other columns are `attribute_cols`.

    - Only attributes in `attribute_cols` with non-null values will be added to the tree

    Examples:
        >>> import polars as pl
        >>> from bigtree import polars_to_tree_by_relation
        >>> relation_data = pl.DataFrame([
        ...     ["a", None, 90],
        ...     ["b", "a", 65],
        ...     ["c", "a", 60],
        ...     ["d", "b", 40],
        ...     ["e", "b", 35],
        ...     ["f", "c", 38],
        ...     ["g", "e", 10],
        ...     ["h", "e", 6],
        ... ],
        ...     schema=["child", "parent", "age"]
        ... )
        >>> root = polars_to_tree_by_relation(relation_data)
        >>> root.show(attr_list=["age"])
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        │       ├── g [age=10]
        │       └── h [age=6]
        └── c [age=60]
            └── f [age=38]

    Args:
        data: data containing path and node attribute information
        child_col: column of data containing child name information, if not set, it will take the first column of data
        parent_col: column of data containing parent name information, if not set, it will take the second column of data
        attribute_cols: columns of data containing node attribute information, if not set, it will take all columns of
            data except `child_col` and `parent_col`
        allow_duplicates: allow duplicate intermediate nodes such that child node will be tagged to multiple parent nodes
        node_type: node type of tree to be created

    Returns:
        Node
    """
    assertions.assert_dataframe_not_empty(data)

    if not child_col:
        child_col = data.columns[0]
    if not parent_col:
        parent_col = data.columns[1]
    if not len(attribute_cols):
        attribute_cols = list(data.columns)
        attribute_cols.remove(child_col)
        attribute_cols.remove(parent_col)

    data = data[[child_col, parent_col] + attribute_cols]
    if not allow_duplicates:
        assertions.assert_dataframe_no_duplicate_children(data, child_col, parent_col)

    # Infer root node
    root_names = set(data.filter(data[parent_col].is_null())[child_col])
    root_names.update(set(data[parent_col]) - set(data[child_col]) - {None})
    if len(root_names) != 1:
        raise ValueError(
            f"Unable to determine root node\n"
            f"Possible root nodes: {sorted(list(root_names), key=lambda v: (isinstance(v, str), v))}"
        )
    root_name = list(root_names)[0]

    def _retrieve_attr(_row: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve node attributes from dictionary, remove parent and child column from dictionary.

        Args:
            _row: node attributes

        Returns:
            Attribute dictionary
        """
        node_attrs = assertions.filter_attributes(
            _row, omit_keys=[child_col, parent_col], omit_null_values=True
        )
        node_attrs["name"] = _row[child_col]
        return node_attrs

    def _recursive_add_child(parent_node: T) -> None:
        """Recursive add child to tree, given current node.

        Args:
            parent_node: parent node
        """
        child_rows = data.filter(data[parent_col] == parent_node.node_name)

        for row_kwargs in child_rows.to_dicts():
            child_node = node_type(**_retrieve_attr(row_kwargs))
            child_node.parent = parent_node
            _recursive_add_child(child_node)

    # Create root node attributes
    root_row = data.filter(data[child_col] == root_name)
    if len(root_row):
        root_row_kwargs_list = root_row.to_dicts()
        root_row_kwargs = root_row_kwargs_list[0] if root_row_kwargs_list else {}
        root_node = node_type(**_retrieve_attr(root_row_kwargs))
    else:
        root_node = node_type(root_name)
    _recursive_add_child(root_node)
    return root_node

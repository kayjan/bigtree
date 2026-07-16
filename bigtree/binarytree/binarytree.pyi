from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Iterable, Mapping, Sequence, TypeVar

from bigtree.node import node as _node
from bigtree.tree.tree import Tree

if TYPE_CHECKING:
    from bigtree.node import binarynode

    NodeT = TypeVar("NodeT", bound=_node.Node)
    BinaryNodeT = TypeVar("BinaryNodeT", bound=binarynode.BinaryNode)

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

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover
    plt = None

try:
    import rich
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    rich = MagicMock()

class BinaryTree(Tree):

    _plugins: dict[str, Callable[..., Any]] = {}
    construct_kwargs: dict[str, Any] = dict()

    @classmethod
    def from_dataframe(
        cls,
        data: pd.DataFrame,
        path_col: str | None = None,
        attribute_cols: list[str] | None = None,
        sep: str = "/",
        duplicate_name_allowed: bool = True,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    @classmethod
    def from_dataframe_relation(
        cls,
        data: pd.DataFrame,
        child_col: str | None = None,
        parent_col: str | None = None,
        attribute_cols: list[str] | None = None,
        allow_duplicates: bool = False,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    @classmethod
    def from_polars(
        cls,
        data: pl.DataFrame,
        path_col: str | None = None,
        attribute_cols: list[str] | None = None,
        sep: str = "/",
        duplicate_name_allowed: bool = True,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    @classmethod
    def from_polars_relation(
        cls,
        data: pl.DataFrame,
        path_col: str | None = None,
        attribute_cols: list[str] | None = None,
        sep: str = "/",
        duplicate_name_allowed: bool = True,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    @classmethod
    def from_dict(
        cls,
        path_attrs: Mapping[str, Any],
        sep: str = "/",
        duplicate_name_allowed: bool = True,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    @classmethod
    def from_nested_dict(
        cls,
        node_attrs: Mapping[str, Any],
        name_key: str = "name",
        child_key: str = "children",
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    @classmethod
    def from_nested_dict_key(
        cls,
        node_attrs: Mapping[str, Mapping[str, Any]],
        child_key: str | None = "children",
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    @classmethod
    def from_list(
        cls,
        paths: list[str],
        sep: str = "/",
        duplicate_name_allowed: bool = True,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    @classmethod
    def from_list_relation(
        cls,
        relations: list[tuple[str, str]],
        allow_duplicates: bool = False,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    @classmethod
    def from_str(
        cls,
        tree_string: str,
        tree_prefix_list: Iterable[str] = (),
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    @classmethod
    def from_newick(
        cls,
        tree_string: str,
        length_attr: str = "length",
        attr_prefix: str = "&&NHX:",
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    @classmethod
    def from_rich(
        cls, rich_tree: rich.tree.Tree, node_format_attr: str = "style"
    ) -> BinaryTree: ...

    # Plugins
    @classmethod
    def from_heapq_list(
        cls,
        heapq_list: Sequence[int],
        node_type: type[BinaryNodeT] = binarynode.BinaryNode,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    def inorder_iter(
        self,
        filter_condition: Callable[[BinaryNodeT], bool] | None = None,
        max_depth: int = 0,
    ) -> Iterable[BinaryNodeT]: ...

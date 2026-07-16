from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Iterable,
    Literal,
    Mapping,
    TypeVar,
)

from bigtree.node import node as _node
from bigtree.utils import constants

if TYPE_CHECKING:
    from bigtree.node import basenode, binarynode, dagnode

    BaseNodeT = TypeVar("BaseNodeT", bound=basenode.BaseNode)
    BinaryNodeT = TypeVar("BinaryNodeT", bound=binarynode.BinaryNode)
    DAGNodeT = TypeVar("DAGNodeT", bound=dagnode.DAGNode)
    NodeT = TypeVar("NodeT", bound=_node.Node)
    Tr = TypeVar("Tr", bound=Tree)

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

try:
    import pydot
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pydot = MagicMock()

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    Image = ImageDraw = ImageFont = MagicMock()

try:
    import matplotlib as mpl
    from matplotlib.colors import Normalize
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    mpl = MagicMock()
    Normalize = MagicMock()

try:
    import pyvis
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pyvis = MagicMock()

class Tree:

    _plugins: dict[str, Callable[..., Any]] = {}
    construct_kwargs: dict[str, Any] = dict()

    @classmethod
    def register_plugins(
        cls,
        mapping: dict[str, Callable[..., Any]],
        method: Literal["default", "class", "helper", "diff"] = "default",
    ) -> None: ...
    @property
    def diameter(self) -> int: ...
    @property
    def depth(self) -> int: ...
    def plot(self, *args: Any, **kwargs: Any) -> plt.Figure: ...
    def copy(self: Tr) -> Tr: ...
    # Plugins
    @classmethod
    def from_dataframe(
        cls,
        data: pd.DataFrame,
        path_col: str | None = None,
        attribute_cols: list[str] | None = None,
        sep: str = "/",
        duplicate_name_allowed: bool = True,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> Tree: ...
    @classmethod
    def from_dataframe_relation(
        cls,
        data: pd.DataFrame,
        child_col: str | None = None,
        parent_col: str | None = None,
        attribute_cols: list[str] | None = None,
        allow_duplicates: bool = False,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> Tree: ...
    @classmethod
    def from_polars(
        cls,
        data: pl.DataFrame,
        path_col: str | None = None,
        attribute_cols: list[str] | None = None,
        sep: str = "/",
        duplicate_name_allowed: bool = True,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> Tree: ...
    @classmethod
    def from_polars_relation(
        cls,
        data: pl.DataFrame,
        path_col: str | None = None,
        attribute_cols: list[str] | None = None,
        sep: str = "/",
        duplicate_name_allowed: bool = True,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> Tree: ...
    @classmethod
    def from_dict(
        cls,
        path_attrs: Mapping[str, Any],
        sep: str = "/",
        duplicate_name_allowed: bool = True,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> Tree: ...
    @classmethod
    def from_nested_dict(
        cls,
        node_attrs: Mapping[str, Any],
        name_key: str = "name",
        child_key: str = "children",
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> Tree: ...
    @classmethod
    def from_nested_dict_key(
        cls,
        node_attrs: Mapping[str, Mapping[str, Any]],
        child_key: str | None = "children",
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> Tree: ...
    @classmethod
    def from_list(
        cls,
        paths: list[str],
        sep: str = "/",
        duplicate_name_allowed: bool = True,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> Tree: ...
    @classmethod
    def from_list_relation(
        cls,
        relations: list[tuple[str, str]],
        allow_duplicates: bool = False,
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> Tree: ...
    @classmethod
    def from_str(
        cls,
        tree_string: str,
        tree_prefix_list: Iterable[str] = (),
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> Tree: ...
    @classmethod
    def from_newick(
        cls,
        tree_string: str,
        length_attr: str = "length",
        attr_prefix: str = "&&NHX:",
        node_type: type[NodeT] = _node.Node,  # type: ignore[assignment]
    ) -> Tree: ...
    @classmethod
    def from_rich(
        cls, rich_tree: rich.tree.Tree, node_format_attr: str = "style"
    ) -> Tree: ...
    def add_dataframe_by_path(
        self,
        data: pd.DataFrame,
        path_col: str | None = None,
        attribute_cols: list[str] | None = None,
        sep: str = "/",
        duplicate_name_allowed: bool = True,
    ) -> type[_node.Node]: ...
    def add_dataframe_by_name(
        self,
        data: pd.DataFrame,
        name_col: str | None = None,
        attribute_cols: list[str] | None = None,
    ) -> type[_node.Node]: ...
    def add_polars_by_path(
        self,
        data: pl.DataFrame,
        path_col: str | None = None,
        attribute_cols: list[str] | None = None,
        sep: str = "/",
        duplicate_name_allowed: bool = True,
    ) -> type[_node.Node]: ...
    def add_polars_by_name(
        self,
        data: pl.DataFrame,
        name_col: str | None = None,
        attribute_cols: list[str] | None = None,
    ) -> type[_node.Node]: ...
    def add_dict_by_path(
        self,
        data: pl.DataFrame,
        name_col: str | None = None,
        attribute_cols: list[str] | None = None,
    ) -> type[_node.Node]: ...
    def add_dict_by_name(
        self,
        path_attrs: Mapping[str, Mapping[str, Any]],
        sep: str = "/",
        duplicate_name_allowed: bool = True,
    ) -> type[_node.Node]: ...
    def show(
        self,
        alias: str = "node_name",
        node_name_or_path: str | None = None,
        max_depth: int = 0,
        all_attrs: bool = False,
        attr_list: Iterable[str] | None = None,
        attr_format: str = "{k}={v}",
        attr_sep: str = ", ",
        attr_omit_null: bool = False,
        attr_bracket: tuple[str, str] = ("[", "]"),
        style: str | Iterable[str] | constants.BasePrintStyle = "const",
        **kwargs: Any,
    ) -> None: ...
    def hshow(
        self,
        alias: str = "node_name",
        node_name_or_path: str | None = None,
        max_depth: int = 0,
        intermediate_node_name: bool = True,
        spacing: int = 0,
        style: str | Iterable[str] | constants.BaseHPrintStyle = "const",
        border_style: str | Iterable[str] | constants.BorderStyle | None = None,
        strip: bool = True,
        **kwargs: Any,
    ) -> None: ...
    def vshow(
        self,
        alias: str = "node_name",
        node_name_or_path: str | None = None,
        max_depth: int = 0,
        intermediate_node_name: bool = True,
        spacing: int = 2,
        style: str | Iterable[str] | constants.BaseVPrintStyle = "const",
        border_style: str | Iterable[str] | constants.BorderStyle | None = "const",
        strip: bool = False,
        **kwargs: Any,
    ) -> None: ...
    def ishow(
        self,
        **kwargs: Any,
    ) -> None: ...
    def yield_tree(
        self,
        node_name_or_path: str | None = None,
        max_depth: int = 0,
        style: str | Iterable[str] | constants.BasePrintStyle = "const",
    ) -> Iterable[tuple[str, str, NodeT]]: ...
    def hyield(
        self,
        alias: str = "node_name",
        node_name_or_path: str | None = None,
        max_depth: int = 0,
        intermediate_node_name: bool = True,
        spacing: int = 0,
        style: str | Iterable[str] | constants.BaseHPrintStyle = "const",
        border_style: str | Iterable[str] | constants.BorderStyle | None = None,
        strip: bool = True,
    ) -> list[str]: ...
    def vyield(
        self,
        alias: str = "node_name",
        node_name_or_path: str | None = None,
        max_depth: int = 0,
        intermediate_node_name: bool = True,
        spacing: int = 2,
        style: str | Iterable[str] | constants.BaseVPrintStyle = "const",
        border_style: str | Iterable[str] | constants.BorderStyle | None = "const",
        strip: bool = False,
    ) -> list[str]: ...
    def to_dataframe(
        self,
        path_col: str | None = "path",
        name_col: str | None = "name",
        parent_col: str | None = None,
        attr_dict: dict[str, str] | None = None,
        all_attrs: bool = False,
        max_depth: int = 0,
        skip_depth: int = 0,
        leaf_only: bool = False,
    ) -> pd.DataFrame: ...
    def to_polars(
        self,
        path_col: str | None = "path",
        name_col: str | None = "name",
        parent_col: str | None = None,
        attr_dict: dict[str, str] | None = None,
        all_attrs: bool = False,
        max_depth: int = 0,
        skip_depth: int = 0,
        leaf_only: bool = False,
    ) -> pl.DataFrame: ...
    def to_dict(
        self,
        name_key: str | None = "name",
        parent_key: str | None = None,
        attr_dict: dict[str, str] | None = None,
        all_attrs: bool = False,
        max_depth: int = 0,
        skip_depth: int = 0,
        leaf_only: bool = False,
    ) -> dict[str, Any]: ...
    def to_nested_dict(
        self,
        name_key: str = "name",
        child_key: str = "children",
        attr_dict: dict[str, str] | None = None,
        all_attrs: bool = False,
        max_depth: int = 0,
    ) -> dict[str, Any]: ...
    def to_nested_dict_key(
        self,
        child_key: str | None = "children",
        attr_dict: dict[str, str] | None = None,
        all_attrs: bool = False,
        max_depth: int = 0,
    ) -> dict[str, Any]: ...
    def to_html(
        self,
        all_attrs: bool = False,
        attr_list: Iterable[str] | None = None,
        node_colour: str = "#f8f9fa",
        node_width: int = 160,
        border_colour: str = "#dee2e6",
        border_radius: int = 12,
        border_width: float | int | str = 1,
        edge_colour: str = "#ccc",
        edge_width: float | int = 1.5,
        font_colour: str = "#333",
        font_title_size: int = 13,
        font_size: int = 11,
        height: int = 500,
        width: int = 900,
    ) -> str: ...
    def to_newick(
        self,
        intermediate_node_name: bool = True,
        length_attr: str | None = None,
        length_sep: str | constants.NewickCharacter = constants.NewickCharacter.SEP,
        attr_list: Iterable[str] | None = None,
        attr_prefix: str = "&&NHX:",
        attr_sep: str | constants.NewickCharacter = constants.NewickCharacter.SEP,
    ) -> str: ...
    def to_dot(
        self,
        directed: bool = True,
        rankdir: str = "TB",
        bg_colour: str | None = None,
        node_colour: str | None = None,
        node_shape: str | None = None,
        edge_colour: str | None = None,
        node_attr: Callable[[NodeT], dict[str, Any]] | str | None = None,
        edge_attr: Callable[[NodeT], dict[str, Any]] | str | None = None,
    ) -> pydot.Dot: ...
    def to_pillow_graph(
        self,
        node_content: str = "{node_name}",
        *,
        margin: dict[str, int] | None = None,
        height_buffer: int | float = 20,
        width_buffer: int | float = 10,
        font_family: str | None = None,
        font_size: int = 12,
        font_colour: tuple[int, int, int] | str = "black",
        text_align: str = "center",
        bg_colour: tuple[int, int, int] | str = "white",
        rect_margin: dict[str, int] | None = None,
        rect_fill: tuple[int, int, int] | str | mpl.colors.Colormap = "white",
        rect_cmap_attr: str | None = None,
        rect_outline: tuple[int, int, int] | str = "black",
        rect_width: int = 1,
        **kwargs: Any,
    ) -> Image.Image: ...
    def to_pillow(
        self,
        width: int = 0,
        height: int = 0,
        start_pos: tuple[int, int] = (10, 10),
        font_family: str | None = None,
        font_size: int = 12,
        font_colour: tuple[int, int, int] | str = "black",
        bg_colour: tuple[int, int, int] | str = "white",
        **kwargs: Any,
    ) -> Image.Image: ...
    def to_mermaid(
        self,
        title: str | None = None,
        theme: str | None = None,
        rankdir: str = "TB",
        line_shape: str = "basis",
        node_colour: str | None = None,
        node_border_colour: str | None = None,
        node_border_width: float = 1,
        node_shape: str = "rounded_edge",
        node_shape_attr: Callable[[NodeT], str] | str | None = None,
        edge_arrow: str = "normal",
        edge_arrow_attr: Callable[[NodeT], str] | str | None = None,
        edge_label: str | None = None,
        node_attr: Callable[[NodeT], str] | str | None = None,
        **kwargs: Any,
    ) -> str: ...
    def to_vis(
        self,
        alias: str = "node_name",
        plot_kwargs: dict[str, Any] | None = None,
        custom_node_kwargs: dict[str, str] | None = None,
        node_kwargs: dict[str, Any] | None = None,
        custom_edge_kwargs: dict[str, str] | None = None,
        edge_kwargs: dict[str, Any] | None = None,
        network_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> pyvis.network.Network: ...
    def preorder_iter(
        self,
        filter_condition: Callable[[NodeT], bool] | None = None,
        stop_condition: Callable[[NodeT], bool] | None = None,
        max_depth: int = 0,
    ) -> Iterable[NodeT]: ...
    def postorder_iter(
        self,
        filter_condition: Callable[[BaseNodeT], bool] | None = None,
        stop_condition: Callable[[BaseNodeT], bool] | None = None,
        max_depth: int = 0,
    ) -> Iterable[BaseNodeT]: ...
    def levelorder_iter(
        self,
        filter_condition: Callable[[BaseNodeT], bool] | None = None,
        stop_condition: Callable[[BaseNodeT], bool] | None = None,
        max_depth: int = 0,
    ) -> Iterable[BaseNodeT]: ...
    def levelordergroup_iter(
        self,
        filter_condition: Callable[[BaseNodeT], bool] | None = None,
        stop_condition: Callable[[BaseNodeT], bool] | None = None,
        max_depth: int = 0,
    ) -> Iterable[Iterable[BaseNodeT]]: ...
    def zigzag_iter(
        self,
        filter_condition: Callable[[BaseNodeT], bool] | None = None,
        stop_condition: Callable[[BaseNodeT], bool] | None = None,
        max_depth: int = 0,
    ) -> Iterable[BaseNodeT]: ...
    def zigzaggroup_iter(
        self,
        filter_condition: Callable[[BaseNodeT], bool] | None = None,
        stop_condition: Callable[[BaseNodeT], bool] | None = None,
        max_depth: int = 0,
    ) -> Iterable[Iterable[BaseNodeT]]: ...
    def shift_nodes(
        self,
        tree: NodeT,
        from_paths: Collection[str],
        to_paths: Collection[str | None],
        sep: str = "/",
        skippable: bool = False,
        overriding: bool = False,
        merge_attribute: bool = False,
        merge_children: bool = False,
        merge_leaves: bool = False,
        delete_children: bool = False,
        with_full_path: bool = False,
    ) -> None: ...
    def copy_nodes(
        self,
        from_paths: Collection[str],
        to_paths: Collection[str | None],
        sep: str = "/",
        skippable: bool = False,
        overriding: bool = False,
        merge_attribute: bool = False,
        merge_children: bool = False,
        merge_leaves: bool = False,
        delete_children: bool = False,
        with_full_path: bool = False,
    ) -> None: ...
    def shift_and_replace_nodes(
        self,
        from_paths: Collection[str],
        to_paths: Collection[str],
        sep: str = "/",
        skippable: bool = False,
        delete_children: bool = False,
        with_full_path: bool = False,
    ) -> None: ...
    def query(
        self, tree_node: BaseNodeT, query: str, debug: bool = False
    ) -> list[BaseNodeT]: ...
    def findall(
        self,
        condition: Callable[[BaseNodeT], bool],
        max_depth: int = 0,
        min_count: int = 0,
        max_count: int = 0,
    ) -> tuple[BaseNodeT, ...]: ...
    def find(
        self, condition: Callable[[BaseNodeT], bool], max_depth: int = 0
    ) -> BaseNodeT | None: ...
    def find_name(
        self, name: str, max_depth: int = 0, regex: bool = False
    ) -> NodeT | None: ...
    def find_names(
        self, name: str, max_depth: int = 0, regex: bool = False
    ) -> Iterable[NodeT]: ...
    def find_relative_path(self, path_name: str) -> NodeT | None: ...
    def find_relative_paths(
        self,
        path_name: str,
        min_count: int = 0,
        max_count: int = 0,
    ) -> tuple[NodeT, ...]: ...
    def find_full_path(self, path_name: str) -> NodeT | None: ...
    def find_path(self, path_name: str) -> Iterable[NodeT]: ...
    def find_paths(self, path_name: str) -> Iterable[NodeT]: ...
    def find_attr(
        self, attr_name: str, attr_value: Any, max_depth: int = 0
    ) -> basenode.BaseNode | None: ...
    def find_attrs(
        self, attr_name: str, attr_value: Any, max_depth: int = 0
    ) -> Iterable[basenode.BaseNode]: ...
    def find_children(
        self,
        condition: Callable[[BaseNodeT | DAGNodeT], bool],
        min_count: int = 0,
        max_count: int = 0,
    ) -> tuple[BaseNodeT | DAGNodeT, ...]: ...
    def find_child(
        self,
        condition: Callable[[BaseNodeT | DAGNodeT], bool],
    ) -> BaseNodeT | DAGNodeT | None: ...
    def find_child_by_name(self, name: str) -> NodeT | DAGNodeT | None: ...
    def clone(self, node_type: type[BaseNodeT]) -> Tree: ...
    def subtree(
        self,
        node_name_or_path: str | None = None,
        max_depth: int = 0,
    ) -> Tree: ...
    def prune(
        self,
        prune_path: Iterable[str] | str | None = None,
        exact: bool = False,
        sep: str = "/",
        max_depth: int = 0,
    ) -> Tree: ...
    def diff_dataframe(
        self,
        other_tree: _node.Node,
        only_diff: bool = True,
        detail: bool = False,
        aggregate: bool = False,
        attr_list: list[str] | None = None,
        fallback_sep: str = "/",
        name_col: str = "name",
        path_col: str = "path",
        parent_col: str = "parent",
        indicator_col: str = "Exists",
        old_suffix: str = "_old",
        new_suffix: str = "_new",
        suffix_col: str = "suffix",
    ) -> pd.DataFrame: ...
    def diff(
        self,
        other_tree: Tr,
        only_diff: bool = True,
        detail: bool = False,
        aggregate: bool = False,
        attr_list: Iterable[str] | None = None,
        fallback_sep: str = "/",
    ) -> Tr | None: ...

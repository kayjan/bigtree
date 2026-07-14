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

if TYPE_CHECKING:
    from bigtree.node import dagnode

    T = TypeVar("T", bound=dagnode.DAGNode)

from bigtree.node import dagnode

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pd = MagicMock()

try:
    import pydot
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pydot = MagicMock()

class DAG:

    _plugins: dict[str, Callable[..., Any]] = {}
    construct_kwargs: dict[str, Any] = dict()

    @classmethod
    def register_plugins(
        cls,
        mapping: dict[str, Callable[..., Any]],
        method: Literal["default", "class"] = "default",
    ) -> None: ...
    @classmethod
    def from_dataframe(
        cls,
        data: pd.DataFrame,
        child_col: str | None = None,
        parent_col: str | None = None,
        attribute_cols: list[str] | None = None,
        node_type: type[T] = dagnode.DAGNode,  # type: ignore[assignment]
    ) -> T: ...
    @classmethod
    def from_dict(
        cls,
        relation_attrs: Mapping[str, Any],
        parent_key: str = "parents",
        node_type: type[T] = dagnode.DAGNode,  # type: ignore[assignment]
    ) -> T: ...
    @classmethod
    def from_list(
        cls,
        relations: Collection[tuple[str, str]],
        node_type: type[T] = dagnode.DAGNode,  # type: ignore[assignment]
    ) -> T: ...
    def to_dataframe(
        self,
        name_col: str = "name",
        parent_col: str = "parent",
        attr_dict: Mapping[str, str] | None = None,
        all_attrs: bool = False,
    ) -> pd.DataFrame: ...
    def to_dict(
        self,
        parent_key: str = "parents",
        attr_dict: Mapping[str, str] | None = None,
        all_attrs: bool = False,
    ) -> dict[str, Any]: ...
    def to_list(self) -> list[tuple[str, str]]: ...
    def to_dot(
        self,
        rankdir: str = "TB",
        bg_colour: str | None = None,
        node_colour: str | None = None,
        node_shape: str | None = None,
        edge_colour: str | None = None,
        node_attr: str | None = None,
        edge_attr: str | None = None,
    ) -> pydot.Dot: ...
    def iterate(self) -> Iterable[tuple[T, T]]: ...

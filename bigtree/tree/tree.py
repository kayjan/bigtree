from typing import Any, Mapping

from bigtree.node import node
from bigtree.tree import construct, export
from bigtree.utils import exceptions

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
    def __init__(self, root: node.Node):
        self.root = root

    @classmethod
    def from_dataframe(cls, data: pd.DataFrame, **kwargs: Any) -> "Tree":
        root_node = construct.dataframe_to_tree(data, **kwargs)
        return cls(root_node)

    @classmethod
    def from_dataframe_relation(cls, data: pd.DataFrame, **kwargs: Any) -> "Tree":
        root_node = construct.dataframe_to_tree_by_relation(data, **kwargs)
        return cls(root_node)

    @classmethod
    def from_polars(cls, data: pl.DataFrame, **kwargs: Any) -> "Tree":
        root_node = construct.polars_to_tree(data, **kwargs)
        return cls(root_node)

    @classmethod
    def from_polars_relation(cls, data: pl.DataFrame, **kwargs: Any) -> "Tree":
        root_node = construct.polars_to_tree_by_relation(data, **kwargs)
        return cls(root_node)

    @classmethod
    def from_dict(cls, path_attrs: Mapping[str, Any], **kwargs: Any) -> "Tree":
        root_node = construct.dict_to_tree(path_attrs, **kwargs)
        return cls(root_node)

    @classmethod
    def from_nested_dict(cls, node_attrs: Mapping[str, Any], **kwargs: Any) -> "Tree":
        root_node = construct.nested_dict_to_tree(node_attrs, **kwargs)
        return cls(root_node)

    @classmethod
    def from_nested_dict_key(
        cls, node_attrs: Mapping[str, Any], **kwargs: Any
    ) -> "Tree":
        root_node = construct.nested_dict_key_to_tree(node_attrs, **kwargs)
        return cls(root_node)

    @classmethod
    def from_list(cls, paths: list[str], **kwargs: Any) -> "Tree":
        root_node = construct.list_to_tree(paths, **kwargs)
        return cls(root_node)

    @classmethod
    def from_list_relation(
        cls, relations: list[tuple[str, str]], **kwargs: Any
    ) -> "Tree":
        root_node = construct.list_to_tree_by_relation(relations, **kwargs)
        return cls(root_node)

    @classmethod
    def from_str(cls, tree_string: str, **kwargs: Any) -> "Tree":
        root_node = construct.str_to_tree(tree_string, **kwargs)
        return cls(root_node)

    @classmethod
    def from_newick(cls, tree_string: str, **kwargs: Any) -> "Tree":
        root_node = construct.newick_to_tree(tree_string, **kwargs)
        return cls(root_node)

    def to_dataframe(self, **kwargs: Any) -> pd.DataFrame:
        return export.tree_to_dataframe(self.root, **kwargs)

    def to_polars(self, **kwargs: Any) -> pl.DataFrame:
        return export.tree_to_polars(self.root, **kwargs)

    def to_dict(self, **kwargs: Any) -> dict[str, Any]:
        return export.tree_to_dict(self.root, **kwargs)

    def to_nested_dict(self, **kwargs: Any) -> dict[str, Any]:
        return export.tree_to_nested_dict(self.root, **kwargs)

    def to_nested_dict_key(self, **kwargs: Any) -> dict[str, Any]:
        return export.tree_to_nested_dict_key(self.root, **kwargs)

    @exceptions.optional_dependencies_image("pydot")
    def to_dot(self, **kwargs: Any) -> pydot.Dot:
        return export.tree_to_dot(self.root, **kwargs)

    @exceptions.optional_dependencies_image("Pillow")
    def to_pillow_graph(self, **kwargs: Any) -> Image.Image:
        return export.tree_to_pillow_graph(self.root, **kwargs)

    @exceptions.optional_dependencies_image("Pillow")
    def to_pillow(self, **kwargs: Any) -> Image.Image:
        return export.tree_to_pillow(self.root, **kwargs)

    def to_mermaid(self, **kwargs: Any) -> str:
        return export.tree_to_mermaid(self.root, **kwargs)

    @exceptions.optional_dependencies_vis
    def to_vis(self, **kwargs: Any) -> pyvis.network.Network:
        return export.tree_to_vis(self.root, **kwargs)

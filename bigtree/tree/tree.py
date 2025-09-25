from typing import Any, Mapping, TypeVar

from bigtree.node import basenode, binarynode, node
from bigtree.tree import construct, export, helper
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

BaseNodeT = TypeVar("BaseNodeT", bound=basenode.BaseNode)
BinaryNodeT = TypeVar("BinaryNodeT", bound=binarynode.BinaryNode)
NodeT = TypeVar("NodeT", bound=node.Node)


class Tree:
    """
    Tree wraps around Node class to provide an intuitive, Pythonic API for
        - Quick construction of tree with dataframe, dictionary, list, or string
        - Quick export to dataframe, dictionary, list, string, or images

    Do refer to the various modules respectively on the keyword parameters.
    """

    construct_kwargs: dict[str, Any] = dict()

    def __init__(self, root: node.Node):
        self.root = root

    def show(self, **kwargs: Any) -> None:
        self.root.show(**kwargs)

    def hshow(self, **kwargs: Any) -> None:
        self.root.hshow(**kwargs)

    def vshow(self, **kwargs: Any) -> None:
        self.root.vshow(**kwargs)

    @property
    def diameter(self) -> int:
        """Get diameter of tree, the length of longest path between any two nodes.

        Returns:
            Diameter of tree
        """
        return self.root.diameter

    @property
    def depth(self) -> int:
        """Get depth of tree, indexing starts from 1.

        Returns:
            Depth of tree
        """
        return self.root.max_depth

    # Construct methods
    @classmethod
    def from_dataframe(cls, data: pd.DataFrame, **kwargs: Any) -> "Tree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.dataframe_to_tree(data, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_dataframe_relation(cls, data: pd.DataFrame, **kwargs: Any) -> "Tree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.dataframe_to_tree_by_relation(data, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_polars(cls, data: pl.DataFrame, **kwargs: Any) -> "Tree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.polars_to_tree(data, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_polars_relation(cls, data: pl.DataFrame, **kwargs: Any) -> "Tree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.polars_to_tree_by_relation(data, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_dict(cls, path_attrs: Mapping[str, Any], **kwargs: Any) -> "Tree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.dict_to_tree(path_attrs, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_nested_dict(cls, node_attrs: Mapping[str, Any], **kwargs: Any) -> "Tree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.nested_dict_to_tree(node_attrs, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_nested_dict_key(
        cls, node_attrs: Mapping[str, Any], **kwargs: Any
    ) -> "Tree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.nested_dict_key_to_tree(node_attrs, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_list(cls, paths: list[str], **kwargs: Any) -> "Tree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.list_to_tree(paths, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_list_relation(
        cls, relations: list[tuple[str, str]], **kwargs: Any
    ) -> "Tree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.list_to_tree_by_relation(relations, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_str(cls, tree_string: str, **kwargs: Any) -> "Tree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.str_to_tree(tree_string, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_newick(cls, tree_string: str, **kwargs: Any) -> "Tree":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.newick_to_tree(tree_string, **construct_kwargs)
        return cls(root_node)

    # Export methods
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

    def to_newick(self, **kwargs: Any) -> str:
        return export.tree_to_newick(self.root, **kwargs)

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

    # Helper methods
    def clone(self, node_type: type[BaseNodeT]) -> BaseNodeT:
        return helper.clone_tree(self.root, node_type)

    def prune(self, **kwargs: Any) -> BinaryNodeT | NodeT:
        return helper.prune_tree(self.root, **kwargs)  # type: ignore

    def diff(self, other_tree: node.Node, **kwargs: Any) -> node.Node:
        return helper.get_tree_diff(self.root, other_tree, **kwargs)

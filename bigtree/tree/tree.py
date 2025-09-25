from __future__ import annotations

import copy
from typing import Any, Iterable, Mapping, TypeVar

from bigtree.node import basenode, binarynode, node
from bigtree.tree import construct, export, helper, query, search
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
    Tree wraps around Node class to provide a quick, intuitive, Pythonic API for
        - Construction with dataframe, dictionary, list, or string
        - Export to dataframe, dictionary, list, string, or images
        - Helper methods for cloning, pruning, getting tree diff
        - Query and Search methods to find one or more Nodes

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

    # Append methods
    def add_dataframe_by_path(
        self, data: pd.DataFrame, *args: Any, **kwargs: Any
    ) -> None:
        construct.add_dataframe_to_tree_by_path(self.root, data, *args, **kwargs)

    def add_dataframe_by_name(
        self, data: pd.DataFrame, *args: Any, **kwargs: Any
    ) -> None:
        construct.add_dataframe_to_tree_by_name(self.root, data, *args, **kwargs)

    def add_polars_by_path(self, data: pl.DataFrame, *args: Any, **kwargs: Any) -> None:
        construct.add_polars_to_tree_by_path(self.root, data, *args, **kwargs)

    def add_polars_by_name(self, data: pl.DataFrame, *args: Any, **kwargs: Any) -> None:
        construct.add_polars_to_tree_by_name(self.root, data, *args, **kwargs)

    def add_dict_by_path(
        self, path_attrs: Mapping[str, Mapping[str, Any]], *args: Any, **kwargs: Any
    ) -> None:
        construct.add_dict_to_tree_by_path(self.root, path_attrs, *args, **kwargs)

    def add_dict_by_name(self, name_attrs: Mapping[str, Mapping[str, Any]]) -> None:
        construct.add_dict_to_tree_by_name(self.root, name_attrs)

    # Export methods
    def to_dataframe(self, *args: Any, **kwargs: Any) -> pd.DataFrame:
        return export.tree_to_dataframe(self.root, *args, **kwargs)

    def to_polars(self, *args: Any, **kwargs: Any) -> pl.DataFrame:
        return export.tree_to_polars(self.root, *args, **kwargs)

    def to_dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return export.tree_to_dict(self.root, *args, **kwargs)

    def to_nested_dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return export.tree_to_nested_dict(self.root, *args, **kwargs)

    def to_nested_dict_key(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return export.tree_to_nested_dict_key(self.root, *args, **kwargs)

    def to_newick(self, *args: Any, **kwargs: Any) -> str:
        return export.tree_to_newick(self.root, *args, **kwargs)

    @exceptions.optional_dependencies_image("pydot")
    def to_dot(self, *args: Any, **kwargs: Any) -> pydot.Dot:
        return export.tree_to_dot(self.root, *args, **kwargs)

    @exceptions.optional_dependencies_image("Pillow")
    def to_pillow_graph(self, *args: Any, **kwargs: Any) -> Image.Image:
        return export.tree_to_pillow_graph(self.root, *args, **kwargs)

    @exceptions.optional_dependencies_image("Pillow")
    def to_pillow(self, *args: Any, **kwargs: Any) -> Image.Image:
        return export.tree_to_pillow(self.root, *args, **kwargs)

    def to_mermaid(self, *args: Any, **kwargs: Any) -> str:
        return export.tree_to_mermaid(self.root, *args, **kwargs)

    @exceptions.optional_dependencies_vis
    def to_vis(self, *args: Any, **kwargs: Any) -> pyvis.network.Network:
        return export.tree_to_vis(self.root, *args, **kwargs)

    # Helper methods
    def clone(self, node_type: type[BaseNodeT]) -> BaseNodeT:
        return helper.clone_tree(self.root, node_type)

    def prune(self, *args: Any, **kwargs: Any) -> BinaryNodeT | NodeT:
        return helper.prune_tree(self.root, *args, **kwargs)  # type: ignore

    def diff_dataframe(
        self, other_tree: node.Node, *args: Any, **kwargs: Any
    ) -> pd.DataFrame:
        return helper.get_tree_diff_dataframe(
            self.root, other_tree.root, *args, **kwargs
        )

    def diff(self, other_tree: node.Node, *args: Any, **kwargs: Any) -> node.Node:
        return helper.get_tree_diff(self.root, other_tree.root, *args, **kwargs)

    # Query methods
    def query(
        self, query_str: str, *args: Any, **kwargs: Any
    ) -> list[basenode.BaseNode]:
        return query.query_tree(self.root, query_str, *args, **kwargs)

    # Search methods
    def findall(self, *args: Any, **kwargs: Any) -> tuple[basenode.BaseNode, ...]:
        return search.findall(self.root, *args, **kwargs)

    def find(self, *args: Any, **kwargs: Any) -> basenode.BaseNode:
        return search.find(self.root, *args, **kwargs)

    def find_name(self, *args: Any, **kwargs: Any) -> node.Node:
        return search.find_name(self.root, *args, **kwargs)

    def find_names(self, *args: Any, **kwargs: Any) -> Iterable[node.Node]:
        return search.find_names(self.root, *args, **kwargs)

    def find_full_path(self, *args: Any, **kwargs: Any) -> node.Node:
        return search.find_full_path(self.root, *args, **kwargs)

    def find_path(self, *args: Any, **kwargs: Any) -> node.Node:
        return search.find_path(self.root, *args, **kwargs)

    def find_paths(self, *args: Any, **kwargs: Any) -> Iterable[node.Node]:
        return search.find_paths(self.root, *args, **kwargs)

    def find_attr(self, *args: Any, **kwargs: Any) -> basenode.BaseNode:
        return search.find_attr(self.root, *args, **kwargs)

    def find_attrs(self, *args: Any, **kwargs: Any) -> Iterable[basenode.BaseNode]:
        return search.find_attrs(self.root, *args, **kwargs)

    def find_children(self, *args: Any, **kwargs: Any) -> tuple[node.Node, ...]:
        return search.find_children(self.root, *args, **kwargs)

    def find_child(self, *args: Any, **kwargs: Any) -> node.Node:
        return search.find_child(self.root, *args, **kwargs)

    def find_child_by_name(self, *args: Any, **kwargs: Any) -> node.Node:
        return search.find_child_by_name(self.root, *args, **kwargs)

    def __getitem__(self, child_name: str) -> "Tree":
        """Get child by name identifier.

        Args:
            child_name: name of child node

        Returns:
            Child node as tree
        """
        return type(self)(self.root[child_name])

    def __delitem__(self, child_name: str) -> None:
        """Delete child by name identifier, will not throw error if child does not exist.

        Args:
            child_name: name of child node
        """
        from bigtree.tree.search import find_child_by_name

        child = find_child_by_name(self.root, child_name)
        if child:
            child.parent = None

    def copy(self: T) -> T:
        """Deep copy self; clone BaseNode.

        Examples:
            >>> from bigtree.node.node import Node
            >>> a = Node('a')
            >>> a_copy = a.copy()

        Returns:
            Cloned copy of node
        """
        return copy.deepcopy(self)

    def __copy__(self: T) -> T:
        """Shallow copy self.

        Returns:
            Shallow copy of node
        """
        obj: T = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __repr__(self) -> str:
        """Print format of Tree.

        Returns:
            Print format of Tree
        """
        class_name = self.__class__.__name__
        node_dict = self.root.describe(exclude_prefix="_", exclude_attributes=["name"])
        node_description = ", ".join([f"{k}={v}" for k, v in node_dict])
        return f"{class_name}({self.root.path_name}, {node_description})"


T = TypeVar("T", bound=Tree)

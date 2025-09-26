from __future__ import annotations

import copy
from typing import Any, Iterable, Mapping, TypeVar

from bigtree.node import basenode, binarynode, node
from bigtree.tree import construct, export, helper, query, search
from bigtree.utils import exceptions, iterators

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

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover
    plt = None


BaseNodeT = TypeVar("BaseNodeT", bound=basenode.BaseNode)
BinaryNodeT = TypeVar("BinaryNodeT", bound=binarynode.BinaryNode)
NodeT = TypeVar("NodeT", bound=node.Node)


class Tree:
    """
    Tree wraps around Node class to provide a quick, intuitive, Pythonic API for

        * Construction with dataframe, dictionary, list, or string
        * Export to dataframe, dictionary, list, string, or images
        * Helper methods for cloning, pruning, getting tree diff
        * Query and Search methods to find one or more Nodes
        * Plot methods

    Do refer to the various modules respectively on the keyword parameters.
    """

    construct_kwargs: dict[str, Any] = dict()

    def __init__(self, root: node.Node):
        self.node = root

    def show(self, **kwargs: Any) -> None:
        self.node.show(**kwargs)

    def hshow(self, **kwargs: Any) -> None:
        self.node.hshow(**kwargs)

    def vshow(self, **kwargs: Any) -> None:
        self.node.vshow(**kwargs)

    @property
    def diameter(self) -> int:
        """Get diameter of tree, the length of longest path between any two nodes.

        Returns:
            Diameter of tree
        """
        return self.node.diameter

    @property
    def depth(self) -> int:
        """Get depth of tree, indexing starts from 1.

        Returns:
            Depth of tree
        """
        return self.node.max_depth

    # Construct methods
    @classmethod
    def from_dataframe(cls, data: pd.DataFrame, *args: Any, **kwargs: Any) -> "Tree":
        """See `dataframe_to_tree` for full details.

        Accepts the same arguments as `dataframe_to_tree`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.dataframe_to_tree(data, *args, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_dataframe_relation(
        cls, data: pd.DataFrame, *args: Any, **kwargs: Any
    ) -> "Tree":
        """See `dataframe_to_tree_by_relation` for full details.

        Accepts the same arguments as `dataframe_to_tree_by_relation`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.dataframe_to_tree_by_relation(
            data, *args, **construct_kwargs
        )
        return cls(root_node)

    @classmethod
    def from_polars(cls, data: pl.DataFrame, *args: Any, **kwargs: Any) -> "Tree":
        """See `polars_to_tree` for full details.

        Accepts the same arguments as `polars_to_tree`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.polars_to_tree(data, *args, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_polars_relation(
        cls, data: pl.DataFrame, *args: Any, **kwargs: Any
    ) -> "Tree":
        """See `polars_to_tree_by_relation` for full details.

        Accepts the same arguments as `polars_to_tree_by_relation`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.polars_to_tree_by_relation(
            data, *args, **construct_kwargs
        )
        return cls(root_node)

    @classmethod
    def from_dict(
        cls, path_attrs: Mapping[str, Any], *args: Any, **kwargs: Any
    ) -> "Tree":
        """See `dict_to_tree` for full details.

        Accepts the same arguments as `dict_to_tree`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.dict_to_tree(path_attrs, *args, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_nested_dict(
        cls, node_attrs: Mapping[str, Any], *args: Any, **kwargs: Any
    ) -> "Tree":
        """See `nested_dict_to_tree` for full details.

        Accepts the same arguments as `nested_dict_to_tree`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.nested_dict_to_tree(node_attrs, *args, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_nested_dict_key(
        cls, node_attrs: Mapping[str, Any], *args: Any, **kwargs: Any
    ) -> "Tree":
        """See `nested_dict_key_to_tree` for full details.

        Accepts the same arguments as `nested_dict_key_to_tree`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.nested_dict_key_to_tree(
            node_attrs, *args, **construct_kwargs
        )
        return cls(root_node)

    @classmethod
    def from_list(cls, paths: list[str], *args: Any, **kwargs: Any) -> "Tree":
        """See `list_to_tree` for full details.

        Accepts the same arguments as `list_to_tree`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.list_to_tree(paths, *args, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_list_relation(
        cls, relations: list[tuple[str, str]], *args: Any, **kwargs: Any
    ) -> "Tree":
        """See `list_to_tree_by_relation` for full details.

        Accepts the same arguments as `list_to_tree_by_relation`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.list_to_tree_by_relation(
            relations, *args, **construct_kwargs
        )
        return cls(root_node)

    @classmethod
    def from_str(cls, tree_string: str, *args: Any, **kwargs: Any) -> "Tree":
        """See `str_to_tree` for full details.

        Accepts the same arguments as `str_to_tree`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.str_to_tree(tree_string, *args, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_newick(cls, tree_string: str, *args: Any, **kwargs: Any) -> "Tree":
        """See `newick_to_tree` for full details.

        Accepts the same arguments as `newick_to_tree`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.newick_to_tree(tree_string, *args, **construct_kwargs)
        return cls(root_node)

    # Append methods
    def add_dataframe_by_path(
        self, data: pd.DataFrame, *args: Any, **kwargs: Any
    ) -> None:
        """See `add_dataframe_to_tree_by_path` for full details.

        Accepts the same arguments as `add_dataframe_to_tree_by_path`.
        """
        construct.add_dataframe_to_tree_by_path(self.node, data, *args, **kwargs)

    def add_dataframe_by_name(
        self, data: pd.DataFrame, *args: Any, **kwargs: Any
    ) -> None:
        """See `add_dataframe_to_tree_by_name` for full details.

        Accepts the same arguments as `add_dataframe_to_tree_by_name`.
        """
        construct.add_dataframe_to_tree_by_name(self.node, data, *args, **kwargs)

    def add_polars_by_path(self, data: pl.DataFrame, *args: Any, **kwargs: Any) -> None:
        """See `add_polars_to_tree_by_path` for full details.

        Accepts the same arguments as `add_polars_to_tree_by_path`.
        """
        construct.add_polars_to_tree_by_path(self.node, data, *args, **kwargs)

    def add_polars_by_name(self, data: pl.DataFrame, *args: Any, **kwargs: Any) -> None:
        """See `add_polars_to_tree_by_name` for full details.

        Accepts the same arguments as `add_polars_to_tree_by_name`.
        """
        construct.add_polars_to_tree_by_name(self.node, data, *args, **kwargs)

    def add_dict_by_path(
        self, path_attrs: Mapping[str, Mapping[str, Any]], *args: Any, **kwargs: Any
    ) -> None:
        """See `add_dict_to_tree_by_path` for full details.

        Accepts the same arguments as `add_dict_to_tree_by_path`.
        """
        construct.add_dict_to_tree_by_path(self.node, path_attrs, *args, **kwargs)

    def add_dict_by_name(self, name_attrs: Mapping[str, Mapping[str, Any]]) -> None:
        """See `add_dict_to_tree_by_name` for full details.

        Accepts the same arguments as `add_dict_to_tree_by_name`.
        """
        construct.add_dict_to_tree_by_name(self.node, name_attrs)

    # Export methods
    def to_dataframe(self, *args: Any, **kwargs: Any) -> pd.DataFrame:
        """See `tree_to_dataframe` for full details.

        Accepts the same arguments as `tree_to_dataframe`.
        """
        return export.tree_to_dataframe(self.node, *args, **kwargs)

    def to_polars(self, *args: Any, **kwargs: Any) -> pl.DataFrame:
        """See `tree_to_polars` for full details.

        Accepts the same arguments as `tree_to_polars`.
        """
        return export.tree_to_polars(self.node, *args, **kwargs)

    def to_dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """See `tree_to_dict` for full details.

        Accepts the same arguments as `tree_to_dict`.
        """
        return export.tree_to_dict(self.node, *args, **kwargs)

    def to_nested_dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """See `tree_to_nested_dict` for full details.

        Accepts the same arguments as `tree_to_nested_dict`.
        """
        return export.tree_to_nested_dict(self.node, *args, **kwargs)

    def to_nested_dict_key(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """See `tree_to_nested_dict_key` for full details.

        Accepts the same arguments as `tree_to_nested_dict_key`.
        """
        return export.tree_to_nested_dict_key(self.node, *args, **kwargs)

    def to_newick(self, *args: Any, **kwargs: Any) -> str:
        """See `tree_to_newick` for full details.

        Accepts the same arguments as `tree_to_newick`.
        """
        return export.tree_to_newick(self.node, *args, **kwargs)

    @exceptions.optional_dependencies_image("pydot")
    def to_dot(self, *args: Any, **kwargs: Any) -> pydot.Dot:
        """See `tree_to_dot` for full details.

        Accepts the same arguments as `tree_to_dot`.
        """
        return export.tree_to_dot(self.node, *args, **kwargs)

    @exceptions.optional_dependencies_image("Pillow")
    def to_pillow_graph(self, *args: Any, **kwargs: Any) -> Image.Image:
        """See `tree_to_pillow_graph` for full details.

        Accepts the same arguments as `tree_to_pillow_graph`.
        """
        return export.tree_to_pillow_graph(self.node, *args, **kwargs)

    @exceptions.optional_dependencies_image("Pillow")
    def to_pillow(self, *args: Any, **kwargs: Any) -> Image.Image:
        """See `tree_to_pillow` for full details.

        Accepts the same arguments as `tree_to_pillow`.
        """
        return export.tree_to_pillow(self.node, *args, **kwargs)

    def to_mermaid(self, *args: Any, **kwargs: Any) -> str:
        """See `tree_to_mermaid` for full details.

        Accepts the same arguments as `tree_to_mermaid`.
        """
        return export.tree_to_mermaid(self.node, *args, **kwargs)

    @exceptions.optional_dependencies_vis
    def to_vis(self, *args: Any, **kwargs: Any) -> pyvis.network.Network:
        """See `tree_to_vis` for full details.

        Accepts the same arguments as `tree_to_vis`.
        """
        return export.tree_to_vis(self.node, *args, **kwargs)

    # Helper methods
    def clone(self, node_type: type[BaseNodeT]) -> "Tree":
        """See `clone_tree` for full details.

        Accepts the same arguments as `clone_tree`.
        """
        return type(self)(helper.clone_tree(self.node, node_type))  # type: ignore

    def prune(self, *args: Any, **kwargs: Any) -> "Tree":
        """See `prune_tree` for full details.

        Accepts the same arguments as `prune_tree`.
        """
        return type(self)(helper.prune_tree(self.node, *args, **kwargs))

    def diff_dataframe(self, other_tree: T, *args: Any, **kwargs: Any) -> pd.DataFrame:
        """See `get_tree_diff_dataframe` for full details.

        Accepts the same arguments as `get_tree_diff_dataframe`.
        """
        return helper.get_tree_diff_dataframe(
            self.node, other_tree.node, *args, **kwargs
        )

    def diff(self, other_tree: T, *args: Any, **kwargs: Any) -> node.Node:
        """See `get_tree_diff` for full details.

        Accepts the same arguments as `get_tree_diff`.
        """
        return helper.get_tree_diff(self.node, other_tree.node, *args, **kwargs)

    # Query methods
    def query(
        self, query_str: str, *args: Any, **kwargs: Any
    ) -> list[basenode.BaseNode]:
        """See `query_tree` for full details.

        Accepts the same arguments as `query_tree`.
        """
        return query.query_tree(self.node, query_str, *args, **kwargs)

    # Search methods
    def findall(self, *args: Any, **kwargs: Any) -> tuple[basenode.BaseNode, ...]:
        """See `findall` for full details.

        Accepts the same arguments as `findall`.
        """
        return search.findall(self.node, *args, **kwargs)

    def find(self, *args: Any, **kwargs: Any) -> basenode.BaseNode:
        """See `find` for full details.

        Accepts the same arguments as `find`.
        """
        return search.find(self.node, *args, **kwargs)

    def find_name(self, *args: Any, **kwargs: Any) -> node.Node:
        """See `find_name` for full details.

        Accepts the same arguments as `find_name`.
        """
        return search.find_name(self.node, *args, **kwargs)

    def find_names(self, *args: Any, **kwargs: Any) -> Iterable[node.Node]:
        """See `find_names` for full details.

        Accepts the same arguments as `find_names`.
        """
        return search.find_names(self.node, *args, **kwargs)

    def find_relative_path(self, *args: Any, **kwargs: Any) -> node.Node:
        """See `find_relative_path` for full details.

        Accepts the same arguments as `find_relative_path`.
        """
        return search.find_relative_path(self.node, *args, **kwargs)

    def find_relative_paths(self, *args: Any, **kwargs: Any) -> Iterable[node.Node]:
        """See `find_relative_paths` for full details.

        Accepts the same arguments as `find_relative_paths`.
        """
        return search.find_relative_paths(self.node, *args, **kwargs)

    def find_full_path(self, *args: Any, **kwargs: Any) -> node.Node:
        """See `find_full_path` for full details.

        Accepts the same arguments as `find_full_path`.
        """
        return search.find_full_path(self.node, *args, **kwargs)

    def find_path(self, *args: Any, **kwargs: Any) -> node.Node:
        """See `find_path` for full details.

        Accepts the same arguments as `find_path`.
        """
        return search.find_path(self.node, *args, **kwargs)

    def find_paths(self, *args: Any, **kwargs: Any) -> Iterable[node.Node]:
        """See `find_paths` for full details.

        Accepts the same arguments as `find_paths`.
        """
        return search.find_paths(self.node, *args, **kwargs)

    def find_attr(self, *args: Any, **kwargs: Any) -> basenode.BaseNode:
        """See `find_attr` for full details.

        Accepts the same arguments as `find_attr`.
        """
        return search.find_attr(self.node, *args, **kwargs)

    def find_attrs(self, *args: Any, **kwargs: Any) -> Iterable[basenode.BaseNode]:
        """See `find_attrs` for full details.

        Accepts the same arguments as `find_attrs`.
        """
        return search.find_attrs(self.node, *args, **kwargs)

    def find_children(self, *args: Any, **kwargs: Any) -> tuple[node.Node, ...]:
        """See `find_children` for full details.

        Accepts the same arguments as `find_children`.
        """
        return search.find_children(self.node, *args, **kwargs)

    def find_child(self, *args: Any, **kwargs: Any) -> node.Node:
        """See `find_child` for full details.

        Accepts the same arguments as `find_child`.
        """
        return search.find_child(self.node, *args, **kwargs)

    def find_child_by_name(self, *args: Any, **kwargs: Any) -> node.Node:
        """See `find_child_by_name` for full details.

        Accepts the same arguments as `find_child_by_name`.
        """
        return search.find_child_by_name(self.node, *args, **kwargs)

    # Iterator methods
    def preorder_iter(self, *args: Any, **kwargs: Any) -> Iterable[node.Node]:
        """See `preorder_iter` for full details.

        Accepts the same arguments as `preorder_iter`.
        """
        return iterators.preorder_iter(self.node, *args, **kwargs)

    def postorder_iter(self, *args: Any, **kwargs: Any) -> Iterable[basenode.BaseNode]:
        """See `postorder_iter` for full details.

        Accepts the same arguments as `postorder_iter`.
        """
        return iterators.postorder_iter(self.node, *args, **kwargs)

    def levelorder_iter(self, *args: Any, **kwargs: Any) -> Iterable[basenode.BaseNode]:
        """See `levelorder_iter` for full details.

        Accepts the same arguments as `levelorder_iter`.
        """
        return iterators.levelorder_iter(self.node, *args, **kwargs)

    def levelordergroup_iter(
        self, *args: Any, **kwargs: Any
    ) -> Iterable[Iterable[basenode.BaseNode]]:
        """See `levelordergroup_iter` for full details.

        Accepts the same arguments as `levelordergroup_iter`.
        """
        return iterators.levelordergroup_iter(self.node, *args, **kwargs)

    def zigzag_iter(self, *args: Any, **kwargs: Any) -> Iterable[basenode.BaseNode]:
        """See `zigzag_iter` for full details.

        Accepts the same arguments as `zigzag_iter`.
        """
        return iterators.zigzag_iter(self.node, *args, **kwargs)

    def zigzaggroup_iter(
        self, *args: Any, **kwargs: Any
    ) -> Iterable[Iterable[basenode.BaseNode]]:
        """See `zigzaggroup_iter` for full details.

        Accepts the same arguments as `zigzaggroup_iter`.
        """
        return iterators.zigzaggroup_iter(self.node, *args, **kwargs)

    # Plot methods
    def plot(self, *args: Any, **kwargs: Any) -> plt.Figure:
        """Plot tree in line form. Accepts args and kwargs for matplotlib.pyplot.plot() function.

        Examples:
            >>> from bigtree import Tree
            >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
            >>> tree = Tree.from_list(path_list)
            >>> tree.plot("-ok")
            <Figure size 1280x960 with 1 Axes>
        """
        return self.node.plot(*args, **kwargs)

    # Magic methods
    def __getitem__(self, child_name: str) -> "Tree":
        """Get child by name identifier.

        Args:
            child_name: name of child node

        Returns:
            Child node as tree
        """
        return type(self)(self.node[child_name])

    def __delitem__(self, child_name: str) -> None:
        """Delete child by name identifier, will not throw error if child does not exist.

        Args:
            child_name: name of child node
        """
        from bigtree.tree.search import find_child_by_name

        child = find_child_by_name(self.node, child_name)
        if child:
            child.parent = None

    def copy(self: T) -> T:
        """Deep copy self; clone Tree.

        Returns:
            Cloned copy of Tree
        """
        return copy.deepcopy(self)

    def __copy__(self: T) -> T:
        """Shallow copy self.

        Returns:
            Shallow copy of Tree
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
        node_dict = self.node.describe(exclude_prefix="_", exclude_attributes=["name"])
        node_description = ", ".join([f"{k}={v}" for k, v in node_dict])
        return f"{class_name}({self.node.path_name}, {node_description})"


T = TypeVar("T", bound=Tree)

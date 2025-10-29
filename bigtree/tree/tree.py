from __future__ import annotations

import copy
import functools
from typing import Any, Callable, Literal, TypeVar

from bigtree.node import basenode, binarynode, node
from bigtree.tree import construct, export, helper, query, search
from bigtree.utils import iterators

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

    _plugins: dict[str, Callable[..., Any]] = {}
    construct_kwargs: dict[str, Any] = dict()

    def __init__(self, root: node.Node):
        self.node = root

    @classmethod
    def register_plugin(
        cls,
        name: str,
        func: Callable[..., Any],
        method: Literal["default", "class", "helper", "diff"],
    ) -> None:
        base_func = func.func if isinstance(func, functools.partial) else func

        if method == "default":

            def wrapper(self, *args, **kwargs):  # type: ignore
                return func(self.node, *args, **kwargs)

        elif method == "class":

            def wrapper(cls, *args, **kwargs):  # type: ignore
                construct_kwargs = {**cls.construct_kwargs, **kwargs}
                root_node = func(*args, **construct_kwargs)
                return cls(root_node)

        elif method == "helper":

            def wrapper(self, *args, **kwargs):  # type: ignore
                return type(self)(func(self.node, *args, **kwargs))

        else:

            def wrapper(self, other_tree: T, *args, **kwargs):  # type: ignore
                return func(self.node, other_tree.node, *args, **kwargs)

        functools.update_wrapper(wrapper, base_func)
        wrapper.__name__ = name
        if method == "class":
            setattr(cls, name, classmethod(wrapper))  # type: ignore
        else:
            setattr(cls, name, wrapper)
        cls._plugins[name] = func

    @classmethod
    def register_plugins(
        cls,
        mapping: dict[str, Callable[..., Any]],
        method: Literal["default", "class", "helper", "diff"] = "default",
    ) -> None:
        for name, func in mapping.items():
            cls.register_plugin(name, func, method)

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


Tree.register_plugins(
    {
        # Construct methods
        "from_dataframe": construct.dataframe_to_tree,
        "from_dataframe_relation": construct.dataframe_to_tree_by_relation,
        "from_polars": construct.polars_to_tree,
        "from_polars_relation": construct.polars_to_tree_by_relation,
        "from_dict": construct.dict_to_tree,
        "from_nested_dict": construct.nested_dict_to_tree,
        "from_nested_dict_key": construct.nested_dict_key_to_tree,
        "from_list": construct.list_to_tree,
        "from_list_relation": construct.list_to_tree_by_relation,
        "from_str": construct.str_to_tree,
        "from_newick": construct.newick_to_tree,
    },
    method="class",
)

Tree.register_plugins(
    {
        # Append methods
        "add_dataframe_by_path": construct.add_dataframe_to_tree_by_path,
        "add_dataframe_by_name": construct.add_dataframe_to_tree_by_name,
        "add_polars_by_path": construct.add_polars_to_tree_by_path,
        "add_polars_by_name": construct.add_polars_to_tree_by_name,
        "add_dict_by_path": construct.add_dict_to_tree_by_path,
        "add_dict_by_name": construct.add_dict_to_tree_by_name,
        # Export methods
        "show": export.print_tree,
        "hshow": export.hprint_tree,
        "vshow": export.vprint_tree,
        "yield": export.yield_tree,
        "hyield": export.hyield_tree,
        "vyield": export.vyield_tree,
        "to_dataframe": export.tree_to_dataframe,
        "to_polars": export.tree_to_polars,
        "to_dict": export.tree_to_dict,
        "to_nested_dict": export.tree_to_nested_dict,
        "to_nested_dict_key": export.tree_to_nested_dict_key,
        "to_newick": export.tree_to_newick,
        "to_dot": export.tree_to_dot,
        "to_pillow_graph": export.tree_to_pillow_graph,
        "to_pillow": export.tree_to_pillow,
        "to_mermaid": export.tree_to_mermaid,
        "to_vis": export.tree_to_vis,
        # Query methods
        "query": query.query_tree,
        # Search methods
        "findall": search.findall,
        "find": search.find,
        "find_name": search.find_name,
        "find_names": search.find_names,
        "find_relative_path": search.find_relative_path,
        "find_relative_paths": search.find_relative_paths,
        "find_full_path": search.find_full_path,
        "find_path": search.find_path,
        "find_paths": search.find_paths,
        "find_attr": search.find_attr,
        "find_attrs": search.find_attrs,
        "find_children": search.find_children,
        "find_child": search.find_child,
        "find_child_by_name": search.find_child_by_name,
        # Iterator methods
        "preorder_iter": iterators.preorder_iter,
        "postorder_iter": iterators.postorder_iter,
        "levelorder_iter": iterators.levelorder_iter,
        "levelordergroup_iter": iterators.levelordergroup_iter,
        "zigzag_iter": iterators.zigzag_iter,
        "zigzaggroup_iter": iterators.zigzaggroup_iter,
    }
)
Tree.register_plugins(
    {
        # Helper methods
        "clone": helper.clone_tree,
        "prune": helper.prune_tree,
    },
    method="helper",
)
Tree.register_plugins(
    {
        # Helper methods
        "diff_dataframe": helper.get_tree_diff_dataframe,
        "diff": helper.get_tree_diff,
    },
    method="diff",
)

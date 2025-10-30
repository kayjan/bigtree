from __future__ import annotations

import copy
import functools
from typing import Any, Callable, Literal, TypeVar

from bigtree._plugins import register_tree_plugins
from bigtree.node import basenode, binarynode, node

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

register_tree_plugins()

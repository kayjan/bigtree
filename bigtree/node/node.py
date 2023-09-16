from __future__ import annotations

from collections import Counter
from typing import Any, List, TypeVar

from bigtree.node.basenode import BaseNode
from bigtree.utils.exceptions import TreeError


class Node(BaseNode):
    """
    Node is an extension of BaseNode, and is able to extend to any Python class.
    Nodes can have attributes if they are initialized from `Node`, *dictionary*, or *pandas DataFrame*.

    Nodes can be linked to each other with `parent` and `children` setter methods.

    >>> from bigtree import Node
    >>> a = Node("a")
    >>> b = Node("b")
    >>> c = Node("c")
    >>> d = Node("d")
    >>> b.parent = a
    >>> b.children = [c, d]

    Directly passing `parent` argument.

    >>> from bigtree import Node
    >>> a = Node("a")
    >>> b = Node("b", parent=a)
    >>> c = Node("c", parent=b)
    >>> d = Node("d", parent=b)

    Directly passing `children` argument.

    >>> from bigtree import Node
    >>> d = Node("d")
    >>> c = Node("c")
    >>> b = Node("b", children=[c, d])
    >>> a = Node("a", children=[b])

    **Node Creation**

    Node can be created by instantiating a `Node` class or by using a *dictionary*.
    If node is created with dictionary, all keys of dictionary will be stored as class attributes.

    >>> from bigtree import Node
    >>> a = Node.from_dict({"name": "a", "age": 90})

    **Node Attributes**

    These are node attributes that have getter and/or setter methods.

    Get and set `Node` configuration

    1. ``sep``: Get/set separator for path name

    Get `Node` configuration

    1. ``node_name``: Get node name, without accessing `name` directly
    2. ``path_name``: Get path name from root, separated by `sep`

    **Node Methods**

    These are methods available to be performed on `Node`.

    `Node` methods

    1. ``show()``: Print tree to console

    ----

    """

    def __init__(self, name: str = "", sep: str = "/", **kwargs: Any):
        self.name = name
        self._sep = sep
        super().__init__(**kwargs)
        if not self.node_name:
            raise TreeError("Node must have a `name` attribute")

    @property
    def sep(self) -> str:
        """Get separator, gets from root node

        Returns:
            (str)
        """
        if self.parent is None:
            return self._sep
        return self.parent.sep

    @sep.setter
    def sep(self, value: str) -> None:
        """Set separator, affects root node

        Args:
            value (str): separator to replace default separator
        """
        self.root._sep = value

    @property
    def node_name(self) -> str:
        """Get node name

        Returns:
            (str)
        """
        return self.name

    @property
    def path_name(self) -> str:
        """Get path name, separated by self.sep

        Returns:
            (str)
        """
        ancestors = [self] + list(self.ancestors)
        sep = ancestors[-1].sep
        return sep + sep.join([str(node.name) for node in reversed(ancestors)])

    def __pre_assign_children(self: T, new_children: List[T]) -> None:
        """Custom method to check before attaching children
        Can be overridden with `_Node__pre_assign_children()`

        Args:
            new_children (List[Self]): new children to be added
        """
        pass

    def __post_assign_children(self: T, new_children: List[T]) -> None:
        """Custom method to check after attaching children
        Can be overridden with `_Node__post_assign_children()`

        Args:
            new_children (List[Self]): new children to be added
        """
        pass

    def __pre_assign_parent(self: T, new_parent: T) -> None:
        """Custom method to check before attaching parent
        Can be overridden with `_Node__pre_assign_parent()`

        Args:
            new_parent (Self): new parent to be added
        """
        pass

    def __post_assign_parent(self: T, new_parent: T) -> None:
        """Custom method to check after attaching parent
        Can be overridden with `_Node__post_assign_parent()`

        Args:
            new_parent (Self): new parent to be added
        """
        pass

    def _BaseNode__pre_assign_parent(self: T, new_parent: T) -> None:
        """Do not allow duplicate nodes of same path

        Args:
            new_parent (Self): new parent to be added
        """
        self.__pre_assign_parent(new_parent)
        if new_parent is not None:
            if any(
                child.node_name == self.node_name and child is not self
                for child in new_parent.children
            ):
                raise TreeError(
                    f"Duplicate node with same path\n"
                    f"There exist a node with same path {new_parent.path_name}{new_parent.sep}{self.node_name}"
                )

    def _BaseNode__post_assign_parent(self: T, new_parent: T) -> None:
        """No rules

        Args:
            new_parent (Self): new parent to be added
        """
        self.__post_assign_parent(new_parent)

    def _BaseNode__pre_assign_children(self: T, new_children: List[T]) -> None:
        """Do not allow duplicate nodes of same path

        Args:
            new_children (List[Self]): new children to be added
        """
        self.__pre_assign_children(new_children)
        children_names = [node.node_name for node in new_children]
        duplicate_names = [
            item[0] for item in Counter(children_names).items() if item[1] > 1
        ]
        if len(duplicate_names):
            duplicate_names_str = " and ".join(
                [f"{self.path_name}{self.sep}{name}" for name in duplicate_names]
            )
            raise TreeError(
                f"Duplicate node with same path\n"
                f"Attempting to add nodes with same path {duplicate_names_str}"
            )

    def _BaseNode__post_assign_children(self: T, new_children: List[T]) -> None:
        """No rules

        Args:
            new_children (List[Self]): new children to be added
        """
        self.__post_assign_children(new_children)

    def show(self, **kwargs: Any) -> None:
        """Print tree to console, takes in same keyword arguments as `print_tree` function"""
        from bigtree.tree.export import print_tree

        print_tree(self, **kwargs)

    def __repr__(self) -> str:
        """Print format of Node

        Returns:
            (str)
        """
        class_name = self.__class__.__name__
        node_dict = self.describe(exclude_prefix="_", exclude_attributes=["name"])
        node_description = ", ".join([f"{k}={v}" for k, v in node_dict])
        return f"{class_name}({self.path_name}, {node_description})"


T = TypeVar("T", bound=Node)

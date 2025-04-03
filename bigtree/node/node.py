from __future__ import annotations

from collections import Counter
from typing import Any, List, TypeVar

from bigtree.node import basenode
from bigtree.utils import exceptions


class Node(basenode.BaseNode):
    """
    Node is an extension of BaseNode, and is able to extend to any Python class. Nodes can have attributes if they are
    initialized from `Node`, *dictionary*, or *pandas DataFrame*.

    !!! note
        Node names cannot contain separator symbol! This will not throw error, but you might run into issues
        when performing certain functions such as export-then-import of tree.

    Nodes can be linked to each other with `parent` and `children` setter methods.

    Examples:
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

    Node can be created by instantiating a `Node` class or by using a *dictionary*. If node is created with dictionary,
    all keys of dictionary will be stored as class attributes.

        >>> from bigtree import Node
        >>> a = Node.from_dict({"name": "a", "age": 90})

    **Node Attributes**

    These are node attributes that have getter and/or setter methods.

    Get and set `Node` configuration

    1. ``sep``: Get/set separator for path name

    Get `Node` configuration

    1. ``node_name``: Get node name, without accessing `name` directly. This is the preferred way to access node name
        as `node_name` is immutable, whereas `name` is mutable
    2. ``path_name``: Get path name from root, separated by `sep`

    **Node Methods**

    These are methods available to be performed on `Node`.

    `Node` methods

    1. ``show()``: Print tree to console
    2. ``hshow()``: Print tree in horizontal orientation to console
    3. ``vshow()``: Print tree in vertical orientation to console

    ----

    """

    def __init__(self, name: str, sep: str = "/", **kwargs: Any):
        self.name = name
        self._sep = sep
        super().__init__(**kwargs)
        if not self.node_name:
            raise exceptions.TreeError("Node must have a `name` attribute")

    @property
    def sep(self) -> str:
        """Get separator, gets from root node.

        Returns:
            Seperator
        """
        if self.parent is None:
            return self._sep
        return self.parent.sep

    @sep.setter
    def sep(self, value: str) -> None:
        """Set separator, affects root node.

        Args:
            value: separator to replace default separator
        """
        self.root._sep = value

    @property
    def node_name(self) -> str:
        """Get node name.

        Returns:
            Node name
        """
        return self.name

    @property
    def path_name(self) -> str:
        """Get path name, separated by self.sep.

        Returns:
            Path name
        """
        ancestors = [self] + list(self.ancestors)
        sep = ancestors[-1].sep
        return sep + sep.join([str(node.node_name) for node in reversed(ancestors)])

    def __pre_assign_children(self: T, new_children: List[T]) -> None:
        """Custom method to check before attaching children
        Can be overridden with `_Node__pre_assign_children()`

        Args:
            new_children (List[Self]): new children to be added
        """
        pass

    def __post_assign_children(self: T, new_children: List[T]) -> None:
        """Custom method to check after attaching children. Can be overridden with `_Node__post_assign_children()`.

        Args:
            new_children: new children to be added
        """
        pass

    def __pre_assign_parent(self: T, new_parent: T) -> None:
        """Custom method to check before attaching parent. Can be overridden with `_Node__pre_assign_parent()`.

        Args:
            new_parent: new parent to be added
        """
        pass

    def __post_assign_parent(self: T, new_parent: T) -> None:
        """Custom method to check after attaching parent. Can be overridden with `_Node__post_assign_parent()`.

        Args:
            new_parent: new parent to be added
        """
        pass

    def _BaseNode__pre_assign_parent(self: T, new_parent: T) -> None:
        """Do not allow duplicate nodes of same path.

        Args:
            new_parent: new parent to be added
        """
        self.__pre_assign_parent(new_parent)
        if new_parent is not None:
            if any(
                child.node_name == self.node_name and child is not self
                for child in new_parent.children
            ):
                raise exceptions.TreeError(
                    f"Duplicate node with same path\n"
                    f"There exist a node with same path {new_parent.path_name}{new_parent.sep}{self.node_name}"
                )

    def _BaseNode__post_assign_parent(self: T, new_parent: T) -> None:
        """No rules.

        Args:
            new_parent: new parent to be added
        """
        self.__post_assign_parent(new_parent)

    def _BaseNode__pre_assign_children(self: T, new_children: List[T]) -> None:
        """Do not allow duplicate nodes of same path.

        Args:
            new_children: new children to be added
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
            raise exceptions.TreeError(
                f"Duplicate node with same path\n"
                f"Attempting to add nodes with same path {duplicate_names_str}"
            )

    def _BaseNode__post_assign_children(self: T, new_children: List[T]) -> None:
        """No rules.

        Args:
            new_children: new children to be added
        """
        self.__post_assign_children(new_children)

    def show(self, **kwargs: Any) -> None:
        """Print tree to console, takes in same keyword arguments as `print_tree` function."""
        from bigtree.tree.export import print_tree

        print_tree(self, **kwargs)

    def hshow(self, **kwargs: Any) -> None:
        """Print tree in horizontal orientation to console, takes in same keyword arguments as `hprint_tree` function."""
        from bigtree.tree.export import hprint_tree

        hprint_tree(self, **kwargs)

    def vshow(self, **kwargs: Any) -> None:
        """Print tree in vertical orientation to console, takes in same keyword arguments as `vprint_tree` function."""
        from bigtree.tree.export import vprint_tree

        vprint_tree(self, **kwargs)

    def __getitem__(self, child_name: str) -> "Node":
        """Get child by name identifier.

        Args:
            child_name: name of child node

        Returns:
            Child node
        """
        from bigtree.tree.search import find_child_by_name

        return find_child_by_name(self, child_name)

    def __delitem__(self, child_name: str) -> None:
        """Delete child by name identifier, will not throw error if child does not exist.

        Args:
            child_name: name of child node
        """
        from bigtree.tree.search import find_child_by_name

        child = find_child_by_name(self, child_name)
        if child:
            child.parent = None

    def __repr__(self) -> str:
        """Print format of Node.

        Returns:
            Print format of Node
        """
        class_name = self.__class__.__name__
        node_dict = self.describe(exclude_prefix="_", exclude_attributes=["name"])
        node_description = ", ".join([f"{k}={v}" for k, v in node_dict])
        return f"{class_name}({self.path_name}, {node_description})"


T = TypeVar("T", bound=Node)

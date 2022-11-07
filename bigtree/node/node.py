from collections import Counter
from typing import List

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

    ------------

    """

    def __init__(self, name: str = "", **kwargs):
        self.name = name
        self._sep: str = "/"
        super().__init__(**kwargs)
        if not self.node_name:
            raise TreeError("Node must have a `name` attribute")

    @property
    def node_name(self) -> str:
        """Get node name

        Returns:
            (str)
        """
        return self.name

    @property
    def sep(self) -> str:
        """Get separator, gets from root node

        Returns:
            (str)
        """
        if self.is_root:
            return self._sep
        return self.parent.sep

    @sep.setter
    def sep(self, value: str):
        """Set separator, affects root node

        Args:
            value (str): separator to replace default separator
        """
        self.root._sep = value

    @property
    def path_name(self) -> str:
        """Get path name, separated by self.sep

        Returns:
            (str)
        """
        if self.is_root:
            return f"{self.sep}{self.name}"
        return f"{self.parent.path_name}{self.sep}{self.name}"

    def _BaseNode__pre_assign_parent(self, new_parent):
        """Do not allow duplicate nodes of same path

        Args:
            new_parent (Self): new parent to be added
        """
        if new_parent is not None:
            if any(
                child.node_name == self.node_name and child is not self
                for child in new_parent.children
            ):
                raise TreeError(
                    f"Error: Duplicate node with same path\n"
                    f"There exist a node with same path {new_parent.path_name}{self.sep}{self.node_name}"
                )

    def _BaseNode__pre_assign_children(self, new_children: List):
        """Do not allow duplicate nodes of same path

        Args:
            new_children (List[Self]): new children to be added
        """
        children_names = [node.node_name for node in new_children]
        duplicated_names = [
            item[0] for item in Counter(children_names).items() if item[1] > 1
        ]
        if len(duplicated_names):
            duplicated_names = " and ".join(
                [f"{self.path_name}{self.sep}{name}" for name in duplicated_names]
            )
            raise TreeError(
                f"Error: Duplicate node with same path\n"
                f"Attempting to add nodes same path {duplicated_names}"
            )

    def __repr__(self):
        class_name = self.__class__.__name__
        node_dict = self.describe(exclude_prefix="_", exclude_attributes=["name"])
        node_description = ", ".join([f"{k}={v}" for k, v in node_dict])
        return f"{class_name}({self.path_name}, {node_description})"

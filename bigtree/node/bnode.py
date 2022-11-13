from typing import Iterable, List, Union

from bigtree.node.node import Node
from bigtree.utils.exceptions import CorruptedTreeError, LoopError, TreeError


class BNode(Node):
    """
    BNode is an extension of Node, and is able to extend to any Python class for Binary Tree implementation.
    Nodes can have attributes if they are initialized from `BNode`, *dictionary*, or *pandas DataFrame*.

    BNode can be linked to each other with `children`, `left`, or `right` setter methods.
    If initialized with `children`, it must be length 2, denoting left and right child.

    >>> from bigtree import BNode, print_tree
    >>> a = BNode(1)
    >>> b = BNode(2)
    >>> c = BNode(3)
    >>> d = BNode(4)
    >>> a.children = [b, c]
    >>> b.right = d
    >>> print_tree(a)
    1
    ├── 2
    │   └── 4
    └── 3

    Directly passing `left`, `right`, or `children` argument.

    >>> from bigtree import BNode
    >>> d = BNode(4)
    >>> c = BNode(3)
    >>> b = BNode(2, right=d)
    >>> a = BNode(1, children=[b, c])

    **Node Creation**

    Node can be created by instantiating a `BNode` class or by using a *dictionary*.
    If node is created with dictionary, all keys of dictionary will be stored as class attributes.

    >>> from bigtree import BNode
    >>> a = BNode.from_dict({"name": "1"})
    >>> a
    BNode(name=1, val=1)

    **Node Attributes**

    These are node attributes that have getter and/or setter methods.

    Get `Node` configuration

    1. ``left``: Get left children
    2. ``right``: Get right children

    ----

    """

    def __init__(
        self,
        name: Union[str, int] = "",
        left=None,
        right=None,
        parent=None,
        children: List = None,
        **kwargs,
    ):
        self.val = int(name)
        self.name = str(name)
        self._sep = "/"
        self.__parent = None
        self.__children = []
        if not children:
            children = []
        if len(children):
            if len(children) and len(children) != 2:
                raise ValueError("Children input must have length 2")
            if left and left != children[0]:
                raise ValueError(
                    f"Attempting to set both left and children with mismatched values\n"
                    f"Check left {left} and children {children}"
                )
            if right and right != children[1]:
                raise ValueError(
                    f"Attempting to set both right and children with mismatched values\n"
                    f"Check right {right} and children {children}"
                )
        else:
            children = [left, right]
        self.parent = parent
        self.children = children
        if "parents" in kwargs:
            raise ValueError(
                "Attempting to set `parents` attribute, do you mean `parent`?"
            )
        self.__dict__.update(**kwargs)

    @property
    def left(self):
        """Get left children

        Returns:
            (Self)
        """
        return self.__children[0]

    @left.setter
    def left(self, left_child):
        """Set left children

        Args:
            left_child (Self): left child
        """
        self.children = [left_child, self.right]

    @property
    def right(self):
        """Get right children

        Returns:
            (Self)
        """
        return self.__children[1]

    @right.setter
    def right(self, right_child):
        """Set right children

        Args:
            right_child (Self): right child
        """
        self.children = [self.left, right_child]

    @property
    def parent(self):
        """Get parent node

        Returns:
            (Self)
        """
        return self.__parent

    @parent.setter
    def parent(self, new_parent):
        """Set parent node

        Args:
            new_parent (Self): parent node
        """
        # Check type
        if not (isinstance(new_parent, BNode) or new_parent is None):
            raise TypeError(
                f"Expect input to be BNode type or NoneType, received input type {type(new_parent)}"
            )

        # Check for loop
        if new_parent is not None:
            if new_parent is self:
                raise LoopError("Error setting parent: Node cannot be parent of itself")
            if any(
                ancestor is self
                for ancestor in new_parent.ancestors
                if new_parent.ancestors
            ):
                raise LoopError(
                    "Error setting parent: Node cannot be ancestor of itself"
                )

        current_parent = self.__parent
        current_child_idx = None
        if current_parent is not None:
            current_child_idx = current_parent.__children.index(self)

        # Assign new parent - rollback if error
        try:
            # Customizable check before assigning parent
            self.__pre_assign_parent(new_parent)

            # Remove child from current_parent
            if current_parent is not None:
                # Check for loop tree structure
                if not any(
                    child is self for child in current_parent.children
                ):  # pragma: no cover
                    raise CorruptedTreeError(
                        "Error setting parent: Node does not exist as children of its parent"
                    )

                # Detach child from current parent
                child_idx = current_parent.__children.index(self)
                current_parent.__children[child_idx] = None

            # Add child to new_parent
            self.__parent = new_parent
            if new_parent is not None:
                inserted = False
                for child_idx, child in enumerate(new_parent.__children):
                    if not child and not inserted:
                        new_parent.__children[child_idx] = self
                        inserted = True
                if not inserted:
                    raise TreeError(f"Parent {new_parent} already has 2 children")

            # Customizable check after assigning parent
            self.__post_assign_parent(new_parent)

        except Exception as exc_info:
            self.__parent = current_parent
            if current_parent is not None and self not in current_parent.__children:
                current_parent.__children.insert(current_child_idx, self)
            if new_parent is not None and self in new_parent.__children:
                new_parent.__children.remove(self)
            raise TreeError(exc_info)

    @property
    def children(self) -> Iterable:
        """Get child nodes

        Returns:
            (Iterable[Self])
        """
        return tuple(self.__children)

    @children.setter
    def children(self, new_children: List):
        """Set child nodes

        Args:
            new_children (List[Self]): child node
        """
        if not isinstance(new_children, list):
            raise TypeError(
                f"Children input should be list type, received input type {type(new_children)}"
            )
        if not len(new_children):
            new_children = [None, None]
        if len(new_children) != 2:
            raise ValueError("Children input must have length 2")

        seen_children = []
        for new_child in new_children:
            # Check type
            if new_child is not None and not isinstance(new_child, BNode):
                raise TypeError(
                    f"Expect input to be BNode type or NoneType, received input type {type(new_child)}"
                )

            # Check for loop and tree structure
            if new_child is self:
                raise LoopError("Error setting child: Node cannot be child of itself")
            if any(child is new_child for child in self.ancestors):
                raise LoopError(
                    "Error setting child: Node cannot be ancestors of itself"
                )

            # Check for duplicate children
            if new_child is not None:
                if id(new_child) in seen_children:
                    raise TreeError(
                        "Error setting child: Node cannot be added multiple times as a child"
                    )
                else:
                    seen_children.append(id(new_child))

        # Detach existing child node(s) - rollback if error
        current_new_children = {
            new_child: (new_child.parent.__children.index(new_child), new_child.parent)
            for new_child in new_children
            if new_child is not None and new_child.parent is not None
        }
        current_new_orphan = [
            new_child
            for new_child in new_children
            if new_child is not None and new_child.parent is None
        ]
        current_children = list(self.children)
        del self.children
        try:
            self.__pre_assign_children(new_children)
            self.__children = new_children
            for new_child in new_children:
                if new_child is not None:
                    new_child.__parent = self
            self.__post_assign_children(new_children)
        except Exception as exc_info:
            for child, idx_parent in current_new_children.items():
                child_idx, parent = idx_parent
                child.__parent = parent
                parent.__children.insert(child_idx, child)
            for child in current_new_orphan:
                child.__parent = None
            self.__children = current_children
            for child in current_children:
                child.__parent = self
            raise TreeError(exc_info)

    @children.deleter
    def children(self):
        """Delete child node(s)"""
        for child in self.children:
            if child is not None:
                child.__parent.__children.remove(child)
                child.__parent = None

    def __pre_assign_children(self, new_children: List):
        """Custom method to check before attaching children
        Can be overriden with `_BNode__pre_assign_children()`

        Args:
            new_children (List[Self]): new children to be added
        """
        pass

    def __post_assign_children(self, new_children: List):
        """Custom method to check after attaching children
        Can be overriden with `_BNode__post_assign_children()`

        Args:
            new_children (List[Self]): new children to be added
        """
        pass

    def __pre_assign_parent(self, new_parent):
        """Custom method to check before attaching parent
        Can be overriden with `_BNode__pre_assign_parent()`

        Args:
            new_parent (Self): new parent to be added
        """
        pass

    def __post_assign_parent(self, new_parent):
        """Custom method to check after attaching parent
        Can be overriden with `_BNode__post_assign_parent()`

        Args:
            new_parent (Self): new parent to be added
        """
        pass

    @property
    def is_leaf(self) -> bool:
        """Get indicator if self is leaf node

        Returns:
            (bool)
        """
        return not len([child for child in self.children if child])

    def sort(self, **kwargs):
        """Sort children, possible keyword arguments include ``key=lambda node: node.name``, ``reverse=True``

        >>> from bigtree import BNode, print_tree
        >>> a = BNode(1)
        >>> c = BNode(3, parent=a)
        >>> b = BNode(2, parent=a)
        >>> print_tree(a)
        1
        ├── 3
        └── 2
        >>> a.sort(key=lambda node: node.val)
        >>> print_tree(a)
        1
        ├── 2
        └── 3
        """
        children = [child for child in self.children if child]
        if len(children) == 2:
            children.sort(**kwargs)
            self.__children = children

    def __repr__(self):
        class_name = self.__class__.__name__
        node_dict = self.describe(exclude_prefix="_", exclude_attributes=[])
        node_description = ", ".join([f"{k}={v}" for k, v in node_dict])
        return f"{class_name}({node_description})"

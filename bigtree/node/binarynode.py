from typing import Iterable, List, Union

from bigtree.node.node import Node
from bigtree.utils.exceptions import CorruptedTreeError, LoopError, TreeError


class BinaryNode(Node):
    """
    BinaryNode is an extension of Node, and is able to extend to any Python class for Binary Tree implementation.
    Nodes can have attributes if they are initialized from `BinaryNode`, *dictionary*, or *pandas DataFrame*.

    BinaryNode can be linked to each other with `children`, `left`, or `right` setter methods.
    If initialized with `children`, it must be length 2, denoting left and right child.

    >>> from bigtree import BinaryNode, print_tree
    >>> a = BinaryNode(1)
    >>> b = BinaryNode(2)
    >>> c = BinaryNode(3)
    >>> d = BinaryNode(4)
    >>> a.children = [b, c]
    >>> b.right = d
    >>> print_tree(a)
    1
    ├── 2
    │   └── 4
    └── 3

    Directly passing `left`, `right`, or `children` argument.

    >>> from bigtree import BinaryNode
    >>> d = BinaryNode(4)
    >>> c = BinaryNode(3)
    >>> b = BinaryNode(2, right=d)
    >>> a = BinaryNode(1, children=[b, c])

    **Node Creation**

    Node can be created by instantiating a `BinaryNode` class or by using a *dictionary*.
    If node is created with dictionary, all keys of dictionary will be stored as class attributes.

    >>> from bigtree import BinaryNode
    >>> a = BinaryNode.from_dict({"name": "1"})
    >>> a
    BinaryNode(name=1, val=1)

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

    @staticmethod
    def __check_parent_type(new_parent):
        """Check parent type

        Args:
            new_parent (Self): parent node
        """
        if not (isinstance(new_parent, BinaryNode) or new_parent is None):
            raise TypeError(
                f"Expect input to be BinaryNode type or NoneType, received input type {type(new_parent)}"
            )

    @parent.setter
    def parent(self, new_parent):
        """Set parent node

        Args:
            new_parent (Self): parent node
        """
        self.__check_parent_type(new_parent)
        self._BaseNode__check_parent_loop(new_parent)

        current_parent = self.parent
        current_child_idx = None

        # Assign new parent - rollback if error
        self.__pre_assign_parent(new_parent)
        try:
            # Remove self from old parent
            if current_parent is not None:
                if not any(
                    child is self for child in current_parent.children
                ):  # pragma: no cover
                    raise CorruptedTreeError(
                        "Error setting parent: Node does not exist as children of its parent"
                    )
                current_child_idx = current_parent.__children.index(self)
                current_parent.__children[current_child_idx] = None

            # Assign self to new parent
            self.__parent = new_parent
            if new_parent is not None:
                inserted = False
                for child_idx, child in enumerate(new_parent.__children):
                    if not child and not inserted:
                        new_parent.__children[child_idx] = self
                        inserted = True
                if not inserted:
                    raise TreeError(f"Parent {new_parent} already has 2 children")

            self.__post_assign_parent(new_parent)

        except Exception as exc_info:
            # Remove self from new parent
            if new_parent is not None and self in new_parent.__children:
                child_idx = new_parent.__children.index(self)
                new_parent.__children[child_idx] = None

            # Reassign self to old parent
            self.__parent = current_parent
            if current_child_idx is not None:
                current_parent.__children[current_child_idx] = self
            raise TreeError(exc_info)

    def __pre_assign_parent(self, new_parent):
        """Custom method to check before attaching parent
        Can be overriden with `_BinaryNode__pre_assign_parent()`

        Args:
            new_parent (Self): new parent to be added
        """
        pass

    def __post_assign_parent(self, new_parent):
        """Custom method to check after attaching parent
        Can be overriden with `_BinaryNode__post_assign_parent()`

        Args:
            new_parent (Self): new parent to be added
        """
        pass

    @property
    def children(self) -> Iterable:
        """Get child nodes

        Returns:
            (Iterable[Self])
        """
        return tuple(self.__children)

    def __check_children_type(self, new_children: List) -> List:
        """Check child type

        Args:
            new_children (List[Self]): child node
        """
        if not len(new_children):
            new_children = [None, None]
        if len(new_children) != 2:
            raise ValueError("Children input must have length 2")
        return new_children

    def __check_children_loop(self, new_children: List):
        """Check child loop

        Args:
            new_children (List[Self]): child node
        """
        seen_children = []
        for new_child in new_children:
            # Check type
            if new_child is not None and not isinstance(new_child, BinaryNode):
                raise TypeError(
                    f"Expect input to be BinaryNode type or NoneType, received input type {type(new_child)}"
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

    @children.setter
    def children(self, new_children: List):
        """Set child nodes

        Args:
            new_children (List[Self]): child node
        """
        self._BaseNode__check_children_type(new_children)
        new_children = self.__check_children_type(new_children)
        self.__check_children_loop(new_children)

        current_new_children = {
            new_child: (
                new_child.parent.__children.index(new_child),
                new_child.parent,
            )
            for new_child in new_children
            if new_child is not None and new_child.parent is not None
        }
        current_new_orphan = [
            new_child
            for new_child in new_children
            if new_child is not None and new_child.parent is None
        ]
        current_children = list(self.children)

        # Assign new children - rollback if error
        self.__pre_assign_children(new_children)
        try:
            # Remove old children from self
            del self.children

            # Assign new children to self
            self.__children = new_children
            for new_child in new_children:
                if new_child is not None:
                    if new_child.parent:
                        child_idx = new_child.parent.__children.index(new_child)
                        new_child.parent.__children[child_idx] = None
                    new_child.__parent = self
            self.__post_assign_children(new_children)
        except Exception as exc_info:
            # Reassign new children to their original parent
            for child, idx_parent in current_new_children.items():
                child_idx, parent = idx_parent
                child.__parent = parent
                parent.__children[child_idx] = child
            for child in current_new_orphan:
                child.__parent = None

            # Reassign old children to self
            self.__children = current_children
            for child in current_children:
                if child:
                    child.__parent = self
            raise TreeError(exc_info)

    @children.deleter
    def children(self):
        """Delete child node(s)"""
        for child in self.children:
            if child is not None:
                child.parent.__children.remove(child)
                child.__parent = None

    def __pre_assign_children(self, new_children: List):
        """Custom method to check before attaching children
        Can be overriden with `_BinaryNode__pre_assign_children()`

        Args:
            new_children (List[Self]): new children to be added
        """
        pass

    def __post_assign_children(self, new_children: List):
        """Custom method to check after attaching children
        Can be overriden with `_BinaryNode__post_assign_children()`

        Args:
            new_children (List[Self]): new children to be added
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

        >>> from bigtree import BinaryNode, print_tree
        >>> a = BinaryNode(1)
        >>> c = BinaryNode(3, parent=a)
        >>> b = BinaryNode(2, parent=a)
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

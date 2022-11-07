import copy
from typing import Any, Dict, Iterable, List

from bigtree.utils.exceptions import LoopError, TreeError
from bigtree.utils.iterators import preorder_iter


class DAGNode:
    """
    Base DAGNode extends any Python class to a DAG node, for DAG implementation.
    In DAG implementation, a node can have multiple parents.
    If each node only has one parent, use `Node` class.
    DAGNodes can have attributes if they are initialized from `DAGNode` or dictionary.

    DAGNode can be linked to each other with `parents` and `children` setter methods,
    or using bitshift operator with the convention `parent_node >> child_node` or `child_node << parent_node`.

    >>> from bigtree import DAGNode
    >>> a = DAGNode("a")
    >>> b = DAGNode("b")
    >>> c = DAGNode("c")
    >>> d = DAGNode("d")
    >>> c.parents = [a, b]
    >>> c.children = [d]

    >>> from bigtree import DAGNode
    >>> a = DAGNode("a")
    >>> b = DAGNode("b")
    >>> c = DAGNode("c")
    >>> d = DAGNode("d")
    >>> a >> c
    >>> b >> c
    >>> d << c

    Directly passing `parents` argument.

    >>> from bigtree import DAGNode
    >>> a = DAGNode("a")
    >>> b = DAGNode("b")
    >>> c = DAGNode("c", parents=[a, b])
    >>> d = DAGNode("d", parents=[c])

    Directly passing `children` argument.

    >>> from bigtree import DAGNode
    >>> d = DAGNode("d")
    >>> c = DAGNode("c", children=[d])
    >>> b = DAGNode("b", children=[c])
    >>> a = DAGNode("a", children=[c])

    **Node Creation**

    Node can be created by instantiating a `Node` class or by using a *dictionary*.
    If node is created with dictionary, all keys of dictionary will be stored as class attributes.

    >>> from bigtree import DAGNode
    >>> a = DAGNode.from_dict({"name": "a", "age": 90})

    **Node Attributes**

    These are node attributes that have getter and/or setter methods.

    Get and set other `Node`

    1. ``parents``: Get/set parent nodes
    2. ``children``: Get/set child nodes

    Get other `Node`

    1. ``ancestors``: Get ancestors of node excluding self, iterator
    2. ``descendants``: Get descendants of node excluding self, iterator
    3. ``siblings``: Get siblings of self

    Get `Node` configuration

    1. ``node_name``: Get node name, without accessing `name` directly
    2. ``is_root``: Get indicator if self is root node
    3. ``is_leaf``: Get indicator if self is leaf node

    **Node Methods**

    These are methods available to be performed on `DAGNode`.

    Constructor methods

    1. ``from_dict()``: Create DAGNode from dictionary

    `Node` methods

    1. ``describe()``: Get node information sorted by attributes, returns list of tuples
    2. ``get_attr(attr_name: str)``: Get value of node attribute
    3. ``set_attrs(attrs: dict)``: Set node attribute name(s) and value(s)
    4. ``copy()``: Deep copy DAGNode

    ------------

    """

    def __init__(self, name: str = "", parents=None, children=None, **kwargs):
        self.name = name
        self.__parents = []
        self.__children = []
        if parents is None:
            parents = []
        if children is None:
            children = []
        self.parents = parents
        self.children = children
        if "parent" in kwargs:
            raise ValueError(
                "Attempting to set `parent` attribute, do you mean `parents`?"
            )
        self.__dict__.update(**kwargs)

    @property
    def parent(self) -> None:
        """Do not allow `parent` attribute to be accessed"""
        raise ValueError(
            "Attempting to access `parent` attribute, do you mean `parents`?"
        )

    @parent.setter
    def parent(self, new_parent):
        """Do not allow `parent` attribute to be set

        Args:
            new_parent (Self): parent node
        """
        raise ValueError("Attempting to set `parent` attribute, do you mean `parents`?")

    @property
    def parents(self) -> Iterable:
        """Get parent nodes

        Returns:
            (Iterable[Self])
        """
        return tuple(self.__parents)

    @parents.setter
    def parents(self, new_parents: List):
        """Set parent node

        Args:
            new_parents (List[Self]): parent nodes
        """
        # Check type
        if not isinstance(new_parents, list):
            raise TypeError(
                f"Parents input should be list type, received input type {type(new_parents)}"
            )
        seen_parent = []
        for new_parent in new_parents:
            # Check type
            if not isinstance(new_parent, DAGNode):
                raise TypeError(
                    f"Expect input to be DAGNode type, received input type {type(new_parent)}"
                )

            # Check for loop and tree structure
            if new_parent is self:
                raise LoopError("Error setting parent: Node cannot be parent of itself")
            if new_parent.ancestors:
                if any(ancestor is self for ancestor in new_parent.ancestors):
                    raise LoopError(
                        "Error setting parent: Node cannot be ancestor of itself"
                    )

            # Check for duplicate children
            if id(new_parent) in seen_parent:
                raise TreeError(
                    "Error setting parent: Node cannot be added multiple times as a parent"
                )
            else:
                seen_parent.append(id(new_parent))

        # Customizable check before assigning parent
        self.__pre_assign_parents(new_parents)

        # Add child to new_parent
        for new_parent in new_parents:
            if new_parent not in self.__parents:
                self.__parents.append(new_parent)
            new_parent.__children.append(self)

        # Customizable check after assigning parent
        self.__post_assign_parents(new_parents)

    def __pre_assign_parents(self, new_parents: List):
        """Custom method to check before attaching parent
        Can be overriden with `_DAGNode__pre_assign_parent()`

        Args:
            new_parents (List): new parents to be added
        """
        pass

    def __post_assign_parents(self, new_parents: List):
        """Custom method to check after attaching parent
        Can be overriden with `_DAGNode__post_assign_parent()`

        Args:
            new_parents (List): new parents to be added
        """
        pass

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
        seen_children = []
        for new_child in new_children:
            # Check type
            if not isinstance(new_child, DAGNode):
                raise TypeError(
                    f"Expect input to be DAGNode type, received input type {type(new_child)}"
                )

            # Check for loop and tree structure
            if new_child is self:
                raise LoopError("Error setting child: Node cannot be child of itself")
            if any(child is new_child for child in self.ancestors):
                raise LoopError(
                    "Error setting child: Node cannot be ancestors of itself"
                )

            # Check for duplicate children
            if id(new_child) in seen_children:
                raise TreeError(
                    "Error setting child: Node cannot be added multiple times as a child"
                )
            else:
                seen_children.append(id(new_child))

        # Detach existing child node(s)
        current_children = list(self.children)
        try:
            self.__pre_assign_children(new_children)
            for new_child in new_children:
                new_child.parents = [self]
            self.__post_assign_children(new_children)
        except TreeError or TypeError as exc_info:  # pragma: no cover
            self.children = current_children
            raise TreeError(exc_info)

    def __pre_assign_children(self, new_children: List):
        """Custom method to check before attaching children
        Can be overriden with `_DAGNode__pre_assign_children()`

        Args:
            new_children (List[Self]): new children to be added
        """
        pass

    def __post_assign_children(self, new_children: List):
        """Custom method to check after attaching children
        Can be overriden with `_DAGNode__post_assign_children()`

        Args:
            new_children (List[Self]): new children to be added
        """
        pass

    @property
    def ancestors(self) -> Iterable:
        """Get iterator to yield all ancestors of self, does not include self

        Returns:
            (Iterable[Self])
        """
        if not len(list(self.parents)):
            return ()

        def recursive_parent(node):
            for _node in node.parents:
                yield from recursive_parent(_node)
                yield _node

        ancestors = list(recursive_parent(self))
        return list(dict.fromkeys(ancestors))

    @property
    def descendants(self) -> Iterable:
        """Get iterator to yield all descendants of self, does not include self

        Returns:
            (Iterable[Self])
        """
        descendants = list(
            preorder_iter(self, filter_condition=lambda _node: _node != self)
        )
        return list(dict.fromkeys(descendants))

    @property
    def siblings(self) -> Iterable:
        """Get siblings of self

        Returns:
            (Iterable[Self])
        """
        if self.is_root:
            return ()
        return tuple(
            child
            for parent in self.parents
            for child in parent.children
            if child is not self
        )

    @property
    def node_name(self) -> str:
        """Get node name

        Returns:
            (str)
        """
        return self.name

    @property
    def is_root(self) -> bool:
        """Get indicator if self is root node

        Returns:
            (bool)
        """
        return not len(list(self.parents))

    @property
    def is_leaf(self) -> bool:
        """Get indicator if self is leaf node

        Returns:
            (bool)
        """
        return not len(list(self.children))

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]):
        """Construct node from dictionary, all keys of dictionary will be stored as class attributes
        Input dictionary must have key `name` if not `Node` will not have any name

        >>> from bigtree import DAGNode
        >>> a = DAGNode.from_dict({"name": "a", "age": 90})

        Args:
            input_dict (Dict[str, Any]): dictionary with node information, key: attribute name, value: attribute value

        Returns:
            (Self)
        """
        return cls(**input_dict)

    def describe(self, exclude_attributes: List[str] = [], exclude_prefix: str = ""):
        """Get node information sorted by attribute name, returns list of tuples

        Args:
            exclude_attributes (List[str]): list of attributes to exclude
            exclude_prefix (str): prefix of attributes to exclude

        Returns:
            (List[str])
        """
        return [
            item
            for item in sorted(self.__dict__.items(), key=lambda item: item[0])
            if (item[0] not in exclude_attributes)
            and (not len(exclude_prefix) or not item[0].startswith(exclude_prefix))
        ]

    def get_attr(self, attr_name: str) -> Any:
        """Get value of node attribute
        Returns None if attribute name does not exist

        Args:
            attr_name (str): attribute name

        Returns:
            (Any)
        """
        try:
            return self.__getattribute__(attr_name)
        except AttributeError:
            return None

    def set_attrs(self, attrs: Dict[str, Any]):
        """Set node attributes

        Args:
            attrs (Dict[str, Any]): attribute dictionary,
                key: attribute name, value: attribute value
        """
        self.__dict__.update(attrs)

    def copy(self):
        """Deep copy self; clone DAGNode

        >>> from bigtree.node.dagnode import DAGNode
        >>> a = DAGNode('a')
        >>> a_copy = a.copy()

        Returns:
            (Self)
        """
        return copy.deepcopy(self)

    def __copy__(self):
        """Shallow copy self

        >>> import copy
        >>> from bigtree.node.dagnode import DAGNode
        >>> a = DAGNode('a')
        >>> a_copy = copy.deepcopy(a)

        Returns:
            (Self)
        """
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __rshift__(self, other):
        """Set children using >> bitshift operator for self >> other

        Args:
            other (Self): other node, children
        """
        other.parents = [self]

    def __lshift__(self, other):
        """Set parent using << bitshift operator for self << other

        Args:
            other (Self): other node, parent
        """
        self.parents = [other]

    def __repr__(self):
        class_name = self.__class__.__name__
        node_dict = self.describe(exclude_attributes=["name"])
        node_description = ", ".join(
            [f"{k}={v}" for k, v in node_dict if not k.startswith("_")]
        )
        return f"{class_name}({self.node_name}, {node_description})"

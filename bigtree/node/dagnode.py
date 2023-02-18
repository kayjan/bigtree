import copy
from typing import Any, Dict, Iterable, List

from bigtree.utils.exceptions import LoopError, TreeError
from bigtree.utils.iterators import preorder_iter


class DAGNode:
    """
    Base DAGNode extends any Python class to a DAG node, for DAG implementation.
    In DAG implementation, a node can have multiple parents.
    Parents and children cannot be reassigned once assigned, as Nodes are allowed to have multiple parents and children.
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

    **DAGNode Creation**

    Node can be created by instantiating a `DAGNode` class or by using a *dictionary*.
    If node is created with dictionary, all keys of dictionary will be stored as class attributes.

    >>> from bigtree import DAGNode
    >>> a = DAGNode.from_dict({"name": "a", "age": 90})

    **DAGNode Attributes**

    These are node attributes that have getter and/or setter methods.

    Get and set other `DAGNode`

    1. ``parents``: Get/set parent nodes
    2. ``children``: Get/set child nodes

    Get other `DAGNode`

    1. ``ancestors``: Get ancestors of node excluding self, iterator
    2. ``descendants``: Get descendants of node excluding self, iterator
    3. ``siblings``: Get siblings of self

    Get `DAGNode` configuration

    1. ``node_name``: Get node name, without accessing `name` directly
    2. ``is_root``: Get indicator if self is root node
    3. ``is_leaf``: Get indicator if self is leaf node

    **DAGNode Methods**

    These are methods available to be performed on `DAGNode`.

    Constructor methods

    1. ``from_dict()``: Create DAGNode from dictionary

    `DAGNode` methods

    1. ``describe()``: Get node information sorted by attributes, returns list of tuples
    2. ``get_attr(attr_name: str)``: Get value of node attribute
    3. ``set_attrs(attrs: dict)``: Set node attribute name(s) and value(s)
    4. ``go_to(node: BaseNode)``: Get a path from own node to another node from same DAG
    5. ``copy()``: Deep copy DAGNode

    ----

    """

    def __init__(
        self, name: str = "", parents: List = None, children: List = None, **kwargs
    ):
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

    @staticmethod
    def __check_parent_type(new_parents: List):
        """Check parent type

        Args:
            new_parents (List[Self]): parent nodes
        """
        if not isinstance(new_parents, list):
            raise TypeError(
                f"Parents input should be list type, received input type {type(new_parents)}"
            )

    def __check_parent_loop(self, new_parents: List):
        """Check parent type

        Args:
            new_parents (List[Self]): parent nodes
        """
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

    @parents.setter
    def parents(self, new_parents: List):
        """Set parent node

        Args:
            new_parents (List[Self]): parent nodes
        """
        self.__check_parent_type(new_parents)
        self.__check_parent_loop(new_parents)

        current_parents = self.__parents.copy()

        # Assign new parents - rollback if error
        self.__pre_assign_parents(new_parents)
        try:
            # Assign self to new parent
            for new_parent in new_parents:
                if new_parent not in self.__parents:
                    self.__parents.append(new_parent)
                    new_parent.__children.append(self)

            self.__post_assign_parents(new_parents)
        except Exception as exc_info:
            # Remove self from new parent
            for new_parent in new_parents:
                if new_parent not in current_parents:
                    self.__parents.remove(new_parent)
                    new_parent.__children.remove(self)
            raise TreeError(
                f"{exc_info}, current parents {current_parents}, new parents {new_parents}"
            )

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

    def __check_children_type(self, new_children: List):
        """Check child type

        Args:
            new_children (List[Self]): child node
        """
        if not isinstance(new_children, list):
            raise TypeError(
                f"Children input should be list type, received input type {type(new_children)}"
            )

    def __check_children_loop(self, new_children: List):
        """Check child loop

        Args:
            new_children (List[Self]): child node
        """
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

    @children.setter
    def children(self, new_children: List):
        """Set child nodes

        Args:
            new_children (List[Self]): child node
        """
        self.__check_children_type(new_children)
        self.__check_children_loop(new_children)

        current_children = list(self.children)

        # Assign new children - rollback if error
        self.__pre_assign_children(new_children)
        try:
            # Assign new children to self
            for new_child in new_children:
                if self not in new_child.__parents:
                    new_child.__parents.append(self)
                    self.__children.append(new_child)
            self.__post_assign_children(new_children)
        except Exception as exc_info:
            # Reassign old children to self
            for new_child in new_children:
                if new_child not in current_children:
                    new_child.__parents.remove(self)
                    self.__children.remove(new_child)
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

        >>> from bigtree.node.dagnode import DAGNode
        >>> a = DAGNode('a')
        >>> a.set_attrs({"age": 90})
        >>> a
        DAGNode(a, age=90)

        Args:
            attrs (Dict[str, Any]): attribute dictionary,
                key: attribute name, value: attribute value
        """
        self.__dict__.update(attrs)

    def go_to(self, node) -> Iterable[Iterable]:
        """Get list of possible paths from current node to specified node from same tree

        >>> from bigtree import DAGNode
        >>> a = DAGNode("a")
        >>> b = DAGNode("b")
        >>> c = DAGNode("c")
        >>> d = DAGNode("d")
        >>> a >> c
        >>> b >> c
        >>> c >> d
        >>> a >> d
        >>> a.go_to(c)
        [[DAGNode(a, ), DAGNode(c, )]]
        >>> a.go_to(d)
        [[DAGNode(a, ), DAGNode(c, ), DAGNode(d, )], [DAGNode(a, ), DAGNode(d, )]]
        >>> a.go_to(b)
        Traceback (most recent call last):
            ...
        bigtree.utils.exceptions.TreeError: It is not possible to go to DAGNode(b, )

        Args:
            node (Self): node to travel to from current node, inclusive of start and end node

        Returns:
            (Iterable[Iterable])
        """
        if not isinstance(node, DAGNode):
            raise TypeError(
                f"Expect node to be DAGNode type, received input type {type(node)}"
            )
        if self == node:
            return [self]
        if node not in self.descendants:
            raise TreeError(f"It is not possible to go to {node}")

        self.__path = []

        def recursive_path(_node, _path, _ans):
            if _node:  # pragma: no cover
                _path.append(_node)
                if _node == node:
                    return _path
                for _child in _node.children:
                    ans = recursive_path(_child, _path.copy(), _ans)
                    if ans:
                        self.__path.append(ans)

        recursive_path(self, [], [])
        return self.__path

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

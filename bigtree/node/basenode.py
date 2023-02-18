import copy
from typing import Any, Dict, Iterable, List

from bigtree.utils.exceptions import CorruptedTreeError, LoopError, TreeError
from bigtree.utils.iterators import preorder_iter


class BaseNode:
    """
    BaseNode extends any Python class to a tree node.
    Nodes can have attributes if they are initialized from `Node`, *dictionary*, or *pandas DataFrame*.

    Nodes can be linked to each other with `parent` and `children` setter methods,
    or using bitshift operator with the convention `parent_node >> child_node` or `child_node << parent_node`.

    >>> from bigtree import Node, print_tree
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65)
    >>> c = Node("c", age=60)
    >>> d = Node("d", age=40)
    >>> root.children = [b, c]
    >>> d.parent = b
    >>> print_tree(root, attr_list=["age"])
    a [age=90]
    ├── b [age=65]
    │   └── d [age=40]
    └── c [age=60]

    >>> from bigtree import Node
    >>> root = Node("a", age=90)
    >>> b = Node("b", age=65)
    >>> c = Node("c", age=60)
    >>> d = Node("d", age=40)
    >>> root >> b
    >>> root >> c
    >>> d << b
    >>> print_tree(root, attr_list=["age"])
    a [age=90]
    ├── b [age=65]
    │   └── d [age=40]
    └── c [age=60]

    Directly passing `parent` argument.

    >>> from bigtree import Node
    >>> root = Node("a")
    >>> b = Node("b", parent=root)
    >>> c = Node("c", parent=root)
    >>> d = Node("d", parent=b)

    Directly passing `children` argument.

    >>> from bigtree import Node
    >>> d = Node("d")
    >>> c = Node("c")
    >>> b = Node("b", children=[d])
    >>> a = Node("a", children=[b, c])

    **BaseNode Creation**

    Node can be created by instantiating a `BaseNode` class or by using a *dictionary*.
    If node is created with dictionary, all keys of dictionary will be stored as class attributes.

    >>> from bigtree import Node
    >>> root = Node.from_dict({"name": "a", "age": 90})

    **BaseNode Attributes**

    These are node attributes that have getter and/or setter methods.

    Get and set other `BaseNode`

    1. ``parent``: Get/set parent node
    2. ``children``: Get/set child nodes

    Get other `BaseNode`

    1. ``ancestors``: Get ancestors of node excluding self, iterator
    2. ``descendants``: Get descendants of node excluding self, iterator
    3. ``leaves``: Get all leaf node(s) from self, iterator
    4. ``siblings``: Get siblings of self
    5. ``left_sibling``: Get sibling left of self
    6. ``right_sibling``: Get sibling right of self

    Get `BaseNode` configuration

    1. ``node_path``: Get tuple of nodes from root
    2. ``is_root``: Get indicator if self is root node
    3. ``is_leaf``: Get indicator if self is leaf node
    4. ``root``: Get root node of tree
    5. ``depth``: Get depth of self
    6. ``max_depth``: Get maximum depth from root to leaf node

    **BaseNode Methods**

    These are methods available to be performed on `BaseNode`.

    Constructor methods

    1. ``from_dict()``: Create BaseNode from dictionary

    `BaseNode` methods

    1. ``describe()``: Get node information sorted by attributes, returns list of tuples
    2. ``get_attr(attr_name: str)``: Get value of node attribute
    3. ``set_attrs(attrs: dict)``: Set node attribute name(s) and value(s)
    4. ``go_to(node: BaseNode)``: Get a path from own node to another node from same tree
    5. ``copy()``: Deep copy BaseNode
    6. ``sort()``: Sort child nodes

    ----

    """

    def __init__(self, parent=None, children: List = None, **kwargs):
        self.__parent = None
        self.__children = []
        if children is None:
            children = []
        self.parent = parent
        self.children = children
        if "parents" in kwargs:
            raise ValueError(
                "Attempting to set `parents` attribute, do you mean `parent`?"
            )
        self.__dict__.update(**kwargs)

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
        if not (isinstance(new_parent, BaseNode) or new_parent is None):
            raise TypeError(
                f"Expect input to be BaseNode type or NoneType, received input type {type(new_parent)}"
            )

    def __check_parent_loop(self, new_parent):
        """Check parent type

        Args:
            new_parent (Self): parent node
        """
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

    @parent.setter
    def parent(self, new_parent):
        """Set parent node

        Args:
            new_parent (Self): parent node
        """
        self.__check_parent_type(new_parent)
        self.__check_parent_loop(new_parent)

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
                current_parent.__children.remove(self)

            # Assign self to new parent
            self.__parent = new_parent
            if new_parent is not None:
                new_parent.__children.append(self)

            self.__post_assign_parent(new_parent)

        except Exception as exc_info:
            # Remove self from new parent
            if new_parent is not None:
                new_parent.__children.remove(self)

            # Reassign self to old parent
            self.__parent = current_parent
            if current_child_idx is not None:
                current_parent.__children.insert(current_child_idx, self)
            raise TreeError(exc_info)

    def __pre_assign_parent(self, new_parent):
        """Custom method to check before attaching parent
        Can be overriden with `_BaseNode__pre_assign_parent()`

        Args:
            new_parent (Self): new parent to be added
        """
        pass

    def __post_assign_parent(self, new_parent):
        """Custom method to check after attaching parent
        Can be overriden with `_BaseNode__post_assign_parent()`

        Args:
            new_parent (Self): new parent to be added
        """
        pass

    @property
    def parents(self) -> None:
        """Do not allow `parents` attribute to be accessed"""
        raise ValueError(
            "Attempting to access `parents` attribute, do you mean `parent`?"
        )

    @parents.setter
    def parents(self, new_parent):
        """Do not allow `parents` attribute to be set

        Args:
            new_parent (Self): parent node
        """
        raise ValueError("Attempting to set `parents` attribute, do you mean `parent`?")

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
            if not isinstance(new_child, BaseNode):
                raise TypeError(
                    f"Expect input to be BaseNode type, received input type {type(new_child)}"
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

        current_new_children = {
            new_child: (new_child.parent.__children.index(new_child), new_child.parent)
            for new_child in new_children
            if new_child.parent is not None
        }
        current_new_orphan = [
            new_child for new_child in new_children if new_child.parent is None
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
                if new_child.parent:
                    new_child.parent.__children.remove(new_child)
                new_child.__parent = self
            self.__post_assign_children(new_children)
        except Exception as exc_info:
            # Reassign new children to their original parent
            for child, idx_parent in current_new_children.items():
                child_idx, parent = idx_parent
                child.__parent = parent
                parent.__children.insert(child_idx, child)
            for child in current_new_orphan:
                child.__parent = None

            # Reassign old children to self
            self.__children = current_children
            for child in current_children:
                child.__parent = self
            raise TreeError(exc_info)

    @children.deleter
    def children(self):
        """Delete child node(s)"""
        for child in self.children:
            child.parent.__children.remove(child)
            child.__parent = None

    def __pre_assign_children(self, new_children: List):
        """Custom method to check before attaching children
        Can be overriden with `_BaseNode__pre_assign_children()`

        Args:
            new_children (List[Self]): new children to be added
        """
        pass

    def __post_assign_children(self, new_children: List):
        """Custom method to check after attaching children
        Can be overriden with `_BaseNode__post_assign_children()`

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
        node = self.parent
        while node is not None:
            yield node
            node = node.parent

    @property
    def descendants(self) -> Iterable:
        """Get iterator to yield all descendants of self, does not include self

        Returns:
            (Iterable[Self])
        """
        yield from preorder_iter(self, filter_condition=lambda _node: _node != self)

    @property
    def leaves(self) -> Iterable:
        """Get iterator to yield all leaf nodes from self

        Returns:
            (Iterable[Self])
        """
        yield from preorder_iter(self, filter_condition=lambda _node: _node.is_leaf)

    @property
    def siblings(self) -> Iterable:
        """Get siblings of self

        Returns:
            (Iterable[Self])
        """
        if self.is_root:
            return ()
        return tuple(child for child in self.parent.children if child is not self)

    @property
    def left_sibling(self):
        """Get sibling left of self

        Returns:
            (Self)
        """
        if self.parent:
            children = self.parent.children
            child_idx = children.index(self)
            if child_idx:
                return self.parent.children[child_idx - 1]
        return None

    @property
    def right_sibling(self):
        """Get sibling right of self

        Returns:
            (Self)
        """
        if self.parent:
            children = self.parent.children
            child_idx = children.index(self)
            if child_idx + 1 < len(children):
                return self.parent.children[child_idx + 1]
        return None

    @property
    def node_path(self) -> Iterable:
        """Get tuple of nodes starting from root

        Returns:
            (Iterable[Self])
        """
        if self.is_root:
            return [self]
        return tuple(list(self.parent.node_path) + [self])

    @property
    def is_root(self) -> bool:
        """Get indicator if self is root node

        Returns:
            (bool)
        """
        return self.parent is None

    @property
    def is_leaf(self) -> bool:
        """Get indicator if self is leaf node

        Returns:
            (bool)
        """
        return not len(list(self.children))

    @property
    def root(self):
        """Get root node of tree

        Returns:
            (Self)
        """
        if self.is_root:
            return self
        return self.parent.root

    @property
    def depth(self) -> int:
        """Get depth of self, indexing starts from 1

        Returns:
            (int)
        """
        if self.is_root:
            return 1
        return self.parent.depth + 1

    @property
    def max_depth(self) -> int:
        """Get maximum depth from root to leaf node

        Returns:
            (int)
        """
        return max(node.depth for node in list(preorder_iter(self.root)))

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]):
        """Construct node from dictionary, all keys of dictionary will be stored as class attributes
        Input dictionary must have key `name` if not `Node` will not have any name

        >>> from bigtree import Node
        >>> a = Node.from_dict({"name": "a", "age": 90})

        Args:
            input_dict (Dict[str, Any]): dictionary with node information, key: attribute name, value: attribute value

        Returns:
            (Self)
        """
        return cls(**input_dict)

    def describe(self, exclude_attributes: List[str] = [], exclude_prefix: str = ""):
        """Get node information sorted by attribute name, returns list of tuples

        >>> from bigtree.node.node import Node
        >>> a = Node('a', age=90)
        >>> a.describe()
        [('_BaseNode__children', []), ('_BaseNode__parent', None), ('_sep', '/'), ('age', 90), ('name', 'a')]
        >>> a.describe(exclude_prefix="_")
        [('age', 90), ('name', 'a')]
        >>> a.describe(exclude_prefix="_", exclude_attributes=["name"])
        [('age', 90)]

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

        >>> from bigtree.node.node import Node
        >>> a = Node('a', age=90)
        >>> a.get_attr("age")
        90

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

        >>> from bigtree.node.node import Node
        >>> a = Node('a')
        >>> a.set_attrs({"age": 90})
        >>> a
        Node(/a, age=90)

        Args:
            attrs (Dict[str, Any]): attribute dictionary,
                key: attribute name, value: attribute value
        """
        self.__dict__.update(attrs)

    def go_to(self, node) -> Iterable:
        """Get path from current node to specified node from same tree

        >>> from bigtree import Node, print_tree
        >>> a = Node(name="a")
        >>> b = Node(name="b", parent=a)
        >>> c = Node(name="c", parent=a)
        >>> d = Node(name="d", parent=b)
        >>> e = Node(name="e", parent=b)
        >>> f = Node(name="f", parent=c)
        >>> g = Node(name="g", parent=e)
        >>> h = Node(name="h", parent=e)
        >>> print_tree(a)
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f
        >>> d.go_to(d)
        [Node(/a/b/d, )]
        >>> d.go_to(g)
        [Node(/a/b/d, ), Node(/a/b, ), Node(/a/b/e, ), Node(/a/b/e/g, )]
        >>> d.go_to(f)
        [Node(/a/b/d, ), Node(/a/b, ), Node(/a, ), Node(/a/c, ), Node(/a/c/f, )]

        Args:
            node (Self): node to travel to from current node, inclusive of start and end node

        Returns:
            (Iterable)
        """
        if not isinstance(node, BaseNode):
            raise TypeError(
                f"Expect node to be BaseNode type, received input type {type(node)}"
            )
        if self.root != node.root:
            raise TreeError(
                f"Nodes are not from the same tree. Check {self} and {node}"
            )
        if self == node:
            return [self]
        self_path = [self] + list(self.ancestors)
        node_path = ([node] + list(node.ancestors))[::-1]
        common_nodes = set(self_path).intersection(set(node_path))
        self_min_index, min_common_node = sorted(
            [(self_path.index(_node), _node) for _node in common_nodes]
        )[0]
        node_min_index = node_path.index(min_common_node)
        return self_path[:self_min_index] + node_path[node_min_index:]

    def copy(self):
        """Deep copy self; clone BaseNode

        >>> from bigtree.node.node import Node
        >>> a = Node('a')
        >>> a_copy = a.copy()

        Returns:
            (Self)
        """
        return copy.deepcopy(self)

    def sort(self, **kwargs):
        """Sort children, possible keyword arguments include ``key=lambda node: node.name``, ``reverse=True``

        >>> from bigtree import Node, print_tree
        >>> a = Node('a')
        >>> c = Node("c", parent=a)
        >>> b = Node("b", parent=a)
        >>> print_tree(a)
        a
        ├── c
        └── b
        >>> a.sort(key=lambda node: node.name)
        >>> print_tree(a)
        a
        ├── b
        └── c
        """
        children = list(self.children)
        children.sort(**kwargs)
        self.__children = children

    def __copy__(self):
        """Shallow copy self

        >>> import copy
        >>> from bigtree.node.node import Node
        >>> a = Node('a')
        >>> a_copy = copy.deepcopy(a)

        Returns:
            (Self)
        """
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __repr__(self):
        class_name = self.__class__.__name__
        node_dict = self.describe(exclude_prefix="_")
        node_description = ", ".join([f"{k}={v}" for k, v in node_dict])
        return f"{class_name}({node_description})"

    def __rshift__(self, other):
        """Set children using >> bitshift operator for self >> other

        Args:
            other (Self): other node, children
        """
        other.parent = self

    def __lshift__(self, other):
        """Set parent using << bitshift operator for self << other

        Args:
            other (Self): other node, parent
        """
        self.parent = other

from __future__ import annotations

import copy
import heapq
from typing import Any, Dict, Generator, Iterable, List, Optional, Set, Tuple, TypeVar

from bigtree.globals import ASSERTIONS
from bigtree.utils import exceptions, iterators

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover
    plt = None


class BaseNode:
    """
    BaseNode extends any Python class to a tree node. Nodes can have attributes if they are initialized from `Node`,
    *dictionary*, or *pandas DataFrame*.

    Nodes can be linked to each other with `parent` and `children` setter methods, or using bitshift operator with the
    convention `parent_node >> child_node` or `child_node << parent_node`.

    Examples:
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

    Node can be created by instantiating a `BaseNode` class or by using a *dictionary*. If node is created with
    dictionary, all keys of dictionary will be stored as class attributes.

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
    5. ``diameter``: Get diameter of self
    6. ``depth``: Get depth of self
    7. ``max_depth``: Get maximum depth from root to leaf node

    **BaseNode Methods**

    These are methods available to be performed on `BaseNode`.

    Constructor methods

    1. ``from_dict()``: Create BaseNode from dictionary

    `BaseNode` methods

    1. ``describe()``: Get node information sorted by attributes, return list of tuples
    2. ``get_attr(attr_name: str)``: Get value of node attribute
    3. ``set_attrs(attrs: dict)``: Set node attribute name(s) and value(s)
    4. ``go_to(node: Self)``: Get a path from own node to another node from same tree
    5. ``append(node: Self)``: Add child to node
    6. ``extend(nodes: List[Self])``: Add multiple children to node
    7. ``copy()``: Deep copy self
    8. ``sort()``: Sort child nodes
    9. ``plot()``: Plot tree in line form

    ----

    """

    def __init__(
        self,
        parent: Optional[T] = None,
        children: Optional[List[T]] = None,
        **kwargs: Any,
    ):
        self.__parent: Optional[T] = None
        self.__children: List[T] = []
        if children is None:
            children = []
        self.parent = parent
        self.children = children  # type: ignore
        if "parents" in kwargs:
            raise AttributeError(
                "Attempting to set `parents` attribute, do you mean `parent`?"
            )
        self.__dict__.update(**kwargs)

    @staticmethod
    def __check_parent_type(new_parent: T) -> None:
        """Check parent type.

        Args:
            new_parent: parent node
        """
        if not (isinstance(new_parent, BaseNode) or new_parent is None):
            raise TypeError(
                f"Expect parent to be BaseNode type or NoneType, received input type {type(new_parent)}"
            )

    def __check_parent_loop(self, new_parent: T) -> None:
        """Check parent type.

        Args:
            new_parent: parent node
        """
        if new_parent is not None:
            if new_parent is self:
                raise exceptions.LoopError(
                    "Error setting parent: Node cannot be parent of itself"
                )
            if any(
                ancestor is self
                for ancestor in new_parent.ancestors
                if new_parent.ancestors
            ):
                raise exceptions.LoopError(
                    "Error setting parent: Node cannot be ancestor of itself"
                )

    @property
    def parent(self: T) -> Optional[T]:
        """Get parent node.

        Returns:
            Parent node, none if the node is root
        """
        return self.__parent

    @parent.setter
    def parent(self: T, new_parent: T) -> None:
        """Set parent node.

        Args:
            new_parent: parent node
        """
        if ASSERTIONS:
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
                    raise exceptions.CorruptedTreeError(
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
            raise exceptions.TreeError(exc_info)

    def __pre_assign_parent(self, new_parent: T) -> None:
        """Custom method to check before attaching parent. Can be overridden with `_BaseNode__pre_assign_parent()`.

        Args:
            new_parent: new parent to be added
        """
        pass

    def __post_assign_parent(self, new_parent: T) -> None:
        """Custom method to check after attaching parent. Can be overridden with `_BaseNode__post_assign_parent()`.

        Args:
            new_parent: new parent to be added
        """
        pass

    @property
    def parents(self) -> None:
        """Do not allow `parents` attribute to be accessed.

        Raises:
            AttributeError: No such attribute
        """
        raise AttributeError(
            "Attempting to access `parents` attribute, do you mean `parent`?"
        )

    @parents.setter
    def parents(self, new_parent: T) -> None:
        """Do not allow `parents` attribute to be set.

        Args:
            new_parent: parent node

        Raises:
            AttributeError: No such attribute
        """
        raise AttributeError(
            "Attempting to set `parents` attribute, do you mean `parent`?"
        )

    def __check_children_type(self: T, new_children: Iterable[T]) -> None:
        """Check child type.

        Args:
            new_children: child node
        """
        if (
            not isinstance(new_children, list)
            and not isinstance(new_children, tuple)
            and not isinstance(new_children, set)
        ):
            raise TypeError(
                f"Expect children to be List or Tuple or Set type, received input type {type(new_children)}"
            )

    def __check_children_loop(self: T, new_children: Iterable[T]) -> None:
        """Check child loop.

        Args:
            new_children: child node
        """
        seen_children = []
        for new_child in new_children:
            # Check type
            if not isinstance(new_child, BaseNode):
                raise TypeError(
                    f"Expect children to be BaseNode type, received input type {type(new_child)}"
                )

            # Check for loop and tree structure
            if new_child is self:
                raise exceptions.LoopError(
                    "Error setting child: Node cannot be child of itself"
                )
            if any(child is new_child for child in self.ancestors):
                raise exceptions.LoopError(
                    "Error setting child: Node cannot be ancestor of itself"
                )

            # Check for duplicate children
            if id(new_child) in seen_children:
                raise exceptions.TreeError(
                    "Error setting child: Node cannot be added multiple times as a child"
                )
            else:
                seen_children.append(id(new_child))

    @property
    def children(self: T) -> Tuple[T, ...]:
        """Get child nodes.

        Returns:
            Child node(s)
        """
        return tuple(self.__children)

    @children.setter
    def children(self: T, new_children: List[T] | Tuple[T] | Set[T]) -> None:
        """Set child nodes.

        Args:
            new_children: child node
        """
        if ASSERTIONS:
            self.__check_children_type(new_children)
            self.__check_children_loop(new_children)
        new_children = list(new_children)

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
            raise exceptions.TreeError(exc_info)

    @children.deleter
    def children(self) -> None:
        """Delete child node(s)."""
        for child in self.children:
            child.parent.__children.remove(child)  # type: ignore
            child.__parent = None

    def __pre_assign_children(self: T, new_children: Iterable[T]) -> None:
        """Custom method to check before attaching children. Can be overridden with `_BaseNode__pre_assign_children()`.

        Args:
            new_children: new children to be added
        """
        pass

    def __post_assign_children(self: T, new_children: Iterable[T]) -> None:
        """Custom method to check after attaching children. Can be overridden with `_BaseNode__post_assign_children()`.

        Args:
            new_children (Iterable[Self]): new children to be added
        """
        pass

    @property
    def ancestors(self: T) -> Iterable[T]:
        """Get iterator to yield all ancestors of self, does not include self.

        Returns:
            Ancestor(s) of node excluding itself
        """
        node = self.parent
        while node is not None:
            yield node
            node = node.parent

    @property
    def descendants(self: T) -> Iterable[T]:
        """Get iterator to yield all descendants of self, does not include self.

        Returns:
            Descendant(s) of node excluding itself
        """
        yield from iterators.preorder_iter(
            self, filter_condition=lambda _node: _node != self
        )

    @property
    def leaves(self: T) -> Iterable[T]:
        """Get iterator to yield all leaf nodes from self.

        Returns:
            Leaf node(s) of node
        """
        yield from iterators.preorder_iter(
            self, filter_condition=lambda _node: _node.is_leaf
        )

    @property
    def siblings(self: T) -> Iterable[T]:
        """Get siblings of self.

        Returns:
            Sibling(s) of node
        """
        if self.parent is None:
            return ()
        return tuple(child for child in self.parent.children if child is not self)

    @property
    def left_sibling(self: T) -> Optional[T]:
        """Get sibling left of self.

        Returns:
            Left sibling of node
        """
        if self.parent:
            children = self.parent.children
            child_idx = children.index(self)
            if child_idx:
                return self.parent.children[child_idx - 1]

    @property
    def right_sibling(self: T) -> Optional[T]:
        """Get sibling right of self.

        Returns:
            Right sibling of node
        """
        if self.parent:
            children = self.parent.children
            child_idx = children.index(self)
            if child_idx + 1 < len(children):
                return self.parent.children[child_idx + 1]

    @property
    def node_path(self: T) -> Iterable[T]:
        """Get tuple of nodes starting from root.

        Returns:
            Node path from root to itself
        """
        if self.parent is None:
            return tuple([self])
        return tuple(list(self.parent.node_path) + [self])

    @property
    def is_root(self) -> bool:
        """Get indicator if self is root node.

        Returns:
            Indicator if node is root node
        """
        return self.parent is None

    @property
    def is_leaf(self) -> bool:
        """Get indicator if self is leaf node.

        Returns:
            Indicator if node is leaf node
        """
        return not len(list(self.children))

    @property
    def root(self: T) -> T:
        """Get root node of tree.

        Returns:
            Root node
        """
        if self.parent is None:
            return self
        return self.parent.root

    @property
    def diameter(self) -> int:
        """Get diameter of tree or subtree, the length of longest path between any two nodes.

        Returns:
            Diameter of node
        """
        diameter = 0

        if self.is_leaf:
            return diameter

        def _recursive_diameter(node: T) -> int:
            """Recursively iterate through node and its children to get diameter of node.

            Args:
                node: current node

            Returns:
                Diameter of node
            """
            nonlocal diameter
            if node.is_leaf:
                return 1
            child_length = [_recursive_diameter(child) for child in node.children]
            diameter = max(diameter, sum(heapq.nlargest(2, child_length)))
            return 1 + max(child_length)

        _recursive_diameter(self)
        return diameter

    @property
    def depth(self) -> int:
        """Get depth of self, indexing starts from 1.

        Returns:
            Depth of node
        """
        if self.parent is None:
            return 1
        return self.parent.depth + 1

    @property
    def max_depth(self) -> int:
        """Get maximum depth from root to leaf node.

        Returns:
            Maximum depth of tree
        """
        return max(
            [self.root.depth] + [node.depth for node in list(self.root.descendants)]
        )

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> BaseNode:
        """Construct node from dictionary, all keys of dictionary will be stored as class attributes.
        Input dictionary must have key `name` if not `Node` will not have any name.

        Examples:
            >>> from bigtree import Node
            >>> a = Node.from_dict({"name": "a", "age": 90})

        Args:
            input_dict: dictionary with node information, key: attribute name, value: attribute value

        Returns:
            Base node
        """
        return cls(**input_dict)

    def describe(
        self, exclude_attributes: List[str] = [], exclude_prefix: str = ""
    ) -> List[Tuple[str, Any]]:
        """Get node information sorted by attribute name, returns list of tuples.

        Examples:
            >>> from bigtree.node.node import Node
            >>> a = Node('a', age=90)
            >>> a.describe()
            [('_BaseNode__children', []), ('_BaseNode__parent', None), ('_sep', '/'), ('age', 90), ('name', 'a')]
            >>> a.describe(exclude_prefix="_")
            [('age', 90), ('name', 'a')]
            >>> a.describe(exclude_prefix="_", exclude_attributes=["name"])
            [('age', 90)]

        Args:
            exclude_attributes: list of attributes to exclude
            exclude_prefix: prefix of attributes to exclude

        Returns:
            List of attribute name and attribute value pairs
        """
        return [
            item
            for item in sorted(self.__dict__.items(), key=lambda item: item[0])
            if (item[0] not in exclude_attributes)
            and (not len(exclude_prefix) or not item[0].startswith(exclude_prefix))
        ]

    def get_attr(self, attr_name: str, default_value: Any = None) -> Any:
        """Get value of node attribute. Returns default value if attribute name does not exist.

        Examples:
            >>> from bigtree.node.node import Node
            >>> a = Node('a', age=90)
            >>> a.get_attr("age")
            90

        Args:
            attr_name: attribute name
            default_value: default value if attribute does not exist

        Returns:
            Attribute value of node
        """
        try:
            return getattr(self, attr_name)
        except AttributeError:
            return default_value

    def set_attrs(self, attrs: Dict[str, Any]) -> None:
        """Set node attributes.

        Examples:
            >>> from bigtree.node.node import Node
            >>> a = Node('a')
            >>> a.set_attrs({"age": 90})
            >>> a
            Node(/a, age=90)

        Args:
            attrs: attribute dictionary, key: attribute name, value: attribute value
        """
        self.__dict__.update(attrs)

    def go_to(self: T, node: T) -> Iterable[T]:
        """Get path from current node to specified node from same tree, uses `get_path` function.

        Args:
            node: node to travel to from current node, inclusive of start and end node

        Returns:
            Path from current node to destination node
        """
        from bigtree.tree.parsing import get_path

        return get_path(self, node)

    def append(self: T, other: T) -> None:
        """Add other as child of self.

        Args:
            other: other node, child to be added
        """
        other.parent = self

    def extend(self: T, others: List[T]) -> None:
        """Add others as children of self.

        Args:
            others: other nodes, children to be added
        """
        for child in others:
            child.parent = self

    def copy(self: T) -> T:
        """Deep copy self; clone self.

        Examples:
            >>> from bigtree.node.node import Node
            >>> a = Node('a')
            >>> a_copy = a.copy()

        Returns:
            Cloned copy of node
        """
        return copy.deepcopy(self)

    def sort(self: T, **kwargs: Any) -> None:
        """Sort children, possible keyword arguments include ``key=lambda node: node.node_name``, ``reverse=True``.
        Accepts kwargs for sort() function.

        Examples:
            >>> from bigtree import Node, print_tree
            >>> a = Node('a')
            >>> c = Node("c", parent=a)
            >>> b = Node("b", parent=a)
            >>> print_tree(a)
            a
            ├── c
            └── b
            >>> a.sort(key=lambda node: node.node_name)
            >>> print_tree(a)
            a
            ├── b
            └── c
        """
        children = list(self.children)
        children.sort(**kwargs)
        self.__children = children

    def plot(self, *args: Any, **kwargs: Any) -> plt.Figure:
        """Plot tree in line form. Accepts args and kwargs for matplotlib.pyplot.plot() function.

        Examples:
            >>> import matplotlib.pyplot as plt
            >>> from bigtree import list_to_tree
            >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
            >>> root = list_to_tree(path_list)
            >>> root.plot("-ok")
            <Figure size 1280x960 with 1 Axes>
        """
        from bigtree.utils.plot import plot_tree, reingold_tilford

        if self.get_attr("x") is None or self.get_attr("y") is None:
            reingold_tilford(self)
        return plot_tree(self, *args, **kwargs)

    def __copy__(self: T) -> T:
        """Shallow copy self.

        Examples:
            >>> import copy
            >>> from bigtree.node.node import Node
            >>> a = Node('a')
            >>> a_copy = copy.deepcopy(a)

        Returns:
            Shallow copy of node
        """
        obj: T = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __repr__(self) -> str:
        """Print format of BaseNode.

        Returns:
            Print format of BaseNode
        """
        class_name = self.__class__.__name__
        node_dict = self.describe(exclude_prefix="_")
        node_description = ", ".join([f"{k}={v}" for k, v in node_dict])
        return f"{class_name}({node_description})"

    def __rshift__(self: T, other: T) -> None:
        """Set children using >> bitshift operator for self >> children (other).

        Args:
            other: other node, children
        """
        other.parent = self

    def __lshift__(self: T, other: T) -> None:
        """Set parent using << bitshift operator for self << parent (other).

        Args:
            other: other node, parent
        """
        self.parent = other

    def __iter__(self) -> Generator[T, None, None]:
        """Iterate through child nodes

        Returns:
            Iterable of child node(s)
        """
        yield from self.children  # type: ignore

    def __contains__(self, other_node: T) -> bool:
        """Check if child node exists.

        Args:
            other_node: child node

        Returns:
            Indicator if other node is child of current node
        """
        return other_node in self.children


T = TypeVar("T", bound=BaseNode)

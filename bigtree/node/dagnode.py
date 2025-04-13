from __future__ import annotations

import copy
from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, TypeVar

from bigtree.globals import ASSERTIONS
from bigtree.utils import exceptions, iterators


class DAGNode:
    """
    Base DAGNode extends any Python class to a DAG node, for DAG implementation. In DAG implementation, a node can have
    multiple parents.

    Parents and children cannot be reassigned once assigned, as Nodes are allowed to have multiple parents and children.
    If each node only has one parent, use `Node` class. DAGNodes can have attributes if they are initialized from
    `DAGNode` or dictionary.

    DAGNode can be linked to each other with `parents` and `children` setter methods, or using bitshift operator with
    the convention `parent_node >> child_node` or `child_node << parent_node`.

    Examples:
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

    Node can be created by instantiating a `DAGNode` class or by using a *dictionary*. If node is created with dictionary,
    all keys of dictionary will be stored as class attributes.

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

    1. ``describe()``: Get node information sorted by attributes, return list of tuples
    2. ``get_attr(attr_name: str)``: Get value of node attribute
    3. ``set_attrs(attrs: dict)``: Set node attribute name(s) and value(s)
    4. ``go_to(node: Self)``: Get a path from own node to another node from same DAG
    5. ``copy()``: Deep copy self

    ----

    """

    def __init__(
        self,
        name: str = "",
        parents: Optional[List[T]] = None,
        children: Optional[List[T]] = None,
        **kwargs: Any,
    ):
        self.name = name
        self.__parents: List[T] = []
        self.__children: List[T] = []
        if parents is None:
            parents = []
        if children is None:
            children = []
        self.parents = parents
        self.children = children
        if "parent" in kwargs:
            raise AttributeError(
                "Attempting to set `parent` attribute, do you mean `parents`?"
            )
        self.__dict__.update(**kwargs)

    @property
    def parent(self) -> None:
        """Do not allow `parent` attribute to be accessed.

        Raises:
            AttributeError: No such attribute
        """
        raise AttributeError(
            "Attempting to access `parent` attribute, do you mean `parents`?"
        )

    @parent.setter
    def parent(self, new_parent: T) -> None:
        """Do not allow `parent` attribute to be set.

        Args:
            new_parent: parent node

        Raises:
            AttributeError
        """
        raise AttributeError(
            "Attempting to set `parent` attribute, do you mean `parents`?"
        )

    @staticmethod
    def __check_parent_type(new_parents: List[T]) -> None:
        """Check parent type.

        Args:
            new_parents: parent nodes
        """
        if not isinstance(new_parents, list):
            raise TypeError(
                f"Parents input should be list type, received input type {type(new_parents)}"
            )

    def __check_parent_loop(self: T, new_parents: List[T]) -> None:
        """Check parent type.

        Args:
            new_parents: parent nodes
        """
        seen_parent = []
        for new_parent in new_parents:
            # Check type
            if not isinstance(new_parent, DAGNode):
                raise TypeError(
                    f"Expect parent to be DAGNode type, received input type {type(new_parent)}"
                )

            # Check for loop and tree structure
            if new_parent is self:
                raise exceptions.LoopError(
                    "Error setting parent: Node cannot be parent of itself"
                )
            if new_parent.ancestors:
                if any(ancestor is self for ancestor in new_parent.ancestors):
                    raise exceptions.LoopError(
                        "Error setting parent: Node cannot be ancestor of itself"
                    )

            # Check for duplicate children
            if id(new_parent) in seen_parent:
                raise exceptions.TreeError(
                    "Error setting parent: Node cannot be added multiple times as a parent"
                )
            else:
                seen_parent.append(id(new_parent))

    @property
    def parents(self: T) -> Iterable[T]:
        """Get parent nodes.

        Returns:
            Parent node(s)
        """
        return tuple(self.__parents)

    @parents.setter
    def parents(self: T, new_parents: List[T]) -> None:
        """Set parent node.

        Args:
            new_parents: parent nodes
        """
        if ASSERTIONS:
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
            raise exceptions.TreeError(exc_info)

    def __pre_assign_parents(self: T, new_parents: List[T]) -> None:
        """Custom method to check before attaching parent. Can be overridden with `_DAGNode__pre_assign_parent()`.

        Args:
            new_parents: new parents to be added
        """
        pass

    def __post_assign_parents(self: T, new_parents: List[T]) -> None:
        """Custom method to check after attaching parent. Can be overridden with `_DAGNode__post_assign_parent()`.

        Args:
            new_parents: new parents to be added
        """
        pass

    def __check_children_type(self: T, new_children: Iterable[T]) -> None:
        """Check child type.

        Args:
            new_children: child node
        """
        if not isinstance(new_children, Iterable):
            raise TypeError(
                f"Expect children to be Iterable type, received input type {type(new_children)}"
            )

    def __check_children_loop(self: T, new_children: Iterable[T]) -> None:
        """Check child loop.

        Args:
            new_children: child node
        """
        seen_children = []
        for new_child in new_children:
            # Check type
            if not isinstance(new_child, DAGNode):
                raise TypeError(
                    f"Expect children to be DAGNode type, received input type {type(new_child)}"
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
    def children(self: T) -> Iterable[T]:
        """Get child nodes.

        Returns:
            Child node(s)
        """
        return tuple(self.__children)

    @children.setter
    def children(self: T, new_children: Iterable[T]) -> None:
        """Set child nodes.

        Args:
            new_children: child node
        """
        if ASSERTIONS:
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
            raise exceptions.TreeError(exc_info)

    @children.deleter
    def children(self) -> None:
        """Delete child node(s)."""
        for child in self.children:
            self.__children.remove(child)  # type: ignore
            child.__parents.remove(self)  # type: ignore

    def __pre_assign_children(self: T, new_children: Iterable[T]) -> None:
        """Custom method to check before attaching children. Can be overridden with `_DAGNode__pre_assign_children()`.

        Args:
            new_children: new children to be added
        """
        pass

    def __post_assign_children(self: T, new_children: Iterable[T]) -> None:
        """Custom method to check after attaching children. Can be overridden with `_DAGNode__post_assign_children()`.

        Args:
            new_children: new children to be added
        """
        pass

    @property
    def ancestors(self: T) -> Iterable[T]:
        """Get iterator to yield all ancestors of self, does not include self.

        Returns:
            Ancestor(s) of node excluding itself
        """
        if not len(list(self.parents)):
            return ()

        def _recursive_parent(node: T) -> Iterable[T]:
            """Recursively yield parent of current node, returns earliest to latest ancestor.

            Args:
                node: current node

            Returns:
                Parent node
            """
            for _node in node.parents:
                yield from _recursive_parent(_node)
                yield _node

        ancestors = list(_recursive_parent(self))
        return list(dict.fromkeys(ancestors))

    @property
    def descendants(self: T) -> Iterable[T]:
        """Get iterator to yield all descendants of self, does not include self.

        Returns:
            Descendant(s) of node excluding itself
        """
        descendants = iterators.preorder_iter(
            self, filter_condition=lambda _node: _node != self
        )
        return list(dict.fromkeys(descendants))

    @property
    def siblings(self: T) -> Iterable[T]:
        """Get siblings of self.

        Returns:
            Sibling(s) of node
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
        """Get node name.

        Returns:
            Node name
        """
        return self.name

    @property
    def is_root(self) -> bool:
        """Get indicator if self is root node.

        Returns:
            Indicator if node is root node
        """
        return not len(list(self.parents))

    @property
    def is_leaf(self) -> bool:
        """Get indicator if self is leaf node.

        Returns:
            Indicator if node is leaf node
        """
        return not len(list(self.children))

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> DAGNode:
        """Construct node from dictionary, all keys of dictionary will be stored as class attributes.
        Input dictionary must have key `name` if not `Node` will not have any name.

        Examples:
            >>> from bigtree import DAGNode
            >>> a = DAGNode.from_dict({"name": "a", "age": 90})

        Args:
            input_dict: dictionary with node information, key: attribute name, value: attribute value

        Returns:
            DAG node
        """
        return cls(**input_dict)

    def describe(
        self, exclude_attributes: List[str] = [], exclude_prefix: str = ""
    ) -> List[Tuple[str, Any]]:
        """Get node information sorted by attribute name, returns list of tuples.

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
            >>> from bigtree.node.dagnode import DAGNode
            >>> a = DAGNode('a')
            >>> a.set_attrs({"age": 90})
            >>> a
            DAGNode(a, age=90)

        Args:
            attrs: attribute dictionary, key: attribute name, value: attribute value
        """
        self.__dict__.update(attrs)

    def go_to(self: T, node: T) -> List[List[T]]:
        """Get list of possible paths from current node to specified node from same tree, uses `get_path_dag` function.

        Args:
            node: node to travel to from current node, inclusive of start and end node

        Returns:
            Possible paths from current node to destination node
        """
        from bigtree.dag.parsing import get_path_dag

        return get_path_dag(self, node)

    def copy(self: T) -> T:
        """Deep copy self; clone DAGNode.

        Examples:
            >>> from bigtree.node.dagnode import DAGNode
            >>> a = DAGNode('a')
            >>> a_copy = a.copy()

        Returns:
            Cloned copy of node
        """
        return copy.deepcopy(self)

    def __copy__(self: T) -> T:
        """Shallow copy self.

        Examples:
            >>> import copy
            >>> from bigtree.node.dagnode import DAGNode
            >>> a = DAGNode('a')
            >>> a_copy = copy.deepcopy(a)

        Returns:
            Shallow copy of node
        """
        obj: T = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __getitem__(self, child_name: str) -> "DAGNode":
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
            self.__children.remove(child)  # type: ignore
            child.__parents.remove(self)  # type: ignore

    def __repr__(self) -> str:
        """Print format of DAGNode.

        Returns:
            Print format of DAGNode
        """
        class_name = self.__class__.__name__
        node_dict = self.describe(exclude_attributes=["name"])
        node_description = ", ".join(
            [f"{k}={v}" for k, v in node_dict if not k.startswith("_")]
        )
        return f"{class_name}({self.node_name}, {node_description})"

    def __rshift__(self: T, other: T) -> None:
        """Set children using >> bitshift operator for self >> children (other).

        Args:
            other: other node, children
        """
        other.parents = [self]

    def __lshift__(self: T, other: T) -> None:
        """Set parent using << bitshift operator for self << parent (other).

        Args:
            other: other node, parent
        """
        self.parents = [other]

    def __iter__(self) -> Generator[T, None, None]:
        """Iterate through child nodes.

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


T = TypeVar("T", bound=DAGNode)

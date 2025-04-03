from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Callable,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

if TYPE_CHECKING:
    from bigtree.node import basenode, binarynode, dagnode

    BaseNodeT = TypeVar("BaseNodeT", bound=basenode.BaseNode)
    BinaryNodeT = TypeVar("BinaryNodeT", bound=binarynode.BinaryNode)
    DAGNodeT = TypeVar("DAGNodeT", bound=dagnode.DAGNode)
    T = TypeVar("T", bound=Union[basenode.BaseNode, dagnode.DAGNode])

__all__ = [
    "inorder_iter",
    "preorder_iter",
    "postorder_iter",
    "levelorder_iter",
    "levelordergroup_iter",
    "zigzag_iter",
    "zigzaggroup_iter",
    "dag_iterator",
]


def inorder_iter(
    tree: BinaryNodeT,
    filter_condition: Optional[Callable[[BinaryNodeT], bool]] = None,
    max_depth: int = 0,
) -> Iterable[BinaryNodeT]:
    """Iterate through all children of a tree.

    In-Order Iteration Algorithm LNR:
        1. Recursively traverse the current node's left subtree
        2. Visit the current node
        3. Recursively traverse the current node's right subtree

    Examples:
        >>> from bigtree import BinaryNode, list_to_binarytree, inorder_iter
        >>> num_list = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> root = list_to_binarytree(num_list)
        >>> root.show()
        1
        ├── 2
        │   ├── 4
        │   │   └── 8
        │   └── 5
        └── 3
            ├── 6
            └── 7

        >>> [node.node_name for node in inorder_iter(root)]
        ['8', '4', '2', '5', '1', '6', '3', '7']

        >>> [node.node_name for node in inorder_iter(root, filter_condition=lambda x: x.node_name in ["1", "4", "3", "6", "7"])]
        ['4', '1', '6', '3', '7']

        >>> [node.node_name for node in inorder_iter(root, max_depth=3)]
        ['4', '2', '5', '1', '6', '3', '7']

    Args:
        tree: input tree
        filter_condition: function that takes in node as argument. Return node if condition evaluates to `True`
        max_depth: maximum depth of iteration, based on `depth` attribute

    Returns:
        Iterable of nodes
    """
    if tree and (not max_depth or not tree.depth > max_depth):
        yield from inorder_iter(tree.left, filter_condition, max_depth)
        if not filter_condition or filter_condition(tree):
            yield tree
        yield from inorder_iter(tree.right, filter_condition, max_depth)


def preorder_iter(
    tree: T,
    filter_condition: Optional[Callable[[T], bool]] = None,
    stop_condition: Optional[Callable[[T], bool]] = None,
    max_depth: int = 0,
) -> Iterable[T]:
    """Iterate through all children of a tree.

    Pre-Order Iteration Algorithm NLR:
        1. Visit the current node
        2. Recursively traverse the current node's left subtree
        3. Recursively traverse the current node's right subtree

    It is topologically sorted because a parent node is processed before its child nodes.

    Examples:
        >>> from bigtree import Node, list_to_tree, preorder_iter
        >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
        >>> root = list_to_tree(path_list)
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f

        >>> [node.node_name for node in preorder_iter(root)]
        ['a', 'b', 'd', 'e', 'g', 'h', 'c', 'f']

        >>> [node.node_name for node in preorder_iter(root, filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"])]
        ['a', 'd', 'e', 'g', 'f']

        >>> [node.node_name for node in preorder_iter(root, stop_condition=lambda x: x.node_name == "e")]
        ['a', 'b', 'd', 'c', 'f']

        >>> [node.node_name for node in preorder_iter(root, max_depth=3)]
        ['a', 'b', 'd', 'e', 'c', 'f']

    Args:
        tree: input tree
        filter_condition: function that takes in node as argument. Return node if condition evaluates to `True`
        stop_condition: function that takes in node as argument. Stops iteration if condition evaluates to `True`
        max_depth: maximum depth of iteration, based on `depth` attribute

    Returns:
        Iterable of nodes
    """
    if (
        tree
        and (not max_depth or not tree.get_attr("depth") > max_depth)
        and (not stop_condition or not stop_condition(tree))
    ):
        if not filter_condition or filter_condition(tree):
            yield tree
        for child in tree.children:
            yield from preorder_iter(child, filter_condition, stop_condition, max_depth)  # type: ignore


def postorder_iter(
    tree: BaseNodeT,
    filter_condition: Optional[Callable[[BaseNodeT], bool]] = None,
    stop_condition: Optional[Callable[[BaseNodeT], bool]] = None,
    max_depth: int = 0,
) -> Iterable[BaseNodeT]:
    """Iterate through all children of a tree.

    Post-Order Iteration Algorithm LRN:
        1. Recursively traverse the current node's left subtree
        2. Recursively traverse the current node's right subtree
        3. Visit the current node

    Examples:
        >>> from bigtree import Node, list_to_tree, postorder_iter
        >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
        >>> root = list_to_tree(path_list)
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f

        >>> [node.node_name for node in postorder_iter(root)]
        ['d', 'g', 'h', 'e', 'b', 'f', 'c', 'a']

        >>> [node.node_name for node in postorder_iter(root, filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"])]
        ['d', 'g', 'e', 'f', 'a']

        >>> [node.node_name for node in postorder_iter(root, stop_condition=lambda x: x.node_name == "e")]
        ['d', 'b', 'f', 'c', 'a']

        >>> [node.node_name for node in postorder_iter(root, max_depth=3)]
        ['d', 'e', 'b', 'f', 'c', 'a']

    Args:
        tree: input tree
        filter_condition: function that takes in node as argument. Return node if condition evaluates to `True`
        stop_condition: function that takes in node as argument. Stops iteration if condition evaluates to `True`
        max_depth: maximum depth of iteration, based on `depth` attribute

    Returns:
        Iterable of nodes
    """
    if (
        tree
        and (not max_depth or not tree.depth > max_depth)
        and (not stop_condition or not stop_condition(tree))
    ):
        for child in tree.children:
            yield from postorder_iter(
                child, filter_condition, stop_condition, max_depth
            )
        if not filter_condition or filter_condition(tree):
            yield tree


def levelorder_iter(
    tree: BaseNodeT,
    filter_condition: Optional[Callable[[BaseNodeT], bool]] = None,
    stop_condition: Optional[Callable[[BaseNodeT], bool]] = None,
    max_depth: int = 0,
) -> Iterable[BaseNodeT]:
    """Iterate through all children of a tree.

    Level-Order Iteration Algorithm:
        1. Recursively traverse the nodes on same level

    Examples:
        >>> from bigtree import Node, list_to_tree, levelorder_iter
        >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
        >>> root = list_to_tree(path_list)
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f

        >>> [node.node_name for node in levelorder_iter(root)]
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        >>> [node.node_name for node in levelorder_iter(root, filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"])]
        ['a', 'd', 'e', 'f', 'g']

        >>> [node.node_name for node in levelorder_iter(root, stop_condition=lambda x: x.node_name == "e")]
        ['a', 'b', 'c', 'd', 'f']

        >>> [node.node_name for node in levelorder_iter(root, max_depth=3)]
        ['a', 'b', 'c', 'd', 'e', 'f']

    Args:
        tree: input tree
        filter_condition: function that takes in node as argument. Return node if condition evaluates to `True`
        stop_condition: function that takes in node as argument. Stops iteration if condition evaluates to `True`
        max_depth: maximum depth of iteration, based on `depth` attribute

    Returns:
        Iterable of nodes
    """

    def _levelorder_iter(trees: List[BaseNodeT]) -> Iterable[BaseNodeT]:
        """Iterate through all children of a tree.

        Args:
            trees: trees to get children for next level

        Returns:
            Iterable of nodes
        """
        next_level = []
        for _tree in trees:
            if _tree:
                if (not max_depth or not _tree.depth > max_depth) and (
                    not stop_condition or not stop_condition(_tree)
                ):
                    if not filter_condition or filter_condition(_tree):
                        yield _tree
                    next_level.extend(list(_tree.children))
        if len(next_level):
            yield from _levelorder_iter(next_level)

    yield from _levelorder_iter([tree])


def levelordergroup_iter(
    tree: BaseNodeT,
    filter_condition: Optional[Callable[[BaseNodeT], bool]] = None,
    stop_condition: Optional[Callable[[BaseNodeT], bool]] = None,
    max_depth: int = 0,
) -> Iterable[Iterable[BaseNodeT]]:
    """Iterate through all children of a tree.

    Level-Order Group Iteration Algorithm:
        1. Recursively traverse the nodes on same level, returns nodes level by level in a nested list

    Examples:
        >>> from bigtree import Node, list_to_tree, levelordergroup_iter
        >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
        >>> root = list_to_tree(path_list)
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f

        >>> [[node.node_name for node in group] for group in levelordergroup_iter(root)]
        [['a'], ['b', 'c'], ['d', 'e', 'f'], ['g', 'h']]

        >>> [[node.node_name for node in group] for group in levelordergroup_iter(root, filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"])]
        [['a'], [], ['d', 'e', 'f'], ['g']]

        >>> [[node.node_name for node in group] for group in levelordergroup_iter(root, stop_condition=lambda x: x.node_name == "e")]
        [['a'], ['b', 'c'], ['d', 'f']]

        >>> [[node.node_name for node in group] for group in levelordergroup_iter(root, max_depth=3)]
        [['a'], ['b', 'c'], ['d', 'e', 'f']]

    Args:
        tree: input tree
        filter_condition: function that takes in node as argument. Return node if condition evaluates to `True`
        stop_condition: function that takes in node as argument. Stops iteration if condition evaluates to `True`
        max_depth: maximum depth of iteration, based on `depth` attribute

    Returns:
        List of iterable of nodes
    """

    def _levelordergroup_iter(trees: List[BaseNodeT]) -> Iterable[Iterable[BaseNodeT]]:
        """Iterate through all children of a tree.

        Args:
            trees: trees to get children for next level

        Returns:
            List of iterable of nodes
        """
        current_tree = []
        next_level = []
        for _tree in trees:
            if (not max_depth or not _tree.depth > max_depth) and (
                not stop_condition or not stop_condition(_tree)
            ):
                if not filter_condition or filter_condition(_tree):
                    current_tree.append(_tree)
                next_level.extend([_child for _child in _tree.children if _child])
        yield tuple(current_tree)
        if len(next_level) and (not max_depth or not next_level[0].depth > max_depth):
            yield from _levelordergroup_iter(next_level)

    yield from _levelordergroup_iter([tree])


def zigzag_iter(
    tree: BaseNodeT,
    filter_condition: Optional[Callable[[BaseNodeT], bool]] = None,
    stop_condition: Optional[Callable[[BaseNodeT], bool]] = None,
    max_depth: int = 0,
) -> Iterable[BaseNodeT]:
    """ "Iterate through all children of a tree.

    ZigZag Iteration Algorithm:
        1. Recursively traverse the nodes on same level, in a zigzag manner across different levels

    Examples:
        >>> from bigtree import Node, list_to_tree, zigzag_iter
        >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
        >>> root = list_to_tree(path_list)
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f

        >>> [node.node_name for node in zigzag_iter(root)]
        ['a', 'c', 'b', 'd', 'e', 'f', 'h', 'g']

        >>> [node.node_name for node in zigzag_iter(root, filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"])]
        ['a', 'd', 'e', 'f', 'g']

        >>> [node.node_name for node in zigzag_iter(root, stop_condition=lambda x: x.node_name == "e")]
        ['a', 'c', 'b', 'd', 'f']

        >>> [node.node_name for node in zigzag_iter(root, max_depth=3)]
        ['a', 'c', 'b', 'd', 'e', 'f']

    Args:
        tree: input tree
        filter_condition: function that takes in node as argument. Return node if condition evaluates to `True`
        stop_condition: function that takes in node as argument. Stops iteration if condition evaluates to `True`
        max_depth: maximum depth of iteration, based on `depth` attribute

    Returns:
        Iterable of nodes
    """

    def _zigzag_iter(
        trees: List[BaseNodeT], reverse_indicator: bool = False
    ) -> Iterable[BaseNodeT]:
        """Iterate through all children of a tree.

        Args:
            trees: trees to get children for next level
            reverse_indicator: indicator whether it is in reverse order

        Returns:
            Iterable of nodes
        """
        next_level = []
        for _tree in trees:
            if _tree:
                if (not max_depth or not _tree.depth > max_depth) and (
                    not stop_condition or not stop_condition(_tree)
                ):
                    if not filter_condition or filter_condition(_tree):
                        yield _tree
                    next_level_nodes = list(_tree.children)
                    if reverse_indicator:
                        next_level_nodes = next_level_nodes[::-1]
                    next_level.extend(next_level_nodes)
        if len(next_level):
            yield from _zigzag_iter(
                next_level[::-1], reverse_indicator=not reverse_indicator
            )

    yield from _zigzag_iter([tree])


def zigzaggroup_iter(
    tree: BaseNodeT,
    filter_condition: Optional[Callable[[BaseNodeT], bool]] = None,
    stop_condition: Optional[Callable[[BaseNodeT], bool]] = None,
    max_depth: int = 0,
) -> Iterable[Iterable[BaseNodeT]]:
    """Iterate through all children of a tree.

    ZigZag Group Iteration Algorithm:
        1. Recursively traverse the nodes on same level, in a zigzag manner across different levels, returns nodes level
        by level in a nested list

    Examples:
        >>> from bigtree import Node, list_to_tree, zigzaggroup_iter
        >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
        >>> root = list_to_tree(path_list)
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f

        >>> [[node.node_name for node in group] for group in zigzaggroup_iter(root)]
        [['a'], ['c', 'b'], ['d', 'e', 'f'], ['h', 'g']]

        >>> [[node.node_name for node in group] for group in zigzaggroup_iter(root, filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"])]
        [['a'], [], ['d', 'e', 'f'], ['g']]

        >>> [[node.node_name for node in group] for group in zigzaggroup_iter(root, stop_condition=lambda x: x.node_name == "e")]
        [['a'], ['c', 'b'], ['d', 'f']]

        >>> [[node.node_name for node in group] for group in zigzaggroup_iter(root, max_depth=3)]
        [['a'], ['c', 'b'], ['d', 'e', 'f']]

    Args:
        tree: input tree
        filter_condition: function that takes in node as argument. Return node if condition evaluates to `True`
        stop_condition: function that takes in node as argument. Stops iteration if condition evaluates to `True`
        max_depth: maximum depth of iteration, based on `depth` attribute

    Returns:
        List of iterable of nodes
    """

    def _zigzaggroup_iter(
        trees: List[BaseNodeT], reverse_indicator: bool = False
    ) -> Iterable[Iterable[BaseNodeT]]:
        """Iterate through all children of a tree.

        Args:
            trees: trees to get children for next level
            reverse_indicator: indicator whether it is in reverse order

        Returns:
            List of iterable of nodes
        """
        current_tree = []
        next_level = []
        for _tree in trees:
            if (not max_depth or not _tree.depth > max_depth) and (
                not stop_condition or not stop_condition(_tree)
            ):
                if not filter_condition or filter_condition(_tree):
                    current_tree.append(_tree)
                next_level_nodes = [_child for _child in _tree.children if _child]
                if reverse_indicator:
                    next_level_nodes = next_level_nodes[::-1]
                next_level.extend(next_level_nodes)
        yield tuple(current_tree)
        if len(next_level) and (not max_depth or not next_level[0].depth > max_depth):
            yield from _zigzaggroup_iter(
                next_level[::-1], reverse_indicator=not reverse_indicator
            )

    yield from _zigzaggroup_iter([tree])


def dag_iterator(dag: DAGNodeT) -> Iterable[Tuple[DAGNodeT, DAGNodeT]]:
    """Iterate through all nodes of a Directed Acyclic Graph (DAG). Note that node names must be unique. Note that DAG
    must at least have two nodes to be shown on graph.

    DAG Iteration:
        1. Visit the current node
        2. Recursively traverse the current node's parents
        3. Recursively traverse the current node's children

    Examples:
        >>> from bigtree import DAGNode, dag_iterator
        >>> a = DAGNode("a", step=1)
        >>> b = DAGNode("b", step=1)
        >>> c = DAGNode("c", step=2, parents=[a, b])
        >>> d = DAGNode("d", step=2, parents=[a, c])
        >>> e = DAGNode("e", step=3, parents=[d])
        >>> [(parent.node_name, child.node_name) for parent, child in dag_iterator(a)]
        [('a', 'c'), ('a', 'd'), ('b', 'c'), ('c', 'd'), ('d', 'e')]

    Args:
        dag: input dag

    Returns:
        Iterable of parent-child pair
    """
    visited_nodes = set()

    def _dag_iterator(node: DAGNodeT) -> Iterable[Tuple[DAGNodeT, DAGNodeT]]:
        """Iterate through all children of a DAG.

        Args:
            node: current node

        Returns:
            Iterable of parent-child pair
        """
        node_name = node.node_name
        visited_nodes.add(node_name)

        # Parse upwards
        for parent in node.parents:
            parent_name = parent.node_name
            if parent_name not in visited_nodes:
                yield parent, node

        # Parse downwards
        for child in node.children:
            child_name = child.node_name
            if child_name not in visited_nodes:
                yield node, child

        # Parse upwards
        for parent in node.parents:
            parent_name = parent.node_name
            if parent_name not in visited_nodes:
                yield from _dag_iterator(parent)

        # Parse downwards
        for child in node.children:
            child_name = child.node_name
            if child_name not in visited_nodes:
                yield from _dag_iterator(child)

    yield from _dag_iterator(dag)

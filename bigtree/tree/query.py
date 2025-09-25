from typing import TypeVar

from bigtree.node import basenode
from bigtree.tree._query import QUERY_GRAMMAR, QueryTransformer
from bigtree.utils import exceptions, iterators

try:
    from lark import Lark
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    Lark = MagicMock()

__all__ = [
    "query_tree",
]

T = TypeVar("T", bound=basenode.BaseNode)


@exceptions.optional_dependencies_query
def query_tree(tree_node: T, query: str, debug: bool = False) -> list[T]:
    """Query tree using Tree Definition Language.

    - Supports clauses: AND, OR, NOT
    - Supports operation: ==, !=, >, <, >=, <=, BETWEEN, IN, LIKE
    - Note that string match in query must be in double quotes

    Examples:
        >>> from bigtree import Node, Tree
        >>> paths = {
        ...     "a": {"age": 90},
        ...     "a/b": {"age": 65},
        ...     "a/c": {"age": 60},
        ...     "a/b/d": {"age": 40},
        ...     "a/b/e": {"age": 35},
        ...     "a/c/f": {"age": 38},
        ...     "a/b/e/g": {"age": 10},
        ...     "a/b/e/h": {"age": 6},
        ... }
        >>> tree = Tree.from_dict(paths)
        >>> tree.show(all_attrs=True)
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        │       ├── g [age=10]
        │       └── h [age=6]
        └── c [age=60]
            └── f [age=38]

        **Field-based comparisons**

        >>> results = tree.query('age >= 30 AND is_leaf OR node_name IN ["a"]')
        >>> [result.node_name for result in results]
        ['a', 'd', 'f']

        **Path-based conditions**

        >>> results = tree.query('path_name LIKE ".*/b/.*"')
        >>> [result.node_name for result in results]
        ['d', 'e', 'g', 'h']

        **Nested attribute conditions**

        >>> results = query_tree(root, "parent.is_root")
        >>> [result.node_name for result in results]
        ['b', 'c']

    Args:
        tree_node: tree to query
        query: query
        debug: if True, will print out the parsed query

    Returns:
        List of nodes that fulfil the condition of query
    """
    if not query.strip():
        raise ValueError("Please enter a valid query.")

    if debug:
        parser = Lark(QUERY_GRAMMAR, start="start", parser="lalr", debug=True)
    else:
        parser = Lark(
            QUERY_GRAMMAR, start="start", parser="lalr", transformer=QueryTransformer()
        )
    tree = parser.parse(query)
    if debug:
        print(tree)
        print(tree.pretty())

    func = QueryTransformer().transform(tree)
    return [node for node in iterators.preorder_iter(tree_node) if func(node)]

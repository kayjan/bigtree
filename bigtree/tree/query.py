import operator
from typing import Any, Callable, List, TypeVar

from bigtree.node import basenode
from bigtree.utils import exceptions, iterators

try:
    from lark import Lark, Token, Transformer
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    Lark = MagicMock()
    Token = MagicMock()
    Transformer = MagicMock()

__all__ = [
    "query_tree",
]

T = TypeVar("T", bound=basenode.BaseNode)


class QueryTransformer(Transformer):  # type: ignore
    # Tree is made up of Token
    # Token has .type and .value
    OPERATORS = {
        "==": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
        "contains": lambda a, b: b in a,
        "in": lambda a, b: a in b,
    }

    @staticmethod
    def or_clause(args: List[Callable[[T], bool]]) -> Callable[[T], bool]:
        return lambda node: any(cond(node) for cond in args)

    @staticmethod
    def and_clause(args: List[Callable[[T], bool]]) -> Callable[[T], bool]:
        return lambda node: all(cond(node) for cond in args)

    def comparison(self, args: List[Token]) -> Callable[[T], bool]:
        attr, op, value = args
        op_func = self.OPERATORS[op]
        if op in ("contains", "in"):
            return lambda node: op_func(attr(node) or "", value)
        return lambda node: op_func(attr(node), value)

    def unary(self, args: List[Token]) -> Callable[[T], bool]:
        attr = args[0]
        return lambda node: bool(attr(node))

    def not_comparison(self, args: List[Token]) -> Callable[[T], bool]:
        attr = args[0]
        return lambda node: not attr(node)

    @staticmethod
    def object_attr(args: List[Token]) -> Callable[[T], Any]:
        # e.g., ['parent', 'name'] => lambda node: node.parent.name
        def accessor(node: T) -> Any:
            obj = node
            for arg in args:
                obj = obj.get_attr(arg)
                if obj is None:
                    break
            return obj

        return accessor

    @staticmethod
    def list(args: List[Token]) -> Any:
        return list(args)

    @staticmethod
    def string(args: List[Token]) -> Any:
        return args[0][1:-1]

    @staticmethod
    def number(args: List[Token]) -> Any:
        val = args[0]
        try:
            return int(val)
        except ValueError:
            return float(val)


@exceptions.optional_dependencies_query
def query_tree(tree_node: T, query: str, debug: bool = False) -> List[T]:
    """Query tree using Tree Definition Language.

    - Supports clauses: AND, OR, NOT
    - Supports operation: ==, !=, >, <, >=, <=, contains, in
    - Note that string match in query must be in double quotes

    Examples:
        >>> from bigtree import Node, dict_to_tree, query_tree
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
        >>> root = dict_to_tree(paths)
        >>> root.show(all_attrs=True)
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        │       ├── g [age=10]
        │       └── h [age=6]
        └── c [age=60]
            └── f [age=38]

        **Field-based comparisons**

        >>> results = query_tree(root, 'age >= 30 AND is_leaf OR node_name in ["a"]')
        >>> [result.node_name for result in results]
        ['a', 'd', 'f']

        **Path-based conditions**

        >>> results = query_tree(root, 'path_name contains "/b/"')
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

    query_grammar = """
        ?start: expr

        ?expr: or_clause+
        ?or_clause: and_clause ("OR" and_clause)*
        ?and_clause: predicate ("AND" predicate)*

        ?predicate: "(" predicate ")"
               | comparison
               | unary
               | not_comparison

        comparison: object_attr OP _value
                | object_attr OP_CONTAINS string
                | object_attr OP_IN list
        unary: object_attr
        not_comparison: "NOT" predicate

        _attr: /[a-zA-Z_][a-zA-Z0-9_]*/
        object_attr: _attr ("." _attr)*
        list: "[" [_value ("," _value)*] "]"
        _value: string | number
        string: ESCAPED_STRING
        number: SIGNED_NUMBER

        OP: "==" | "!=" | ">" | "<" | ">=" | "<="
        OP_CONTAINS: "contains"
        OP_IN: "in"

        %import common.ESCAPED_STRING
        %import common.SIGNED_NUMBER
        %import common.WS
        %ignore WS
    """
    if debug:
        parser = Lark(query_grammar, start="start", parser="lalr", debug=True)
    else:
        parser = Lark(
            query_grammar, start="start", parser="lalr", transformer=QueryTransformer()
        )
    tree = parser.parse(query)
    if debug:
        print(tree)
        print(tree.pretty())

    func = QueryTransformer().transform(tree)
    return [node for node in iterators.preorder_iter(tree_node) if func(node)]

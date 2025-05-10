import operator
import re
from typing import Any, Callable, List, TypeVar

from bigtree.node import basenode

try:
    from lark import Token, Transformer
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    Token = MagicMock()
    Transformer = MagicMock()


T = TypeVar("T", bound=basenode.BaseNode)


QUERY_GRAMMAR = """
    ?start: expr

    ?expr: or_clause+
    ?or_clause: and_clause ("OR" and_clause)*
    ?and_clause: predicate ("AND" predicate)*

    ?predicate: "(" predicate ")"
           | condition
           | unary
           | not_predicate

    condition: object_attr OP _value
            | object_attr OP_IN list          -> string_condition
            | object_attr OP_LIKE string      -> string_condition
            | object_attr OP_BETWEEN number "AND" number  -> between_condition
    unary: object_attr
    not_predicate: "NOT" predicate

    _attr: /[a-zA-Z_][a-zA-Z0-9_]*/
    object_attr: _attr ("." _attr)*
    list: "[" [_value ("," _value)*] "]"
    _value: string | number
    string: ESCAPED_STRING
    number: SIGNED_NUMBER

    OP: "==" | "!=" | ">" | "<" | ">=" | "<="
    OP_IN: "IN"
    OP_LIKE: "LIKE"
    OP_BETWEEN: "BETWEEN"

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
"""


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
        "IN": lambda attr, value: attr in value,
        "LIKE": lambda attr, value: re.match(value, attr),
    }

    OPERATOR_BETWEEN = {
        "BETWEEN": lambda attr, value_from, value_to: value_from <= attr <= value_to
    }

    @staticmethod
    def or_clause(args: List[Callable[[T], bool]]) -> Callable[[T], bool]:
        return lambda node: any(cond(node) for cond in args)

    @staticmethod
    def and_clause(args: List[Callable[[T], bool]]) -> Callable[[T], bool]:
        return lambda node: all(cond(node) for cond in args)

    def condition(self, args: List[Token]) -> Callable[[T], bool]:
        attr, op, value = args
        op_func = self.OPERATORS[op]
        return lambda node: op_func(attr(node), value)

    def string_condition(self, args: List[Token]) -> Callable[[T], bool]:
        attr, op, value = args
        op_func = self.OPERATORS[op]
        return lambda node: op_func(attr(node) or "", value)

    def between_condition(self, args: List[Token]) -> Callable[[T], bool]:
        attr, op, value_from, value_to = args
        op_func = self.OPERATOR_BETWEEN[op]
        return lambda node: op_func(attr(node) or float("inf"), value_from, value_to)

    def unary(self, args: List[Token]) -> Callable[[T], bool]:
        attr = args[0]
        return lambda node: bool(attr(node))

    def not_predicate(self, args: List[Token]) -> Callable[[T], bool]:
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

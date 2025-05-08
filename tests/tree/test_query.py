import pytest

from bigtree.tree import query
from tests.test_constants import Constants


class TestQueryTree:
    @staticmethod
    def test_query_tree(tree_node):
        results = query.query_tree(tree_node, "age >= 30", debug=True)
        expected = ["a", "b", "d", "e", "c", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_empty_string(tree_node):
        with pytest.raises(ValueError) as exc_info:
            query.query_tree(tree_node, "")
        assert str(exc_info.value) == Constants.ERROR_QUERY_EMPTY

        with pytest.raises(ValueError) as exc_info:
            query.query_tree(tree_node, "  ")
        assert str(exc_info.value) == Constants.ERROR_QUERY_EMPTY

    @staticmethod
    def test_query_tree_object_attr_str(tree_node):
        results = query.query_tree(tree_node, 'parent.name == "b"')
        expected = ["d", "e"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_object_attr_int(tree_node):
        results = query.query_tree(tree_node, "parent.age == 65")
        expected = ["d", "e"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_unary_expr(tree_node):
        results = query.query_tree(tree_node, "is_leaf")
        expected = ["d", "g", "h", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_unary_expr_object_attr(tree_node):
        results = query.query_tree(tree_node, "parent.siblings")
        expected = ["d", "e", "g", "h", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_unary_expr_and(tree_node):
        results = query.query_tree(tree_node, "is_leaf AND siblings")
        expected = ["d", "g", "h"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_unary_expr_or(tree_node):
        results = query.query_tree(tree_node, "is_leaf OR is_root")
        expected = ["a", "d", "g", "h", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_op_equal_int(tree_node):
        results = query.query_tree(tree_node, "age == 65")
        expected = ["b"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_op_equal_float(tree_node):
        tree_node["b"].age = 65.5
        results = query.query_tree(tree_node, "age == 65.5")
        expected = ["b"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_op_contains(tree_node):
        tree_node["b"].parameter = "something"
        results = query.query_tree(tree_node, 'parameter contains "thing"')
        expected = ["b"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_op_in(tree_node):
        tree_node["b"].parameter = "something"
        tree_node["c"].parameter = "thing"
        tree_node["b"]["d"].parameter = "nothing"
        results = query.query_tree(tree_node, 'parameter in ["thing", "something"]')
        expected = ["b", "c"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_and_expr_multiple(tree_node):
        results = query.query_tree(tree_node, 'age == 40 AND name == "d" AND is_leaf')
        expected = ["d"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_or_expr_multiple(tree_node):
        results = query.query_tree(tree_node, 'age == 38 OR name == "d" OR is_root')
        expected = ["a", "d", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

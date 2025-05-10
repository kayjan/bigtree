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

    # object_attr
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
    def test_query_tree_object_attr_not(tree_node):
        results = query.query_tree(tree_node, "NOT parent.name")
        expected = ["a"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    # unary
    @staticmethod
    def test_query_tree_unary(tree_node):
        results = query.query_tree(tree_node, "is_leaf")
        expected = ["d", "g", "h", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_unary_object_attr(tree_node):
        results = query.query_tree(tree_node, "parent.siblings")
        expected = ["d", "e", "g", "h", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_unary_and(tree_node):
        results = query.query_tree(tree_node, "is_leaf AND siblings")
        expected = ["d", "g", "h"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_unary_or(tree_node):
        results = query.query_tree(tree_node, "is_leaf OR is_root")
        expected = ["a", "d", "g", "h", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_unary_not(tree_node):
        results = query.query_tree(tree_node, "NOT is_leaf")
        expected = ["a", "b", "e", "c"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    # condition
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
    def test_query_tree_op_not_equal(tree_node):
        results = query.query_tree(tree_node, "age != 65")
        expected = ["a", "d", "e", "g", "h", "c", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_op_more_than(tree_node):
        results = query.query_tree(tree_node, "age > 60")
        expected = ["a", "b"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_op_more_than_equal(tree_node):
        results = query.query_tree(tree_node, "age >= 60")
        expected = ["a", "b", "c"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_op_less_than(tree_node):
        results = query.query_tree(tree_node, "age < 60")
        expected = ["d", "e", "g", "h", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_op_less_than_equal(tree_node):
        results = query.query_tree(tree_node, "age <= 60")
        expected = ["d", "e", "g", "h", "c", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_op_in(tree_node):
        tree_node["b"].parameter = "something"
        tree_node["c"].parameter = "thing"
        tree_node["b"]["d"].parameter = "nothing"
        results = query.query_tree(tree_node, 'parameter IN ["thing", "something"]')
        expected = ["b", "c"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_op_in_int(tree_node):
        results = query.query_tree(tree_node, "age IN [90, 60]")
        expected = ["a", "c"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_op_in_not(tree_node):
        results = query.query_tree(tree_node, "NOT age IN [90, 60]")
        expected = ["b", "d", "e", "g", "h", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_like(tree_node):
        results = query.query_tree(tree_node, r'path_name LIKE ".*/b/.*"')
        expected = ["d", "e", "g", "h"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_like_parameter(tree_node):
        tree_node["b"].parameter = "something"
        tree_node["c"].parameter = "thing"
        tree_node["b"]["d"].parameter = "nothing"
        results = query.query_tree(tree_node, 'parameter LIKE ".+thing"')
        expected = ["b", "d"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_like_not(tree_node):
        tree_node["b"].parameter = "something"
        tree_node["c"].parameter = "thing"
        tree_node["b"]["d"].parameter = "nothing"
        results = query.query_tree(tree_node, 'NOT parameter LIKE ".+thing"')
        expected = ["a", "e", "g", "h", "c", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_between(tree_node):
        results = query.query_tree(tree_node, "age BETWEEN 6 AND 10")
        expected = ["g", "h"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    # and_clause
    @staticmethod
    def test_query_tree_and_clause_multiple(tree_node):
        results = query.query_tree(tree_node, 'age == 40 AND name == "d" AND is_leaf')
        expected = ["d"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_and_clause_multiple_parenthesis(tree_node):
        results = query.query_tree(
            tree_node, '(age == 40) AND (name == "d") AND is_leaf'
        )
        expected = ["d"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    # or_clause
    @staticmethod
    def test_query_tree_or_clause_multiple(tree_node):
        results = query.query_tree(tree_node, 'age == 38 OR name == "d" OR is_root')
        expected = ["a", "d", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

    @staticmethod
    def test_query_tree_or_clause_multiple_parenthesis(tree_node):
        results = query.query_tree(tree_node, '(age == 38) OR (name == "d") OR is_root')
        expected = ["a", "d", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"

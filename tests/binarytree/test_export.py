import pandas as pd
import polars as pl

from bigtree.tree import export
from tests.conftest import assert_print_statement
from tests.test_constants import Constants

LOCAL = Constants.LOCAL


class TestPrintTree:
    @staticmethod
    def test_print_tree(binarytree_node):
        expected_str = """1\n├── 2\n│   ├── 4\n│   │   └── 8\n│   └── 5\n└── 3\n    ├── 6\n    └── 7\n"""
        assert_print_statement(export.print_tree, expected_str, tree=binarytree_node)


class TestTreeToDataFrame:
    @staticmethod
    def test_tree_to_dataframe(binarytree_node):
        expected = pd.DataFrame(
            [
                ["/1", "1"],
                ["/1/2", "2"],
                ["/1/2/4", "4"],
                ["/1/2/4/8", "8"],
                ["/1/2/5", "5"],
                ["/1/3", "3"],
                ["/1/3/6", "6"],
                ["/1/3/7", "7"],
            ],
            columns=["path", "name"],
        )
        actual = export.tree_to_dataframe(binarytree_node)
        pd.testing.assert_frame_equal(expected, actual)


class TestTreeToPolars:
    @staticmethod
    def test_tree_to_polars(binarytree_node):
        expected = pl.DataFrame(
            [
                ["/1", "1"],
                ["/1/2", "2"],
                ["/1/2/4", "4"],
                ["/1/2/4/8", "8"],
                ["/1/2/5", "5"],
                ["/1/3", "3"],
                ["/1/3/6", "6"],
                ["/1/3/7", "7"],
            ],
            schema=["path", "name"],
        )
        actual = export.tree_to_polars(binarytree_node)
        assert expected.equals(actual)


class TestTreeToDict:
    @staticmethod
    def test_tree_to_dict(binarytree_node):
        expected = {
            "/1": {"name": "1"},
            "/1/2": {"name": "2"},
            "/1/2/4": {"name": "4"},
            "/1/2/4/8": {"name": "8"},
            "/1/2/5": {"name": "5"},
            "/1/3": {"name": "3"},
            "/1/3/6": {"name": "6"},
            "/1/3/7": {"name": "7"},
        }
        actual = export.tree_to_dict(binarytree_node)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


class TestTreeToNestedDict:
    @staticmethod
    def test_tree_to_nested_dict(binarytree_node):
        expected = {
            "name": "1",
            "children": [
                {
                    "name": "2",
                    "children": [
                        {"name": "4", "children": [{"name": "8"}]},
                        {"name": "5"},
                    ],
                },
                {"name": "3", "children": [{"name": "6"}, {"name": "7"}]},
            ],
        }
        actual = export.tree_to_nested_dict(binarytree_node)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


class TestTreeToDot:
    @staticmethod
    def test_tree_to_dot(binarytree_node):
        graph = export.tree_to_dot(binarytree_node)
        expected = """strict digraph G {\nrankdir=TB;\n10 [label=1];\n20 [label=2];\n10 -> 20;\n40 [label=4];\n20 -> 40;\n80 [label=8];\n40 -> 80;\n50 [label=5];\n20 -> 50;\n30 [label=3];\n10 -> 30;\n60 [label=6];\n30 -> 60;\n70 [label=7];\n30 -> 70;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/binarytree.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"


class TestTreeToNewick:
    @staticmethod
    def test_tree_to_newick(binarytree_node):
        newick_str = export.tree_to_newick(binarytree_node)
        expected_str = """(((,8)4,5)2,(6,7)3)1"""
        assert newick_str == expected_str

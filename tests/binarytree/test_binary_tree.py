import unittest

import pandas as pd
import polars as pl

from bigtree.binarytree.binarytree import BinaryTree
from bigtree.node import node
from tests.conftest import assert_print_statement
from tests.node.test_binarynode import assert_binarytree_structure_root2
from tests.test_constants import Constants

LOCAL = Constants.LOCAL


class TestBinaryTreeConstruct(unittest.TestCase):
    @staticmethod
    def test_from_heapq_list():
        nums_list = [1, 2, 3, 4, 5, 6, 7, 8]
        tree = BinaryTree.from_heapq_list(nums_list)
        assert_binarytree_structure_root2(tree.node)

    @staticmethod
    def test_from_list():
        path_list = ["1/2/4/8", "1/2/5", "1/3/6", "1/3/7"]
        tree = BinaryTree.from_list(path_list)
        assert_binarytree_structure_root2(tree.node)

    @staticmethod
    def test_from_list_relation():
        relations = [
            ("1", "2"),
            ("1", "3"),
            ("2", "4"),
            ("2", "5"),
            ("3", "6"),
            ("3", "7"),
            ("4", "8"),
        ]
        tree = BinaryTree.from_list_relation(relations)
        assert_binarytree_structure_root2(tree.node)

    @staticmethod
    def test_from_dict():
        path_dict = {
            "1": {"age": 90},
            "1/2": {"age": 65},
            "1/3": {"age": 60},
            "1/2/4": {"age": 40},
            "1/2/5": {"age": 35},
            "1/3/6": {"age": 38},
            "1/3/7": {"age": 10},
            "1/2/4/8": {"age": 6},
        }
        tree = BinaryTree.from_dict(path_dict)
        assert_binarytree_structure_root2(tree.node)

    @staticmethod
    def test_from_nested_dict():
        path_dict = {
            "name": "1",
            "age": 90,
            "children": [
                {
                    "name": "2",
                    "age": 65,
                    "children": [
                        {"name": "4", "age": 40, "children": [{"name": "8", "age": 6}]},
                        {"name": "5", "age": 35},
                    ],
                },
                {
                    "name": "3",
                    "age": 60,
                    "children": [
                        {"name": "6", "age": 38},
                        {"name": "7", "age": 10},
                    ],
                },
            ],
        }
        tree = BinaryTree.from_nested_dict(path_dict)
        assert_binarytree_structure_root2(tree.node)

    @staticmethod
    def test_from_dataframe():
        path_data = pd.DataFrame(
            [
                ["1", 90],
                ["1/2", 65],
                ["1/3", 60],
                ["1/2/4", 40],
                ["1/2/5", 35],
                ["1/3/6", 38],
                ["1/3/7", 10],
                ["1/2/4/8", 6],
            ],
            columns=["PATH", "age"],
        )
        tree = BinaryTree.from_dataframe(path_data)
        assert_binarytree_structure_root2(tree.node)

    @staticmethod
    def test_from_dataframe_relation():
        relation_data = pd.DataFrame(
            [
                ["1", None, 90],
                ["2", "1", 65],
                ["3", "1", 60],
                ["4", "2", 40],
                ["5", "2", 35],
                ["6", "3", 38],
                ["7", "3", 10],
                ["8", "4", 6],
            ],
            columns=["child", "parent", "age"],
        )
        tree = BinaryTree.from_dataframe_relation(relation_data)
        assert_binarytree_structure_root2(tree.node)

    @staticmethod
    def test_from_polars():
        path_data = pl.DataFrame(
            [
                ["1", 90],
                ["1/2", 65],
                ["1/3", 60],
                ["1/2/4", 40],
                ["1/2/5", 35],
                ["1/3/6", 38],
                ["1/3/7", 10],
                ["1/2/4/8", 6],
            ],
            schema=["PATH", "age"],
        )
        tree = BinaryTree.from_polars(path_data)
        assert_binarytree_structure_root2(tree.node)

    @staticmethod
    def test_from_polars_relation():
        relation_data = pl.DataFrame(
            [
                ["1", None, 90],
                ["2", "1", 65],
                ["3", "1", 60],
                ["4", "2", 40],
                ["5", "2", 35],
                ["6", "3", 38],
                ["7", "3", 10],
                ["8", "4", 6],
            ],
            schema=["child", "parent", "age"],
        )
        tree = BinaryTree.from_polars_relation(relation_data)
        assert_binarytree_structure_root2(tree.node)


class TestBinaryTreeExport:
    @staticmethod
    def test_show(binarytree_tree):
        expected_str = (
            """1\n"""
            """├── 2\n"""
            """│   ├── 4\n"""
            """│   │   └── 8\n"""
            """│   └── 5\n"""
            """└── 3\n"""
            """    ├── 6\n"""
            """    └── 7\n"""
        )
        assert_print_statement(binarytree_tree.show, expected_str)

    @staticmethod
    def test_to_dataframe(binarytree_tree):
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
        actual = binarytree_tree.to_dataframe()
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_to_polars(binarytree_tree):
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
        actual = binarytree_tree.to_polars()
        assert expected.equals(actual)

    @staticmethod
    def test_to_dict(binarytree_tree):
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
        actual = binarytree_tree.to_dict()
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_to_nested_dict(binarytree_tree):
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
        actual = binarytree_tree.to_nested_dict()
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_to_nested_dict_key(binarytree_tree):
        expected = {
            "1": {
                "children": {
                    "2": {
                        "children": {
                            "4": {"children": {"8": {}}},
                            "5": {},
                        },
                    },
                    "3": {"children": {"6": {}, "7": {}}},
                },
            }
        }
        actual = binarytree_tree.to_nested_dict_key()
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_to_dot(binarytree_tree):
        graph = binarytree_tree.to_dot()
        expected = """strict digraph G {\nrankdir=TB;\n10 [label=1];\n20 [label=2];\n10 -> 20;\n40 [label=4];\n20 -> 40;\n80 [label=8];\n40 -> 80;\n50 [label=5];\n20 -> 50;\n30 [label=3];\n10 -> 30;\n60 [label=6];\n30 -> 60;\n70 [label=7];\n30 -> 70;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png(f"{Constants.LOCAL_FILE}/binarytree.test_to_dot.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_to_newick(binarytree_tree):
        newick_str = binarytree_tree.to_newick()
        expected_str = """(((,8)4,5)2,(6,7)3)1"""
        assert newick_str == expected_str


class TestBinaryTreeHelper:
    @staticmethod
    def test_clone(binarytree_tree):
        tree_clone = binarytree_tree.clone(node_type=node.Node)
        assert isinstance(tree_clone.node, node.Node), "Wrong type returned"
        expected_str = (
            "1\n"
            "├── 2\n"
            "│   ├── 4\n"
            "│   │   └── 8\n"
            "│   └── 5\n"
            "└── 3\n"
            "    ├── 6\n"
            "    └── 7\n"
        )
        assert_print_statement(tree_clone.show, expected_str)


class TestBinaryTreeIterators:
    @staticmethod
    def test_inorder_iter(binarytree_tree):
        expected = ["4", "8", "2", "5", "1", "6", "3", "7"]
        actual = [node.node_name for node in binarytree_tree.inorder_iter()]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

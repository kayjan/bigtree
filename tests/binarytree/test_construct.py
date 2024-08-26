import unittest

import pandas as pd
import polars as pl
import pytest

from bigtree.binarytree import construct as binarytree_construct
from bigtree.node import binarynode
from bigtree.tree import construct as tree_construct
from tests.node.test_binarynode import assert_binarytree_structure_root2
from tests.test_constants import Constants


class BinaryNodeA(binarynode.BinaryNode):
    pass


class TestListToBinaryTree(unittest.TestCase):
    def setUp(self):
        self.nums_list = [1, 2, 3, 4, 5, 6, 7, 8]

    def tearDown(self):
        self.nums_list = None

    def test_list_to_binarytree(self):
        root = binarytree_construct.list_to_binarytree(self.nums_list)
        assert_binarytree_structure_root2(root)

    def test_list_to_binarytree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            binarytree_construct.list_to_binarytree([])
        assert str(exc_info.value) == Constants.ERROR_BINARY_DAG_LIST_EMPTY.format(
            parameter="heapq_list"
        )

    def test_list_to_binarytree_node_type(self):
        root = binarytree_construct.list_to_binarytree(
            self.nums_list, node_type=BinaryNodeA
        )
        assert isinstance(root, BinaryNodeA), Constants.ERROR_CUSTOM_TYPE.format(
            type="BinaryNodeA"
        )
        assert_binarytree_structure_root2(root)


class TestListToTree(unittest.TestCase):
    def setUp(self):
        """
        Binary Tree should have structure
        1
        ├── 2
        │   ├── 4
        │   │   └── 8
        │   └── 5
        └── 3
            ├── 6
            └── 7
        """
        self.path_list = ["1/2/4/8", "1/2/5", "1/3/6", "1/3/7"]

    def tearDown(self):
        self.path_list = None

    def test_list_to_tree(self):
        root = tree_construct.list_to_tree(
            self.path_list, node_type=binarynode.BinaryNode
        )
        assert_binarytree_structure_root2(root)


class TestListToTreeByRelation(unittest.TestCase):
    def setUp(self):
        """
        Binary Tree should have structure
        1
        ├── 2
        │   ├── 4
        │   │   └── 8
        │   └── 5
        └── 3
            ├── 6
            └── 7
        """
        self.relations = [
            ("1", "2"),
            ("1", "3"),
            ("2", "4"),
            ("2", "5"),
            ("3", "6"),
            ("3", "7"),
            ("4", "8"),
        ]

    def tearDown(self):
        self.relations = None

    def test_list_to_tree_by_relation(self):
        root = tree_construct.list_to_tree_by_relation(
            self.relations, node_type=binarynode.BinaryNode
        )
        assert_binarytree_structure_root2(root)


class TestDictToTree(unittest.TestCase):
    def setUp(self):
        """
        Binary Tree should have structure
        1
        ├── 2
        │   ├── 4
        │   │   └── 8
        │   └── 5
        └── 3
            ├── 6
            └── 7
        """
        self.path_dict = {
            "1": {"age": 90},
            "1/2": {"age": 65},
            "1/3": {"age": 60},
            "1/2/4": {"age": 40},
            "1/2/5": {"age": 35},
            "1/3/6": {"age": 38},
            "1/3/7": {"age": 10},
            "1/2/4/8": {"age": 6},
        }

    def tearDown(self):
        self.path_dict = None

    def test_dict_to_tree(self):
        root = tree_construct.dict_to_tree(
            self.path_dict, node_type=binarynode.BinaryNode
        )
        assert_binarytree_structure_root2(root)


class TestNestedDictToTree(unittest.TestCase):
    def setUp(self):
        """
        Binary Tree should have structure
        1
        ├── 2
        │   ├── 4
        │   │   └── 8
        │   └── 5
        └── 3
            ├── 6
            └── 7
        """
        self.path_dict = {
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

    def tearDown(self):
        self.path_dict = None

    def test_nested_dict_to_tree(self):
        root = tree_construct.nested_dict_to_tree(
            self.path_dict, node_type=binarynode.BinaryNode
        )
        assert_binarytree_structure_root2(root)


class TestDataFrameToTree(unittest.TestCase):
    def setUp(self):
        """
        Binary Tree should have structure
        1
        ├── 2
        │   ├── 4
        │   │   └── 8
        │   └── 5
        └── 3
            ├── 6
            └── 7
        """
        self.path_data = pd.DataFrame(
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

    def tearDown(self):
        self.path_data = None

    def test_dataframe_to_tree(self):
        root = tree_construct.dataframe_to_tree(
            self.path_data, node_type=binarynode.BinaryNode
        )
        assert_binarytree_structure_root2(root)


class TestDataFrameToTreeByRelation(unittest.TestCase):
    def setUp(self):
        self.relation_data = pd.DataFrame(
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

    def tearDown(self):
        self.relation_data = None

    def test_dataframe_to_tree_by_relation(self):
        root = tree_construct.dataframe_to_tree_by_relation(
            self.relation_data, node_type=binarynode.BinaryNode
        )
        assert_binarytree_structure_root2(root)


class TestPolarsToTree(unittest.TestCase):
    def setUp(self):
        """
        Binary Tree should have structure
        1
        ├── 2
        │   ├── 4
        │   │   └── 8
        │   └── 5
        └── 3
            ├── 6
            └── 7
        """
        self.path_data = pl.DataFrame(
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

    def tearDown(self):
        self.path_data = None

    def test_polars_to_tree(self):
        root = tree_construct.polars_to_tree(
            self.path_data, node_type=binarynode.BinaryNode
        )
        assert_binarytree_structure_root2(root)


class TestPolarsToTreeByRelation(unittest.TestCase):
    def setUp(self):
        self.relation_data = pl.DataFrame(
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

    def tearDown(self):
        self.relation_data = None

    def test_polars_to_tree_by_relation(self):
        root = tree_construct.polars_to_tree_by_relation(
            self.relation_data, node_type=binarynode.BinaryNode
        )
        assert_binarytree_structure_root2(root)

import unittest

import pandas as pd
import pytest

from bigtree.dag.construct import dataframe_to_dag, dict_to_dag, list_to_dag
from bigtree.node.dagnode import DAGNode
from tests.node.test_dagnode import (
    assert_dag_structure_attr_root,
    assert_dag_structure_root,
)


class DAGNodeA(DAGNode):
    pass


class TestListToDAG(unittest.TestCase):
    def setUp(self):
        self.relations = [
            ("a", "c"),
            ("a", "d"),
            ("b", "c"),
            ("c", "d"),
            ("c", "f"),
            ("c", "g"),
            ("d", "e"),
            ("d", "f"),
            ("g", "h"),
        ]

    def tearDown(self):
        self.relations = None

    def test_list_to_dag(self):
        dag = list_to_dag(self.relations)
        assert_dag_structure_root(dag)

    def test_list_to_dag_node_type(self):
        dag = list_to_dag(self.relations, node_type=DAGNodeA)
        assert isinstance(dag, DAGNodeA), "Node type is not `DAGNodeA`"
        assert_dag_structure_root(dag)


class TestDictToDAG(unittest.TestCase):
    def setUp(self):
        self.relation_dict = {
            "a": {"age": 90},
            "b": {"age": 65},
            "c": {"parent": ["a", "b"], "age": 60},
            "d": {"parent": ["a", "c"], "age": 40},
            "e": {"parent": ["d"], "age": 35},
            "f": {"parent": ["c", "d"], "age": 38},
            "g": {"parent": ["c"], "age": 10},
            "h": {"parent": ["g"], "age": 6},
        }

    def tearDown(self):
        self.relation_dict = None

    def test_dict_to_dag(self):
        dag = dict_to_dag(self.relation_dict, parent_key="parent")
        assert_dag_structure_root(dag)
        assert_dag_structure_attr_root(dag)

    def test_dict_to_dag_empty(self):
        with pytest.raises(ValueError):
            dict_to_dag({})


class TestDataFrameToDAG(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", None, 65],
                ["c", "a", 60],
                ["c", "b", 60],
                ["d", "a", 40],
                ["d", "c", 40],
                ["e", "d", 35],
                ["f", "c", 38],
                ["f", "d", 38],
                ["g", "c", 10],
                ["h", "g", 6],
            ],
            columns=["child", "parent", "age"],
        )

    def tearDown(self):
        self.data = None

    def test_dataframe_to_dag(self):
        dag = dataframe_to_dag(self.data)
        assert_dag_structure_root(dag)
        assert_dag_structure_attr_root(dag)

    @staticmethod
    def test_dataframe_to_dag_change_order():
        data = pd.DataFrame(
            [
                ["h", "g", 6],
                ["g", "c", 10],
                ["f", "d", 38],
                ["f", "c", 38],
                ["e", "d", 35],
                ["d", "c", 40],
                ["d", "a", 40],
                ["c", "b", 60],
                ["c", "a", 60],
                ["a", None, 90],
                ["b", None, 65],
            ],
            columns=["child", "parent", "age"],
        )
        dag = dataframe_to_dag(data)
        assert_dag_structure_root(dag)
        assert_dag_structure_attr_root(dag)

    def test_dataframe_to_dag_child_col(self):
        dag = dataframe_to_dag(self.data, child_col="child")
        assert_dag_structure_root(dag)
        assert_dag_structure_attr_root(dag)

    def test_dataframe_to_dag_parent_col(self):
        dag = dataframe_to_dag(self.data, parent_col="parent")
        assert_dag_structure_root(dag)
        assert_dag_structure_attr_root(dag)

    def test_dataframe_to_dag_attribute_cols(self):
        dag = dataframe_to_dag(self.data, attribute_cols=["age"])
        assert_dag_structure_root(dag)
        assert_dag_structure_attr_root(dag)

    def test_dataframe_to_dag_empty_row(self):
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_dag(pd.DataFrame(columns=["child", "parent", "age"]))
        assert str(exc_info.value).startswith("Data does not contain any rows")

    def test_dataframe_to_dag_empty_col(self):
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_dag(pd.DataFrame())
        assert str(exc_info.value).startswith("Data does not contain any columns")

    @staticmethod
    def test_dataframe_to_dag_empty_child():
        data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", None, 65],
                ["c", "a", 60],
                [None, "b", 60],  # empty child
                ["d", "a", 40],
                ["d", "c", 40],
                ["e", "d", 35],
                ["f", "c", 38],
                ["f", "d", 38],
                ["g", "c", 10],
                ["h", "g", 6],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_dag(data)
        assert str(exc_info.value).startswith("Child name cannot be empty")

    @staticmethod
    def test_dataframe_to_dag_duplicate():
        data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", None, 65],
                ["c", "a", 60],
                ["c", "b", 40],  # duplicate, wrong
                ["d", "a", 40],
                ["d", "c", 40],
                ["e", "d", 35],
                ["f", "c", 38],
                ["f", "d", 38],
                ["g", "c", 10],
                ["h", "g", 6],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_dag(data)
        assert str(exc_info.value).startswith(
            "There exists duplicate child name with different attributes"
        )

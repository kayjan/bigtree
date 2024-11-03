import unittest

import pandas as pd
import pytest

from bigtree.dag import construct
from bigtree.node import dagnode
from tests.node.test_dagnode import (
    assert_dag_structure_root,
    assert_dag_structure_root_attr,
)
from tests.test_constants import Constants


class DAGNodeA(dagnode.DAGNode):
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
        dag = construct.list_to_dag(self.relations)
        assert_dag_structure_root(dag)

    def test_list_to_dag_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.list_to_dag([])
        assert str(exc_info.value) == Constants.ERROR_BINARY_DAG_LIST_EMPTY.format(
            parameter="relations"
        )

    def test_list_to_dag_node_type(self):
        dag = construct.list_to_dag(self.relations, node_type=DAGNodeA)
        assert isinstance(dag, DAGNodeA), Constants.ERROR_CUSTOM_TYPE.format(
            type="DAGNodeA"
        )
        assert_dag_structure_root(dag)


class TestDictToDAG(unittest.TestCase):
    def setUp(self):
        self.relation_dict = {
            "a": {"age": 90},
            "b": {"age": 65},
            "c": {"parents": ["a", "b"], "age": 60},
            "d": {"parents": ["a", "c"], "age": 40},
            "e": {"parents": ["d"], "age": 35},
            "f": {"parents": ["c", "d"], "age": 38},
            "g": {"parents": ["c"], "age": 10},
            "h": {"parents": ["g"], "age": 6},
        }

    def tearDown(self):
        self.relation_dict = None

    def test_dict_to_dag(self):
        dag = construct.dict_to_dag(self.relation_dict)
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

    def test_dict_to_dag_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.dict_to_dag({})
        assert str(exc_info.value) == Constants.ERROR_NODE_DICT_EMPTY.format(
            parameter="relation_attrs"
        )

    @staticmethod
    def test_dict_to_dag_parent_key_error():
        relation_dict = {
            "a": {"age": 90},
            "b": {"age": 65},
            "c": {"parent1": ["a", "b"], "age": 60},
            "d": {"parent1": ["a", "c"], "age": 40},
            "e": {"parent1": ["d"], "age": 35},
            "f": {"parent1": ["c", "d"], "age": 38},
            "g": {"parent1": ["c"], "age": 10},
            "h": {"parent1": ["g"], "age": 6},
        }
        with pytest.raises(ValueError) as exc_info:
            construct.dict_to_dag(relation_dict)
        assert str(exc_info.value) == Constants.ERROR_DAG_DICT_PARENT_KEY.format(
            parent_key="parents"
        )

    def test_dict_to_dag_parent_key_reserved_keyword_parents_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.dict_to_dag(self.relation_dict, parent_key="parent")
        assert str(exc_info.value) == Constants.ERROR_DAG_DICT_INVALID_KEY.format(
            parameter="parents"
        )

    @staticmethod
    def test_dict_to_dag_parent_key_reserved_keyword_parent_error():
        relation_dict = {
            "a": {"age": 90},
            "b": {"age": 65},
            "c": {"parent": ["a", "b"], "age": 60},
            "d": {"parent": ["a", "c"], "age": 40},
            "e": {"parent": ["d"], "age": 35},
            "f": {"parent": ["c", "d"], "age": 38},
            "g": {"parent": ["c"], "age": 10},
            "h": {"parent": ["g"], "age": 6},
        }
        with pytest.raises(ValueError) as exc_info:
            construct.dict_to_dag(relation_dict)
        assert str(exc_info.value) == Constants.ERROR_DAG_DICT_INVALID_KEY.format(
            parameter="parent"
        )

    def test_dict_to_dag_node_type(self):
        dag = construct.dict_to_dag(self.relation_dict, node_type=DAGNodeA)
        assert isinstance(dag, DAGNodeA), Constants.ERROR_CUSTOM_TYPE.format(
            type="DAGNodeA"
        )
        assert_dag_structure_root(dag)


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
        dag = construct.dataframe_to_dag(self.data)
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

    @staticmethod
    def test_dataframe_to_dag_reverse():
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
        dag = construct.dataframe_to_dag(data)
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

    @staticmethod
    def test_dataframe_to_dag_zero_attribute():
        from bigtree.utils.iterators import dag_iterator

        data = pd.DataFrame(
            [
                ["a", None, 0],
                ["b", None, None],
                ["c", "a", -1],
                ["c", "b", -1],
                ["d", "a", 40],
                ["d", "c", 40],
                ["e", "d", 35],
                ["f", "c", 38],
                ["f", "d", 38],
                ["g", "c", 10],
                ["h", "g", 6],
            ],
            columns=["child", "parent", "value"],
        )
        dag = construct.dataframe_to_dag(data)
        assert_dag_structure_root(dag)
        for parent, _ in dag_iterator(dag):
            if parent.node_name == "a":
                assert hasattr(
                    parent, "value"
                ), "Check a attribute, expected value attribute"
                assert parent.value == 0, "Check a value, expected 0"
            elif parent.node_name == "b":
                assert not hasattr(
                    parent, "value"
                ), "Check b attribute, expected no value attribute"
            elif parent.node_name == "c":
                assert parent.value == -1, "Check c value, expected -1"

    def test_dataframe_to_dag_empty_row_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.dataframe_to_dag(pd.DataFrame(columns=["child", "parent", "age"]))
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    def test_dataframe_to_dag_empty_col_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.dataframe_to_dag(pd.DataFrame())
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_dataframe_to_dag_child_col(self):
        dag = construct.dataframe_to_dag(self.data, child_col="child")
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

    def test_dataframe_to_dag_child_col_error(self):
        child_col = "child2"
        with pytest.raises(ValueError) as exc_info:
            construct.dataframe_to_dag(self.data, child_col=child_col)
        assert str(exc_info.value) == Constants.ERROR_DAG_DATAFRAME_CHILD_COL.format(
            child_col=child_col
        )

    def test_dataframe_to_dag_parent_col(self):
        dag = construct.dataframe_to_dag(self.data, parent_col="parent")
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

    def test_dataframe_to_dag_parent_col_error(self):
        parent_col = "parent2"
        with pytest.raises(ValueError) as exc_info:
            construct.dataframe_to_dag(self.data, parent_col=parent_col)
        assert str(exc_info.value) == Constants.ERROR_DAG_DATAFRAME_PARENT_COL.format(
            parent_col=parent_col
        )

    @staticmethod
    def test_dataframe_to_dag_parent_col_reserved_keyword_parents_error():
        data = pd.DataFrame(
            [
                ["h", "g", "a", 6],
                ["g", "c", "a", 10],
                ["f", "d", "a", 38],
                ["f", "c", "a", 38],
                ["e", "d", "a", 35],
                ["d", "c", "a", 40],
                ["d", "a", "a", 40],
                ["c", "b", "a", 60],
                ["c", "a", "a", 60],
                ["a", None, None, 90],
                ["b", None, None, 65],
            ],
            columns=["child", "parent", "parents", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            construct.dataframe_to_dag(data, parent_col="parent")
        assert str(exc_info.value) == Constants.ERROR_DAG_DICT_INVALID_KEY.format(
            parameter="parents"
        )

    @staticmethod
    def test_dataframe_to_dag_parent_col_reserved_keyword_parent_error():
        data = pd.DataFrame(
            [
                ["h", "g", "a", 6],
                ["g", "c", "a", 10],
                ["f", "d", "a", 38],
                ["f", "c", "a", 38],
                ["e", "d", "a", 35],
                ["d", "c", "a", 40],
                ["d", "a", "a", 40],
                ["c", "b", "a", 60],
                ["c", "a", "a", 60],
                ["a", None, None, 90],
                ["b", None, None, 65],
            ],
            columns=["child", "parent", "parents", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            construct.dataframe_to_dag(data, parent_col="parents")
        assert str(exc_info.value) == Constants.ERROR_DAG_DICT_INVALID_KEY.format(
            parameter="parent"
        )

    def test_dataframe_to_dag_attribute_cols(self):
        dag = construct.dataframe_to_dag(self.data, attribute_cols=["age"])
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

    def test_dataframe_to_dag_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(KeyError):
            construct.dataframe_to_dag(self.data, attribute_cols=attribute_cols)

    @staticmethod
    def test_dataframe_to_dag_empty_child_error():
        child_col = "child"
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
            columns=[child_col, "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            construct.dataframe_to_dag(data)
        assert str(exc_info.value) == Constants.ERROR_DAG_DATAFRAME_EMPTY_CHILD.format(
            child_col=child_col
        )

    @staticmethod
    def test_dataframe_to_dag_ignore_name_col():
        data = pd.DataFrame(
            [
                ["a", None, 90, "a1"],
                ["b", None, 65, "b1"],
                ["c", "a", 60, "c1"],
                ["c", "b", 60, "c1"],
                ["d", "a", 40, "d1"],
                ["d", "c", 40, "d1"],
                ["e", "d", 35, "e1"],
                ["f", "c", 38, "f1"],
                ["f", "d", 38, "f1"],
                ["g", "c", 10, "g1"],
                ["h", "g", 6, "h1"],
            ],
            columns=["child", "parent", "age", "name"],
        )
        dag = construct.dataframe_to_dag(data)
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

    @staticmethod
    def test_dataframe_to_dag_ignore_non_attribute_cols():
        data = pd.DataFrame(
            [
                ["a", None, 90, "a1"],
                ["b", None, 65, "b1"],
                ["c", "a", 60, "c1"],
                ["c", "b", 60, "c1"],
                ["d", "a", 40, "d1"],
                ["d", "c", 40, "d1"],
                ["e", "d", 35, "e1"],
                ["f", "c", 38, "f1"],
                ["f", "d", 38, "f1"],
                ["g", "c", 10, "g1"],
                ["h", "g", 6, "h1"],
            ],
            columns=["child", "parent", "age", "name2"],
        )
        dag = construct.dataframe_to_dag(
            data, child_col="child", parent_col="parent", attribute_cols=["age"]
        )
        assert not dag.get_attr("name2")
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

    @staticmethod
    def test_dataframe_to_dag_node_empty_attribute():
        data = pd.DataFrame(
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
                ["g", "c", None],
                ["h", "g", 6],
            ],
            columns=["child", "parent", "age"],
        )
        dag = construct.dataframe_to_dag(data)
        assert not dag.get_attr("age")
        dag.set_attrs({"age": 10})
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

    @staticmethod
    def test_dataframe_to_dag_duplicate_data():
        data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", None, 65],
                ["c", "a", 60],
                ["c", "b", 60],  # duplicate
                ["c", "b", 60],  # duplicate
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
        dag = construct.dataframe_to_dag(data)
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

    @staticmethod
    def test_dataframe_to_dag_duplicate_leaf_node_error():
        data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", None, 65],
                ["c", "a", 60],
                ["c", "b", 60],
                ["d", "a", 40],
                ["d", "c", 40],
                ["e", "d", 35],
                ["f", "c", 38],
                ["f", "d", 40],  # duplicate
                ["g", "c", 10],
                ["h", "g", 6],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            construct.dataframe_to_dag(data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_DAG_DATAFRAME_DUPLICATE_PARENT
        )

    @staticmethod
    def test_dataframe_to_dag_duplicate_intermediate_node_error():
        data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", None, 65],
                ["c", "a", 60],
                ["c", "b", 40],  # duplicate
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
            construct.dataframe_to_dag(data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_DAG_DATAFRAME_DUPLICATE_PARENT
        )

    def test_dataframe_to_dag_node_type(self):
        dag = construct.dataframe_to_dag(self.data, node_type=DAGNodeA)
        assert isinstance(dag, DAGNodeA), Constants.ERROR_CUSTOM_TYPE.format(
            type="DAGNodeA"
        )
        assert_dag_structure_root(dag)

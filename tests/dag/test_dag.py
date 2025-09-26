import unittest

import pandas as pd

from bigtree.dag.dag import DAG
from tests.conftest import assert_print_statement
from tests.node.test_dagnode import (
    assert_dag_structure_root,
    assert_dag_structure_root_attr,
)
from tests.test_constants import Constants

LOCAL = Constants.LOCAL


class TestDAG:
    @staticmethod
    def test_tree_magic_methods(dag_dag):
        # Test __repr__
        assert_print_statement(print, "DAG(a, age=90)\n", dag_dag)
        assert_print_statement(print, "DAG(c, age=60)\n", dag_dag["c"])

        # Test __copy__, __getitem__, __delitem__
        import copy

        dag_deep_copy = dag_dag.copy()
        dag_shallow_copy = copy.copy(dag_dag)
        del dag_dag["c"]
        del dag_dag["something"]
        assert len(list(dag_dag.iterate())) == 8
        assert len(list(dag_shallow_copy.iterate())) == 8
        assert len(list(dag_deep_copy.iterate())) == 9


class TestDAGConstruct(unittest.TestCase):
    @staticmethod
    def test_from_list():
        relations = [
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
        dag = DAG.from_list(relations)
        assert_dag_structure_root(dag.dag)

    @staticmethod
    def test_from_dict():
        relation_dict = {
            "a": {"age": 90},
            "b": {"age": 65},
            "c": {"parents": ["a", "b"], "age": 60},
            "d": {"parents": ["a", "c"], "age": 40},
            "e": {"parents": ["d"], "age": 35},
            "f": {"parents": ["c", "d"], "age": 38},
            "g": {"parents": ["c"], "age": 10},
            "h": {"parents": ["g"], "age": 6},
        }
        dag = DAG.from_dict(relation_dict)
        assert_dag_structure_root(dag.dag)
        assert_dag_structure_root_attr(dag.dag)

    @staticmethod
    def test_from_dataframe():
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
                ["g", "c", 10],
                ["h", "g", 6],
            ],
            columns=["child", "parent", "age"],
        )
        dag = DAG.from_dataframe(data)
        assert_dag_structure_root(dag.dag)
        assert_dag_structure_root_attr(dag.dag)


class TestDAGExport:
    @staticmethod
    def test_to_list(dag_dag):
        expected = [
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
        actual = dag_dag.to_list()
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_to_dict(dag_dag):
        expected = {
            "a": {},
            "c": {"parents": ["a", "b"]},
            "d": {"parents": ["a", "c"]},
            "b": {},
            "f": {"parents": ["c", "d"]},
            "g": {"parents": ["c"]},
            "e": {"parents": ["d"]},
            "h": {"parents": ["g"]},
        }
        actual = dag_dag.to_dict()
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_to_dataframe(dag_dag):
        expected = pd.DataFrame(
            [
                ["a", None],
                ["c", "a"],
                ["d", "a"],
                ["b", None],
                ["c", "b"],
                ["d", "c"],
                ["f", "c"],
                ["g", "c"],
                ["e", "d"],
                ["f", "d"],
                ["h", "g"],
            ],
            columns=["name", "parent"],
        )
        actual = dag_dag.to_dataframe()
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_to_dot(dag_dag):
        graph = dag_dag.to_dot()
        expected = """strict digraph G {\na [label=a];\nc [label=c];\na -> c;\nd [label=d];\na -> d;\nc [label=c];\na [label=a];\na -> c;\nb [label=b];\nb -> c;\nd [label=d];\nc -> d;\nf [label=f];\nc -> f;\ng [label=g];\nc -> g;\nd [label=d];\na [label=a];\na -> d;\nc [label=c];\nc -> d;\ne [label=e];\nd -> e;\nf [label=f];\nd -> f;\ne [label=e];\nd [label=d];\nd -> e;\nf [label=f];\nc [label=c];\nc -> f;\nd [label=d];\nd -> f;\ng [label=g];\nc [label=c];\nc -> g;\nh [label=h];\ng -> h;\nh [label=h];\ng [label=g];\ng -> h;\nb [label=b];\nc [label=c];\nb -> c;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png(f"{Constants.LOCAL_FILE}/dag.test_to_dot.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"


class TestDAGIterator:
    @staticmethod
    def test_iterate(dag_dag):
        expected = [
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
        actual = [
            (parent.node_name, child.node_name) for parent, child in dag_dag.iterate()
        ]
        len_expected = 9
        len_actual = len(actual)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"
        assert (
            len_expected == len_actual
        ), f"Expected\n{len_expected}\nReceived\n{len_actual}"

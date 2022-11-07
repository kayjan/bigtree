import pandas as pd
import pytest

from bigtree import (
    dag_to_dataframe,
    dag_to_dict,
    dag_to_dot,
    dag_to_list,
    dataframe_to_dag,
    dict_to_dag,
    list_to_dag,
)
from tests.node.test_dagnode import (
    assert_dag_structure_attr_root,
    assert_dag_structure_root,
)


class TestDAGToList:
    @staticmethod
    def test_dag_to_list(dag_node):
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
        actual = dag_to_list(dag_node)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

        dag = list_to_dag(actual)
        assert_dag_structure_root(dag)


class TestDAGToDict:
    @staticmethod
    def test_dag_to_dict(dag_node):
        expected = {
            "a": {"age": 90},
            "c": {"parents": ["a", "b"], "age": 60},
            "d": {"parents": ["a", "c"], "age": 40},
            "b": {"age": 65},
            "f": {"parents": ["c", "d"], "age": 38},
            "g": {"parents": ["c"], "age": 10},
            "e": {"parents": ["d"], "age": 35},
            "h": {"parents": ["g"], "age": 6},
        }
        actual = dag_to_dict(dag_node, all_attrs=True)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

        dag = dict_to_dag(actual)
        assert_dag_structure_root(dag)
        assert_dag_structure_attr_root(dag)

    @staticmethod
    def test_dag_to_dict_attr_dict(dag_node):
        expected = {
            "a": {"AGE": 90},
            "c": {"PARENTS": ["a", "b"], "AGE": 60},
            "d": {"PARENTS": ["a", "c"], "AGE": 40},
            "b": {"AGE": 65},
            "f": {"PARENTS": ["c", "d"], "AGE": 38},
            "g": {"PARENTS": ["c"], "AGE": 10},
            "e": {"PARENTS": ["d"], "AGE": 35},
            "h": {"PARENTS": ["g"], "AGE": 6},
        }
        actual = dag_to_dict(dag_node, parent_key="PARENTS", attr_dict={"age": "AGE"})
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"


class TestDAGToDataFrame:
    @staticmethod
    def test_dag_to_dataframe(dag_node):
        expected = pd.DataFrame(
            [
                ["a", None, 90],
                ["c", "a", 60],
                ["d", "a", 40],
                ["b", None, 65],
                ["c", "b", 60],
                ["d", "c", 40],
                ["f", "c", 38],
                ["g", "c", 10],
                ["e", "d", 35],
                ["f", "d", 38],
                ["h", "g", 6],
            ],
            columns=["name", "parent", "age"],
        )
        actual = dag_to_dataframe(dag_node, all_attrs=True)
        pd.testing.assert_frame_equal(expected, actual)

        dag = dataframe_to_dag(actual)
        assert_dag_structure_root(dag)
        assert_dag_structure_attr_root(dag)

    @staticmethod
    def test_dag_to_dataframe_attr_dict(dag_node):
        expected = pd.DataFrame(
            [
                ["a", None, 90],
                ["c", "a", 60],
                ["d", "a", 40],
                ["b", None, 65],
                ["c", "b", 60],
                ["d", "c", 40],
                ["f", "c", 38],
                ["g", "c", 10],
                ["e", "d", 35],
                ["f", "d", 38],
                ["h", "g", 6],
            ],
            columns=["NAME", "PARENT", "AGE"],
        )
        actual = dag_to_dataframe(
            dag_node, name_col="NAME", parent_col="PARENT", attr_dict={"age": "AGE"}
        )
        pd.testing.assert_frame_equal(expected, actual)


class TestDAGToDot:
    @staticmethod
    def test_dag_to_dot(dag_node):
        graph = dag_to_dot(dag_node)
        expected = """strict digraph G {\na [label=a];\nc [label=c];\na -> c;\nd [label=d];\na -> d;\nc [label=c];\na [label=a];\na -> c;\nb [label=b];\nb -> c;\nd [label=d];\nc -> d;\nf [label=f];\nc -> f;\ng [label=g];\nc -> g;\nd [label=d];\na [label=a];\na -> d;\nc [label=c];\nc -> d;\ne [label=e];\nd -> e;\nf [label=f];\nd -> f;\ne [label=e];\nd [label=d];\nd -> e;\nf [label=f];\nc [label=c];\nc -> f;\nd [label=d];\nd -> f;\ng [label=g];\nc [label=c];\nc -> g;\nh [label=h];\ng -> h;\nh [label=h];\ng [label=g];\ng -> h;\nb [label=b];\nc [label=c];\nb -> c;\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/dag.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_dag_to_dot_from_child(dag_node_child):
        graph = dag_to_dot(dag_node_child)
        expected = """strict digraph G {\nf [label=f];\nc [label=c];\nc -> f;\nd [label=d];\nd -> f;\nc [label=c];\na [label=a];\na -> c;\nb [label=b];\nb -> c;\nd [label=d];\nc -> d;\nf [label=f];\nc -> f;\ng [label=g];\nc -> g;\nd [label=d];\na [label=a];\na -> d;\nc [label=c];\nc -> d;\ne [label=e];\nd -> e;\nf [label=f];\nd -> f;\ne [label=e];\nd [label=d];\nd -> e;\na [label=a];\nc [label=c];\na -> c;\nd [label=d];\na -> d;\ng [label=g];\nc [label=c];\nc -> g;\nh [label=h];\ng -> h;\nh [label=h];\ng [label=g];\ng -> h;\nb [label=b];\nc [label=c];\nb -> c;\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/dag_child.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_dag_to_dot_type_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            dag_to_dot(tree_node)
        assert str(exc_info.value).startswith("Tree should be of type `DAGNode`")

    @staticmethod
    def test_dag_to_dot_bg_color(dag_node):
        graph = dag_to_dot(dag_node, bgcolor="blue")
        expected = """strict digraph G {\nbgcolor=blue;\na [label=a];\nc [label=c];\na -> c;\nd [label=d];\na -> d;\nc [label=c];\na [label=a];\na -> c;\nb [label=b];\nb -> c;\nd [label=d];\nc -> d;\nf [label=f];\nc -> f;\ng [label=g];\nc -> g;\nd [label=d];\na [label=a];\na -> d;\nc [label=c];\nc -> d;\ne [label=e];\nd -> e;\nf [label=f];\nd -> f;\ne [label=e];\nd [label=d];\nd -> e;\nf [label=f];\nc [label=c];\nc -> f;\nd [label=d];\nd -> f;\ng [label=g];\nc [label=c];\nc -> g;\nh [label=h];\ng -> h;\nh [label=h];\ng [label=g];\ng -> h;\nb [label=b];\nc [label=c];\nb -> c;\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/dag_bg.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_dag_to_dot_fill_color(dag_node):
        graph = dag_to_dot(dag_node, node_colour="gold")
        expected = """strict digraph G {\na [fillcolor=gold, label=a, style=filled];\nc [fillcolor=gold, label=c, style=filled];\na -> c;\nd [fillcolor=gold, label=d, style=filled];\na -> d;\nc [fillcolor=gold, label=c, style=filled];\na [fillcolor=gold, label=a, style=filled];\na -> c;\nb [fillcolor=gold, label=b, style=filled];\nb -> c;\nd [fillcolor=gold, label=d, style=filled];\nc -> d;\nf [fillcolor=gold, label=f, style=filled];\nc -> f;\ng [fillcolor=gold, label=g, style=filled];\nc -> g;\nd [fillcolor=gold, label=d, style=filled];\na [fillcolor=gold, label=a, style=filled];\na -> d;\nc [fillcolor=gold, label=c, style=filled];\nc -> d;\ne [fillcolor=gold, label=e, style=filled];\nd -> e;\nf [fillcolor=gold, label=f, style=filled];\nd -> f;\ne [fillcolor=gold, label=e, style=filled];\nd [fillcolor=gold, label=d, style=filled];\nd -> e;\nf [fillcolor=gold, label=f, style=filled];\nc [fillcolor=gold, label=c, style=filled];\nc -> f;\nd [fillcolor=gold, label=d, style=filled];\nd -> f;\ng [fillcolor=gold, label=g, style=filled];\nc [fillcolor=gold, label=c, style=filled];\nc -> g;\nh [fillcolor=gold, label=h, style=filled];\ng -> h;\nh [fillcolor=gold, label=h, style=filled];\ng [fillcolor=gold, label=g, style=filled];\ng -> h;\nb [fillcolor=gold, label=b, style=filled];\nc [fillcolor=gold, label=c, style=filled];\nb -> c;\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/dag_fill.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_dag_to_dot_edge_colour(dag_node):
        graph = dag_to_dot(dag_node, edge_colour="red")
        expected = """strict digraph G {\na [label=a];\nc [label=c];\na -> c  [color=red];\nd [label=d];\na -> d  [color=red];\nc [label=c];\na [label=a];\na -> c  [color=red];\nb [label=b];\nb -> c  [color=red];\nd [label=d];\nc -> d  [color=red];\nf [label=f];\nc -> f  [color=red];\ng [label=g];\nc -> g  [color=red];\nd [label=d];\na [label=a];\na -> d  [color=red];\nc [label=c];\nc -> d  [color=red];\ne [label=e];\nd -> e  [color=red];\nf [label=f];\nd -> f  [color=red];\ne [label=e];\nd [label=d];\nd -> e  [color=red];\nf [label=f];\nc [label=c];\nc -> f  [color=red];\nd [label=d];\nd -> f  [color=red];\ng [label=g];\nc [label=c];\nc -> g  [color=red];\nh [label=h];\ng -> h  [color=red];\nh [label=h];\ng [label=g];\ng -> h  [color=red];\nb [label=b];\nc [label=c];\nb -> c  [color=red];\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/dag_edge.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_dag_to_dot_node_attr(dag_node_style):
        graph = dag_to_dot(dag_node_style, node_attr="node_style")
        expected = """strict digraph G {\na [fillcolor=gold, label=a, style=filled];\nc [fillcolor=gold, label=c, style=filled];\na -> c;\nd [fillcolor=gold, label=d, style=filled];\na -> d;\nc [fillcolor=blue, label=c, style=filled];\na [fillcolor=blue, label=a, style=filled];\na -> c;\nb [fillcolor=blue, label=b, style=filled];\nb -> c;\nd [fillcolor=blue, label=d, style=filled];\nc -> d;\nf [fillcolor=blue, label=f, style=filled];\nc -> f;\ng [fillcolor=blue, label=g, style=filled];\nc -> g;\nd [fillcolor=green, label=d, style=filled];\na [fillcolor=green, label=a, style=filled];\na -> d;\nc [fillcolor=green, label=c, style=filled];\nc -> d;\ne [fillcolor=green, label=e, style=filled];\nd -> e;\nf [fillcolor=green, label=f, style=filled];\nd -> f;\ne [fillcolor=green, label=e, style=filled];\nd [fillcolor=green, label=d, style=filled];\nd -> e;\nf [fillcolor=green, label=f, style=filled];\nc [fillcolor=green, label=c, style=filled];\nc -> f;\nd [fillcolor=green, label=d, style=filled];\nd -> f;\ng [fillcolor=red, label=g, style=filled];\nc [fillcolor=red, label=c, style=filled];\nc -> g;\nh [fillcolor=red, label=h, style=filled];\ng -> h;\nh [fillcolor=red, label=h, style=filled];\ng [fillcolor=red, label=g, style=filled];\ng -> h;\nb [fillcolor=blue, label=b, style=filled];\nc [fillcolor=blue, label=c, style=filled];\nb -> c;\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/dag_style.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

import pandas as pd
import pydot
import pytest

from bigtree.dag import construct, export
from tests.node.test_dagnode import (
    assert_dag_structure_root,
    assert_dag_structure_root_attr,
)
from tests.test_constants import Constants

LOCAL = Constants.LOCAL


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
        actual = export.dag_to_list(dag_node)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

        dag = construct.list_to_dag(actual)
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
        actual = export.dag_to_dict(dag_node, all_attrs=True)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

        dag = construct.dict_to_dag(actual)
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

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
        actual = export.dag_to_dict(
            dag_node, parent_key="PARENTS", attr_dict={"age": "AGE"}
        )
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


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
        actual = export.dag_to_dataframe(dag_node, all_attrs=True)
        pd.testing.assert_frame_equal(expected, actual)

        dag = construct.dataframe_to_dag(actual)
        assert_dag_structure_root(dag)
        assert_dag_structure_root_attr(dag)

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
        actual = export.dag_to_dataframe(
            dag_node, name_col="NAME", parent_col="PARENT", attr_dict={"age": "AGE"}
        )
        pd.testing.assert_frame_equal(expected, actual)


class TestDAGToDot:
    @staticmethod
    def test_dag_to_dot(dag_node):
        graph = export.dag_to_dot(dag_node)
        expected = """strict digraph G {\na [label=a];\nc [label=c];\na -> c;\nd [label=d];\na -> d;\nc [label=c];\na [label=a];\na -> c;\nb [label=b];\nb -> c;\nd [label=d];\nc -> d;\nf [label=f];\nc -> f;\ng [label=g];\nc -> g;\nd [label=d];\na [label=a];\na -> d;\nc [label=c];\nc -> d;\ne [label=e];\nd -> e;\nf [label=f];\nd -> f;\ne [label=e];\nd [label=d];\nd -> e;\nf [label=f];\nc [label=c];\nc -> f;\nd [label=d];\nd -> f;\ng [label=g];\nc [label=c];\nc -> g;\nh [label=h];\ng -> h;\nh [label=h];\ng [label=g];\ng -> h;\nb [label=b];\nc [label=c];\nb -> c;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_dag_to_dot_multiple(dag_node, dag_node_plot):
        graph = export.dag_to_dot([dag_node, dag_node_plot])
        expected = """strict digraph G {\nrankdir=TB;\nc [label=c];\na [label=a];\na -> c;\nd [label=d];\na [label=a];\na -> d;\nc [label=c];\nb [label=b];\nb -> c;\nd [label=d];\nc [label=c];\nc -> d;\nf [label=f];\nc [label=c];\nc -> f;\ng [label=g];\nc [label=c];\nc -> g;\ne [label=e];\nd [label=d];\nd -> e;\nf [label=f];\nd [label=d];\nd -> f;\nh [label=h];\ng [label=g];\ng -> h;\ny [label=y];\nz [label=z];\nz -> y;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_multiple.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_dag_to_dot_from_child(dag_node_child):
        graph = export.dag_to_dot(dag_node_child)
        expected = """strict digraph G {\nf [label=f];\nc [label=c];\nc -> f;\nd [label=d];\nd -> f;\nc [label=c];\na [label=a];\na -> c;\nb [label=b];\nb -> c;\nd [label=d];\nc -> d;\nf [label=f];\nc -> f;\ng [label=g];\nc -> g;\nd [label=d];\na [label=a];\na -> d;\nc [label=c];\nc -> d;\ne [label=e];\nd -> e;\nf [label=f];\nd -> f;\ne [label=e];\nd [label=d];\nd -> e;\na [label=a];\nc [label=c];\na -> c;\nd [label=d];\na -> d;\ng [label=g];\nc [label=c];\nc -> g;\nh [label=h];\ng -> h;\nh [label=h];\ng [label=g];\ng -> h;\nb [label=b];\nc [label=c];\nb -> c;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_child.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_dag_to_dot_type_error(tree_node):
        with pytest.raises(TypeError) as exc_info:
            export.dag_to_dot(tree_node)
        assert str(exc_info.value) == Constants.ERROR_NODE_TYPE.format(type="DAGNode")

    @staticmethod
    def test_dag_to_dot_bg_colour(dag_node):
        graph = export.dag_to_dot(dag_node, bg_colour="blue")
        expected = """strict digraph G {\nbgcolor=blue;\na [label=a];\nc [label=c];\na -> c;\nd [label=d];\na -> d;\nc [label=c];\na [label=a];\na -> c;\nb [label=b];\nb -> c;\nd [label=d];\nc -> d;\nf [label=f];\nc -> f;\ng [label=g];\nc -> g;\nd [label=d];\na [label=a];\na -> d;\nc [label=c];\nc -> d;\ne [label=e];\nd -> e;\nf [label=f];\nd -> f;\ne [label=e];\nd [label=d];\nd -> e;\nf [label=f];\nc [label=c];\nc -> f;\nd [label=d];\nd -> f;\ng [label=g];\nc [label=c];\nc -> g;\nh [label=h];\ng -> h;\nh [label=h];\ng [label=g];\ng -> h;\nb [label=b];\nc [label=c];\nb -> c;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_bg_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ >= "3.0.0", reason="Results have different ordering"
    )
    def test_dag_to_dot_fill_colour(dag_node):
        graph = export.dag_to_dot(dag_node, node_colour="gold")
        expected = """strict digraph G {\na [fillcolor=gold, label=a, style=filled];\nc [fillcolor=gold, label=c, style=filled];\na -> c;\nd [fillcolor=gold, label=d, style=filled];\na -> d;\nc [fillcolor=gold, label=c, style=filled];\na [fillcolor=gold, label=a, style=filled];\na -> c;\nb [fillcolor=gold, label=b, style=filled];\nb -> c;\nd [fillcolor=gold, label=d, style=filled];\nc -> d;\nf [fillcolor=gold, label=f, style=filled];\nc -> f;\ng [fillcolor=gold, label=g, style=filled];\nc -> g;\nd [fillcolor=gold, label=d, style=filled];\na [fillcolor=gold, label=a, style=filled];\na -> d;\nc [fillcolor=gold, label=c, style=filled];\nc -> d;\ne [fillcolor=gold, label=e, style=filled];\nd -> e;\nf [fillcolor=gold, label=f, style=filled];\nd -> f;\ne [fillcolor=gold, label=e, style=filled];\nd [fillcolor=gold, label=d, style=filled];\nd -> e;\nf [fillcolor=gold, label=f, style=filled];\nc [fillcolor=gold, label=c, style=filled];\nc -> f;\nd [fillcolor=gold, label=d, style=filled];\nd -> f;\ng [fillcolor=gold, label=g, style=filled];\nc [fillcolor=gold, label=c, style=filled];\nc -> g;\nh [fillcolor=gold, label=h, style=filled];\ng -> h;\nh [fillcolor=gold, label=h, style=filled];\ng [fillcolor=gold, label=g, style=filled];\ng -> h;\nb [fillcolor=gold, label=b, style=filled];\nc [fillcolor=gold, label=c, style=filled];\nb -> c;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_fill_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ < "3.0.0",
        reason="Results have different ordering (new pydot)",
    )
    def test_dag_to_dot_fill_colour2(dag_node):
        graph = export.dag_to_dot(dag_node, node_colour="gold")
        expected = """strict digraph G {\nrankdir=TB;\nc [label=c, style=filled, fillcolor=gold];\na [label=a, style=filled, fillcolor=gold];\na -> c;\nd [label=d, style=filled, fillcolor=gold];\na [label=a, style=filled, fillcolor=gold];\na -> d;\nc [label=c, style=filled, fillcolor=gold];\nb [label=b, style=filled, fillcolor=gold];\nb -> c;\nd [label=d, style=filled, fillcolor=gold];\nc [label=c, style=filled, fillcolor=gold];\nc -> d;\nf [label=f, style=filled, fillcolor=gold];\nc [label=c, style=filled, fillcolor=gold];\nc -> f;\ng [label=g, style=filled, fillcolor=gold];\nc [label=c, style=filled, fillcolor=gold];\nc -> g;\ne [label=e, style=filled, fillcolor=gold];\nd [label=d, style=filled, fillcolor=gold];\nd -> e;\nf [label=f, style=filled, fillcolor=gold];\nd [label=d, style=filled, fillcolor=gold];\nd -> f;\nh [label=h, style=filled, fillcolor=gold];\ng [label=g, style=filled, fillcolor=gold];\ng -> h;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_fill_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ >= "3.0.0", reason="Results have different ordering"
    )
    def test_dag_to_dot_edge_colour(dag_node):
        graph = export.dag_to_dot(dag_node, edge_colour="red")
        expected = """strict digraph G {\na [label=a];\nc [label=c];\na -> c  [color=red];\nd [label=d];\na -> d  [color=red];\nc [label=c];\na [label=a];\na -> c  [color=red];\nb [label=b];\nb -> c  [color=red];\nd [label=d];\nc -> d  [color=red];\nf [label=f];\nc -> f  [color=red];\ng [label=g];\nc -> g  [color=red];\nd [label=d];\na [label=a];\na -> d  [color=red];\nc [label=c];\nc -> d  [color=red];\ne [label=e];\nd -> e  [color=red];\nf [label=f];\nd -> f  [color=red];\ne [label=e];\nd [label=d];\nd -> e  [color=red];\nf [label=f];\nc [label=c];\nc -> f  [color=red];\nd [label=d];\nd -> f  [color=red];\ng [label=g];\nc [label=c];\nc -> g  [color=red];\nh [label=h];\ng -> h  [color=red];\nh [label=h];\ng [label=g];\ng -> h  [color=red];\nb [label=b];\nc [label=c];\nb -> c  [color=red];\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_edge_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ < "3.0.0",
        reason="Results have different ordering (new pydot)",
    )
    def test_dag_to_dot_edge_colour2(dag_node):
        graph = export.dag_to_dot(dag_node, edge_colour="red")
        expected = """strict digraph G {\nrankdir=TB;\nc [label=c];\na [label=a];\na -> c [color=red];\nd [label=d];\na [label=a];\na -> d [color=red];\nc [label=c];\nb [label=b];\nb -> c [color=red];\nd [label=d];\nc [label=c];\nc -> d [color=red];\nf [label=f];\nc [label=c];\nc -> f [color=red];\ng [label=g];\nc [label=c];\nc -> g [color=red];\ne [label=e];\nd [label=d];\nd -> e [color=red];\nf [label=f];\nd [label=d];\nd -> f [color=red];\nh [label=h];\ng [label=g];\ng -> h [color=red];\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_edge_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_dag_to_dot_node_shape(dag_node):
        graph = export.dag_to_dot(dag_node, node_shape="triangle")
        expected = """strict digraph G {\nrankdir=TB;\nc [label=c, shape=triangle];\na [label=a, shape=triangle];\na -> c;\nd [label=d, shape=triangle];\na [label=a, shape=triangle];\na -> d;\nc [label=c, shape=triangle];\nb [label=b, shape=triangle];\nb -> c;\nd [label=d, shape=triangle];\nc [label=c, shape=triangle];\nc -> d;\nf [label=f, shape=triangle];\nc [label=c, shape=triangle];\nc -> f;\ng [label=g, shape=triangle];\nc [label=c, shape=triangle];\nc -> g;\ne [label=e, shape=triangle];\nd [label=d, shape=triangle];\nd -> e;\nf [label=f, shape=triangle];\nd [label=d, shape=triangle];\nd -> f;\nh [label=h, shape=triangle];\ng [label=g, shape=triangle];\ng -> h;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_node_shape.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ >= "3.0.0", reason="Results have different ordering"
    )
    def test_dag_to_dot_node_attr(dag_node_style):
        graph = export.dag_to_dot(dag_node_style, node_attr="node_style")
        expected = """strict digraph G {\na [fillcolor=gold, label=a, style=filled];\nc [fillcolor=gold, label=c, style=filled];\na -> c;\nd [fillcolor=gold, label=d, style=filled];\na -> d;\nc [fillcolor=blue, label=c, style=filled];\na [fillcolor=blue, label=a, style=filled];\na -> c;\nb [fillcolor=blue, label=b, style=filled];\nb -> c;\nd [fillcolor=blue, label=d, style=filled];\nc -> d;\nf [fillcolor=blue, label=f, style=filled];\nc -> f;\ng [fillcolor=blue, label=g, style=filled];\nc -> g;\nd [fillcolor=green, label=d, style=filled];\na [fillcolor=green, label=a, style=filled];\na -> d;\nc [fillcolor=green, label=c, style=filled];\nc -> d;\ne [fillcolor=green, label=e, style=filled];\nd -> e;\nf [fillcolor=green, label=f, style=filled];\nd -> f;\ne [fillcolor=green, label=e, style=filled];\nd [fillcolor=green, label=d, style=filled];\nd -> e;\nf [fillcolor=green, label=f, style=filled];\nc [fillcolor=green, label=c, style=filled];\nc -> f;\nd [fillcolor=green, label=d, style=filled];\nd -> f;\ng [fillcolor=red, label=g, style=filled];\nc [fillcolor=red, label=c, style=filled];\nc -> g;\nh [fillcolor=red, label=h, style=filled];\ng -> h;\nh [fillcolor=red, label=h, style=filled];\ng [fillcolor=red, label=g, style=filled];\ng -> h;\nb [fillcolor=blue, label=b, style=filled];\nc [fillcolor=blue, label=c, style=filled];\nb -> c;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_node_attr.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ < "3.0.0",
        reason="Results have different ordering (new pydot)",
    )
    def test_dag_to_dot_node_attr2(dag_node_style):
        graph = export.dag_to_dot(dag_node_style, node_attr="node_style")
        expected = """strict digraph G {\nrankdir=TB;\nc [label=c, style=filled, fillcolor=blue];\na [label=a, style=filled, fillcolor=gold];\na -> c;\nd [label=d, style=filled, fillcolor=green];\na [label=a, style=filled, fillcolor=gold];\na -> d;\nc [label=c, style=filled, fillcolor=blue];\nb [label=b, style=filled, fillcolor=blue];\nb -> c;\nd [label=d, style=filled, fillcolor=green];\nc [label=c, style=filled, fillcolor=blue];\nc -> d;\nf [label=f, style=filled, fillcolor=green];\nc [label=c, style=filled, fillcolor=blue];\nc -> f;\ng [label=g, style=filled, fillcolor=red];\nc [label=c, style=filled, fillcolor=blue];\nc -> g;\ne [label=e, style=filled, fillcolor=green];\nd [label=d, style=filled, fillcolor=green];\nd -> e;\nf [label=f, style=filled, fillcolor=green];\nd [label=d, style=filled, fillcolor=green];\nd -> f;\nh [label=h, style=filled, fillcolor=red];\ng [label=g, style=filled, fillcolor=red];\ng -> h;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_node_attr.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ >= "3.0.0", reason="Results have different ordering"
    )
    def test_dag_to_dot_edge_attr(dag_node_style):
        graph = export.dag_to_dot(dag_node_style, edge_attr="edge_style")
        expected = """strict digraph G {\nrankdir=TB;\nc [label=c];\na [label=a];\na -> c  [label=c, style=bold];\nd [label=d];\na [label=a];\na -> d  [label=1, style=bold];\nc [label=c];\nb [label=b];\nb -> c  [label=c, style=bold];\nd [label=d];\nc [label=c];\nc -> d  [label=1, style=bold];\nf [label=f];\nc [label=c];\nc -> f  [label=3, style=bold];\ng [label=g];\nc [label=c];\nc -> g  [label=4, style=bold];\ne [label=e];\nd [label=d];\nd -> e  [label=2, style=bold];\nf [label=f];\nd [label=d];\nd -> f  [label=3, style=bold];\nh [label=h];\ng [label=g];\ng -> h  [label=5, style=bold];\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_edge_attr.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ < "3.0.0",
        reason="Results have different ordering (new pydot)",
    )
    def test_dag_to_dot_edge_attr2(dag_node_style):
        graph = export.dag_to_dot(dag_node_style, edge_attr="edge_style")
        expected = """strict digraph G {\nrankdir=TB;\nc [label=c];\na [label=a];\na -> c [style=bold, label=c];\nd [label=d];\na [label=a];\na -> d [style=bold, label=1];\nc [label=c];\nb [label=b];\nb -> c [style=bold, label=c];\nd [label=d];\nc [label=c];\nc -> d [style=bold, label=1];\nf [label=f];\nc [label=c];\nc -> f [style=bold, label=3];\ng [label=g];\nc [label=c];\nc -> g [style=bold, label=4];\ne [label=e];\nd [label=d];\nd -> e [style=bold, label=2];\nf [label=f];\nd [label=d];\nd -> f [style=bold, label=3];\nh [label=h];\ng [label=g];\ng -> h [style=bold, label=5];\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_edge_attr.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ >= "3.0.0", reason="Results have different ordering"
    )
    def test_dag_to_dot_attr_override(dag_node):
        dag_node.children[0].set_attrs(
            {
                "node_style": {"style": "filled", "fillcolor": "blue"},
                "edge_style": {"style": "bold"},
            }
        )
        graph = export.dag_to_dot(
            dag_node, node_attr="node_style", edge_attr="edge_style"
        )
        expected = """strict digraph G {\nrankdir=TB;\nc [fillcolor=blue, label=c, style=filled];\na [label=a];\na -> c  [style=bold];\nd [label=d];\na [label=a];\na -> d;\nc [fillcolor=blue, label=c, style=filled];\nb [label=b];\nb -> c  [style=bold];\nd [label=d];\nc [fillcolor=blue, label=c, style=filled];\nc -> d;\nf [label=f];\nc [fillcolor=blue, label=c, style=filled];\nc -> f;\ng [label=g];\nc [fillcolor=blue, label=c, style=filled];\nc -> g;\ne [label=e];\nd [label=d];\nd -> e;\nf [label=f];\nd [label=d];\nd -> f;\nh [label=h];\ng [label=g];\ng -> h;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_attr_override.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ < "3.0.0",
        reason="Results have different ordering (new pydot)",
    )
    def test_dag_to_dot_attr_override2(dag_node):
        dag_node.children[0].set_attrs(
            {
                "node_style": {"style": "filled", "fillcolor": "blue"},
                "edge_style": {"style": "bold"},
            }
        )
        graph = export.dag_to_dot(
            dag_node, node_attr="node_style", edge_attr="edge_style"
        )
        expected = """strict digraph G {\nrankdir=TB;\nc [label=c, style=filled, fillcolor=blue];\na [label=a];\na -> c [style=bold];\nd [label=d];\na [label=a];\na -> d;\nc [label=c, style=filled, fillcolor=blue];\nb [label=b];\nb -> c [style=bold];\nd [label=d];\nc [label=c, style=filled, fillcolor=blue];\nc -> d;\nf [label=f];\nc [label=c, style=filled, fillcolor=blue];\nc -> f;\ng [label=g];\nc [label=c, style=filled, fillcolor=blue];\nc -> g;\ne [label=e];\nd [label=d];\nd -> e;\nf [label=f];\nd [label=d];\nd -> f;\nh [label=h];\ng [label=g];\ng -> h;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/dag_attr_override.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

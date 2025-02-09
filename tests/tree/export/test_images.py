import matplotlib as mpl
import pydot
import pytest

from bigtree.tree import export
from tests.test_constants import Constants

LOCAL = Constants.LOCAL


class TestTreeToDot:
    @staticmethod
    def test_tree_to_dot(tree_node):
        graph = export.tree_to_dot(tree_node)
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\n"
            "b0 [label=b];\n"
            "a0 -> b0;\n"
            "d0 [label=d];\n"
            "b0 -> d0;\n"
            "e0 [label=e];\n"
            "b0 -> e0;\n"
            "g0 [label=g];\n"
            "e0 -> g0;\n"
            "h0 [label=h];\n"
            "e0 -> h0;\n"
            "c0 [label=c];\n"
            "a0 -> c0;\n"
            "f0 [label=f];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_multiple(tree_node, tree_node_plot):
        graph = export.tree_to_dot([tree_node, tree_node_plot])
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\n"
            "b0 [label=b];\n"
            "a0 -> b0;\n"
            "d0 [label=d];\n"
            "b0 -> d0;\n"
            "e0 [label=e];\n"
            "b0 -> e0;\n"
            "g0 [label=g];\n"
            "e0 -> g0;\n"
            "h0 [label=h];\n"
            "e0 -> h0;\n"
            "c0 [label=c];\n"
            "a0 -> c0;\n"
            "f0 [label=f];\n"
            "c0 -> f0;\n"
            "z0 [label=z];\n"
            "y0 [label=y];\n"
            "z0 -> y0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_multiple.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_duplicate_names(tree_node_duplicate_names):
        graph = export.tree_to_dot(tree_node_duplicate_names)
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\n"
            "a1 [label=a];\n"
            "a0 -> a1;\n"
            "a2 [label=a];\n"
            "a1 -> a2;\n"
            "b0 [label=b];\n"
            "a1 -> b0;\n"
            "a3 [label=a];\n"
            "b0 -> a3;\n"
            "b1 [label=b];\n"
            "b0 -> b1;\n"
            "b2 [label=b];\n"
            "a0 -> b2;\n"
            "a4 [label=a];\n"
            "b2 -> a4;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_duplicate_names.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_type_error(dag_node):
        with pytest.raises(TypeError) as exc_info:
            export.tree_to_dot(dag_node)
        assert str(exc_info.value) == Constants.ERROR_NODE_TYPE.format(type="Node")

    @staticmethod
    def test_tree_to_dot_directed(tree_node):
        graph = export.tree_to_dot(tree_node, directed=False)
        expected = (
            "strict graph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\n"
            "b0 [label=b];\n"
            "a0 -- b0;\n"
            "d0 [label=d];\n"
            "b0 -- d0;\n"
            "e0 [label=e];\n"
            "b0 -- e0;\n"
            "g0 [label=g];\n"
            "e0 -- g0;\n"
            "h0 [label=h];\n"
            "e0 -- h0;\n"
            "c0 [label=c];\n"
            "a0 -- c0;\n"
            "f0 [label=f];\n"
            "c0 -- f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_undirected.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_bg_colour(tree_node):
        graph = export.tree_to_dot(tree_node, bg_colour="blue")
        expected = (
            "strict digraph G {\n"
            "bgcolor=blue;\n"
            "rankdir=TB;\na0 [label=a];\n"
            "b0 [label=b];\n"
            "a0 -> b0;\n"
            "d0 [label=d];\n"
            "b0 -> d0;\n"
            "e0 [label=e];\n"
            "b0 -> e0;\n"
            "g0 [label=g];\n"
            "e0 -> g0;\n"
            "h0 [label=h];\n"
            "e0 -> h0;\n"
            "c0 [label=c];\n"
            "a0 -> c0;\n"
            "f0 [label=f];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_bg_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ >= "3.0.0", reason="Results have different ordering"
    )
    def test_tree_to_dot_fill_colour(tree_node):
        graph = export.tree_to_dot(tree_node, node_colour="gold")
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [fillcolor=gold, label=a, style=filled];\n"
            "b0 [fillcolor=gold, label=b, style=filled];\n"
            "a0 -> b0;\n"
            "d0 [fillcolor=gold, label=d, style=filled];\n"
            "b0 -> d0;\n"
            "e0 [fillcolor=gold, label=e, style=filled];\n"
            "b0 -> e0;\n"
            "g0 [fillcolor=gold, label=g, style=filled];\n"
            "e0 -> g0;\n"
            "h0 [fillcolor=gold, label=h, style=filled];\n"
            "e0 -> h0;\n"
            "c0 [fillcolor=gold, label=c, style=filled];\n"
            "a0 -> c0;\n"
            "f0 [fillcolor=gold, label=f, style=filled];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_fill_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ < "3.0.0",
        reason="Results have different ordering (new pydot)",
    )
    def test_tree_to_dot_fill_colour2(tree_node):
        graph = export.tree_to_dot(tree_node, node_colour="gold")
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a, style=filled, fillcolor=gold];\n"
            "b0 [label=b, style=filled, fillcolor=gold];\n"
            "a0 -> b0;\n"
            "d0 [label=d, style=filled, fillcolor=gold];\n"
            "b0 -> d0;\n"
            "e0 [label=e, style=filled, fillcolor=gold];\n"
            "b0 -> e0;\n"
            "g0 [label=g, style=filled, fillcolor=gold];\n"
            "e0 -> g0;\n"
            "h0 [label=h, style=filled, fillcolor=gold];\n"
            "e0 -> h0;\n"
            "c0 [label=c, style=filled, fillcolor=gold];\n"
            "a0 -> c0;\n"
            "f0 [label=f, style=filled, fillcolor=gold];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_fill_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_edge_colour(tree_node):
        graph = export.tree_to_dot(tree_node, edge_colour="red")
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\n"
            "b0 [label=b];\n"
            "a0 -> b0  [color=red];\n"
            "d0 [label=d];\n"
            "b0 -> d0  [color=red];\n"
            "e0 [label=e];\n"
            "b0 -> e0  [color=red];\n"
            "g0 [label=g];\n"
            "e0 -> g0  [color=red];\n"
            "h0 [label=h];\n"
            "e0 -> h0  [color=red];\n"
            "c0 [label=c];\n"
            "a0 -> c0  [color=red];\n"
            "f0 [label=f];\n"
            "c0 -> f0  [color=red];\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_edge_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_node_shape(tree_node):
        graph = export.tree_to_dot(tree_node, node_shape="triangle")
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a, shape=triangle];\nb0 [label=b, shape=triangle];\n"
            "a0 -> b0;\n"
            "d0 [label=d, shape=triangle];\n"
            "b0 -> d0;\ne0 [label=e, shape=triangle];\n"
            "b0 -> e0;\n"
            "g0 [label=g, shape=triangle];\n"
            "e0 -> g0;\nh0 [label=h, shape=triangle];\n"
            "e0 -> h0;\n"
            "c0 [label=c, shape=triangle];\n"
            "a0 -> c0;\nf0 [label=f, shape=triangle];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_node_shape.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ >= "3.0.0", reason="Results have different ordering"
    )
    def test_tree_to_dot_node_attr(tree_node_style):
        graph = export.tree_to_dot(tree_node_style, node_attr="node_style")
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [fillcolor=gold, label=a, style=filled];\n"
            "b0 [fillcolor=blue, label=b, style=filled];\na0 -> b0;\n"
            "d0 [fillcolor=green, label=d, style=filled];\n"
            "b0 -> d0;\n"
            "g0 [fillcolor=red, label=g, style=filled];\n"
            "d0 -> g0;\n"
            "e0 [fillcolor=green, label=e, style=filled];\n"
            "b0 -> e0;\n"
            "h0 [fillcolor=red, label=h, style=filled];\n"
            "e0 -> h0;\n"
            "c0 [fillcolor=blue, label=c, style=filled];\n"
            "a0 -> c0;\n"
            "f0 [fillcolor=green, label=f, style=filled];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_node_attr.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ < "3.0.0",
        reason="Results have different ordering (new pydot)",
    )
    def test_tree_to_dot_node_attr2(tree_node_style):
        graph = export.tree_to_dot(tree_node_style, node_attr="node_style")
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a, style=filled, fillcolor=gold];\n"
            "b0 [label=b, style=filled, fillcolor=blue];\n"
            "a0 -> b0;\n"
            "d0 [label=d, style=filled, fillcolor=green];\n"
            "b0 -> d0;\n"
            "g0 [label=g, style=filled, fillcolor=red];\n"
            "d0 -> g0;\n"
            "e0 [label=e, style=filled, fillcolor=green];\n"
            "b0 -> e0;\n"
            "h0 [label=h, style=filled, fillcolor=red];\n"
            "e0 -> h0;\n"
            "c0 [label=c, style=filled, fillcolor=blue];\n"
            "a0 -> c0;\n"
            "f0 [label=f, style=filled, fillcolor=green];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_node_attr.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ >= "3.0.0", reason="Results have different ordering"
    )
    def test_tree_to_dot_node_attr_callable(tree_node_style_callable):
        def get_node_attr(node):
            if node.get_attr("style") and node.style == 1:
                return {"style": "filled", "fillcolor": "gold"}
            elif node.get_attr("style") and node.style == "two":
                return {"style": "filled", "fillcolor": "blue"}
            elif node.node_name in ["d", "e", "f"]:
                return {"style": "filled", "fillcolor": "green"}
            return {"style": "filled", "fillcolor": "red"}

        graph = export.tree_to_dot(tree_node_style_callable, node_attr=get_node_attr)
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [fillcolor=gold, label=a, style=filled];\n"
            "b0 [fillcolor=blue, label=b, style=filled];\n"
            "a0 -> b0;\n"
            "d0 [fillcolor=green, label=d, style=filled];\n"
            "b0 -> d0;\n"
            "g0 [fillcolor=red, label=g, style=filled];\n"
            "d0 -> g0;\n"
            "e0 [fillcolor=green, label=e, style=filled];\n"
            "b0 -> e0;\n"
            "h0 [fillcolor=red, label=h, style=filled];\n"
            "e0 -> h0;\n"
            "c0 [fillcolor=blue, label=c, style=filled];\n"
            "a0 -> c0;\n"
            "f0 [fillcolor=green, label=f, style=filled];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_node_attr_callable.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ < "3.0.0",
        reason="Results have different ordering (new pydot)",
    )
    def test_tree_to_dot_node_attr_callable2(tree_node_style_callable):
        def get_node_attr(node):
            if node.get_attr("style") and node.style == 1:
                return {"style": "filled", "fillcolor": "gold"}
            elif node.get_attr("style") and node.style == "two":
                return {"style": "filled", "fillcolor": "blue"}
            elif node.node_name in ["d", "e", "f"]:
                return {"style": "filled", "fillcolor": "green"}
            return {"style": "filled", "fillcolor": "red"}

        graph = export.tree_to_dot(tree_node_style_callable, node_attr=get_node_attr)
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a, style=filled, fillcolor=gold];\n"
            "b0 [label=b, style=filled, fillcolor=blue];\n"
            "a0 -> b0;\n"
            "d0 [label=d, style=filled, fillcolor=green];\n"
            "b0 -> d0;\n"
            "g0 [label=g, style=filled, fillcolor=red];\n"
            "d0 -> g0;\n"
            "e0 [label=e, style=filled, fillcolor=green];\n"
            "b0 -> e0;\n"
            "h0 [label=h, style=filled, fillcolor=red];\n"
            "e0 -> h0;\n"
            "c0 [label=c, style=filled, fillcolor=red];\n"
            "a0 -> c0;\n"
            "f0 [label=f, style=filled, fillcolor=green];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_node_attr_callable.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ >= "3.0.0", reason="Results have different ordering"
    )
    def test_tree_to_dot_edge_attr(tree_node_style):
        graph = export.tree_to_dot(tree_node_style, edge_attr="edge_style")
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\n"
            "b0 [label=b];\n"
            "a0 -> b0  [label=b, style=bold];\n"
            "d0 [label=d];\n"
            "b0 -> d0  [label=1, style=bold];\n"
            "g0 [label=g];\n"
            "d0 -> g0  [label=4, style=bold];\n"
            "e0 [label=e];\n"
            "b0 -> e0  [label=2, style=bold];\n"
            "h0 [label=h];\n"
            "e0 -> h0  [label=5, style=bold];\n"
            "c0 [label=c];\n"
            "a0 -> c0  [label=c, style=bold];\n"
            "f0 [label=f];\n"
            "c0 -> f0  [label=3, style=bold];\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_edge_attr.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ < "3.0.0",
        reason="Results have different ordering (new pydot)",
    )
    def test_tree_to_dot_edge_attr2(tree_node_style):
        graph = export.tree_to_dot(tree_node_style, edge_attr="edge_style")
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\n"
            "b0 [label=b];\n"
            "a0 -> b0 [style=bold, label=b];\n"
            "d0 [label=d];\n"
            "b0 -> d0 [style=bold, label=1];\n"
            "g0 [label=g];\n"
            "d0 -> g0 [style=bold, label=4];\n"
            "e0 [label=e];\n"
            "b0 -> e0 [style=bold, label=2];\n"
            "h0 [label=h];\n"
            "e0 -> h0 [style=bold, label=5];\n"
            "c0 [label=c];\n"
            "a0 -> c0 [style=bold, label=c];\n"
            "f0 [label=f];\n"
            "c0 -> f0 [style=bold, label=3];\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_edge_attr.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ >= "3.0.0", reason="Results have different ordering"
    )
    def test_tree_to_dot_edge_attr_callable(tree_node_style_callable):
        def get_edge_attr(node):
            if node.get_attr("style") and node.style == 1:
                return {"style": "bold", "label": "a"}
            elif node.get_attr("style") and node.style == "two":
                return {"style": "bold", "label": "b"}
            elif node.get_attr("style") and node.style == ("three"):
                return {"style": "bold", "label": "c"}
            elif node.node_name in ["d", "e", "f", "g", "h"]:
                return {
                    "style": "bold",
                    "label": ["d", "e", "f", "g", "h"].index(node.node_name) + 1,
                }
            raise Exception("Node with invalid edge_attr not covered")

        graph = export.tree_to_dot(tree_node_style_callable, edge_attr=get_edge_attr)
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\n"
            "b0 [label=b];\n"
            "a0 -> b0  [label=b, style=bold];\n"
            "d0 [label=d];\n"
            "b0 -> d0  [label=1, style=bold];\n"
            "g0 [label=g];\n"
            "d0 -> g0  [label=4, style=bold];\n"
            "e0 [label=e];\n"
            "b0 -> e0  [label=2, style=bold];\n"
            "h0 [label=h];\n"
            "e0 -> h0  [label=5, style=bold];\n"
            "c0 [label=c];\n"
            "a0 -> c0  [label=c, style=bold];\n"
            "f0 [label=f];\n"
            "c0 -> f0  [label=3, style=bold];\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_edge_attr_callable.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ < "3.0.0",
        reason="Results have different ordering (new pydot)",
    )
    def test_tree_to_dot_edge_attr_callable2(tree_node_style_callable):
        def get_edge_attr(node):
            if node.get_attr("style") and node.style == 1:
                return {"style": "bold", "label": "a"}
            elif node.get_attr("style") and node.style == "two":
                return {"style": "bold", "label": "b"}
            elif node.get_attr("style") and node.style == ("three"):
                return {"style": "bold", "label": "c"}
            elif node.node_name in ["d", "e", "f", "g", "h"]:
                return {
                    "style": "bold",
                    "label": ["d", "e", "f", "g", "h"].index(node.node_name) + 1,
                }
            raise Exception("Node with invalid edge_attr not covered")

        graph = export.tree_to_dot(tree_node_style_callable, edge_attr=get_edge_attr)
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\nb0 [label=b];\n"
            "a0 -> b0 [style=bold, label=b];\n"
            "d0 [label=d];\n"
            "b0 -> d0 [style=bold, label=1];\n"
            "g0 [label=g];\n"
            "d0 -> g0 [style=bold, label=4];\n"
            "e0 [label=e];\n"
            "b0 -> e0 [style=bold, label=2];\n"
            "h0 [label=h];\n"
            "e0 -> h0 [style=bold, label=5];\n"
            "c0 [label=c];\n"
            "a0 -> c0 [style=bold, label=c];\n"
            "f0 [label=f];\n"
            "c0 -> f0 [style=bold, label=3];\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_edge_attr_callable.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ >= "3.0.0", reason="Results have different ordering"
    )
    def test_tree_to_dot_attr_override(tree_node):
        tree_node.children[0].set_attrs(
            {
                "node_style": {"style": "filled", "fillcolor": "blue"},
                "edge_style": {"style": "bold"},
            }
        )
        graph = export.tree_to_dot(
            tree_node, node_attr="node_style", edge_attr="edge_style"
        )
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\n"
            "b0 [fillcolor=blue, label=b, style=filled];\n"
            "a0 -> b0  [style=bold];\n"
            "d0 [label=d];\n"
            "b0 -> d0;\n"
            "e0 [label=e];\n"
            "b0 -> e0;\n"
            "g0 [label=g];\n"
            "e0 -> g0;\n"
            "h0 [label=h];\n"
            "e0 -> h0;\n"
            "c0 [label=c];\n"
            "a0 -> c0;\n"
            "f0 [label=f];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_attr_override.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    @pytest.mark.skipif(
        pydot.__version__ < "3.0.0",
        reason="Results have different ordering (new pydot)",
    )
    def test_tree_to_dot_attr_override2(tree_node):
        tree_node.children[0].set_attrs(
            {
                "node_style": {"style": "filled", "fillcolor": "blue"},
                "edge_style": {"style": "bold"},
            }
        )
        graph = export.tree_to_dot(
            tree_node, node_attr="node_style", edge_attr="edge_style"
        )
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\n"
            "b0 [label=b, style=filled, fillcolor=blue];\n"
            "a0 -> b0 [style=bold];\n"
            "d0 [label=d];\n"
            "b0 -> d0;\n"
            "e0 [label=e];\nb0 -> e0;\n"
            "g0 [label=g];\n"
            "e0 -> g0;\nh0 [label=h];\n"
            "e0 -> h0;\n"
            "c0 [label=c];\na0 -> c0;\n"
            "f0 [label=f];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_attr_override.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"


class TestTreeToPillowGraph:
    @staticmethod
    def test_tree_to_pillow_graph(tree_node):
        pillow_image = export.tree_to_pillow_graph(tree_node)
        if LOCAL:
            pillow_image.save("tests/tree_pillow_graph.png")

    @staticmethod
    def test_tree_to_pillow_graph_multiline(tree_node):
        pillow_image = export.tree_to_pillow_graph(
            tree_node, node_content="{node_name}\nAge: {age}"
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_graph_multiline.png")

    @staticmethod
    def test_tree_to_pillow_graph_tb_margins(tree_node):
        pillow_image = export.tree_to_pillow_graph(
            tree_node, node_content="{node_name}\nAge: {age}", margin={"t": 60, "b": 60}
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_graph_tb_margins.png")

    @staticmethod
    def test_tree_to_pillow_graph_lr_margins(tree_node):
        pillow_image = export.tree_to_pillow_graph(
            tree_node, node_content="{node_name}\nAge: {age}", margin={"l": 60, "r": 60}
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_graph_lr_margins.png")

    @staticmethod
    def test_tree_to_pillow_graph_buffer(tree_node):
        pillow_image = export.tree_to_pillow_graph(
            tree_node,
            node_content="{node_name}\nAge: {age}",
            height_buffer=60,
            width_buffer=60,
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_graph_buffer.png")

    @staticmethod
    def test_tree_to_pillow_graph_bg_colour(tree_node):
        pillow_image = export.tree_to_pillow_graph(
            tree_node, node_content="{node_name}\nAge: {age}", bg_colour="beige"
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_graph_bg_colour.png")

    @staticmethod
    def test_tree_to_pillow_graph_rect_tb_margins(tree_node):
        pillow_image = export.tree_to_pillow_graph(
            tree_node,
            node_content="{node_name}\nAge: {age}",
            rect_margin={"t": 60, "b": 60},
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_graph_rect_tb_margins.png")

    @staticmethod
    def test_tree_to_pillow_graph_rect_lr_margins(tree_node):
        pillow_image = export.tree_to_pillow_graph(
            tree_node,
            node_content="{node_name}\nAge: {age}",
            rect_margin={"l": 60, "r": 60},
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_graph_rect_lr_margins.png")

    @staticmethod
    def test_tree_to_pillow_graph_rect_fill(tree_node):
        pillow_image = export.tree_to_pillow_graph(
            tree_node,
            node_content="{node_name}\nAge: {age}",
            rect_fill="beige",
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_graph_rect_fill.png")

    @staticmethod
    def test_tree_to_pillow_graph_rect_fill_cmap_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.tree_to_pillow_graph(
                tree_node,
                node_content="{node_name}\nAge: {age}",
                rect_fill=mpl.colormaps["RdBu"],
            )
        assert str(exc_info.value) == Constants.ERROR_NODE_EXPORT_PILLOW_CMAP

    @staticmethod
    def test_tree_to_pillow_graph_rect_fill_cmap(tree_node):
        pillow_image = export.tree_to_pillow_graph(
            tree_node,
            node_content="{node_name}\nAge: {age}",
            rect_fill=mpl.colormaps["RdBu"],
            rect_cmap_attr="age",
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_graph_rect_fill_cmap.png")

    @staticmethod
    def test_tree_to_pillow_graph_rect_width(tree_node):
        pillow_image = export.tree_to_pillow_graph(
            tree_node,
            node_content="{node_name}\nAge: {age}",
            rect_width=3,
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_graph_rect_width.png")


class TestTreeToPillow:
    @staticmethod
    def test_tree_to_pillow(tree_node):
        pillow_image = export.tree_to_pillow(tree_node)
        if LOCAL:
            pillow_image.save("tests/tree_pillow.png")

    @staticmethod
    def test_tree_to_pillow_start_pos(tree_node):
        pillow_image = export.tree_to_pillow(tree_node, start_pos=(100, 50))
        if LOCAL:
            pillow_image.save("tests/tree_pillow_start_pos.png")

    @staticmethod
    def test_tree_to_pillow_start_pos_small(tree_node):
        pillow_image = export.tree_to_pillow(tree_node, start_pos=(0, 0))
        if LOCAL:
            pillow_image.save("tests/tree_pillow_start_pos_small.png")

    @staticmethod
    def test_tree_to_pillow_font(tree_node):
        pillow_image = export.tree_to_pillow(
            tree_node, font_size=20, font_colour="red", bg_colour="lightblue"
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_font.png")

    @staticmethod
    def test_tree_to_pillow_kwargs(tree_node):
        pillow_image = export.tree_to_pillow(tree_node, max_depth=2, style="const_bold")
        if LOCAL:
            pillow_image.save("tests/tree_pillow_style.png")

    @staticmethod
    def test_tree_to_pillow_font_family(tree_node):
        font_family = "invalid.ttf"
        with pytest.raises(ValueError) as exc_info:
            export.tree_to_pillow(tree_node, font_family=font_family)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_EXPORT_PILLOW_FONT_FAMILY.format(
            font_family=font_family
        )


class TestTreeToMermaid:
    MERMAID_STR_NODE_SHAPE = (
        """```mermaid\n"""
        """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\n"""
        """flowchart TB\n"""
        """0{"a"} --> 0-0(["b"])\n"""
        """0-0 --> 0-0-0("d")\n"""
        """0-0 --> 0-0-1("e")\n"""
        """0-0-1 --> 0-0-1-0("g")\n"""
        """0-0-1 --> 0-0-1-1("h")\n"""
        """0{"a"} --> 0-1(["c"])\n"""
        """0-1 --> 0-1-0("f")\n"""
        """classDef default stroke-width:1\n"""
        """```"""
    )
    MERMAID_STR_EDGE_ARROW = (
        """```mermaid\n"""
        """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\n"""
        """flowchart TB\n"""
        """0("a") -.-> 0-0("b")\n"""
        """0-0 --> 0-0-0("d")\n"""
        """0-0 --> 0-0-1("e")\n"""
        """0-0-1 --> 0-0-1-0("g")\n"""
        """0-0-1 --> 0-0-1-1("h")\n"""
        """0("a") -.- 0-1("c")\n"""
        """0-1 --> 0-1-0("f")\n"""
        """classDef default stroke-width:1\n"""
        """```"""
    )
    MERMAID_STR_NODE_ATTR = (
        """```mermaid\n"""
        """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\n"""
        """flowchart TB\n"""
        """0("a") --> 0-0("b"):::class0-0\n"""
        """0-0 --> 0-0-0("d")\n"""
        """0-0 --> 0-0-1("e")\n"""
        """0-0-1 --> 0-0-1-0("g"):::class0-0-1-0\n"""
        """0-0-1 --> 0-0-1-1("h"):::class0-0-1-1\n"""
        """0("a") --> 0-1("c")\n"""
        """0-1 --> 0-1-0("f")\n"""
        """classDef default stroke-width:1\n"""
        """classDef class0-0 fill:green,stroke:black\n"""
        """classDef class0-0-1-0 fill:red,stroke:black,stroke-width:2\n"""
        """classDef class0-0-1-1 fill:red,stroke:black,stroke-width:2\n```"""
    )

    @staticmethod
    def test_tree_to_mermaid(tree_node):
        mermaid_md = export.tree_to_mermaid(tree_node)
        expected_str = (
            """```mermaid\n"""
            """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\n"""
            """flowchart TB\n"""
            """0("a") --> 0-0("b")\n"""
            """0-0 --> 0-0-0("d")\n"""
            """0-0 --> 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g")\n"""
            """0-0-1 --> 0-0-1-1("h")\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
            """classDef default stroke-width:1\n"""
            """```"""
        )
        assert mermaid_md == expected_str

    @staticmethod
    def test_tree_to_mermaid_title(tree_node):
        mermaid_md = export.tree_to_mermaid(tree_node, title="Mermaid Diagram")
        expected_str = (
            """```mermaid\n"""
            """---\n"""
            """title: Mermaid Diagram\n"""
            """---\n"""
            """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\n"""
            """flowchart TB\n"""
            """0("a") --> 0-0("b")\n"""
            """0-0 --> 0-0-0("d")\n"""
            """0-0 --> 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g")\n"""
            """0-0-1 --> 0-0-1-1("h")\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
            """classDef default stroke-width:1\n"""
            """```"""
        )
        assert mermaid_md == expected_str

    @staticmethod
    def test_tree_to_mermaid_theme(tree_node):
        mermaid_md = export.tree_to_mermaid(tree_node, theme="forest")
        expected_str = (
            """```mermaid\n"""
            """%%{ init: { \'flowchart\': { \'curve\': \'basis\' }, \'theme\': \'forest\' } }%%\n"""
            """flowchart TB\n"""
            """0("a") --> 0-0("b")\n"""
            """0-0 --> 0-0-0("d")\n"""
            """0-0 --> 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g")\n"""
            """0-0-1 --> 0-0-1-1("h")\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
            """classDef default stroke-width:1\n"""
            """```"""
        )
        assert mermaid_md == expected_str

    @staticmethod
    def test_tree_to_mermaid_invalid_theme_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.tree_to_mermaid(tree_node, theme="invalid")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_MERMAID_INVALID_ARGUMENT.format(parameter="theme")
        )

    @staticmethod
    def test_tree_to_mermaid_invalid_rankdir_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.tree_to_mermaid(tree_node, rankdir="invalid")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_MERMAID_INVALID_ARGUMENT.format(parameter="rankdir")
        )

    @staticmethod
    def test_tree_to_mermaid_invalid_line_shape_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.tree_to_mermaid(tree_node, line_shape="invalid")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_MERMAID_INVALID_ARGUMENT.format(parameter="line_shape")
        )

    @staticmethod
    def test_tree_to_mermaid_invalid_node_shape_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.tree_to_mermaid(tree_node, node_shape="invalid")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_MERMAID_INVALID_ARGUMENT.format(parameter="node_shape")
        )

    @staticmethod
    def test_tree_to_mermaid_invalid_edge_arrow_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.tree_to_mermaid(tree_node, edge_arrow="invalid")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_MERMAID_INVALID_ARGUMENT.format(parameter="edge_arrow")
        )

    @staticmethod
    def test_tree_to_mermaid_invalid_style_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.tree_to_mermaid(tree_node, node_border_width=0)
        assert str(exc_info.value) == Constants.ERROR_NODE_MERMAID_INVALID_STYLE

    @staticmethod
    def test_tree_to_mermaid_rankdir(tree_node):
        rankdirs = ["TB", "BT", "LR", "RL"]
        mermaid_mds = [
            export.tree_to_mermaid(tree_node, rankdir=rankdir) for rankdir in rankdirs
        ]
        expected_graph = (
            """0("a") --> 0-0("b")\n"""
            """0-0 --> 0-0-0("d")\n"""
            """0-0 --> 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g")\n"""
            """0-0-1 --> 0-0-1-1("h")\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
            """classDef default stroke-width:1\n"""
        )
        expected_strs = [
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'basis\' }} }} }}%%\nflowchart TB\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'basis\' }} }} }}%%\nflowchart BT\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'basis\' }} }} }}%%\nflowchart LR\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'basis\' }} }} }}%%\nflowchart RL\n{expected_graph}```""",
        ]
        for rankdir, mermaid_md, expected_str in zip(
            rankdirs, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check rankdir {rankdir}"

    @staticmethod
    def test_tree_to_mermaid_line_shape(tree_node):
        line_shapes = [
            "basis",
            "bumpX",
            "bumpY",
            "cardinal",
            "catmullRom",
            "linear",
            "monotoneX",
            "monotoneY",
            "natural",
            "step",
            "stepAfter",
            "stepBefore",
        ]
        mermaid_mds = [
            export.tree_to_mermaid(tree_node, line_shape=line_shape)
            for line_shape in line_shapes
        ]
        expected_graph = (
            """flowchart TB\n"""
            """0("a") --> 0-0("b")\n"""
            """0-0 --> 0-0-0("d")\n"""
            """0-0 --> 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g")\n"""
            """0-0-1 --> 0-0-1-1("h")\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
            """classDef default stroke-width:1\n"""
        )
        expected_strs = [
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'basis\' }} }} }}%%\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'bumpX\' }} }} }}%%\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'bumpY\' }} }} }}%%\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'cardinal\' }} }} }}%%\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'catmullRom\' }} }} }}%%\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'linear\' }} }} }}%%\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'monotoneX\' }} }} }}%%\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'monotoneY\' }} }} }}%%\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'natural\' }} }} }}%%\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'step\' }} }} }}%%\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'stepAfter\' }} }} }}%%\n{expected_graph}```""",
            f"""```mermaid\n%%{{ init: {{ \'flowchart\': {{ \'curve\': \'stepBefore\' }} }} }}%%\n{expected_graph}```""",
        ]
        for line_shape, mermaid_md, expected_str in zip(
            line_shapes, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check line_shape {line_shape}"

    @staticmethod
    def test_tree_to_mermaid_node_colour(tree_node):
        node_colours = ["yellow", "blue", "#000", "#ff0000"]
        mermaid_mds = [
            export.tree_to_mermaid(tree_node, node_colour=node_colour)
            for node_colour in node_colours
        ]
        expected_graph = (
            """mermaid\n"""
            """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\n"""
            """flowchart TB\n"""
            """0("a") --> 0-0("b")\n"""
            """0-0 --> 0-0-0("d")\n"""
            """0-0 --> 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g")\n"""
            """0-0-1 --> 0-0-1-1("h")\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
        )
        expected_strs = [
            f"""```{expected_graph}classDef default fill:yellow,stroke-width:1\n```""",
            f"""```{expected_graph}classDef default fill:blue,stroke-width:1\n```""",
            f"""```{expected_graph}classDef default fill:#000,stroke-width:1\n```""",
            f"""```{expected_graph}classDef default fill:#ff0000,stroke-width:1\n```""",
        ]
        for node_colour, mermaid_md, expected_str in zip(
            node_colours, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check node_colour {node_colour}"

    @staticmethod
    def test_tree_to_mermaid_node_border_colour(tree_node):
        node_border_colours = ["yellow", "blue", "#000", "#ff0000"]
        mermaid_mds = [
            export.tree_to_mermaid(tree_node, node_border_colour=node_border_colour)
            for node_border_colour in node_border_colours
        ]
        expected_graph = (
            """mermaid\n"""
            """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\n"""
            """flowchart TB\n"""
            """0("a") --> 0-0("b")\n"""
            """0-0 --> 0-0-0("d")\n"""
            """0-0 --> 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g")\n"""
            """0-0-1 --> 0-0-1-1("h")\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
        )
        expected_strs = [
            f"""```{expected_graph}classDef default stroke:yellow,stroke-width:1\n```""",
            f"""```{expected_graph}classDef default stroke:blue,stroke-width:1\n```""",
            f"""```{expected_graph}classDef default stroke:#000,stroke-width:1\n```""",
            f"""```{expected_graph}classDef default stroke:#ff0000,stroke-width:1\n```""",
        ]
        for node_border_colour, mermaid_md, expected_str in zip(
            node_border_colours, mermaid_mds, expected_strs
        ):
            assert (
                mermaid_md == expected_str
            ), f"Check node_border_colour {node_border_colour}"

    @staticmethod
    def test_tree_to_mermaid_node_border_width(tree_node):
        node_border_widths = [1, 1.5, 2, 10.5]
        mermaid_mds = [
            export.tree_to_mermaid(tree_node, node_border_width=node_border_width)
            for node_border_width in node_border_widths
        ]
        expected_graph = (
            """mermaid\n"""
            """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n"""
            """0("a") --> 0-0("b")\n"""
            """0-0 --> 0-0-0("d")\n"""
            """0-0 --> 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g")\n"""
            """0-0-1 --> 0-0-1-1("h")\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
        )
        expected_strs = [
            f"""```{expected_graph}classDef default stroke-width:1\n```""",
            f"""```{expected_graph}classDef default stroke-width:1.5\n```""",
            f"""```{expected_graph}classDef default stroke-width:2\n```""",
            f"""```{expected_graph}classDef default stroke-width:10.5\n```""",
        ]
        for node_border_width, mermaid_md, expected_str in zip(
            node_border_widths, mermaid_mds, expected_strs
        ):
            assert (
                mermaid_md == expected_str
            ), f"Check node_border_width {node_border_width}"

    @staticmethod
    def test_tree_to_mermaid_node_colour_border_colour_border_width(tree_node):
        node_styles = [("yellow", "#ff0", 0), ("#ff0000", "#000", 2)]
        mermaid_mds = [
            export.tree_to_mermaid(
                tree_node,
                node_colour=node_colour,
                node_border_colour=node_border_colour,
                node_border_width=node_border_width,
            )
            for node_colour, node_border_colour, node_border_width in node_styles
        ]
        expected_graph = (
            """mermaid\n"""
            """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\n"""
            """flowchart TB\n"""
            """0("a") --> 0-0("b")\n"""
            """0-0 --> 0-0-0("d")\n"""
            """0-0 --> 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g")\n"""
            """0-0-1 --> 0-0-1-1("h")\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
        )
        expected_strs = [
            f"""```{expected_graph}classDef default fill:yellow,stroke:#ff0\n```""",
            f"""```{expected_graph}classDef default fill:#ff0000,stroke:#000,stroke-width:2\n```""",
        ]
        for node_style, mermaid_md, expected_str in zip(
            node_styles, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check node_style {node_style}"

    @staticmethod
    def test_tree_to_mermaid_node_shape(tree_node):
        node_shapes = [
            "rounded_edge",
            "stadium",
            "subroutine",
            "cylindrical",
            "circle",
            "asymmetric",
            "rhombus",
            "hexagon",
            "parallelogram",
            "parallelogram_alt",
            "trapezoid",
            "trapezoid_alt",
            "double_circle",
        ]
        mermaid_mds = [
            export.tree_to_mermaid(tree_node, node_shape=node_shape)
            for node_shape in node_shapes
        ]
        expected_strs = [
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 0-0("b")\n0-0 --> 0-0-0("d")\n0-0 --> 0-0-1("e")\n0-0-1 --> 0-0-1-0("g")\n0-0-1 --> 0-0-1-1("h")\n0("a") --> 0-1("c")\n0-1 --> 0-1-0("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0(["a"]) --> 0-0(["b"])\n0-0 --> 0-0-0(["d"])\n0-0 --> 0-0-1(["e"])\n0-0-1 --> 0-0-1-0(["g"])\n0-0-1 --> 0-0-1-1(["h"])\n0(["a"]) --> 0-1(["c"])\n0-1 --> 0-1-0(["f"])\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[["a"]] --> 0-0[["b"]]\n0-0 --> 0-0-0[["d"]]\n0-0 --> 0-0-1[["e"]]\n0-0-1 --> 0-0-1-0[["g"]]\n0-0-1 --> 0-0-1-1[["h"]]\n0[["a"]] --> 0-1[["c"]]\n0-1 --> 0-1-0[["f"]]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[("a")] --> 0-0[("b")]\n0-0 --> 0-0-0[("d")]\n0-0 --> 0-0-1[("e")]\n0-0-1 --> 0-0-1-0[("g")]\n0-0-1 --> 0-0-1-1[("h")]\n0[("a")] --> 0-1[("c")]\n0-1 --> 0-1-0[("f")]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0(("a")) --> 0-0(("b"))\n0-0 --> 0-0-0(("d"))\n0-0 --> 0-0-1(("e"))\n0-0-1 --> 0-0-1-0(("g"))\n0-0-1 --> 0-0-1-1(("h"))\n0(("a")) --> 0-1(("c"))\n0-1 --> 0-1-0(("f"))\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0>"a"] --> 0-0>"b"]\n0-0 --> 0-0-0>"d"]\n0-0 --> 0-0-1>"e"]\n0-0-1 --> 0-0-1-0>"g"]\n0-0-1 --> 0-0-1-1>"h"]\n0>"a"] --> 0-1>"c"]\n0-1 --> 0-1-0>"f"]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0{"a"} --> 0-0{"b"}\n0-0 --> 0-0-0{"d"}\n0-0 --> 0-0-1{"e"}\n0-0-1 --> 0-0-1-0{"g"}\n0-0-1 --> 0-0-1-1{"h"}\n0{"a"} --> 0-1{"c"}\n0-1 --> 0-1-0{"f"}\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0{{"a"}} --> 0-0{{"b"}}\n0-0 --> 0-0-0{{"d"}}\n0-0 --> 0-0-1{{"e"}}\n0-0-1 --> 0-0-1-0{{"g"}}\n0-0-1 --> 0-0-1-1{{"h"}}\n0{{"a"}} --> 0-1{{"c"}}\n0-1 --> 0-1-0{{"f"}}\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[/"a"/] --> 0-0[/"b"/]\n0-0 --> 0-0-0[/"d"/]\n0-0 --> 0-0-1[/"e"/]\n0-0-1 --> 0-0-1-0[/"g"/]\n0-0-1 --> 0-0-1-1[/"h"/]\n0[/"a"/] --> 0-1[/"c"/]\n0-1 --> 0-1-0[/"f"/]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[\\"a"\\] --> 0-0[\\"b"\\]\n0-0 --> 0-0-0[\\"d"\\]\n0-0 --> 0-0-1[\\"e"\\]\n0-0-1 --> 0-0-1-0[\\"g"\\]\n0-0-1 --> 0-0-1-1[\\"h"\\]\n0[\\"a"\\] --> 0-1[\\"c"\\]\n0-1 --> 0-1-0[\\"f"\\]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[/"a"\\] --> 0-0[/"b"\\]\n0-0 --> 0-0-0[/"d"\\]\n0-0 --> 0-0-1[/"e"\\]\n0-0-1 --> 0-0-1-0[/"g"\\]\n0-0-1 --> 0-0-1-1[/"h"\\]\n0[/"a"\\] --> 0-1[/"c"\\]\n0-1 --> 0-1-0[/"f"\\]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[\\"a"/] --> 0-0[\\"b"/]\n0-0 --> 0-0-0[\\"d"/]\n0-0 --> 0-0-1[\\"e"/]\n0-0-1 --> 0-0-1-0[\\"g"/]\n0-0-1 --> 0-0-1-1[\\"h"/]\n0[\\"a"/] --> 0-1[\\"c"/]\n0-1 --> 0-1-0[\\"f"/]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0((("a"))) --> 0-0((("b")))\n0-0 --> 0-0-0((("d")))\n0-0 --> 0-0-1((("e")))\n0-0-1 --> 0-0-1-0((("g")))\n0-0-1 --> 0-0-1-1((("h")))\n0((("a"))) --> 0-1((("c")))\n0-1 --> 0-1-0((("f")))\nclassDef default stroke-width:1\n```""",
        ]
        for node_shape, mermaid_md, expected_str in zip(
            node_shapes, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check node_shape {node_shape}"

    def test_tree_to_mermaid_node_shape_attr(self, tree_node_mermaid_style):
        mermaid_md = export.tree_to_mermaid(
            tree_node_mermaid_style, node_shape_attr="node_shape"
        )
        assert mermaid_md == self.MERMAID_STR_NODE_SHAPE

    def test_tree_to_mermaid_node_shape_attr_callable(self, tree_node_no_attr):
        def get_node_shape(node):
            if node.node_name == "a":
                return "rhombus"
            elif node.depth == 2:
                return "stadium"
            return "rounded_edge"

        mermaid_md = export.tree_to_mermaid(
            tree_node_no_attr, node_shape_attr=get_node_shape
        )
        assert mermaid_md == self.MERMAID_STR_NODE_SHAPE

    @staticmethod
    def test_tree_to_mermaid_edge_arrow(tree_node):
        edge_arrows = [
            "normal",
            "bold",
            "dotted",
            "open",
            "bold_open",
            "dotted_open",
            "invisible",
            "circle",
            "cross",
            "double_normal",
            "double_circle",
            "double_cross",
        ]
        mermaid_mds = [
            export.tree_to_mermaid(tree_node, edge_arrow=edge_arrow)
            for edge_arrow in edge_arrows
        ]
        expected_strs = [
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 0-0("b")\n0-0 --> 0-0-0("d")\n0-0 --> 0-0-1("e")\n0-0-1 --> 0-0-1-0("g")\n0-0-1 --> 0-0-1-1("h")\n0("a") --> 0-1("c")\n0-1 --> 0-1-0("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") ==> 0-0("b")\n0-0 ==> 0-0-0("d")\n0-0 ==> 0-0-1("e")\n0-0-1 ==> 0-0-1-0("g")\n0-0-1 ==> 0-0-1-1("h")\n0("a") ==> 0-1("c")\n0-1 ==> 0-1-0("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") -.-> 0-0("b")\n0-0 -.-> 0-0-0("d")\n0-0 -.-> 0-0-1("e")\n0-0-1 -.-> 0-0-1-0("g")\n0-0-1 -.-> 0-0-1-1("h")\n0("a") -.-> 0-1("c")\n0-1 -.-> 0-1-0("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --- 0-0("b")\n0-0 --- 0-0-0("d")\n0-0 --- 0-0-1("e")\n0-0-1 --- 0-0-1-0("g")\n0-0-1 --- 0-0-1-1("h")\n0("a") --- 0-1("c")\n0-1 --- 0-1-0("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") === 0-0("b")\n0-0 === 0-0-0("d")\n0-0 === 0-0-1("e")\n0-0-1 === 0-0-1-0("g")\n0-0-1 === 0-0-1-1("h")\n0("a") === 0-1("c")\n0-1 === 0-1-0("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") -.- 0-0("b")\n0-0 -.- 0-0-0("d")\n0-0 -.- 0-0-1("e")\n0-0-1 -.- 0-0-1-0("g")\n0-0-1 -.- 0-0-1-1("h")\n0("a") -.- 0-1("c")\n0-1 -.- 0-1-0("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") ~~~ 0-0("b")\n0-0 ~~~ 0-0-0("d")\n0-0 ~~~ 0-0-1("e")\n0-0-1 ~~~ 0-0-1-0("g")\n0-0-1 ~~~ 0-0-1-1("h")\n0("a") ~~~ 0-1("c")\n0-1 ~~~ 0-1-0("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --o 0-0("b")\n0-0 --o 0-0-0("d")\n0-0 --o 0-0-1("e")\n0-0-1 --o 0-0-1-0("g")\n0-0-1 --o 0-0-1-1("h")\n0("a") --o 0-1("c")\n0-1 --o 0-1-0("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --x 0-0("b")\n0-0 --x 0-0-0("d")\n0-0 --x 0-0-1("e")\n0-0-1 --x 0-0-1-0("g")\n0-0-1 --x 0-0-1-1("h")\n0("a") --x 0-1("c")\n0-1 --x 0-1-0("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") <--> 0-0("b")\n0-0 <--> 0-0-0("d")\n0-0 <--> 0-0-1("e")\n0-0-1 <--> 0-0-1-0("g")\n0-0-1 <--> 0-0-1-1("h")\n0("a") <--> 0-1("c")\n0-1 <--> 0-1-0("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") o--o 0-0("b")\n0-0 o--o 0-0-0("d")\n0-0 o--o 0-0-1("e")\n0-0-1 o--o 0-0-1-0("g")\n0-0-1 o--o 0-0-1-1("h")\n0("a") o--o 0-1("c")\n0-1 o--o 0-1-0("f")\nclassDef default stroke-width:1\n```""",
        ]
        for edge_arrow, mermaid_md, expected_str in zip(
            edge_arrows, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check edge_arrow {edge_arrow}"

    def test_tree_to_mermaid_edge_arrow_attr(self, tree_node_mermaid_style):
        mermaid_md = export.tree_to_mermaid(
            tree_node_mermaid_style, edge_arrow_attr="edge_arrow"
        )
        assert mermaid_md == self.MERMAID_STR_EDGE_ARROW

    def test_tree_to_mermaid_edge_arrow_attr_callable(self, tree_node_no_attr):
        def get_edge_arrow_attr(node):
            if node.node_name == "b":
                return "dotted"
            if node.node_name == "c":
                return "dotted_open"
            return "normal"

        mermaid_md = export.tree_to_mermaid(
            tree_node_no_attr, edge_arrow_attr=get_edge_arrow_attr
        )
        assert mermaid_md == self.MERMAID_STR_EDGE_ARROW

    @staticmethod
    def test_tree_to_mermaid_edge_label(tree_node_mermaid_style):
        mermaid_md = export.tree_to_mermaid(tree_node_mermaid_style, edge_label="label")
        expected_str = (
            """```mermaid\n"""
            """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\n"""
            """flowchart TB\n"""
            """0("a") --> 0-0("b")\n"""
            """0-0 -->|c-d link| 0-0-0("d")\n"""
            """0-0 -->|c-e link| 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g")\n"""
            """0-0-1 --> 0-0-1-1("h")\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
            """classDef default stroke-width:1\n```"""
        )
        assert mermaid_md == expected_str

    def test_tree_to_mermaid_node_attr(self, tree_node_mermaid_style):
        mermaid_md = export.tree_to_mermaid(tree_node_mermaid_style, node_attr="attr")
        assert mermaid_md == self.MERMAID_STR_NODE_ATTR

    def test_tree_to_mermaid_node_attr_callable(self, tree_node_no_attr):
        def get_node_attr(node):
            if node.node_name == "b":
                return "fill:green,stroke:black"
            elif node.node_name in ["g", "h"]:
                return "fill:red,stroke:black,stroke-width:2"
            return ""

        mermaid_md = export.tree_to_mermaid(tree_node_no_attr, node_attr=get_node_attr)
        assert mermaid_md == self.MERMAID_STR_NODE_ATTR

    def test_tree_to_mermaid_node_attr_root(self, tree_node_no_attr):
        def get_node_attr(node):
            if node.node_name == "a":
                return "fill:green,stroke:black"
            elif node.node_name in ["g", "h"]:
                return "fill:red,stroke:black,stroke-width:2"
            return ""

        mermaid_md = export.tree_to_mermaid(tree_node_no_attr, node_attr=get_node_attr)
        expected_str = (
            """```mermaid\n"""
            """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\n"""
            """flowchart TB\n"""
            """0("a"):::class0 --> 0-0("b")\n"""
            """0-0 --> 0-0-0("d")\n"""
            """0-0 --> 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g"):::class0-0-1-0\n"""
            """0-0-1 --> 0-0-1-1("h"):::class0-0-1-1\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
            """classDef default stroke-width:1\n"""
            """classDef class0 fill:green,stroke:black\n"""
            """classDef class0-0-1-0 fill:red,stroke:black,stroke-width:2\n"""
            """classDef class0-0-1-1 fill:red,stroke:black,stroke-width:2\n```"""
        )
        assert mermaid_md == expected_str

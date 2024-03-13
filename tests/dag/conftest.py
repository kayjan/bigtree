import pytest

from bigtree.node.dagnode import DAGNode


@pytest.fixture
def dag_node_plot():
    z = DAGNode("z")
    y = DAGNode("y")
    y.parents = [z]
    return z


@pytest.fixture
def dag_node_style():
    a = DAGNode(
        "a",
        node_style={"style": "filled", "fillcolor": "gold"},
        edge_style={"style": "bold", "label": "a"},
    )
    b = DAGNode(
        "b",
        node_style={"style": "filled", "fillcolor": "blue"},
        edge_style={"style": "bold", "label": "b"},
    )
    c = DAGNode(
        "c",
        node_style={"style": "filled", "fillcolor": "blue"},
        edge_style={"style": "bold", "label": "c"},
    )
    d = DAGNode(
        "d",
        node_style={"style": "filled", "fillcolor": "green"},
        edge_style={"style": "bold", "label": 1},
    )
    e = DAGNode(
        "e",
        node_style={"style": "filled", "fillcolor": "green"},
        edge_style={"style": "bold", "label": 2},
    )
    f = DAGNode(
        "f",
        node_style={"style": "filled", "fillcolor": "green"},
        edge_style={"style": "bold", "label": 3},
    )
    g = DAGNode(
        "g",
        node_style={"style": "filled", "fillcolor": "red"},
        edge_style={"style": "bold", "label": 4},
    )
    h = DAGNode(
        "h",
        node_style={"style": "filled", "fillcolor": "red"},
        edge_style={"style": "bold", "label": 5},
    )

    c.parents = [a, b]
    d.parents = [a, c]
    e.parents = [d]
    f.parents = [c, d]
    g.parents = [c]
    h.parents = [g]
    return a

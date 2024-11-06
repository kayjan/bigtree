import pytest

from bigtree.node import node
from bigtree.tree import helper, modify


@pytest.fixture
def tree_node_plot():
    z = node.Node("z")
    y = node.Node("y")
    y.parent = z
    return z


@pytest.fixture
def tree_node_duplicate_names():
    """
    Tree should have structure
    a (age=90)
    |-- a (age=65)
    |   |-- a (age=40)
    |   +-- b (age=35)
    |       |-- a (age=10)
    |       +-- b (age=6)
    +-- b (age=60)
        +-- a (age=38)
    """
    a = node.Node("a", age=90)
    b = node.Node("a", age=65)
    c = node.Node("b", age=60)
    d = node.Node("a", age=40)
    e = node.Node("b", age=35)
    f = node.Node("a", age=38)
    g = node.Node("a", age=10)
    h = node.Node("b", age=6)

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = e
    h.parent = e
    return a


@pytest.fixture
def tree_node_no_attr():
    """
    Tree should have structure
    a
    |-- b
    |   |-- d
    |   +-- e
    |       |-- g
    |       +-- h
    +-- c
        +-- f
    """
    a = node.Node("a")
    b = node.Node("b")
    c = node.Node("c")
    d = node.Node("d")
    e = node.Node("e")
    f = node.Node("f")
    g = node.Node("g")
    h = node.Node("h")

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = e
    h.parent = e
    return a


@pytest.fixture
def tree_node_negative_null_attr():
    """
    Tree should have structure
    a
    |-- b
    |   |-- d
    |   +-- e
    |       |-- g
    |       +-- h
    +-- c
        +-- f
    """
    a = node.Node("a")
    b = node.Node("b", age=-1)
    c = node.Node("c", age=0)
    d = node.Node("d", age=1)
    e = node.Node("e", age=None)
    f = node.Node("f", age=float("nan"))
    g = node.Node("g", age="10")
    h = node.Node("h")

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = e
    h.parent = e
    return a


@pytest.fixture
def tree_node_style():
    """
    Tree should have structure
    a
    |-- b
    |   |-- d
    |   +-- e
    |       |-- g
    |       +-- h
    +-- c
        +-- f
    """
    a = node.Node(
        "a",
        node_style={"style": "filled", "fillcolor": "gold"},
        edge_style={"style": "bold", "label": "a"},
    )
    b = node.Node(
        "b",
        node_style={"style": "filled", "fillcolor": "blue"},
        edge_style={"style": "bold", "label": "b"},
    )
    c = node.Node(
        "c",
        node_style={"style": "filled", "fillcolor": "blue"},
        edge_style={"style": "bold", "label": "c"},
    )
    d = node.Node(
        "d",
        node_style={"style": "filled", "fillcolor": "green"},
        edge_style={"style": "bold", "label": 1},
    )
    e = node.Node(
        "e",
        node_style={"style": "filled", "fillcolor": "green"},
        edge_style={"style": "bold", "label": 2},
    )
    f = node.Node(
        "f",
        node_style={"style": "filled", "fillcolor": "green"},
        edge_style={"style": "bold", "label": 3},
    )
    g = node.Node(
        "g",
        node_style={"style": "filled", "fillcolor": "red"},
        edge_style={"style": "bold", "label": 4},
    )
    h = node.Node(
        "h",
        node_style={"style": "filled", "fillcolor": "red"},
        edge_style={"style": "bold", "label": 5},
    )

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = d
    h.parent = e
    return a


@pytest.fixture
def tree_node_style_callable():
    """
    Tree should have structure
    a
    |-- b
    |   |-- d
    |   +-- e
    |       |-- g
    |       +-- h
    +-- c
        +-- f
    """
    a = node.Node("a", style=1)
    b = node.Node("b", style="two")
    c = node.Node("c", style=("three"))
    d = node.Node("d")
    e = node.Node("e")
    f = node.Node("f")
    g = node.Node("g")
    h = node.Node("h")

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = d
    h.parent = e
    return a


@pytest.fixture
def tree_node_mermaid_style():
    """
    Tree should have structure
    a
    |-- b
    |   |-- d
    |   +-- e
    |       |-- g
    |       +-- h
    +-- c
        +-- f
    """
    a = node.Node("a", node_shape="rhombus")
    b = node.Node(
        "b", node_shape="stadium", edge_arrow="dotted", attr="fill:green,stroke:black"
    )
    c = node.Node("c", node_shape="stadium", edge_arrow="dotted_open")
    d = node.Node("d", label="c-d link")
    e = node.Node("e", label="c-e link")
    f = node.Node("f")
    g = node.Node("g", attr="fill:red,stroke:black,stroke-width:2")
    h = node.Node("h", attr="fill:red,stroke:black,stroke-width:2")

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = e
    h.parent = e
    return a


@pytest.fixture
def phylogenetic_tree():
    """
    Example taken from: https://www.cs.mcgill.ca/~birch/doc/forester/NHX.pdf
    """
    root = node.Node("placeholder_root", E="1.1.1.1", D="N")
    metazoa = node.Node(
        "placeholder_metazoa",
        length=0.1,
        S="Metazoa",
        E="1.1.1.1",
        D="N",
        parent=root,
    )
    primates = node.Node(
        "placeholder_primates",
        length=0.05,
        S="Primates",
        E="1.1.1.1",
        D="Y",
        B="100",
        parent=metazoa,
    )
    _ = node.Node("ADH2", length=0.1, S="human", E="1.1.1.1", parent=primates)
    _ = node.Node("ADH1", length=0.11, S="human", E="1.1.1.1", parent=primates)
    _ = node.Node("ADHY", length=0.1, S="nematode", E="1.1.1.1", parent=metazoa)
    _ = node.Node("ADHX", length=0.12, S="insect", E="1.1.1.1", parent=metazoa)
    fungi = node.Node("placeholder_fungi", length=0.1, S="Fungi", parent=root)
    _ = node.Node("ADH4", length=0.09, S="yeast", E="1.1.1.1", parent=fungi)
    _ = node.Node("ADH3", length=0.13, S="yeast", E="1.1.1.1", parent=fungi)
    _ = node.Node("ADH2", length=0.12, S="yeast", E="1.1.1.1", parent=fungi)
    _ = node.Node("ADH1", length=0.11, S="yeast", E="1.1.1.1", parent=fungi)
    return root


@pytest.fixture
def tree_node_diff(tree_node):
    # Remove nodes + shift nodes + add nodes
    other_tree_node = helper.prune_tree(tree_node, "a/c")
    modify.copy_nodes_from_tree_to_tree(
        tree_node, other_tree_node, ["a/b/e"], ["a/c/e"]
    )
    node.Node("i", parent=other_tree_node, children=[node.Node("j")])
    return other_tree_node

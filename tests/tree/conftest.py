import pytest

from bigtree.node.node import Node


@pytest.fixture
def tree_node_plot():
    z = Node("z")
    y = Node("y")
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
    a = Node("a", age=90)
    b = Node("a", age=65)
    c = Node("b", age=60)
    d = Node("a", age=40)
    e = Node("b", age=35)
    f = Node("a", age=38)
    g = Node("a", age=10)
    h = Node("b", age=6)

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
    a = Node("a")
    b = Node("b")
    c = Node("c")
    d = Node("d")
    e = Node("e")
    f = Node("f")
    g = Node("g")
    h = Node("h")

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
    a = Node("a")
    b = Node("b", age=-1)
    c = Node("c", age=0)
    d = Node("d", age=1)
    e = Node("e", age=None)
    f = Node("f", age=float("nan"))
    g = Node("g", age="10")
    h = Node("h")

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
    a = Node(
        "a",
        node_style={"style": "filled", "fillcolor": "gold"},
        edge_style={"style": "bold", "label": "a"},
    )
    b = Node(
        "b",
        node_style={"style": "filled", "fillcolor": "blue"},
        edge_style={"style": "bold", "label": "b"},
    )
    c = Node(
        "c",
        node_style={"style": "filled", "fillcolor": "blue"},
        edge_style={"style": "bold", "label": "c"},
    )
    d = Node(
        "d",
        node_style={"style": "filled", "fillcolor": "green"},
        edge_style={"style": "bold", "label": 1},
    )
    e = Node(
        "e",
        node_style={"style": "filled", "fillcolor": "green"},
        edge_style={"style": "bold", "label": 2},
    )
    f = Node(
        "f",
        node_style={"style": "filled", "fillcolor": "green"},
        edge_style={"style": "bold", "label": 3},
    )
    g = Node(
        "g",
        node_style={"style": "filled", "fillcolor": "red"},
        edge_style={"style": "bold", "label": 4},
    )
    h = Node(
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
    a = Node("a", style=1)
    b = Node("b", style="two")
    c = Node("c", style=("three"))
    d = Node("d")
    e = Node("e")
    f = Node("f")
    g = Node("g")
    h = Node("h")

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
    a = Node("a", node_shape="rhombus")
    b = Node("b", node_shape="stadium", edge_arrow="dotted")
    c = Node("c", node_shape="stadium", edge_arrow="dotted_open")
    d = Node("d", label="c-d link")
    e = Node("e", label="c-e link")
    f = Node("f")
    g = Node("g", attr="fill:red,stroke:black,stroke-width:2")
    h = Node("h", attr="fill:red,stroke:black,stroke-width:2")

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = d
    h.parent = e
    return a


@pytest.fixture
def tree_node_mermaid_style_callable():
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
    a = Node("a")
    b = Node("b")
    c = Node("c")
    d = Node("d", label="c-d link")
    e = Node("e", label="c-e link")
    f = Node("f")
    g = Node("g")
    h = Node("h")

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = d
    h.parent = e
    return a


@pytest.fixture
def phylogenetic_tree():
    """
    Example taken from: https://www.cs.mcgill.ca/~birch/doc/forester/NHX.pdf
    """
    root = Node("placeholder_root", E="1.1.1.1", D="N")
    metazoa = Node(
        "placeholder_metazoa",
        length=0.1,
        S="Metazoa",
        E="1.1.1.1",
        D="N",
        parent=root,
    )
    primates = Node(
        "placeholder_primates",
        length=0.05,
        S="Primates",
        E="1.1.1.1",
        D="Y",
        B="100",
        parent=metazoa,
    )
    _ = Node("ADH2", length=0.1, S="human", E="1.1.1.1", parent=primates)
    _ = Node("ADH1", length=0.11, S="human", E="1.1.1.1", parent=primates)
    _ = Node("ADHY", length=0.1, S="nematode", E="1.1.1.1", parent=metazoa)
    _ = Node("ADHX", length=0.12, S="insect", E="1.1.1.1", parent=metazoa)
    fungi = Node("placeholder_fungi", length=0.1, S="Fungi", parent=root)
    _ = Node("ADH4", length=0.09, S="yeast", E="1.1.1.1", parent=fungi)
    _ = Node("ADH3", length=0.13, S="yeast", E="1.1.1.1", parent=fungi)
    _ = Node("ADH2", length=0.12, S="yeast", E="1.1.1.1", parent=fungi)
    _ = Node("ADH1", length=0.11, S="yeast", E="1.1.1.1", parent=fungi)
    return root

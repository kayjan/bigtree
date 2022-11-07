import io
import logging
import sys
from typing import List, Union

import pytest

from bigtree.node.basenode import BaseNode
from bigtree.node.dagnode import DAGNode
from bigtree.node.node import Node


@pytest.fixture
def tree_basenode():
    """
    Tree should have structure
    a (age=90)
    |-- b (age=65)
    |   |-- d (age=40)
    |   +-- e (age=35)
    |       |-- g (age=10)
    |       +-- h (age=6)
    +-- c (age=60)
        +-- f (age=38)
    """
    a = BaseNode(name="a", age=90)
    b = BaseNode(name="b", age=65)
    c = BaseNode(name="c", age=60)
    d = BaseNode(name="d", age=40)
    e = BaseNode(name="e", age=35)
    f = BaseNode(name="f", age=38)
    g = BaseNode(name="g", age=10)
    h = BaseNode(name="h", age=6)

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = e
    h.parent = e
    return a


@pytest.fixture
def tree_node():
    """
    Tree should have structure
    a (age=90)
    |-- b (age=65)
    |   |-- d (age=40)
    |   +-- e (age=35)
    |       |-- g (age=10)
    |       +-- h (age=6)
    +-- c (age=60)
        +-- f (age=38)
    """
    a = Node("a", age=90)
    b = Node("b", age=65)
    c = Node("c", age=60)
    d = Node("d", age=40)
    e = Node("e", age=35)
    f = Node("f", age=38)
    g = Node("g", age=10)
    h = Node("h", age=6)

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = e
    h.parent = e
    return a


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
def tree_node2():
    """
    Tree should have structure
    a (age=90)
    |-- b (age=65)
    |   |-- d (age=40)
    |       |-- g (age=10)
    |   +-- e (age=35)
    |       |-- h (age=6)
    |       +-- i (age=4)
    +-- c (age=60)
        +-- f (age=38)
    """
    a = Node("a", age=90)
    b = Node("b", age=65)
    c = Node("c", age=60)
    d = Node("d", age=40)
    e = Node("e", age=35)
    f = Node("f", age=38)
    g = Node("g", age=10)
    h = Node("h", age=6)
    i = Node("i", age=4)

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = d
    h.parent = e
    i.parent = e
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
    a = Node("a", node_style={"style": "filled", "fillcolor": "gold"})
    b = Node("b", node_style={"style": "filled", "fillcolor": "blue"})
    c = Node("c", node_style={"style": "filled", "fillcolor": "blue"})
    d = Node("d", node_style={"style": "filled", "fillcolor": "green"})
    e = Node("e", node_style={"style": "filled", "fillcolor": "green"})
    f = Node("f", node_style={"style": "filled", "fillcolor": "green"})
    g = Node("g", node_style={"style": "filled", "fillcolor": "red"})
    h = Node("h", node_style={"style": "filled", "fillcolor": "red"})

    b.parent = a
    c.parent = a
    d.parent = b
    e.parent = b
    f.parent = c
    g.parent = d
    h.parent = e
    return a


@pytest.fixture
def dag_node():
    a = DAGNode("a", age=90)
    b = DAGNode("b", age=65)
    c = DAGNode("c", age=60)
    d = DAGNode("d", age=40)
    e = DAGNode("e", age=35)
    f = DAGNode("f", age=38)
    g = DAGNode("g", age=10)
    h = DAGNode("h", age=6)

    c.parents = [a, b]
    d.parents = [a, c]
    e.parents = [d]
    f.parents = [c, d]
    g.parents = [c]
    h.parents = [g]
    return a


@pytest.fixture
def dag_node_child():
    a = DAGNode("a", age=90)
    b = DAGNode("b", age=65)
    c = DAGNode("c", age=60)
    d = DAGNode("d", age=40)
    e = DAGNode("e", age=35)
    f = DAGNode("f", age=38)
    g = DAGNode("g", age=10)
    h = DAGNode("h", age=6)

    c.parents = [a, b]
    d.parents = [a, c]
    e.parents = [d]
    f.parents = [c, d]
    g.parents = [c]
    h.parents = [g]
    return f


@pytest.fixture
def dag_node_style():
    a = DAGNode("a", node_style={"style": "filled", "fillcolor": "gold"})
    b = DAGNode("b", node_style={"style": "filled", "fillcolor": "blue"})
    c = DAGNode("c", node_style={"style": "filled", "fillcolor": "blue"})
    d = DAGNode("d", node_style={"style": "filled", "fillcolor": "green"})
    e = DAGNode("e", node_style={"style": "filled", "fillcolor": "green"})
    f = DAGNode("f", node_style={"style": "filled", "fillcolor": "green"})
    g = DAGNode("g", node_style={"style": "filled", "fillcolor": "red"})
    h = DAGNode("h", node_style={"style": "filled", "fillcolor": "red"})

    c.parents = [a, b]
    d.parents = [a, c]
    e.parents = [d]
    f.parents = [c, d]
    g.parents = [c]
    h.parents = [g]
    return a


def assert_print_statement(func, expected, *args, **kwargs):
    captured_output = io.StringIO()
    sys.stdout = captured_output
    func(*args, **kwargs)
    sys.stdout = sys.__stdout__
    actual = captured_output.getvalue()
    assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"


def assert_console_output(expected: Union[List[str], str]):
    def _decorator(func):
        def wrapper(caplog, *args, **kwargs):
            caplog.set_level(logging.DEBUG)
            func(*args, **kwargs)
            if isinstance(expected, str):
                assert (
                    expected in caplog.text
                ), f"Expected\n{expected}\nReceived\n{caplog.text}"
            elif isinstance(expected, list):
                log_list = caplog.text.rstrip("\n").split("\n")
                assert len(expected) == len(
                    log_list
                ), f"Unequal length: Expected\n{expected}\nReceived\n{log_list}"
                for _expected, _actual in zip(expected, log_list):
                    assert (
                        _expected in _actual
                    ), f"Expected\n{_expected}\nReceived\n{_actual}"

        return wrapper

    return _decorator

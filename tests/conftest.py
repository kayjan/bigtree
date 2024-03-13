import io
import logging
import sys
from typing import List, Union

import pytest

from bigtree.node.basenode import BaseNode
from bigtree.node.binarynode import BinaryNode
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
def binarytree_node():
    """
    Binary Tree should have structure
    1
    ├── 2
    │   ├── 4
    │   │   └── 8
    │   └── 5
    └── 3
        ├── 6
        └── 7
    """
    a = BinaryNode(1)
    b = BinaryNode(2, parent=a)
    c = BinaryNode(3, parent=a)
    d = BinaryNode(4, parent=b)
    e = BinaryNode(5)
    f = BinaryNode(6)
    g = BinaryNode(7)
    h = BinaryNode(8)
    d.children = [None, h]
    e.parent = b
    f.parent = c
    g.parent = c
    return a


def pytest_benchmark_scale_unit(config, unit, benchmarks, best, worst, sort):
    prefix = ""
    if unit == "seconds":
        scale = 1.0
    elif unit == "operations":
        scale = 0.001
    else:
        raise RuntimeError("Unexpected measurement unit %r" % unit)

    return prefix, scale


def assert_print_statement(func, expected, *args, **kwargs):
    captured_output = io.StringIO()
    sys.stdout = captured_output
    func(*args, **kwargs)
    sys.stdout = sys.__stdout__
    actual = captured_output.getvalue()
    assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


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

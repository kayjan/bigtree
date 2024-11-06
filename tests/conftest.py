import io
import logging
import sys
from typing import List, Union

import pytest

from bigtree.node import basenode, binarynode, dagnode, node


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
    a = basenode.BaseNode(name="a", age=90)
    b = basenode.BaseNode(name="b", age=65)
    c = basenode.BaseNode(name="c", age=60)
    d = basenode.BaseNode(name="d", age=40)
    e = basenode.BaseNode(name="e", age=35)
    f = basenode.BaseNode(name="f", age=38)
    g = basenode.BaseNode(name="g", age=10)
    h = basenode.BaseNode(name="h", age=6)

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
    a = node.Node("a", age=90)
    b = node.Node("b", age=65)
    c = node.Node("c", age=60)
    d = node.Node("d", age=40)
    e = node.Node("e", age=35)
    f = node.Node("f", age=38)
    g = node.Node("g", age=10)
    h = node.Node("h", age=6)

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
    a = node.Node("a", age=90)
    b = node.Node("b", age=65)
    c = node.Node("c", age=60)
    d = node.Node("d", age=40)
    e = node.Node("e", age=35)
    f = node.Node("f", age=38)
    g = node.Node("g", age=10)
    h = node.Node("h", age=6)
    i = node.Node("i", age=4)

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
    a = dagnode.DAGNode("a", age=90)
    b = dagnode.DAGNode("b", age=65)
    c = dagnode.DAGNode("c", age=60)
    d = dagnode.DAGNode("d", age=40)
    e = dagnode.DAGNode("e", age=35)
    f = dagnode.DAGNode("f", age=38)
    g = dagnode.DAGNode("g", age=10)
    h = dagnode.DAGNode("h", age=6)

    c.parents = [a, b]
    d.parents = [a, c]
    e.parents = [d]
    f.parents = [c, d]
    g.parents = [c]
    h.parents = [g]
    return a


@pytest.fixture
def dag_node_child():
    a = dagnode.DAGNode("a", age=90)
    b = dagnode.DAGNode("b", age=65)
    c = dagnode.DAGNode("c", age=60)
    d = dagnode.DAGNode("d", age=40)
    e = dagnode.DAGNode("e", age=35)
    f = dagnode.DAGNode("f", age=38)
    g = dagnode.DAGNode("g", age=10)
    h = dagnode.DAGNode("h", age=6)

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
    a = binarynode.BinaryNode(1)
    b = binarynode.BinaryNode(2, parent=a)
    c = binarynode.BinaryNode(3, parent=a)
    d = binarynode.BinaryNode(4, parent=b)
    e = binarynode.BinaryNode(5)
    f = binarynode.BinaryNode(6)
    g = binarynode.BinaryNode(7)
    h = binarynode.BinaryNode(8)
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

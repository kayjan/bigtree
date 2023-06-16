import io
import logging
import sys
from dataclasses import dataclass
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
def dag_node_plot():
    z = DAGNode("z")
    y = DAGNode("y")
    y.parents = [z]
    return z


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


@dataclass
class Constants:
    # binarytree/construct
    ERROR_BINARY_EMPTY_LIST = "Input list does not contain any data, check"
    ERROR_BINARY_NODE_TYPE = "Node type is not `BinaryNodeA`"

    # dag/construct
    ERROR_DAG_EMPTY_LIST = "Input list does not contain any data, check"
    ERROR_DAG_EMPTY_DICT = (
        "Dictionary does not contain any data, check `relation_attrs`"
    )
    ERROR_DAG_PARENT_KEY = (
        "Parent key parent not in dictionary, check `relation_attrs` and `parent_key`"
    )
    ERROR_DAG_PARENT_COL = "Parent column not in data, check `parent_col`"
    ERROR_DAG_CHILD_COL = "Child column not in data, check `child_col`"
    ERROR_DAG_ATTRIBUTE_COL = (
        "One or more attribute column(s) not in data, check `attribute_col`"
    )

    ERROR_DAG_EMPTY_CHILD = "Child name cannot be empty"
    ERROR_DAG_DUPLICATE_PARENT = (
        "There exists duplicate child name with different attributes"
    )
    ERROR_DAG_NODE_TYPE = "Node type is not `DAGNodeA`"

    # dag/export
    ERROR_DAG_TYPE = "Tree should be of type `DAGNode`, or inherit from `DAGNode`"

    # node/basenode
    ERROR_SET_PARENTS_ATTR = (
        "Attempting to set `parents` attribute, do you mean `parent`?"
    )
    ERROR_GET_PARENTS_ATTR = (
        "Attempting to access `parents` attribute, do you mean `parent`?"
    )
    ERROR_LOOP_PARENT = "Error setting parent: Node cannot be parent of itself"
    ERROR_LOOP_ANCESTOR = "Error setting parent: Node cannot be ancestor of itself"
    ERROR_LOOP_CHILD = "Error setting child: Node cannot be child of itself"
    ERROR_LOOP_DESCENDANT = "Error setting child: Node cannot be ancestor of itself"
    ERROR_SET_DUPLICATE_CHILD = (
        "Error setting child: Node cannot be added multiple times as a child"
    )
    ERROR_SET_DUPLICATE_PARENT = (
        "Error setting parent: Node cannot be added multiple times as a parent"
    )

    ERROR_CHILDREN_TYPE = "Children input should be list type, received input type"
    ERROR_BASENODE_CHILDREN_TYPE = (
        "Expect input to be BaseNode type, received input type"
    )
    ERROR_BASENODE_PARENT_TYPE = (
        "Expect input to be BaseNode type or NoneType, received input type"
    )

    # node/binarynode
    ERROR_BINARYNODE_CHILDREN_LENGTH = "Children input must have length 2"

    ERROR_SET_LEFT_CHILDREN = (
        "Attempting to set both left and children with mismatched values"
    )
    ERROR_SET_RIGHT_CHILDREN = (
        "Attempting to set both right and children with mismatched values"
    )
    ERROR_BINARYNODE_TYPE = (
        "Expect input to be BinaryNode type or NoneType, received input type"
    )

    # node/dagnode
    ERROR_SET_PARENT_ATTR = (
        "Attempting to set `parent` attribute, do you mean `parents`?"
    )
    ERROR_GET_PARENT_ATTR = (
        "Attempting to access `parent` attribute, do you mean `parents`?"
    )

    ERROR_DAGNODE_PARENT_TYPE = "Parents input should be list type, received input type"
    ERROR_DAGNODE_TYPE = "Expect input to be DAGNode type, received input type"

    # node/node
    ERROR_NODE_NAME = "Node must have a `name` attribute"

    ERROR_SAME_PATH = "Duplicate node with same path"

    # tree/construct
    ERROR_EMPTY_PATH = "Path is empty, check `path`"
    ERROR_EMPTY_ROW = "Data does not contain any rows, check `data`"
    ERROR_EMPTY_COL = "Data does not contain any columns, check `data`"
    ERROR_EMPTY_STRING = "Tree string does not contain any data, check `tree_string`"

    ERROR_EMPTY_DICT = "Dictionary does not contain any data, check"
    ERROR_EMPTY_LIST = "Path list does not contain any data, check"
    ERROR_DIFFERENT_ROOT = "Path does not have same root node"
    ERROR_MULTIPLE_ROOT = "Unable to determine root node"
    ERROR_DUPLICATE_PATH = "There exists duplicate path with different attributes"
    ERROR_DUPLICATE_NAME = "There exists duplicate name with different attributes"
    ERROR_DUPLICATE_PARENT = "There exists duplicate child with different parent where the child is also a parent node"
    ERROR_NODE_TYPE = "Node type is not `NodeA`"
    ERROR_PREFIX = "Invalid prefix, prefix should be unicode character or whitespace, otherwise specify one or more prefixes"
    ERROR_PREFIX_LENGTH = "Tree string have different prefix length, check branch"
    ERROR_JOIN_TYPE = "`join_type` must be one of 'inner' or 'left'"

    # tree/export
    ERROR_EXPORT_NODE_TYPE = "Tree should be of type `Node`, or inherit from `Node`"
    ERROR_CUSTOM_STYLE_SELECT = "Custom style selected, please specify the style of stem, branch, and final stem in `custom_style`"
    ERROR_CUSTOM_STYLE_DIFFERENT_LENGTH = (
        "`style_stem`, `style_branch`, and `style_stem_final` are of different length"
    )

    ERROR_ATTR_BRACKET = "Expect open and close brackets in `attr_bracket`, received"

    # tree/helper
    ERROR_NOT_FOUND = "Cannot find any node matching path_name ending with"
    ERROR_HELPER_BASENODE_TYPE = (
        "Tree should be of type `BaseNode`, or inherit from `BaseNode`"
    )

    # tree/modify
    ERROR_MERGE_CHILDREN_OR_LEAVES = "Invalid shifting, can only specify one type of merging, check `merge_children` and `merge_leaves`"
    ERROR_MODIFY_TYPE = "Invalid type, `from_paths` and `to_paths` should be list type"
    ERROR_DELETION_AND_COPY = (
        "Deletion of node will not happen if `copy=True`, check your `copy` parameter."
    )
    ERROR_INVALID_TO_PATH = "Invalid path in `to_paths` not starting with the root node. Check your `to_paths` parameter."

    ERROR_DIFFERENT_PATH_LENGTH = "Paths are different length"
    ERROR_PATH_MISMATCH = "Unable to assign from_path"
    ERROR_INVALID_FULL_PATH = (
        "Invalid path in `from_paths` not starting with the root node"
    )
    ERROR_FROM_PATH_NOT_FOUND = "Unable to find from_path"
    ERROR_SHIFT_SAME_NODE = "Attempting to shift the same node"

    # tree/search
    ERROR_ONE_ELEMENT = "Expected less than 1 element(s), found"
    ERROR_TWO_ELEMENT = "Expected less than 2 element(s), found"
    ERROR_MORE_THAN_THREE_ELEMENT = "Expected more than 3 element(s), found"
    ERROR_MORE_THAN_FOUR_ELEMENT = "Expected more than 4 element(s), found"

    # workflow/todo
    ERROR_TODO_TYPE = "Invalid data type for item"

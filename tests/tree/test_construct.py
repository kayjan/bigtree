import unittest

import pandas as pd
import polars as pl
import pytest

from bigtree.node.node import Node
from bigtree.tree.construct import (
    add_dataframe_to_tree_by_name,
    add_dataframe_to_tree_by_path,
    add_dict_to_tree_by_name,
    add_dict_to_tree_by_path,
    add_path_to_tree,
    add_polars_to_tree_by_name,
    add_polars_to_tree_by_path,
    dataframe_to_tree,
    dataframe_to_tree_by_relation,
    dict_to_tree,
    list_to_tree,
    list_to_tree_by_relation,
    nested_dict_to_tree,
    newick_to_tree,
    polars_to_tree,
    polars_to_tree_by_relation,
    str_to_tree,
)
from bigtree.tree.export import print_tree
from bigtree.tree.search import find_name, find_names
from bigtree.utils.exceptions import DuplicatedNodeError, TreeError
from tests.conftest import assert_print_statement
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
    assert_tree_structure_customnode_root_attr,
)
from tests.node.test_node import (
    assert_tree_structure_node_root,
    assert_tree_structure_node_root_sep,
)
from tests.test_constants import Constants


class NodeA(Node):
    pass


class CustomNode(Node):
    def __init__(self, name: str, custom_field: int, custom_field_str: str, **kwargs):
        super().__init__(name, **kwargs)
        self.custom_field = custom_field
        self.custom_field_str = custom_field_str


class TestAddPathToTree(unittest.TestCase):
    def setUp(self):
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
        self.root = Node("a")
        self.path_list = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]

    def tearDown(self):
        self.root = None
        self.path_list = None

    def test_add_path_to_tree(self):
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/f",
            "a/b/e/g",
            "a/b/e/h",
        ]
        for path in path_list:
            add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_leaves(self):
        for path in self.path_list:
            add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            add_path_to_tree(self.root, "")
        assert str(exc_info.value) == Constants.ERROR_NODE_PATH_EMPTY

    def test_add_path_to_tree_sep_leading(self):
        path_list = ["/a/b/d", "/a/b/e", "/a/b/e/g", "/a/b/e/h", "/a/c/f"]
        for path in path_list:
            add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_sep_trailing(self):
        path_list = ["a/b/d/", "a/b/e/", "a/b/e/g/", "a/b/e/h/", "a/c/f/"]
        for path in path_list:
            add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_sep_error(self):
        root1 = self.root.name
        root2 = "a\\b\\d"
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]

        with pytest.raises(TreeError) as exc_info:
            for path in path_list:
                add_path_to_tree(self.root, path)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )

    def test_add_path_to_tree_sep(self):
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]

        for path in path_list:
            add_path_to_tree(self.root, path, sep="\\")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_sep_tree(self):
        self.root.sep = "\\"

        for path in self.path_list:
            add_path_to_tree(self.root, path)
        assert_tree_structure_node_root_sep(self.root)

    def test_add_path_to_tree_duplicate_node_error(self):
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/d",  # duplicate
            "a/b/e/g",
            "a/b/e/h",
        ]

        with pytest.raises(DuplicatedNodeError) as exc_info:
            for path in path_list:
                add_path_to_tree(self.root, path, duplicate_name_allowed=False)
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_NAME.format(
            name="d"
        )

    def test_add_path_to_tree_duplicate_node(self):
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/d",  # duplicate
            "a/b/e/g",
            "a/b/e/h",
        ]

        for path in path_list:
            add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root, f="/a/c/d")

    def test_add_path_to_tree_node_type(self):
        root = NodeA("a")
        for path in self.path_list:
            add_path_to_tree(root, path)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_different_root_error(self):
        root1 = self.root.name
        root2 = "a/b"
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/f",
            "a/b/e/g",
            "a/b/e/h",
        ]
        with pytest.raises(TreeError) as exc_info:
            for path in path_list:
                add_path_to_tree(self.root, path, sep="-")
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )


class TestAddDictToTreeByPath(unittest.TestCase):
    def setUp(self):
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
        self.root = Node("a", age=1)
        self.paths = {
            "a": {"age": 90},
            "a/b": {"age": 65},
            "a/c": {"age": 60},
            "a/b/d": {"age": 40},
            "a/b/e": {"age": 35},
            "a/c/f": {"age": 38},
            "a/b/e/g": {"age": 10},
            "a/b/e/h": {"age": 6},
        }

    def tearDown(self):
        self.root = None
        self.paths = None

    def test_add_dict_to_tree_by_path(self):
        add_dict_to_tree_by_path(self.root, self.paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dict_to_tree_by_path_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            add_dict_to_tree_by_path(self.root, {})
        assert str(exc_info.value) == Constants.ERROR_NODE_DICT_EMPTY.format(
            parameter="path_attrs"
        )

    def test_add_dict_to_tree_by_path_sep_leading(self):
        paths = {
            "/a": {"age": 90},
            "/a/b": {"age": 65},
            "/a/c": {"age": 60},
            "/a/b/d": {"age": 40},
            "/a/b/e": {"age": 35},
            "/a/c/f": {"age": 38},
            "/a/b/e/g": {"age": 10},
            "/a/b/e/h": {"age": 6},
        }
        add_dict_to_tree_by_path(self.root, paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dict_to_tree_by_path_sep_trailing(self):
        paths = {
            "a/": {"age": 90},
            "a/b/": {"age": 65},
            "a/c/": {"age": 60},
            "a/b/d/": {"age": 40},
            "a/b/e/": {"age": 35},
            "a/c/f/": {"age": 38},
            "a/b/e/g/": {"age": 10},
            "a/b/e/h/": {"age": 6},
        }
        add_dict_to_tree_by_path(self.root, paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dict_to_tree_by_path_sep_error(self):
        root1 = self.root.name
        root2 = "a-b"
        paths = {
            "a": {"age": 90},
            "a-b": {"age": 65},
            "a-c": {"age": 60},
            "a-b-d": {"age": 40},
            "a-b-e": {"age": 35},
            "a-c-f": {"age": 38},
            "a-b-e-g": {"age": 10},
            "a-b-e-h": {"age": 6},
        }
        with pytest.raises(TreeError) as exc_info:
            add_dict_to_tree_by_path(self.root, paths)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )

    def test_add_dict_to_tree_by_path_sep(self):
        paths = {
            "a": {"age": 90},
            "a-b": {"age": 65},
            "a-c": {"age": 60},
            "a-b-d": {"age": 40},
            "a-b-e": {"age": 35},
            "a-c-f": {"age": 38},
            "a-b-e-g": {"age": 10},
            "a-b-e-h": {"age": 6},
        }
        add_dict_to_tree_by_path(self.root, paths, sep="-")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dict_to_tree_by_path_sep_tree(self):
        self.root = Node("a", age=89)
        self.root.sep = "\\"
        paths = {
            "a": {"age": 90},
            "a\\b": {"age": 65},
            "a\\c": {"age": 60},
            "a\\b\\d": {"age": 40},
            "a\\b\\e": {"age": 35},
            "a\\c\\f": {"age": 38},
            "a\\b\\e\\g": {"age": 10},
            "a\\b\\e\\h": {"age": 6},
        }
        add_dict_to_tree_by_path(self.root, paths, sep="\\")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_sep(self.root)

    def test_add_dict_to_tree_by_path_duplicate_node_error(self):
        paths = {
            "a": {"age": 90},
            "a/b": {"age": 65},
            "a/c": {"age": 60},
            "a/b/d": {"age": 40},
            "a/b/e": {"age": 35},
            "a/c/d": {"age": 38},  # duplicate
            "a/b/e/g": {"age": 10},
            "a/b/e/h": {"age": 6},
        }
        with pytest.raises(DuplicatedNodeError) as exc_info:
            add_dict_to_tree_by_path(self.root, paths, duplicate_name_allowed=False)
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_NAME.format(
            name="d"
        )

    def test_add_dict_to_tree_by_path_duplicate_node(self):
        paths = {
            "a": {"age": 90},
            "a/b": {"age": 65},
            "a/c": {"age": 60},
            "a/b/d": {"age": 40},
            "a/b/e": {"age": 35},
            "a/c/d": {"age": 38},  # duplicate
            "a/b/e/g": {"age": 10},
            "a/b/e/h": {"age": 6},
        }
        add_dict_to_tree_by_path(self.root, paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root, f=("d", 38))

    def test_add_dict_to_tree_by_path_node_type(self):
        root = NodeA("a", age=1)
        add_dict_to_tree_by_path(root, self.paths)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)

    def test_add_dict_to_tree_by_path_custom_node_type(self):
        paths = {
            "a": {"custom_field": 90, "custom_field_str": "a"},
            "a/b": {"custom_field": 65, "custom_field_str": "b"},
            "a/c": {"custom_field": 60, "custom_field_str": "c"},
            "a/b/d": {"custom_field": 40, "custom_field_str": "d"},
            "a/b/e": {"custom_field": 35, "custom_field_str": "e"},
            "a/c/f": {"custom_field": 38, "custom_field_str": "f"},
            "a/b/e/g": {"custom_field": 10, "custom_field_str": "g"},
            "a/b/e/h": {"custom_field": 6, "custom_field_str": "h"},
        }
        root = CustomNode("a", custom_field=1, custom_field_str="abc")
        add_dict_to_tree_by_path(root, paths)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_dict_to_tree_by_path_different_root_error(self):
        root1 = self.root.name
        root2 = "b"
        paths = {
            "a": {"age": 90},
            "a/b": {"age": 65},
            "a/c": {"age": 60},
            "a/b/d": {"age": 40},
            "a/b/e": {"age": 35},
            "a/c/f": {"age": 38},
            "a/b/e/g": {"age": 10},
            "b/b/e/h": {"age": 6},  # different root
        }
        with pytest.raises(TreeError) as exc_info:
            add_dict_to_tree_by_path(self.root, paths)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )


class TestAddDictToTreeByName(unittest.TestCase):
    def setUp(self):
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
        self.root = Node("a", age=1)
        self.b = Node("b", parent=self.root, age=1)
        self.c = Node("c", parent=self.root, age=1)
        self.d = NodeA("d", parent=self.b, age=1)
        self.e = NodeA("e", parent=self.b)
        self.f = NodeA("f", parent=self.c)
        self.g = NodeA("g", parent=self.e)
        self.h = NodeA("h", parent=self.e)
        self.name_dict = {
            "a": {"age": 90},
            "b": {"age": 65},
            "c": {"age": 60},
            "d": {"age": 40},
            "e": {"age": 35},
            "f": {"age": 38},
            "g": {"age": 10},
            "h": {"age": 6},
        }

    def tearDown(self):
        self.root = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None
        self.name_dict = None

    def test_add_dict_to_tree_by_name(self):
        add_dict_to_tree_by_name(self.root, self.name_dict)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dict_to_tree_by_name_different_dtype(self):
        name_dict = {
            "a": {"random": [1]},
            "b": {"random": [1, 2]},
            "c": {"random": [1, None]},
            "d": {"random": [None]},
            "e": {"random": None},
            "f": {"random": 0},
            "g": {"random": -1},
            "h": {"random": [-1]},
        }
        add_dict_to_tree_by_name(self.root, name_dict)
        nodes = ["a", "b", "c", "d", "e", "f", "g", "h"]
        expected_list = [[1], [1, 2], [1, None], [None], None, 0, -1, [-1]]
        for node_name, expected in zip(nodes, expected_list):
            actual = find_name(self.root, node_name).get_attr("random")
            assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    def test_add_dict_to_tree_by_name_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            add_dict_to_tree_by_name(self.root, {})
        assert str(exc_info.value) == Constants.ERROR_NODE_DICT_EMPTY.format(
            parameter="name_attrs"
        )

    def test_add_dict_to_tree_by_name_sep_tree(self):
        self.root.sep = "\\"
        root = add_dict_to_tree_by_name(self.root, self.name_dict)
        assert_tree_structure_node_root_sep(root)

    def test_add_dict_to_tree_by_name_duplicate_name(self):
        hh = Node("h", age=6)
        hh.parent = self.root
        add_dict_to_tree_by_name(self.root, self.name_dict)
        assert (
            len(list(find_names(self.root, "h"))) == 2
        ), "There is less node 'h' than expected"
        for _node in list(find_names(self.root, "h")):
            assert _node.get_attr("age") == 6

    def test_add_dict_to_tree_by_name_node_type(self):
        root = NodeA("a", age=1)
        b = NodeA("b", parent=root, age=1)
        c = NodeA("c", parent=root, age=1)
        d = NodeA("d", age=1)
        e = NodeA("e")
        f = NodeA("f")
        g = NodeA("g")
        h = NodeA("h")
        d.parent = b
        e.parent = b
        f.parent = c
        g.parent = e
        h.parent = e
        add_dict_to_tree_by_name(root, self.name_dict)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_dict_to_tree_by_name_custom_node_type(self):
        root = CustomNode("a", custom_field=1, custom_field_str="abc")
        b = CustomNode("b", parent=root, custom_field=1, custom_field_str="abc")
        c = CustomNode("c", parent=root, custom_field=1, custom_field_str="abc")
        _ = CustomNode("d", parent=b, custom_field=1, custom_field_str="abc")
        e = CustomNode("e", parent=b, custom_field=1, custom_field_str="abc")
        _ = CustomNode("f", parent=c, custom_field=1, custom_field_str="abc")
        _ = CustomNode("g", parent=e, custom_field=1, custom_field_str="abc")
        _ = CustomNode("h", parent=e, custom_field=1, custom_field_str="abc")
        name_dict = {
            "a": {"custom_field": 90, "custom_field_str": "a"},
            "b": {"custom_field": 65, "custom_field_str": "b"},
            "c": {"custom_field": 60, "custom_field_str": "c"},
            "d": {"custom_field": 40, "custom_field_str": "d"},
            "e": {"custom_field": 35, "custom_field_str": "e"},
            "f": {"custom_field": 38, "custom_field_str": "f"},
            "g": {"custom_field": 10, "custom_field_str": "g"},
            "h": {"custom_field": 6, "custom_field_str": "h"},
        }
        add_dict_to_tree_by_name(root, name_dict)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_dict_to_tree_by_name_inconsistent_attributes(self):
        name_dict = {
            "a": {"age": 90},
            "b": {},
            "c": {"age": 60},
        }
        add_dict_to_tree_by_name(self.root, name_dict)
        expected_root_str = "a [age=90]\n" "├── b [age=1]\n" "└── c [age=60]\n"
        assert_print_statement(
            print_tree, expected_root_str, self.root, all_attrs=True, max_depth=2
        )


class TestAddDataFrameToTreeByPath(unittest.TestCase):
    def setUp(self):
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
        self.root = Node("a", age=1)
        self.data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )

    def tearDown(self):
        self.root = None
        self.data = None

    def test_add_dataframe_to_tree_by_path(self):
        add_dataframe_to_tree_by_path(self.root, self.data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_col_name(self):
        add_dataframe_to_tree_by_path(
            self.root, self.data, path_col="PATH", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_col_name_reverse(self):
        data = pd.DataFrame(
            [
                ["a", 0],
                ["a/b", None],
                ["a/c", -1],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "value"],
        )
        add_dataframe_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)
        assert hasattr(
            self.root, "value"
        ), "Check root attribute, expected value attribute"
        assert self.root.value == 0, "Check root value, expected 0"
        assert not hasattr(
            self.root["b"], "value"
        ), "Check b attribute, expected no value attribute"
        assert self.root["c"].value == -1, "Check c value, expected -1"

    def test_add_dataframe_to_tree_by_path_zero_attribute(self):
        add_dataframe_to_tree_by_path(
            self.root,
            self.data[["age", "PATH"]],
            path_col="PATH",
            attribute_cols=["age"],
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            add_dataframe_to_tree_by_path(self.root, pd.DataFrame())
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_dataframe_to_tree_by_path_empty_row_error(self):
        data = pd.DataFrame(columns=["PATH", "age"])
        with pytest.raises(ValueError) as exc_info:
            add_dataframe_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    def test_add_dataframe_to_tree_by_path_empty_col_error(self):
        data = pd.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            add_dataframe_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_dataframe_to_tree_by_path_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(KeyError):
            add_dataframe_to_tree_by_path(
                self.root, self.data, attribute_cols=attribute_cols
            )

    def test_add_dataframe_to_tree_by_path_ignore_name_col(self):
        data = pd.DataFrame(
            [
                ["a", 90, "a1"],
                ["a/b", 65, "b1"],
                ["a/c", 60, "c1"],
                ["a/b/d", 40, "d1"],
                ["a/b/e", 35, "e1"],
                ["a/c/f", 38, "f1"],
                ["a/b/e/g", 10, "g1"],
                ["a/b/e/h", 6, "h1"],
            ],
            columns=["PATH", "age", "name"],
        )
        add_dataframe_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_ignore_non_attribute_cols(self):
        data = pd.DataFrame(
            [
                ["a", 90, "a1"],
                ["a/b", 65, "b1"],
                ["a/c", 60, "c1"],
                ["a/b/d", 40, "d1"],
                ["a/b/e", 35, "e1"],
                ["a/c/f", 38, "f1"],
                ["a/b/e/g", 10, "g1"],
                ["a/b/e/h", 6, "h1"],
            ],
            columns=["PATH", "age", "name2"],
        )
        add_dataframe_to_tree_by_path(
            self.root, data, path_col="PATH", attribute_cols=["age"]
        )
        assert not self.root.get_attr("name2")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_root_node_empty_attribute(self):
        data = pd.DataFrame(
            [
                ["a", None],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )
        add_dataframe_to_tree_by_path(self.root, data)
        assert self.root.get_attr("age") == 1
        self.root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_no_attribute(self):
        data = pd.DataFrame(
            [
                ["a"],
                ["a/b"],
                ["a/c"],
                ["a/b/d"],
                ["a/b/e"],
                ["a/c/f"],
                ["a/b/e/g"],
                ["a/b/e/h"],
            ],
            columns=["PATH"],
        )
        add_dataframe_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_sep_leading(self):
        data = pd.DataFrame(
            [
                ["/a", 90],
                ["/a/b", 65],
                ["/a/c", 60],
                ["/a/b/d", 40],
                ["/a/b/e", 35],
                ["/a/c/f", 38],
                ["/a/b/e/g", 10],
                ["/a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )
        add_dataframe_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_sep_trailing(self):
        data = pd.DataFrame(
            [
                ["a/", 90],
                ["a/b/", 65],
                ["a/c/", 60],
                ["a/b/d/", 40],
                ["a/b/e/", 35],
                ["a/c/f/", 38],
                ["a/b/e/g/", 10],
                ["a/b/e/h/", 6],
            ],
            columns=["PATH", "age"],
        )
        add_dataframe_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_sep_error(self):
        root1 = self.root.name
        root2 = "a\\b"
        data = pd.DataFrame(
            [
                ["a", 90],
                ["a\\b", 65],
                ["a\\c", 60],
                ["a\\b\\d", 40],
                ["a\\b\\e", 35],
                ["a\\c\\f", 38],
                ["a\\b\\e\\g", 10],
                ["a\\b\\e\\h", 6],
            ],
            columns=["PATH", "age"],
        )
        with pytest.raises(TreeError) as exc_info:
            add_dataframe_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )

    def test_add_dataframe_to_tree_by_path_sep(self):
        data = pd.DataFrame(
            [
                ["a", 90],
                ["a\\b", 65],
                ["a\\c", 60],
                ["a\\b\\d", 40],
                ["a\\b\\e", 35],
                ["a\\c\\f", 38],
                ["a\\b\\e\\g", 10],
                ["a\\b\\e\\h", 6],
            ],
            columns=["PATH", "age"],
        )
        add_dataframe_to_tree_by_path(self.root, data, sep="\\")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_sep_tree(self):
        self.root.sep = "\\"
        add_dataframe_to_tree_by_path(self.root, self.data)
        assert_tree_structure_node_root_sep(self.root)

    def test_add_dataframe_to_tree_by_path_duplicate_name_error(self):
        data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )
        with pytest.raises(DuplicatedNodeError) as exc_info:
            add_dataframe_to_tree_by_path(self.root, data, duplicate_name_allowed=False)
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_NAME.format(
            name="d"
        )

    def test_add_dataframe_to_tree_by_path_duplicate_name(self):
        data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )
        add_dataframe_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root, f=("d", 38))
        assert_tree_structure_node_root(self.root, f="/a/c/d")

    def test_add_dataframe_to_tree_by_path_duplicate_data_error(self):
        data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/c/d", 35],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            add_dataframe_to_tree_by_path(self.root, data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_PATH
        )

    def test_add_dataframe_to_tree_by_path_duplicate_data_and_entry_error(self):
        data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/c/d", 38],  # duplicate
                ["a/c/d", 35],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            add_dataframe_to_tree_by_path(self.root, data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_PATH
        )

    def test_add_dataframe_to_tree_by_path_duplicate_data(self):
        data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/c/d", 38],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )
        add_dataframe_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root, f=("d", 38))
        assert_tree_structure_node_root(self.root, f="/a/c/d")

    def test_add_dataframe_to_tree_by_path_node_type(self):
        root = NodeA("a", age=1)
        add_dataframe_to_tree_by_path(root, self.data)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_dataframe_to_tree_by_path_custom_node_type(self):
        root = CustomNode("a", custom_field=1, custom_field_str="abc")
        data = pd.DataFrame(
            [
                ["a", 90, "a"],
                ["a/b", 65, "b"],
                ["a/c", 60, "c"],
                ["a/b/d", 40, "d"],
                ["a/b/e", 35, "e"],
                ["a/c/f", 38, "f"],
                ["a/b/e/g", 10, "g"],
                ["a/b/e/h", 6, "h"],
            ],
            columns=["PATH", "custom_field", "custom_field_str"],
        )
        add_dataframe_to_tree_by_path(root, data)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_dataframe_to_tree_by_path_different_root_error(self):
        root1 = self.root.name
        root2 = "b"
        data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["b/b/e/h", 6],  # different root
            ],
            columns=["PATH", "age"],
        )
        with pytest.raises(TreeError) as exc_info:
            add_dataframe_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )


class TestAddDataFrameToTreeByName(unittest.TestCase):
    def setUp(self):
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
        self.root = Node("a", age=1)
        self.b = Node("b", parent=self.root, age=1)
        self.c = Node("c", parent=self.root, age=1)
        self.d = NodeA("d", parent=self.b, age=1)
        self.e = NodeA("e", parent=self.b)
        self.f = NodeA("f", parent=self.c)
        self.g = NodeA("g", parent=self.e)
        self.h = NodeA("h", parent=self.e)
        self.data = pd.DataFrame(
            [
                ["a", 90],
                ["b", 65],
                ["c", 60],
                ["d", 40],
                ["e", 35],
                ["f", 38],
                ["g", 10],
                ["h", 6],
            ],
            columns=["NAME", "age"],
        )

    def tearDown(self):
        self.root = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None
        self.data = None

    def test_add_dataframe_to_tree_by_name(self):
        add_dataframe_to_tree_by_name(self.root, self.data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_name_col_name(self):
        add_dataframe_to_tree_by_name(
            self.root, self.data, name_col="NAME", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_name_col_name_reverse(self):
        add_dataframe_to_tree_by_name(
            self.root,
            self.data[["age", "NAME"]],
            name_col="NAME",
            attribute_cols=["age"],
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_name_zero_attribute(self):
        data = pd.DataFrame(
            [
                ["a", 0],
                ["b", None],
                ["c", -1],
                ["d", 40],
                ["e", 35],
                ["f", 38],
                ["g", 10],
                ["h", 6],
            ],
            columns=["NAME", "value"],
        )
        add_dataframe_to_tree_by_name(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)
        assert hasattr(
            self.root, "value"
        ), "Check root attribute, expected value attribute"
        assert self.root.value == 0, "Check root value, expected 0"
        assert not hasattr(
            self.root["b"], "value"
        ), "Check b attribute, expected no value attribute"
        assert self.root["c"].value == -1, "Check c value, expected -1"

    def test_add_dataframe_to_tree_by_name_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            add_dataframe_to_tree_by_name(self.root, pd.DataFrame())
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_dataframe_to_tree_by_name_empty_row_error(self):
        data = pd.DataFrame(columns=["NAME", "age"])
        with pytest.raises(ValueError) as exc_info:
            add_dataframe_to_tree_by_name(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    def test_add_dataframe_to_tree_by_name_empty_col_error(self):
        data = pd.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            add_dataframe_to_tree_by_name(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_dataframe_to_tree_by_name_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(KeyError):
            add_dataframe_to_tree_by_name(
                self.root, self.data, attribute_cols=attribute_cols
            )

    def test_add_dataframe_to_tree_by_name_ignore_name_col(self):
        data = pd.DataFrame(
            [
                ["a", 90, "a1"],
                ["b", 65, "b1"],
                ["c", 60, "c1"],
                ["d", 40, "d1"],
                ["e", 35, "e1"],
                ["f", 38, "f1"],
                ["g", 10, "g1"],
                ["h", 6, "h1"],
            ],
            columns=["name2", "age", "name"],
        )
        add_dataframe_to_tree_by_name(self.root, data, name_col="name2")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_name_ignore_non_attribute_cols(self):
        data = pd.DataFrame(
            [
                ["a", 90, "a1"],
                ["b", 65, "b1"],
                ["c", 60, "c1"],
                ["d", 40, "d1"],
                ["e", 35, "e1"],
                ["f", 38, "f1"],
                ["g", 10, "g1"],
                ["h", 6, "h1"],
            ],
            columns=["NAME", "age", "name2"],
        )
        add_dataframe_to_tree_by_name(
            self.root, data, name_col="NAME", attribute_cols=["age"]
        )
        assert not self.root.get_attr("name2")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_name_root_node_empty_attribute(self):
        data = pd.DataFrame(
            [
                ["a", None],
                ["b", 65],
                ["c", 60],
                ["d", 40],
                ["e", 35],
                ["f", 38],
                ["g", 10],
                ["h", 6],
            ],
            columns=["NAME", "age"],
        )
        add_dataframe_to_tree_by_name(self.root, data)
        assert self.root.get_attr("age") == 1
        self.root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_name_sep_tree(self):
        self.root.sep = "\\"
        root = add_dataframe_to_tree_by_name(self.root, self.data)
        assert_tree_structure_node_root_sep(root)

    def test_add_dataframe_to_tree_by_name_duplicate_name(self):
        hh = Node("h")
        hh.parent = self.root
        root = add_dataframe_to_tree_by_name(self.root, self.data)
        assert (
            len(list(find_names(root, "h"))) == 2
        ), "There is less node 'h' than expected"
        for _node in list(find_names(root, "h")):
            assert _node.get_attr("age") == 6

    def test_add_dataframe_to_tree_by_name_duplicate_data_error(self):
        data = pd.DataFrame(
            [
                ["a", 90],
                ["b", 65],
                ["c", 60],
                ["d", 40],
                ["e", 35],
                ["f", 38],
                ["g", 10],
                ["g", 6],  # duplicate
            ],
            columns=["NAME", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            add_dataframe_to_tree_by_name(self.root, data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_NAME
        )

    def test_add_dataframe_to_tree_by_name_duplicate_data_and_entry_error(self):
        data = pd.DataFrame(
            [
                ["a", 90],
                ["b", 65],
                ["c", 60],
                ["d", 40],
                ["e", 35],
                ["f", 38],
                ["g", 10],
                ["g", 10],  # duplicate
                ["g", 6],  # duplicate
            ],
            columns=["NAME", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            add_dataframe_to_tree_by_name(self.root, data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_NAME
        )

    def test_add_dataframe_to_tree_by_name_node_type(self):
        root = NodeA("a", age=1)
        b = NodeA("b", parent=root, age=1)
        c = NodeA("c", parent=root, age=1)
        d = NodeA("d", age=1)
        e = NodeA("e")
        f = NodeA("f")
        g = NodeA("g")
        h = NodeA("h")
        d.parent = b
        e.parent = b
        f.parent = c
        g.parent = e
        h.parent = e
        add_dataframe_to_tree_by_name(root, self.data)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_dataframe_to_tree_by_name_custom_node_type(self):
        root = CustomNode("a", custom_field=1, custom_field_str="abc")
        b = CustomNode("b", parent=root, custom_field=1, custom_field_str="abc")
        c = CustomNode("c", parent=root, custom_field=1, custom_field_str="abc")
        _ = CustomNode("d", parent=b, custom_field=1, custom_field_str="abc")
        e = CustomNode("e", parent=b, custom_field=1, custom_field_str="abc")
        _ = CustomNode("f", parent=c, custom_field=1, custom_field_str="abc")
        _ = CustomNode("g", parent=e, custom_field=1, custom_field_str="abc")
        _ = CustomNode("h", parent=e, custom_field=1, custom_field_str="abc")
        data = pd.DataFrame(
            [
                ["a", 90, "a"],
                ["b", 65, "b"],
                ["c", 60, "c"],
                ["d", 40, "d"],
                ["e", 35, "e"],
                ["f", 38, "f"],
                ["g", 10, "g"],
                ["h", 6, "h"],
            ],
            columns=["NAME", "custom_field", "custom_field_str"],
        )
        add_dataframe_to_tree_by_name(root, data)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_dataframe_to_tree_by_name_inconsistent_attributes(self):
        data = pd.DataFrame(
            [
                ["a", 90],
                ["b", None],
                ["c", 60],
            ],
            columns=["NAME", "age"],
        )
        add_dataframe_to_tree_by_name(self.root, data)
        expected_root_str = "a [age=90.0]\n" "├── b [age=1]\n" "└── c [age=60.0]\n"
        assert_print_statement(
            print_tree, expected_root_str, self.root, all_attrs=True, max_depth=2
        )


class TestAddPolarsToTreeByPath(unittest.TestCase):
    def setUp(self):
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
        self.root = Node("a", age=1)
        self.data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )

    def tearDown(self):
        self.root = None
        self.data = None

    def test_add_polars_to_tree_by_path(self):
        add_polars_to_tree_by_path(self.root, self.data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_col_name(self):
        add_polars_to_tree_by_path(
            self.root, self.data, path_col="PATH", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_col_name_reverse(self):
        data = pl.DataFrame(
            [
                ["a", 0],
                ["a/b", None],
                ["a/c", -1],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "value"],
        )
        add_polars_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)
        assert hasattr(
            self.root, "value"
        ), "Check root attribute, expected value attribute"
        assert self.root.value == 0, "Check root value, expected 0"
        assert not hasattr(
            self.root["b"], "value"
        ), "Check b attribute, expected no value attribute"
        assert self.root["c"].value == -1, "Check c value, expected -1"

    def test_add_polars_to_tree_by_path_zero_attribute(self):
        add_polars_to_tree_by_path(
            self.root,
            self.data[["age", "PATH"]],
            path_col="PATH",
            attribute_cols=["age"],
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            add_polars_to_tree_by_path(self.root, pl.DataFrame())
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_polars_to_tree_by_path_empty_row_error(self):
        data = pl.DataFrame(schema=["PATH", "age"])
        with pytest.raises(ValueError) as exc_info:
            add_polars_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    def test_add_polars_to_tree_by_path_empty_col_error(self):
        data = pl.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            add_polars_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_polars_to_tree_by_path_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(pl.exceptions.ColumnNotFoundError):
            add_polars_to_tree_by_path(
                self.root, self.data, attribute_cols=attribute_cols
            )

    def test_add_polars_to_tree_by_path_ignore_name_col(self):
        data = pl.DataFrame(
            [
                ["a", 90, "a1"],
                ["a/b", 65, "b1"],
                ["a/c", 60, "c1"],
                ["a/b/d", 40, "d1"],
                ["a/b/e", 35, "e1"],
                ["a/c/f", 38, "f1"],
                ["a/b/e/g", 10, "g1"],
                ["a/b/e/h", 6, "h1"],
            ],
            schema=["PATH", "age", "name"],
        )
        add_polars_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_ignore_non_attribute_cols(self):
        data = pl.DataFrame(
            [
                ["a", 90, "a1"],
                ["a/b", 65, "b1"],
                ["a/c", 60, "c1"],
                ["a/b/d", 40, "d1"],
                ["a/b/e", 35, "e1"],
                ["a/c/f", 38, "f1"],
                ["a/b/e/g", 10, "g1"],
                ["a/b/e/h", 6, "h1"],
            ],
            schema=["PATH", "age", "name2"],
        )
        add_polars_to_tree_by_path(
            self.root, data, path_col="PATH", attribute_cols=["age"]
        )
        assert not self.root.get_attr("name2")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_root_node_empty_attribute(self):
        data = pl.DataFrame(
            [
                ["a", None],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        add_polars_to_tree_by_path(self.root, data)
        assert self.root.get_attr("age") == 1
        self.root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_no_attribute(self):
        data = pl.DataFrame(
            [
                ["a"],
                ["a/b"],
                ["a/c"],
                ["a/b/d"],
                ["a/b/e"],
                ["a/c/f"],
                ["a/b/e/g"],
                ["a/b/e/h"],
            ],
            schema=["PATH"],
        )
        add_polars_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_sep_leading(self):
        data = pl.DataFrame(
            [
                ["/a", 90],
                ["/a/b", 65],
                ["/a/c", 60],
                ["/a/b/d", 40],
                ["/a/b/e", 35],
                ["/a/c/f", 38],
                ["/a/b/e/g", 10],
                ["/a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        add_polars_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_sep_trailing(self):
        data = pl.DataFrame(
            [
                ["a/", 90],
                ["a/b/", 65],
                ["a/c/", 60],
                ["a/b/d/", 40],
                ["a/b/e/", 35],
                ["a/c/f/", 38],
                ["a/b/e/g/", 10],
                ["a/b/e/h/", 6],
            ],
            schema=["PATH", "age"],
        )
        add_polars_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_sep_error(self):
        root1 = self.root.name
        root2 = "a\\b"
        data = pl.DataFrame(
            [
                ["a", 90],
                ["a\\b", 65],
                ["a\\c", 60],
                ["a\\b\\d", 40],
                ["a\\b\\e", 35],
                ["a\\c\\f", 38],
                ["a\\b\\e\\g", 10],
                ["a\\b\\e\\h", 6],
            ],
            schema=["PATH", "age"],
        )
        with pytest.raises(TreeError) as exc_info:
            add_polars_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )

    def test_add_polars_to_tree_by_path_sep(self):
        data = pl.DataFrame(
            [
                ["a", 90],
                ["a\\b", 65],
                ["a\\c", 60],
                ["a\\b\\d", 40],
                ["a\\b\\e", 35],
                ["a\\c\\f", 38],
                ["a\\b\\e\\g", 10],
                ["a\\b\\e\\h", 6],
            ],
            schema=["PATH", "age"],
        )
        add_polars_to_tree_by_path(self.root, data, sep="\\")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_sep_tree(self):
        self.root.sep = "\\"
        add_polars_to_tree_by_path(self.root, self.data)
        assert_tree_structure_node_root_sep(self.root)

    def test_add_polars_to_tree_by_path_duplicate_name_error(self):
        data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        with pytest.raises(DuplicatedNodeError) as exc_info:
            add_polars_to_tree_by_path(self.root, data, duplicate_name_allowed=False)
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_NAME.format(
            name="d"
        )

    def test_add_polars_to_tree_by_path_duplicate_name(self):
        data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        add_polars_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root, f=("d", 38))
        assert_tree_structure_node_root(self.root, f="/a/c/d")

    def test_add_polars_to_tree_by_path_duplicate_data_error(self):
        data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/c/d", 35],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            add_polars_to_tree_by_path(self.root, data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_PATH
        )

    def test_add_polars_to_tree_by_path_duplicate_data_and_entry_error(self):
        data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/c/d", 38],  # duplicate
                ["a/c/d", 35],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            add_polars_to_tree_by_path(self.root, data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_PATH
        )

    def test_add_polars_to_tree_by_path_duplicate_data(self):
        data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/c/d", 38],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        add_polars_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root, f=("d", 38))
        assert_tree_structure_node_root(self.root, f="/a/c/d")

    def test_add_polars_to_tree_by_path_node_type(self):
        root = NodeA("a", age=1)
        add_polars_to_tree_by_path(root, self.data)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_polars_to_tree_by_path_custom_node_type(self):
        root = CustomNode("a", custom_field=1, custom_field_str="abc")
        data = pl.DataFrame(
            [
                ["a", 90, "a"],
                ["a/b", 65, "b"],
                ["a/c", 60, "c"],
                ["a/b/d", 40, "d"],
                ["a/b/e", 35, "e"],
                ["a/c/f", 38, "f"],
                ["a/b/e/g", 10, "g"],
                ["a/b/e/h", 6, "h"],
            ],
            schema=["PATH", "custom_field", "custom_field_str"],
        )
        add_polars_to_tree_by_path(root, data)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_polars_to_tree_by_path_different_root_error(self):
        root1 = self.root.name
        root2 = "b"
        data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["b/b/e/h", 6],  # different root
            ],
            schema=["PATH", "age"],
        )
        with pytest.raises(TreeError) as exc_info:
            add_polars_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )


class TestAddPolarsToTreeByName(unittest.TestCase):
    def setUp(self):
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
        self.root = Node("a", age=1)
        self.b = Node("b", parent=self.root, age=1)
        self.c = Node("c", parent=self.root, age=1)
        self.d = NodeA("d", parent=self.b, age=1)
        self.e = NodeA("e", parent=self.b)
        self.f = NodeA("f", parent=self.c)
        self.g = NodeA("g", parent=self.e)
        self.h = NodeA("h", parent=self.e)
        self.data = pl.DataFrame(
            [
                ["a", 90],
                ["b", 65],
                ["c", 60],
                ["d", 40],
                ["e", 35],
                ["f", 38],
                ["g", 10],
                ["h", 6],
            ],
            schema=["NAME", "age"],
        )

    def tearDown(self):
        self.root = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None
        self.data = None

    def test_add_polars_to_tree_by_name(self):
        add_polars_to_tree_by_name(self.root, self.data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_name_col_name(self):
        add_polars_to_tree_by_name(
            self.root, self.data, name_col="NAME", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_name_col_name_reverse(self):
        add_polars_to_tree_by_name(
            self.root,
            self.data[["age", "NAME"]],
            name_col="NAME",
            attribute_cols=["age"],
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_name_zero_attribute(self):
        data = pl.DataFrame(
            [
                ["a", 0],
                ["b", None],
                ["c", -1],
                ["d", 40],
                ["e", 35],
                ["f", 38],
                ["g", 10],
                ["h", 6],
            ],
            schema=["NAME", "value"],
        )
        add_polars_to_tree_by_name(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)
        assert hasattr(
            self.root, "value"
        ), "Check root attribute, expected value attribute"
        assert self.root.value == 0, "Check root value, expected 0"
        assert not hasattr(
            self.root["b"], "value"
        ), "Check b attribute, expected no value attribute"
        assert self.root["c"].value == -1, "Check c value, expected -1"

    def test_add_polars_to_tree_by_name_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            add_polars_to_tree_by_name(self.root, pl.DataFrame())
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_polars_to_tree_by_name_empty_row_error(self):
        data = pl.DataFrame(schema=["NAME", "age"])
        with pytest.raises(ValueError) as exc_info:
            add_polars_to_tree_by_name(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    def test_add_polars_to_tree_by_name_empty_col_error(self):
        data = pl.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            add_polars_to_tree_by_name(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_polars_to_tree_by_name_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(pl.exceptions.ColumnNotFoundError):
            add_polars_to_tree_by_name(
                self.root, self.data, attribute_cols=attribute_cols
            )

    def test_add_polars_to_tree_by_name_ignore_name_col(self):
        data = pl.DataFrame(
            [
                ["a", 90, "a1"],
                ["b", 65, "b1"],
                ["c", 60, "c1"],
                ["d", 40, "d1"],
                ["e", 35, "e1"],
                ["f", 38, "f1"],
                ["g", 10, "g1"],
                ["h", 6, "h1"],
            ],
            schema=["name2", "age", "name"],
        )
        add_polars_to_tree_by_name(self.root, data, name_col="name2")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_name_ignore_non_attribute_cols(self):
        data = pl.DataFrame(
            [
                ["a", 90, "a1"],
                ["b", 65, "b1"],
                ["c", 60, "c1"],
                ["d", 40, "d1"],
                ["e", 35, "e1"],
                ["f", 38, "f1"],
                ["g", 10, "g1"],
                ["h", 6, "h1"],
            ],
            schema=["NAME", "age", "name2"],
        )
        add_polars_to_tree_by_name(
            self.root, data, name_col="NAME", attribute_cols=["age"]
        )
        assert not self.root.get_attr("name2")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_name_root_node_empty_attribute(self):
        data = pl.DataFrame(
            [
                ["a", None],
                ["b", 65],
                ["c", 60],
                ["d", 40],
                ["e", 35],
                ["f", 38],
                ["g", 10],
                ["h", 6],
            ],
            schema=["NAME", "age"],
        )
        add_polars_to_tree_by_name(self.root, data)
        assert self.root.get_attr("age") == 1
        self.root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_name_sep_tree(self):
        self.root.sep = "\\"
        root = add_polars_to_tree_by_name(self.root, self.data)
        assert_tree_structure_node_root_sep(root)

    def test_add_polars_to_tree_by_name_duplicate_name(self):
        hh = Node("h")
        hh.parent = self.root
        root = add_polars_to_tree_by_name(self.root, self.data)
        assert (
            len(list(find_names(root, "h"))) == 2
        ), "There is less node 'h' than expected"
        for _node in list(find_names(root, "h")):
            assert _node.get_attr("age") == 6

    def test_add_polars_to_tree_by_name_duplicate_data_error(self):
        data = pl.DataFrame(
            [
                ["a", 90],
                ["b", 65],
                ["c", 60],
                ["d", 40],
                ["e", 35],
                ["f", 38],
                ["g", 10],
                ["g", 6],  # duplicate
            ],
            schema=["NAME", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            add_polars_to_tree_by_name(self.root, data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_NAME
        )

    def test_add_polars_to_tree_by_name_duplicate_data_and_entry_error(self):
        data = pl.DataFrame(
            [
                ["a", 90],
                ["b", 65],
                ["c", 60],
                ["d", 40],
                ["e", 35],
                ["f", 38],
                ["g", 10],
                ["g", 10],  # duplicate
                ["g", 6],  # duplicate
            ],
            schema=["NAME", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            add_polars_to_tree_by_name(self.root, data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_NAME
        )

    def test_add_polars_to_tree_by_name_node_type(self):
        root = NodeA("a", age=1)
        b = NodeA("b", parent=root, age=1)
        c = NodeA("c", parent=root, age=1)
        d = NodeA("d", age=1)
        e = NodeA("e")
        f = NodeA("f")
        g = NodeA("g")
        h = NodeA("h")
        d.parent = b
        e.parent = b
        f.parent = c
        g.parent = e
        h.parent = e
        add_polars_to_tree_by_name(root, self.data)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_polars_to_tree_by_name_custom_node_type(self):
        root = CustomNode("a", custom_field=1, custom_field_str="abc")
        b = CustomNode("b", parent=root, custom_field=1, custom_field_str="abc")
        c = CustomNode("c", parent=root, custom_field=1, custom_field_str="abc")
        _ = CustomNode("d", parent=b, custom_field=1, custom_field_str="abc")
        e = CustomNode("e", parent=b, custom_field=1, custom_field_str="abc")
        _ = CustomNode("f", parent=c, custom_field=1, custom_field_str="abc")
        _ = CustomNode("g", parent=e, custom_field=1, custom_field_str="abc")
        _ = CustomNode("h", parent=e, custom_field=1, custom_field_str="abc")
        data = pl.DataFrame(
            [
                ["a", 90, "a"],
                ["b", 65, "b"],
                ["c", 60, "c"],
                ["d", 40, "d"],
                ["e", 35, "e"],
                ["f", 38, "f"],
                ["g", 10, "g"],
                ["h", 6, "h"],
            ],
            schema=["NAME", "custom_field", "custom_field_str"],
        )
        add_polars_to_tree_by_name(root, data)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_polars_to_tree_by_name_inconsistent_attributes(self):
        data = pl.DataFrame(
            [
                ["a", 90],
                ["b", None],
                ["c", 60],
            ],
            schema=["NAME", "age"],
        )
        add_polars_to_tree_by_name(self.root, data)
        expected_root_str = "a [age=90]\n" "├── b [age=1]\n" "└── c [age=60]\n"
        assert_print_statement(
            print_tree, expected_root_str, self.root, all_attrs=True, max_depth=2
        )


class TestStrToTree(unittest.TestCase):
    def setUp(self):
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
        self.tree_str = "a\n├── b\n│   ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f"

    def test_str_to_tree(self):
        root = str_to_tree(self.tree_str)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_str_to_tree_with_prefix(self):
        root = str_to_tree(self.tree_str, tree_prefix_list=["─"])
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_str_to_tree_with_multiple_prefix(self):
        root = str_to_tree(self.tree_str, tree_prefix_list=["├──", "└──"])
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_ascii_character_error(self):
        node_str = "|-- b"
        tree_str = "a\n|-- b\n|   |-- d\n|   +-- e\n|       |-- g\n|       +-- h\n+-- c\n    +-- f"
        with pytest.raises(ValueError) as exc_info:
            str_to_tree(tree_str)
        assert str(exc_info.value) == Constants.ERROR_NODE_STRING_PREFIX.format(
            node_str=node_str
        )

    def test_ascii_character_with_prefix(self):
        tree_str = "a\n|-- b\n|   |-- d\n|   +-- e\n|       |-- g\n|       +-- h\n+-- c\n    +-- f"
        root = str_to_tree(tree_str, tree_prefix_list=["-"])
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_empty_string_error(self):
        with pytest.raises(ValueError) as exc_info:
            str_to_tree("")
        assert str(exc_info.value) == Constants.ERROR_NODE_STRING_EMPTY

    def test_empty_newline_string_error(self):
        with pytest.raises(ValueError) as exc_info:
            str_to_tree("\n\n")
        assert str(exc_info.value) == Constants.ERROR_NODE_STRING_EMPTY

    def test_unequal_prefix_length_error(self):
        branch = "│  ├── d"
        tree_str = "a\n├── b\n│  ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f"
        with pytest.raises(ValueError) as exc_info:
            str_to_tree(tree_str)
        assert str(exc_info.value) == Constants.ERROR_NODE_STRING_PREFIX_LENGTH.format(
            branch=branch
        )


class TestListToTree(unittest.TestCase):
    def setUp(self):
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
        self.path_list = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        self.path_list_full = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/f",
            "a/b/e/g",
            "a/b/e/h",
        ]

    def tearDown(self):
        self.path_list = None
        self.path_list_full = None

    def test_list_to_tree(self):
        root = list_to_tree(self.path_list_full)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_leaves(self):
        root = list_to_tree(self.path_list)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            list_to_tree([])
        assert str(exc_info.value) == Constants.ERROR_NODE_LIST_EMPTY.format(
            parameter="paths"
        )

    def test_list_to_tree_sep_leading(self):
        path_list = ["/a/b/d", "/a/b/e", "/a/b/e/g", "/a/b/e/h", "/a/c/f"]
        root = list_to_tree(path_list)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_sep_trailing(self):
        path_list = ["a/b/d/", "a/b/e/", "a/b/e/g/", "a/b/e/h/", "a/c/f/"]
        root = list_to_tree(path_list)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_sep_error(self):
        root1 = "a\\b\\d"
        root2 = "a\\b\\e"
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        with pytest.raises(TreeError) as exc_info:
            list_to_tree(path_list)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )

    def test_list_to_tree_sep(self):
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        root = list_to_tree(path_list, sep="\\")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root_sep(root)

    def test_list_to_tree_duplicate_node_error(self):
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/d",  # duplicate
            "a/b/e/g",
            "a/b/e/h",
        ]
        with pytest.raises(DuplicatedNodeError) as exc_info:
            list_to_tree(path_list, duplicate_name_allowed=False)
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_NAME.format(
            name="d"
        )

    def test_list_to_tree_duplicate_node(self):
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/d",  # duplicate
            "a/b/e/g",
            "a/b/e/h",
        ]
        root = list_to_tree(path_list)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root, f="/a/c/d")

    def test_list_to_tree_node_type(self):
        root = list_to_tree(self.path_list, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_different_root_error(self):
        root1 = "a"
        root2 = "b"
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/f",
            "a/b/e/g",
            "b/b/e/h",  # different root
        ]
        with pytest.raises(TreeError) as exc_info:
            list_to_tree(path_list)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )


class TestListToTreeByRelation(unittest.TestCase):
    def setUp(self):
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
        self.relations = [
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("b", "e"),
            ("c", "f"),
            ("e", "g"),
            ("e", "h"),
        ]
        self.relations_reverse = [
            ("e", "g"),
            ("e", "h"),
            ("b", "d"),
            ("b", "e"),
            ("c", "f"),
            ("a", "b"),
            ("a", "c"),
        ]
        self.relations_switch = [
            ("h", "g"),
            ("h", "f"),
            ("g", "e"),
            ("g", "d"),
            ("g", "a"),
            ("f", "a"),
            ("d", "b"),
            ("d", "a"),
        ]

    def tearDown(self):
        self.relations = None

    def test_list_to_tree_by_relation(self):
        root = list_to_tree_by_relation(self.relations)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_by_relation_reverse(self):
        root = list_to_tree_by_relation(self.relations_reverse)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_list_to_tree_by_relation_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            list_to_tree_by_relation([])
        assert str(exc_info.value) == Constants.ERROR_NODE_LIST_EMPTY.format(
            parameter="relations"
        )

    @staticmethod
    def test_list_to_tree_by_relation_duplicate_leaf_node():
        relations = [
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("b", "e"),
            ("b", "h"),
            ("c", "h"),
            ("e", "g"),
            ("e", "h"),
        ]
        root = list_to_tree_by_relation(relations)
        expected = """a\n├── b\n│   ├── d\n│   ├── e\n│   │   ├── g\n│   │   └── h\n│   └── h\n└── c\n    └── h\n"""
        assert_print_statement(print_tree, expected, tree=root, style="const")

    @staticmethod
    def test_list_to_tree_by_relation_duplicate_intermediate_node_error():
        relations = [
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("b", "e"),
            ("c", "e"),
            ("c", "f"),
            ("e", "g"),  # duplicate parent
            ("e", "h"),  # duplicate parent
        ]
        with pytest.raises(ValueError) as exc_info:
            list_to_tree_by_relation(relations)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DUPLICATED_INTERMEDIATE_NODE
        )

    @staticmethod
    def test_list_to_tree_by_relation_duplicate_intermediate_node_entry_error():
        relations = [
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("b", "e"),
            ("c", "e"),
            ("c", "f"),
            ("e", "g"),
            ("e", "g"),  # duplicate entry
            ("e", "h"),  # duplicate parent
        ]
        with pytest.raises(ValueError) as exc_info:
            list_to_tree_by_relation(relations)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DUPLICATED_INTERMEDIATE_NODE
        )

    @staticmethod
    def test_list_to_tree_by_relation_duplicate_intermediate_node():
        relations = [
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("b", "e"),
            ("c", "e"),
            ("c", "f"),
            ("e", "g"),  # duplicate parent
            ("e", "h"),  # duplicate parent
        ]
        root = list_to_tree_by_relation(relations, allow_duplicates=True)
        expected = (
            "a\n"
            "├── b\n"
            "│   ├── d\n"
            "│   └── e\n"
            "│       ├── g\n"
            "│       └── h\n"
            "└── c\n"
            "    ├── e\n"
            "    │   ├── g\n"
            "    │   └── h\n"
            "    └── f\n"
        )
        assert_print_statement(print_tree, expected, tree=root)

    def test_list_to_tree_by_relation_empty_parent(self):
        self.relations.append((None, "a"))
        root = list_to_tree_by_relation(self.relations)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_list_to_tree_by_relation_one_tuple():
        root = list_to_tree_by_relation([(None, "a")])
        assert root.max_depth == 1, "Max depth is wrong"
        assert root.node_name == "a", "Node name is wrong"

    def test_list_to_tree_by_relation_switch_order(self):
        root = list_to_tree_by_relation(self.relations_switch)
        expected = (
            "h\n"
            "├── g\n"
            "│   ├── e\n"
            "│   ├── d\n"
            "│   │   ├── b\n"
            "│   │   └── a\n"
            "│   └── a\n"
            "└── f\n"
            "    └── a\n"
        )
        assert_print_statement(print_tree, expected, root)

    def test_list_to_tree_by_relation_switch_order_reverse(self):
        root = list_to_tree_by_relation(self.relations_switch[::-1])
        expected = (
            "h\n"
            "├── f\n"
            "│   └── a\n"
            "└── g\n"
            "    ├── a\n"
            "    ├── d\n"
            "    │   ├── a\n"
            "    │   └── b\n"
            "    └── e\n"
        )
        assert_print_statement(print_tree, expected, root)


class TestDictToTree(unittest.TestCase):
    def setUp(self):
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
        self.path_dict = {
            "a": {"age": 90},
            "a/b": {"age": 65},
            "a/c": {"age": 60},
            "a/b/d": {"age": 40},
            "a/b/e": {"age": 35},
            "a/c/f": {"age": 38},
            "a/b/e/g": {"age": 10},
            "a/b/e/h": {"age": 6},
        }

    def tearDown(self):
        self.path_dict = None

    def test_dict_to_tree(self):
        root = dict_to_tree(self.path_dict)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dict_to_tree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            dict_to_tree({})
        assert str(exc_info.value) == Constants.ERROR_NODE_DICT_EMPTY.format(
            parameter="path_attrs"
        )

    @staticmethod
    def test_dict_to_tree_sep_leading():
        paths = {
            "/a": {"age": 90},
            "/a/b": {"age": 65},
            "/a/c": {"age": 60},
            "/a/b/d": {"age": 40},
            "/a/b/e": {"age": 35},
            "/a/c/f": {"age": 38},
            "/a/b/e/g": {"age": 10},
            "/a/b/e/h": {"age": 6},
        }
        root = dict_to_tree(paths)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dict_to_tree_sep_trailing():
        paths = {
            "a/": {"age": 90},
            "a/b/": {"age": 65},
            "a/c/": {"age": 60},
            "a/b/d/": {"age": 40},
            "a/b/e/": {"age": 35},
            "a/c/f/": {"age": 38},
            "a/b/e/g/": {"age": 10},
            "a/b/e/h/": {"age": 6},
        }
        root = dict_to_tree(paths)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dict_to_tree_sep_error():
        root1 = "a"
        root2 = "a-b"
        paths = {
            "a": {"age": 90},
            "a-b": {"age": 65},
            "a-c": {"age": 60},
            "a-b-d": {"age": 40},
            "a-b-e": {"age": 35},
            "a-c-f": {"age": 38},
            "a-b-e-g": {"age": 10},
            "a-b-e-h": {"age": 6},
        }
        with pytest.raises(TreeError) as exc_info:
            dict_to_tree(paths)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )

    @staticmethod
    def test_dict_to_tree_sep():
        paths = {
            "a": {"age": 90},
            "a\\b": {"age": 65},
            "a\\c": {"age": 60},
            "a\\b\\d": {"age": 40},
            "a\\b\\e": {"age": 35},
            "a\\c\\f": {"age": 38},
            "a\\b\\e\\g": {"age": 10},
            "a\\b\\e\\h": {"age": 6},
        }
        root = dict_to_tree(paths, sep="\\")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_sep(root)

    @staticmethod
    def test_dict_to_tree_duplicate_node_error():
        path_dict = {
            "a": {"age": 90},
            "a/b": {"age": 65},
            "a/c": {"age": 60},
            "a/b/d": {"age": 40},
            "a/b/e": {"age": 35},
            "a/c/d": {"age": 38},  # duplicate
            "a/b/e/g": {"age": 10},
            "a/b/e/h": {"age": 6},
        }
        with pytest.raises(DuplicatedNodeError) as exc_info:
            dict_to_tree(path_dict, duplicate_name_allowed=False)
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_NAME.format(
            name="d"
        )

    @staticmethod
    def test_dict_to_tree_duplicate_node():
        path_dict = {
            "a": {"age": 90},
            "a/b": {"age": 65},
            "a/c": {"age": 60},
            "a/b/d": {"age": 40},
            "a/b/e": {"age": 35},
            "a/c/d": {"age": 38},  # duplicate
            "a/b/e/g": {"age": 10},
            "a/b/e/h": {"age": 6},
        }
        root = dict_to_tree(path_dict)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root, f=("d", 38))
        assert_tree_structure_node_root(root, f="/a/c/d")

    def test_dict_to_tree_node_type(self):
        root = dict_to_tree(self.path_dict, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dict_to_tree_custom_node_type(self):
        path_dict = {
            "a": {"custom_field": 90, "custom_field_str": "a"},
            "a/b": {"custom_field": 65, "custom_field_str": "b"},
            "a/c": {"custom_field": 60, "custom_field_str": "c"},
            "a/b/d": {"custom_field": 40, "custom_field_str": "d"},
            "a/b/e": {"custom_field": 35, "custom_field_str": "e"},
            "a/c/f": {"custom_field": 38, "custom_field_str": "f"},
            "a/b/e/g": {"custom_field": 10, "custom_field_str": "g"},
            "a/b/e/h": {"custom_field": 6, "custom_field_str": "h"},
        }
        root = dict_to_tree(path_dict, node_type=CustomNode)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dict_to_tree_different_root_error():
        root1 = "a"
        root2 = "b"
        path_dict = {
            "a": {"age": 90},
            "a/b": {"age": 65},
            "a/c": {"age": 60},
            "a/b/d": {"age": 40},
            "a/b/e": {"age": 35},
            "a/c/f": {"age": 38},
            "a/b/e/g": {"age": 10},
            "b/b/e/h": {"age": 6},  # different root
        }
        with pytest.raises(TreeError) as exc_info:
            dict_to_tree(path_dict)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )

    @staticmethod
    def test_dict_to_tree_inconsistent_attributes():
        path_dict = {
            "a": {"age": 90},
            "a/b": {},
            "a/c": {"age": 60},
        }
        root = dict_to_tree(path_dict)
        expected_root_str = "a [age=90]\n" "├── b\n" "└── c [age=60]\n"
        assert_print_statement(print_tree, expected_root_str, root, all_attrs=True)


class TestNestedDictToTree(unittest.TestCase):
    def setUp(self):
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
        self.path_dict = {
            "name": "a",
            "age": 90,
            "children": [
                {
                    "name": "b",
                    "age": 65,
                    "children": [
                        {"name": "d", "age": 40},
                        {
                            "name": "e",
                            "age": 35,
                            "children": [
                                {"name": "g", "age": 10},
                                {"name": "h", "age": 6},
                            ],
                        },
                    ],
                },
                {"name": "c", "age": 60, "children": [{"name": "f", "age": 38}]},
            ],
        }

    def tearDown(self):
        self.path_dict = None

    def test_nested_dict_to_tree(self):
        root = nested_dict_to_tree(self.path_dict)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_nested_dict_to_tree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            nested_dict_to_tree({})
        assert str(exc_info.value) == Constants.ERROR_NODE_DICT_EMPTY.format(
            parameter="node_attrs"
        )

    def test_nested_dict_to_tree_null_children_error(self):
        child_key = "children"
        child = None
        path_dict = {
            "name": "a",
            "age": 90,
            "children": [
                {
                    "name": "b",
                    "age": 65,
                    "children": [
                        {"name": "d", "age": 40},
                        {
                            "name": "e",
                            "age": 35,
                            "children": [
                                {"name": "g", "age": 10, "children": child},
                            ],
                        },
                    ],
                },
            ],
        }
        with pytest.raises(TypeError) as exc_info:
            nested_dict_to_tree(path_dict)
        assert str(exc_info.value) == Constants.ERROR_NODE_DICT_CHILD_TYPE.format(
            child_key=child_key, child=child
        )

    def test_nested_dict_to_tree_int_children_error(self):
        child_key = "children"
        child = 1
        path_dict = {
            "name": "a",
            "age": 90,
            "children": [
                {
                    "name": "b",
                    "age": 65,
                    "children": [
                        {"name": "d", "age": 40},
                        {
                            "name": "e",
                            "age": 35,
                            "children": [
                                {"name": "g", "age": 10, "children": child},
                            ],
                        },
                    ],
                },
            ],
        }
        with pytest.raises(TypeError) as exc_info:
            nested_dict_to_tree(path_dict)
        assert str(exc_info.value) == Constants.ERROR_NODE_DICT_CHILD_TYPE.format(
            child_key=child_key, child=child
        )

    @staticmethod
    def test_nested_dict_to_tree_key_name():
        path_dict = {
            "node_name": "a",
            "age": 90,
            "node_children": [
                {
                    "node_name": "b",
                    "age": 65,
                    "node_children": [
                        {"node_name": "d", "age": 40},
                        {
                            "node_name": "e",
                            "age": 35,
                            "node_children": [
                                {"node_name": "g", "age": 10},
                                {"node_name": "h", "age": 6},
                            ],
                        },
                    ],
                },
                {
                    "node_name": "c",
                    "age": 60,
                    "node_children": [{"node_name": "f", "age": 38}],
                },
            ],
        }
        root = nested_dict_to_tree(
            path_dict, name_key="node_name", child_key="node_children"
        )
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_nested_dict_to_tree_node_type(self):
        root = nested_dict_to_tree(self.path_dict, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_nested_dict_to_tree_custom_node_type(self):
        path_dict = {
            "name": "a",
            "custom_field": 90,
            "custom_field_str": "a",
            "children": [
                {
                    "name": "b",
                    "custom_field": 65,
                    "custom_field_str": "b",
                    "children": [
                        {"name": "d", "custom_field": 40, "custom_field_str": "d"},
                        {
                            "name": "e",
                            "custom_field": 35,
                            "custom_field_str": "e",
                            "children": [
                                {
                                    "name": "g",
                                    "custom_field": 10,
                                    "custom_field_str": "g",
                                },
                                {
                                    "name": "h",
                                    "custom_field": 6,
                                    "custom_field_str": "h",
                                },
                            ],
                        },
                    ],
                },
                {
                    "name": "c",
                    "custom_field": 60,
                    "custom_field_str": "c",
                    "children": [
                        {
                            "name": "f",
                            "custom_field": 38,
                            "custom_field_str": "f",
                        }
                    ],
                },
            ],
        }
        root = nested_dict_to_tree(path_dict, node_type=CustomNode)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)


class TestDataFrameToTree(unittest.TestCase):
    def setUp(self):
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
        self.path_data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )

    def tearDown(self):
        self.path_data = None

    def test_dataframe_to_tree(self):
        root = dataframe_to_tree(self.path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_col_name(self):
        root = dataframe_to_tree(
            self.path_data, path_col="PATH", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_col_name_reverse(self):
        root = dataframe_to_tree(self.path_data[["age", "PATH"]], path_col="PATH")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dataframe_to_tree_no_attribute():
        path_data = pd.DataFrame(
            [
                ["a"],
                ["a/b"],
                ["a/c"],
                ["a/b/d"],
                ["a/b/e"],
                ["a/c/f"],
                ["a/b/e/g"],
                ["a/b/e/h"],
            ],
            columns=["PATH"],
        )
        root = dataframe_to_tree(path_data)
        assert_tree_structure_basenode_root(root)

    @staticmethod
    def test_dataframe_to_tree_zero_attribute():
        path_data = pd.DataFrame(
            [
                ["a", 0],
                ["a/b", None],
                ["a/c", -1],
                ["a/b/d", 1],
                ["a/b/e", 1],
                ["a/c/f", 1],
                ["a/b/e/g", 1],
                ["a/b/e/h", 1],
            ],
            columns=["PATH", "value"],
        )
        root = dataframe_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert hasattr(root, "value"), "Check root attribute, expected value attribute"
        assert root.value == 0, "Check root value, expected 0"
        assert not hasattr(
            root["b"], "value"
        ), "Check b attribute, expected no value attribute"
        assert root["c"].value == -1, "Check c value, expected -1"

    @staticmethod
    def test_dataframe_to_tree_empty_row_error():
        path_data = pd.DataFrame(columns=["PATH", "age"])
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    @staticmethod
    def test_dataframe_to_tree_empty_col_error():
        path_data = pd.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_dataframe_to_tree_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(KeyError):
            dataframe_to_tree(self.path_data, attribute_cols=attribute_cols)

    @staticmethod
    def test_dataframe_to_tree_ignore_name_col():
        path_data = pd.DataFrame(
            [
                ["a", 90, "a1"],
                ["a/b", 65, "b1"],
                ["a/c", 60, "c1"],
                ["a/b/d", 40, "d1"],
                ["a/b/e", 35, "e1"],
                ["a/c/f", 38, "f1"],
                ["a/b/e/g", 10, "g1"],
                ["a/b/e/h", 6, "h1"],
            ],
            columns=["PATH", "age", "name"],
        )
        root = dataframe_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dataframe_to_tree_ignore_non_attribute_cols():
        path_data = pd.DataFrame(
            [
                ["a", 90, "a1"],
                ["a/b", 65, "b1"],
                ["a/c", 60, "c1"],
                ["a/b/d", 40, "d1"],
                ["a/b/e", 35, "e1"],
                ["a/c/f", 38, "f1"],
                ["a/b/e/g", 10, "g1"],
                ["a/b/e/h", 6, "h1"],
            ],
            columns=["PATH", "age", "name2"],
        )
        root = dataframe_to_tree(path_data, path_col="PATH", attribute_cols=["age"])
        assert not root.get_attr("name2")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dataframe_to_tree_root_node_empty_attribute():
        path_data = pd.DataFrame(
            [
                ["a", None],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )
        root = dataframe_to_tree(path_data)
        assert not root.get_attr("age")
        root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dataframe_to_tree_sep_leading():
        path_data = pd.DataFrame(
            [
                ["/a", 90],
                ["/a/b", 65],
                ["/a/c", 60],
                ["/a/b/d", 40],
                ["/a/b/e", 35],
                ["/a/c/f", 38],
                ["/a/b/e/g", 10],
                ["/a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )
        root = dataframe_to_tree(path_data)
        assert path_data["PATH"][0].startswith("/"), "Original dataframe changed"
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_sep_trailing(self):
        path_data = pd.DataFrame(
            [
                ["a/", 90],
                ["a/b/", 65],
                ["a/c/", 60],
                ["a/b/d/", 40],
                ["a/b/e/", 35],
                ["a/c/f/", 38],
                ["a/b/e/g/", 10],
                ["a/b/e/h/", 6],
            ],
            columns=["PATH", "age"],
        )
        root = dataframe_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_sep_error(self):
        root1 = "a"
        root2 = "a\\b"
        path_data = pd.DataFrame(
            [
                ["a", 90],
                ["a\\b", 65],
                ["a\\c", 60],
                ["a\\b\\d", 40],
                ["a\\b\\e", 35],
                ["a\\c\\f", 38],
                ["a\\b\\e\\g", 10],
                ["a\\b\\e\\h", 6],
            ],
            columns=["PATH", "age"],
        )
        with pytest.raises(TreeError) as exc_info:
            dataframe_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )

    def test_dataframe_to_tree_sep(self):
        path_data = pd.DataFrame(
            [
                ["a", 90],
                ["a\\b", 65],
                ["a\\c", 60],
                ["a\\b\\d", 40],
                ["a\\b\\e", 35],
                ["a\\c\\f", 38],
                ["a\\b\\e\\g", 10],
                ["a\\b\\e\\h", 6],
            ],
            columns=["PATH", "age"],
        )
        root = dataframe_to_tree(path_data, sep="\\")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_sep(root)

    @staticmethod
    def test_dataframe_to_tree_duplicate_data_error():
        path_data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
                ["a/b/e/h", 7],  # duplicate
            ],
            columns=["PATH", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree(path_data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_PATH
        )

    @staticmethod
    def test_dataframe_to_tree_duplicate_data_and_entry_error():
        path_data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
                ["a/b/e/h", 6],  # duplicate
                ["a/b/e/h", 7],  # duplicate
            ],
            columns=["PATH", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree(path_data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_PATH
        )

    @staticmethod
    def test_dataframe_to_tree_duplicate_data():
        path_data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
                ["a/b/e/h", 6],  # duplicate
            ],
            columns=["PATH", "age"],
        )
        root = dataframe_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dataframe_to_tree_duplicate_node_error():
        path_data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )
        with pytest.raises(DuplicatedNodeError) as exc_info:
            dataframe_to_tree(path_data, duplicate_name_allowed=False)
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_NAME.format(
            name="d"
        )

    @staticmethod
    def test_dataframe_to_tree_duplicate_node():
        path_data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            columns=["PATH", "age"],
        )
        root = dataframe_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root, f=("d", 38))
        assert_tree_structure_node_root(root, f="/a/c/d")

    def test_dataframe_to_tree_node_type(self):
        root = dataframe_to_tree(self.path_data, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_custom_node_type(self):
        path_data = pd.DataFrame(
            [
                ["a", 90, "a"],
                ["a/b", 65, "b"],
                ["a/c", 60, "c"],
                ["a/b/d", 40, "d"],
                ["a/b/e", 35, "e"],
                ["a/c/f", 38, "f"],
                ["a/b/e/g", 10, "g"],
                ["a/b/e/h", 6, "h"],
            ],
            columns=["PATH", "custom_field", "custom_field_str"],
        )
        root = dataframe_to_tree(path_data, node_type=CustomNode)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dataframe_to_tree_different_root_error():
        root1 = "a"
        root2 = "b"
        path_data = pd.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["b/b/e/h", 6],  # different root
            ],
            columns=["PATH", "age"],
        )
        with pytest.raises(TreeError) as exc_info:
            dataframe_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )


class TestDataFrameToTreeByRelation(unittest.TestCase):
    def setUp(self):
        self.relation_data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "age"],
        )

    def tearDown(self):
        self.relation_data = None

    def test_dataframe_to_tree_by_relation(self):
        root = dataframe_to_tree_by_relation(self.relation_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_by_relation_col_name(self):
        root = dataframe_to_tree_by_relation(
            self.relation_data,
            child_col="child",
            parent_col="parent",
            attribute_cols=["age"],
        )
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_by_relation_col_name_reverse(self):
        root = dataframe_to_tree_by_relation(
            self.relation_data[["age", "parent", "child"]],
            child_col="child",
            parent_col="parent",
            attribute_cols=["age"],
        )
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dataframe_to_tree_by_relation_zero_attribute():
        relation_data = pd.DataFrame(
            [
                ["a", None, 0],
                ["b", "a", None],
                ["c", "a", -1],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "value"],
        )
        root = dataframe_to_tree_by_relation(relation_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)
        assert hasattr(root, "value"), "Check root attribute, expected value attribute"
        assert root.value == 0, "Check root value, expected 0"
        assert not hasattr(
            root["b"], "value"
        ), "Check b attribute, expected no value attribute"
        assert root["c"].value == -1, "Check c value, expected -1"

    @staticmethod
    def test_dataframe_to_tree_by_relation_empty_row_error():
        relation_data = pd.DataFrame(columns=["child", "parent"])
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(relation_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    @staticmethod
    def test_dataframe_to_tree_by_relation_empty_col_error():
        relation_data = pd.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(relation_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_dataframe_to_tree_by_relation_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(KeyError):
            dataframe_to_tree_by_relation(
                self.relation_data, attribute_cols=attribute_cols
            )

    @staticmethod
    def test_dataframe_to_tree_by_relation_ignore_name_col():
        relation_data = pd.DataFrame(
            [
                ["a", None, 90, "a1"],
                ["b", "a", 65, "b1"],
                ["c", "a", 60, "c1"],
                ["d", "b", 40, "d1"],
                ["e", "b", 35, "e1"],
                ["f", "c", 38, "f1"],
                ["g", "e", 10, "g1"],
                ["h", "e", 6, "h1"],
            ],
            columns=["child", "parent", "age", "name"],
        )
        root = dataframe_to_tree_by_relation(relation_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dataframe_to_tree_by_relation_ignore_non_attribute_cols():
        relation_data = pd.DataFrame(
            [
                ["a", None, 90, "a1"],
                ["b", "a", 65, "b1"],
                ["c", "a", 60, "c1"],
                ["d", "b", 40, "d1"],
                ["e", "b", 35, "e1"],
                ["f", "c", 38, "f1"],
                ["g", "e", 10, "g1"],
                ["h", "e", 6, "h1"],
            ],
            columns=["child", "parent", "age", "name2"],
        )
        root = dataframe_to_tree_by_relation(
            relation_data,
            child_col="child",
            parent_col="parent",
            attribute_cols=["age"],
        )
        assert not root.get_attr("name2")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dataframe_to_tree_by_relation_root_node_empty_attribute():
        relation_data = pd.DataFrame(
            [
                ["a", None, None],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "age"],
        )
        root = dataframe_to_tree_by_relation(relation_data)
        assert not root.get_attr("age")
        root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dataframe_to_tree_by_relation_duplicate_leaf_node():
        relation_data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["h", "b", 1],  # duplicate
                ["h", "c", 2],  # duplicate
                ["g", "e", 10],
                ["h", "e", 6],  # duplicate
            ],
            columns=["child", "parent", "age"],
        )
        root = dataframe_to_tree_by_relation(relation_data)
        expected = (
            "a\n"
            "├── b\n"
            "│   ├── d\n"
            "│   ├── e\n"
            "│   │   ├── g\n"
            "│   │   └── h\n"
            "│   └── h\n"
            "└── c\n"
            "    └── h\n"
        )
        assert_print_statement(print_tree, expected, tree=root, style="const")

    @staticmethod
    def test_dataframe_to_tree_by_relation_duplicate_intermediate_node_error():
        relation_data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["e", "c", 1],  # duplicate parent
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(relation_data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DUPLICATED_INTERMEDIATE_NODE
        )

    @staticmethod
    def test_dataframe_to_tree_by_relation_duplicate_intermediate_node_entry_error():
        relation_data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["e", "b", 35],  # duplicate entry
                ["e", "c", 1],  # duplicate parent
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(relation_data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DUPLICATED_INTERMEDIATE_NODE
        )

    @staticmethod
    def test_dataframe_to_tree_by_relation_duplicate_intermediate_node():
        relation_data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["e", "c", 1],  # duplicate intermediate node
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "age"],
        )
        root = dataframe_to_tree_by_relation(relation_data, allow_duplicates=True)
        actual = len(list(root.descendants))
        assert actual == 10, f"Expected tree to have 10 descendants, received {actual}"

    def test_dataframe_to_tree_by_relation_node_type(self):
        root = dataframe_to_tree_by_relation(self.relation_data, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_by_relation_custom_node_type(self):
        relation_data = pd.DataFrame(
            [
                ["a", None, 90, "a"],
                ["b", "a", 65, "b"],
                ["c", "a", 60, "c"],
                ["d", "b", 40, "d"],
                ["e", "b", 35, "e"],
                ["f", "c", 38, "f"],
                ["g", "e", 10, "g"],
                ["h", "e", 6, "h"],
            ],
            columns=["child", "parent", "custom_field", "custom_field_str"],
        )
        root = dataframe_to_tree_by_relation(relation_data, node_type=CustomNode)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_dataframe_to_tree_by_relation_multiple_root_parent_none_error():
        relation_data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", None, 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(relation_data)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_DATAFRAME_MULTIPLE_ROOT.format(root_nodes=["a", "b"])

    @staticmethod
    def test_dataframe_to_tree_by_relation_multiple_root_error():
        relation_data = pd.DataFrame(
            [
                ["a", None, 90],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(relation_data)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_DATAFRAME_MULTIPLE_ROOT.format(root_nodes=["a", "b"])

    @staticmethod
    def test_dataframe_to_tree_by_relation_multiple_root_and_type_error():
        relation_data = pd.DataFrame(
            [
                ["a", None, 90],
                ["c", "a", 60],
                ["d", 1, 40],
                ["e", 1, 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(relation_data)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_DATAFRAME_MULTIPLE_ROOT.format(root_nodes=[1, "a"])

    @staticmethod
    def test_dataframe_to_tree_by_relation_no_root_error():
        relation_data = pd.DataFrame(
            [
                ["a", "b", 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(relation_data)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_DATAFRAME_MULTIPLE_ROOT.format(root_nodes=[])


class TestPolarsToTree(unittest.TestCase):
    def setUp(self):
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
        self.path_data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )

    def tearDown(self):
        self.path_data = None

    def test_polars_to_tree(self):
        root = polars_to_tree(self.path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_col_name(self):
        root = polars_to_tree(self.path_data, path_col="PATH", attribute_cols=["age"])
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_col_name_reverse(self):
        root = polars_to_tree(self.path_data[["age", "PATH"]], path_col="PATH")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_no_attribute():
        path_data = pl.DataFrame(
            [
                ["a"],
                ["a/b"],
                ["a/c"],
                ["a/b/d"],
                ["a/b/e"],
                ["a/c/f"],
                ["a/b/e/g"],
                ["a/b/e/h"],
            ],
            schema=["PATH"],
        )
        root = polars_to_tree(path_data)
        assert_tree_structure_basenode_root(root)

    @staticmethod
    def test_polars_to_tree_zero_attribute():
        path_data = pl.DataFrame(
            [
                ["a", 0],
                ["a/b", None],
                ["a/c", -1],
                ["a/b/d", 1],
                ["a/b/e", 1],
                ["a/c/f", 1],
                ["a/b/e/g", 1],
                ["a/b/e/h", 1],
            ],
            schema=["PATH", "value"],
        )
        root = polars_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert hasattr(root, "value"), "Check root attribute, expected value attribute"
        assert root.value == 0, "Check root value, expected 0"
        assert not hasattr(
            root["b"], "value"
        ), "Check b attribute, expected no value attribute"
        assert root["c"].value == -1, "Check c value, expected -1"

    @staticmethod
    def test_polars_to_tree_empty_row_error():
        path_data = pl.DataFrame(schema=["PATH", "age"])
        with pytest.raises(ValueError) as exc_info:
            polars_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    @staticmethod
    def test_polars_to_tree_empty_col_error():
        path_data = pl.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            polars_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_polars_to_tree_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(pl.exceptions.ColumnNotFoundError):
            polars_to_tree(self.path_data, attribute_cols=attribute_cols)

    @staticmethod
    def test_polars_to_tree_ignore_name_col():
        path_data = pl.DataFrame(
            [
                ["a", 90, "a1"],
                ["a/b", 65, "b1"],
                ["a/c", 60, "c1"],
                ["a/b/d", 40, "d1"],
                ["a/b/e", 35, "e1"],
                ["a/c/f", 38, "f1"],
                ["a/b/e/g", 10, "g1"],
                ["a/b/e/h", 6, "h1"],
            ],
            schema=["PATH", "age", "name"],
        )
        root = polars_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_ignore_non_attribute_cols():
        path_data = pl.DataFrame(
            [
                ["a", 90, "a1"],
                ["a/b", 65, "b1"],
                ["a/c", 60, "c1"],
                ["a/b/d", 40, "d1"],
                ["a/b/e", 35, "e1"],
                ["a/c/f", 38, "f1"],
                ["a/b/e/g", 10, "g1"],
                ["a/b/e/h", 6, "h1"],
            ],
            schema=["PATH", "age", "name2"],
        )
        root = polars_to_tree(path_data, path_col="PATH", attribute_cols=["age"])
        assert not root.get_attr("name2")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_root_node_empty_attribute():
        path_data = pl.DataFrame(
            [
                ["a", None],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        root = polars_to_tree(path_data)
        assert not root.get_attr("age")
        root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_root_node_missing():
        path_data = pl.DataFrame(
            [
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        root = polars_to_tree(path_data)
        assert not root.get_attr("age")
        root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_sep_leading():
        path_data = pl.DataFrame(
            [
                ["/a", 90],
                ["/a/b", 65],
                ["/a/c", 60],
                ["/a/b/d", 40],
                ["/a/b/e", 35],
                ["/a/c/f", 38],
                ["/a/b/e/g", 10],
                ["/a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        root = polars_to_tree(path_data)
        assert path_data["PATH"][0].startswith("/"), "Original dataframe changed"
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_sep_trailing(self):
        path_data = pl.DataFrame(
            [
                ["a/", 90],
                ["a/b/", 65],
                ["a/c/", 60],
                ["a/b/d/", 40],
                ["a/b/e/", 35],
                ["a/c/f/", 38],
                ["a/b/e/g/", 10],
                ["a/b/e/h/", 6],
            ],
            schema=["PATH", "age"],
        )
        root = polars_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_sep_error(self):
        root1 = "a"
        root2 = "a\\b"
        path_data = pl.DataFrame(
            [
                ["a", 90],
                ["a\\b", 65],
                ["a\\c", 60],
                ["a\\b\\d", 40],
                ["a\\b\\e", 35],
                ["a\\c\\f", 38],
                ["a\\b\\e\\g", 10],
                ["a\\b\\e\\h", 6],
            ],
            schema=["PATH", "age"],
        )
        with pytest.raises(TreeError) as exc_info:
            polars_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )

    def test_polars_to_tree_sep(self):
        path_data = pl.DataFrame(
            [
                ["a", 90],
                ["a\\b", 65],
                ["a\\c", 60],
                ["a\\b\\d", 40],
                ["a\\b\\e", 35],
                ["a\\c\\f", 38],
                ["a\\b\\e\\g", 10],
                ["a\\b\\e\\h", 6],
            ],
            schema=["PATH", "age"],
        )
        root = polars_to_tree(path_data, sep="\\")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_sep(root)

    @staticmethod
    def test_polars_to_tree_duplicate_data_error():
        path_data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
                ["a/b/e/h", 7],  # duplicate
            ],
            schema=["PATH", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            polars_to_tree(path_data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_PATH
        )

    @staticmethod
    def test_polars_to_tree_duplicate_data_and_entry_error():
        path_data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
                ["a/b/e/h", 6],  # duplicate
                ["a/b/e/h", 7],  # duplicate
            ],
            schema=["PATH", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            polars_to_tree(path_data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DATAFRAME_DUPLICATE_PATH
        )

    @staticmethod
    def test_polars_to_tree_duplicate_data():
        path_data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
                ["a/b/e/h", 6],  # duplicate
            ],
            schema=["PATH", "age"],
        )
        root = polars_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_duplicate_node_error():
        path_data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        with pytest.raises(DuplicatedNodeError) as exc_info:
            polars_to_tree(path_data, duplicate_name_allowed=False)
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_NAME.format(
            name="d"
        )

    @staticmethod
    def test_polars_to_tree_duplicate_node():
        path_data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/d", 38],  # duplicate
                ["a/b/e/g", 10],
                ["a/b/e/h", 6],
            ],
            schema=["PATH", "age"],
        )
        root = polars_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root, f=("d", 38))
        assert_tree_structure_node_root(root, f="/a/c/d")

    def test_polars_to_tree_node_type(self):
        root = polars_to_tree(self.path_data, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_custom_node_type(self):
        path_data = pl.DataFrame(
            [
                ["a", 90, "a"],
                ["a/b", 65, "b"],
                ["a/c", 60, "c"],
                ["a/b/d", 40, "d"],
                ["a/b/e", 35, "e"],
                ["a/c/f", 38, "f"],
                ["a/b/e/g", 10, "g"],
                ["a/b/e/h", 6, "h"],
            ],
            schema=["PATH", "custom_field", "custom_field_str"],
        )
        root = polars_to_tree(path_data, node_type=CustomNode)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_different_root_error():
        root1 = "a"
        root2 = "b"
        path_data = pl.DataFrame(
            [
                ["a", 90],
                ["a/b", 65],
                ["a/c", 60],
                ["a/b/d", 40],
                ["a/b/e", 35],
                ["a/c/f", 38],
                ["a/b/e/g", 10],
                ["b/b/e/h", 6],  # different root
            ],
            schema=["PATH", "age"],
        )
        with pytest.raises(TreeError) as exc_info:
            polars_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )


class TestPolarsToTreeByRelation(unittest.TestCase):
    def setUp(self):
        self.relation_data = pl.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            schema=["child", "parent", "age"],
        )

    def tearDown(self):
        self.relation_data = None

    def test_polars_to_tree_by_relation(self):
        root = polars_to_tree_by_relation(self.relation_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_by_relation_col_name(self):
        root = polars_to_tree_by_relation(
            self.relation_data,
            child_col="child",
            parent_col="parent",
            attribute_cols=["age"],
        )
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_by_relation_col_name_reverse(self):
        root = polars_to_tree_by_relation(
            self.relation_data[["age", "parent", "child"]],
            child_col="child",
            parent_col="parent",
            attribute_cols=["age"],
        )
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_by_relation_zero_attribute():
        relation_data = pl.DataFrame(
            [
                ["a", None, 0],
                ["b", "a", None],
                ["c", "a", -1],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            schema=["child", "parent", "value"],
        )
        root = polars_to_tree_by_relation(relation_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)
        assert hasattr(root, "value"), "Check root attribute, expected value attribute"
        assert root.value == 0, "Check root value, expected 0"
        assert not hasattr(
            root["b"], "value"
        ), "Check b attribute, expected no value attribute"
        assert root["c"].value == -1, "Check c value, expected -1"

    @staticmethod
    def test_polars_to_tree_by_relation_empty_row_error():
        relation_data = pl.DataFrame(schema=["child", "parent"])
        with pytest.raises(ValueError) as exc_info:
            polars_to_tree_by_relation(relation_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    @staticmethod
    def test_polars_to_tree_by_relation_empty_col_error():
        relation_data = pl.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            polars_to_tree_by_relation(relation_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_polars_to_tree_by_relation_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(pl.exceptions.ColumnNotFoundError):
            polars_to_tree_by_relation(
                self.relation_data, attribute_cols=attribute_cols
            )

    @staticmethod
    def test_polars_to_tree_by_relation_ignore_name_col():
        relation_data = pl.DataFrame(
            [
                ["a", None, 90, "a1"],
                ["b", "a", 65, "b1"],
                ["c", "a", 60, "c1"],
                ["d", "b", 40, "d1"],
                ["e", "b", 35, "e1"],
                ["f", "c", 38, "f1"],
                ["g", "e", 10, "g1"],
                ["h", "e", 6, "h1"],
            ],
            schema=["child", "parent", "age", "name"],
        )
        root = polars_to_tree_by_relation(relation_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_by_relation_ignore_non_attribute_cols():
        relation_data = pl.DataFrame(
            [
                ["a", None, 90, "a1"],
                ["b", "a", 65, "b1"],
                ["c", "a", 60, "c1"],
                ["d", "b", 40, "d1"],
                ["e", "b", 35, "e1"],
                ["f", "c", 38, "f1"],
                ["g", "e", 10, "g1"],
                ["h", "e", 6, "h1"],
            ],
            schema=["child", "parent", "age", "name2"],
        )
        root = polars_to_tree_by_relation(
            relation_data,
            child_col="child",
            parent_col="parent",
            attribute_cols=["age"],
        )
        assert not root.get_attr("name2")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_by_relation_root_node_empty_attribute():
        relation_data = pl.DataFrame(
            [
                ["a", None, None],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            schema=["child", "parent", "age"],
        )
        root = polars_to_tree_by_relation(relation_data)
        assert not root.get_attr("age")
        root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_by_relation_root_node_missing():
        relation_data = pl.DataFrame(
            [
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            schema=["child", "parent", "age"],
        )
        root = polars_to_tree_by_relation(relation_data)
        assert not root.get_attr("age")
        root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_by_relation_duplicate_leaf_node():
        relation_data = pl.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["h", "b", 1],  # duplicate
                ["h", "c", 2],  # duplicate
                ["g", "e", 10],
                ["h", "e", 6],  # duplicate
            ],
            schema=["child", "parent", "age"],
        )
        root = polars_to_tree_by_relation(relation_data)
        expected = (
            "a\n"
            "├── b\n"
            "│   ├── d\n"
            "│   ├── e\n"
            "│   │   ├── g\n"
            "│   │   └── h\n"
            "│   └── h\n"
            "└── c\n"
            "    └── h\n"
        )
        assert_print_statement(print_tree, expected, tree=root, style="const")

    @staticmethod
    def test_polars_to_tree_by_relation_duplicate_intermediate_node_error():
        relation_data = pl.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["e", "c", 1],  # duplicate parent
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            schema=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            polars_to_tree_by_relation(relation_data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DUPLICATED_INTERMEDIATE_NODE
        )

    @staticmethod
    def test_polars_to_tree_by_relation_duplicate_intermediate_node_entry_error():
        relation_data = pl.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["e", "b", 35],  # duplicate entry
                ["e", "c", 1],  # duplicate parent
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            schema=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            polars_to_tree_by_relation(relation_data)
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_DUPLICATED_INTERMEDIATE_NODE
        )

    @staticmethod
    def test_polars_to_tree_by_relation_duplicate_intermediate_node():
        relation_data = pl.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["e", "c", 1],  # duplicate intermediate node
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            schema=["child", "parent", "age"],
        )
        root = polars_to_tree_by_relation(relation_data, allow_duplicates=True)
        actual = len(list(root.descendants))
        assert actual == 10, f"Expected tree to have 10 descendants, received {actual}"

    def test_polars_to_tree_by_relation_node_type(self):
        root = polars_to_tree_by_relation(self.relation_data, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_by_relation_custom_node_type(self):
        relation_data = pl.DataFrame(
            [
                ["a", None, 90, "a"],
                ["b", "a", 65, "b"],
                ["c", "a", 60, "c"],
                ["d", "b", 40, "d"],
                ["e", "b", 35, "e"],
                ["f", "c", 38, "f"],
                ["g", "e", 10, "g"],
                ["h", "e", 6, "h"],
            ],
            schema=["child", "parent", "custom_field", "custom_field_str"],
        )
        root = polars_to_tree_by_relation(relation_data, node_type=CustomNode)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(node, CustomNode) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    @staticmethod
    def test_polars_to_tree_by_relation_multiple_root_parent_none_error():
        relation_data = pl.DataFrame(
            [
                ["a", None, 90],
                ["b", None, 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            schema=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            polars_to_tree_by_relation(relation_data)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_DATAFRAME_MULTIPLE_ROOT.format(root_nodes=["a", "b"])

    @staticmethod
    def test_polars_to_tree_by_relation_multiple_root_error():
        relation_data = pl.DataFrame(
            [
                ["a", None, 90],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            schema=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            polars_to_tree_by_relation(relation_data)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_DATAFRAME_MULTIPLE_ROOT.format(root_nodes=["a", "b"])

    @staticmethod
    def test_polars_to_tree_by_relation_no_root_error():
        relation_data = pl.DataFrame(
            [
                ["a", "b", 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            schema=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            polars_to_tree_by_relation(relation_data)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_DATAFRAME_MULTIPLE_ROOT.format(root_nodes=[])


class TestNewickToTree(unittest.TestCase):
    def setUp(self):
        self.newick_str = "((d,(g,h)e)b,(f)c)a"
        self.newick_str_with_attr = "((d[&&NHX:age=40],(g[&&NHX:age=10],h[&&NHX:age=6])e[&&NHX:age=35])b[&&NHX:age=65],(f[&&NHX:age=38])c[&&NHX:age=60])a[&&NHX:age=90]"

    def tearDown(self):
        self.newick_str = None
        self.newick_str_with_attr = None

    def test_newick_to_tree(self):
        root = newick_to_tree(self.newick_str)
        assert_tree_structure_basenode_root(root)

    def test_newick_to_tree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            newick_to_tree("")
        assert str(exc_info.value) == Constants.ERROR_NODE_STRING_EMPTY

    def test_newick_to_tree_bracket_error(self):
        newick_strs_error = [
            (
                "((d:40[age=4(0],(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                12,
            ),  # NewickCharacter.OPEN_BRACKET, state
            (
                "((d:(40,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                4,
            ),  # NewickCharacter.OPEN_BRACKET, current_node
            (
                "((d(:40,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                3,
            ),  # NewickCharacter.OPEN_BRACKET, cumulative_string
            (
                "((d:40[age=),(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                11,
            ),  # NewickCharacter.CLOSE_BRACKET, state
            (
                "((d]:40,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                3,
            ),  # NewickCharacter.ATTR_END, state
            (
                "((d=:40,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                3,
            ),  # NewickCharacter.ATTR_KEY_VALUE, state
            (
                "((d:40[=,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                7,
            ),  # NewickCharacter.ATTR_KEY_VALUE, cumulative_string
            (
                "(('d:40[age=40],(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                2,
            ),  # NewickCharacter.ATTR_QUOTE, no end quote
            (
                "((d:40[a:ge=40],(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                8,
            ),  # NewickCharacter.SEP, state
            (
                "((d::40[age=40],(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                4,
            ),  # NewickCharacter.SEP, current_node
            (
                "((d:40,(g:10,h:6)e:35)b:65,(f:38)c:60",
                37,
            ),  # final depth
        ]
        for newick_str, error_idx in newick_strs_error:
            with pytest.raises(ValueError) as exc_info:
                newick_to_tree(newick_str)
            assert str(exc_info.value) == Constants.ERROR_NODE_NEWICK_NOT_CLOSED.format(
                index=error_idx
            )

    def test_newick_to_tree_length(self):
        newick_str_length = "((d:40,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90"
        root = newick_to_tree(newick_str_length, length_attr="age")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_attr(self):
        root = newick_to_tree(self.newick_str_with_attr)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(
            root,
            a=("a", "90"),
            b=("b", "65"),
            c=("c", "60"),
            d=("d", "40"),
            e=("e", "35"),
            f=("f", "38"),
            g=("g", "10"),
            h=("h", "6"),
        )
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_attr_no_prefix(self):
        newick_str_no_attr_prefix = "((d[age=40],(g[age=10],h[age=6])e[age=35])b[age=65],(f[age=38])c[age=60])a[age=90]"
        root = newick_to_tree(newick_str_no_attr_prefix, attr_prefix="")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(
            root,
            a=("a", "90"),
            b=("b", "65"),
            c=("c", "60"),
            d=("d", "40"),
            e=("e", "35"),
            f=("f", "38"),
            g=("g", "10"),
            h=("h", "6"),
        )
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_quote_name(self):
        newick_str_no_attr_prefix = "((d[age=40],('(g)'[age=10],h[age=6])e[age=35])b[age=65],(f[age=38])c[age=60])a[age=90]"
        root = newick_to_tree(newick_str_no_attr_prefix, attr_prefix="")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(
            root,
            a=("a", "90"),
            b=("b", "65"),
            c=("c", "60"),
            d=("d", "40"),
            e=("e", "35"),
            f=("f", "38"),
            g=("(g)", "10"),
            h=("h", "6"),
        )
        assert_tree_structure_node_root(root, g="/a/b/e/(g)")

    def test_newick_to_tree_quote_attr_name(self):
        newick_str_no_attr_prefix = "((d[age=40],(g['(age)'=10],h[age=6])e[age=35])b[age=65],(f[age=38])c[age=60])a[age=90]"
        root = newick_to_tree(newick_str_no_attr_prefix, attr_prefix="")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_quote_attr_value(self):
        newick_str_no_attr_prefix = "((d[age=40],(g[age='[10]'],h[age=6])e[age=35])b[age=65],(f[age=38])c[age=60])a[age=90]"
        root = newick_to_tree(newick_str_no_attr_prefix, attr_prefix="")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(
            root,
            a=("a", "90"),
            b=("b", "65"),
            c=("c", "60"),
            d=("d", "40"),
            e=("e", "35"),
            f=("f", "38"),
            g=("g", "[10]"),
            h=("h", "6"),
        )
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_phylogenetic(self):
        newick_str_phylogenetic = "(((ADH2:0.1[&&NHX:S=human:E=1.1.1.1],ADH1:0.11[&&NHX:S=human:E=1.1.1.1]):0.05[&&NHX:S=Primates:E=1.1.1.1:D=Y:B=100],ADHY:0.1[&&NHX:S=nematode:E=1.1.1.1],ADHX:0.12[&&NHX:S=insect:E=1.1.1.1]):0.1[&&NHX:S=Metazoa:E=1.1.1.1:D=N],(ADH4:0.09[&&NHX:S=yeast:E=1.1.1.1],ADH3:0.13[&&NHX:S=yeast:E=1.1.1.1],ADH2:0.12[&&NHX:S=yeast:E=1.1.1.1],ADH1:0.11[&&NHX:S=yeast:E=1.1.1.1]):0.1[&&NHX:S=Fungi])[&&NHX:E=1.1.1.1:D=N]"
        root = newick_to_tree(newick_str_phylogenetic, length_attr="length")
        assert_tree_structure_phylogenetic(root)
        assert_tree_structure_phylogenetic_attr(root)

    def test_newick_to_tree_phylogenetic_no_length_attr(self):
        newick_str_phylogenetic = "(((ADH2:0.1[&&NHX:S=human:E=1.1.1.1],ADH1:0.11[&&NHX:S=human:E=1.1.1.1]):0.05[&&NHX:S=Primates:E=1.1.1.1:D=Y:B=100],ADHY:0.1[&&NHX:S=nematode:E=1.1.1.1],ADHX:0.12[&&NHX:S=insect:E=1.1.1.1]):0.1[&&NHX:S=Metazoa:E=1.1.1.1:D=N],(ADH4:0.09[&&NHX:S=yeast:E=1.1.1.1],ADH3:0.13[&&NHX:S=yeast:E=1.1.1.1],ADH2:0.12[&&NHX:S=yeast:E=1.1.1.1],ADH1:0.11[&&NHX:S=yeast:E=1.1.1.1]):0.1[&&NHX:S=Fungi])[&&NHX:E=1.1.1.1:D=N]"
        root = newick_to_tree(newick_str_phylogenetic)
        assert_tree_structure_phylogenetic(root)
        assert_tree_structure_phylogenetic_attr(root, attrs=["B", "D", "E", "S"])

    def test_newick_to_tree_node_type(self):
        root = newick_to_tree(self.newick_str_with_attr, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(node, NodeA) for node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(
            root,
            a=("a", "90"),
            b=("b", "65"),
            c=("c", "60"),
            d=("d", "40"),
            e=("e", "35"),
            f=("f", "38"),
            g=("g", "10"),
            h=("h", "6"),
        )
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_invalid_character_error(self):
        newick_strs_error = [
            (
                """((d,(g,h)e)b,(f)c)"'a'\"""",
                19,
            ),  # NewickCharacter.ATTR_QUOTE, wrong order of bracket (name)
            (
                """((d,(g,h)e)b,(f[age="'38'"])c)a""",
                21,
            ),  # NewickCharacter.ATTR_QUOTE, wrong order of bracket (attr value)
        ]
        for newick_str, error_idx in newick_strs_error:
            with pytest.raises(ValueError) as exc_info:
                newick_to_tree(newick_str)
            assert str(exc_info.value) == Constants.ERROR_NODE_NEWICK_NOT_CLOSED.format(
                index=error_idx
            )


def assert_tree_structure_phylogenetic(root):
    assert root.max_depth == 4, f"Expected max_depth 4, received {root.max_depth}"
    assert (
        len(list(root.descendants)) == 11
    ), f"Expected 11 descendants, received {len(root.descendants)}"
    assert root.node_name == "node3"
    assert [node.node_name for node in root.children] == ["node1", "node2"]
    assert [node.node_name for node in root["node1"].children] == [
        "node0",
        "ADHY",
        "ADHX",
    ]
    assert [node.node_name for node in root["node1"]["node0"].children] == [
        "ADH2",
        "ADH1",
    ]
    assert [node.node_name for node in root["node2"].children] == [
        "ADH4",
        "ADH3",
        "ADH2",
        "ADH1",
    ]


def assert_tree_structure_phylogenetic_attr(root, attrs=["B", "D", "E", "S", "length"]):
    from bigtree.utils.iterators import preorder_iter

    if "B" in attrs:
        expected = [
            None,
            None,
            "100",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
        actual = [node.get_attr("B") for node in preorder_iter(root)]
        assert expected == actual, f"Expected B to be {expected}, received {actual}"
    if "D" in attrs:
        expected = ["N", "N", "Y", None, None, None, None, None, None, None, None, None]
        actual = [node.get_attr("D") for node in preorder_iter(root)]
        assert expected == actual, f"Expected D to be {expected}, received {actual}"
    if "E" in attrs:
        expected = [
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            None,
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
        ]
        actual = [node.get_attr("E") for node in preorder_iter(root)]
        assert expected == actual, f"Expected E to be {expected}, received {actual}"
    if "S" in attrs:
        expected = [
            None,
            "Metazoa",
            "Primates",
            "human",
            "human",
            "nematode",
            "insect",
            "Fungi",
            "yeast",
            "yeast",
            "yeast",
            "yeast",
        ]
        actual = [node.get_attr("S") for node in preorder_iter(root)]
        assert expected == actual, f"Expected S to be {expected}, received {actual}"
    if "length" in attrs:
        expected = [None, 0.1, 0.05, 0.1, 0.11, 0.1, 0.12, 0.1, 0.09, 0.13, 0.12, 0.11]
        actual = [node.get_attr("length") for node in preorder_iter(root)]
        assert (
            expected == actual
        ), f"Expected length to be {expected}, received {actual}"

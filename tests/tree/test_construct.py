import unittest

import pandas as pd
import pytest

from bigtree.node.node import Node
from bigtree.tree.construct import (
    add_dataframe_to_tree_by_name,
    add_dataframe_to_tree_by_path,
    add_dict_to_tree_by_name,
    add_dict_to_tree_by_path,
    add_path_to_tree,
    dataframe_to_tree,
    dataframe_to_tree_by_relation,
    dict_to_tree,
    list_to_tree,
    list_to_tree_by_relation,
    nested_dict_to_tree,
    str_to_tree,
)
from bigtree.tree.export import print_tree
from bigtree.tree.search import find_name, find_names
from bigtree.utils.exceptions import DuplicatedNodeError, TreeError
from tests.conftest import assert_print_statement
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root_attr,
    assert_tree_structure_basenode_root_generic,
)
from tests.node.test_node import (
    assert_tree_structure_node_root_generic,
    assert_tree_structure_node_root_sep,
)


class NodeA(Node):
    pass


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
        assert_tree_structure_basenode_root_generic(self.root)

    def test_add_path_to_tree_leaves(self):
        for path in self.path_list:
            add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root_generic(self.root)

    def test_add_path_to_tree_empty(self):
        with pytest.raises(ValueError):
            add_path_to_tree(self.root, "")

    def test_add_path_to_tree_sep_leading(self):
        path_list = ["/a/b/d", "/a/b/e", "/a/b/e/g", "/a/b/e/h", "/a/c/f"]
        for path in path_list:
            add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root_generic(self.root)

    def test_add_path_to_tree_sep_trailing(self):
        path_list = ["a/b/d/", "a/b/e/", "a/b/e/g/", "a/b/e/h/", "a/c/f/"]
        for path in path_list:
            add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root_generic(self.root)

    def test_add_path_to_tree_sep_undefined(self):
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]

        with pytest.raises(TreeError):
            for path in path_list:
                add_path_to_tree(self.root, path)

    def test_add_path_to_tree_sep(self):
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]

        for path in path_list:
            add_path_to_tree(self.root, path, sep="\\")
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_add_path_to_tree_sep_tree(self):
        self.root.sep = "\\"

        for path in self.path_list:
            add_path_to_tree(self.root, path)
        assert_tree_structure_node_root_sep(self.root)

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

        with pytest.raises(DuplicatedNodeError):
            for path in path_list:
                add_path_to_tree(self.root, path, duplicate_name_allowed=False)

        for path in path_list:
            add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root_generic(self.root)

    def test_add_path_to_tree_node_type(self):
        root = NodeA("a")
        for path in self.path_list:
            add_path_to_tree(root, path)
        assert isinstance(root, NodeA), "Node type is not `NodeA`"
        assert_tree_structure_basenode_root_generic(root)

    def test_add_path_to_tree_different_root(self):
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
        with pytest.raises(TreeError):
            for path in path_list:
                add_path_to_tree(self.root, path, sep="-")


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
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_add_dict_to_tree_by_path_empty(self):
        paths = {}
        with pytest.raises(ValueError):
            add_dict_to_tree_by_path(self.root, paths)

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
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

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
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_add_dict_to_tree_by_path_sep_undefined(self):
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
        with pytest.raises(TreeError):
            add_dict_to_tree_by_path(self.root, paths)

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
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

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
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_sep(self.root)

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
        with pytest.raises(DuplicatedNodeError):
            add_dict_to_tree_by_path(self.root, paths, duplicate_name_allowed=False)

        add_dict_to_tree_by_path(self.root, paths)
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root, f=("d", 38))

    def test_add_dict_to_tree_by_path_node_type(self):
        root = NodeA("a", age=1)
        add_dict_to_tree_by_path(root, self.paths)
        assert isinstance(root, NodeA), "Node type is not `NodeA`"
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)

    def test_add_dict_to_tree_by_path_different_root(self):
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
        with pytest.raises(TreeError):
            add_dict_to_tree_by_path(self.root, paths)


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
        root = add_dict_to_tree_by_name(self.root, self.name_dict)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

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
        root = add_dict_to_tree_by_name(self.root, name_dict)
        nodes = ["a", "b", "c", "d", "e", "f", "g", "h"]
        expected_list = [[1], [1, 2], [1, None], [None], None, 0, -1, [-1]]
        for node_name, expected in zip(nodes, expected_list):
            actual = find_name(root, node_name).get_attr("random")
            assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    def test_add_dict_to_tree_by_name_empty(self):
        with pytest.raises(ValueError):
            add_dict_to_tree_by_name(self.root, {})

    def test_add_dict_to_tree_by_name_duplicate_in_tree(self):
        hh = Node("h")
        hh.parent = self.root
        root = add_dict_to_tree_by_name(self.root, self.name_dict)
        assert (
            len(list(find_names(root, "h"))) == 2
        ), "There is less node 'h' than expected"
        for _node in list(find_names(root, "h")):
            assert _node.age == 6

    def test_add_dict_to_tree_by_name_inner_join_tree(self):
        dummy = Node("dummy")
        dummy.parent = self.b
        root = add_dict_to_tree_by_name(self.root, self.name_dict, join_type="inner")
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_add_dict_to_tree_by_name_inner_join_dict(self):
        self.name_dict["dummy"] = {"age": 100}
        root = add_dict_to_tree_by_name(self.root, self.name_dict, join_type="inner")
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_add_dict_to_tree_by_name_left_join(self):
        root = add_dict_to_tree_by_name(self.root, self.name_dict, join_type="left")
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_add_dict_to_tree_by_name_invalid_join(self):
        with pytest.raises(ValueError):
            add_dict_to_tree_by_name(self.root, self.name_dict, join_type="something")

    def test_add_dict_to_tree_by_name_sep_tree(self):
        self.root.sep = "\\"
        root = add_dict_to_tree_by_name(self.root, self.name_dict)
        assert_tree_structure_node_root_sep(root)

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
        root = add_dict_to_tree_by_name(root, self.name_dict)
        assert isinstance(root, NodeA), "Node type is not `NodeA`"
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)


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
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_add_dataframe_to_tree_by_path_col_name(self):
        add_dataframe_to_tree_by_path(
            self.root, self.data, path_col="PATH", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_add_dataframe_to_tree_by_path_empty_row(self):
        data = pd.DataFrame(columns=["PATH", "age"])
        with pytest.raises(ValueError):
            add_dataframe_to_tree_by_path(self.root, data)

    def test_add_dataframe_to_tree_by_path_empty_col(self):
        data = pd.DataFrame()
        with pytest.raises(ValueError):
            add_dataframe_to_tree_by_path(self.root, data)

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
        assert_tree_structure_basenode_root_generic(self.root)

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
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

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
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_add_dataframe_to_tree_by_path_sep_undefined(self):
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
        with pytest.raises(TreeError):
            add_dataframe_to_tree_by_path(self.root, data)

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
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root_generic(self.root)

    def test_add_dataframe_to_tree_by_path_sep_tree(self):
        self.root.sep = "\\"
        add_dataframe_to_tree_by_path(self.root, self.data)
        assert_tree_structure_node_root_sep(self.root)

    def test_add_dataframe_to_tree_by_path_node_type(self):
        root = NodeA("a", age=1)
        add_dataframe_to_tree_by_path(root, self.data)
        assert isinstance(root, NodeA), "Node type is not `NodeA`"
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_add_dataframe_to_tree_by_path_different_root(self):
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
        with pytest.raises(TreeError):
            add_dataframe_to_tree_by_path(self.root, data)

    def test_add_dataframe_to_tree_by_path_duplicate(self):
        data = pd.DataFrame(
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
        with pytest.raises(ValueError):
            add_dataframe_to_tree_by_path(self.root, data)

    def test_add_dataframe_to_tree_by_path_duplicate_node(self):
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
        with pytest.raises(DuplicatedNodeError):
            add_dataframe_to_tree_by_path(self.root, data, duplicate_name_allowed=False)

        add_dataframe_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root_generic(self.root)
        assert_tree_structure_basenode_root_attr(self.root, f=("d", 38))
        assert_tree_structure_node_root_generic(self.root, f="/a/c/d")


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
        root = add_dataframe_to_tree_by_name(self.root, self.data)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_add_dataframe_to_tree_by_name_duplicate_in_tree(self):
        hh = Node("h")
        hh.parent = self.root
        root = add_dataframe_to_tree_by_name(self.root, self.data)
        assert (
            len(list(find_names(root, "h"))) == 2
        ), "There is less node 'h' than expected"
        for _node in list(find_names(root, "h")):
            assert _node.age == 6

    def test_add_dataframe_to_tree_by_name_col_name(self):
        root = add_dataframe_to_tree_by_name(
            self.root, self.data, name_col="NAME", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_add_dataframe_to_tree_by_name_empty(self):
        with pytest.raises(ValueError):
            add_dataframe_to_tree_by_name(self.root, pd.DataFrame())

    def test_add_dataframe_to_tree_by_name_empty_row(self):
        data = pd.DataFrame(columns=["NAME", "age"])
        with pytest.raises(ValueError):
            add_dataframe_to_tree_by_name(self.root, data, join_type="inner")

    def test_add_dataframe_to_tree_by_name_inner_join_tree(self):
        dummy = Node("dummy")
        dummy.parent = self.b
        root = add_dataframe_to_tree_by_name(self.root, self.data, join_type="inner")
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_add_dataframe_to_tree_by_name_inner_join_data(self):
        data = pd.DataFrame(
            [
                ["a", 90],
                ["b", 65],
                ["c", 60],
                ["d", 40],
                ["e", 35],
                ["f", 38],
                ["g", 10],
                ["h", 6],
                ["dummy", 100],
            ],
            columns=["NAME", "age"],
        )
        root = add_dataframe_to_tree_by_name(self.root, data, join_type="inner")
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_add_dataframe_to_tree_by_name_left_join(self):
        root = add_dataframe_to_tree_by_name(self.root, self.data, join_type="left")
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_add_dataframe_to_tree_by_name_invalid_join(self):
        with pytest.raises(ValueError):
            add_dataframe_to_tree_by_name(self.root, self.data, join_type="something")

    def test_add_dataframe_to_tree_by_name_sep_tree(self):
        self.root.sep = "\\"
        root = add_dataframe_to_tree_by_name(self.root, self.data)
        assert_tree_structure_node_root_sep(root)

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
        root = add_dataframe_to_tree_by_name(root, self.data)
        assert isinstance(root, NodeA), "Node type is not `NodeA`"
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_add_dataframe_to_tree_by_name_duplicate(self):
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
        with pytest.raises(ValueError):
            add_dataframe_to_tree_by_name(self.root, data)

    def test_add_dataframe_to_tree_by_name_duplicate_node(self):
        root = Node("a", age=1)
        b = Node("b", parent=root, age=1)
        c = Node("c", parent=root, age=1)
        d = Node("d", age=1)
        e = Node("e")
        f = Node("f")
        g = Node("g")
        h = Node("f")  # duplicate node
        d.parent = b
        e.parent = b
        f.parent = c
        g.parent = e
        h.parent = e
        root = add_dataframe_to_tree_by_name(root, self.data)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root, h=("f", 38))


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
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

    def test_str_to_tree_with_prefix(self):
        root = str_to_tree(self.tree_str, tree_prefix_list=["─"])
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

    def test_str_to_tree_with_multiple_prefix(self):
        root = str_to_tree(self.tree_str, tree_prefix_list=["├──", "└──"])
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

    def test_ascii_character_error(self):
        tree_str = "a\n|-- b\n|   |-- d\n|   +-- e\n|       |-- g\n|       +-- h\n+-- c\n    +-- f"
        with pytest.raises(ValueError) as exc_info:
            str_to_tree(tree_str)
        assert str(exc_info.value).startswith(
            "Invalid prefix, prefix should be unicode character or whitespace, otherwise specify one or more prefixes"
        )

    def test_ascii_character_with_prefix(self):
        tree_str = "a\n|-- b\n|   |-- d\n|   +-- e\n|       |-- g\n|       +-- h\n+-- c\n    +-- f"
        root = str_to_tree(tree_str, tree_prefix_list=["-"])
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

    def test_empty_string(self):
        with pytest.raises(ValueError) as exc_info:
            str_to_tree("")
        assert (
            str(exc_info.value)
            == "Tree string does not contain any data, check `tree_string`"
        )

    def test_empty_newline_string(self):
        with pytest.raises(ValueError) as exc_info:
            str_to_tree("\n\n")
        assert (
            str(exc_info.value)
            == "Tree string does not contain any data, check `tree_string`"
        )

    def test_unequal_prefix_length(self):
        tree_str = "a\n├── b\n│  ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f"
        with pytest.raises(ValueError) as exc_info:
            str_to_tree(tree_str)
        assert str(exc_info.value).startswith(
            "Tree string have different prefix length, check branch"
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
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

    def test_list_to_tree_leaves(self):
        root = list_to_tree(self.path_list)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

    def test_list_to_tree_empty(self):
        with pytest.raises(ValueError):
            list_to_tree("")

    def test_list_to_tree_sep_leading(self):
        path_list = ["/a/b/d", "/a/b/e", "/a/b/e/g", "/a/b/e/h", "/a/c/f"]
        root = list_to_tree(path_list)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

    def test_list_to_tree_sep_trailing(self):
        path_list = ["a/b/d/", "a/b/e/", "a/b/e/g/", "a/b/e/h/", "a/c/f/"]
        root = list_to_tree(path_list)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

    def test_list_to_tree_sep_undefined(self):
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        with pytest.raises(TreeError):
            list_to_tree(path_list)

    def test_list_to_tree_sep(self):
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]
        root = list_to_tree(path_list, sep="\\")
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_sep(root)

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
        with pytest.raises(DuplicatedNodeError):
            list_to_tree(path_list, duplicate_name_allowed=False)

        root = list_to_tree(path_list)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root, f="/a/c/d")

    def test_list_to_tree_node_type(self):
        root = list_to_tree(self.path_list, node_type=NodeA)
        assert isinstance(root, NodeA), "Node type is not `NodeA`"
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

    def test_list_to_tree_different_root(self):
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
        with pytest.raises(TreeError):
            list_to_tree(path_list)


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
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

    def test_list_to_tree_by_relation_reverse(self):
        root = list_to_tree_by_relation(self.relations_reverse)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

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

    def test_list_to_tree_by_relation_empty_parent(self):
        self.relations.append((None, "a"))
        root = list_to_tree_by_relation(self.relations)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_node_root_generic(root)

    @staticmethod
    def test_list_to_tree_by_relation_one_tuple():
        root = list_to_tree_by_relation([(None, "a")])
        assert root.max_depth == 1, "Max depth is wrong"
        assert root.node_name == "a", "Node name is wrong"

    def test_list_to_tree_by_relation_empty(self):
        with pytest.raises(ValueError):
            list_to_tree_by_relation([])

    def test_list_to_tree_by_relation_switch_order(self):
        root = list_to_tree_by_relation(self.relations_switch)
        expected = """h\n├── g\n│   ├── e\n│   ├── d\n│   │   ├── b\n│   │   └── a\n│   └── a\n└── f\n    └── a\n"""
        assert_print_statement(print_tree, expected, root)

    def test_list_to_tree_by_relation_switch_order_reverse(self):
        root = list_to_tree_by_relation(self.relations_switch[::-1])
        expected = """h\n├── f\n│   └── a\n└── g\n    ├── a\n    ├── d\n    │   ├── a\n    │   └── b\n    └── e\n"""
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
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_dict_to_tree_empty(self):
        paths = {}
        with pytest.raises(ValueError):
            dict_to_tree(paths)

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
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

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
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    @staticmethod
    def test_dict_to_tree_sep_undefined():
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
        with pytest.raises(TreeError):
            dict_to_tree(paths)

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
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_sep(root)

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
        with pytest.raises(DuplicatedNodeError):
            dict_to_tree(path_dict, duplicate_name_allowed=False)

        root = dict_to_tree(path_dict)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root, f=("d", 38))
        assert_tree_structure_node_root_generic(root, f="/a/c/d")

    def test_dict_to_tree_node_type(self):
        root = dict_to_tree(self.path_dict, node_type=NodeA)
        assert isinstance(root, NodeA), "Node type is not `NodeA`"
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    @staticmethod
    def test_dict_to_tree_different_root():
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
        with pytest.raises(TreeError):
            dict_to_tree(path_dict)


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
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

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
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_nested_dict_to_tree_node_type(self):
        root = nested_dict_to_tree(self.path_dict, node_type=NodeA)
        assert isinstance(root, NodeA), "Node type is not `NodeA`"
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)


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
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_dataframe_to_tree_col_name(self):
        root = dataframe_to_tree(
            self.path_data, path_col="PATH", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

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
        assert_tree_structure_basenode_root_generic(root)

    @staticmethod
    def test_dataframe_to_tree_empty_row():
        data = pd.DataFrame(columns=["PATH", "age"])
        with pytest.raises(ValueError):
            dataframe_to_tree(data)

    @staticmethod
    def test_dataframe_to_tree_empty_col():
        data = pd.DataFrame()
        with pytest.raises(ValueError):
            dataframe_to_tree(data)

    @staticmethod
    def test_dataframe_to_tree_sep_leading():
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
        root = dataframe_to_tree(data)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_dataframe_to_tree_sep_trailing(self):
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
        root = dataframe_to_tree(data)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_dataframe_to_tree_sep_undefined(self):
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
        with pytest.raises(TreeError):
            dataframe_to_tree(data)

    def test_dataframe_to_tree_sep(self):
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
        root = dataframe_to_tree(data, sep="\\")
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_sep(root)

    def test_dataframe_to_tree_node_type(self):
        root = dataframe_to_tree(self.path_data, node_type=NodeA)
        assert isinstance(root, NodeA), "Node type is not `NodeA`"
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    @staticmethod
    def test_dataframe_to_tree_different_root():
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
        with pytest.raises(TreeError):
            dataframe_to_tree(path_data)

    @staticmethod
    def test_dataframe_to_tree_duplicate():
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
            "There exists duplicate path with different attributes"
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
        with pytest.raises(DuplicatedNodeError):
            dataframe_to_tree(path_data, duplicate_name_allowed=False)

        root = dataframe_to_tree(path_data)
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root, f=("d", 38))
        assert_tree_structure_node_root_generic(root, f="/a/c/d")


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
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    def test_dataframe_to_tree_by_relation_col_name(self):
        root = dataframe_to_tree_by_relation(
            self.relation_data,
            child_col="child",
            parent_col="parent",
            attribute_cols=["age"],
        )
        assert_tree_structure_basenode_root_generic(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root_generic(root)

    @staticmethod
    def test_dataframe_to_tree_by_relation_duplicate_leaf_node():
        relation_data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["h", "b", 1],
                ["h", "c", 2],
                ["g", "e", 10],
                ["h", "e", 1],
            ],
            columns=["child", "parent", "age"],
        )
        root = dataframe_to_tree_by_relation(relation_data)
        expected = """a\n├── b\n│   ├── d\n│   ├── e\n│   │   ├── g\n│   │   └── h\n│   └── h\n└── c\n    └── h\n"""
        assert_print_statement(print_tree, expected, tree=root, style="const")

    @staticmethod
    def test_dataframe_to_tree_by_relation_empty_row():
        data = pd.DataFrame(columns=["child", "parent"])
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(data)
        assert str(exc_info.value) == "Data does not contain any rows, check `data`"

    @staticmethod
    def test_dataframe_to_tree_by_relation_empty_col():
        data = pd.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(data)
        assert str(exc_info.value) == "Data does not contain any columns, check `data`"

    @staticmethod
    def test_dataframe_to_tree_by_relation_duplicated_intermediate_node_error():
        data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["e", "c", 1],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(data)
        assert str(exc_info.value).startswith(
            "There exists duplicate child with different parent where the child is also a parent node"
        )

    @staticmethod
    def test_dataframe_to_tree_by_relation_duplicated_intermediate_node():
        data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["e", "c", 1],
                ["f", "c", 38],
                ["g", "e", 10],
                ["h", "e", 6],
            ],
            columns=["child", "parent", "age"],
        )
        root = dataframe_to_tree_by_relation(data, allow_duplicates=True)
        actual = len(list(root.descendants))
        assert actual == 10, f"Expected tree to have 10 descendants, received {actual}"

    @staticmethod
    def test_dataframe_to_tree_by_relation_multiple_root():
        data = pd.DataFrame(
            [
                ["a", None, 90],
                ["b", None, 65],
                ["c", "a", 60],
                ["e", "b", 40],
                ["e", "b", 35],
                ["h", "b", 1],
                ["h", "c", 2],
                ["g", "e", 10],
                ["h", "e", 1],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(data)
        assert str(exc_info.value).startswith("Unable to determine root node")

    @staticmethod
    def test_dataframe_to_tree_by_relation_no_root():
        data = pd.DataFrame(
            [
                ["a", "b", 90],
                ["b", "a", 65],
                ["c", "a", 60],
                ["d", "b", 40],
                ["e", "b", 35],
                ["h", "b", 1],
                ["h", "c", 2],
                ["g", "e", 10],
                ["h", "e", 1],
            ],
            columns=["child", "parent", "age"],
        )
        with pytest.raises(ValueError) as exc_info:
            dataframe_to_tree_by_relation(data)
        assert str(exc_info.value).startswith("Unable to determine root node")

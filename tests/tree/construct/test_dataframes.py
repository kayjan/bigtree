import unittest

import pandas as pd
import polars as pl
import pytest

from bigtree.node import node
from bigtree.tree import construct, export, search
from bigtree.utils import exceptions
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
from tests.tree.construct.conftest import CustomNode, NodeA


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
        self.root = node.Node("a", age=1)
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
        construct.add_dataframe_to_tree_by_path(self.root, self.data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_col_name(self):
        construct.add_dataframe_to_tree_by_path(
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
        construct.add_dataframe_to_tree_by_path(self.root, data)
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
        construct.add_dataframe_to_tree_by_path(
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
            construct.add_dataframe_to_tree_by_path(self.root, pd.DataFrame())
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_dataframe_to_tree_by_path_empty_row_error(self):
        data = pd.DataFrame(columns=["PATH", "age"])
        with pytest.raises(ValueError) as exc_info:
            construct.add_dataframe_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    def test_add_dataframe_to_tree_by_path_empty_col_error(self):
        data = pd.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            construct.add_dataframe_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_dataframe_to_tree_by_path_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(KeyError):
            construct.add_dataframe_to_tree_by_path(
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
        construct.add_dataframe_to_tree_by_path(self.root, data)
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
        construct.add_dataframe_to_tree_by_path(
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
        construct.add_dataframe_to_tree_by_path(self.root, data)
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
        construct.add_dataframe_to_tree_by_path(self.root, data)
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
        construct.add_dataframe_to_tree_by_path(self.root, data)
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
        construct.add_dataframe_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_sep_error(self):
        root1 = self.root.node_name
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.add_dataframe_to_tree_by_path(self.root, data)
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
        construct.add_dataframe_to_tree_by_path(self.root, data, sep="\\")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_path_sep_tree(self):
        self.root.sep = "\\"
        construct.add_dataframe_to_tree_by_path(self.root, self.data)
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
        with pytest.raises(exceptions.DuplicatedNodeError) as exc_info:
            construct.add_dataframe_to_tree_by_path(
                self.root, data, duplicate_name_allowed=False
            )
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
        construct.add_dataframe_to_tree_by_path(self.root, data)
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
            construct.add_dataframe_to_tree_by_path(self.root, data)
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
            construct.add_dataframe_to_tree_by_path(self.root, data)
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
        construct.add_dataframe_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root, f=("d", 38))
        assert_tree_structure_node_root(self.root, f="/a/c/d")

    def test_add_dataframe_to_tree_by_path_node_type(self):
        root = NodeA("a", age=1)
        construct.add_dataframe_to_tree_by_path(root, self.data)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        construct.add_dataframe_to_tree_by_path(root, data)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(_node, CustomNode) for _node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_dataframe_to_tree_by_path_different_root_error(self):
        root1 = self.root.node_name
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.add_dataframe_to_tree_by_path(self.root, data)
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
        self.root = node.Node("a", age=1)
        self.b = node.Node("b", parent=self.root, age=1)
        self.c = node.Node("c", parent=self.root, age=1)
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
        construct.add_dataframe_to_tree_by_name(self.root, self.data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_name_col_name(self):
        construct.add_dataframe_to_tree_by_name(
            self.root, self.data, name_col="NAME", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_name_col_name_reverse(self):
        construct.add_dataframe_to_tree_by_name(
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
        construct.add_dataframe_to_tree_by_name(self.root, data)
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
            construct.add_dataframe_to_tree_by_name(self.root, pd.DataFrame())
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_dataframe_to_tree_by_name_empty_row_error(self):
        data = pd.DataFrame(columns=["NAME", "age"])
        with pytest.raises(ValueError) as exc_info:
            construct.add_dataframe_to_tree_by_name(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    def test_add_dataframe_to_tree_by_name_empty_col_error(self):
        data = pd.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            construct.add_dataframe_to_tree_by_name(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_dataframe_to_tree_by_name_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(KeyError):
            construct.add_dataframe_to_tree_by_name(
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
        construct.add_dataframe_to_tree_by_name(self.root, data, name_col="name2")
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
        construct.add_dataframe_to_tree_by_name(
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
        construct.add_dataframe_to_tree_by_name(self.root, data)
        assert self.root.get_attr("age") == 1
        self.root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dataframe_to_tree_by_name_sep_tree(self):
        self.root.sep = "\\"
        root = construct.add_dataframe_to_tree_by_name(self.root, self.data)
        assert_tree_structure_node_root_sep(root)

    def test_add_dataframe_to_tree_by_name_duplicate_name(self):
        hh = node.Node("h")
        hh.parent = self.root
        root = construct.add_dataframe_to_tree_by_name(self.root, self.data)
        assert (
            len(list(search.find_names(root, "h"))) == 2
        ), "There is less node 'h' than expected"
        for _node in list(search.find_names(root, "h")):
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
            construct.add_dataframe_to_tree_by_name(self.root, data)
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
            construct.add_dataframe_to_tree_by_name(self.root, data)
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
        construct.add_dataframe_to_tree_by_name(root, self.data)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        construct.add_dataframe_to_tree_by_name(root, data)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(_node, CustomNode) for _node in root.children
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
        construct.add_dataframe_to_tree_by_name(self.root, data)
        expected_root_str = "a [age=90.0]\n" "├── b [age=1]\n" "└── c [age=60.0]\n"
        assert_print_statement(
            export.print_tree, expected_root_str, self.root, all_attrs=True, max_depth=2
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
        self.root = node.Node("a", age=1)
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
        construct.add_polars_to_tree_by_path(self.root, self.data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_col_name(self):
        construct.add_polars_to_tree_by_path(
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
        construct.add_polars_to_tree_by_path(self.root, data)
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
        construct.add_polars_to_tree_by_path(
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
            construct.add_polars_to_tree_by_path(self.root, pl.DataFrame())
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_polars_to_tree_by_path_empty_row_error(self):
        data = pl.DataFrame(schema=["PATH", "age"])
        with pytest.raises(ValueError) as exc_info:
            construct.add_polars_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    def test_add_polars_to_tree_by_path_empty_col_error(self):
        data = pl.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            construct.add_polars_to_tree_by_path(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_polars_to_tree_by_path_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(pl.exceptions.ColumnNotFoundError):
            construct.add_polars_to_tree_by_path(
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
        construct.add_polars_to_tree_by_path(self.root, data)
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
        construct.add_polars_to_tree_by_path(
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
        construct.add_polars_to_tree_by_path(self.root, data)
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
        construct.add_polars_to_tree_by_path(self.root, data)
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
        construct.add_polars_to_tree_by_path(self.root, data)
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
        construct.add_polars_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_sep_error(self):
        root1 = self.root.node_name
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.add_polars_to_tree_by_path(self.root, data)
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
        construct.add_polars_to_tree_by_path(self.root, data, sep="\\")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_path_sep_tree(self):
        self.root.sep = "\\"
        construct.add_polars_to_tree_by_path(self.root, self.data)
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
        with pytest.raises(exceptions.DuplicatedNodeError) as exc_info:
            construct.add_polars_to_tree_by_path(
                self.root, data, duplicate_name_allowed=False
            )
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
        construct.add_polars_to_tree_by_path(self.root, data)
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
            construct.add_polars_to_tree_by_path(self.root, data)
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
            construct.add_polars_to_tree_by_path(self.root, data)
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
        construct.add_polars_to_tree_by_path(self.root, data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root, f=("d", 38))
        assert_tree_structure_node_root(self.root, f="/a/c/d")

    def test_add_polars_to_tree_by_path_node_type(self):
        root = NodeA("a", age=1)
        construct.add_polars_to_tree_by_path(root, self.data)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        construct.add_polars_to_tree_by_path(root, data)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(_node, CustomNode) for _node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_polars_to_tree_by_path_different_root_error(self):
        root1 = self.root.node_name
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.add_polars_to_tree_by_path(self.root, data)
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
        self.root = node.Node("a", age=1)
        self.b = node.Node("b", parent=self.root, age=1)
        self.c = node.Node("c", parent=self.root, age=1)
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
        construct.add_polars_to_tree_by_name(self.root, self.data)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_name_col_name(self):
        construct.add_polars_to_tree_by_name(
            self.root, self.data, name_col="NAME", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_name_col_name_reverse(self):
        construct.add_polars_to_tree_by_name(
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
        construct.add_polars_to_tree_by_name(self.root, data)
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
            construct.add_polars_to_tree_by_name(self.root, pl.DataFrame())
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_polars_to_tree_by_name_empty_row_error(self):
        data = pl.DataFrame(schema=["NAME", "age"])
        with pytest.raises(ValueError) as exc_info:
            construct.add_polars_to_tree_by_name(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    def test_add_polars_to_tree_by_name_empty_col_error(self):
        data = pl.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            construct.add_polars_to_tree_by_name(self.root, data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_add_polars_to_tree_by_name_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(pl.exceptions.ColumnNotFoundError):
            construct.add_polars_to_tree_by_name(
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
        construct.add_polars_to_tree_by_name(self.root, data, name_col="name2")
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
        construct.add_polars_to_tree_by_name(
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
        construct.add_polars_to_tree_by_name(self.root, data)
        assert self.root.get_attr("age") == 1
        self.root.set_attrs({"age": 90})
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_polars_to_tree_by_name_sep_tree(self):
        self.root.sep = "\\"
        root = construct.add_polars_to_tree_by_name(self.root, self.data)
        assert_tree_structure_node_root_sep(root)

    def test_add_polars_to_tree_by_name_duplicate_name(self):
        hh = node.Node("h")
        hh.parent = self.root
        root = construct.add_polars_to_tree_by_name(self.root, self.data)
        assert (
            len(list(search.find_names(root, "h"))) == 2
        ), "There is less node 'h' than expected"
        for _node in list(search.find_names(root, "h")):
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
            construct.add_polars_to_tree_by_name(self.root, data)
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
            construct.add_polars_to_tree_by_name(self.root, data)
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
        construct.add_polars_to_tree_by_name(root, self.data)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        construct.add_polars_to_tree_by_name(root, data)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(_node, CustomNode) for _node in root.children
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
        construct.add_polars_to_tree_by_name(self.root, data)
        expected_root_str = "a [age=90]\n" "├── b [age=1]\n" "└── c [age=60]\n"
        assert_print_statement(
            export.print_tree, expected_root_str, self.root, all_attrs=True, max_depth=2
        )


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
        root = construct.dataframe_to_tree(self.path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_col_name(self):
        root = construct.dataframe_to_tree(
            self.path_data, path_col="PATH", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_col_name_reverse(self):
        root = construct.dataframe_to_tree(
            self.path_data[["age", "PATH"]], path_col="PATH"
        )
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
        root = construct.dataframe_to_tree(path_data)
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
        root = construct.dataframe_to_tree(path_data)
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
            construct.dataframe_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    @staticmethod
    def test_dataframe_to_tree_empty_col_error():
        path_data = pd.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            construct.dataframe_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_dataframe_to_tree_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(KeyError):
            construct.dataframe_to_tree(self.path_data, attribute_cols=attribute_cols)

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
        root = construct.dataframe_to_tree(path_data)
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
        root = construct.dataframe_to_tree(
            path_data, path_col="PATH", attribute_cols=["age"]
        )
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
        root = construct.dataframe_to_tree(path_data)
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
        root = construct.dataframe_to_tree(path_data)
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
        root = construct.dataframe_to_tree(path_data)
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.dataframe_to_tree(path_data)
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
        root = construct.dataframe_to_tree(path_data, sep="\\")
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
            construct.dataframe_to_tree(path_data)
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
            construct.dataframe_to_tree(path_data)
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
        root = construct.dataframe_to_tree(path_data)
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
        with pytest.raises(exceptions.DuplicatedNodeError) as exc_info:
            construct.dataframe_to_tree(path_data, duplicate_name_allowed=False)
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
        root = construct.dataframe_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root, f=("d", 38))
        assert_tree_structure_node_root(root, f="/a/c/d")

    def test_dataframe_to_tree_node_type(self):
        root = construct.dataframe_to_tree(self.path_data, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        root = construct.dataframe_to_tree(path_data, node_type=CustomNode)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(_node, CustomNode) for _node in root.children
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.dataframe_to_tree(path_data)
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
        root = construct.dataframe_to_tree_by_relation(self.relation_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_by_relation_col_name(self):
        root = construct.dataframe_to_tree_by_relation(
            self.relation_data,
            child_col="child",
            parent_col="parent",
            attribute_cols=["age"],
        )
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dataframe_to_tree_by_relation_col_name_reverse(self):
        root = construct.dataframe_to_tree_by_relation(
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
        root = construct.dataframe_to_tree_by_relation(relation_data)
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
            construct.dataframe_to_tree_by_relation(relation_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    @staticmethod
    def test_dataframe_to_tree_by_relation_empty_col_error():
        relation_data = pd.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            construct.dataframe_to_tree_by_relation(relation_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_dataframe_to_tree_by_relation_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(KeyError):
            construct.dataframe_to_tree_by_relation(
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
        root = construct.dataframe_to_tree_by_relation(relation_data)
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
        root = construct.dataframe_to_tree_by_relation(
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
        root = construct.dataframe_to_tree_by_relation(relation_data)
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
        root = construct.dataframe_to_tree_by_relation(relation_data)
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
        assert_print_statement(export.print_tree, expected, tree=root, style="const")

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
            construct.dataframe_to_tree_by_relation(relation_data)
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
            construct.dataframe_to_tree_by_relation(relation_data)
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
        root = construct.dataframe_to_tree_by_relation(
            relation_data, allow_duplicates=True
        )
        actual = len(list(root.descendants))
        assert actual == 10, f"Expected tree to have 10 descendants, received {actual}"

    def test_dataframe_to_tree_by_relation_node_type(self):
        root = construct.dataframe_to_tree_by_relation(
            self.relation_data, node_type=NodeA
        )
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        root = construct.dataframe_to_tree_by_relation(
            relation_data, node_type=CustomNode
        )
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(_node, CustomNode) for _node in root.children
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
            construct.dataframe_to_tree_by_relation(relation_data)
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
            construct.dataframe_to_tree_by_relation(relation_data)
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
            construct.dataframe_to_tree_by_relation(relation_data)
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
            construct.dataframe_to_tree_by_relation(relation_data)
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
        root = construct.polars_to_tree(self.path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_col_name(self):
        root = construct.polars_to_tree(
            self.path_data, path_col="PATH", attribute_cols=["age"]
        )
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_col_name_reverse(self):
        root = construct.polars_to_tree(
            self.path_data[["age", "PATH"]], path_col="PATH"
        )
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
        root = construct.polars_to_tree(path_data)
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
        root = construct.polars_to_tree(path_data)
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
            construct.polars_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    @staticmethod
    def test_polars_to_tree_empty_col_error():
        path_data = pl.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            construct.polars_to_tree(path_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_polars_to_tree_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(pl.exceptions.ColumnNotFoundError):
            construct.polars_to_tree(self.path_data, attribute_cols=attribute_cols)

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
        root = construct.polars_to_tree(path_data)
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
        root = construct.polars_to_tree(
            path_data, path_col="PATH", attribute_cols=["age"]
        )
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
        root = construct.polars_to_tree(path_data)
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
        root = construct.polars_to_tree(path_data)
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
        root = construct.polars_to_tree(path_data)
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
        root = construct.polars_to_tree(path_data)
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.polars_to_tree(path_data)
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
        root = construct.polars_to_tree(path_data, sep="\\")
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
            construct.polars_to_tree(path_data)
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
            construct.polars_to_tree(path_data)
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
        root = construct.polars_to_tree(path_data)
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
        with pytest.raises(exceptions.DuplicatedNodeError) as exc_info:
            construct.polars_to_tree(path_data, duplicate_name_allowed=False)
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
        root = construct.polars_to_tree(path_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root, f=("d", 38))
        assert_tree_structure_node_root(root, f="/a/c/d")

    def test_polars_to_tree_node_type(self):
        root = construct.polars_to_tree(self.path_data, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        root = construct.polars_to_tree(path_data, node_type=CustomNode)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(_node, CustomNode) for _node in root.children
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.polars_to_tree(path_data)
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
        root = construct.polars_to_tree_by_relation(self.relation_data)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_by_relation_col_name(self):
        root = construct.polars_to_tree_by_relation(
            self.relation_data,
            child_col="child",
            parent_col="parent",
            attribute_cols=["age"],
        )
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_polars_to_tree_by_relation_col_name_reverse(self):
        root = construct.polars_to_tree_by_relation(
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
        root = construct.polars_to_tree_by_relation(relation_data)
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
            construct.polars_to_tree_by_relation(relation_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_ROW

    @staticmethod
    def test_polars_to_tree_by_relation_empty_col_error():
        relation_data = pl.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            construct.polars_to_tree_by_relation(relation_data)
        assert str(exc_info.value) == Constants.ERROR_NODE_DATAFRAME_EMPTY_COL

    def test_polars_to_tree_by_relation_attribute_cols_error(self):
        attribute_cols = ["age2"]
        with pytest.raises(pl.exceptions.ColumnNotFoundError):
            construct.polars_to_tree_by_relation(
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
        root = construct.polars_to_tree_by_relation(relation_data)
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
        root = construct.polars_to_tree_by_relation(
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
        root = construct.polars_to_tree_by_relation(relation_data)
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
        root = construct.polars_to_tree_by_relation(relation_data)
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
        root = construct.polars_to_tree_by_relation(relation_data)
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
        assert_print_statement(export.print_tree, expected, tree=root, style="const")

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
            construct.polars_to_tree_by_relation(relation_data)
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
            construct.polars_to_tree_by_relation(relation_data)
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
        root = construct.polars_to_tree_by_relation(
            relation_data, allow_duplicates=True
        )
        actual = len(list(root.descendants))
        assert actual == 10, f"Expected tree to have 10 descendants, received {actual}"

    def test_polars_to_tree_by_relation_node_type(self):
        root = construct.polars_to_tree_by_relation(self.relation_data, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        root = construct.polars_to_tree_by_relation(relation_data, node_type=CustomNode)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(_node, CustomNode) for _node in root.children
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
            construct.polars_to_tree_by_relation(relation_data)
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
            construct.polars_to_tree_by_relation(relation_data)
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
            construct.polars_to_tree_by_relation(relation_data)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_DATAFRAME_MULTIPLE_ROOT.format(root_nodes=[])

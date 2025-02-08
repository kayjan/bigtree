import unittest

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
        self.root = node.Node("a", age=1)
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
        construct.add_dict_to_tree_by_path(self.root, self.paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dict_to_tree_by_path_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.add_dict_to_tree_by_path(self.root, {})
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
        construct.add_dict_to_tree_by_path(self.root, paths)
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
        construct.add_dict_to_tree_by_path(self.root, paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dict_to_tree_by_path_sep_error(self):
        root1 = self.root.node_name
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.add_dict_to_tree_by_path(self.root, paths)
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
        construct.add_dict_to_tree_by_path(self.root, paths, sep="-")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_dict_to_tree_by_path_sep_tree(self):
        self.root = node.Node("a", age=89)
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
        construct.add_dict_to_tree_by_path(self.root, paths, sep="\\")
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
        with pytest.raises(exceptions.DuplicatedNodeError) as exc_info:
            construct.add_dict_to_tree_by_path(
                self.root, paths, duplicate_name_allowed=False
            )
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
        construct.add_dict_to_tree_by_path(self.root, paths)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_basenode_root_attr(self.root, f=("d", 38))

    def test_add_dict_to_tree_by_path_node_type(self):
        root = NodeA("a", age=1)
        construct.add_dict_to_tree_by_path(root, self.paths)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        construct.add_dict_to_tree_by_path(root, paths)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(_node, CustomNode) for _node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_add_dict_to_tree_by_path_different_root_error(self):
        root1 = self.root.node_name
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.add_dict_to_tree_by_path(self.root, paths)
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
        self.root = node.Node("a", age=1)
        self.b = node.Node("b", parent=self.root, age=1)
        self.c = node.Node("c", parent=self.root, age=1)
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
        construct.add_dict_to_tree_by_name(self.root, self.name_dict)
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
        construct.add_dict_to_tree_by_name(self.root, name_dict)
        nodes = ["a", "b", "c", "d", "e", "f", "g", "h"]
        expected_list = [[1], [1, 2], [1, None], [None], None, 0, -1, [-1]]
        for node_name, expected in zip(nodes, expected_list):
            actual = search.find_name(self.root, node_name).get_attr("random")
            assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    def test_add_dict_to_tree_by_name_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.add_dict_to_tree_by_name(self.root, {})
        assert str(exc_info.value) == Constants.ERROR_NODE_DICT_EMPTY.format(
            parameter="name_attrs"
        )

    def test_add_dict_to_tree_by_name_sep_tree(self):
        self.root.sep = "\\"
        root = construct.add_dict_to_tree_by_name(self.root, self.name_dict)
        assert_tree_structure_node_root_sep(root)

    def test_add_dict_to_tree_by_name_duplicate_name(self):
        hh = node.Node("h", age=6)
        hh.parent = self.root
        construct.add_dict_to_tree_by_name(self.root, self.name_dict)
        assert (
            len(list(search.find_names(self.root, "h"))) == 2
        ), "There is less node 'h' than expected"
        for _node in list(search.find_names(self.root, "h")):
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
        construct.add_dict_to_tree_by_name(root, self.name_dict)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        construct.add_dict_to_tree_by_name(root, name_dict)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(_node, CustomNode) for _node in root.children
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
        construct.add_dict_to_tree_by_name(self.root, name_dict)
        expected_root_str = "a [age=90]\n" "├── b [age=1]\n" "└── c [age=60]\n"
        assert_print_statement(
            export.print_tree, expected_root_str, self.root, all_attrs=True, max_depth=2
        )


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
        root = construct.dict_to_tree(self.path_dict)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_dict_to_tree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.dict_to_tree({})
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
        root = construct.dict_to_tree(paths)
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
        root = construct.dict_to_tree(paths)
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.dict_to_tree(paths)
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
        root = construct.dict_to_tree(paths, sep="\\")
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
        with pytest.raises(exceptions.DuplicatedNodeError) as exc_info:
            construct.dict_to_tree(path_dict, duplicate_name_allowed=False)
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
        root = construct.dict_to_tree(path_dict)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root, f=("d", 38))
        assert_tree_structure_node_root(root, f="/a/c/d")

    def test_dict_to_tree_node_type(self):
        root = construct.dict_to_tree(self.path_dict, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        root = construct.dict_to_tree(path_dict, node_type=CustomNode)
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
        with pytest.raises(exceptions.TreeError) as exc_info:
            construct.dict_to_tree(path_dict)
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
        root = construct.dict_to_tree(path_dict)
        expected_root_str = "a [age=90]\n" "├── b\n" "└── c [age=60]\n"
        assert_print_statement(
            export.print_tree, expected_root_str, root, all_attrs=True
        )


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
        root = construct.nested_dict_to_tree(self.path_dict)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_nested_dict_to_tree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.nested_dict_to_tree({})
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
            construct.nested_dict_to_tree(path_dict)
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
            construct.nested_dict_to_tree(path_dict)
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
        root = construct.nested_dict_to_tree(
            path_dict, name_key="node_name", child_key="node_children"
        )
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_nested_dict_to_tree_node_type(self):
        root = construct.nested_dict_to_tree(self.path_dict, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
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
        root = construct.nested_dict_to_tree(path_dict, node_type=CustomNode)
        assert isinstance(root, CustomNode), Constants.ERROR_CUSTOM_TYPE.format(
            type="CustomNode"
        )
        assert all(
            isinstance(_node, CustomNode) for _node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="CustomNode")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_customnode_root_attr(root)
        assert_tree_structure_node_root(root)

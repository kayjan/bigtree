import unittest

import pandas as pd
import polars as pl

from bigtree.node import basenode, node
from bigtree.tree.tree import Tree
from tests.conftest import assert_print_statement
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
    assert_tree_structure_basenode_tree,
)
from tests.node.test_node import assert_tree_structure_node_root
from tests.test_constants import Constants
from tests.tree.export.test_stdout import (
    tree_node_hstr,
    tree_node_no_attr_str,
    tree_node_vstr,
)
from tests.tree.test_helper import EXPECTED_TREE_NODE_DIFF

LOCAL = Constants.LOCAL


class TestTree:
    @staticmethod
    def test_tree_magic_methods(tree_tree):
        # Test __repr__
        assert_print_statement(print, "Tree(/a, age=90)\n", tree_tree)

        # Test __copy__, __getitem__, __delitem__
        import copy

        tree_deep_copy = tree_tree.copy()
        tree_shallow_copy = copy.copy(tree_tree)
        del tree_shallow_copy["b"]
        del tree_shallow_copy["something"]
        assert len(tree_tree.node.children) == 1
        assert len(tree_shallow_copy.node.children) == 1
        assert len(tree_deep_copy.node.children) == 2


class TestTreeConstruct(unittest.TestCase):
    @staticmethod
    def test_from_dataframe():
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
            ],
            columns=["PATH", "age"],
        )
        tree = Tree.from_dataframe(path_data)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_basenode_root_attr(tree.node)
        assert_tree_structure_node_root(tree.node)

    @staticmethod
    def test_from_dataframe_relation():
        relation_data = pd.DataFrame(
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
        tree = Tree.from_dataframe_relation(relation_data)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_basenode_root_attr(tree.node)
        assert_tree_structure_node_root(tree.node)

    @staticmethod
    def test_from_polars():
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
            ],
            schema=["PATH", "age"],
        )
        tree = Tree.from_polars(path_data)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_basenode_root_attr(tree.node)
        assert_tree_structure_node_root(tree.node)

    @staticmethod
    def test_from_polars_relation():
        relation_data = pl.DataFrame(
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
        tree = Tree.from_polars_relation(relation_data)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_basenode_root_attr(tree.node)
        assert_tree_structure_node_root(tree.node)

    @staticmethod
    def test_from_dict():
        path_dict = {
            "a": {"age": 90},
            "a/b": {"age": 65},
            "a/c": {"age": 60},
            "a/b/d": {"age": 40},
            "a/b/e": {"age": 35},
            "a/c/f": {"age": 38},
            "a/b/e/g": {"age": 10},
            "a/b/e/h": {"age": 6},
        }
        tree = Tree.from_dict(path_dict)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_basenode_root_attr(tree.node)
        assert_tree_structure_node_root(tree.node)

    @staticmethod
    def test_from_nested_dict():
        nested_dict = {
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
        tree = Tree.from_nested_dict(nested_dict)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_basenode_root_attr(tree.node)
        assert_tree_structure_node_root(tree.node)

    @staticmethod
    def test_from_nested_dict_key():
        nested_dict = {
            "a": {
                "age": 90,
                "children": {
                    "b": {
                        "age": 65,
                        "children": {
                            "d": {"age": 40},
                            "e": {
                                "age": 35,
                                "children": {
                                    "g": {"age": 10},
                                    "h": {"age": 6},
                                },
                            },
                        },
                    },
                    "c": {"age": 60, "children": {"f": {"age": 38}}},
                },
            }
        }
        tree = Tree.from_nested_dict_key(nested_dict)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_basenode_root_attr(tree.node)
        assert_tree_structure_node_root(tree.node)

    @staticmethod
    def test_from_list():
        path_list = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        tree = Tree.from_list(path_list)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_node_root(tree.node)

    @staticmethod
    def test_from_list_relation():
        relations = [
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("b", "e"),
            ("c", "f"),
            ("e", "g"),
            ("e", "h"),
        ]
        tree = Tree.from_list_relation(relations)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_node_root(tree.node)

    @staticmethod
    def test_from_str():
        tree_str = "a\n├── b\n│   ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f"
        tree = Tree.from_str(tree_str)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_node_root(tree.node)

    @staticmethod
    def test_from_newick():
        newick_str = "((d,(g,h)e)b,(f)c)a"
        tree = Tree.from_newick(newick_str)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)


class TestTreeAdd(unittest.TestCase):

    def setUp(self):
        root = node.Node("a", age=1)
        b = node.Node("b", parent=root, age=1)
        c = node.Node("c", parent=root, age=1)
        _ = node.Node("d", parent=b, age=1)
        e = node.Node("e", parent=b)
        _ = node.Node("f", parent=c)
        _ = node.Node("g", parent=e)
        _ = node.Node("h", parent=e)
        self.tree = Tree(root)

    def tearDown(self):
        self.tree = None

    @staticmethod
    def test_add_dataframe_by_path():
        tree = Tree(node.Node("a", age=1))
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
            ],
            columns=["PATH", "age"],
        )
        tree.add_dataframe_by_path(data)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_basenode_root_attr(tree.node)
        assert_tree_structure_node_root(tree.node)

    def test_add_dataframe_by_name(self):
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
            ],
            columns=["NAME", "age"],
        )
        self.tree.add_dataframe_by_name(data)
        assert_tree_structure_basenode_tree(self.tree)
        assert_tree_structure_basenode_root(self.tree.node)
        assert_tree_structure_basenode_root_attr(self.tree.node)
        assert_tree_structure_node_root(self.tree.node)

    @staticmethod
    def test_add_polars_by_path():
        tree = Tree(node.Node("a", age=1))
        data = pl.DataFrame(
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
        tree.add_polars_by_path(data)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_basenode_root_attr(tree.node)
        assert_tree_structure_node_root(tree.node)

    def test_add_polars_by_name(self):
        data = pl.DataFrame(
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
        self.tree.add_polars_by_name(data)
        assert_tree_structure_basenode_tree(self.tree)
        assert_tree_structure_basenode_root(self.tree.node)
        assert_tree_structure_basenode_root_attr(self.tree.node)
        assert_tree_structure_node_root(self.tree.node)

    @staticmethod
    def test_add_dict_by_path():
        tree = Tree(node.Node("a", age=1))
        paths = {
            "a": {"age": 90},
            "a/b": {"age": 65},
            "a/c": {"age": 60},
            "a/b/d": {"age": 40},
            "a/b/e": {"age": 35},
            "a/c/f": {"age": 38},
            "a/b/e/g": {"age": 10},
            "a/b/e/h": {"age": 6},
        }
        tree.add_dict_by_path(paths)
        assert_tree_structure_basenode_tree(tree)
        assert_tree_structure_basenode_root(tree.node)
        assert_tree_structure_basenode_root_attr(tree.node)
        assert_tree_structure_node_root(tree.node)

    def test_add_dict_by_name(self):
        name_dict = {
            "a": {"age": 90},
            "b": {"age": 65},
            "c": {"age": 60},
            "d": {"age": 40},
            "e": {"age": 35},
            "f": {"age": 38},
            "g": {"age": 10},
            "h": {"age": 6},
        }
        self.tree.add_dict_by_name(name_dict)
        assert_tree_structure_basenode_tree(self.tree)
        assert_tree_structure_basenode_root(self.tree.node)
        assert_tree_structure_basenode_root_attr(self.tree.node)
        assert_tree_structure_node_root(self.tree.node)


class TestTreeExport:
    @staticmethod
    def test_to_dataframe(tree_tree):
        expected = pd.DataFrame(
            [
                ["/a", "a"],
                ["/a/b", "b"],
                ["/a/b/d", "d"],
                ["/a/b/e", "e"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c", "c"],
                ["/a/c/f", "f"],
            ],
            columns=["path", "name"],
        )
        actual = tree_tree.to_dataframe()
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_to_polars(tree_tree):
        expected = pl.DataFrame(
            [
                ["/a", "a"],
                ["/a/b", "b"],
                ["/a/b/d", "d"],
                ["/a/b/e", "e"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c", "c"],
                ["/a/c/f", "f"],
            ],
            schema=["path", "name"],
        )
        actual = tree_tree.to_polars()
        assert expected.equals(actual)

    @staticmethod
    def test_to_dict(tree_tree):
        expected = {
            "/a": {"name": "a"},
            "/a/b": {"name": "b"},
            "/a/b/d": {"name": "d"},
            "/a/b/e": {"name": "e"},
            "/a/b/e/g": {"name": "g"},
            "/a/b/e/h": {"name": "h"},
            "/a/c": {"name": "c"},
            "/a/c/f": {"name": "f"},
        }
        actual = tree_tree.to_dict()
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_to_nested_dict(tree_tree):
        name_key = "name"
        child_key = "children"
        expected = {
            name_key: "a",
            child_key: [
                {
                    name_key: "b",
                    child_key: [
                        {name_key: "d"},
                        {name_key: "e", child_key: [{name_key: "g"}, {name_key: "h"}]},
                    ],
                },
                {name_key: "c", child_key: [{name_key: "f"}]},
            ],
        }
        actual = tree_tree.to_nested_dict()
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_to_nested_dict_key(tree_tree):
        child_key = "children"
        expected = {
            "a": {
                child_key: {
                    "b": {
                        child_key: {
                            "d": {},
                            "e": {child_key: {"g": {}, "h": {}}},
                        },
                    },
                    "c": {child_key: {"f": {}}},
                }
            }
        }
        actual = tree_tree.to_nested_dict_key()
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_print_tree(tree_tree):
        assert_print_statement(
            tree_tree.show,
            tree_node_no_attr_str,
        )

    @staticmethod
    def test_hprint_tree(tree_tree):
        assert_print_statement(
            tree_tree.hshow,
            tree_node_hstr,
        )

    @staticmethod
    def test_vprint_tree(tree_tree):
        assert_print_statement(
            tree_tree.vshow,
            tree_node_vstr,
        )

    @staticmethod
    def test_to_newick(tree_tree):
        newick_str = tree_tree.to_newick()
        expected_str = "((d,(g,h)e)b,(f)c)a"
        assert newick_str == expected_str

    @staticmethod
    def test_to_dot(tree_tree):
        graph = tree_tree.to_dot()
        expected = (
            "strict digraph G {\n"
            "rankdir=TB;\n"
            "a0 [label=a];\n"
            "b0 [label=b];\n"
            "a0 -> b0;\n"
            "d0 [label=d];\n"
            "b0 -> d0;\n"
            "e0 [label=e];\n"
            "b0 -> e0;\n"
            "g0 [label=g];\n"
            "e0 -> g0;\n"
            "h0 [label=h];\n"
            "e0 -> h0;\n"
            "c0 [label=c];\n"
            "a0 -> c0;\n"
            "f0 [label=f];\n"
            "c0 -> f0;\n"
            "}\n"
        )
        actual = graph.to_string()
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_to_pillow_graph(tree_tree):
        tree_tree.to_pillow_graph()

    @staticmethod
    def test_to_pillow(tree_tree):
        tree_tree.to_pillow()

    @staticmethod
    def test_to_mermaid(tree_tree):
        mermaid_md = tree_tree.to_mermaid()
        expected_str = (
            """```mermaid\n"""
            """%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\n"""
            """flowchart TB\n"""
            """0("a") --> 0-0("b")\n"""
            """0-0 --> 0-0-0("d")\n"""
            """0-0 --> 0-0-1("e")\n"""
            """0-0-1 --> 0-0-1-0("g")\n"""
            """0-0-1 --> 0-0-1-1("h")\n"""
            """0("a") --> 0-1("c")\n"""
            """0-1 --> 0-1-0("f")\n"""
            """classDef default stroke-width:1\n"""
            """```"""
        )
        assert mermaid_md == expected_str

    @staticmethod
    def test_to_vis(tree_tree):
        tree_tree.to_vis()


class TestTreeHelper:
    @staticmethod
    def test_clone(tree_tree):
        tree_clone = tree_tree.clone(node_type=basenode.BaseNode)
        assert isinstance(tree_clone.node, basenode.BaseNode), "Wrong type returned"
        assert_tree_structure_basenode_root(tree_clone.node)
        assert_tree_structure_basenode_root_attr(tree_clone.node)

    @staticmethod
    def test_prune(tree_tree):
        # Pruned tree is a/b/d, a/b/e/g, a/b/e/h
        tree_prune = tree_tree.prune("a/b")

        assert len(list(tree_prune.node.children)) == 1
        assert len(tree_prune.node.children[0].children) == 2
        assert len(tree_prune.node.children[0].children[0].children) == 0
        assert len(tree_prune.node.children[0].children[1].children) == 2

    @staticmethod
    def test_diff_dataframe(tree_tree):
        tree_tree_diff = tree_tree.copy()
        del tree_tree_diff["c"]
        actual = tree_tree.diff_dataframe(tree_tree_diff, only_diff=True)
        expected = pd.DataFrame(
            [
                ["/a", "a", None, "both", None],
                ["/a/b", "b", "a", "both", None],
                ["/a/b/d", "d", "b", "both", None],
                ["/a/b/e", "e", "b", "both", None],
                ["/a/b/e/g", "g", "e", "both", None],
                ["/a/b/e/h", "h", "e", "both", None],
                ["/a/c", "c", "a", "left_only", "-"],
                ["/a/c/f", "f", "c", "left_only", "-"],
            ],
            columns=["path", "name", "parent", "Exists", "suffix"],
        )
        pd.testing.assert_frame_equal(
            expected, actual, check_dtype=False, check_categorical=False
        )

    @staticmethod
    def test_diff(tree_tree, tree_tree_diff):
        tree_diff = tree_tree.diff(tree_tree_diff)
        assert_print_statement(tree_diff.show, EXPECTED_TREE_NODE_DIFF)


class TestTreeQuery:
    @staticmethod
    def test_query(tree_tree):
        results = tree_tree.query("age >= 30", debug=True)
        expected = ["a", "b", "d", "e", "c", "f"]
        actual = [_node.node_name for _node in results]
        assert (
            actual == expected
        ), f"Wrong query results, expected {expected}, received {actual}"


class TestTreeSearch:
    @staticmethod
    def test_find_all(tree_tree):
        actual = tree_tree.findall(lambda _node: _node.age >= 60)
        expected = (tree_tree.node, tree_tree.node["b"], tree_tree.node["c"])
        assert (
            actual == expected
        ), f"Expected find_all to return {expected}, received {actual}"

    @staticmethod
    def test_find(tree_tree):
        actual = tree_tree.find(lambda _node: _node.age == 60)
        expected = tree_tree.node["c"]
        assert (
            actual == expected
        ), f"Expected find to return {expected}, received {actual}"

    @staticmethod
    def test_find_name(tree_tree):
        actual = tree_tree.find_name("a")
        expected = tree_tree.node
        assert (
            actual == expected
        ), f"Expected find_name to return {expected}, received {actual}"

    @staticmethod
    def test_find_names(tree_tree):
        actual = tree_tree.find_names("a")
        expected = (tree_tree.node,)
        assert (
            actual == expected
        ), f"Expected find_name to return {expected}, received {actual}"

    @staticmethod
    def test_find_relative_path(tree_tree):
        inputs = (".", "b")
        expected_ans = (tree_tree.node, tree_tree.node["b"])
        for input_, expected in zip(inputs, expected_ans):
            actual = tree_tree.find_relative_path(input_)
            assert (
                actual == expected
            ), f"Expected find_path to return {expected}, received {actual}"

    @staticmethod
    def test_find_relative_paths(tree_tree):
        actual = tree_tree.find_relative_paths("*")
        expected = (tree_tree.node["b"], tree_tree.node["c"])
        assert (
            actual == expected
        ), f"Expected find_name to return {expected}, received {actual}"

    @staticmethod
    def test_find_full_path(tree_tree):
        inputs = [
            "a",
            "a/b",
            "a/c",
        ]
        expected_ans = (tree_tree.node, tree_tree.node["b"], tree_tree.node["c"])
        for input_, expected in zip(inputs, expected_ans):
            actual = tree_tree.find_full_path(input_)
            assert (
                actual == expected
            ), f"Expected find_full_path to return {expected}, received {actual}"

    @staticmethod
    def test_find_path(tree_tree):
        inputs = [
            "a",
            "a/b",
            "a/c",
        ]
        expected_ans = (tree_tree.node, tree_tree.node["b"], tree_tree.node["c"])
        for input_, expected in zip(inputs, expected_ans):
            actual = tree_tree.find_path(input_)
            assert (
                actual == expected
            ), f"Expected find_path to return {expected}, received {actual}"

    @staticmethod
    def test_find_paths(tree_tree):
        inputs = [
            "a",
            "a/b",
            "a/c",
        ]
        expected_ans = (
            (tree_tree.node,),
            (tree_tree.node["b"],),
            (tree_tree.node["c"],),
        )
        for input_, expected in zip(inputs, expected_ans):
            actual = tree_tree.find_paths(input_)
            assert (
                actual == expected
            ), f"Expected find_path to return {expected}, received {actual}"

    @staticmethod
    def test_find_attr(tree_tree):
        inputs = ["a", "b", "c", "i"]
        expected_ans = (tree_tree.node, tree_tree.node["b"], tree_tree.node["c"], None)
        for input_, expected in zip(inputs, expected_ans):
            actual = tree_tree.find_attr("name", input_)
            assert (
                actual == expected
            ), f"Expected find_attr to return {expected}, received {actual}"

        inputs = [90, 65, 60, 1]
        expected_ans = (tree_tree.node, tree_tree.node["b"], tree_tree.node["c"], None)
        for input_, expected in zip(inputs, expected_ans):
            actual = tree_tree.find_attr("age", input_)
            assert (
                actual == expected
            ), f"Expected find_attr to return {expected}, received {actual}"

    @staticmethod
    def test_find_attrs(tree_tree):
        inputs = ["a", "b", "c", "i"]
        expected_ans = (
            (tree_tree.node,),
            (tree_tree.node["b"],),
            (tree_tree.node["c"],),
            (),
        )
        for input_, expected in zip(inputs, expected_ans):
            actual = tree_tree.find_attrs("name", input_)
            assert (
                actual == expected
            ), f"Expected find_attr to return {expected}, received {actual}"

        inputs = [90, 65, 60, 1]
        expected_ans = (
            (tree_tree.node,),
            (tree_tree.node["b"],),
            (tree_tree.node["c"],),
            (),
        )
        for input_, expected in zip(inputs, expected_ans):
            actual = tree_tree.find_attrs("age", input_)
            assert (
                actual == expected
            ), f"Expected find_attr to return {expected}, received {actual}"

    @staticmethod
    def test_find_children(tree_tree):
        actual = tree_tree.find_children(lambda _node: _node.age > 1)
        expected = (tree_tree.node["b"], tree_tree.node["c"])
        assert (
            actual == expected
        ), f"Expected find_attr to return {expected}, received {actual}"

    @staticmethod
    def test_find_child(tree_tree):
        inputs = [tree_tree, tree_tree["b"], tree_tree["c"], tree_tree["b"]["e"]]
        expected_ans = (
            tree_tree.node["b"],
            tree_tree.node["b"]["e"],
            tree_tree.node["c"]["f"],
            tree_tree.node["b"]["e"]["g"],
        )
        for input_, expected in zip(inputs, expected_ans):
            actual = input_.find_child(
                lambda _node: any(
                    _node.node_name.startswith(_name) for _name in ["b", "e", "f", "g"]
                )
            )
            assert (
                actual == expected
            ), f"Expected find_attr to return {expected}, received {actual}"

    @staticmethod
    def test_find_child_by_name(tree_tree):
        inputs1 = [tree_tree, tree_tree["b"], tree_tree["c"], tree_tree["b"]["e"]]
        inputs2 = ["b", "e", "f", "g"]
        expected_ans = (
            tree_tree.node["b"],
            tree_tree.node["b"]["e"],
            tree_tree.node["c"]["f"],
            tree_tree.node["b"]["e"]["g"],
        )
        for input1_, input2_, expected in zip(inputs1, inputs2, expected_ans):
            actual = input1_.find_child_by_name(input2_)
            assert (
                actual == expected
            ), f"Expected find_attr to return {expected}, received {actual}"


class TestTreeIterators:
    @staticmethod
    def test_preorder_iter(tree_tree):
        expected = ["a", "b", "d", "e", "g", "h", "c", "f"]
        actual = [node.node_name for node in tree_tree.preorder_iter()]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter(tree_tree):
        expected = ["d", "g", "h", "e", "b", "f", "c", "a"]
        actual = [node.node_name for node in tree_tree.postorder_iter()]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter(tree_tree):
        expected = ["a", "b", "c", "d", "e", "f", "g", "h"]
        actual = [node.node_name for node in tree_tree.levelorder_iter()]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter(tree_tree):
        expected = [["a"], ["b", "c"], ["d", "e", "f"], ["g", "h"]]
        actual = [
            [node.node_name for node in group]
            for group in tree_tree.levelordergroup_iter()
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzag_iter(tree_tree):
        expected = ["a", "c", "b", "d", "e", "f", "h", "g"]
        actual = [node.node_name for node in tree_tree.zigzag_iter()]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzaggroup_iter(tree_tree):
        expected = [["a"], ["c", "b"], ["d", "e", "f"], ["h", "g"]]
        actual = [
            [node.node_name for node in group] for group in tree_tree.zigzaggroup_iter()
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


class TestTreePlot:
    @staticmethod
    def test_plot(tree_tree):
        root = node.Node("a", children=[node.Node("b"), node.Node("c")])
        tree = Tree(root)
        fig = tree.plot()
        if LOCAL:
            fig.savefig(f"{Constants.LOCAL_FILE}/tree.test_plot.png")
        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)

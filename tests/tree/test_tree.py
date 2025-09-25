import unittest

import pandas as pd
import polars as pl

from bigtree.tree.tree import Tree
from tests.conftest import assert_print_statement
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
)
from tests.node.test_node import assert_tree_structure_node_root
from tests.tree.export.test_stdout import (
    tree_node_hstr,
    tree_node_no_attr_str,
    tree_node_vstr,
)


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
        assert_tree_structure_basenode_root(tree.root)
        assert_tree_structure_basenode_root_attr(tree.root)
        assert_tree_structure_node_root(tree.root)

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
        assert_tree_structure_basenode_root(tree.root)
        assert_tree_structure_basenode_root_attr(tree.root)
        assert_tree_structure_node_root(tree.root)

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
        assert_tree_structure_basenode_root(tree.root)
        assert_tree_structure_basenode_root_attr(tree.root)
        assert_tree_structure_node_root(tree.root)

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
        assert_tree_structure_basenode_root(tree.root)
        assert_tree_structure_basenode_root_attr(tree.root)
        assert_tree_structure_node_root(tree.root)

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
        assert_tree_structure_basenode_root(tree.root)
        assert_tree_structure_basenode_root_attr(tree.root)
        assert_tree_structure_node_root(tree.root)

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
        assert_tree_structure_basenode_root(tree.root)
        assert_tree_structure_basenode_root_attr(tree.root)
        assert_tree_structure_node_root(tree.root)

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
        assert_tree_structure_basenode_root(tree.root)
        assert_tree_structure_basenode_root_attr(tree.root)
        assert_tree_structure_node_root(tree.root)

    @staticmethod
    def test_from_list():
        path_list = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]
        tree = Tree.from_list(path_list)
        assert_tree_structure_basenode_root(tree.root)
        assert_tree_structure_node_root(tree.root)

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
        assert_tree_structure_basenode_root(tree.root)
        assert_tree_structure_node_root(tree.root)

    @staticmethod
    def test_from_str():
        tree_str = "a\n├── b\n│   ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f"
        tree = Tree.from_str(tree_str)
        assert_tree_structure_basenode_root(tree.root)
        assert_tree_structure_node_root(tree.root)

    @staticmethod
    def test_from_newick():
        newick_str = "((d,(g,h)e)b,(f)c)a"
        tree = Tree.from_newick(newick_str)
        assert_tree_structure_basenode_root(tree.root)


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

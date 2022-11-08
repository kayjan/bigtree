import pandas as pd
import pytest

from bigtree.tree.construct import dataframe_to_tree, dict_to_tree, nested_dict_to_tree
from bigtree.tree.export import (
    print_tree,
    tree_to_dataframe,
    tree_to_dict,
    tree_to_dot,
    tree_to_nested_dict,
)
from tests.conftest import assert_print_statement
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root_attr,
    assert_tree_structure_basenode_root_generic,
)
from tests.node.test_node import assert_tree_structure_node_root_generic


class TestPrintTree:
    @staticmethod
    def test_print_tree_ansi(tree_node):
        expected_str = """a\n|-- b\n|   |-- d\n|   `-- e\n|       |-- g\n|       `-- h\n`-- c\n    `-- f\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_node, style="ansi")

    @staticmethod
    def test_print_tree_ascii(tree_node):
        expected_str = """a\n|-- b\n|   |-- d\n|   +-- e\n|       |-- g\n|       +-- h\n+-- c\n    +-- f\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_node, style="ascii")

    @staticmethod
    def test_print_tree_const(tree_node):
        expected_str = """a\n├── b\n│   ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_node, style="const")

    @staticmethod
    def test_print_tree_const_bold(tree_node):
        expected_str = """a\n┣━━ b\n┃   ┣━━ d\n┃   ┗━━ e\n┃       ┣━━ g\n┃       ┗━━ h\n┗━━ c\n    ┗━━ f\n"""
        assert_print_statement(
            print_tree, expected_str, tree=tree_node, style="const_bold"
        )

    @staticmethod
    def test_print_tree_rounded(tree_node):
        expected_str = """a\n├── b\n│   ├── d\n│   ╰── e\n│       ├── g\n│       ╰── h\n╰── c\n    ╰── f\n"""
        assert_print_statement(
            print_tree, expected_str, tree=tree_node, style="rounded"
        )

    @staticmethod
    def test_print_tree_double(tree_node):
        expected_str = """a\n╠══ b\n║   ╠══ d\n║   ╚══ e\n║       ╠══ g\n║       ╚══ h\n╚══ c\n    ╚══ f\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_node, style="double")

    @staticmethod
    def test_print_tree_custom(tree_node):
        expected_str = """a\nb\nd\ne\ng\nh\nc\nf\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_node, style="custom")

    @staticmethod
    def test_print_tree_unknown_style(tree_node):
        with pytest.raises(ValueError):
            print_tree(tree_node, style="something")

    @staticmethod
    def test_print_tree_no_attr(tree_node):
        expected_str = """a\n|-- b\n|   |-- d\n|   `-- e\n|       |-- g\n|       `-- h\n`-- c\n    `-- f\n"""
        assert_print_statement(
            print_tree, expected_str, tree=tree_node, attr_list=["random"], style="ansi"
        )

    @staticmethod
    def test_print_tree_child_node(tree_node):
        expected_str = """b\n|-- d\n`-- e\n    |-- g\n    `-- h\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_node, node_name="b")

    @staticmethod
    def test_print_tree_unequal_char(tree_node):
        with pytest.raises(ValueError):
            print_tree(
                tree_node,
                style="custom",
                style_stem="",
                style_branch=" ",
                style_stem_final="",
            )

    @staticmethod
    def test_print_tree_attr(tree_node):
        expected_str = """a [age=90]\n|-- b [age=65]\n|   |-- d [age=40]\n|   `-- e [age=35]\n|       |-- g [age=10]\n|       `-- h [age=6]\n`-- c [age=60]\n    `-- f [age=38]\n"""
        assert_print_statement(
            print_tree,
            expected_str,
            tree=tree_node,
            attr_list=["age"],
            attr_omit_null=False,
        )

    @staticmethod
    def test_print_tree_all_attr(tree_node):
        expected_str = """a [age=90]\n|-- b [age=65]\n|   |-- d [age=40]\n|   `-- e [age=35]\n|       |-- g [age=10]\n|       `-- h [age=6]\n`-- c [age=60]\n    `-- f [age=38]\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_node, all_attrs=True)

    @staticmethod
    def test_print_tree_all_attr_empty(tree_node_no_attr):
        expected_str = """a\n|-- b\n|   |-- d\n|   `-- e\n|       |-- g\n|       `-- h\n`-- c\n    `-- f\n"""
        assert_print_statement(
            print_tree, expected_str, tree=tree_node_no_attr, all_attrs=True
        )


class TestTreeToDataFrame:
    @staticmethod
    def test_tree_to_dataframe(tree_node):
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
        actual = tree_to_dataframe(tree_node)
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_path_col(tree_node):
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
            columns=["PATH", "name"],
        )
        actual = tree_to_dataframe(tree_node, path_col="PATH")
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_path_col_missing(tree_node):
        expected = pd.DataFrame(
            [
                ["a"],
                ["b"],
                ["d"],
                ["e"],
                ["g"],
                ["h"],
                ["c"],
                ["f"],
            ],
            columns=["name"],
        )
        actual = tree_to_dataframe(tree_node, path_col="")
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_name_col(tree_node):
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
            columns=["path", "NAME"],
        )
        actual = tree_to_dataframe(tree_node, name_col="NAME")
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_name_col_missing(tree_node):
        expected = pd.DataFrame(
            [
                ["/a"],
                ["/a/b"],
                ["/a/b/d"],
                ["/a/b/e"],
                ["/a/b/e/g"],
                ["/a/b/e/h"],
                ["/a/c"],
                ["/a/c/f"],
            ],
            columns=["path"],
        )
        actual = tree_to_dataframe(tree_node, name_col="")
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_name_path_col_missing(tree_node):
        expected = pd.DataFrame()
        expected.index = range(8)
        actual = tree_to_dataframe(tree_node, name_col="", path_col="")
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_parent_col(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a", None],
                ["/a/b", "b", "a"],
                ["/a/b/d", "d", "b"],
                ["/a/b/e", "e", "b"],
                ["/a/b/e/g", "g", "e"],
                ["/a/b/e/h", "h", "e"],
                ["/a/c", "c", "a"],
                ["/a/c/f", "f", "c"],
            ],
            columns=["path", "name", "parent"],
        )
        actual = tree_to_dataframe(tree_node, parent_col="parent")
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_attr_dict(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a", 90],
                ["/a/b", "b", 65],
                ["/a/b/d", "d", 40],
                ["/a/b/e", "e", 35],
                ["/a/b/e/g", "g", 10],
                ["/a/b/e/h", "h", 6],
                ["/a/c", "c", 60],
                ["/a/c/f", "f", 38],
            ],
            columns=["path", "name", "AGE"],
        )
        actual = tree_to_dataframe(tree_node, attr_dict={"age": "AGE"})
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_all_attr(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a", 90],
                ["/a/b", "b", 65],
                ["/a/b/d", "d", 40],
                ["/a/b/e", "e", 35],
                ["/a/b/e/g", "g", 10],
                ["/a/b/e/h", "h", 6],
                ["/a/c", "c", 60],
                ["/a/c/f", "f", 38],
            ],
            columns=["path", "name", "age"],
        )
        actual = tree_to_dataframe(tree_node, all_attrs=True)
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_max_depth(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a"],
                ["/a/b", "b"],
                ["/a/c", "c"],
            ],
            columns=["path", "name"],
        )
        actual = tree_to_dataframe(tree_node, max_depth=2)
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_skip_depth(tree_node):
        expected = pd.DataFrame(
            [
                ["/a/b/d", "d"],
                ["/a/b/e", "e"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c/f", "f"],
            ],
            columns=["path", "name"],
        )
        actual = tree_to_dataframe(tree_node, skip_depth=2)
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_leaf_only(tree_node):
        expected = pd.DataFrame(
            [
                ["/a/b/d", "d"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c/f", "f"],
            ],
            columns=["path", "name"],
        )
        actual = tree_to_dataframe(tree_node, leaf_only=True)
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_multiple_columns(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a", None, 90],
                ["/a/b", "b", "a", 65],
                ["/a/b/d", "d", "b", 40],
                ["/a/b/e", "e", "b", 35],
                ["/a/b/e/g", "g", "e", 10],
                ["/a/b/e/h", "h", "e", 6],
                ["/a/c", "c", "a", 60],
                ["/a/c/f", "f", "c", 38],
            ],
            columns=["PATH", "NAME", "PARENT", "AGE"],
        )
        actual = tree_to_dataframe(
            tree_node,
            name_col="NAME",
            path_col="PATH",
            parent_col="PARENT",
            attr_dict={"age": "AGE"},
        )
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_multiple_cols_subset_tree(tree_node):
        expected = pd.DataFrame(
            [
                ["/a/b", "b", "a", 65],
                ["/a/b/d", "d", "b", 40],
                ["/a/b/e", "e", "b", 35],
                ["/a/b/e/g", "g", "e", 10],
                ["/a/b/e/h", "h", "e", 6],
            ],
            columns=["PATH", "NAME", "PARENT", "AGE"],
        )
        actual = tree_to_dataframe(
            tree_node.children[0],
            name_col="NAME",
            path_col="PATH",
            parent_col="PARENT",
            attr_dict={"age": "AGE"},
        )
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_to_tree(tree_node):
        d = tree_to_dataframe(tree_node, all_attrs=True)
        tree = dataframe_to_tree(d)
        assert_tree_structure_basenode_root_generic(tree)
        assert_tree_structure_basenode_root_attr(tree)
        assert_tree_structure_node_root_generic(tree)


class TestTreeToDict:
    @staticmethod
    def test_tree_to_dict(tree_node):
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
        actual = tree_to_dict(tree_node)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_name_key_empty(tree_node):
        expected = {
            "/a": {},
            "/a/b": {},
            "/a/b/d": {},
            "/a/b/e": {},
            "/a/b/e/g": {},
            "/a/b/e/h": {},
            "/a/c": {},
            "/a/c/f": {},
        }
        actual = tree_to_dict(tree_node, name_key="")
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_name_key(tree_node):
        expected = {
            "/a": {"NAME": "a"},
            "/a/b": {"NAME": "b"},
            "/a/b/d": {"NAME": "d"},
            "/a/b/e": {"NAME": "e"},
            "/a/b/e/g": {"NAME": "g"},
            "/a/b/e/h": {"NAME": "h"},
            "/a/c": {"NAME": "c"},
            "/a/c/f": {"NAME": "f"},
        }
        actual = tree_to_dict(tree_node, name_key="NAME")
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_parent_key(tree_node):
        expected = {
            "/a": {"name": "a", "PARENT": None},
            "/a/b": {"name": "b", "PARENT": "a"},
            "/a/b/d": {"name": "d", "PARENT": "b"},
            "/a/b/e": {"name": "e", "PARENT": "b"},
            "/a/b/e/g": {"name": "g", "PARENT": "e"},
            "/a/b/e/h": {"name": "h", "PARENT": "e"},
            "/a/c": {"name": "c", "PARENT": "a"},
            "/a/c/f": {"name": "f", "PARENT": "c"},
        }
        actual = tree_to_dict(tree_node, parent_key="PARENT")
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_attr_dict(tree_node):
        expected = {
            "/a": {"name": "a", "AGE": 90},
            "/a/b": {"name": "b", "AGE": 65},
            "/a/b/d": {"name": "d", "AGE": 40},
            "/a/b/e": {"name": "e", "AGE": 35},
            "/a/b/e/g": {"name": "g", "AGE": 10},
            "/a/b/e/h": {"name": "h", "AGE": 6},
            "/a/c": {"name": "c", "AGE": 60},
            "/a/c/f": {"name": "f", "AGE": 38},
        }
        actual = tree_to_dict(tree_node, attr_dict={"age": "AGE"})
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_all_attr(tree_node):
        expected = {
            "/a": {"name": "a", "age": 90},
            "/a/b": {"name": "b", "age": 65},
            "/a/b/d": {"name": "d", "age": 40},
            "/a/b/e": {"name": "e", "age": 35},
            "/a/b/e/g": {"name": "g", "age": 10},
            "/a/b/e/h": {"name": "h", "age": 6},
            "/a/c": {"name": "c", "age": 60},
            "/a/c/f": {"name": "f", "age": 38},
        }
        actual = tree_to_dict(tree_node, all_attrs=True)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_max_depth(tree_node):
        expected = {
            "/a": {"name": "a"},
            "/a/b": {"name": "b"},
            "/a/c": {"name": "c"},
        }
        actual = tree_to_dict(tree_node, max_depth=2)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_skip_depth(tree_node):
        expected = {
            "/a/b/d": {"name": "d"},
            "/a/b/e": {"name": "e"},
            "/a/b/e/g": {"name": "g"},
            "/a/b/e/h": {"name": "h"},
            "/a/c/f": {"name": "f"},
        }
        actual = tree_to_dict(tree_node, skip_depth=2)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_leaf_only(tree_node):
        expected = {
            "/a/b/d": {"name": "d"},
            "/a/b/e/g": {"name": "g"},
            "/a/b/e/h": {"name": "h"},
            "/a/c/f": {"name": "f"},
        }
        actual = tree_to_dict(tree_node, leaf_only=True)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_multiple_keys(tree_node):
        expected = {
            "/a": {"NAME": "a", "PARENT": None, "AGE": 90},
            "/a/b": {"NAME": "b", "PARENT": "a", "AGE": 65},
            "/a/b/d": {"NAME": "d", "PARENT": "b", "AGE": 40},
            "/a/b/e": {"NAME": "e", "PARENT": "b", "AGE": 35},
            "/a/b/e/g": {"NAME": "g", "PARENT": "e", "AGE": 10},
            "/a/b/e/h": {"NAME": "h", "PARENT": "e", "AGE": 6},
            "/a/c": {"NAME": "c", "PARENT": "a", "AGE": 60},
            "/a/c/f": {"NAME": "f", "PARENT": "c", "AGE": 38},
        }
        actual = tree_to_dict(
            tree_node, name_key="NAME", parent_key="PARENT", attr_dict={"age": "AGE"}
        )
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_multiple_keys_subset_tree(tree_node):
        expected = {
            "/a/b": {"NAME": "b", "PARENT": "a", "AGE": 65},
            "/a/b/d": {"NAME": "d", "PARENT": "b", "AGE": 40},
            "/a/b/e": {"NAME": "e", "PARENT": "b", "AGE": 35},
            "/a/b/e/g": {"NAME": "g", "PARENT": "e", "AGE": 10},
            "/a/b/e/h": {"NAME": "h", "PARENT": "e", "AGE": 6},
        }
        actual = tree_to_dict(
            tree_node.children[0],
            name_key="NAME",
            parent_key="PARENT",
            attr_dict={"age": "AGE"},
        )
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_to_tree(tree_node):
        d = tree_to_dict(tree_node, all_attrs=True)
        tree = dict_to_tree(d)
        assert_tree_structure_basenode_root_generic(tree)
        assert_tree_structure_basenode_root_attr(tree)
        assert_tree_structure_node_root_generic(tree)


class TestTreeToNestedDict:
    @staticmethod
    def test_tree_to_nested_dict(tree_node):
        expected = {
            "name": "a",
            "children": [
                {
                    "name": "b",
                    "children": [
                        {"name": "d"},
                        {"name": "e", "children": [{"name": "g"}, {"name": "h"}]},
                    ],
                },
                {"name": "c", "children": [{"name": "f"}]},
            ],
        }
        actual = tree_to_nested_dict(tree_node)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_name_key(tree_node):
        expected = {
            "NAME": "a",
            "children": [
                {
                    "NAME": "b",
                    "children": [
                        {"NAME": "d"},
                        {"NAME": "e", "children": [{"NAME": "g"}, {"NAME": "h"}]},
                    ],
                },
                {"NAME": "c", "children": [{"NAME": "f"}]},
            ],
        }
        actual = tree_to_nested_dict(tree_node, name_key="NAME")
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_child_key(tree_node):
        expected = {
            "name": "a",
            "CHILDREN": [
                {
                    "name": "b",
                    "CHILDREN": [
                        {"name": "d"},
                        {"name": "e", "CHILDREN": [{"name": "g"}, {"name": "h"}]},
                    ],
                },
                {"name": "c", "CHILDREN": [{"name": "f"}]},
            ],
        }
        actual = tree_to_nested_dict(tree_node, child_key="CHILDREN")
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_attr_dict(tree_node):
        expected = {
            "name": "a",
            "AGE": 90,
            "children": [
                {
                    "name": "b",
                    "AGE": 65,
                    "children": [
                        {"name": "d", "AGE": 40},
                        {
                            "name": "e",
                            "AGE": 35,
                            "children": [
                                {"name": "g", "AGE": 10},
                                {"name": "h", "AGE": 6},
                            ],
                        },
                    ],
                },
                {"name": "c", "AGE": 60, "children": [{"name": "f", "AGE": 38}]},
            ],
        }
        actual = tree_to_nested_dict(tree_node, attr_dict={"age": "AGE"})
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_all_attr(tree_node):
        expected = {
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
        actual = tree_to_nested_dict(tree_node, all_attrs=True)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_max_depth(tree_node):
        expected = {"name": "a", "children": [{"name": "b"}, {"name": "c"}]}
        actual = tree_to_nested_dict(tree_node, max_depth=2)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_multiple_keys(tree_node):
        expected = {
            "NAME": "a",
            "AGE": 90,
            "CHILDREN": [
                {
                    "NAME": "b",
                    "AGE": 65,
                    "CHILDREN": [
                        {"NAME": "d", "AGE": 40},
                        {
                            "NAME": "e",
                            "AGE": 35,
                            "CHILDREN": [
                                {"NAME": "g", "AGE": 10},
                                {"NAME": "h", "AGE": 6},
                            ],
                        },
                    ],
                },
                {"NAME": "c", "AGE": 60, "CHILDREN": [{"NAME": "f", "AGE": 38}]},
            ],
        }
        actual = tree_to_nested_dict(
            tree_node, name_key="NAME", child_key="CHILDREN", attr_dict={"age": "AGE"}
        )
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_multiple_keys_subset_tree(tree_node):
        expected = {
            "NAME": "b",
            "AGE": 65,
            "CHILDREN": [
                {"NAME": "d", "AGE": 40},
                {
                    "NAME": "e",
                    "AGE": 35,
                    "CHILDREN": [{"NAME": "g", "AGE": 10}, {"NAME": "h", "AGE": 6}],
                },
            ],
        }
        actual = tree_to_nested_dict(
            tree_node.children[0],
            name_key="NAME",
            child_key="CHILDREN",
            attr_dict={"age": "AGE"},
        )
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_to_tree(tree_node):
        d = tree_to_nested_dict(tree_node, all_attrs=True)
        tree = nested_dict_to_tree(d)
        assert_tree_structure_basenode_root_generic(tree)
        assert_tree_structure_basenode_root_attr(tree)
        assert_tree_structure_node_root_generic(tree)


class TestTreeToDot:
    @staticmethod
    def test_tree_to_dot(tree_node):
        graph = tree_to_dot(tree_node)
        expected = """strict digraph G {\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -> b0;\nd0 [label=d];\nb0 -> d0;\ne0 [label=e];\nb0 -> e0;\ng0 [label=g];\ne0 -> g0;\nh0 [label=h];\ne0 -> h0;\nc0 [label=c];\na0 -> c0;\nf0 [label=f];\nc0 -> f0;\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/tree.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_duplicate_names(tree_node_duplicate_names):
        graph = tree_to_dot(tree_node_duplicate_names)
        expected = """strict digraph G {\nrankdir=TB;\na0 [label=a];\na1 [label=a];\na0 -> a1;\na2 [label=a];\na1 -> a2;\nb0 [label=b];\na1 -> b0;\na3 [label=a];\nb0 -> a3;\nb1 [label=b];\nb0 -> b1;\nb2 [label=b];\na0 -> b2;\na4 [label=a];\nb2 -> a4;\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/tree_duplicate.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_type_error(dag_node):
        with pytest.raises(ValueError) as exc_info:
            tree_to_dot(dag_node)
        assert str(exc_info.value).startswith("Tree should be of type `Node`")

    @staticmethod
    def test_tree_to_dot_directed(tree_node):
        graph = tree_to_dot(tree_node, directed=False)
        expected = """strict graph G {\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -- b0;\nd0 [label=d];\nb0 -- d0;\ne0 [label=e];\nb0 -- e0;\ng0 [label=g];\ne0 -- g0;\nh0 [label=h];\ne0 -- h0;\nc0 [label=c];\na0 -- c0;\nf0 [label=f];\nc0 -- f0;\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/tree_undirected.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_bg_color(tree_node):
        graph = tree_to_dot(tree_node, bgcolor="blue")
        expected = """strict digraph G {\nbgcolor=blue;\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -> b0;\nd0 [label=d];\nb0 -> d0;\ne0 [label=e];\nb0 -> e0;\ng0 [label=g];\ne0 -> g0;\nh0 [label=h];\ne0 -> h0;\nc0 [label=c];\na0 -> c0;\nf0 [label=f];\nc0 -> f0;\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/tree_bg.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_fill_color(tree_node):
        graph = tree_to_dot(tree_node, node_colour="gold")
        expected = """strict digraph G {\nrankdir=TB;\na0 [fillcolor=gold, label=a, style=filled];\nb0 [fillcolor=gold, label=b, style=filled];\na0 -> b0;\nd0 [fillcolor=gold, label=d, style=filled];\nb0 -> d0;\ne0 [fillcolor=gold, label=e, style=filled];\nb0 -> e0;\ng0 [fillcolor=gold, label=g, style=filled];\ne0 -> g0;\nh0 [fillcolor=gold, label=h, style=filled];\ne0 -> h0;\nc0 [fillcolor=gold, label=c, style=filled];\na0 -> c0;\nf0 [fillcolor=gold, label=f, style=filled];\nc0 -> f0;\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/tree_fill.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_edge_colour(tree_node):
        graph = tree_to_dot(tree_node, edge_colour="red")
        expected = """strict digraph G {\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -> b0  [color=red];\nd0 [label=d];\nb0 -> d0  [color=red];\ne0 [label=e];\nb0 -> e0  [color=red];\ng0 [label=g];\ne0 -> g0  [color=red];\nh0 [label=h];\ne0 -> h0  [color=red];\nc0 [label=c];\na0 -> c0  [color=red];\nf0 [label=f];\nc0 -> f0  [color=red];\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/tree_edge.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_node_attr(tree_node_style):
        graph = tree_to_dot(tree_node_style, node_attr="node_style")
        expected = """strict digraph G {\nrankdir=TB;\na0 [fillcolor=gold, label=a, style=filled];\nb0 [fillcolor=blue, label=b, style=filled];\na0 -> b0;\nd0 [fillcolor=green, label=d, style=filled];\nb0 -> d0;\ng0 [fillcolor=red, label=g, style=filled];\nd0 -> g0;\ne0 [fillcolor=green, label=e, style=filled];\nb0 -> e0;\nh0 [fillcolor=red, label=h, style=filled];\ne0 -> h0;\nc0 [fillcolor=blue, label=c, style=filled];\na0 -> c0;\nf0 [fillcolor=green, label=f, style=filled];\nc0 -> f0;\n}\n"""
        actual = graph.to_string()
        graph.write_png("tests/tree_style.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

import pandas as pd
import pytest

from bigtree.tree.construct import dataframe_to_tree, dict_to_tree, nested_dict_to_tree
from bigtree.tree.export import (
    print_tree,
    tree_to_dataframe,
    tree_to_dict,
    tree_to_dot,
    tree_to_mermaid,
    tree_to_nested_dict,
    tree_to_pillow,
)
from tests.conftest import assert_print_statement
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
)
from tests.node.test_node import assert_tree_structure_node_root
from tests.test_constants import Constants

tree_node_str = """a [age=90]\n├── b [age=65]\n│   ├── d [age=40]\n│   └── e [age=35]\n│       ├── g [age=10]
│       └── h [age=6]\n└── c [age=60]\n    └── f [age=38]\n"""
tree_node_no_attr_str = """a\n├── b\n│   ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f\n"""

LOCAL = Constants.LOCAL


class TestPrintTree:
    @staticmethod
    def test_print_tree_child_node_name(tree_node):
        expected_str = """b\n├── d\n└── e\n    ├── g\n    └── h\n"""
        assert_print_statement(
            print_tree,
            expected_str,
            tree=tree_node,
            node_name_or_path="b",
        )

    @staticmethod
    def test_print_tree_child_node_name_error(tree_node):
        node_name_or_path = "z"
        with pytest.raises(ValueError) as exc_info:
            print_tree(tree_node, node_name_or_path=node_name_or_path)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_EXPORT_PRINT_INVALID_PATH.format(
            node_name_or_path=node_name_or_path
        )

    @staticmethod
    def test_print_tree_child_node_path(tree_node):
        expected_str = """b\n├── d\n└── e\n    ├── g\n    └── h\n"""
        assert_print_statement(
            print_tree,
            expected_str,
            tree=tree_node,
            node_name_or_path="a/b",
        )

    # all_attr
    @staticmethod
    def test_print_tree_all_attr(tree_node):
        assert_print_statement(
            print_tree, tree_node_str, tree=tree_node, all_attrs=True
        )

    @staticmethod
    def test_print_tree_all_attr_empty(tree_node_no_attr):
        assert_print_statement(
            print_tree,
            tree_node_no_attr_str,
            tree=tree_node_no_attr,
            all_attrs=True,
        )

    # attr_list
    @staticmethod
    def test_print_tree_attr_list(tree_node):
        assert_print_statement(
            print_tree, tree_node_str, tree=tree_node, attr_list=["age"]
        )

    @staticmethod
    def test_print_tree_invalid_attr(tree_node):
        assert_print_statement(
            print_tree, tree_node_no_attr_str, tree=tree_node, attr_list=["random"]
        )

    # attr_list, attr_omit_null
    @staticmethod
    def test_print_tree_attr_omit_null_false(tree_node_negative_null_attr):
        expected_str = """a\n├── b [age=-1]\n│   ├── d [age=1]\n│   └── e [age=None]\n│       ├── g\n│       └── h\n└── c [age=0]\n    └── f\n"""
        assert_print_statement(
            print_tree,
            expected_str,
            tree=tree_node_negative_null_attr,
            attr_list=["age"],
            attr_omit_null=False,
        )

    @staticmethod
    def test_print_tree_attr_omit_null_true(tree_node_negative_null_attr):
        expected_str = """a\n├── b [age=-1]\n│   ├── d [age=1]\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f\n"""
        assert_print_statement(
            print_tree,
            expected_str,
            tree=tree_node_negative_null_attr,
            attr_list=["age"],
            attr_omit_null=True,
        )

    # attr_bracket
    @staticmethod
    def test_print_tree_attr_bracket(tree_node):
        assert_print_statement(
            print_tree,
            tree_node_str.replace("[", "(").replace("]", ")"),
            tree=tree_node,
            all_attrs=True,
            attr_bracket=["(", ")"],
        )

    @staticmethod
    def test_print_tree_attr_bracket_missing_error(tree_node):
        attr_bracket = [""]
        with pytest.raises(ValueError) as exc_info:
            print_tree(tree_node, all_attrs=True, attr_bracket=attr_bracket)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_EXPORT_PRINT_ATTR_BRACKET.format(
            attr_bracket=attr_bracket
        )

    # style
    @staticmethod
    def test_print_tree_style_ansi(tree_node):
        expected_str = """a\n|-- b\n|   |-- d\n|   `-- e\n|       |-- g\n|       `-- h\n`-- c\n    `-- f\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_node, style="ansi")

    @staticmethod
    def test_print_tree_style_ascii(tree_node):
        expected_str = """a\n|-- b\n|   |-- d\n|   +-- e\n|       |-- g\n|       +-- h\n+-- c\n    +-- f\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_node, style="ascii")

    @staticmethod
    def test_print_tree_style_const(tree_node):
        expected_str = """a\n├── b\n│   ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_node, style="const")

    @staticmethod
    def test_print_tree_style_const_bold(tree_node):
        expected_str = """a\n┣━━ b\n┃   ┣━━ d\n┃   ┗━━ e\n┃       ┣━━ g\n┃       ┗━━ h\n┗━━ c\n    ┗━━ f\n"""
        assert_print_statement(
            print_tree, expected_str, tree=tree_node, style="const_bold"
        )

    @staticmethod
    def test_print_tree_style_rounded(tree_node):
        expected_str = """a\n├── b\n│   ├── d\n│   ╰── e\n│       ├── g\n│       ╰── h\n╰── c\n    ╰── f\n"""
        assert_print_statement(
            print_tree, expected_str, tree=tree_node, style="rounded"
        )

    @staticmethod
    def test_print_tree_style_double(tree_node):
        expected_str = """a\n╠══ b\n║   ╠══ d\n║   ╚══ e\n║       ╠══ g\n║       ╚══ h\n╚══ c\n    ╚══ f\n"""
        assert_print_statement(print_tree, expected_str, tree=tree_node, style="double")

    @staticmethod
    def test_print_tree_style_unknown_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            print_tree(tree_node, style="something")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_EXPORT_PRINT_INVALID_STYLE
        )

    # custom_style
    @staticmethod
    def test_print_tree_custom_style(tree_node):
        expected_str = """a\nb\nd\ne\ng\nh\nc\nf\n"""
        assert_print_statement(
            print_tree,
            expected_str,
            tree=tree_node,
            style="custom",
            custom_style=["", "", ""],
        )

    @staticmethod
    def test_print_tree_custom_style_unequal_char_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            print_tree(
                tree_node,
                style="custom",
                custom_style=["", " ", ""],
            )
        assert (
            str(exc_info.value)
            == Constants.ERROR_NODE_EXPORT_PRINT_CUSTOM_STYLE_DIFFERENT_LENGTH
        )

    @staticmethod
    def test_print_tree_custom_style_missing_style_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            print_tree(
                tree_node,
                style="custom",
                custom_style=["", ""],
            )
        assert str(exc_info.value) == Constants.ERROR_NODE_EXPORT_PRINT_STYLE_SELECT


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
        pd.testing.assert_frame_equal(expected, actual, check_column_type=False)

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
        assert_tree_structure_basenode_root(tree)
        assert_tree_structure_basenode_root_attr(tree)
        assert_tree_structure_node_root(tree)


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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_max_depth(tree_node):
        expected = {
            "/a": {"name": "a"},
            "/a/b": {"name": "b"},
            "/a/c": {"name": "c"},
        }
        actual = tree_to_dict(tree_node, max_depth=2)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_leaf_only(tree_node):
        expected = {
            "/a/b/d": {"name": "d"},
            "/a/b/e/g": {"name": "g"},
            "/a/b/e/h": {"name": "h"},
            "/a/c/f": {"name": "f"},
        }
        actual = tree_to_dict(tree_node, leaf_only=True)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_to_tree(tree_node):
        d = tree_to_dict(tree_node, all_attrs=True)
        tree = dict_to_tree(d)
        assert_tree_structure_basenode_root(tree)
        assert_tree_structure_basenode_root_attr(tree)
        assert_tree_structure_node_root(tree)


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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_max_depth(tree_node):
        expected = {"name": "a", "children": [{"name": "b"}, {"name": "c"}]}
        actual = tree_to_nested_dict(tree_node, max_depth=2)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

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
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_to_tree(tree_node):
        d = tree_to_nested_dict(tree_node, all_attrs=True)
        tree = nested_dict_to_tree(d)
        assert_tree_structure_basenode_root(tree)
        assert_tree_structure_basenode_root_attr(tree)
        assert_tree_structure_node_root(tree)


class TestTreeToDot:
    @staticmethod
    def test_tree_to_dot(tree_node):
        graph = tree_to_dot(tree_node)
        expected = """strict digraph G {\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -> b0;\nd0 [label=d];\nb0 -> d0;\ne0 [label=e];\nb0 -> e0;\ng0 [label=g];\ne0 -> g0;\nh0 [label=h];\ne0 -> h0;\nc0 [label=c];\na0 -> c0;\nf0 [label=f];\nc0 -> f0;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_multiple(tree_node, tree_node_plot):
        graph = tree_to_dot([tree_node, tree_node_plot])
        expected = """strict digraph G {\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -> b0;\nd0 [label=d];\nb0 -> d0;\ne0 [label=e];\nb0 -> e0;\ng0 [label=g];\ne0 -> g0;\nh0 [label=h];\ne0 -> h0;\nc0 [label=c];\na0 -> c0;\nf0 [label=f];\nc0 -> f0;\nz0 [label=z];\ny0 [label=y];\nz0 -> y0;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_multiple.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_duplicate_names(tree_node_duplicate_names):
        graph = tree_to_dot(tree_node_duplicate_names)
        expected = """strict digraph G {\nrankdir=TB;\na0 [label=a];\na1 [label=a];\na0 -> a1;\na2 [label=a];\na1 -> a2;\nb0 [label=b];\na1 -> b0;\na3 [label=a];\nb0 -> a3;\nb1 [label=b];\nb0 -> b1;\nb2 [label=b];\na0 -> b2;\na4 [label=a];\nb2 -> a4;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_duplicate_names.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_type_error(dag_node):
        with pytest.raises(TypeError) as exc_info:
            tree_to_dot(dag_node)
        assert str(exc_info.value) == Constants.ERROR_NODE_TYPE.format(type="Node")

    @staticmethod
    def test_tree_to_dot_directed(tree_node):
        graph = tree_to_dot(tree_node, directed=False)
        expected = """strict graph G {\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -- b0;\nd0 [label=d];\nb0 -- d0;\ne0 [label=e];\nb0 -- e0;\ng0 [label=g];\ne0 -- g0;\nh0 [label=h];\ne0 -- h0;\nc0 [label=c];\na0 -- c0;\nf0 [label=f];\nc0 -- f0;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_undirected.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_bg_colour(tree_node):
        graph = tree_to_dot(tree_node, bg_colour="blue")
        expected = """strict digraph G {\nbgcolor=blue;\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -> b0;\nd0 [label=d];\nb0 -> d0;\ne0 [label=e];\nb0 -> e0;\ng0 [label=g];\ne0 -> g0;\nh0 [label=h];\ne0 -> h0;\nc0 [label=c];\na0 -> c0;\nf0 [label=f];\nc0 -> f0;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_bg_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_fill_colour(tree_node):
        graph = tree_to_dot(tree_node, node_colour="gold")
        expected = """strict digraph G {\nrankdir=TB;\na0 [fillcolor=gold, label=a, style=filled];\nb0 [fillcolor=gold, label=b, style=filled];\na0 -> b0;\nd0 [fillcolor=gold, label=d, style=filled];\nb0 -> d0;\ne0 [fillcolor=gold, label=e, style=filled];\nb0 -> e0;\ng0 [fillcolor=gold, label=g, style=filled];\ne0 -> g0;\nh0 [fillcolor=gold, label=h, style=filled];\ne0 -> h0;\nc0 [fillcolor=gold, label=c, style=filled];\na0 -> c0;\nf0 [fillcolor=gold, label=f, style=filled];\nc0 -> f0;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_fill_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_edge_colour(tree_node):
        graph = tree_to_dot(tree_node, edge_colour="red")
        expected = """strict digraph G {\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -> b0  [color=red];\nd0 [label=d];\nb0 -> d0  [color=red];\ne0 [label=e];\nb0 -> e0  [color=red];\ng0 [label=g];\ne0 -> g0  [color=red];\nh0 [label=h];\ne0 -> h0  [color=red];\nc0 [label=c];\na0 -> c0  [color=red];\nf0 [label=f];\nc0 -> f0  [color=red];\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_edge_colour.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_node_shape(tree_node):
        graph = tree_to_dot(tree_node, node_shape="triangle")
        expected = """strict digraph G {\nrankdir=TB;\na0 [label=a, shape=triangle];\nb0 [label=b, shape=triangle];\na0 -> b0;\nd0 [label=d, shape=triangle];\nb0 -> d0;\ne0 [label=e, shape=triangle];\nb0 -> e0;\ng0 [label=g, shape=triangle];\ne0 -> g0;\nh0 [label=h, shape=triangle];\ne0 -> h0;\nc0 [label=c, shape=triangle];\na0 -> c0;\nf0 [label=f, shape=triangle];\nc0 -> f0;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_node_shape.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_node_attr(tree_node_style):
        graph = tree_to_dot(tree_node_style, node_attr="node_style")
        expected = """strict digraph G {\nrankdir=TB;\na0 [fillcolor=gold, label=a, style=filled];\nb0 [fillcolor=blue, label=b, style=filled];\na0 -> b0;\nd0 [fillcolor=green, label=d, style=filled];\nb0 -> d0;\ng0 [fillcolor=red, label=g, style=filled];\nd0 -> g0;\ne0 [fillcolor=green, label=e, style=filled];\nb0 -> e0;\nh0 [fillcolor=red, label=h, style=filled];\ne0 -> h0;\nc0 [fillcolor=blue, label=c, style=filled];\na0 -> c0;\nf0 [fillcolor=green, label=f, style=filled];\nc0 -> f0;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_node_attr.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_edge_attr(tree_node_style):
        graph = tree_to_dot(tree_node_style, edge_attr="edge_style")
        expected = """strict digraph G {\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -> b0  [label=b, style=bold];\nd0 [label=d];\nb0 -> d0  [label=1, style=bold];\ng0 [label=g];\nd0 -> g0  [label=4, style=bold];\ne0 [label=e];\nb0 -> e0  [label=2, style=bold];\nh0 [label=h];\ne0 -> h0  [label=5, style=bold];\nc0 [label=c];\na0 -> c0  [label=c, style=bold];\nf0 [label=f];\nc0 -> f0  [label=3, style=bold];\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_edge_attr.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"

    @staticmethod
    def test_tree_to_dot_attr_override(tree_node):
        tree_node.children[0].set_attrs(
            {
                "node_style": {"style": "filled", "fillcolor": "blue"},
                "edge_style": {"style": "bold"},
            }
        )
        graph = tree_to_dot(tree_node, node_attr="node_style", edge_attr="edge_style")
        expected = """strict digraph G {\nrankdir=TB;\na0 [label=a];\nb0 [fillcolor=blue, label=b, style=filled];\na0 -> b0  [style=bold];\nd0 [label=d];\nb0 -> d0;\ne0 [label=e];\nb0 -> e0;\ng0 [label=g];\ne0 -> g0;\nh0 [label=h];\ne0 -> h0;\nc0 [label=c];\na0 -> c0;\nf0 [label=f];\nc0 -> f0;\n}\n"""
        actual = graph.to_string()
        if LOCAL:
            graph.write_png("tests/tree_attr_override.png")
        for expected_str in expected.split():
            assert (
                expected_str in actual
            ), f"Expected {expected_str} not in actual string"


class TestTreeToPillow:
    @staticmethod
    def test_tree_to_pillow(tree_node):
        pillow_image = tree_to_pillow(tree_node)
        if LOCAL:
            pillow_image.save("tests/tree_pillow.png")

    @staticmethod
    def test_tree_to_pillow_start_pos(tree_node):
        pillow_image = tree_to_pillow(tree_node, start_pos=(100, 50))
        if LOCAL:
            pillow_image.save("tests/tree_pillow_start_pos.png")

    @staticmethod
    def test_tree_to_pillow_start_pos_small(tree_node):
        pillow_image = tree_to_pillow(tree_node, start_pos=(0, 0))
        if LOCAL:
            pillow_image.save("tests/tree_pillow_start_pos_small.png")

    @staticmethod
    def test_tree_to_pillow_font(tree_node):
        pillow_image = tree_to_pillow(
            tree_node, font_size=20, font_colour="red", bg_colour="lightblue"
        )
        if LOCAL:
            pillow_image.save("tests/tree_pillow_font.png")

    @staticmethod
    def test_tree_to_pillow_kwargs(tree_node):
        pillow_image = tree_to_pillow(tree_node, max_depth=2, style="const_bold")
        if LOCAL:
            pillow_image.save("tests/tree_pillow_style.png")

    @staticmethod
    def test_tree_to_pillow_font_family(tree_node):
        font_family = "invalid.ttf"
        with pytest.raises(ValueError) as exc_info:
            tree_to_pillow(tree_node, font_family=font_family)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_EXPORT_PILLOW_FONT_FAMILY.format(
            font_family=font_family
        )


class TestTreeToMermaid:
    @staticmethod
    def test_tree_to_mermaid(tree_node):
        mermaid_md = tree_to_mermaid(tree_node)
        expected_str = """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```"""
        assert mermaid_md == expected_str

    @staticmethod
    def test_tree_to_mermaid_invalid_rankdir_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            tree_to_mermaid(tree_node, rankdir="invalid")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_MERMAID_INVALID_ARGUMENT.format(parameter="rankdir")
        )

    @staticmethod
    def test_tree_to_mermaid_invalid_node_shape_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            tree_to_mermaid(tree_node, node_shape="invalid")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_MERMAID_INVALID_ARGUMENT.format(parameter="node_shape")
        )

    @staticmethod
    def test_tree_to_mermaid_invalid_line_shape_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            tree_to_mermaid(tree_node, line_shape="invalid")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_MERMAID_INVALID_ARGUMENT.format(parameter="line_shape")
        )

    @staticmethod
    def test_tree_to_mermaid_invalid_edge_arrow_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            tree_to_mermaid(tree_node, edge_arrow="invalid")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_MERMAID_INVALID_ARGUMENT.format(parameter="edge_arrow")
        )

    @staticmethod
    def test_tree_to_mermaid_invalid_style_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            tree_to_mermaid(tree_node, node_border_width=0)
        assert str(exc_info.value) == Constants.ERROR_NODE_MERMAID_INVALID_STYLE

    @staticmethod
    def test_tree_to_mermaid_rankdir(tree_node):
        rankdirs = ["TB", "BT", "LR", "RL"]
        mermaid_mds = [
            tree_to_mermaid(tree_node, rankdir=rankdir) for rankdir in rankdirs
        ]
        expected_strs = [
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart BT\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart LR\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart RL\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
        ]
        for rankdir, mermaid_md, expected_str in zip(
            rankdirs, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check rankdir {rankdir}"

    @staticmethod
    def test_tree_to_mermaid_line_shape(tree_node):
        line_shapes = [
            "basis",
            "bumpX",
            "bumpY",
            "cardinal",
            "catmullRom",
            "linear",
            "monotoneX",
            "monotoneY",
            "natural",
            "step",
            "stepAfter",
            "stepBefore",
        ]
        mermaid_mds = [
            tree_to_mermaid(tree_node, line_shape=line_shape)
            for line_shape in line_shapes
        ]
        expected_strs = [
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'bumpX\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'bumpY\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'cardinal\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'catmullRom\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'linear\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'monotoneX\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'monotoneY\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'natural\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'step\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'stepAfter\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'stepBefore\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
        ]
        for line_shape, mermaid_md, expected_str in zip(
            line_shapes, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check line_shape {line_shape}"

    @staticmethod
    def test_tree_to_mermaid_node_colour(tree_node):
        node_colours = ["yellow", "blue", "#000", "#ff0000"]
        mermaid_mds = [
            tree_to_mermaid(tree_node, node_colour=node_colour)
            for node_colour in node_colours
        ]
        expected_strs = [
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default fill:yellow,stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default fill:blue,stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default fill:#000,stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default fill:#ff0000,stroke-width:1\n```""",
        ]
        for node_colour, mermaid_md, expected_str in zip(
            node_colours, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check node_colour {node_colour}"

    @staticmethod
    def test_tree_to_mermaid_node_border_colour(tree_node):
        node_border_colours = ["yellow", "blue", "#000", "#ff0000"]
        mermaid_mds = [
            tree_to_mermaid(tree_node, node_border_colour=node_border_colour)
            for node_border_colour in node_border_colours
        ]
        expected_strs = [
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke:yellow,stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke:blue,stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke:#000,stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke:#ff0000,stroke-width:1\n```""",
        ]
        for node_border_colour, mermaid_md, expected_str in zip(
            node_border_colours, mermaid_mds, expected_strs
        ):
            assert (
                mermaid_md == expected_str
            ), f"Check node_border_colour {node_border_colour}"

    @staticmethod
    def test_tree_to_mermaid_node_border_width(tree_node):
        node_border_widths = [1, 1.5, 2, 10.5]
        mermaid_mds = [
            tree_to_mermaid(tree_node, node_border_width=node_border_width)
            for node_border_width in node_border_widths
        ]
        expected_strs = [
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1.5\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:2\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:10.5\n```""",
        ]
        for node_border_width, mermaid_md, expected_str in zip(
            node_border_widths, mermaid_mds, expected_strs
        ):
            assert (
                mermaid_md == expected_str
            ), f"Check node_border_width {node_border_width}"

    @staticmethod
    def test_tree_to_mermaid_node_colour_border_colour_border_width(tree_node):
        node_styles = [("yellow", "#ff0", 0), ("#ff0000", "#000", 2)]
        mermaid_mds = [
            tree_to_mermaid(
                tree_node,
                node_colour=node_colour,
                node_border_colour=node_border_colour,
                node_border_width=node_border_width,
            )
            for node_colour, node_border_colour, node_border_width in node_styles
        ]
        expected_strs = [
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default fill:yellow,stroke:#ff0\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default fill:#ff0000,stroke:#000,stroke-width:2\n```""",
        ]
        for node_style, mermaid_md, expected_str in zip(
            node_styles, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check node_style {node_style}"

    @staticmethod
    def test_tree_to_mermaid_node_shape(tree_node):
        node_shapes = [
            "rounded_edge",
            "stadium",
            "subroutine",
            "cylindrical",
            "circle",
            "asymmetric",
            "rhombus",
            "hexagon",
            "parallelogram",
            "parallelogram_alt",
            "trapezoid",
            "trapezoid_alt",
            "double_circle",
        ]
        mermaid_mds = [
            tree_to_mermaid(tree_node, node_shape=node_shape)
            for node_shape in node_shapes
        ]
        expected_strs = [
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0(["a"]) --> 00(["b"])\n00 --> 000(["d"])\n00 --> 001(["e"])\n001 --> 0010(["g"])\n001 --> 0011(["h"])\n0(["a"]) --> 01(["c"])\n01 --> 010(["f"])\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[["a"]] --> 00[["b"]]\n00 --> 000[["d"]]\n00 --> 001[["e"]]\n001 --> 0010[["g"]]\n001 --> 0011[["h"]]\n0[["a"]] --> 01[["c"]]\n01 --> 010[["f"]]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[("a")] --> 00[("b")]\n00 --> 000[("d")]\n00 --> 001[("e")]\n001 --> 0010[("g")]\n001 --> 0011[("h")]\n0[("a")] --> 01[("c")]\n01 --> 010[("f")]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0(("a")) --> 00(("b"))\n00 --> 000(("d"))\n00 --> 001(("e"))\n001 --> 0010(("g"))\n001 --> 0011(("h"))\n0(("a")) --> 01(("c"))\n01 --> 010(("f"))\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0>"a"] --> 00>"b"]\n00 --> 000>"d"]\n00 --> 001>"e"]\n001 --> 0010>"g"]\n001 --> 0011>"h"]\n0>"a"] --> 01>"c"]\n01 --> 010>"f"]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0{"a"} --> 00{"b"}\n00 --> 000{"d"}\n00 --> 001{"e"}\n001 --> 0010{"g"}\n001 --> 0011{"h"}\n0{"a"} --> 01{"c"}\n01 --> 010{"f"}\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0{{"a"}} --> 00{{"b"}}\n00 --> 000{{"d"}}\n00 --> 001{{"e"}}\n001 --> 0010{{"g"}}\n001 --> 0011{{"h"}}\n0{{"a"}} --> 01{{"c"}}\n01 --> 010{{"f"}}\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[/"a"/] --> 00[/"b"/]\n00 --> 000[/"d"/]\n00 --> 001[/"e"/]\n001 --> 0010[/"g"/]\n001 --> 0011[/"h"/]\n0[/"a"/] --> 01[/"c"/]\n01 --> 010[/"f"/]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[\\"a"\\] --> 00[\\"b"\\]\n00 --> 000[\\"d"\\]\n00 --> 001[\\"e"\\]\n001 --> 0010[\\"g"\\]\n001 --> 0011[\\"h"\\]\n0[\\"a"\\] --> 01[\\"c"\\]\n01 --> 010[\\"f"\\]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[/"a"\\] --> 00[/"b"\\]\n00 --> 000[/"d"\\]\n00 --> 001[/"e"\\]\n001 --> 0010[/"g"\\]\n001 --> 0011[/"h"\\]\n0[/"a"\\] --> 01[/"c"\\]\n01 --> 010[/"f"\\]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0[\\"a"/] --> 00[\\"b"/]\n00 --> 000[\\"d"/]\n00 --> 001[\\"e"/]\n001 --> 0010[\\"g"/]\n001 --> 0011[\\"h"/]\n0[\\"a"/] --> 01[\\"c"/]\n01 --> 010[\\"f"/]\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0((("a"))) --> 00((("b")))\n00 --> 000((("d")))\n00 --> 001((("e")))\n001 --> 0010((("g")))\n001 --> 0011((("h")))\n0((("a"))) --> 01((("c")))\n01 --> 010((("f")))\nclassDef default stroke-width:1\n```""",
        ]
        for node_shape, mermaid_md, expected_str in zip(
            node_shapes, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check node_shape {node_shape}"

    @staticmethod
    def test_tree_to_mermaid_edge_arrow(tree_node):
        edge_arrows = [
            "normal",
            "bold",
            "dotted",
            "open",
            "bold_open",
            "dotted_open",
            "invisible",
            "circle",
            "cross",
            "double_normal",
            "double_circle",
            "double_cross",
        ]
        mermaid_mds = [
            tree_to_mermaid(tree_node, edge_arrow=edge_arrow)
            for edge_arrow in edge_arrows
        ]
        expected_strs = [
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n00 --> 001("e")\n001 --> 0010("g")\n001 --> 0011("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") ==> 00("b")\n00 ==> 000("d")\n00 ==> 001("e")\n001 ==> 0010("g")\n001 ==> 0011("h")\n0("a") ==> 01("c")\n01 ==> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") -.-> 00("b")\n00 -.-> 000("d")\n00 -.-> 001("e")\n001 -.-> 0010("g")\n001 -.-> 0011("h")\n0("a") -.-> 01("c")\n01 -.-> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --- 00("b")\n00 --- 000("d")\n00 --- 001("e")\n001 --- 0010("g")\n001 --- 0011("h")\n0("a") --- 01("c")\n01 --- 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") === 00("b")\n00 === 000("d")\n00 === 001("e")\n001 === 0010("g")\n001 === 0011("h")\n0("a") === 01("c")\n01 === 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") -.- 00("b")\n00 -.- 000("d")\n00 -.- 001("e")\n001 -.- 0010("g")\n001 -.- 0011("h")\n0("a") -.- 01("c")\n01 -.- 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") ~~~ 00("b")\n00 ~~~ 000("d")\n00 ~~~ 001("e")\n001 ~~~ 0010("g")\n001 ~~~ 0011("h")\n0("a") ~~~ 01("c")\n01 ~~~ 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --o 00("b")\n00 --o 000("d")\n00 --o 001("e")\n001 --o 0010("g")\n001 --o 0011("h")\n0("a") --o 01("c")\n01 --o 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --x 00("b")\n00 --x 000("d")\n00 --x 001("e")\n001 --x 0010("g")\n001 --x 0011("h")\n0("a") --x 01("c")\n01 --x 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") <--> 00("b")\n00 <--> 000("d")\n00 <--> 001("e")\n001 <--> 0010("g")\n001 <--> 0011("h")\n0("a") <--> 01("c")\n01 <--> 010("f")\nclassDef default stroke-width:1\n```""",
            """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") o--o 00("b")\n00 o--o 000("d")\n00 o--o 001("e")\n001 o--o 0010("g")\n001 o--o 0011("h")\n0("a") o--o 01("c")\n01 o--o 010("f")\nclassDef default stroke-width:1\n```""",
        ]
        for edge_arrow, mermaid_md, expected_str in zip(
            edge_arrows, mermaid_mds, expected_strs
        ):
            assert mermaid_md == expected_str, f"Check edge_arrow {edge_arrow}"

    @staticmethod
    def test_tree_to_mermaid_node_shape_attr(tree_node_mermaid_style):
        mermaid_md = tree_to_mermaid(
            tree_node_mermaid_style, node_shape_attr="node_shape"
        )
        expected_str = """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0{"a"} --> 00(["b"])\n00 --> 000("d")\n000 --> 0000("g")\n00 --> 001("e")\n001 --> 0010("h")\n0{"a"} --> 01(["c"])\n01 --> 010("f")\nclassDef default stroke-width:1\n```"""
        assert mermaid_md == expected_str

    @staticmethod
    def test_tree_to_mermaid_edge_label(tree_node_mermaid_style):
        mermaid_md = tree_to_mermaid(tree_node_mermaid_style, edge_label="label")
        expected_str = """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 -->|c-d link| 000("d")\n000 --> 0000("g")\n00 -->|c-e link| 001("e")\n001 --> 0010("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\n```"""
        assert mermaid_md == expected_str

    @staticmethod
    def test_tree_to_mermaid_node_attr(tree_node_mermaid_style):
        mermaid_md = tree_to_mermaid(tree_node_mermaid_style, node_attr="attr")
        expected_str = """```mermaid\n%%{ init: { \'flowchart\': { \'curve\': \'basis\' } } }%%\nflowchart TB\n0("a") --> 00("b")\n00 --> 000("d")\n000:::class0000 --> 0000("g")\n00 --> 001("e")\n001:::class0010 --> 0010("h")\n0("a") --> 01("c")\n01 --> 010("f")\nclassDef default stroke-width:1\nclassDef class0000 fill:red,stroke:black,stroke-width:2\nclassDef class0010 fill:red,stroke:black,stroke-width:2\n```"""
        assert mermaid_md == expected_str

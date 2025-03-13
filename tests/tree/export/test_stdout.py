import io

import pytest

from bigtree.tree import export
from tests.conftest import assert_print_statement
from tests.test_constants import Constants

tree_node_str = (
    "a [age=90]\n"
    "├── b [age=65]\n"
    "│   ├── d [age=40]\n"
    "│   └── e [age=35]\n"
    "│       ├── g [age=10]\n"
    "│       └── h [age=6]\n"
    "└── c [age=60]\n"
    "    └── f [age=38]\n"
)
tree_node_no_attr_str = (
    "a\n"
    "├── b\n"
    "│   ├── d\n"
    "│   └── e\n"
    "│       ├── g\n"
    "│       └── h\n"
    "└── c\n"
    "    └── f\n"
)
tree_node_hstr = (
    "           ┌─ d\n"
    "     ┌─ b ─┤     ┌─ g\n"
    "─ a ─┤     └─ e ─┤\n"
    "     │           └─ h\n"
    "     └─ c ─── f\n"
)
tree_node_vstr = (
    "             ┌───┐        \n"
    "             │ a │        \n"
    "             └─┬─┘        \n"
    "       ┌───────┴───────┐  \n"
    "     ┌─┴─┐           ┌─┴─┐\n"
    "     │ b │           │ c │\n"
    "     └─┬─┘           └─┬─┘\n"
    "  ┌────┴────┐          │  \n"
    "┌─┴─┐     ┌─┴─┐      ┌─┴─┐\n"
    "│ d │     │ e │      │ f │\n"
    "└───┘     └─┬─┘      └───┘\n"
    "         ┌──┴───┐         \n"
    "       ┌─┴─┐  ┌─┴─┐       \n"
    "       │ g │  │ h │       \n"
    "       └───┘  └───┘       \n"
)
# fmt: off
tree_node_branch_hstr = (
    "     ┌─ d\n"
    "─ b ─┤     ┌─ g\n"
    "     └─ e ─┤\n"
    "           └─ h\n"
)
# fmt: on
tree_node_branch_vstr = (
    "     ┌───┐         \n"
    "     │ b │         \n"
    "     └─┬─┘         \n"
    "  ┌────┴────┐      \n"
    "┌─┴─┐     ┌─┴─┐    \n"
    "│ d │     │ e │    \n"
    "└───┘     └─┬─┘    \n"
    "         ┌──┴───┐  \n"
    "       ┌─┴─┐  ┌─┴─┐\n"
    "       │ g │  │ h │\n"
    "       └───┘  └───┘\n"
)


class TestPrintTree:
    @staticmethod
    def test_print_tree(tree_node):
        assert_print_statement(
            export.print_tree,
            tree_node_no_attr_str,
            tree=tree_node,
        )

    @staticmethod
    def test_print_tree_alias(tree_node):
        expected_str = (
            "alias a\n"
            "├── b\n"
            "│   ├── d\n"
            "│   └── e\n"
            "│       ├── g\n"
            "│       └── h\n"
            "└── c\n"
            "    └── f\n"
        )
        tree_node.set_attrs({"alias": "alias a"})
        assert_print_statement(
            export.print_tree,
            expected_str,
            tree=tree_node,
            alias="alias",
        )

    @staticmethod
    def test_print_tree_child_node_name(tree_node):
        # fmt: off
        expected_str = (
            "b\n"
            "├── d\n"
            "└── e\n"
            "    ├── g\n"
            "    └── h\n"
        )
        # fmt: on
        assert_print_statement(
            export.print_tree,
            expected_str,
            tree=tree_node,
            node_name_or_path="b",
        )

    @staticmethod
    def test_print_tree_child_node_name_error(tree_node):
        node_name_or_path = "z"
        with pytest.raises(ValueError) as exc_info:
            export.print_tree(tree_node, node_name_or_path=node_name_or_path)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_EXPORT_PRINT_INVALID_PATH.format(
            node_name_or_path=node_name_or_path
        )

    @staticmethod
    def test_print_tree_child_node_path(tree_node):
        # fmt: off
        expected_str = (
            "b\n"
            "├── d\n"
            "└── e\n"
            "    ├── g\n"
            "    └── h\n"
        )
        # fmt: on
        assert_print_statement(
            export.print_tree,
            expected_str,
            tree=tree_node,
            node_name_or_path="a/b",
        )

    # all_attr
    @staticmethod
    def test_print_tree_all_attr(tree_node):
        assert_print_statement(
            export.print_tree, tree_node_str, tree=tree_node, all_attrs=True
        )

    @staticmethod
    def test_print_tree_all_attr_empty(tree_node_no_attr):
        assert_print_statement(
            export.print_tree,
            tree_node_no_attr_str,
            tree=tree_node_no_attr,
            all_attrs=True,
        )

    # attr_list
    @staticmethod
    def test_print_tree_attr_list(tree_node):
        assert_print_statement(
            export.print_tree, tree_node_str, tree=tree_node, attr_list=["age"]
        )

    @staticmethod
    def test_print_tree_invalid_attr(tree_node):
        assert_print_statement(
            export.print_tree,
            tree_node_no_attr_str,
            tree=tree_node,
            attr_list=["random"],
        )

    # attr_list, attr_omit_null
    @staticmethod
    def test_print_tree_attr_omit_null_false(tree_node_negative_null_attr):
        expected_str = (
            "a\n"
            "├── b [age=-1]\n"
            "│   ├── d [age=1]\n"
            "│   └── e [age=None]\n"
            "│       ├── g [age=10]\n"
            "│       └── h\n"
            "└── c [age=0]\n"
            "    └── f [age=nan]\n"
        )
        assert_print_statement(
            export.print_tree,
            expected_str,
            tree=tree_node_negative_null_attr,
            attr_list=["age"],
            attr_omit_null=False,
        )

    @staticmethod
    def test_print_tree_attr_omit_null_true(tree_node_negative_null_attr):
        expected_str = (
            "a\n"
            "├── b [age=-1]\n"
            "│   ├── d [age=1]\n"
            "│   └── e\n"
            "│       ├── g [age=10]\n"
            "│       └── h\n"
            "└── c [age=0]\n"
            "    └── f\n"
        )
        assert_print_statement(
            export.print_tree,
            expected_str,
            tree=tree_node_negative_null_attr,
            attr_list=["age"],
            attr_omit_null=True,
        )

    # attr_bracket
    @staticmethod
    def test_print_tree_attr_bracket(tree_node):
        assert_print_statement(
            export.print_tree,
            tree_node_str.replace("[", "(").replace("]", ")"),
            tree=tree_node,
            all_attrs=True,
            attr_bracket=["(", ")"],
        )

    @staticmethod
    def test_print_tree_attr_bracket_missing_error(tree_node):
        attr_bracket = [""]
        with pytest.raises(ValueError) as exc_info:
            export.print_tree(tree_node, all_attrs=True, attr_bracket=attr_bracket)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_EXPORT_PRINT_ATTR_BRACKET.format(
            attr_bracket=attr_bracket
        )

    # style
    @staticmethod
    def test_print_tree_style_ansi(tree_node):
        expected_str = (
            "a\n"
            "|-- b\n"
            "|   |-- d\n"
            "|   `-- e\n"
            "|       |-- g\n"
            "|       `-- h\n"
            "`-- c\n"
            "    `-- f\n"
        )
        assert_print_statement(
            export.print_tree, expected_str, tree=tree_node, style="ansi"
        )

    @staticmethod
    def test_print_tree_style_ascii(tree_node):
        expected_str = (
            "a\n"
            "|-- b\n"
            "|   |-- d\n"
            "|   +-- e\n"
            "|       |-- g\n"
            "|       +-- h\n"
            "+-- c\n"
            "    +-- f\n"
        )
        assert_print_statement(
            export.print_tree, expected_str, tree=tree_node, style="ascii"
        )

    @staticmethod
    def test_print_tree_style_const(tree_node):
        expected_str = (
            "a\n"
            "├── b\n"
            "│   ├── d\n"
            "│   └── e\n"
            "│       ├── g\n"
            "│       └── h\n"
            "└── c\n"
            "    └── f\n"
        )
        assert_print_statement(
            export.print_tree, expected_str, tree=tree_node, style="const"
        )

    @staticmethod
    def test_print_tree_style_const_bold(tree_node):
        expected_str = (
            "a\n"
            "┣━━ b\n"
            "┃   ┣━━ d\n"
            "┃   ┗━━ e\n"
            "┃       ┣━━ g\n"
            "┃       ┗━━ h\n"
            "┗━━ c\n"
            "    ┗━━ f\n"
        )
        assert_print_statement(
            export.print_tree, expected_str, tree=tree_node, style="const_bold"
        )

    @staticmethod
    def test_print_tree_style_rounded(tree_node):
        expected_str = (
            "a\n"
            "├── b\n"
            "│   ├── d\n"
            "│   ╰── e\n"
            "│       ├── g\n"
            "│       ╰── h\n"
            "╰── c\n"
            "    ╰── f\n"
        )
        assert_print_statement(
            export.print_tree, expected_str, tree=tree_node, style="rounded"
        )

    @staticmethod
    def test_print_tree_style_double(tree_node):
        expected_str = (
            "a\n"
            "╠══ b\n"
            "║   ╠══ d\n"
            "║   ╚══ e\n"
            "║       ╠══ g\n"
            "║       ╚══ h\n"
            "╚══ c\n"
            "    ╚══ f\n"
        )
        assert_print_statement(
            export.print_tree, expected_str, tree=tree_node, style="double"
        )

    @staticmethod
    def test_print_tree_style_unknown_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.print_tree(tree_node, style="something")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_EXPORT_PRINT_INVALID_STYLE
        )

    # custom_style - BasePrintStyle
    @staticmethod
    def test_print_tree_style_ansi_class(tree_node):
        from bigtree.utils.constants import ANSIPrintStyle

        expected_str = (
            "a\n"
            "|-- b\n"
            "|   |-- d\n"
            "|   `-- e\n"
            "|       |-- g\n"
            "|       `-- h\n"
            "`-- c\n"
            "    `-- f\n"
        )
        assert_print_statement(
            export.print_tree,
            expected_str,
            tree=tree_node,
            style=ANSIPrintStyle,
        )

    @staticmethod
    def test_print_tree_style_ascii_class(tree_node):
        from bigtree.utils.constants import ASCIIPrintStyle

        expected_str = (
            "a\n"
            "|-- b\n"
            "|   |-- d\n"
            "|   +-- e\n"
            "|       |-- g\n"
            "|       +-- h\n"
            "+-- c\n"
            "    +-- f\n"
        )
        assert_print_statement(
            export.print_tree,
            expected_str,
            tree=tree_node,
            style=ASCIIPrintStyle,
        )

    @staticmethod
    def test_print_tree_style_custom_class(tree_node):
        from bigtree.utils.constants import BasePrintStyle

        expected_str = "a\nb\nd\ne\ng\nh\nc\nf\n"
        assert_print_statement(
            export.print_tree,
            expected_str,
            tree=tree_node,
            style=BasePrintStyle("", "", ""),
        )

    @staticmethod
    def test_print_tree_style_class_error(tree_node):
        from bigtree.utils.constants import BasePrintStyle

        with pytest.raises(ValueError) as exc_info:
            export.print_tree(
                tree_node,
                style=BasePrintStyle("", "", " "),
            )
        assert (
            str(exc_info.value)
            == Constants.ERROR_NODE_EXPORT_PRINT_CUSTOM_STYLE_DIFFERENT_LENGTH
        )

    # custom_style
    @staticmethod
    def test_print_tree_custom_style(tree_node):
        expected_str = "a\nb\nd\ne\ng\nh\nc\nf\n"
        assert_print_statement(
            export.print_tree,
            expected_str,
            tree=tree_node,
            style=["", "", ""],
        )

    @staticmethod
    def test_print_tree_custom_style_unequal_char_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.print_tree(
                tree_node,
                style=["", " ", ""],
            )
        assert (
            str(exc_info.value)
            == Constants.ERROR_NODE_EXPORT_PRINT_CUSTOM_STYLE_DIFFERENT_LENGTH
        )

    @staticmethod
    def test_print_tree_custom_style_missing_style_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.print_tree(
                tree_node,
                style=["", ""],
            )
        assert str(exc_info.value) == Constants.ERROR_NODE_EXPORT_PRINT_STYLE_SELECT

    @staticmethod
    def test_print_tree_kwargs(tree_node):
        output = io.StringIO()
        export.print_tree(tree_node, file=output)
        assert output.getvalue() == tree_node_no_attr_str


class TestHPrintTree:
    @staticmethod
    def test_hprint_tree(tree_node):
        assert_print_statement(
            export.hprint_tree,
            tree_node_hstr,
            tree=tree_node,
        )

    @staticmethod
    def test_hprint_tree2():
        from bigtree.tree.construct import list_to_tree

        tree_node = list_to_tree(
            [
                "a/b/b1",
                "a/b/b2",
                "a/b/b3",
                "a/b/b4",
                "a/b/b5",
                "a/c/c1/c11",
                "a/c/c1/c12",
                "a/d/d1",
                "a/d/d2",
                "a/d/d3",
                "a/d/d4",
                "a/d/d5/d51",
                "a/d/d5/d52",
                "a/d/d5/d53",
                "a/d/d5/d54",
                "a/d/d6",
                "a/e/e1/e11",
                "a/e/e1/e12",
                "a/e/e1/e13",
                "a/e/e1/e14",
                "a/e/e1/e15",
                "a/e/e1/e16",
                "a/e/e2",
                "a/e/e3/e311",
                "a/e/e3/e312",
                "a/e/e3/e313",
            ]
        )
        expected_str = (
            "           ┌─ b1\n"
            "           ├─ b2\n"
            "     ┌─ b ─┼─ b3\n"
            "     │     ├─ b4\n"
            "     │     └─ b5\n"
            "     │            ┌─ c11\n"
            "     ├─ c ─── c1 ─┤\n"
            "     │            └─ c12\n"
            "     │     ┌─ d1\n"
            "     │     ├─ d2\n"
            "     │     ├─ d3\n"
            "     │     ├─ d4\n"
            "─ a ─┼─ d ─┤      ┌─ d51\n"
            "     │     ├─ d5 ─┼─ d52\n"
            "     │     │      ├─ d53\n"
            "     │     │      └─ d54\n"
            "     │     └─ d6\n"
            "     │            ┌─ e11\n"
            "     │            ├─ e12\n"
            "     │     ┌─ e1 ─┼─ e13\n"
            "     │     │      ├─ e14\n"
            "     │     │      ├─ e15\n"
            "     └─ e ─┤      └─ e16\n"
            "           ├─ e2\n"
            "           │      ┌─ e311\n"
            "           └─ e3 ─┼─ e312\n"
            "                  └─ e313\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
        )

    @staticmethod
    def test_hprint_tree_multiline(tree_node):
        tree_node.name = "a\na2"
        tree_node["b"]["e"].name = "e\ne2\nmultiln"
        expected_str = (
            "            ┌─    d\n"
            "      ┌─ b ─┤     e     ┌─ g\n"
            "─ a  ─┤     └─    e2   ─┤\n"
            "  a2  │        multiln  └─ h\n"
            "      └─ c ───    f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
        )

    @staticmethod
    def test_hprint_tree_multiline_parent_longer(tree_node):
        tree_node.name = "a\na2"
        tree_node["c"].name = "c\nc2\nmultiln"
        expected_str = (
            "                  ┌─ d\n"
            "      ┌─    b    ─┤     ┌─ g\n"
            "      │           └─ e ─┤\n"
            "─ a  ─┤                 └─ h\n"
            "  a2  │     c\n"
            "      └─    c2   ─── f\n"
            "         multiln\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
        )

    @staticmethod
    def test_hprint_tree_multiline_parent_longer2(tree_node):
        tree_node.name = "a\na2"
        tree_node["b"]["e"].name = "e\ne2\nmultiln\nmultiln\nmultiln"
        expected_str = (
            "            ┌─    d\n"
            "      ┌─ b ─┤     e\n"
            "      │     │     e2    ┌─ g\n"
            "─ a  ─┤     └─ multiln ─┤\n"
            "  a2  │        multiln  └─ h\n"
            "      │        multiln\n"
            "      └─ c ───    f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
        )

    @staticmethod
    def test_hprint_tree_alias(tree_node):
        tree_node.alias_attr = "a\na2"
        tree_node["b"]["e"].alias_attr = "e\ne2\nalias_1"
        expected_str = (
            "            ┌─    d\n"
            "      ┌─ b ─┤     e     ┌─ g\n"
            "─ a  ─┤     └─    e2   ─┤\n"
            "  a2  │        alias_1  └─ h\n"
            "      └─ c ───    f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            alias="alias_attr",
        )

    @staticmethod
    def test_hprint_tree_spacing(tree_node):
        expected_str = (
            "                       ┌───── d\n"
            "         ┌───── b ─────┤             ┌───── g\n"
            "─ a ─────┤             └───── e ─────┤\n"
            "         │                           └───── h\n"
            "         └───── c ─────────── f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            spacing=4,
        )

    @staticmethod
    def test_hprint_tree_strip(tree_node):
        expected_str = (
            "           ┌─ d      \n"
            "     ┌─ b ─┤     ┌─ g\n"
            "─ a ─┤     └─ e ─┤   \n"
            "     │           └─ h\n"
            "     └─ c ─── f      \n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            strip=False,
        )

    @staticmethod
    def test_hprint_tree_long_root_name_length(tree_node):
        tree_node.name = "abcdefghijkl"
        expected_str = (
            "                      ┌─ d\n"
            "                ┌─ b ─┤     ┌─ g\n"
            "─ abcdefghijkl ─┤     └─ e ─┤\n"
            "                │           └─ h\n"
            "                └─ c ─── f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
        )

    @staticmethod
    def test_hprint_tree_diff_node_name_length(tree_node):
        tree_node["b"].name = "bcde"
        tree_node["c"]["f"].name = "fghijk"
        expected_str = (
            "              ┌─   d\n"
            "     ┌─ bcde ─┤          ┌─ g\n"
            "─ a ─┤        └─   e    ─┤\n"
            "     │                   └─ h\n"
            "     └─  c   ─── fghijk\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
        )

    @staticmethod
    def test_hprint_tree_child_node_name(tree_node):
        assert_print_statement(
            export.hprint_tree,
            tree_node_branch_hstr,
            tree=tree_node,
            node_name_or_path="b",
        )

    @staticmethod
    def test_hprint_tree_child_node_name_error(tree_node):
        node_name_or_path = "bb"
        with pytest.raises(ValueError) as exc_info:
            export.hprint_tree(tree_node, node_name_or_path=node_name_or_path)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_EXPORT_PRINT_INVALID_PATH.format(
            node_name_or_path=node_name_or_path
        )

    @staticmethod
    def test_hprint_tree_child_node_path(tree_node):
        assert_print_statement(
            export.hprint_tree,
            tree_node_branch_hstr,
            tree=tree_node,
            node_name_or_path="a/b",
        )

    @staticmethod
    def test_hprint_tree_intermediate_node_name(tree_node):
        expected_str = (
            "       ┌─ d\n"
            "   ┌───┤   ┌─ g\n"
            "───┤   └───┤\n"
            "   │       └─ h\n"
            "   └───── f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            intermediate_node_name=False,
        )

    @staticmethod
    def test_hprint_tree_intermediate_node_name_border(tree_node):
        expected_str = (
            "          ┌───┐\n"
            "         ┌┤ d │\n"
            "     ┌──┐│└───┘\n"
            "    ┌┤  ├┤     ┌───┐\n"
            "    │└──┘│┌──┐┌┤ g │\n"
            "┌──┐│    └┤  ├┤└───┘\n"
            "│  ├┤     └──┘│┌───┐\n"
            "└──┘│         └┤ h │\n"
            "    │          └───┘\n"
            "    │┌──┐ ┌───┐\n"
            "    └┤  ├─┤ f │\n"
            "     └──┘ └───┘\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            intermediate_node_name=False,
            border_style="const",
        )

    @staticmethod
    def test_hprint_tree_intermediate_node_name_diff_node_name_length(tree_node):
        tree_node["b"].name = "bcde"
        tree_node["c"]["f"].name = "fghijk"
        expected_str = (
            "       ┌─ d\n"
            "   ┌───┤   ┌─ g\n"
            "───┤   └───┤\n"
            "   │       └─ h\n"
            "   └───── fghijk\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            intermediate_node_name=False,
        )

    # style
    @staticmethod
    def test_hprint_tree_style_ansi(tree_node):
        expected_str = (
            "           /- d\n"
            "     /- b -+     /- g\n"
            "- a -+     \\- e -+\n"
            "     |           \\- h\n"
            "     \\- c --- f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="ansi",
        )

    @staticmethod
    def test_hprint_tree_style_ascii(tree_node):
        expected_str = (
            "           +- d\n"
            "     +- b -+     +- g\n"
            "- a -+     +- e -+\n"
            "     |           +- h\n"
            "     +- c --- f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="ascii",
        )

    @staticmethod
    def test_hprint_tree_style_const(tree_node):
        expected_str = (
            "           ┌─ d\n"
            "     ┌─ b ─┤     ┌─ g\n"
            "─ a ─┤     └─ e ─┤\n"
            "     │           └─ h\n"
            "     └─ c ─── f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="const",
        )

    @staticmethod
    def test_hprint_tree_style_const_bold(tree_node):
        expected_str = (
            "           ┏━ d\n"
            "     ┏━ b ━┫     ┏━ g\n"
            "━ a ━┫     ┗━ e ━┫\n"
            "     ┃           ┗━ h\n"
            "     ┗━ c ━━━ f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="const_bold",
        )

    @staticmethod
    def test_hprint_tree_style_rounded(tree_node):
        expected_str = (
            "           ╭─ d\n"
            "     ╭─ b ─┤     ╭─ g\n"
            "─ a ─┤     ╰─ e ─┤\n"
            "     │           ╰─ h\n"
            "     ╰─ c ─── f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="rounded",
        )

    @staticmethod
    def test_hprint_tree_style_double(tree_node):
        expected_str = (
            "           ╔═ d\n"
            "     ╔═ b ═╣     ╔═ g\n"
            "═ a ═╣     ╚═ e ═╣\n"
            "     ║           ╚═ h\n"
            "     ╚═ c ═══ f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="double",
        )

    @staticmethod
    def test_hprint_tree_style_unknown_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.hprint_tree(tree_node, style="something")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_EXPORT_PRINT_INVALID_STYLE
        )

    # custom_style - BaseHPrintStyle
    @staticmethod
    def test_hprint_tree_style_ansi_class(tree_node):
        from bigtree.utils.constants import ANSIHPrintStyle

        expected_str = (
            "           /- d\n"
            "     /- b -+     /- g\n"
            "- a -+     \\- e -+\n"
            "     |           \\- h\n"
            "     \\- c --- f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style=ANSIHPrintStyle,
        )

    @staticmethod
    def test_hprint_tree_style_ascii_class(tree_node):
        from bigtree.utils.constants import ASCIIHPrintStyle

        expected_str = (
            "           +- d\n"
            "     +- b -+     +- g\n"
            "- a -+     +- e -+\n"
            "     |           +- h\n"
            "     +- c --- f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style=ASCIIHPrintStyle,
        )

    @staticmethod
    def test_hprint_tree_style_custom_class(tree_node):
        from bigtree.utils.constants import BaseHPrintStyle

        expected_str = (
            "           -= d\n"
            "     -= b =+     -= g\n"
            "= a =+     |= e =+\n"
            "     -           |= h\n"
            "     |= c === f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style=BaseHPrintStyle("-", "-", "+", "+", "|", "-", "="),
        )

    @staticmethod
    def test_hprint_tree_style_class_unequal_char_error(tree_node):
        from bigtree.utils.constants import BaseHPrintStyle

        with pytest.raises(ValueError) as exc_info:
            export.hprint_tree(
                tree_node,
                style=BaseHPrintStyle("- ", "-", "+", "+", "|", "-", "="),
            )
        assert (
            str(exc_info.value)
            == Constants.ERROR_NODE_EXPORT_HPRINT_CUSTOM_STYLE_DIFFERENT_LENGTH
        )

    # custom_style
    @staticmethod
    def test_hprint_tree_custom_style(tree_node):
        expected_str = (
            "           -= d\n"
            "     -= b =+     -= g\n"
            "= a =+     |= e =+\n"
            "     -           |= h\n"
            "     |= c === f\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style=["-", "-", "+", "+", "|", "-", "="],
        )

    @staticmethod
    def test_hprint_tree_custom_style_unequal_char_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.hprint_tree(
                tree_node,
                style=["- ", "-", "+", "+", "|", "-", "="],
            )
        assert (
            str(exc_info.value)
            == Constants.ERROR_NODE_EXPORT_HPRINT_CUSTOM_STYLE_DIFFERENT_LENGTH
        )

    @staticmethod
    def test_hprint_tree_custom_style_missing_style_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.hprint_tree(tree_node, style=["-", "+", "+", "|", "-", "="])
        assert str(exc_info.value) == Constants.ERROR_NODE_EXPORT_HPRINT_STYLE_SELECT

    @staticmethod
    def test_hprint_tree_kwargs(tree_node):
        output = io.StringIO()
        export.hprint_tree(tree_node, file=output)
        assert output.getvalue() == tree_node_hstr

    # border_style
    @staticmethod
    def test_hprint_tree_border_style_ansi(tree_node):
        expected_str = (
            "                    `-------`\n"
            "                   /+   d   |\n"
            "          `-------`|`-------`\n"
            "         /+   b   ++          `-------`\n"
            "         |`-------`|`-------`/+   g   |\n"
            "`-------`|         \\+   e   ++`-------`\n"
            "|   a   ++          `-------`|`-------`\n"
            "`-------`|                   \\+   h   |\n"
            "         |                    `-------`\n"
            "         |`-------` `-------`\n"
            "         \\+   c   +-+   f   |\n"
            "          `-------` `-------`\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="ansi",
            border_style="ansi",
        )

    @staticmethod
    def test_hprint_tree_border_style_ascii(tree_node):
        expected_str = (
            "                    +-------+\n"
            "                   ++   d   |\n"
            "          +-------+|+-------+\n"
            "         ++   b   ++          +-------+\n"
            "         |+-------+|+-------+++   g   |\n"
            "+-------+|         ++   e   +++-------+\n"
            "|   a   ++          +-------+|+-------+\n"
            "+-------+|                   ++   h   |\n"
            "         |                    +-------+\n"
            "         |+-------+ +-------+\n"
            "         ++   c   +-+   f   |\n"
            "          +-------+ +-------+\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="ascii",
            border_style="ascii",
        )

    @staticmethod
    def test_hprint_tree_border_style_const(tree_node):
        expected_str = (
            "                    ┌───────┐\n"
            "                   ┌┤   d   │\n"
            "          ┌───────┐│└───────┘\n"
            "         ┌┤   b   ├┤          ┌───────┐\n"
            "         │└───────┘│┌───────┐┌┤   g   │\n"
            "┌───────┐│         └┤   e   ├┤└───────┘\n"
            "│   a   ├┤          └───────┘│┌───────┐\n"
            "└───────┘│                   └┤   h   │\n"
            "         │                    └───────┘\n"
            "         │┌───────┐ ┌───────┐\n"
            "         └┤   c   ├─┤   f   │\n"
            "          └───────┘ └───────┘\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="const",
            border_style="const",
        )

    @staticmethod
    def test_hprint_tree_border_style_const_bold(tree_node):
        expected_str = (
            "                    ┏━━━━━━━┓\n"
            "                   ┏┫   d   ┃\n"
            "          ┏━━━━━━━┓┃┗━━━━━━━┛\n"
            "         ┏┫   b   ┣┫          ┏━━━━━━━┓\n"
            "         ┃┗━━━━━━━┛┃┏━━━━━━━┓┏┫   g   ┃\n"
            "┏━━━━━━━┓┃         ┗┫   e   ┣┫┗━━━━━━━┛\n"
            "┃   a   ┣┫          ┗━━━━━━━┛┃┏━━━━━━━┓\n"
            "┗━━━━━━━┛┃                   ┗┫   h   ┃\n"
            "         ┃                    ┗━━━━━━━┛\n"
            "         ┃┏━━━━━━━┓ ┏━━━━━━━┓\n"
            "         ┗┫   c   ┣━┫   f   ┃\n"
            "          ┗━━━━━━━┛ ┗━━━━━━━┛\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="const_bold",
            border_style="const_bold",
        )

    @staticmethod
    def test_hprint_tree_border_style_rounded(tree_node):
        expected_str = (
            "                    ╭───────╮\n"
            "                   ╭┤   d   │\n"
            "          ╭───────╮│╰───────╯\n"
            "         ╭┤   b   ├┤          ╭───────╮\n"
            "         │╰───────╯│╭───────╮╭┤   g   │\n"
            "╭───────╮│         ╰┤   e   ├┤╰───────╯\n"
            "│   a   ├┤          ╰───────╯│╭───────╮\n"
            "╰───────╯│                   ╰┤   h   │\n"
            "         │                    ╰───────╯\n"
            "         │╭───────╮ ╭───────╮\n"
            "         ╰┤   c   ├─┤   f   │\n"
            "          ╰───────╯ ╰───────╯\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="rounded",
            border_style="rounded",
        )

    @staticmethod
    def test_hprint_tree_border_style_double(tree_node):
        expected_str = (
            "                    ╔═══════╗\n"
            "                   ╔╣   d   ║\n"
            "          ╔═══════╗║╚═══════╝\n"
            "         ╔╣   b   ╠╣          ╔═══════╗\n"
            "         ║╚═══════╝║╔═══════╗╔╣   g   ║\n"
            "╔═══════╗║         ╚╣   e   ╠╣╚═══════╝\n"
            "║   a   ╠╣          ╚═══════╝║╔═══════╗\n"
            "╚═══════╝║                   ╚╣   h   ║\n"
            "         ║                    ╚═══════╝\n"
            "         ║╔═══════╗ ╔═══════╗\n"
            "         ╚╣   c   ╠═╣   f   ║\n"
            "          ╚═══════╝ ╚═══════╝\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style="double",
            border_style="double",
        )

    @staticmethod
    def test_hprint_tree_border_style_unknown_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.hprint_tree(tree_node, border_style="something")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_EXPORT_PRINT_INVALID_STYLE
        )

    # custom border_style
    @staticmethod
    def test_hprint_tree_border_style_ansi_class(tree_node):
        from bigtree.utils.constants import ANSIBorderStyle, ANSIHPrintStyle

        expected_str = (
            "                    `-------`\n"
            "                   /+   d   |\n"
            "          `-------`|`-------`\n"
            "         /+   b   ++          `-------`\n"
            "         |`-------`|`-------`/+   g   |\n"
            "`-------`|         \\+   e   ++`-------`\n"
            "|   a   ++          `-------`|`-------`\n"
            "`-------`|                   \\+   h   |\n"
            "         |                    `-------`\n"
            "         |`-------` `-------`\n"
            "         \\+   c   +-+   f   |\n"
            "          `-------` `-------`\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            style=ANSIHPrintStyle,
            border_style=ANSIBorderStyle,
        )

    @staticmethod
    def test_hprint_tree_border_style_multiline(tree_node):
        tree_node.name = "a\na2"
        tree_node["b"]["e"].name = "e\ne2\nmultiln"
        expected_str = (
            "                     ┌─────────────┐\n"
            "                    ┌┤      d      │\n"
            "           ┌───────┐│└─────────────┘\n"
            "          ┌┤   b   ├┤┌─────────────┐ ┌───────┐\n"
            "          │└───────┘││      e      │┌┤   g   │\n"
            "┌────────┐│         └┤      e2     ├┤└───────┘\n"
            "│   a    ├┤          │   multiln   ││┌───────┐\n"
            "│   a2   ││          └─────────────┘└┤   h   │\n"
            "└────────┘│                          └───────┘\n"
            "          │┌───────┐ ┌─────────────┐\n"
            "          └┤   c   ├─┤      f      │\n"
            "           └───────┘ └─────────────┘\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            border_style="const",
        )

    @staticmethod
    def test_hprint_tree_border_style_multiline_parent_longer(tree_node):
        tree_node.name = "a\na2"
        tree_node["b"]["e"].name = "e\ne2\nmultiln\nmultiln\nmultiln"
        expected_str = (
            "                     ┌─────────────┐\n"
            "                    ┌┤      d      │\n"
            "           ┌───────┐│└─────────────┘\n"
            "          ┌┤   b   ├┤┌─────────────┐\n"
            "          │└───────┘││      e      │ ┌───────┐\n"
            "          │         ││      e2     │┌┤   g   │\n"
            "┌────────┐│         └┤   multiln   ├┤└───────┘\n"
            "│   a    ├┤          │   multiln   ││┌───────┐\n"
            "│   a2   ││          │   multiln   │└┤   h   │\n"
            "└────────┘│          └─────────────┘ └───────┘\n"
            "          │┌───────┐ ┌─────────────┐\n"
            "          └┤   c   ├─┤      f      │\n"
            "           └───────┘ └─────────────┘\n"
        )
        assert_print_statement(
            export.hprint_tree,
            expected_str,
            tree=tree_node,
            border_style="const",
        )

    @staticmethod
    def test_hprint_tree_border_style_diff_node_name_length(tree_node):
        tree_node["b"].name = "bcde"
        tree_node["c"]["f"].name = "fghijk"
        expected_str = (
            "                       ┌────────────┐\n"
            "                      ┌┤     d      │\n"
            "          ┌──────────┐│└────────────┘\n"
            "         ┌┤   bcde   ├┤               ┌───────┐\n"
            "         │└──────────┘│┌────────────┐┌┤   g   │\n"
            "┌───────┐│            └┤     e      ├┤└───────┘\n"
            "│   a   ├┤             └────────────┘│┌───────┐\n"
            "└───────┘│                           └┤   h   │\n"
            "         │                            └───────┘\n"
            "         │┌──────────┐ ┌────────────┐\n"
            "         └┤    c     ├─┤   fghijk   │\n"
            "          └──────────┘ └────────────┘\n"
        )
        assert_print_statement(
            export.hprint_tree, expected_str, tree=tree_node, border_style="const"
        )

    @staticmethod
    def test_hprint_tree_border_style_unequal_char_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.hprint_tree(
                tree_node,
                border_style=["+ ", "+", "+", "+", "|", "-"],
            )
        assert (
            str(exc_info.value)
            == Constants.ERROR_NODE_EXPORT_HPRINT_CUSTOM_STYLE_DIFFERENT_LENGTH
        )

    @staticmethod
    def test_hprint_tree_border_style_missing_style_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.hprint_tree(tree_node, border_style=["+", "+", "+", "+", "|"])
        assert str(exc_info.value) == Constants.ERROR_NODE_EXPORT_BORDER_STYLE_SELECT


class TestVPrintTree:
    @staticmethod
    def test_vprint_tree(tree_node):
        assert_print_statement(
            export.vprint_tree,
            tree_node_vstr,
            tree=tree_node,
        )

    @staticmethod
    def test_vprint_tree2():
        from bigtree.tree.construct import list_to_tree

        tree_node = list_to_tree(
            [
                "a/b/b1",
                "a/b/b2",
                "a/b/b3",
                "a/b/b4",
                "a/b/b5",
                "a/c/c1/c11",
                "a/c/c1/c12",
                "a/d/d1",
                "a/d/d2",
                "a/d/d3",
                "a/d/d4",
                "a/d/d5/d51",
                "a/d/d5/d52",
                "a/d/d5/d53",
                "a/d/d5/d54",
                "a/d/d6",
                "a/e/e1/e11",
                "a/e/e1/e12",
                "a/e/e1/e13",
                "a/e/e1/e14",
                "a/e/e1/e15",
                "a/e/e1/e16",
                "a/e/e2",
                "a/e/e3/e311",
                "a/e/e3/e312",
                "a/e/e3/e313",
            ]
        )
        expected_str = (
            "                                                                                                   ┌───┐                                                                                                                        \n"
            "                                                                                                   │ a │                                                                                                                        \n"
            "                                                                                                   └─┬─┘                                                                                                                        \n"
            "                  ┌────────────────────────────┬──────────────────────────────────────────────┬──────┴──────────────────────────────────────────────────────────────────────────────────┐                                       \n"
            "                ┌─┴─┐                        ┌─┴─┐                                          ┌─┴─┐                                                                                     ┌─┴─┐                                     \n"
            "                │ b │                        │ c │                                          │ d │                                                                                     │ e │                                     \n"
            "                └─┬─┘                        └─┬─┘                                          └─┬─┘                                                                                     └─┬─┘                                     \n"
            "  ┌───────┬───────┼───────┬───────┐            │            ┌───────┬───────┬───────┬─────────┴───────────┬─────────────────────┐                              ┌────────────────────────┴─────┬──────────────────┐              \n"
            "┌─┴──┐  ┌─┴──┐  ┌─┴──┐  ┌─┴──┐  ┌─┴──┐       ┌─┴──┐       ┌─┴──┐  ┌─┴──┐  ┌─┴──┐  ┌─┴──┐                ┌─┴──┐                ┌─┴──┐                         ┌─┴──┐                         ┌─┴──┐             ┌─┴──┐           \n"
            "│ b1 │  │ b2 │  │ b3 │  │ b4 │  │ b5 │       │ c1 │       │ d1 │  │ d2 │  │ d3 │  │ d4 │                │ d5 │                │ d6 │                         │ e1 │                         │ e2 │             │ e3 │           \n"
            "└────┘  └────┘  └────┘  └────┘  └────┘       └─┬──┘       └────┘  └────┘  └────┘  └────┘                └─┬──┘                └────┘                         └─┬──┘                         └────┘             └─┬──┘           \n"
            "                                           ┌───┴────┐                                        ┌────────┬───┴────┬────────┐                ┌────────┬────────┬───┴────┬────────┬────────┐                ┌─────────┼─────────┐    \n"
            "                                        ┌──┴──┐  ┌──┴──┐                                  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐          ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐          ┌──┴───┐  ┌──┴───┐  ┌──┴───┐\n"
            "                                        │ c11 │  │ c12 │                                  │ d51 │  │ d52 │  │ d53 │  │ d54 │          │ e11 │  │ e12 │  │ e13 │  │ e14 │  │ e15 │  │ e16 │          │ e311 │  │ e312 │  │ e313 │\n"
            "                                        └─────┘  └─────┘                                  └─────┘  └─────┘  └─────┘  └─────┘          └─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘          └──────┘  └──────┘  └──────┘\n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
        )

    @staticmethod
    def test_vprint_tree_multiline(tree_node):
        tree_node.name = "a\na2"
        tree_node["b"]["e"].name = "e\ne2\nmultiln"
        expected_str = (
            "             ┌────┐       \n"
            "             │ a  │       \n"
            "             │ a2 │       \n"
            "             └─┬──┘       \n"
            "       ┌───────┴───────┐  \n"
            "     ┌─┴─┐           ┌─┴─┐\n"
            "     │ b │           │ c │\n"
            "     └─┬─┘           └─┬─┘\n"
            "  ┌────┴────┐          │  \n"
            "┌─┴─┐  ┌────┴────┐   ┌─┴─┐\n"
            "│ d │  │    e    │   │ f │\n"
            "└───┘  │    e2   │   └───┘\n"
            "       │ multiln │        \n"
            "       └────┬────┘        \n"
            "         ┌──┴───┐         \n"
            "       ┌─┴─┐  ┌─┴─┐       \n"
            "       │ g │  │ h │       \n"
            "       └───┘  └───┘       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
        )

    @staticmethod
    def test_vprint_tree_multiline_parent_longer(tree_node):
        from bigtree.node import node

        tree_node = node.Node("a")
        tree_node.children = [
            node.Node("b"),
            node.Node("ccccccc\ncc", children=[node.Node("e")]),
            node.Node("d"),
        ]
        expected_str = (
            "          ┌───┐          \n"
            "          │ a │          \n"
            "          └─┬─┘          \n"
            "  ┌─────────┼─────────┐  \n"
            "┌─┴─┐  ┌────┴────┐  ┌─┴─┐\n"
            "│ b │  │ ccccccc │  │ d │\n"
            "└───┘  │    cc   │  └───┘\n"
            "       └────┬────┘       \n"
            "            │            \n"
            "          ┌─┴─┐          \n"
            "          │ e │          \n"
            "          └───┘          \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
        )

    @staticmethod
    def test_vprint_tree_alias(tree_node):
        tree_node.alias_attr = "a\na2"
        tree_node["b"]["e"].alias_attr = "e\ne2\nalias_1"
        expected_str = (
            "             ┌────┐       \n"
            "             │ a  │       \n"
            "             │ a2 │       \n"
            "             └─┬──┘       \n"
            "       ┌───────┴───────┐  \n"
            "     ┌─┴─┐           ┌─┴─┐\n"
            "     │ b │           │ c │\n"
            "     └─┬─┘           └─┬─┘\n"
            "  ┌────┴────┐          │  \n"
            "┌─┴─┐  ┌────┴────┐   ┌─┴─┐\n"
            "│ d │  │    e    │   │ f │\n"
            "└───┘  │    e2   │   └───┘\n"
            "       │ alias_1 │        \n"
            "       └────┬────┘        \n"
            "         ┌──┴───┐         \n"
            "       ┌─┴─┐  ┌─┴─┐       \n"
            "       │ g │  │ h │       \n"
            "       └───┘  └───┘       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            alias="alias_attr",
        )

    @staticmethod
    def test_vprint_tree_spacing(tree_node):
        expected_str = (
            "                ┌───┐           \n"
            "                │ a │           \n"
            "                └─┬─┘           \n"
            "        ┌─────────┴──────────┐  \n"
            "      ┌─┴─┐                ┌─┴─┐\n"
            "      │ b │                │ c │\n"
            "      └─┬─┘                └─┬─┘\n"
            "  ┌─────┴──────┐             │  \n"
            "┌─┴─┐        ┌─┴─┐         ┌─┴─┐\n"
            "│ d │        │ e │         │ f │\n"
            "└───┘        └─┬─┘         └───┘\n"
            "           ┌───┴────┐           \n"
            "         ┌─┴─┐    ┌─┴─┐         \n"
            "         │ g │    │ h │         \n"
            "         └───┘    └───┘         \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            spacing=4,
        )

    @staticmethod
    def test_vprint_tree_strip(tree_node):
        expected_str = (
            "             ┌───┐\n"
            "             │ a │\n"
            "             └─┬─┘\n"
            "       ┌───────┴───────┐\n"
            "     ┌─┴─┐           ┌─┴─┐\n"
            "     │ b │           │ c │\n"
            "     └─┬─┘           └─┬─┘\n"
            "  ┌────┴────┐          │\n"
            "┌─┴─┐     ┌─┴─┐      ┌─┴─┐\n"
            "│ d │     │ e │      │ f │\n"
            "└───┘     └─┬─┘      └───┘\n"
            "         ┌──┴───┐\n"
            "       ┌─┴─┐  ┌─┴─┐\n"
            "       │ g │  │ h │\n"
            "       └───┘  └───┘\n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            strip=True,
        )

    @staticmethod
    def test_vprint_tree_long_root_name_length(tree_node):
        tree_node.name = "abcdefghijkl"
        expected_str = (
            "        ┌──────────────┐  \n"
            "        │ abcdefghijkl │  \n"
            "        └──────┬───────┘  \n"
            "       ┌───────┴───────┐  \n"
            "     ┌─┴─┐           ┌─┴─┐\n"
            "     │ b │           │ c │\n"
            "     └─┬─┘           └─┬─┘\n"
            "  ┌────┴────┐          │  \n"
            "┌─┴─┐     ┌─┴─┐      ┌─┴─┐\n"
            "│ d │     │ e │      │ f │\n"
            "└───┘     └─┬─┘      └───┘\n"
            "         ┌──┴───┐         \n"
            "       ┌─┴─┐  ┌─┴─┐       \n"
            "       │ g │  │ h │       \n"
            "       └───┘  └───┘       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
        )

    @staticmethod
    def test_vprint_tree_diff_node_name_length(tree_node):
        tree_node["b"].name = "bcde"
        tree_node["c"]["f"].name = "fghijk"
        expected_str = (
            "              ┌───┐            \n"
            "              │ a │            \n"
            "              └─┬─┘            \n"
            "       ┌────────┴────────┐     \n"
            "    ┌──┴───┐           ┌─┴─┐   \n"
            "    │ bcde │           │ c │   \n"
            "    └──┬───┘           └─┬─┘   \n"
            "  ┌────┴────┐            │     \n"
            "┌─┴─┐     ┌─┴─┐      ┌───┴────┐\n"
            "│ d │     │ e │      │ fghijk │\n"
            "└───┘     └─┬─┘      └────────┘\n"
            "         ┌──┴───┐              \n"
            "       ┌─┴─┐  ┌─┴─┐            \n"
            "       │ g │  │ h │            \n"
            "       └───┘  └───┘            \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
        )

    @staticmethod
    def test_vprint_tree_child_node_name(tree_node):
        assert_print_statement(
            export.vprint_tree,
            tree_node_branch_vstr,
            tree=tree_node,
            node_name_or_path="b",
        )

    @staticmethod
    def test_vprint_tree_child_node_name_error(tree_node):
        node_name_or_path = "bb"
        with pytest.raises(ValueError) as exc_info:
            export.vprint_tree(tree_node, node_name_or_path=node_name_or_path)
        assert str(
            exc_info.value
        ) == Constants.ERROR_NODE_EXPORT_PRINT_INVALID_PATH.format(
            node_name_or_path=node_name_or_path
        )

    @staticmethod
    def test_vprint_tree_child_node_path(tree_node):
        assert_print_statement(
            export.vprint_tree,
            tree_node_branch_vstr,
            tree=tree_node,
            node_name_or_path="a/b",
        )

    @staticmethod
    def test_vprint_tree_intermediate_node_name(tree_node):
        expected_str = (
            "              ┌──┐        \n"
            "              │  │        \n"
            "              └┬─┘        \n"
            "       ┌───────┴───────┐  \n"
            "      ┌┴─┐            ┌┴─┐\n"
            "      │  │            │  │\n"
            "      └┬─┘            └┬─┘\n"
            "  ┌────┴────┐          │  \n"
            "┌─┴─┐      ┌┴─┐      ┌─┴─┐\n"
            "│ d │      │  │      │ f │\n"
            "└───┘      └┬─┘      └───┘\n"
            "         ┌──┴───┐         \n"
            "       ┌─┴─┐  ┌─┴─┐       \n"
            "       │ g │  │ h │       \n"
            "       └───┘  └───┘       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            intermediate_node_name=False,
        )

    @staticmethod
    def test_vprint_tree_intermediate_node_name_border_none(tree_node):
        expected_str = (
            "     ┬    \n"
            "  ┌──┴───┐\n"
            "  │      │\n"
            "┌─┴─┐    │\n"
            "d   │    f\n"
            "   ┌┴─┐   \n"
            "   g  h   \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            intermediate_node_name=False,
            border_style=None,
        )

    @staticmethod
    def test_vprint_tree_intermediate_node_name_diff_node_name_length(tree_node):
        tree_node["b"].name = "bcde"
        tree_node["c"]["f"].name = "fghijk"
        expected_str = (
            "               ┌──┐            \n"
            "               │  │            \n"
            "               └┬─┘            \n"
            "       ┌────────┴────────┐     \n"
            "      ┌┴─┐              ┌┴─┐   \n"
            "      │  │              │  │   \n"
            "      └┬─┘              └┬─┘   \n"
            "  ┌────┴────┐            │     \n"
            "┌─┴─┐      ┌┴─┐      ┌───┴────┐\n"
            "│ d │      │  │      │ fghijk │\n"
            "└───┘      └┬─┘      └────────┘\n"
            "         ┌──┴───┐              \n"
            "       ┌─┴─┐  ┌─┴─┐            \n"
            "       │ g │  │ h │            \n"
            "       └───┘  └───┘            \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            intermediate_node_name=False,
        )

    # style
    @staticmethod
    def test_vprint_tree_style_ansi(tree_node):
        expected_str = (
            "             `---`        \n"
            "             | a |        \n"
            "             `-+-`        \n"
            "       /-------+-------\\  \n"
            "     `-+-`           `-+-`\n"
            "     | b |           | c |\n"
            "     `-+-`           `-+-`\n"
            "  /----+----\\          |  \n"
            "`-+-`     `-+-`      `-+-`\n"
            "| d |     | e |      | f |\n"
            "`---`     `-+-`      `---`\n"
            "         /--+---\\         \n"
            "       `-+-`  `-+-`       \n"
            "       | g |  | h |       \n"
            "       `---`  `---`       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            style="ansi",
            border_style="ansi",
        )

    @staticmethod
    def test_vprint_tree_style_ascii(tree_node):
        expected_str = (
            "             +---+        \n"
            "             | a |        \n"
            "             +-+-+        \n"
            "       +-------+-------+  \n"
            "     +-+-+           +-+-+\n"
            "     | b |           | c |\n"
            "     +-+-+           +-+-+\n"
            "  +----+----+          |  \n"
            "+-+-+     +-+-+      +-+-+\n"
            "| d |     | e |      | f |\n"
            "+---+     +-+-+      +---+\n"
            "         +--+---+         \n"
            "       +-+-+  +-+-+       \n"
            "       | g |  | h |       \n"
            "       +---+  +---+       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            style="ascii",
            border_style="ascii",
        )

    @staticmethod
    def test_vprint_tree_style_const(tree_node):
        expected_str = (
            "             ┌───┐        \n"
            "             │ a │        \n"
            "             └─┬─┘        \n"
            "       ┌───────┴───────┐  \n"
            "     ┌─┴─┐           ┌─┴─┐\n"
            "     │ b │           │ c │\n"
            "     └─┬─┘           └─┬─┘\n"
            "  ┌────┴────┐          │  \n"
            "┌─┴─┐     ┌─┴─┐      ┌─┴─┐\n"
            "│ d │     │ e │      │ f │\n"
            "└───┘     └─┬─┘      └───┘\n"
            "         ┌──┴───┐         \n"
            "       ┌─┴─┐  ┌─┴─┐       \n"
            "       │ g │  │ h │       \n"
            "       └───┘  └───┘       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            style="const",
        )

    @staticmethod
    def test_vprint_tree_style_const_bold(tree_node):
        expected_str = (
            "             ┏━━━┓        \n"
            "             ┃ a ┃        \n"
            "             ┗━┳━┛        \n"
            "       ┏━━━━━━━┻━━━━━━━┓  \n"
            "     ┏━┻━┓           ┏━┻━┓\n"
            "     ┃ b ┃           ┃ c ┃\n"
            "     ┗━┳━┛           ┗━┳━┛\n"
            "  ┏━━━━┻━━━━┓          ┃  \n"
            "┏━┻━┓     ┏━┻━┓      ┏━┻━┓\n"
            "┃ d ┃     ┃ e ┃      ┃ f ┃\n"
            "┗━━━┛     ┗━┳━┛      ┗━━━┛\n"
            "         ┏━━┻━━━┓         \n"
            "       ┏━┻━┓  ┏━┻━┓       \n"
            "       ┃ g ┃  ┃ h ┃       \n"
            "       ┗━━━┛  ┗━━━┛       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            style="const_bold",
            border_style="const_bold",
        )

    @staticmethod
    def test_vprint_tree_style_rounded(tree_node):
        expected_str = (
            "             ╭───╮        \n"
            "             │ a │        \n"
            "             ╰─┬─╯        \n"
            "       ╭───────┴───────╮  \n"
            "     ╭─┴─╮           ╭─┴─╮\n"
            "     │ b │           │ c │\n"
            "     ╰─┬─╯           ╰─┬─╯\n"
            "  ╭────┴────╮          │  \n"
            "╭─┴─╮     ╭─┴─╮      ╭─┴─╮\n"
            "│ d │     │ e │      │ f │\n"
            "╰───╯     ╰─┬─╯      ╰───╯\n"
            "         ╭──┴───╮         \n"
            "       ╭─┴─╮  ╭─┴─╮       \n"
            "       │ g │  │ h │       \n"
            "       ╰───╯  ╰───╯       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            style="rounded",
            border_style="rounded",
        )

    @staticmethod
    def test_vprint_tree_style_double(tree_node):
        expected_str = (
            "             ╔═══╗        \n"
            "             ║ a ║        \n"
            "             ╚═╦═╝        \n"
            "       ╔═══════╩═══════╗  \n"
            "     ╔═╩═╗           ╔═╩═╗\n"
            "     ║ b ║           ║ c ║\n"
            "     ╚═╦═╝           ╚═╦═╝\n"
            "  ╔════╩════╗          ║  \n"
            "╔═╩═╗     ╔═╩═╗      ╔═╩═╗\n"
            "║ d ║     ║ e ║      ║ f ║\n"
            "╚═══╝     ╚═╦═╝      ╚═══╝\n"
            "         ╔══╩═══╗         \n"
            "       ╔═╩═╗  ╔═╩═╗       \n"
            "       ║ g ║  ║ h ║       \n"
            "       ╚═══╝  ╚═══╝       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            style="double",
            border_style="double",
        )

    @staticmethod
    def test_vprint_tree_style_unknown_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.vprint_tree(tree_node, style="something")
        assert str(exc_info.value).startswith(
            Constants.ERROR_NODE_EXPORT_PRINT_INVALID_STYLE
        )

    # custom_style - BaseVPrintStyle
    @staticmethod
    def test_vprint_tree_style_ansi_class(tree_node):
        from bigtree.utils.constants import ANSIBorderStyle, ANSIVPrintStyle

        expected_str = (
            "             `---`        \n"
            "             | a |        \n"
            "             `-+-`        \n"
            "       /-------+-------\\  \n"
            "     `-+-`           `-+-`\n"
            "     | b |           | c |\n"
            "     `-+-`           `-+-`\n"
            "  /----+----\\          |  \n"
            "`-+-`     `-+-`      `-+-`\n"
            "| d |     | e |      | f |\n"
            "`---`     `-+-`      `---`\n"
            "         /--+---\\         \n"
            "       `-+-`  `-+-`       \n"
            "       | g |  | h |       \n"
            "       `---`  `---`       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            style=ANSIVPrintStyle,
            border_style=ANSIBorderStyle,
        )

    @staticmethod
    def test_vprint_tree_style_ascii_class(tree_node):
        from bigtree.utils.constants import ASCIIBorderStyle, ASCIIVPrintStyle

        expected_str = (
            "             +---+        \n"
            "             | a |        \n"
            "             +-+-+        \n"
            "       +-------+-------+  \n"
            "     +-+-+           +-+-+\n"
            "     | b |           | c |\n"
            "     +-+-+           +-+-+\n"
            "  +----+----+          |  \n"
            "+-+-+     +-+-+      +-+-+\n"
            "| d |     | e |      | f |\n"
            "+---+     +-+-+      +---+\n"
            "         +--+---+         \n"
            "       +-+-+  +-+-+       \n"
            "       | g |  | h |       \n"
            "       +---+  +---+       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            style=ASCIIVPrintStyle,
            border_style=ASCIIBorderStyle,
        )

    @staticmethod
    def test_vprint_tree_style_custom_class(tree_node):
        from bigtree.utils.constants import BaseVPrintStyle

        expected_str = (
            "             ┌───┐        \n"
            "             │ a │        \n"
            "             └─-─┘        \n"
            "       --------+-------|  \n"
            "     ┌─+─┐           ┌─+─┐\n"
            "     │ b │           │ c │\n"
            "     └─-─┘           └─-─┘\n"
            "  -----+----|          =  \n"
            "┌─+─┐     ┌─+─┐      ┌─+─┐\n"
            "│ d │     │ e │      │ f │\n"
            "└───┘     └─-─┘      └───┘\n"
            "         ---+---|         \n"
            "       ┌─+─┐  ┌─+─┐       \n"
            "       │ g │  │ h │       \n"
            "       └───┘  └───┘       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            style=BaseVPrintStyle("-", "-", "+", "+", "|", "-", "="),
        )

    @staticmethod
    def test_vprint_tree_style_class_unequal_char_error(tree_node):
        from bigtree.utils.constants import BaseVPrintStyle

        with pytest.raises(ValueError) as exc_info:
            export.vprint_tree(
                tree_node,
                style=BaseVPrintStyle("- ", "-", "+", "+", "|", "-", "="),
            )
        assert (
            str(exc_info.value)
            == Constants.ERROR_NODE_EXPORT_HPRINT_CUSTOM_STYLE_DIFFERENT_LENGTH
        )

    # custom_style
    @staticmethod
    def test_vprint_tree_custom_style(tree_node):
        expected_str = (
            "             ┌───┐        \n"
            "             │ a │        \n"
            "             └─-─┘        \n"
            "       --------+-------|  \n"
            "     ┌─+─┐           ┌─+─┐\n"
            "     │ b │           │ c │\n"
            "     └─-─┘           └─-─┘\n"
            "  -----+----|          =  \n"
            "┌─+─┐     ┌─+─┐      ┌─+─┐\n"
            "│ d │     │ e │      │ f │\n"
            "└───┘     └─-─┘      └───┘\n"
            "         ---+---|         \n"
            "       ┌─+─┐  ┌─+─┐       \n"
            "       │ g │  │ h │       \n"
            "       └───┘  └───┘       \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            style=["-", "-", "+", "+", "|", "-", "="],
        )

    @staticmethod
    def test_vprint_tree_custom_style_unequal_char_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.vprint_tree(
                tree_node,
                style=["- ", "-", "+", "+", "|", "-", "="],
            )
        assert (
            str(exc_info.value)
            == Constants.ERROR_NODE_EXPORT_HPRINT_CUSTOM_STYLE_DIFFERENT_LENGTH
        )

    @staticmethod
    def test_vprint_tree_custom_style_missing_style_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.vprint_tree(tree_node, style=["-", "+", "+", "|", "-", "="])
        assert str(exc_info.value) == Constants.ERROR_NODE_EXPORT_HPRINT_STYLE_SELECT

    @staticmethod
    def test_vprint_tree_kwargs(tree_node):
        output = io.StringIO()
        export.vprint_tree(tree_node, file=output)
        assert output.getvalue() == tree_node_vstr

    # border_style
    @staticmethod
    def test_vprint_tree_border_none(tree_node):
        expected_str = (
            "     a    \n"
            "  ┌──┴───┐\n"
            "  b      c\n"
            "┌─┴─┐    │\n"
            "d   e    f\n"
            "   ┌┴─┐   \n"
            "   g  h   \n"
        )
        assert_print_statement(
            export.vprint_tree,
            expected_str,
            tree=tree_node,
            border_style=None,
        )

    @staticmethod
    def test_vprint_tree_border_style_unequal_char_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.vprint_tree(
                tree_node,
                border_style=["+ ", "+", "+", "+", "|", "-"],
            )
        assert (
            str(exc_info.value)
            == Constants.ERROR_NODE_EXPORT_HPRINT_CUSTOM_STYLE_DIFFERENT_LENGTH
        )

    @staticmethod
    def test_vprint_tree_border_style_missing_style_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.vprint_tree(tree_node, border_style=["+", "+", "+", "+", "|"])
        assert str(exc_info.value) == Constants.ERROR_NODE_EXPORT_BORDER_STYLE_SELECT


class TestTreeToNewick:
    @staticmethod
    def test_tree_to_newick(tree_node):
        newick_str = export.tree_to_newick(tree_node)
        expected_str = "((d,(g,h)e)b,(f)c)a"
        assert newick_str == expected_str

    @staticmethod
    def test_tree_to_newick_length(tree_node):
        newick_str = export.tree_to_newick(tree_node, length_attr="age")
        expected_str = "((d:40,(g:10,h:6)e:35)b:65,(f:38)c:60)a"
        assert newick_str == expected_str

    @staticmethod
    def test_tree_to_newick_length_invalid_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            export.tree_to_newick(tree_node, length_attr="age2")
        assert str(exc_info.value).startswith(Constants.ERROR_NODE_NEWICK_ATTR_INVALID)

    @staticmethod
    def test_tree_to_newick_length_sep(tree_node):
        newick_str = export.tree_to_newick(tree_node, length_attr="age", length_sep=";")
        expected_str = "((d;40,(g;10,h;6)e;35)b;65,(f;38)c;60)a"
        assert newick_str == expected_str

    @staticmethod
    def test_tree_to_newick_attr_list(tree_node):
        newick_str = export.tree_to_newick(tree_node, attr_list=["age"])
        expected_str = "((d[&&NHX:age=40],(g[&&NHX:age=10],h[&&NHX:age=6])e[&&NHX:age=35])b[&&NHX:age=65],(f[&&NHX:age=38])c[&&NHX:age=60])a[&&NHX:age=90]"
        assert newick_str == expected_str

    @staticmethod
    def test_tree_to_newick_attr_list_invalid(tree_node):
        newick_str = export.tree_to_newick(tree_node, attr_list=["age2"])
        expected_str = """((d,(g,h)e)b,(f)c)a"""
        assert newick_str == expected_str

    @staticmethod
    def test_tree_to_newick_attr_prefix(tree_node):
        newick_str = export.tree_to_newick(tree_node, attr_list=["age"], attr_prefix="")
        expected_str = "((d[age=40],(g[age=10],h[age=6])e[age=35])b[age=65],(f[age=38])c[age=60])a[age=90]"
        assert newick_str == expected_str

    @staticmethod
    def test_tree_to_newick_intermediate_node_name(tree_node):
        newick_str = export.tree_to_newick(
            tree_node, intermediate_node_name=False, attr_list=["age"]
        )
        expected_str = "((d[&&NHX:age=40],(g[&&NHX:age=10],h[&&NHX:age=6])[&&NHX:age=35])[&&NHX:age=65],(f[&&NHX:age=38])[&&NHX:age=60])[&&NHX:age=90]"
        assert newick_str == expected_str

    @staticmethod
    def test_tree_to_newick_special_character():
        from bigtree.node.node import Node

        root = Node("(root)")
        b = Node("[b]", parent=root)
        c = Node("c:", parent=root)
        _ = Node("d,", parent=b)
        e = Node(":e", parent=b)
        _ = Node("f=", parent=c)
        _ = Node('"g"', parent=e)
        _ = Node("'h'", parent=e)

        newick_str = export.tree_to_newick(root)
        expected_str = """(('d,',("g",'"h"')':e')'[b]',('f=')'c:')'(root)'"""
        assert newick_str == expected_str

    @staticmethod
    def test_tree_to_newick_phylogenetic(phylogenetic_tree):
        newick_str = export.tree_to_newick(
            phylogenetic_tree,
            intermediate_node_name=False,
            length_attr="length",
            attr_list=["S", "E", "D", "B"],
        )
        expected_str = "(((ADH2:0.1[&&NHX:S=human:E=1.1.1.1],ADH1:0.11[&&NHX:S=human:E=1.1.1.1]):0.05[&&NHX:S=Primates:E=1.1.1.1:D=Y:B=100],ADHY:0.1[&&NHX:S=nematode:E=1.1.1.1],ADHX:0.12[&&NHX:S=insect:E=1.1.1.1]):0.1[&&NHX:S=Metazoa:E=1.1.1.1:D=N],(ADH4:0.09[&&NHX:S=yeast:E=1.1.1.1],ADH3:0.13[&&NHX:S=yeast:E=1.1.1.1],ADH2:0.12[&&NHX:S=yeast:E=1.1.1.1],ADH1:0.11[&&NHX:S=yeast:E=1.1.1.1]):0.1[&&NHX:S=Fungi])[&&NHX:E=1.1.1.1:D=N]"
        assert newick_str == expected_str

    @staticmethod
    def test_tree_to_newick_phylogenetic_attr_sep(phylogenetic_tree):
        newick_str = export.tree_to_newick(
            phylogenetic_tree,
            intermediate_node_name=False,
            length_attr="length",
            attr_list=["S", "E", "D", "B"],
            attr_sep=";",
        )
        expected_str = "(((ADH2:0.1[&&NHX:S=human;E=1.1.1.1],ADH1:0.11[&&NHX:S=human;E=1.1.1.1]):0.05[&&NHX:S=Primates;E=1.1.1.1;D=Y;B=100],ADHY:0.1[&&NHX:S=nematode;E=1.1.1.1],ADHX:0.12[&&NHX:S=insect;E=1.1.1.1]):0.1[&&NHX:S=Metazoa;E=1.1.1.1;D=N],(ADH4:0.09[&&NHX:S=yeast;E=1.1.1.1],ADH3:0.13[&&NHX:S=yeast;E=1.1.1.1],ADH2:0.12[&&NHX:S=yeast;E=1.1.1.1],ADH1:0.11[&&NHX:S=yeast;E=1.1.1.1]):0.1[&&NHX:S=Fungi])[&&NHX:E=1.1.1.1;D=N]"
        assert newick_str == expected_str

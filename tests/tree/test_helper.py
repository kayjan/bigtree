import math

import pytest

from bigtree.node import basenode, node
from bigtree.tree import export, helper
from bigtree.utils import exceptions
from tests.conftest import assert_print_statement
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
)
from tests.test_constants import Constants


class TestCloneTree:
    @staticmethod
    def test_clone_tree_wrong_type_error():
        with pytest.raises(TypeError) as exc_info:
            helper.clone_tree({}, node.Node)
        assert str(exc_info.value) == Constants.ERROR_NODE_TYPE.format(type="BaseNode")

    @staticmethod
    def test_clone_tree_basenode_node(tree_basenode):
        root_clone = helper.clone_tree(tree_basenode, node_type=node.Node)
        assert isinstance(root_clone, node.Node), "Wrong type returned"
        assert_tree_structure_basenode_root(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)

    @staticmethod
    def test_clone_tree_node_basenode(tree_node):
        root_clone = helper.clone_tree(tree_node, node_type=basenode.BaseNode)
        assert isinstance(root_clone, basenode.BaseNode), "Wrong type returned"
        assert_tree_structure_basenode_root(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)

    @staticmethod
    def test_clone_tree_basenode_custom(tree_basenode):
        class NodeA(node.Node):
            pass

        root_clone = helper.clone_tree(tree_basenode, node_type=NodeA)
        assert isinstance(root_clone, NodeA), Constants.ERROR_CUSTOM_TYPE.format(
            type="NodeA"
        )
        assert_tree_structure_basenode_root(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)


class TestGetSubtree:
    @staticmethod
    def test_get_subtree(tree_node):
        # Subtree is b/d, b/e/g, b/e/h
        tree_subtree = helper.get_subtree(tree_node, "a/b")
        assert tree_subtree.node_name == "b"
        assert len(tree_subtree.children) == 2
        assert not len(tree_subtree.children[0].children)
        assert len(tree_subtree.children[1].children) == 2

    @staticmethod
    def test_get_subtree_sep(tree_node):
        # Subtree is b/d, b/e/g, b/e/h
        tree_node.sep = "."
        tree_subtree = helper.get_subtree(tree_node, "a.b")
        assert tree_subtree.children[0].path_name == ".b.d"
        assert tree_subtree.children[1].path_name == ".b.e"


class TestPruneTree:
    @staticmethod
    def test_prune_tree(tree_node):
        # Pruned tree is a/b/d, a/b/e/g, a/b/e/h
        tree_prune = helper.prune_tree(tree_node, "a/b")

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 2
        assert len(tree_prune.children[0].children[0].children) == 0
        assert len(tree_prune.children[0].children[1].children) == 2

    @staticmethod
    def test_prune_tree_exact(tree_node):
        # Pruned tree is a/b/e/g
        tree_prune = helper.prune_tree(tree_node, "a/b/e/g", exact=True)

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 1
        assert len(tree_prune.children[0].children[0].children) == 1

    @staticmethod
    def test_prune_tree_list(tree_node):
        # Pruned tree is a/b/d, a/b/e/g, a/b/e/h
        tree_prune = helper.prune_tree(tree_node, ["a/b/d", "a/b/e/g", "a/b/e/h"])

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 2
        assert len(tree_prune.children[0].children[0].children) == 0
        assert len(tree_prune.children[0].children[1].children) == 2

    @staticmethod
    def test_prune_tree_path_and_depth(tree_node):
        # Pruned tree is a/b/d, a/b/e (a/b/e/g, a/b/e/h pruned away)
        tree_prune = helper.prune_tree(tree_node, "a/b", max_depth=3)

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 2
        assert len(tree_prune.children[0].children[0].children) == 0
        assert (
            len(tree_prune.children[0].children[1].children) == 0
        ), "Depth at 4 is not pruned away"

    @staticmethod
    def test_prune_tree_path_and_depth_and_list(tree_node):
        # Pruned tree is a/b/d, a/b/e (a/b/e/g, a/b/e/h pruned away)
        tree_prune = helper.prune_tree(
            tree_node, ["a/b/d", "a/b/e/g", "a/b/e/h"], max_depth=3
        )

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 2
        assert len(tree_prune.children[0].children[0].children) == 0
        assert (
            len(tree_prune.children[0].children[1].children) == 0
        ), "Depth at 4 is not pruned away"

    @staticmethod
    def test_prune_tree_path_and_depth_and_list_and_exact(tree_node):
        # Pruned tree is a/b/d, a/b/e (a/b/e/g, a/b/e/h pruned away)
        tree_prune = helper.prune_tree(
            tree_node, ["a/b/d", "a/b/e/g", "a/b/e/h"], exact=True, max_depth=3
        )

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 2
        assert len(tree_prune.children[0].children[0].children) == 0
        assert (
            len(tree_prune.children[0].children[1].children) == 0
        ), "Depth at 4 is not pruned away"

    @staticmethod
    def test_prune_tree_only_depth(tree_node):
        # Pruned tree is a/b, a/c (a/b/e/g, a/b/e/h, a/c/f pruned away)
        tree_prune = helper.prune_tree(tree_node, max_depth=2)

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 2
        assert (
            len(tree_prune.children[0].children) == 0
        ), "Depth at 3 is not pruned away"
        assert (
            len(tree_prune.children[1].children) == 0
        ), "Depth at 3 is not pruned away"

    @staticmethod
    def test_prune_tree_second_child(tree_node):
        # Pruned tree is a/c/f
        tree_prune = helper.prune_tree(tree_node, "a/c")

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 1

    @staticmethod
    def test_prune_tree_multiple_path_error(tree_node):
        dd = node.Node("d")
        dd.parent = tree_node.children[-1]
        with pytest.raises(exceptions.SearchError) as exc_info:
            helper.prune_tree(tree_node, "d")
        assert str(exc_info.value).startswith(
            Constants.ERROR_SEARCH_LESS_THAN_N_ELEMENT.format(count=1)
        )

    @staticmethod
    def test_prune_tree_nonexistant_path_error(tree_node):
        prune_path = "i"
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            helper.prune_tree(tree_node, prune_path)
        assert str(exc_info.value) == Constants.ERROR_NODE_PRUNE_NOT_FOUND.format(
            prune_path=prune_path
        )

    @staticmethod
    def test_prune_tree_sep(tree_node):
        # Pruned tree is a/c/f
        tree_prune = helper.prune_tree(tree_node, "a\\c", sep="\\")

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 1

    @staticmethod
    def test_prune_tree_sep_error(tree_node):
        prune_path = "a\\c"
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            helper.prune_tree(tree_node, prune_path)
        assert str(exc_info.value) == Constants.ERROR_NODE_PRUNE_NOT_FOUND.format(
            prune_path=prune_path
        )

    @staticmethod
    def test_prune_tree_no_arg_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            helper.prune_tree(tree_node)
        assert str(exc_info.value) == Constants.ERROR_NODE_PRUNE_ARGUMENT


EXPECTED_TREE_NODE_DIFF = (
    "a\n"
    "├── b (-)\n"
    "│   ├── d (-)\n"
    "│   └── e (-)\n"
    "│       ├── g (-)\n"
    "│       └── h (-)\n"
    "├── c\n"
    "│   └── e (+)\n"
    "│       ├── g (+)\n"
    "│       └── h (+)\n"
    "└── i (+)\n"
    "    └── j (+)\n"
)
EXPECTED_TREE_NODE_DIFF_ALL = (
    "a\n"
    "├── b (-)\n"
    "│   ├── d (-)\n"
    "│   └── e (-)\n"
    "│       ├── g (-)\n"
    "│       └── h (-)\n"
    "├── c\n"
    "│   ├── e (+)\n"
    "│   │   ├── g (+)\n"
    "│   │   └── h (+)\n"
    "│   └── f\n"
    "└── i (+)\n"
    "    └── j (+)\n"
)


class TestTreeDiff:
    @staticmethod
    def test_tree_diff(tree_node, tree_node_diff):
        tree_diff = helper.get_tree_diff(tree_node, tree_node_diff)
        assert_print_statement(
            export.print_tree, EXPECTED_TREE_NODE_DIFF, tree=tree_diff
        )

    @staticmethod
    def test_tree_diff_same_prefix():
        tree_node = node.Node(
            "a", children=[node.Node("bb", children=[node.Node("b")])]
        )
        other_tree_node = node.Node("a", children=[node.Node("b")])
        tree_diff = helper.get_tree_diff(tree_node, other_tree_node)
        # fmt: off
        expected_str = (
            "a\n"
            "├── b (+)\n"
            "└── bb (-)\n"
            "    └── b (-)\n"
        )
        # fmt: on
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_diff_sep_error(tree_node):
        other_tree_node = helper.prune_tree(tree_node, "a/c")
        other_tree_node.sep = "-"
        with pytest.raises(ValueError) as exc_info:
            helper.get_tree_diff(tree_node, other_tree_node)
        assert str(exc_info.value) == Constants.ERROR_NODE_TREE_DIFF_DIFF_SEP

    @staticmethod
    def test_tree_diff_sep_clash_with_node_name_error(tree_node):
        other_tree_node = helper.prune_tree(tree_node, "a/c")
        node.Node("/d", parent=other_tree_node)
        with pytest.raises(exceptions.TreeError) as exc_info:
            helper.get_tree_diff(tree_node, other_tree_node)
        assert str(exc_info.value) == Constants.ERROR_NODE_NAME

    @staticmethod
    def test_tree_diff_sep_clash_with_node_name(tree_node):
        other_tree_node = helper.prune_tree(tree_node, "a/c")
        node.Node("/d", parent=other_tree_node)
        tree_node.sep = "."
        other_tree_node.sep = "."
        tree_diff = helper.get_tree_diff(tree_node, other_tree_node)
        expected_str = (
            "a\n"
            "├── /d (+)\n"
            "└── b (-)\n"
            "    ├── d (-)\n"
            "    └── e (-)\n"
            "        ├── g (-)\n"
            "        └── h (-)\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_forbidden_sep(tree_node, tree_node_diff):
        for symbol in [".", "-", "+", "~"]:
            tree_node.sep = symbol
            tree_node_diff.sep = symbol
            tree_diff = helper.get_tree_diff(tree_node, tree_node_diff)
            assert_print_statement(
                export.print_tree, EXPECTED_TREE_NODE_DIFF, tree=tree_diff
            )

    @staticmethod
    def test_tree_diff_all_diff(tree_node, tree_node_diff):
        tree_diff = helper.get_tree_diff(tree_node, tree_node_diff, only_diff=False)
        assert_print_statement(
            export.print_tree, EXPECTED_TREE_NODE_DIFF_ALL, tree=tree_diff
        )

    @staticmethod
    def test_tree_diff_detail(tree_node, tree_node_diff):
        tree_diff = helper.get_tree_diff(tree_node, tree_node_diff, detail=True)
        expected_str = (
            "a\n"
            "├── b (removed)\n"
            "│   ├── d (removed)\n"
            "│   └── e (moved from)\n"
            "│       ├── g (moved from)\n"
            "│       └── h (moved from)\n"
            "├── c\n"
            "│   └── e (moved to)\n"
            "│       ├── g (moved to)\n"
            "│       └── h (moved to)\n"
            "└── i (added)\n"
            "    └── j (added)\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_detail_clash_names(tree_node, tree_node_diff):
        tree_node_diff.append(node.Node("g"))
        tree_diff = helper.get_tree_diff(tree_node, tree_node_diff, detail=True)
        expected_str = (
            "a\n"
            "├── b (removed)\n"
            "│   ├── d (removed)\n"
            "│   └── e (moved from)\n"
            "│       ├── g (moved from)\n"
            "│       └── h (moved from)\n"
            "├── c\n"
            "│   └── e (moved to)\n"
            "│       ├── g (moved to)\n"  # classified as moved to
            "│       └── h (moved to)\n"
            "├── g (moved to)\n"  # classified as moved to instead of added
            "└── i (added)\n"
            "    └── j (added)\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_aggregate(tree_node, tree_node_diff):
        tree_diff = helper.get_tree_diff(tree_node, tree_node_diff, aggregate=True)
        expected_str = (
            "a\n"
            "├── b (-)\n"
            "│   ├── d (-)\n"
            "│   └── e (-)\n"  # children removed
            "├── c\n"
            "│   └── e (+)\n"
            "│       ├── g\n"  # no (+)
            "│       └── h\n"  # no (+)
            "└── i (+)\n"
            "    └── j (+)\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_all_diff_detail(tree_node, tree_node_diff):
        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_diff, only_diff=False, detail=True
        )
        expected_str = (
            "a\n"
            "├── b (removed)\n"
            "│   ├── d (removed)\n"
            "│   └── e (moved from)\n"
            "│       ├── g (moved from)\n"
            "│       └── h (moved from)\n"
            "├── c\n"
            "│   ├── e (moved to)\n"
            "│   │   ├── g (moved to)\n"
            "│   │   └── h (moved to)\n"
            "│   └── f\n"
            "└── i (added)\n"
            "    └── j (added)\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_all_diff_aggregate(tree_node, tree_node_diff):
        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_diff, only_diff=False, aggregate=True
        )
        expected_str = (
            "a\n"
            "├── b (-)\n"
            "│   ├── d (-)\n"
            "│   └── e (-)\n"
            "│       ├── g\n"  # no  (-)
            "│       └── h\n"  # no  (-)
            "├── c\n"
            "│   ├── e (+)\n"
            "│   │   ├── g\n"  # no  (+)
            "│   │   └── h\n"  # no  (+)
            "│   └── f\n"
            "└── i (+)\n"
            "    └── j (+)\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_detail_aggregate(tree_node, tree_node_diff):
        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_diff, detail=True, aggregate=True
        )
        expected_str = (
            "a\n"
            "├── b (removed)\n"
            "│   ├── d (removed)\n"
            "│   └── e (moved from)\n"  # children removed
            "├── c\n"
            "│   └── e (moved to)\n"
            "│       ├── g\n"  # no (moved to)
            "│       └── h\n"  # no (moved to)
            "└── i (added)\n"
            "    └── j (added)\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_detail_aggregate_clash_names(tree_node, tree_node_diff):
        tree_node_diff.append(node.Node("g"))
        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_diff, detail=True, aggregate=True
        )
        expected_str = (
            "a\n"
            "├── b (removed)\n"
            "│   ├── d (removed)\n"
            "│   └── e (moved from)\n"  # children removed
            "├── c\n"
            "│   └── e (moved to)\n"
            "│       ├── g\n"  # no (moved to)
            "│       └── h\n"  # no (moved to)
            "├── g (added)\n"  # classified as added
            "└── i (added)\n"
            "    └── j (added)\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_all_diff_detail_aggregate(tree_node, tree_node_diff):
        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_diff, only_diff=False, detail=True, aggregate=True
        )
        expected_str = (
            "a\n"
            "├── b (removed)\n"
            "│   ├── d (removed)\n"
            "│   └── e (moved from)\n"
            "│       ├── g\n"  # no (moved from)
            "│       └── h\n"  # no (moved from)
            "├── c\n"
            "│   ├── e (moved to)\n"
            "│   │   ├── g\n"  # no (moved to)
            "│   │   └── h\n"  # no (moved to)
            "│   └── f\n"
            "└── i (added)\n"
            "    └── j (added)\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_new_leaf(tree_node):
        other_tree_node = tree_node.copy()
        tree_node_new_parent = other_tree_node["c"]["f"]
        node.Node("i", parent=tree_node_new_parent)
        tree_diff = helper.get_tree_diff(tree_node, other_tree_node)
        # fmt: off
        expected_str = (
            "a\n"
            "└── c\n"
            "    └── f\n"
            "        └── i (+)\n"
        )
        # fmt: on
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_new_leaf_all_diff(tree_node):
        other_tree_node = tree_node.copy()
        tree_node_new_parent = other_tree_node["c"]["f"]
        node.Node("i", parent=tree_node_new_parent)
        tree_diff = helper.get_tree_diff(tree_node, other_tree_node, only_diff=False)
        expected_str = (
            "a\n"
            "├── b\n"
            "│   ├── d\n"
            "│   └── e\n"
            "│       ├── g\n"
            "│       └── h\n"
            "└── c\n"
            "    └── f\n"
            "        └── i (+)\n"
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_same_tree(tree_node):
        expected = None
        actual = helper.get_tree_diff(tree_node, tree_node)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_diff_same_tree_all_diff(tree_node):
        expected = export.tree_to_dict(tree_node)
        tree_diff = helper.get_tree_diff(tree_node, tree_node, only_diff=False)
        actual = export.tree_to_dict(tree_diff)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_diff_attributes_same_structure_different_attributes(tree_node):
        tree_node_copy = tree_node.copy()
        tree_node_copy["c"]["f"].age += 10
        tree_node_copy["b"].age += 10

        # Without attributes
        expected = None
        actual = helper.get_tree_diff(tree_node, tree_node_copy)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

        # With attributes
        expected = {
            "/a": {"name": "a"},
            "/a/b (~)": {"name": "b (~)", "age": (65, 75)},
            "/a/c": {"name": "c"},
            "/a/c/f (~)": {"name": "f (~)", "age": (38, 48)},
        }

        tree_diff = helper.get_tree_diff(tree_node, tree_node_copy, attr_list=["age"])
        actual = export.tree_to_dict(tree_diff, all_attrs=True)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_diff_attributes_same_structure_different_attributes_all_diff(
        tree_node,
    ):
        tree_node_copy = tree_node.copy()
        tree_node_copy["c"]["f"].age += 10
        tree_node_copy["b"].age += 10

        # Without attributes
        expected = export.tree_to_dict(tree_node)
        tree_diff = helper.get_tree_diff(tree_node, tree_node_copy, only_diff=False)
        actual = export.tree_to_dict(tree_diff)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

        # With attributes
        expected = {
            "/a": {"name": "a"},
            "/a/b (~)": {"name": "b (~)", "age": (65, 75)},
            "/a/b (~)/d": {"name": "d"},
            "/a/b (~)/e": {"name": "e"},
            "/a/b (~)/e/g": {"name": "g"},
            "/a/b (~)/e/h": {"name": "h"},
            "/a/c": {"name": "c"},
            "/a/c/f (~)": {"name": "f (~)", "age": (38, 48)},
        }

        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_copy, attr_list=["age"], only_diff=False
        )
        actual = export.tree_to_dict(tree_diff, all_attrs=True)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_diff_attributes_same_structure_multiple_attributes(tree_node):
        tree_node_copy = tree_node.copy()
        tree_node_copy["c"]["f"].age += 10
        tree_node_copy["b"].age2 = 2  # attribute to create
        tree_node_copy["b"]["e"]["g"].age2 = 4  # attribute to change

        tree_node["c"]["f"].age2 = 1  # attribute to delete
        tree_node["b"]["e"]["g"].age2 = 3  # attribute to change

        # Without attributes
        expected = None
        actual = helper.get_tree_diff(tree_node, tree_node_copy)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

        # With attributes
        expected = {
            "/a": {"name": "a"},
            "/a/b (~)": {"name": "b (~)", "age2": (None, 2)},
            "/a/b (~)/e": {"name": "e"},
            "/a/b (~)/e/g (~)": {"name": "g (~)", "age2": (3, 4)},
            "/a/c": {"name": "c"},
            "/a/c/f (~)": {"name": "f (~)", "age": (38, 48), "age2": (1, None)},
        }

        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_copy, attr_list=["age", "age2"]
        )
        actual = export.tree_to_dict(tree_diff, all_attrs=True)
        assert (
            actual.keys() == expected.keys()
        ), f"Expected\n{expected.keys()}\nReceived\n{actual.keys()}"
        assert math.isnan(
            actual["/a/b (~)"]["age2"][0]
        ), "Check /a/b (~) before-value for age2"
        assert actual["/a/b (~)"]["age2"][1] == 2, "Check /a/b (~) after-value for age2"
        assert (
            not actual["/a/c/f (~)"]["age2"] == 1
        ), "Check /a/c/f (~) before-value for age2"
        assert math.isnan(
            actual["/a/c/f (~)"]["age2"][1]
        ), "Check /a/c/f (~) after-value for age2"
        assert (
            actual["/a/c/f (~)"]["age"] == expected["/a/c/f (~)"]["age"]
        ), "Check /a/c/f (~) for age"

    @staticmethod
    def test_tree_diff_attributes_same_structure_multiple_attributes_all_diff(
        tree_node,
    ):
        tree_node_copy = tree_node.copy()
        tree_node_copy["c"]["f"].age += 10
        tree_node_copy["b"].age2 = 2  # attribute to create
        tree_node_copy["b"]["e"]["g"].age2 = 4  # attribute to change

        tree_node["c"]["f"].age2 = 1  # attribute to delete
        tree_node["b"]["e"]["g"].age2 = 3  # attribute to change

        # Without attributes
        expected = export.tree_to_dict(tree_node)
        tree_diff = helper.get_tree_diff(tree_node, tree_node_copy, only_diff=False)
        actual = export.tree_to_dict(tree_diff)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

        # With attributes
        expected = {
            "/a": {"name": "a"},
            "/a/b (~)": {"name": "b (~)", "age2": (None, 2)},
            "/a/b (~)/d": {"name": "d"},
            "/a/b (~)/e": {"name": "e"},
            "/a/b (~)/e/g (~)": {"name": "g (~)", "age2": (3, 4)},
            "/a/b (~)/e/h": {"name": "h"},
            "/a/c": {"name": "c"},
            "/a/c/f (~)": {"name": "f (~)", "age": (38, 48), "age2": (1, None)},
        }

        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_copy, attr_list=["age", "age2"], only_diff=False
        )
        actual = export.tree_to_dict(tree_diff, all_attrs=True)
        assert (
            actual.keys() == expected.keys()
        ), f"Expected\n{expected.keys()}\nReceived\n{actual.keys()}"
        assert math.isnan(
            actual["/a/b (~)"]["age2"][0]
        ), "Check /a/b (~) before-value for age2"
        assert actual["/a/b (~)"]["age2"][1] == 2, "Check /a/b (~) after-value for age2"
        assert (
            not actual["/a/c/f (~)"]["age2"] == 1
        ), "Check /a/c/f (~) before-value for age2"
        assert math.isnan(
            actual["/a/c/f (~)"]["age2"][1]
        ), "Check /a/c/f (~) after-value for age2"
        assert (
            actual["/a/c/f (~)"]["age"] == expected["/a/c/f (~)"]["age"]
        ), "Check /a/c/f (~) for age"

    @staticmethod
    def test_tree_diff_attributes_different_structure_different_attributes(tree_node):
        from bigtree import find_name

        tree_node_copy = tree_node.copy()
        for node_name_to_remove in ["d"]:
            node_to_remove = find_name(tree_node_copy, node_name_to_remove)
            node_to_remove.parent = None
        for node_name_to_change in ["c", "f"]:
            node_to_change = find_name(tree_node_copy, node_name_to_change)
            node_to_change.age += 10

        # Without attributes
        expected_str = "a\n" "└── b\n" "    └── d (-)\n"
        tree_diff = helper.get_tree_diff(tree_node, tree_node_copy)
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

        # With attributes
        expected = {
            "/a": {"name": "a"},
            "/a/b": {"name": "b"},
            "/a/b/d (-)": {"name": "d (-)"},
            "/a/c (~)": {"age": (60, 70.0), "name": "c (~)"},
            "/a/c (~)/f (~)": {"age": (38, 48.0), "name": "f (~)"},
        }
        tree_diff = helper.get_tree_diff(tree_node, tree_node_copy, attr_list=["age"])
        actual = export.tree_to_dict(tree_diff, all_attrs=True)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_diff_attributes_different_structure_different_attributes_all_diff(
        tree_node,
    ):
        from bigtree import find_name

        tree_node_copy = tree_node.copy()
        for node_name_to_remove in ["d"]:
            node_to_remove = find_name(tree_node_copy, node_name_to_remove)
            node_to_remove.parent = None
        for node_name_to_change in ["c", "f"]:
            node_to_change = find_name(tree_node_copy, node_name_to_change)
            node_to_change.age += 10

        # Without attributes
        expected_str = (
            "a\n"
            "├── b\n"
            "│   ├── d (-)\n"
            "│   └── e\n"
            "│       ├── g\n"
            "│       └── h\n"
            "└── c\n"
            "    └── f\n"
        )
        tree_diff = helper.get_tree_diff(tree_node, tree_node_copy, only_diff=False)
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

        # With attributes
        expected = {
            "/a": {"name": "a"},
            "/a/b": {"name": "b"},
            "/a/b/d (-)": {"name": "d (-)"},
            "/a/b/e": {"name": "e"},
            "/a/b/e/g": {"name": "g"},
            "/a/b/e/h": {"name": "h"},
            "/a/c (~)": {"age": (60, 70.0), "name": "c (~)"},
            "/a/c (~)/f (~)": {"age": (38, 48.0), "name": "f (~)"},
        }
        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_copy, only_diff=False, attr_list=["age"]
        )
        actual = export.tree_to_dict(tree_diff, all_attrs=True)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_diff_attributes_different_structure_different_attributes_all_diff_detail(
        tree_node,
    ):
        from bigtree import find_name

        tree_node_copy = tree_node.copy()
        for node_name_to_remove in ["d"]:
            node_to_remove = find_name(tree_node_copy, node_name_to_remove)
            node_to_remove.parent = None
        for node_name_to_change in ["c", "f"]:
            node_to_change = find_name(tree_node_copy, node_name_to_change)
            node_to_change.age += 10

        # Without attributes
        expected_str = (
            "a\n"
            "├── b\n"
            "│   ├── d (removed)\n"
            "│   └── e\n"
            "│       ├── g\n"
            "│       └── h\n"
            "└── c\n"
            "    └── f\n"
        )
        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_copy, only_diff=False, detail=True
        )
        assert_print_statement(export.print_tree, expected_str, tree=tree_diff)

        # With attributes
        expected = {
            "/a": {"name": "a"},
            "/a/b": {"name": "b"},
            "/a/b/d (removed)": {"name": "d (removed)"},
            "/a/b/e": {"name": "e"},
            "/a/b/e/g": {"name": "g"},
            "/a/b/e/h": {"name": "h"},
            "/a/c (~)": {"age": (60, 70.0), "name": "c (~)"},
            "/a/c (~)/f (~)": {"age": (38, 48.0), "name": "f (~)"},
        }
        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_copy, only_diff=False, detail=True, attr_list=["age"]
        )
        actual = export.tree_to_dict(tree_diff, all_attrs=True)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_diff_attributes_invalid_attribute(tree_node):
        from bigtree import find_name

        tree_node_copy = tree_node.copy()
        for node_name_to_remove in ["d"]:
            node_to_remove = find_name(tree_node_copy, node_name_to_remove)
            node_to_remove.parent = None
        for node_name_to_change in ["c", "f"]:
            node_to_change = find_name(tree_node_copy, node_name_to_change)
            node_to_change.age += 10

        # With attributes
        expected = {
            "/a": {"name": "a"},
            "/a/b": {"name": "b"},
            "/a/b/d (-)": {"name": "d (-)"},
            "/a/b/e": {"name": "e"},
            "/a/b/e/g": {"name": "g"},
            "/a/b/e/h": {"name": "h"},
            "/a/c": {"name": "c"},
            "/a/c/f": {"name": "f"},
        }
        tree_diff = helper.get_tree_diff(
            tree_node, tree_node_copy, only_diff=False, attr_list=["age2"]
        )
        actual = export.tree_to_dict(tree_diff)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

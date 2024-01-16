import math

import pytest

from bigtree import print_tree, tree_to_dict
from bigtree.node.basenode import BaseNode
from bigtree.node.node import Node
from bigtree.tree.helper import clone_tree, get_tree_diff, prune_tree
from bigtree.utils.exceptions import NotFoundError, SearchError
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
            clone_tree({}, Node)
        assert str(exc_info.value) == Constants.ERROR_NODE_TYPE.format(type="BaseNode")

    @staticmethod
    def test_clone_tree_basenode_node(tree_basenode):
        root_clone = clone_tree(tree_basenode, node_type=Node)
        assert isinstance(root_clone, Node), "Wrong type returned"
        assert_tree_structure_basenode_root(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)

    @staticmethod
    def test_clone_tree_node_basenode(tree_node):
        root_clone = clone_tree(tree_node, node_type=BaseNode)
        assert isinstance(root_clone, BaseNode), "Wrong type returned"
        assert_tree_structure_basenode_root(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)

    @staticmethod
    def test_clone_tree_basenode_custom(tree_basenode):
        class NodeA(Node):
            pass

        root_clone = clone_tree(tree_basenode, node_type=NodeA)
        assert isinstance(root_clone, NodeA), Constants.ERROR_CUSTOM_TYPE.format(
            type="NodeA"
        )
        assert_tree_structure_basenode_root(root_clone)
        assert_tree_structure_basenode_root_attr(root_clone)


class TestPruneTree:
    @staticmethod
    def test_prune_tree(tree_node):
        # Pruned tree is a/b/d, a/b/e/g, a/b/e/h
        tree_prune = prune_tree(tree_node, "a/b")

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 2
        assert len(tree_prune.children[0].children[0].children) == 0
        assert len(tree_prune.children[0].children[1].children) == 2

    @staticmethod
    def test_prune_tree_exact(tree_node):
        # Pruned tree is a/b/e/g
        tree_prune = prune_tree(tree_node, "a/b/e/g", exact=True)

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 1
        assert len(tree_prune.children[0].children[0].children) == 1

    @staticmethod
    def test_prune_tree_list(tree_node):
        # Pruned tree is a/b/d, a/b/e/g, a/b/e/h
        tree_prune = prune_tree(tree_node, ["a/b/d", "a/b/e/g", "a/b/e/h"])

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 2
        assert len(tree_prune.children[0].children[0].children) == 0
        assert len(tree_prune.children[0].children[1].children) == 2

    @staticmethod
    def test_prune_tree_path_and_depth(tree_node):
        # Pruned tree is a/b/d, a/b/e (a/b/e/g, a/b/e/h pruned away)
        tree_prune = prune_tree(tree_node, "a/b", max_depth=3)

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
        tree_prune = prune_tree(tree_node, ["a/b/d", "a/b/e/g", "a/b/e/h"], max_depth=3)

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
        tree_prune = prune_tree(
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
        tree_prune = prune_tree(tree_node, max_depth=2)

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
        tree_prune = prune_tree(tree_node, "a/c")

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 1

    @staticmethod
    def test_prune_tree_multiple_path_error(tree_node):
        dd = Node("d")
        dd.parent = tree_node.children[-1]
        with pytest.raises(SearchError) as exc_info:
            prune_tree(tree_node, "d")
        assert str(exc_info.value).startswith(
            Constants.ERROR_SEARCH_LESS_THAN_N_ELEMENT.format(count=1)
        )

    @staticmethod
    def test_prune_tree_nonexistant_path_error(tree_node):
        prune_path = "i"
        with pytest.raises(NotFoundError) as exc_info:
            prune_tree(tree_node, prune_path)
        assert str(exc_info.value) == Constants.ERROR_NODE_PRUNE_NOT_FOUND.format(
            prune_path=prune_path
        )

    @staticmethod
    def test_prune_tree_sep(tree_node):
        # Pruned tree is a/c/f
        tree_prune = prune_tree(tree_node, "a\\c", sep="\\")

        assert_tree_structure_basenode_root(tree_node)
        assert_tree_structure_basenode_root_attr(tree_node)
        assert len(list(tree_prune.children)) == 1
        assert len(tree_prune.children[0].children) == 1

    @staticmethod
    def test_prune_tree_sep_error(tree_node):
        prune_path = "a\\c"
        with pytest.raises(NotFoundError) as exc_info:
            prune_tree(tree_node, prune_path)
        assert str(exc_info.value) == Constants.ERROR_NODE_PRUNE_NOT_FOUND.format(
            prune_path=prune_path
        )

    @staticmethod
    def test_prune_tree_no_arg_error(tree_node):
        with pytest.raises(ValueError) as exc_info:
            prune_tree(tree_node)
        assert str(exc_info.value) == Constants.ERROR_NODE_PRUNE_ARGUMENT


class TestTreeDiff:
    @staticmethod
    def test_tree_diff(tree_node):
        other_tree_node = prune_tree(tree_node, "a/c")
        _ = Node("d", parent=other_tree_node)
        tree_only_diff = get_tree_diff(tree_node, other_tree_node)
        expected_str = (
            "a\n"
            "├── b (-)\n"
            "│   ├── d (-)\n"
            "│   └── e (-)\n"
            "│       ├── g (-)\n"
            "│       └── h (-)\n"
            "└── d (+)\n"
        )
        assert_print_statement(print_tree, expected_str, tree=tree_only_diff)

    @staticmethod
    def test_tree_diff_diff_sep(tree_node):
        other_tree_node = prune_tree(tree_node, "a/c")
        _ = Node("d", parent=other_tree_node)
        other_tree_node.sep = "-"
        tree_only_diff = get_tree_diff(tree_node, other_tree_node)
        expected_str = (
            "a\n"
            "├── b (-)\n"
            "│   ├── d (-)\n"
            "│   └── e (-)\n"
            "│       ├── g (-)\n"
            "│       └── h (-)\n"
            "└── d (+)\n"
        )
        assert_print_statement(print_tree, expected_str, tree=tree_only_diff)

    @staticmethod
    def test_tree_diff_all_diff(tree_node):
        other_tree_node = prune_tree(tree_node, "a/c")
        _ = Node("d", parent=other_tree_node)
        tree_diff = get_tree_diff(tree_node, other_tree_node, only_diff=False)
        expected_str = (
            "a\n"
            "├── b (-)\n"
            "│   ├── d (-)\n"
            "│   └── e (-)\n"
            "│       ├── g (-)\n"
            "│       └── h (-)\n"
            "├── c\n"
            "│   └── f\n"
            "└── d (+)\n"
        )
        assert_print_statement(print_tree, expected_str, tree=tree_diff)

    @staticmethod
    def test_tree_diff_new_leaf(tree_node):
        other_tree_node = tree_node.copy()
        tree_node_new_parent = other_tree_node["c"]["f"]
        _ = Node("i", parent=tree_node_new_parent)
        tree_only_diff = get_tree_diff(tree_node, other_tree_node)
        expected_str = "a\n" "└── c\n" "    └── f\n" "        └── i (+)\n"
        assert_print_statement(print_tree, expected_str, tree=tree_only_diff)

    @staticmethod
    def test_tree_diff_new_leaf_all_diff(tree_node):
        other_tree_node = tree_node.copy()
        tree_node_new_parent = other_tree_node["c"]["f"]
        _ = Node("i", parent=tree_node_new_parent)
        tree_only_diff = get_tree_diff(tree_node, other_tree_node, only_diff=False)
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
        assert_print_statement(print_tree, expected_str, tree=tree_only_diff)

    @staticmethod
    def test_tree_diff_same_tree(tree_node):
        expected = None
        actual = get_tree_diff(tree_node, tree_node)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_diff_same_tree_all_diff(tree_node):
        expected = tree_to_dict(tree_node)
        tree_diff = get_tree_diff(tree_node, tree_node, only_diff=False)
        actual = tree_to_dict(tree_diff)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_diff_attributes_same_structure_different_attributes(tree_node):
        tree_node_copy = tree_node.copy()
        tree_node_copy["c"]["f"].age += 10
        tree_node_copy["b"].age += 10

        # Without attributes
        expected = None
        actual = get_tree_diff(tree_node, tree_node_copy)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

        # With attributes
        expected = {
            "/a": {"name": "a"},
            "/a/b (~)": {"name": "b (~)", "age": (65, 75)},
            "/a/c": {"name": "c"},
            "/a/c/f (~)": {"name": "f (~)", "age": (38, 48)},
        }

        tree_diff = get_tree_diff(tree_node, tree_node_copy, attr_list=["age"])
        actual = tree_to_dict(tree_diff, all_attrs=True)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_diff_attributes_same_structure_different_attributes_all_diff(
        tree_node,
    ):
        tree_node_copy = tree_node.copy()
        tree_node_copy["c"]["f"].age += 10
        tree_node_copy["b"].age += 10

        # Without attributes
        expected = tree_to_dict(tree_node)
        tree_diff = get_tree_diff(tree_node, tree_node_copy, only_diff=False)
        actual = tree_to_dict(tree_diff)
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

        tree_diff = get_tree_diff(
            tree_node, tree_node_copy, attr_list=["age"], only_diff=False
        )
        actual = tree_to_dict(tree_diff, all_attrs=True)
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
        actual = get_tree_diff(tree_node, tree_node_copy)
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

        tree_diff = get_tree_diff(tree_node, tree_node_copy, attr_list=["age", "age2"])
        actual = tree_to_dict(tree_diff, all_attrs=True)
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
        expected = tree_to_dict(tree_node)
        tree_diff = get_tree_diff(tree_node, tree_node_copy, only_diff=False)
        actual = tree_to_dict(tree_diff)
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

        tree_diff = get_tree_diff(
            tree_node, tree_node_copy, attr_list=["age", "age2"], only_diff=False
        )
        actual = tree_to_dict(tree_diff, all_attrs=True)
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
        tree_diff = get_tree_diff(tree_node, tree_node_copy)
        assert_print_statement(print_tree, expected_str, tree=tree_diff)

        # With attributes
        expected = {
            "/a": {"name": "a"},
            "/a/b": {"name": "b"},
            "/a/b/d (-)": {"name": "d (-)"},
            "/a/c (~)": {"age": (60, 70.0), "name": "c (~)"},
            "/a/c (~)/f (~)": {"age": (38, 48.0), "name": "f (~)"},
        }
        tree_diff = get_tree_diff(tree_node, tree_node_copy, attr_list=["age"])
        actual = tree_to_dict(tree_diff, all_attrs=True)
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
        tree_diff = get_tree_diff(tree_node, tree_node_copy, only_diff=False)
        assert_print_statement(print_tree, expected_str, tree=tree_diff)

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
        tree_diff = get_tree_diff(
            tree_node, tree_node_copy, only_diff=False, attr_list=["age"]
        )
        actual = tree_to_dict(tree_diff, all_attrs=True)
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
        tree_diff = get_tree_diff(
            tree_node, tree_node_copy, only_diff=False, attr_list=["age2"]
        )
        actual = tree_to_dict(tree_diff)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

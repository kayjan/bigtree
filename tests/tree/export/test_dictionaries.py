from bigtree.tree import export
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
)
from tests.node.test_node import assert_tree_structure_node_root


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
        actual = export.tree_to_dict(tree_node)
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
        actual = export.tree_to_dict(tree_node, name_key="")
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
        actual = export.tree_to_dict(tree_node, name_key="NAME")
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
        actual = export.tree_to_dict(tree_node, parent_key="PARENT")
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
        actual = export.tree_to_dict(tree_node, attr_dict={"age": "AGE"})
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
        actual = export.tree_to_dict(tree_node, all_attrs=True)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_max_depth(tree_node):
        expected = {
            "/a": {"name": "a"},
            "/a/b": {"name": "b"},
            "/a/c": {"name": "c"},
        }
        actual = export.tree_to_dict(tree_node, max_depth=2)
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
        actual = export.tree_to_dict(tree_node, skip_depth=2)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_leaf_only(tree_node):
        expected = {
            "/a/b/d": {"name": "d"},
            "/a/b/e/g": {"name": "g"},
            "/a/b/e/h": {"name": "h"},
            "/a/c/f": {"name": "f"},
        }
        actual = export.tree_to_dict(tree_node, leaf_only=True)
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
        actual = export.tree_to_dict(
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
        actual = export.tree_to_dict(
            tree_node.children[0],
            name_key="NAME",
            parent_key="PARENT",
            attr_dict={"age": "AGE"},
        )
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_dict_to_tree(tree_node):
        from bigtree.tree.construct import dict_to_tree

        d = export.tree_to_dict(tree_node, all_attrs=True)
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
        actual = export.tree_to_nested_dict(tree_node)
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
        actual = export.tree_to_nested_dict(tree_node, name_key="NAME")
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
        actual = export.tree_to_nested_dict(tree_node, child_key="CHILDREN")
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
        actual = export.tree_to_nested_dict(tree_node, attr_dict={"age": "AGE"})
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
        actual = export.tree_to_nested_dict(tree_node, all_attrs=True)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_max_depth(tree_node):
        expected = {"name": "a", "children": [{"name": "b"}, {"name": "c"}]}
        actual = export.tree_to_nested_dict(tree_node, max_depth=2)
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
        actual = export.tree_to_nested_dict(
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
        actual = export.tree_to_nested_dict(
            tree_node.children[0],
            name_key="NAME",
            child_key="CHILDREN",
            attr_dict={"age": "AGE"},
        )
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_tree_to_nested_dict_to_tree(tree_node):
        from bigtree.tree.construct import nested_dict_to_tree

        d = export.tree_to_nested_dict(tree_node, all_attrs=True)
        tree = nested_dict_to_tree(d)
        assert_tree_structure_basenode_root(tree)
        assert_tree_structure_basenode_root_attr(tree)
        assert_tree_structure_node_root(tree)

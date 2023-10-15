import unittest

import pytest

from bigtree.node.node import Node
from bigtree.tree.search import (
    find,
    find_attr,
    find_attrs,
    find_child,
    find_child_by_name,
    find_children,
    find_full_path,
    find_name,
    find_names,
    find_path,
    find_paths,
    find_relative_path,
    findall,
)
from bigtree.utils.exceptions import SearchError
from tests.test_constants import Constants


class TestSearch(unittest.TestCase):
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
        self.a = Node("a", age=90)
        self.b = Node("b", age=65)
        self.c = Node("c", age=60)
        self.d = Node("d", age=40)
        self.e = Node("e", age=35)
        self.f = Node("f", age=38)
        self.g = Node("g", age=10)
        self.h = Node("h", age=6)

        self.b.parent = self.a
        self.c.parent = self.a
        self.d.parent = self.b
        self.e.parent = self.b
        self.f.parent = self.c
        self.g.parent = self.e
        self.h.parent = self.e

    def tearDown(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None

    def test_find_all(self):
        actual = findall(self.a, lambda node: node.age >= 60)
        expected = (self.a, self.b, self.c)
        assert (
            actual == expected
        ), f"Expected find_all to return {expected}, received {actual}"

        actual = findall(self.a, lambda node: node.age >= 30)
        expected = (self.a, self.b, self.d, self.e, self.c, self.f)
        assert (
            actual == expected
        ), f"Expected find_all to return {expected}, received {actual}"

    def test_find_all_descendant(self):
        actual = findall(self.b, lambda node: node.age >= 60)
        expected = (self.b,)
        assert (
            actual == expected
        ), f"Expected find_all to return {expected}, received {actual}"

    def test_find_all_max_depth(self):
        actual = findall(self.a, lambda node: node.age >= 30, max_depth=2)
        expected = (self.a, self.b, self.c)
        assert (
            actual == expected
        ), f"Expected find_all to return {expected}, received {actual}"

    def test_find_all_max_count_error(self):
        with pytest.raises(SearchError) as exc_info:
            findall(self.a, lambda node: node.age >= 30, max_depth=2, max_count=2)
        assert str(exc_info.value).startswith(
            Constants.ERROR_SEARCH_LESS_THAN_N_ELEMENT.format(count=2)
        )

    def test_find_all_min_count_error(self):
        with pytest.raises(SearchError) as exc_info:
            findall(self.a, lambda node: node.age >= 30, max_depth=2, min_count=4)
        assert str(exc_info.value).startswith(
            Constants.ERROR_SEARCH_MORE_THAN_N_ELEMENT.format(count=4)
        )

    def test_find(self):
        actual = find(self.a, lambda node: node.age == 60)
        expected = self.c
        assert (
            actual == expected
        ), f"Expected find to return {expected}, received {actual}"

        actual = find(self.a, lambda node: node.age == 5)
        expected = None
        assert (
            actual == expected
        ), f"Expected find to return {expected}, received {actual}"

    def test_find_descendant(self):
        actual = find(self.b, lambda node: node.age == 60)
        expected = None
        assert (
            actual == expected
        ), f"Expected find to return {expected}, received {actual}"

    def test_find_error(self):
        with pytest.raises(SearchError) as exc_info:
            find(self.a, lambda node: node.age > 5)
        assert str(exc_info.value).startswith(
            Constants.ERROR_SEARCH_LESS_THAN_N_ELEMENT.format(count=1)
        )

    def test_find_name(self):
        inputs = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        expected_ans = [
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
            None,
        ]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_name(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_names(self):
        inputs = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        expected_ans = [
            (self.a,),
            (self.b,),
            (self.c,),
            (self.d,),
            (self.e,),
            (self.f,),
            (self.g,),
            (self.h,),
            (),
        ]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_names(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_names to return {expected}, received {actual}"

    def test_find_relative_path_current_position(self):
        nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for node in nodes:
            expected = node
            actual = find_relative_path(node, ".")
            assert actual == (
                expected,
            ), f"Expected find_relative_path to return {expected}, received {actual}"

    def test_find_relative_path_current_position_multiple(self):
        nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for node in nodes:
            expected = node
            actual = find_relative_path(node, "./././././.")
            assert actual == (
                expected,
            ), f"Expected find_relative_path to return {expected}, received {actual}"

    def test_find_relative_path_parent_position(self):
        inputs = [self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        expected_ans = [self.a, self.a, self.b, self.b, self.c, self.e, self.e]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_relative_path(input_, "..")
            assert actual == (
                expected,
            ), f"Expected find_relative_path to return {expected}, received {actual}"

    def test_find_relative_path_wildcard(self):
        inputs = ["*", "b/*", "c/*", "b/e/*"]
        expected_ans = [
            (self.b, self.c),
            (self.d, self.e),
            (self.f,),
            (self.g, self.h),
        ]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_relative_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_relative_path to return {expected}, received {actual}"

    def test_find_relative_path_wildcard_parent_path(self):
        h2 = self.h.copy()
        h2.parent = self.f
        inputs_list = [
            (self.a, ["b/*/g", "*/f", "*/*/h"]),
            (self.b, ["*/g", "../*/f", "../*/*/h"]),
        ]
        expected_ans = [
            (self.g,),
            (self.f,),
            (self.h, h2),
        ]
        for inputs in inputs_list:
            for input_, expected in zip(inputs[1], expected_ans):
                actual = find_relative_path(inputs[0], input_)
                assert (
                    actual == expected
                ), f"Expected find_relative_path to return {expected}, received {actual}"

    def test_find_relative_path_sep_leading(self):
        inputs = [
            "/a",
            "/a/b",
            "/a/c",
            "/a/b/d",
            "/a/b/e",
            "/a/c/f",
            "/a/b/e/g",
            "/a/b/e/h",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_relative_path(self.b, input_)
            assert actual == (
                expected,
            ), f"Expected find_relative_path to return {expected}, received {actual}"

    def test_find_relative_path_sep_trailing(self):
        inputs = [self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        expected_ans = [self.a, self.a, self.b, self.b, self.c, self.e, self.e]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_relative_path(input_, "../")
            assert actual == (
                expected,
            ), f"Expected find_relative_path to return {expected}, received {actual}"

    def test_find_relative_path_wrong_node_error(self):
        inputs = [
            ("a/e", "a"),
            ("b/f", "f"),
            ("b/e/i", "i"),
        ]
        for input_, component_ in inputs:
            with pytest.raises(SearchError) as exc_info:
                find_relative_path(self.a, input_)
            assert str(
                exc_info.value
            ) == Constants.ERROR_SEARCH_RELATIVE_INVALID_NODE.format(
                component=component_
            )

    def test_find_relative_path_wrong_path_error(self):
        inputs_list = [(self.a, ["../"]), (self.b, ["../../"])]
        for inputs in inputs_list:
            for input_ in inputs[1]:
                with pytest.raises(SearchError) as exc_info:
                    find_relative_path(inputs[0], input_)
        assert str(exc_info.value) == Constants.ERROR_SEARCH_RELATIVE_INVALID_PATH

    def test_find_full_path(self):
        inputs = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/f",
            "a/b/e/g",
            "a/b/e/h",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_full_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_full_path to return {expected}, received {actual}"

    def test_find_full_path_sep_leading(self):
        inputs = [
            "/a",
            "/a/b",
            "/a/c",
            "/a/b/d",
            "/a/b/e",
            "/a/c/f",
            "/a/b/e/g",
            "/a/b/e/h",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_full_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_full_path to return {expected}, received {actual}"

    def test_find_full_pathsep_trailing(self):
        inputs = [
            "a/",
            "a/b/",
            "a/c/",
            "a/b/d/",
            "a/b/e/",
            "a/c/f/",
            "a/b/e/g/",
            "a/b/e/h/",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_full_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_full_path to return {expected}, received {actual}"

    def test_find_full_wrong_path(self):
        inputs = [
            "a/d/",
            "a/e/",
        ]
        expected_ans = [None, None]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_full_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_full_path to return {expected}, received {actual}"

    def test_find_full_wrong_root_error(self):
        root_name = "a"
        inputs = [
            "",
            "b/d/",
            "b/",
        ]
        expected_ans = [None, None, None]
        for input_, expected in zip(inputs, expected_ans):
            with pytest.raises(ValueError) as exc_info:
                find_full_path(self.a, input_)
            assert str(
                exc_info.value
            ) == Constants.ERROR_SEARCH_FULL_PATH_INVALID_ROOT.format(
                path_name=input_, root_name=root_name
            )

    def test_find_path(self):
        inputs = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/f",
            "a/b/e/g",
            "a/b/e/h",
            "a/j",
        ]
        expected_ans = [
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
            None,
        ]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_path to return {expected}, received {actual}"

    def test_find_path_partial(self):
        inputs = ["a", "b", "c", "d", "e", "f", "g", "e/h", "i"]
        expected_ans = [
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
            None,
        ]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_path to return {expected}, received {actual}"

    def test_find_path_sep_leading(self):
        inputs = [
            "/a",
            "/a/b",
            "/a/c",
            "/a/b/d",
            "/a/b/e",
            "/a/c/f",
            "/a/b/e/g",
            "/a/b/e/h",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_path to return {expected}, received {actual}"

    def test_find_path_sep_trailing(self):
        inputs = [
            "a/",
            "a/b/",
            "a/c/",
            "a/b/d/",
            "a/b/e/",
            "a/c/f/",
            "a/b/e/g/",
            "a/b/e/h/",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_paths(self):
        inputs = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/f",
            "a/b/e/g",
            "a/b/e/h",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_paths(self.a, input_)
            assert actual == (
                expected,
            ), f"Expected find_paths to return {expected}, received {actual}"

    def test_find_paths_partial(self):
        inputs = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "e/h",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_paths(self.a, input_)
            assert actual == (
                expected,
            ), f"Expected find_paths to return {expected}, received {actual}"

    def test_find_paths_sep_leading(self):
        inputs = [
            "/a",
            "/a/b",
            "/a/c",
            "/a/b/d",
            "/a/b/e",
            "/a/c/f",
            "/a/b/e/g",
            "/a/b/e/h",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_paths(self.a, input_)
            assert actual == (
                expected,
            ), f"Expected find_paths to return {expected}, received {actual}"

    def test_find_paths_sep_trailing(self):
        inputs = [
            "a/",
            "a/b/",
            "a/c/",
            "a/b/d/",
            "a/b/e/",
            "a/c/f/",
            "a/b/e/g/",
            "a/b/e/h/",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_paths(self.a, input_)
            assert actual == (
                expected,
            ), f"Expected find_paths to return {expected}, received {actual}"

    def test_find_attr(self):
        inputs = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        expected_ans = [
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
            None,
        ]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_attr(self.a, "name", input_)
            assert (
                actual == expected
            ), f"Expected find_attr to return {expected}, received {actual}"

        inputs = [90, 65, 60, 40, 35, 38, 10, 6, 1]
        expected_ans = [
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
            None,
        ]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_attr(self.a, "age", input_)
            assert (
                actual == expected
            ), f"Expected find_attr to return {expected}, received {actual}"

    def test_find_attrs(self):
        inputs = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        expected_ans = [
            (self.a,),
            (self.b,),
            (self.c,),
            (self.d,),
            (self.e,),
            (self.f,),
            (self.g,),
            (self.h,),
            (),
        ]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_attrs(self.a, "name", input_)
            assert (
                actual == expected
            ), f"Expected find_attrs to return {expected}, received {actual}"

        inputs = [90, 65, 60, 40, 35, 38, 10, 6, 1]
        expected_ans = [
            (self.a,),
            (self.b,),
            (self.c,),
            (self.d,),
            (self.e,),
            (self.f,),
            (self.g,),
            (self.h,),
            (),
        ]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_attrs(self.a, "age", input_)
            assert (
                actual == expected
            ), f"Expected find_attrs to return {expected}, received {actual}"

    def test_find_children(self):
        inputs = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        expected_ans = [
            (self.b, self.c),
            (self.d, self.e),
            (self.f,),
            (),
            (self.g, self.h),
            (),
            (),
            (),
        ]
        for idx, input in enumerate(inputs):
            actual = find_children(input, lambda node: node.age > 1)
            expected = expected_ans[idx]
            assert (
                actual == expected
            ), f"Expected find_children to return {expected}, received {actual} for input {input}"

    def test_find_children_condition(self):
        inputs = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        expected_ans = [
            (self.b,),
            (self.e,),
            (self.f,),
            (),
            (self.g,),
            (),
            (),
            (),
        ]
        for idx, input_ in enumerate(inputs):
            actual = find_children(
                input_,
                lambda node: any(
                    node.node_name.startswith(_name) for _name in ["b", "e", "f", "g"]
                ),
            )
            expected = expected_ans[idx]
            assert (
                actual == expected
            ), f"Expected find_children to return {expected}, received {actual} for input {input}"

    def test_find_children_max_count_error(self):
        with pytest.raises(SearchError) as exc_info:
            find_children(self.a, lambda node: node.age >= 30, max_count=1)
        assert str(exc_info.value).startswith(
            Constants.ERROR_SEARCH_LESS_THAN_N_ELEMENT.format(count=1)
        )

    def test_find_children_min_count_error(self):
        with pytest.raises(SearchError) as exc_info:
            find_children(self.a, lambda node: node.age >= 30, min_count=3)
        assert str(exc_info.value).startswith(
            Constants.ERROR_SEARCH_MORE_THAN_N_ELEMENT.format(count=3)
        )

    def test_find_child(self):
        inputs = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        expected_ans = [
            self.b,
            self.e,
            self.f,
            None,
            self.g,
            None,
            None,
            None,
        ]
        for idx, input_ in enumerate(inputs):
            actual = find_child(
                input_,
                lambda node: any(
                    node.node_name.startswith(_name) for _name in ["b", "e", "f", "g"]
                ),
            )
            expected = expected_ans[idx]
            assert (
                actual == expected
            ), f"Expected find_children to return {expected}, received {actual} for input {input}"

    def test_find_child_error(self):
        with pytest.raises(SearchError) as exc_info:
            find_child(self.a, lambda node: node.age > 5)
        assert str(exc_info.value).startswith(
            Constants.ERROR_SEARCH_LESS_THAN_N_ELEMENT.format(count=1)
        )

    def test_find_child_by_name(self):
        inputs1 = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        inputs2 = ["a", "b", "c", "d", "e", "f", "g", "h"]
        expected_ans = [
            [None, self.b, self.c, None, None, None, None, None],
            [None, None, None, self.d, self.e, None, None, None],
            [None, None, None, None, None, self.f, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, self.g, self.h],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]
        for idx1, input_1 in enumerate(inputs1):
            for idx2, input_2 in enumerate(inputs2):
                actual = find_child_by_name(input_1, input_2)
                expected = expected_ans[idx1][idx2]
                assert (
                    actual == expected
                ), f"Expected find_child_by_name to return {expected}, received {actual} for inputs {input_1} and {input_2}"

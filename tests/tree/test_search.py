import unittest

import pytest

from bigtree.node.node import Node
from bigtree.tree.search import (
    find,
    find_attr,
    find_attrs,
    find_children,
    find_full_path,
    find_name,
    find_names,
    find_path,
    find_paths,
    findall,
)
from bigtree.utils.exceptions import SearchError


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

    def test_exception_find_all_max_count(self):
        with pytest.raises(SearchError):
            findall(self.a, lambda node: node.age >= 30, max_depth=2, max_count=2)

    def test_exception_find_all_min_count(self):
        with pytest.raises(SearchError):
            findall(self.a, lambda node: node.age >= 30, max_depth=2, min_count=4)

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

    def test_exception_find(self):
        with pytest.raises(SearchError):
            find(self.a, lambda node: node.age > 5)

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
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_full_path(self):
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
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_full_path_sep_leading(self):
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
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_full_pathsep_trailing(self):
        inputs = [
            "/a/",
            "/a/b/",
            "/a/c/",
            "/a/b/d/",
            "/a/b/e/",
            "/a/c/f/",
            "/a/b/e/g/",
            "/a/b/e/h/",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_full_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_full_wrong_path(self):
        inputs = [
            "/a/d/",
            "/a/e/",
        ]
        expected_ans = [None, None]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_full_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_full_wrong_root(self):
        inputs = [
            "/",
            "/b/d/",
            "/b/",
        ]
        expected_ans = [None, None, None]
        for input_, expected in zip(inputs, expected_ans):
            with pytest.raises(ValueError):
                find_full_path(self.a, input_)

    def test_find_path(self):
        inputs = [
            "/a",
            "/a/b",
            "/a/c",
            "/a/b/d",
            "/a/b/e",
            "/a/c/f",
            "/a/b/e/g",
            "/a/b/e/h",
            "/a/j",
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
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_path_partial(self):
        inputs = ["/a", "/b", "/c", "/d", "/e", "/f", "/g", "/e/h", "/i"]
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
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_path_sep_leading(self):
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
            actual = find_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_path_sep_trailing(self):
        inputs = [
            "/a/",
            "/a/b/",
            "/a/c/",
            "/a/b/d/",
            "/a/b/e/",
            "/a/c/f/",
            "/a/b/e/g/",
            "/a/b/e/h/",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_paths(self):
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
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_paths_partial(self):
        inputs = [
            "/a",
            "/b",
            "/c",
            "/d",
            "/e",
            "/f",
            "/g",
            "/e/h",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_paths(self.a, input_)
            assert actual == (
                expected,
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_paths_sep_leading(self):
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
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_paths_sep_trailing(self):
        inputs = [
            "/a/",
            "/a/b/",
            "/a/c/",
            "/a/b/d/",
            "/a/b/e/",
            "/a/c/f/",
            "/a/b/e/g/",
            "/a/b/e/h/",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = find_paths(self.a, input_)
            assert actual == (
                expected,
            ), f"Expected find_name to return {expected}, received {actual}"

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
            ), f"Expected find_attr to return {expected}, received {actual}"

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
            ), f"Expected find_attr to return {expected}, received {actual}"

    def find_children(self):
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
                actual = find_children(input_1, input_2)
                expected = expected_ans[idx1][idx2]
                assert actual == (
                    expected,
                ), f"Expected find_children to return {expected}, received {actual} for inputs {input_1} and {input_2}"

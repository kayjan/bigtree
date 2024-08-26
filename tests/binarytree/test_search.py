import unittest

from bigtree.node import binarynode
from bigtree.tree import search


class TestSearch(unittest.TestCase):
    def setUp(self):
        """
        Binary Tree should have structure
        1
        ├── 2
        │   ├── 4
        │   │   └── 8
        │   └── 5
        └── 3
            ├── 6
            └── 7
        """
        self.a = binarynode.BinaryNode(1)
        self.b = binarynode.BinaryNode(2, parent=self.a)
        self.c = binarynode.BinaryNode(3, parent=self.a)
        self.d = binarynode.BinaryNode(4, parent=self.b)
        self.e = binarynode.BinaryNode(5)
        self.f = binarynode.BinaryNode(6)
        self.g = binarynode.BinaryNode(7)
        self.h = binarynode.BinaryNode(8)
        self.d.children = [None, self.h]
        self.e.parent = self.b
        self.f.parent = self.c
        self.g.parent = self.c

    def tearDown(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None

    def test_findall(self):
        actual = search.findall(self.a, lambda node: node.val <= 3)
        expected = (self.a, self.b, self.c)
        assert (
            actual == expected
        ), f"Expected find_all to return {expected}, received {actual}"

    def test_find(self):
        actual = search.find(self.a, lambda node: node.val == 5)
        expected = self.e
        assert (
            actual == expected
        ), f"Expected find to return {expected}, received {actual}"

        actual = search.find(self.a, lambda node: node.val == 5, max_depth=2)
        assert not actual, f"Expected find to return None, received {actual}"

    def test_find_name(self):
        inputs = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
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
            actual = search.find_name(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_names(self):
        inputs = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
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
            actual = search.find_names(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_full_path(self):
        inputs = [
            "/1",
            "/1/2",
            "/1/3",
            "/1/2/4",
            "/1/2/5",
            "/1/3/6",
            "/1/3/7",
            "/1/2/4/8",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = search.find_full_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_name to return {expected}, received {actual}"

    def test_find_path(self):
        inputs = ["/1", "/2", "/3", "/4", "/5", "/6", "/7", "/8", "/9"]
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
            actual = search.find_path(self.a, input_)
            assert (
                actual == expected
            ), f"Expected find_path to return {expected}, received {actual}"

    def test_find_paths(self):
        inputs = [
            "/1",
            "/2",
            "/3",
            "/4",
            "/5",
            "/6",
            "/7",
            "/8",
        ]
        expected_ans = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        for input_, expected in zip(inputs, expected_ans):
            actual = search.find_paths(self.a, input_)
            assert actual == (
                expected,
            ), f"Expected find_paths to return {expected}, received {actual}"

    def test_find_attr(self):
        inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9]
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
            actual = search.find_attr(self.a, "val", input_)
            assert (
                actual == expected
            ), f"Expected find_attr to return {expected}, received {actual}"

    def test_find_attrs(self):
        inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9]
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
            actual = search.find_attrs(self.a, "val", input_)
            assert (
                actual == expected
            ), f"Expected find_attrs to return {expected}, received {actual}"

    def test_find_children(self):
        inputs1 = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        inputs2 = [1, 2, 3, 4, 5, 6, 7, 8]
        expected_ans = [
            [None, self.b, self.c, None, None, None, None, None],
            [None, None, None, self.d, self.e, None, None, None],
            [None, None, None, None, None, self.f, self.g, None],
            [None, None, None, None, None, None, None, self.h],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]
        for idx1, input_1 in enumerate(inputs1):
            for idx2, input_2 in enumerate(inputs2):
                actual = search.find_child_by_name(input_1, str(input_2))
                expected = expected_ans[idx1][idx2]
                assert (
                    actual == expected
                ), f"Expected find_children to return {expected}, received {actual} for inputs {input_1} and {input_2}"

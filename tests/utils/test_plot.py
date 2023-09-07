import unittest

from bigtree.node.node import Node
from bigtree.tree.construct import list_to_tree
from bigtree.utils.iterators import postorder_iter
from bigtree.utils.plot import first_pass, reingold_tilford


class TestPlotSmall(unittest.TestCase):
    def setUp(self):
        """
        Tree should have structure
        a
        """
        self.root = Node("a")

    def tearDown(self):
        self.root = None

    def test_reingold_tilford_error(self):
        expected = [
            ("a", 0, 0, 0),
        ]
        reingold_tilford(self.root)
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("mod"),
                node.get_attr("shift"),
            )
            for node in postorder_iter(self.root)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


class TestPlot(unittest.TestCase):
    def setUp(self):
        """
        Tree should have structure
        This tests the traversal of the left/right contour of a tree/subtree
        o
        ├── e
        │   ├── a
        │   └── d
        │       ├── b
        │       └── c
        ├── f
        └── n
            ├── g
            └── m
                ├── h
                ├── i
                ├── j
                ├── k
                └── l
        """
        path_list = [
            "o/e/a",
            "o/e/d/b",
            "o/e/d/c",
            "o/f",
            "o/n/g",
            "o/n/m/h",
            "o/n/m/i",
            "o/n/m/j",
            "o/n/m/k",
            "o/n/m/l",
        ]
        root = list_to_tree(path_list)
        self.root = root

    def tearDown(self):
        self.root = None

    def test_first_pass_with_separation(self):
        sibling_separation = 6
        subtree_separation = 6

        expected = [
            ("a", 0, 0, 0),
            ("b", 0, 0, 0),
            ("c", 6, 0, 0),
            ("d", 6, 3, 0),
            ("e", 3, 0, 0),
            ("f", 9, 0, 4.5),
            ("g", 0, 0, 0),
            ("h", 0, 0, 0),
            ("i", 6, 0, 0),
            ("j", 12, 0, 0),
            ("k", 18, 0, 0),
            ("l", 24, 0, 0),
            ("m", 6, -6, 0),
            ("n", 15, 12, 9),
            ("o", 13.5, 0, 0),
        ]
        first_pass(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
        )
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("mod"),
                node.get_attr("shift"),
            )
            for node in postorder_iter(self.root)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    def test_reingold_tilford(self):
        expected = [
            ("a", 0, 1),
            ("b", 0.5, 0),
            ("c", 1.5, 0),
            ("d", 1, 1),
            ("e", 0.5, 2),
            ("f", 2.25, 2),
            ("g", 3.5, 1),
            ("h", 2.5, 0),
            ("i", 3.5, 0),
            ("j", 4.5, 0),
            ("k", 5.5, 0),
            ("l", 6.5, 0),
            ("m", 4.5, 1),
            ("n", 4, 2),
            ("o", 2.25, 3),
        ]
        reingold_tilford(self.root)
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("y"),
            )
            for node in postorder_iter(self.root)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    def test_reingold_tilford_with_separation(self):
        sibling_separation = 6
        subtree_separation = 6

        expected = [
            ("a", 0, 1),
            ("b", 3, 0),
            ("c", 9, 0),
            ("d", 6, 1),
            ("e", 3, 2),
            ("f", 9 + 4.5, 2),
            ("g", 21, 1),
            ("h", 15, 0),
            ("i", 21, 0),
            ("j", 27, 0),
            ("k", 33, 0),
            ("l", 39, 0),
            ("m", 27, 1),
            ("n", 15 + 9, 2),
            ("o", 13.5, 3),
        ]
        reingold_tilford(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
        )
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("y"),
            )
            for node in postorder_iter(self.root)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    def test_reingold_tilford_with_separation_and_offset(self):
        sibling_separation = 6
        subtree_separation = 6
        x_offset = 3
        y_offset = 4

        expected = [
            ("a", 0 + x_offset, 1 + y_offset),
            ("b", 3 + x_offset, 0 + y_offset),
            ("c", 9 + x_offset, 0 + y_offset),
            ("d", 6 + x_offset, 1 + y_offset),
            ("e", 3 + x_offset, 2 + y_offset),
            ("f", 13.5 + x_offset, 2 + y_offset),
            ("g", 21 + x_offset, 1 + y_offset),
            ("h", 15 + x_offset, 0 + y_offset),
            ("i", 21 + x_offset, 0 + y_offset),
            ("j", 27 + x_offset, 0 + y_offset),
            ("k", 33 + x_offset, 0 + y_offset),
            ("l", 39 + x_offset, 0 + y_offset),
            ("m", 27 + x_offset, 1 + y_offset),
            ("n", 24 + x_offset, 2 + y_offset),
            ("o", 13.5 + x_offset, 3 + y_offset),
        ]
        reingold_tilford(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
            x_offset=x_offset,
            y_offset=y_offset,
        )
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("y"),
            )
            for node in postorder_iter(self.root)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    def test_reingold_tilford_with_separation_and_level_separation(self):
        sibling_separation = 6
        subtree_separation = 6
        level_separation = 3

        expected = [
            ("a", 0, 1 * level_separation),
            ("b", 3, 0 * level_separation),
            ("c", 9, 0 * level_separation),
            ("d", 6, 1 * level_separation),
            ("e", 3, 2 * level_separation),
            ("f", 13.5, 2 * level_separation),
            ("g", 21, 1 * level_separation),
            ("h", 15, 0 * level_separation),
            ("i", 21, 0 * level_separation),
            ("j", 27, 0 * level_separation),
            ("k", 33, 0 * level_separation),
            ("l", 39, 0 * level_separation),
            ("m", 27, 1 * level_separation),
            ("n", 24, 2 * level_separation),
            ("o", 13.5, 3 * level_separation),
        ]
        reingold_tilford(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
            level_separation=level_separation,
        )
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("y"),
            )
            for node in postorder_iter(self.root)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    def test_reingold_tilford_with_separation_and_offset_and_level_separation(self):
        sibling_separation = 6
        subtree_separation = 6
        x_offset = 3
        y_offset = 4
        level_separation = 3

        expected = [
            ("a", 0 + x_offset, 1 * level_separation + y_offset),
            ("b", 3 + x_offset, 0 * level_separation + y_offset),
            ("c", 9 + x_offset, 0 * level_separation + y_offset),
            ("d", 6 + x_offset, 1 * level_separation + y_offset),
            ("e", 3 + x_offset, 2 * level_separation + y_offset),
            ("f", 13.5 + x_offset, 2 * level_separation + y_offset),
            ("g", 21 + x_offset, 1 * level_separation + y_offset),
            ("h", 15 + x_offset, 0 * level_separation + y_offset),
            ("i", 21 + x_offset, 0 * level_separation + y_offset),
            ("j", 27 + x_offset, 0 * level_separation + y_offset),
            ("k", 33 + x_offset, 0 * level_separation + y_offset),
            ("l", 39 + x_offset, 0 * level_separation + y_offset),
            ("m", 27 + x_offset, 1 * level_separation + y_offset),
            ("n", 24 + x_offset, 2 * level_separation + y_offset),
            ("o", 13.5 + x_offset, 3 * level_separation + y_offset),
        ]
        reingold_tilford(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
            level_separation=level_separation,
            x_offset=x_offset,
            y_offset=y_offset,
        )
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("y"),
            )
            for node in postorder_iter(self.root)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


class TestPlotBig(unittest.TestCase):
    def setUp(self):
        """
        Tree should have structure
        This tests the shifting of the second subtree, which should trigger the shifting of right siblings
        z
        ├── h
        │   ├── c
        │   │   ├── a
        │   │   └── b
        │   └── g
        │       ├── d
        │       ├── e
        │       └── f
        ├── p
        │   ├── i
        │   ├── j
        │   └── o
        │       ├── k
        │       ├── l
        │       ├── m
        │       └── n
        ├── q
        ├── x
        │   ├── r
        │   ├── s
        │   ├── t
        │   ├── v
        │   │   └── u
        │   └── w
        └── y
        """
        path_list = [
            "z/h/c/a",
            "z/h/c/b",
            "z/h/g/d",
            "z/h/g/e",
            "z/h/g/f",
            "z/p/i",
            "z/p/j",
            "z/p/o/k",
            "z/p/o/l",
            "z/p/o/m",
            "z/p/o/n",
            "z/q",
            "z/x/r",
            "z/x/s",
            "z/x/t",
            "z/x/v/u",
            "z/x/w",
            "z/y",
        ]
        root = list_to_tree(path_list)
        self.root = root

    def tearDown(self):
        self.root = None

    def test_first_pass_with_separation(self):
        sibling_separation = 1
        subtree_separation = 3
        expected = [
            ("a", 0, 0, 0),
            ("b", 1, 0, 0),
            ("c", 0.5, 0, 0),
            ("d", 0, 0, 0),
            ("e", 1, 0, 0),
            ("f", 2, 0, 0),
            ("g", 1.5, 0.5, 3.5),
            ("h", 1 + 1.75, 0, 0),
            ("i", 0, 0, 0),
            ("j", 1, 0, 0),
            ("k", 0, 0, 0),
            ("l", 1, 0, 0),
            ("m", 2, 0, 0),
            ("n", 3, 0, 0),
            ("o", 2, 0.5, 0),
            ("p", 2 + 1.75, 2.75, 5.75),
            ("q", 3 + 1.75, 0, 2 * 5.75),
            ("r", 0, 0, 0),
            ("s", 1, 0, 0),
            ("t", 2, 0, 0),
            ("u", 0, 0, 0),
            ("v", 3, 3, 0),
            ("w", 4, 0, 0),
            ("x", 4 + 1.75, 3.75, 3 * 5.75),
            ("y", 5 + 1.75, 0, 4 * 5.75),
            ("z", 16.25, 0, 0),
        ]
        first_pass(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
        )
        # from bigtree import find_name
        # print(find_name(tree_node.root, "p"))
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("mod"),
                node.get_attr("shift"),
            )
            for node in postorder_iter(self.root)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    def test_reingold_tilford_with_separation_and_offset_and_level_separation(self):
        sibling_separation = 1
        subtree_separation = 3
        level_separation = 5
        x_offset = 10
        y_offset = 8

        expected = [
            ("a", 0 + x_offset, 0 * level_separation + y_offset),
            ("b", 1 + x_offset, 0 * level_separation + y_offset),
            ("c", 0.5 + x_offset, 1 * level_separation + y_offset),
            ("d", 4 + x_offset, 0 * level_separation + y_offset),
            ("e", 5 + x_offset, 0 * level_separation + y_offset),
            ("f", 6 + x_offset, 0 * level_separation + y_offset),
            ("g", 5 + x_offset, 1 * level_separation + y_offset),
            ("h", 2.75 + x_offset, 2 * level_separation + y_offset),
            ("i", 8.5 + x_offset, 1 * level_separation + y_offset),
            ("j", 9.5 + x_offset, 1 * level_separation + y_offset),
            ("k", 9 + x_offset, 0 * level_separation + y_offset),
            ("l", 10 + x_offset, 0 * level_separation + y_offset),
            ("m", 11 + x_offset, 0 * level_separation + y_offset),
            ("n", 12 + x_offset, 0 * level_separation + y_offset),
            ("o", 10.5 + x_offset, 1 * level_separation + y_offset),
            ("p", 9.5 + x_offset, 2 * level_separation + y_offset),
            ("q", 16.25 + x_offset, 2 * level_separation + y_offset),
            ("r", 21 + x_offset, 1 * level_separation + y_offset),
            ("s", 22 + x_offset, 1 * level_separation + y_offset),
            ("t", 23 + x_offset, 1 * level_separation + y_offset),
            ("u", 24 + x_offset, 0 * level_separation + y_offset),
            ("v", 24 + x_offset, 1 * level_separation + y_offset),
            ("w", 25 + x_offset, 1 * level_separation + y_offset),
            ("x", 23 + x_offset, 2 * level_separation + y_offset),
            ("y", 29.75 + x_offset, 2 * level_separation + y_offset),
            ("z", 16.25 + x_offset, 3 * level_separation + y_offset),
        ]
        reingold_tilford(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
            level_separation=level_separation,
            x_offset=x_offset,
            y_offset=y_offset,
        )
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("y"),
            )
            for node in postorder_iter(self.root)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

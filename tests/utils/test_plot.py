import unittest
from typing import Any, List

import matplotlib.pyplot as plt
import pytest

from bigtree.node import node
from bigtree.tree import construct
from bigtree.utils import iterators, plot
from tests.test_constants import Constants

LOCAL = Constants.LOCAL


class TestPlotTree(unittest.TestCase):
    def test_plot_tree_runtime_error(self):
        root = node.Node("a", children=[node.Node("b")])
        with pytest.raises(RuntimeError) as exc_info:
            plot.plot_tree(root)
        assert str(exc_info.value) == Constants.ERROR_PLOT

    def test_plot_tree_with_fig(self):
        root = node.Node("a", children=[node.Node("b"), node.Node("c")])
        plot.reingold_tilford(root)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig = plot.plot_tree(root, ax=ax)
        if LOCAL:
            fig.savefig("tests/plot.plot_tree_fig.png")
        assert isinstance(fig, plt.Figure)

    def test_plot_tree_with_fig_and_args(self):
        root = node.Node("a", children=[node.Node("b"), node.Node("c")])
        plot.reingold_tilford(root)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig = plot.plot_tree(root, "-ok", ax=ax)
        if LOCAL:
            fig.savefig("tests/plot.plot_tree_fig_and_args.png")
        assert isinstance(fig, plt.Figure)


class TestPlotNoChildren(unittest.TestCase):
    def setUp(self):
        """
        This tests the edge case when the tree does not have children

        Tree should have structure
        a
        """
        self.root = node.Node("a")

    def tearDown(self):
        self.root = None

    def test_reingold_tilford(self):
        expected = [
            ("a", 0, 0, 0),
        ]
        plot.reingold_tilford(self.root)
        assert_x_mod_shift(self.root, expected)


class TestPlotShiftLeftSibling(unittest.TestCase):
    def setUp(self):
        """
        This tests the shifting of the third subtree, which should trigger the shifting of left sibling

        Tree should have structure
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
        root = construct.list_to_tree(path_list)
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
        plot._first_pass(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
        )
        assert_x_mod_shift(self.root, expected)

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
        plot.reingold_tilford(self.root)
        assert_x_y_coordinate(self.root, expected)

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
        plot.reingold_tilford(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
        )
        assert_x_y_coordinate(self.root, expected)

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
        plot.reingold_tilford(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
            x_offset=x_offset,
            y_offset=y_offset,
        )
        assert_x_y_coordinate(self.root, expected)

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
        plot.reingold_tilford(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
            level_separation=level_separation,
        )
        assert_x_y_coordinate(self.root, expected)

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
        plot.reingold_tilford(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
            level_separation=level_separation,
            x_offset=x_offset,
            y_offset=y_offset,
        )
        assert_x_y_coordinate(self.root, expected)


class TestPlotShiftRightSibling(unittest.TestCase):
    def setUp(self):
        """
        This tests the shifting of the second subtree, which should trigger the shifting of right siblings

        Tree should have structure
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
        root = construct.list_to_tree(path_list)
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
        plot._first_pass(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
        )
        assert_x_mod_shift(self.root, expected)

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
        plot.reingold_tilford(
            self.root,
            sibling_separation=sibling_separation,
            subtree_separation=subtree_separation,
            level_separation=level_separation,
            x_offset=x_offset,
            y_offset=y_offset,
        )
        assert_x_y_coordinate(self.root, expected)


class TestPlotRelativeShift(unittest.TestCase):
    def setUp(self):
        """
        This tests the shifting of the third and fourth subtree, which should take into account relative shifting.
        This also tests for nodes that will shift multiple times

        Tree should have structure
        z
        ├── g
        │   ├── c
        │   │   ├── a
        │   │   └── b
        │   └── f
        │       ├── d
        │       └── e
        ├── h
        ├── q
        │   ├── i
        │   ├── j
        │   └── p
        │       ├── k
        │       ├── l
        │       ├── m
        │       ├── n
        │       └── o
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
            "z/g/c/a",
            "z/g/c/b",
            "z/g/f/d",
            "z/g/f/e",
            "z/h",
            "z/q/i",
            "z/q/j",
            "z/q/p/k",
            "z/q/p/l",
            "z/q/p/m",
            "z/q/p/n",
            "z/q/p/o",
            "z/x/r",
            "z/x/s",
            "z/x/t",
            "z/x/v/u",
            "z/x/w",
            "z/y",
        ]
        root = construct.list_to_tree(path_list)
        self.root = root

    def tearDown(self):
        self.root = None

    def test_first_pass(self):
        expected = [
            ("a", 0, 0, 0),
            ("b", 1, 0, 0),
            ("c", 0.5, 0, 0),
            ("d", 0, 0, 0),
            ("e", 1, 0, 0),
            ("f", 1.5, 1, 1),
            ("g", 1.5, 0, 0),
            ("h", 2.5, 0, (1.5 / 2) + (6.75 / 3)),
            ("i", 0, 0, 0),
            ("j", 1, 0, 0),
            ("k", 0, 0, 0),
            ("l", 1, 0, 0),
            ("m", 2, 0, 0),
            ("n", 3, 0, 0),
            ("o", 4, 0, 0),
            ("p", 2, 0, 0),
            ("q", 3.5, 2.5, 1.5 + (6.75 / 3 * 2)),
            ("r", 0, 0, 0),
            ("s", 1, 0, 0),
            ("t", 2, 0, 0),
            ("u", 0, 0, 0),
            ("v", 3, 3, 0),
            ("w", 4, 0, 0),
            ("x", 4.5, 2.5, (1.5 + 1.5 / 2) + 6.75),  # 6.75 shift
            ("y", 5.5, 0, (1.5 + 1.5) + (4.5 + 4.5)),  # 9 shift
            ("z", 9.5, 0, 0),  # 8 x
        ]
        plot._first_pass(self.root, sibling_separation=1, subtree_separation=1)
        assert_x_mod_shift(self.root, expected, approx=True)

    def test_reingold_tilford(self):
        expected = [
            ("a", 0, 0),
            ("b", 1, 0),
            ("c", 0.5, 1),
            ("d", 2, 0),
            ("e", 3, 0),
            ("f", 2.5, 1),
            ("g", 1.5, 2),
            ("h", 5.5, 2),
            ("i", 8.5, 1),
            ("j", 9.5, 1),
            ("k", 8.5, 0),
            ("l", 9.5, 0),
            ("m", 10.5, 0),
            ("n", 11.5, 0),
            ("o", 12.5, 0),
            ("p", 10.5, 1),
            ("q", 9.5, 2),
            ("r", 11.5, 1),
            ("s", 12.5, 1),
            ("t", 13.5, 1),
            ("u", 14.5, 0),
            ("v", 14.5, 1),
            ("w", 15.5, 1),
            ("x", 13.5, 2),
            ("y", 17.5, 2),
            ("z", 9.5, 3),
        ]
        plot.reingold_tilford(self.root)
        assert_x_y_coordinate(self.root, expected, approx=True)


class TestPlotShiftLeftRightSibling(unittest.TestCase):
    def setUp(self):
        """
        This tests the shifting of the third subtree which should trigger shifting of second and fourth subtree.

        Tree should have structure
        r
        ├── g
        │   ├── a
        │   ├── b
        │   ├── e
        │   │   ├── c
        │   │   └── d
        │   └── f
        ├── h
        ├── n
        │   ├── k
        │   │   ├── i
        │   │   └── j
        │   ├── l
        │   └── m
        └── q
            ├── o
            └── p
        """
        path_list = [
            "r/g/a",
            "r/g/b",
            "r/g/e/c",
            "r/g/e/d",
            "r/g/f",
            "r/h",
            "r/n/k/i",
            "r/n/k/j",
            "r/n/l",
            "r/n/m",
            "r/q/o",
            "r/q/p",
        ]
        root = construct.list_to_tree(path_list)
        self.root = root

    def tearDown(self):
        self.root = None

    def test_first_pass(self):
        expected = [
            ("a", 0, 0, 0),
            ("b", 1, 0, 0),
            ("c", 0, 0, 0),
            ("d", 1, 0, 0),
            ("e", 2, 1.5, 0),
            ("f", 3, 0, 0),
            ("g", 1.5, 0, 0),
            ("h", 2.5, 0, (1.5 / 2) + (2.25 / 3)),
            ("i", 0, 0, 0),
            ("j", 1, 0, 0),
            ("k", 0.5, 0, 0),
            ("l", 1.5, 0, 0),
            ("m", 2.5, 0, 0),
            ("n", 3.5, 2, 1.5 + (2.25 / 3 * 2)),
            ("o", 0, 0, 0),
            ("p", 1, 0, 0),
            ("q", 4.5, 4, (1.5 + 1.5 / 2) + 2.25),
            ("r", 5.25, 0, 0),
        ]
        plot._first_pass(self.root, sibling_separation=1, subtree_separation=1)
        assert_x_mod_shift(self.root, expected, approx=True)

    def test_reingold_tilford(self):
        expected = [
            ("a", 0, 1),
            ("b", 1, 1),
            ("c", 1.5, 0),
            ("d", 2.5, 0),
            ("e", 2, 1),
            ("f", 3, 1),
            ("g", 1.5, 2),
            ("h", 4, 2),
            ("i", 5, 0),
            ("j", 6, 0),
            ("k", 5.5, 1),
            ("l", 6.5, 1),
            ("m", 7.5, 1),
            ("n", 6.5, 2),
            ("o", 8.5, 1),
            ("p", 9.5, 1),
            ("q", 9, 2),
            ("r", 5.25, 3),
        ]
        plot.reingold_tilford(self.root)
        assert_x_y_coordinate(self.root, expected, approx=True)


class TestPlotNonNegative(unittest.TestCase):
    def setUp(self):
        """
        This tests the leftmost node having negative x-coordinates and the third pass will have to adjust the tree accordingly.

        Tree should have structure
        m
        ├── a
        ├── b
        ├── k
        │   ├── c
        │   ├── d
        │   ├── g
        │   │   ├── e
        │   │   └── f
        │   ├── h
        │   ├── i
        │   └── j
        └── l
        """
        path_list = [
            "m/a",
            "m/b",
            "m/k/c",
            "m/k/d",
            "m/k/g/e",
            "m/k/g/f",
            "m/k/h",
            "m/k/i",
            "m/k/j",
            "m/l",
        ]
        root = construct.list_to_tree(path_list)
        self.root = root

    def tearDown(self):
        self.root = None

    def test_first_pass(self):
        expected = [
            ("a", 0, 0, 0),
            ("b", 1, 0, 0),
            ("c", 0, 0, 0),
            ("d", 1, 0, 0),
            ("e", 0, 0, 0),
            ("f", 1, 0, 0),
            ("g", 2, 1.5, 0),
            ("h", 3, 0, 0),
            ("i", 4, 0, 0),
            ("j", 5, 0, 0),
            ("k", 2, -0.5, 0),
            ("l", 3, 0, 0),
            ("m", 1.5, 0, 0),
        ]
        plot._first_pass(self.root, sibling_separation=1, subtree_separation=1)
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("mod"),
                node.get_attr("shift"),
            )
            for node in iterators.postorder_iter(self.root)
        ]
        for _actual, _expected in zip(actual, expected):
            assert _actual == pytest.approx(
                _expected, abs=0.1
            ), f"Expected\n{_expected}\nReceived\n{_actual}"

    def test_reingold_tilford(self):
        expected = [
            ("a", 0 + 0.5, 2),
            ("b", 1 + 0.5, 2),
            ("c", -0.5 + 0.5, 1),
            ("d", 0.5 + 0.5, 1),
            ("e", 1 + 0.5, 0),
            ("f", 2 + 0.5, 0),
            ("g", 1.5 + 0.5, 1),
            ("h", 2.5 + 0.5, 1),
            ("i", 3.5 + 0.5, 1),
            ("j", 4.5 + 0.5, 1),
            ("k", 2 + 0.5, 2),
            ("l", 3 + 0.5, 2),
            ("m", 1.5 + 0.5, 3),
        ]
        plot.reingold_tilford(self.root)
        assert_x_y_coordinate(self.root, expected, approx=True)


def assert_x_y_coordinate(tree: node.Node, expected: List[Any], approx: bool = False):
    actual = [
        (
            _node.node_name,
            _node.get_attr("x"),
            _node.get_attr("y"),
        )
        for _node in iterators.postorder_iter(tree)
    ]
    if approx:
        for _actual, _expected in zip(actual, expected):
            assert _actual == pytest.approx(
                _expected, abs=0.1
            ), f"Expected\n{_expected}\nReceived\n{_actual}"
    else:
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


def assert_x_mod_shift(tree: node.Node, expected: List[Any], approx: bool = False):
    actual = [
        (
            _node.node_name,
            _node.get_attr("x"),
            _node.get_attr("mod"),
            _node.get_attr("shift"),
        )
        for _node in iterators.postorder_iter(tree)
    ]
    if approx:
        for _actual, _expected in zip(actual, expected):
            assert _actual == pytest.approx(
                _expected, abs=0.1
            ), f"Expected\n{_expected}\nReceived\n{_actual}"
    else:
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

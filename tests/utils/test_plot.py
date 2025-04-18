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
                             ┌───┐
                             │ o │
                             └─┬─┘
               ┌───────────────┼────────────────┐
             ┌─┴─┐           ┌─┴─┐            ┌─┴─┐
             │ e │           │ f │            │ n │
             └─┬─┘           └───┘            └─┬─┘
          ┌────┴────┐                 ┌─────────┴──────────┐
        ┌─┴─┐     ┌─┴─┐             ┌─┴─┐                ┌─┴─┐
        │ a │     │ d │             │ g │                │ m │
        └───┘     └─┬─┘             └───┘                └─┬─┘
                 ┌──┴───┐                    ┌──────┬──────┼──────┬──────┐
               ┌─┴─┐  ┌─┴─┐                ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐
               │ b │  │ c │                │ h │  │ i │  │ j │  │ k │  │ l │
               └───┘  └───┘                └───┘  └───┘  └───┘  └───┘  └───┘
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
                                                                         ┌───┐
                                                                         │ z │
                                                                         └─┬─┘
                      ┌──────────────────────────────────┬─────────────────┴───────────┬────────────────────┬────────────────────┐
                    ┌─┴─┐                              ┌─┴─┐                         ┌─┴─┐                ┌─┴─┐                ┌─┴─┐
                    │ h │                              │ p │                         │ q │                │ x │                │ y │
                    └─┬─┘                              └─┬─┘                         └───┘                └─┬─┘                └───┘
             ┌────────┴────────┐             ┌──────┬────┴───────────┐                        ┌──────┬──────┼──────┬──────┐
           ┌─┴─┐             ┌─┴─┐         ┌─┴─┐  ┌─┴─┐            ┌─┴─┐                    ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐
           │ c │             │ g │         │ i │  │ j │            │ o │                    │ r │  │ s │  │ t │  │ v │  │ w │
           └─┬─┘             └─┬─┘         └───┘  └───┘            └─┬─┘                    └───┘  └───┘  └───┘  └─┬─┘  └───┘
          ┌──┴───┐      ┌──────┼──────┐                    ┌──────┬──┴───┬──────┐                                  │
        ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐                ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐                              ┌─┴─┐
        │ a │  │ b │  │ d │  │ e │  │ f │                │ k │  │ l │  │ m │  │ n │                              │ u │
        └───┘  └───┘  └───┘  └───┘  └───┘                └───┘  └───┘  └───┘  └───┘                              └───┘
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
                                                                        ┌───┐
                                                                        │ z │
                                                                        └─┬─┘
                    ┌─────────────────┬────────────────────┬──────────────┴─────────────────────────────────┬────────────────────┐
                  ┌─┴─┐             ┌─┴─┐                ┌─┴─┐                                            ┌─┴─┐                ┌─┴─┐
                  │ g │             │ h │                │ q │                                            │ x │                │ y │
                  └─┬─┘             └───┘                └─┬─┘                                            └─┬─┘                └───┘
             ┌──────┴──────┐                 ┌──────┬──────┴─────────────┐                    ┌──────┬──────┼──────┬──────┐
           ┌─┴─┐         ┌─┴─┐             ┌─┴─┐  ┌─┴─┐                ┌─┴─┐                ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐
           │ c │         │ f │             │ i │  │ j │                │ p │                │ r │  │ s │  │ t │  │ v │  │ w │
           └─┬─┘         └─┬─┘             └───┘  └───┘                └─┬─┘                └───┘  └───┘  └───┘  └─┬─┘  └───┘
          ┌──┴───┐      ┌──┴───┐                           ┌──────┬──────┼──────┬──────┐                           │
        ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐                       ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐                       ┌─┴─┐
        │ a │  │ b │  │ d │  │ e │                       │ k │  │ l │  │ m │  │ n │  │ o │                       │ u │
        └───┘  └───┘  └───┘  └───┘                       └───┘  └───┘  └───┘  └───┘  └───┘                       └───┘
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
                                                   ┌───┐
                                                   │ r │
                                                   └─┬─┘
                        ┌────────────────────┬───────┴──────────┬──────────────────┐
                      ┌─┴─┐                ┌─┴─┐              ┌─┴─┐              ┌─┴─┐
                      │ g │                │ h │              │ n │              │ q │
                      └─┬─┘                └───┘              └─┬─┘              └─┬─┘
          ┌──────┬──────┴──┬──────────┐                ┌────────┴─┬──────┐      ┌──┴───┐
        ┌─┴─┐  ┌─┴─┐     ┌─┴─┐      ┌─┴─┐            ┌─┴─┐      ┌─┴─┐  ┌─┴─┐  ┌─┴─┐  ┌─┴─┐
        │ a │  │ b │     │ e │      │ f │            │ k │      │ l │  │ m │  │ o │  │ p │
        └───┘  └───┘     └─┬─┘      └───┘            └─┬─┘      └───┘  └───┘  └───┘  └───┘
                        ┌──┴───┐                    ┌──┴───┐
                      ┌─┴─┐  ┌─┴─┐                ┌─┴─┐  ┌─┴─┐
                      │ c │  │ d │                │ i │  │ j │
                      └───┘  └───┘                └───┘  └───┘
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
                                       ┌───┐
                                       │ m │
                                       └─┬─┘
          ┌──────┬───────────────────────┴───┬───────────────────────────┐
        ┌─┴─┐  ┌─┴─┐                       ┌─┴─┐                       ┌─┴─┐
        │ a │  │ b │                       │ k │                       │ l │
        └───┘  └───┘                       └─┬─┘                       └───┘
                        ┌──────┬─────────┬───┴──────┬──────┬──────┐
                      ┌─┴─┐  ┌─┴─┐     ┌─┴─┐      ┌─┴─┐  ┌─┴─┐  ┌─┴─┐
                      │ c │  │ d │     │ g │      │ h │  │ i │  │ j │
                      └───┘  └───┘     └─┬─┘      └───┘  └───┘  └───┘
                                      ┌──┴───┐
                                    ┌─┴─┐  ┌─┴─┐
                                    │ e │  │ f │
                                    └───┘  └───┘
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


class TestPlotTreeCumulativeShift(unittest.TestCase):
    def setUp(self):
        """
        This tests when the left sub_tree need to take into account the cumulative would-be shift to calculate new_shift.

        Tree should have structure
                                                                                                          ┌───┐
                                                                                                          │ a │
                                                                                                          └─┬─┘
                          ┌────────────────────────────┬──────────────────────────────────────────────┬─────┴──────────────────────────────────────────────────────────────────────────────────┐
                        ┌─┴─┐                        ┌─┴─┐                                          ┌─┴─┐                                                                                    ┌─┴─┐
                        │ b │                        │ c │                                          │ d │                                                                                    │ e │
                        └─┬─┘                        └─┬─┘                                          └─┬─┘                                                                                    └─┬─┘
          ┌───────┬───────┼───────┬───────┐            │            ┌───────┬───────┬───────┬─────────┴───────────┬─────────────────────┐                              ┌───────────────────────┴──────┬─────────────────┐
        ┌─┴──┐  ┌─┴──┐  ┌─┴──┐  ┌─┴──┐  ┌─┴──┐       ┌─┴──┐       ┌─┴──┐  ┌─┴──┐  ┌─┴──┐  ┌─┴──┐                ┌─┴──┐                ┌─┴──┐                         ┌─┴──┐                         ┌─┴──┐            ┌─┴──┐
        │ b1 │  │ b2 │  │ b3 │  │ b4 │  │ b5 │       │ c1 │       │ d1 │  │ d2 │  │ d3 │  │ d4 │                │ d5 │                │ d6 │                         │ e1 │                         │ e2 │            │ e3 │
        └────┘  └────┘  └────┘  └────┘  └────┘       └─┬──┘       └────┘  └────┘  └────┘  └────┘                └─┬──┘                └────┘                         └─┬──┘                         └────┘            └─┬──┘
                                                   ┌───┴────┐                                        ┌────────┬───┴────┬────────┐                ┌────────┬────────┬───┴────┬────────┬────────┐                ┌────────┼────────┐
                                                ┌──┴──┐  ┌──┴──┐                                  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐          ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐          ┌──┴──┐  ┌──┴──┐  ┌──┴──┐
                                                │ c11 │  │ c12 │                                  │ d51 │  │ d52 │  │ d53 │  │ d54 │          │ e11 │  │ e12 │  │ e13 │  │ e14 │  │ e15 │  │ e16 │          │ e31 │  │ e32 │  │ e33 │
                                                └─────┘  └─────┘                                  └─────┘  └─────┘  └─────┘  └─────┘          └─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘          └─────┘  └─────┘  └─────┘
        """
        path_list = [
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
            "a/d/d5/d54",  # left subtree
            "a/d/d6",
            "a/e/e1/e11",  # right subtree
            "a/e/e1/e12",
            "a/e/e1/e13",
            "a/e/e1/e14",
            "a/e/e1/e15",
            "a/e/e1/e16",
            "a/e/e2",
            "a/e/e3/e31",
            "a/e/e3/e32",
            "a/e/e3/e33",
        ]
        root = construct.list_to_tree(path_list)
        self.root = root

    def tearDown(self):
        self.root = None

    def test_first_pass(self):
        expected = [
            ("b1", 0.0, 0.0, 0.0),
            ("b2", 1.0, 0.0, 0.0),
            ("b3", 2.0, 0.0, 0.0),
            ("b4", 3.0, 0.0, 0.0),
            ("b5", 4.0, 0.0, 0.0),
            ("b", 2.0, 0.0, 0.0),
            ("c11", 0.0, 0.0, 0.0),
            ("c12", 1.0, 0.0, 0.0),
            ("c1", 0.5, 0.0, 0.0),
            ("c", 3.0, 2.5, 7.75),
            ("d1", 0.0, 0.0, 0.0),
            ("d2", 1.0, 0.0, 0.0),
            ("d3", 2.0, 0.0, 0.0),
            ("d4", 3.0, 0.0, 0.0),
            ("d51", 0.0, 0.0, 0.0),
            ("d52", 1.0, 0.0, 0.0),
            ("d53", 2.0, 0.0, 0.0),
            ("d54", 3.0, 0.0, 0.0),
            ("d5", 4.0, 2.5, 0.0),
            ("d6", 5.0, 0.0, 0.0),
            ("d", 4.0, 1.5, 15.5),
            ("e11", 0.0, 0.0, 0.0),
            ("e12", 1.0, 0.0, 0.0),
            ("e13", 2.0, 0.0, 0.0),
            ("e14", 3.0, 0.0, 0.0),
            ("e15", 4.0, 0.0, 0.0),
            ("e16", 5.0, 0.0, 0.0),
            ("e1", 2.5, 0.0, 0.0),
            ("e2", 3.5, 0.0, 1.25),
            ("e31", 0.0, 0.0, 0.0),
            ("e32", 1.0, 0.0, 0.0),
            ("e33", 2.0, 0.0, 0.0),
            ("e3", 4.5, 3.5, 2.5),
            ("e", 5.0, 0.25, 23.25),
            ("a", 15.125, 0.0, 0.0),
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
            ("b1", 0.0, 1.0),
            ("b2", 1.0, 1.0),
            ("b3", 2.0, 1.0),
            ("b4", 3.0, 1.0),
            ("b5", 4.0, 1.0),
            ("b", 2.0, 2.0),
            ("c11", 10.25, 0.0),
            ("c12", 11.25, 0.0),
            ("c1", 10.75, 1.0),
            ("c", 10.75, 2.0),
            ("d1", 17.0, 1.0),
            ("d2", 18.0, 1.0),
            ("d3", 19.0, 1.0),
            ("d4", 20.0, 1.0),
            ("d51", 19.5, 0.0),
            ("d52", 20.5, 0.0),
            ("d53", 21.5, 0.0),
            ("d54", 22.5, 0.0),
            ("d5", 21.0, 1.0),
            ("d6", 22.0, 1.0),
            ("d", 19.5, 2.0),
            ("e11", 23.5, 0.0),
            ("e12", 24.5, 0.0),
            ("e13", 25.5, 0.0),
            ("e14", 26.5, 0.0),
            ("e15", 27.5, 0.0),
            ("e16", 28.5, 0.0),
            ("e1", 26, 1.0),
            ("e2", 28.25, 1.0),
            ("e31", 29.5, 0.0),
            ("e32", 30.5, 0.0),
            ("e33", 31.5, 0.0),
            ("e3", 30.5, 1.0),
            ("e", 28.25, 2.0),
            ("a", 15.125, 3.0),
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

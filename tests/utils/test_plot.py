import unittest

from bigtree.tree.construct import list_to_tree
from bigtree.utils.iterators import preorder_iter
from bigtree.utils.plot import first_pass, reingold_tilford, second_pass


class TestPlot(unittest.TestCase):
    def setUp(self):
        """
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
        root = list_to_tree(path_list)
        self.root = root

    def tearDown(self):
        self.root = None

    def test_first_pass(self):
        expected = [
            ("o", 0, 0),
            ("e", 3, 0),
            ("a", 0, 0),
            ("d", 6, 3),
            ("b", 0, 0),
            ("c", 6, 0),
            ("f", 9, 0),
            ("n", 15, 12),
            ("g", 0, 0),
            ("m", 6, -6),
            ("h", 0, 0),
            ("i", 6, 0),
            ("j", 12, 0),
            ("k", 18, 0),
            ("l", 24, 0),
        ]
        first_pass(self.root, sibling_separation=6)
        actual = [
            (node.node_name, node.get_attr("x"), node.get_attr("mod"))
            for node in preorder_iter(self.root)
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    def test_second_pass(self):
        expected = [
            ("o", 0, 0),
            ("e", 3, 0),
            ("a", 0, 0),
            ("d", 6, 3),
            ("b", 0, 0),
            ("c", 6, 0),
            ("f", 9 + 4.5, 4.5),  # updated
            ("n", 15 + 9, 12 + 9),  # updated
            ("g", 0, 0),
            ("m", 6, -6),
            ("h", 0, 0),
            ("i", 6, 0),
            ("j", 12, 0),
            ("k", 18, 0),
            ("l", 24, 0),
        ]
        first_pass(self.root, sibling_separation=6)
        second_pass(self.root, subtree_separation=6)
        actual = [
            (node.node_name, node.get_attr("x"), node.get_attr("mod"))
            for node in preorder_iter(self.root)
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    def test_reingold_tilford(self):
        expected = [
            ("o", 2.25, 0, 3),
            ("e", 0.5, 0, 2),
            ("a", 0, 0, 1),
            ("d", 1, 0.5, 1),
            ("b", 0.5, 0, 0),
            ("c", 1.5, 0, 0),
            ("f", 2.25, 0.75, 2),
            ("n", 4, 1.5 + 2, 2),
            ("g", 3.5, 0, 1),
            ("m", 4.5, -1, 1),
            ("h", 2.5, 0, 0),
            ("i", 3.5, 0, 0),
            ("j", 4.5, 0, 0),
            ("k", 5.5, 0, 0),
            ("l", 6.5, 0, 0),
        ]
        reingold_tilford(self.root)
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("mod"),
                node.get_attr("y"),
            )
            for node in preorder_iter(self.root)
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    def test_reingold_tilford_with_separation(self):
        expected = [
            ("o", 13.5, 0, 3),  # updated
            ("e", 3, 0, 2),
            ("a", 0, 0, 1),
            ("d", 6, 3, 1),
            ("b", 3, 0, 0),  # updated
            ("c", 9, 0, 0),  # updated
            ("f", 9 + 4.5, 4.5, 2),
            ("n", 15 + 9, 12 + 9, 2),
            ("g", 21, 0, 1),  # updated
            ("m", 27, -6, 1),  # updated
            ("h", 15, 0, 0),  # updated
            ("i", 21, 0, 0),  # updated
            ("j", 27, 0, 0),  # updated
            ("k", 33, 0, 0),  # updated
            ("l", 39, 0, 0),  # updated
        ]
        reingold_tilford(self.root, sibling_separation=6, subtree_separation=6)
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("mod"),
                node.get_attr("y"),
            )
            for node in preorder_iter(self.root)
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    def test_reingold_tilford_with_separation_and_offset(self):
        x_offset = 3
        y_offset = 4
        expected = [
            ("o", 13.5 + x_offset, 0, 3 + y_offset),
            ("e", 3 + x_offset, 0, 2 + y_offset),
            ("a", 0 + x_offset, 0, 1 + y_offset),
            ("d", 6 + x_offset, 3, 1 + y_offset),
            ("b", 3 + x_offset, 0, 0 + y_offset),
            ("c", 9 + x_offset, 0, 0 + y_offset),
            ("f", 13.5 + x_offset, 4.5, 2 + y_offset),
            ("n", 24 + x_offset, 21, 2 + y_offset),
            ("g", 21 + x_offset, 0, 1 + y_offset),
            ("m", 27 + x_offset, -6, 1 + y_offset),
            ("h", 15 + x_offset, 0, 0 + y_offset),
            ("i", 21 + x_offset, 0, 0 + y_offset),
            ("j", 27 + x_offset, 0, 0 + y_offset),
            ("k", 33 + x_offset, 0, 0 + y_offset),
            ("l", 39 + x_offset, 0, 0 + y_offset),
        ]
        reingold_tilford(
            self.root,
            sibling_separation=6,
            subtree_separation=6,
            x_offset=x_offset,
            y_offset=y_offset,
        )
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("mod"),
                node.get_attr("y"),
            )
            for node in preorder_iter(self.root)
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    def test_reingold_tilford_with_separation_and_level_separation(self):
        level_separation = 3
        expected = [
            ("o", 13.5, 0, 3 * level_separation),
            ("e", 3, 0, 2 * level_separation),
            ("a", 0, 0, 1 * level_separation),
            ("d", 6, 3, 1 * level_separation),
            ("b", 3, 0, 0 * level_separation),
            ("c", 9, 0, 0 * level_separation),
            ("f", 13.5, 4.5, 2 * level_separation),
            ("n", 24, 21, 2 * level_separation),
            ("g", 21, 0, 1 * level_separation),
            ("m", 27, -6, 1 * level_separation),
            ("h", 15, 0, 0 * level_separation),
            ("i", 21, 0, 0 * level_separation),
            ("j", 27, 0, 0 * level_separation),
            ("k", 33, 0, 0 * level_separation),
            ("l", 39, 0, 0 * level_separation),
        ]
        reingold_tilford(
            self.root,
            sibling_separation=6,
            subtree_separation=6,
            level_separation=level_separation,
        )
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("mod"),
                node.get_attr("y"),
            )
            for node in preorder_iter(self.root)
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    def test_reingold_tilford_with_separation_and_offset_and_level_separation(self):
        x_offset = 3
        y_offset = 4
        level_separation = 3
        expected = [
            ("o", 13.5 + x_offset, 0, 3 * level_separation + y_offset),
            ("e", 3 + x_offset, 0, 2 * level_separation + y_offset),
            ("a", 0 + x_offset, 0, 1 * level_separation + y_offset),
            ("d", 6 + x_offset, 3, 1 * level_separation + y_offset),
            ("b", 3 + x_offset, 0, 0 * level_separation + y_offset),
            ("c", 9 + x_offset, 0, 0 * level_separation + y_offset),
            ("f", 13.5 + x_offset, 4.5, 2 * level_separation + y_offset),
            ("n", 24 + x_offset, 21, 2 * level_separation + y_offset),
            ("g", 21 + x_offset, 0, 1 * level_separation + y_offset),
            ("m", 27 + x_offset, -6, 1 * level_separation + y_offset),
            ("h", 15 + x_offset, 0, 0 * level_separation + y_offset),
            ("i", 21 + x_offset, 0, 0 * level_separation + y_offset),
            ("j", 27 + x_offset, 0, 0 * level_separation + y_offset),
            ("k", 33 + x_offset, 0, 0 * level_separation + y_offset),
            ("l", 39 + x_offset, 0, 0 * level_separation + y_offset),
        ]
        reingold_tilford(
            self.root,
            sibling_separation=6,
            subtree_separation=6,
            level_separation=level_separation,
            x_offset=x_offset,
            y_offset=y_offset,
        )
        actual = [
            (
                node.node_name,
                node.get_attr("x"),
                node.get_attr("mod"),
                node.get_attr("y"),
            )
            for node in preorder_iter(self.root)
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

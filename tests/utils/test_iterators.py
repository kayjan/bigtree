from bigtree.utils import iterators


class TestPreOrderIter:
    @staticmethod
    def test_preorder_iter(tree_node):
        expected = ["a", "b", "d", "e", "g", "h", "c", "f"]
        actual = [node.node_name for node in iterators.preorder_iter(tree_node)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter2(tree_node2):
        expected = ["a", "b", "d", "g", "e", "h", "i", "c", "f"]
        actual = [node.node_name for node in iterators.preorder_iter(tree_node2)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter_filter_condition(tree_node):
        expected = ["a", "d", "e", "g", "f"]
        actual = [
            node.node_name
            for node in iterators.preorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter_filter_condition_skip_level(tree_node):
        expected = ["g", "h"]
        actual = [
            node.node_name
            for node in iterators.preorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["g", "h"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter_stop_condition(tree_node):
        expected = ["a", "b", "d", "c", "f"]
        actual = [
            node.node_name
            for node in iterators.preorder_iter(
                tree_node, stop_condition=lambda x: x.node_name == "e"
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter_max_depth(tree_node):
        expected = ["a", "b", "d", "e", "c", "f"]
        actual = [
            node.node_name for node in iterators.preorder_iter(tree_node, max_depth=3)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


class TestPostOrderIter:
    @staticmethod
    def test_postorder_iter(tree_node):
        expected = ["d", "g", "h", "e", "b", "f", "c", "a"]
        actual = [node.node_name for node in iterators.postorder_iter(tree_node)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter2(tree_node2):
        expected = ["g", "d", "h", "i", "e", "b", "f", "c", "a"]
        actual = [node.node_name for node in iterators.postorder_iter(tree_node2)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter_filter_condition(tree_node):
        expected = ["d", "g", "e", "f", "a"]
        actual = [
            node.node_name
            for node in iterators.postorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter_filter_condition_skip_level(tree_node):
        expected = ["g", "h"]
        actual = [
            node.node_name
            for node in iterators.postorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["g", "h"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter_stop_condition(tree_node):
        expected = ["d", "b", "f", "c", "a"]
        actual = [
            node.node_name
            for node in iterators.postorder_iter(
                tree_node, stop_condition=lambda x: x.node_name == "e"
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter_max_depth(tree_node):
        expected = ["d", "e", "b", "f", "c", "a"]
        actual = [
            node.node_name for node in iterators.postorder_iter(tree_node, max_depth=3)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


class TestLevelOrderIter:
    @staticmethod
    def test_levelorder_iter(tree_node):
        expected = ["a", "b", "c", "d", "e", "f", "g", "h"]
        actual = [node.node_name for node in iterators.levelorder_iter(tree_node)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter2(tree_node2):
        expected = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        actual = [node.node_name for node in iterators.levelorder_iter(tree_node2)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter_filter_condition(tree_node):
        expected = ["a", "d", "e", "f", "g"]
        actual = [
            node.node_name
            for node in iterators.levelorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter_filter_condition_skip_level(tree_node):
        expected = ["g", "h"]
        actual = [
            node.node_name
            for node in iterators.levelorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["g", "h"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter_stop_condition(tree_node):
        expected = ["a", "b", "c", "d", "f"]
        actual = [
            node.node_name
            for node in iterators.levelorder_iter(
                tree_node, stop_condition=lambda x: x.node_name == "e"
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter_max_depth(tree_node):
        expected = ["a", "b", "c", "d", "e", "f"]
        actual = [
            node.node_name for node in iterators.levelorder_iter(tree_node, max_depth=3)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


class TestLevelOrderGroupIter:
    @staticmethod
    def test_levelordergroup_iter(tree_node):
        expected = [["a"], ["b", "c"], ["d", "e", "f"], ["g", "h"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.levelordergroup_iter(tree_node)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter2(tree_node2):
        expected = [["a"], ["b", "c"], ["d", "e", "f"], ["g", "h", "i"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.levelordergroup_iter(tree_node2)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter_filter_condition(tree_node):
        expected = [["a"], [], ["d", "e", "f"], ["g"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.levelordergroup_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter_filter_condition_skip_level(tree_node):
        expected = [[], [], [], ["g", "h"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.levelordergroup_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["g", "h"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter_stop_condition(tree_node):
        expected = [["a"], ["b", "c"], ["d", "f"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.levelordergroup_iter(
                tree_node, stop_condition=lambda x: x.node_name == "e"
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter_max_depth(tree_node):
        expected = [["a"], ["b", "c"], ["d", "e", "f"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.levelordergroup_iter(tree_node, max_depth=3)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


class TestZigZagIter:
    @staticmethod
    def test_zigzag_iter(tree_node):
        expected = ["a", "c", "b", "d", "e", "f", "h", "g"]
        actual = [node.node_name for node in iterators.zigzag_iter(tree_node)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzag_iter2(tree_node2):
        expected = ["a", "c", "b", "d", "e", "f", "i", "h", "g"]
        actual = [node.node_name for node in iterators.zigzag_iter(tree_node2)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzag_iter_filter_condition(tree_node):
        expected = ["a", "d", "e", "f", "g"]
        actual = [
            node.node_name
            for node in iterators.zigzag_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzag_iter_filter_condition_skip_level(tree_node):
        expected = ["h", "g"]
        actual = [
            node.node_name
            for node in iterators.zigzag_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["g", "h"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzag_iter_stop_condition(tree_node):
        expected = ["a", "c", "b", "d", "f"]
        actual = [
            node.node_name
            for node in iterators.zigzag_iter(
                tree_node, stop_condition=lambda x: x.node_name == "e"
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzag_iter_max_depth(tree_node):
        expected = ["a", "c", "b", "d", "e", "f"]
        actual = [
            node.node_name for node in iterators.zigzag_iter(tree_node, max_depth=3)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


class TestZigZagGroupIter:
    @staticmethod
    def test_zigzaggroup_iter(tree_node):
        expected = [["a"], ["c", "b"], ["d", "e", "f"], ["h", "g"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.zigzaggroup_iter(tree_node)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzaggroup_iter2(tree_node2):
        expected = [["a"], ["c", "b"], ["d", "e", "f"], ["i", "h", "g"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.zigzaggroup_iter(tree_node2)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzaggroup_iter_filter_condition(tree_node):
        expected = [["a"], [], ["d", "e", "f"], ["g"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.zigzaggroup_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzaggroup_iter_filter_condition_skip_level(tree_node):
        expected = [[], [], [], ["h", "g"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.zigzaggroup_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["g", "h"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzaggroup_iter_stop_condition(tree_node):
        expected = [["a"], ["c", "b"], ["d", "f"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.zigzaggroup_iter(
                tree_node, stop_condition=lambda x: x.node_name == "e"
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzaggroup_iter_max_depth(tree_node):
        expected = [["a"], ["c", "b"], ["d", "e", "f"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.zigzaggroup_iter(tree_node, max_depth=3)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"


class TestDAGIterator:
    @staticmethod
    def test_dag_iterator(dag_node):
        expected = [
            ("a", "c"),
            ("a", "d"),
            ("b", "c"),
            ("c", "d"),
            ("c", "f"),
            ("c", "g"),
            ("d", "e"),
            ("d", "f"),
            ("g", "h"),
        ]
        actual = [
            (parent.node_name, child.node_name)
            for parent, child in iterators.dag_iterator(dag_node)
        ]
        len_expected = 9
        len_actual = len(actual)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"
        assert (
            len_expected == len_actual
        ), f"Expected\n{len_expected}\nReceived\n{len_actual}"

    @staticmethod
    def test_dag_iterator_child(dag_node_child):
        expected = [
            ("c", "f"),
            ("d", "f"),
            ("a", "c"),
            ("b", "c"),
            ("c", "d"),
            ("c", "g"),
            ("a", "d"),
            ("d", "e"),
            ("g", "h"),
        ]
        actual = [
            (parent.node_name, child.node_name)
            for parent, child in iterators.dag_iterator(dag_node_child)
        ]
        len_expected = 9
        len_actual = len(actual)
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"
        assert (
            len_expected == len_actual
        ), f"Expected\n{len_expected}\nReceived\n{len_actual}"


class TestBinaryTreeIterator:
    @staticmethod
    def test_preorder_iter(binarytree_node):
        expected = ["1", "2", "4", "8", "5", "3", "6", "7"]
        actual = [node.node_name for node in iterators.preorder_iter(binarytree_node)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter_filter_condition(binarytree_node):
        expected = ["1", "4", "3", "6"]
        actual = [
            node.node_name
            for node in iterators.preorder_iter(
                binarytree_node,
                filter_condition=lambda x: x.node_name in ["1", "3", "6", "4"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter_stop_condition(binarytree_node):
        expected = ["1", "2", "4", "8", "5"]
        actual = [
            node.node_name
            for node in iterators.preorder_iter(
                binarytree_node, stop_condition=lambda x: x.node_name == "3"
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter_max_depth(binarytree_node):
        expected = ["1", "2", "4", "5", "3", "6", "7"]
        actual = [
            node.node_name
            for node in iterators.preorder_iter(binarytree_node, max_depth=3)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter(binarytree_node):
        expected = ["8", "4", "5", "2", "6", "7", "3", "1"]
        actual = [node.node_name for node in iterators.postorder_iter(binarytree_node)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter(binarytree_node):
        expected = ["1", "2", "3", "4", "5", "6", "7", "8"]
        actual = [node.node_name for node in iterators.levelorder_iter(binarytree_node)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter_filter_condition(binarytree_node):
        expected = ["1", "3", "4", "6", "7"]
        actual = [
            node.node_name
            for node in iterators.levelorder_iter(
                binarytree_node,
                filter_condition=lambda x: x.node_name in ["1", "4", "3", "6", "7"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter_max_depth(binarytree_node):
        expected = ["1", "2", "3", "4", "5", "6", "7"]
        actual = [
            node.node_name
            for node in iterators.levelorder_iter(binarytree_node, max_depth=3)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter(binarytree_node):
        expected = [["1"], ["2", "3"], ["4", "5", "6", "7"], ["8"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.levelordergroup_iter(binarytree_node)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter_filter_condition(binarytree_node):
        expected = [["1"], ["3"], ["4", "6", "7"], []]
        actual = [
            [node.node_name for node in group]
            for group in iterators.levelordergroup_iter(
                binarytree_node,
                filter_condition=lambda x: x.node_name in ["1", "4", "3", "6", "7"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter_max_depth(binarytree_node):
        expected = [["1"], ["2", "3"], ["4", "5", "6", "7"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.levelordergroup_iter(
                binarytree_node,
                max_depth=3,
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_inorder_iter(binarytree_node):
        expected = ["4", "8", "2", "5", "1", "6", "3", "7"]
        actual = [node.node_name for node in iterators.inorder_iter(binarytree_node)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_inorder_iter_filter_condition(binarytree_node):
        expected = ["4", "1", "6", "3", "7"]
        actual = [
            node.node_name
            for node in iterators.inorder_iter(
                binarytree_node,
                filter_condition=lambda x: x.node_name in ["1", "4", "3", "6", "7"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_inorder_iter_max_depth(binarytree_node):
        expected = ["4", "2", "5", "1", "6", "3", "7"]
        actual = [
            node.node_name
            for node in iterators.inorder_iter(binarytree_node, max_depth=3)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzag_iter(binarytree_node):
        expected = ["1", "3", "2", "4", "5", "6", "7", "8"]
        actual = [node.node_name for node in iterators.zigzag_iter(binarytree_node)]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzag_iter_filter_condition(binarytree_node):
        expected = ["1", "3", "4", "6", "7"]
        actual = [
            node.node_name
            for node in iterators.zigzag_iter(
                binarytree_node,
                filter_condition=lambda x: x.node_name in ["1", "4", "3", "6", "7"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzag_iter_max_depth(binarytree_node):
        expected = ["1", "3", "2", "4", "5", "6", "7"]
        actual = [
            node.node_name
            for node in iterators.zigzag_iter(binarytree_node, max_depth=3)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzaggroup_iter(binarytree_node):
        expected = [["1"], ["3", "2"], ["4", "5", "6", "7"], ["8"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.zigzaggroup_iter(binarytree_node)
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzaggroup_iter_filter_condition(binarytree_node):
        expected = [["1"], ["3"], ["4", "6", "7"], []]
        actual = [
            [node.node_name for node in group]
            for group in iterators.zigzaggroup_iter(
                binarytree_node,
                filter_condition=lambda x: x.node_name in ["1", "4", "3", "6", "7"],
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_zigzaggroup_iter_max_depth(binarytree_node):
        expected = [["1"], ["3", "2"], ["4", "5", "6", "7"]]
        actual = [
            [node.node_name for node in group]
            for group in iterators.zigzaggroup_iter(
                binarytree_node,
                max_depth=3,
            )
        ]
        assert actual == expected, f"Expected\n{expected}\nReceived\n{actual}"

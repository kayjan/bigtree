from bigtree.utils.iterators import (
    dag_iterator,
    levelorder_iter,
    levelordergroup_iter,
    postorder_iter,
    preorder_iter,
)


class TestPreOrderIter:
    @staticmethod
    def test_preorder_iter(tree_node):
        expected = ["a", "b", "d", "e", "g", "h", "c", "f"]
        actual = [node.node_name for node in preorder_iter(tree_node)]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter2(tree_node2):
        expected = ["a", "b", "d", "g", "e", "h", "i", "c", "f"]
        actual = [node.node_name for node in preorder_iter(tree_node2)]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter_filter_condition(tree_node):
        expected = ["a", "d", "e", "g", "f"]
        actual = [
            node.node_name
            for node in preorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"],
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter_filter_condition_skip_level(tree_node):
        expected = ["g", "h"]
        actual = [
            node.node_name
            for node in preorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["g", "h"],
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter_stop_condition(tree_node):
        expected = ["a", "b", "d", "c", "f"]
        actual = [
            node.node_name
            for node in preorder_iter(
                tree_node, stop_condition=lambda x: x.node_name == "e"
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_preorder_iter_max_depth(tree_node):
        expected = ["a", "b", "d", "e", "c", "f"]
        actual = [node.node_name for node in preorder_iter(tree_node, max_depth=3)]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"


class TestPostOrderIter:
    @staticmethod
    def test_postorder_iter(tree_node):
        expected = ["d", "g", "h", "e", "b", "f", "c", "a"]
        actual = [node.node_name for node in postorder_iter(tree_node)]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter2(tree_node2):
        expected = ["g", "d", "h", "i", "e", "b", "f", "c", "a"]
        actual = [node.node_name for node in postorder_iter(tree_node2)]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter_filter_condition(tree_node):
        expected = ["d", "g", "e", "f", "a"]
        actual = [
            node.node_name
            for node in postorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"],
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter_filter_condition_skip_level(tree_node):
        expected = ["g", "h"]
        actual = [
            node.node_name
            for node in postorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["g", "h"],
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter_stop_condition(tree_node):
        expected = ["d", "b", "f", "c", "a"]
        actual = [
            node.node_name
            for node in postorder_iter(
                tree_node, stop_condition=lambda x: x.node_name == "e"
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_postorder_iter_max_depth(tree_node):
        expected = ["d", "e", "b", "f", "c", "a"]
        actual = [node.node_name for node in postorder_iter(tree_node, max_depth=3)]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"


class TestLevelOrderIter:
    @staticmethod
    def test_levelorder_iter(tree_node):
        expected = ["a", "b", "c", "d", "e", "f", "g", "h"]
        actual = [node.node_name for node in levelorder_iter(tree_node)]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter2(tree_node2):
        expected = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        actual = [node.node_name for node in levelorder_iter(tree_node2)]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter_filter_condition(tree_node):
        expected = ["a", "d", "e", "f", "g"]
        actual = [
            node.node_name
            for node in levelorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["a", "d", "e", "f", "g"],
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter_filter_condition_skip_level(tree_node):
        expected = ["g", "h"]
        actual = [
            node.node_name
            for node in levelorder_iter(
                tree_node,
                filter_condition=lambda x: x.node_name in ["g", "h"],
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter_stop_condition(tree_node):
        expected = ["a", "b", "c", "d", "f"]
        actual = [
            node.node_name
            for node in levelorder_iter(
                tree_node, stop_condition=lambda x: x.node_name == "e"
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelorder_iter_max_depth(tree_node):
        expected = ["a", "b", "c", "d", "e", "f"]
        actual = [node.node_name for node in levelorder_iter(tree_node, max_depth=3)]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"


class TestLevelOrderGroupIter:
    @staticmethod
    def test_levelordergroup_iter(tree_node):
        expected = [["a"], ["b", "c"], ["d", "e", "f"], ["g", "h"]]
        actual = [
            [node.node_name for node in group]
            for group in levelordergroup_iter(tree_node)
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter2(tree_node2):
        expected = [["a"], ["b", "c"], ["d", "e", "f"], ["g", "h", "i"]]
        actual = [
            [node.node_name for node in group]
            for group in levelordergroup_iter(tree_node2)
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter_filter_condition(tree_node):
        expected = [["a"], [], ["d", "e", "f"], ["g"]]
        actual = [
            [node.node_name for node in group]
            for group in levelordergroup_iter(
                tree_node,
                filter_condition=lambda x: x.name in ["a", "d", "e", "f", "g"],
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter_filter_condition_skip_level(tree_node):
        expected = [[], [], [], ["g", "h"]]
        actual = [
            [node.node_name for node in group]
            for group in levelordergroup_iter(
                tree_node,
                filter_condition=lambda x: x.name in ["g", "h"],
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter_stop_condition(tree_node):
        expected = [["a"], ["b", "c"], ["d", "f"]]
        actual = [
            [node.node_name for node in group]
            for group in levelordergroup_iter(
                tree_node, stop_condition=lambda x: x.name == "e"
            )
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"

    @staticmethod
    def test_levelordergroup_iter_max_depth(tree_node):
        expected = [["a"], ["b", "c"], ["d", "e", "f"]]
        actual = [
            [node.node_name for node in group]
            for group in levelordergroup_iter(tree_node, max_depth=3)
        ]
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"


class DAGIterator:
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
            for parent, child in dag_iterator(dag_node)
        ]
        len_expected = 9
        len_actual = len(actual)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"
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
            for parent, child in dag_iterator(dag_node_child)
        ]
        len_expected = 9
        len_actual = len(actual)
        assert expected == actual, f"Expected\n{expected}\nReceived\n{actual}"
        assert (
            len_expected == len_actual
        ), f"Expected\n{len_expected}\nReceived\n{len_actual}"

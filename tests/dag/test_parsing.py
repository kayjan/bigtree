import unittest
from itertools import combinations

import pytest

from bigtree.node import dagnode
from bigtree.utils import exceptions
from tests.test_constants import Constants


class TestParsingDAG(unittest.TestCase):
    def setUp(self):
        """
        Tree should have structure
        a >> b
        b >> c
        b >> d
        c >> e
        c >> f
        e >> f
        f >> g
        d >> e
        """
        self.a = dagnode.DAGNode(name="a", age=90)
        self.b = dagnode.DAGNode(name="b", age=65)
        self.c = dagnode.DAGNode(name="c", age=60)
        self.d = dagnode.DAGNode(name="d", age=40)
        self.e = dagnode.DAGNode(name="e", age=35)
        self.f = dagnode.DAGNode(name="f", age=38)
        self.g = dagnode.DAGNode(name="g", age=10)
        self.h = dagnode.DAGNode(name="h", age=6)

        self.nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g]

    def tearDown(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None

    def test_get_path_dag(self):
        self.a >> self.b
        self.b >> self.c
        self.b >> self.d
        self.c >> self.e
        self.c >> self.f
        self.e >> self.f
        self.f >> self.g
        self.d >> self.e

        expected_paths = [
            [["a", "b"]],
            [["a", "b", "c"]],
            [["a", "b", "d"]],
            [["a", "b", "c", "e"], ["a", "b", "d", "e"]],
            [
                ["a", "b", "c", "e", "f"],
                ["a", "b", "c", "f"],
                ["a", "b", "d", "e", "f"],
            ],
            [
                ["a", "b", "c", "e", "f", "g"],
                ["a", "b", "c", "f", "g"],
                ["a", "b", "d", "e", "f", "g"],
            ],
            [["b", "c"]],
            [["b", "d"]],
            [["b", "c", "e"], ["b", "d", "e"]],
            [["b", "c", "e", "f"], ["b", "c", "f"], ["b", "d", "e", "f"]],
            [
                ["b", "c", "e", "f", "g"],
                ["b", "c", "f", "g"],
                ["b", "d", "e", "f", "g"],
            ],
            None,
            [["c", "e"]],
            [["c", "e", "f"], ["c", "f"]],
            [["c", "e", "f", "g"], ["c", "f", "g"]],
            [["d", "e"]],
            [["d", "e", "f"]],
            [["d", "e", "f", "g"]],
            [["e", "f"]],
            [["e", "f", "g"]],
            [["f", "g"]],
        ]
        for node_pair, expected_path in zip(
            combinations(self.nodes, 2), expected_paths
        ):
            if not expected_path:
                with pytest.raises(exceptions.TreeError) as exc_info:
                    node_pair[0].go_to(node_pair[1])
                assert str(exc_info.value) == Constants.ERROR_NODE_GOTO.format(
                    node=node_pair[1]
                )
            else:
                actual_path = [
                    [_node.node_name for _node in _path]
                    for _path in node_pair[0].go_to(node_pair[1])
                ]
                assert (
                    actual_path == expected_path
                ), f"Wrong path for {node_pair}, expected {expected_path}, received {actual_path}"

    def test_get_path_dag_same_node(self):
        self.a >> self.b
        self.b >> self.c
        self.b >> self.d
        self.c >> self.e
        self.c >> self.f
        self.e >> self.f
        self.f >> self.g
        self.d >> self.e

        for _node in self.nodes:
            actual_path = [
                [_node2.node_name for _node2 in _node1] for _node1 in _node.go_to(_node)
            ]
            expected_path = [[_node.node_name]]
            assert (
                actual_path == expected_path
            ), f"Wrong path for {_node}, expected {expected_path}, received {actual_path}"

    def test_get_path_dag_type_error(self):
        destination = 2
        with pytest.raises(TypeError) as exc_info:
            self.a.go_to(destination)
        assert str(exc_info.value) == Constants.ERROR_NODE_GOTO_TYPE.format(
            type="DAGNode", input_type=type(destination)
        )

    def test_get_path_dag_different_tree_error(self):
        a = dagnode.DAGNode("a")
        with pytest.raises(exceptions.TreeError) as exc_info:
            a.go_to(self.a)
        assert str(exc_info.value) == Constants.ERROR_NODE_GOTO.format(node=self.a)

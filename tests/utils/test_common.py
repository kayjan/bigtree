import unittest

import pytest

from bigtree.node import dagnode, node
from bigtree.utils import common


class TestGetAttr:
    @staticmethod
    @pytest.mark.parametrize(
        "attr_name, result",
        [
            ("data", "test"),
            ("data2", "invalid"),
        ],
    )
    def test_get_attr(attr_name, result):
        _node = node.Node("a", data="test")
        assert common.get_attr(_node, attr_name, "invalid") == result

    @staticmethod
    def test_get_attr_chain_attr():
        _node = node.Node("a", data=node.Node("b", data2="test"))
        assert common.get_attr(_node, "data.data2") == "test"

    @staticmethod
    @pytest.mark.parametrize(
        "attr_name, result",
        [
            ("children[0].data", "test"),
            ("children[1].data", "invalid"),
            ("children[abc].data", "invalid"),
        ],
    )
    def test_get_attr_children(attr_name, result):
        _node = node.Node("a", children=[node.Node("b", data="test")])
        assert common.get_attr(_node, attr_name, "invalid") == result

    @staticmethod
    @pytest.mark.parametrize(
        "attr_name, result",
        [
            ("parent.data", "test"),
            ("parent.parent.data", "invalid"),
            ("parent.data2", "invalid"),
        ],
    )
    def test_get_attr_parent(attr_name, result):
        _node = node.Node("a", data="test")
        _child = node.Node("b", parent=_node)
        assert common.get_attr(_child, attr_name, "invalid") == result

    @staticmethod
    @pytest.mark.parametrize(
        "attr_name, result",
        [
            ("parents[0].parents[0].data", "a-test"),
            ("parents[0].parents[1].data", "b-test"),
            ("parents[0].parents[2].data", "invalid"),
        ],
    )
    def test_get_attr_parents(attr_name, result):
        a = dagnode.DAGNode("a", data="a-test")
        b = dagnode.DAGNode("b", data="b-test")
        c = dagnode.DAGNode("c")
        d = dagnode.DAGNode("d")
        c.parents = [a, b]
        c.children = [d]
        assert d.get_attr(attr_name, "invalid") == result

    @staticmethod
    @pytest.mark.parametrize(
        "attr_value, attr_name, result",
        [
            ("test", "data.data2", "test"),
            ([["test", "test1"], "test2"], "data.data2[0][0]", "test"),
            ([["test", "test1"], "test2"], "data.data2[0][1]", "test1"),
            ([["test", "test1"], "test2"], "data.data2[1]", "test2"),
            ([["test", ["test1", "test11"]], "test2"], "data.data2[0][1][1]", "test11"),
            (
                [["test", ["test1", "test11"]], "test2"],
                "data.data2[0][2][1]",
                "invalid",
            ),
            (
                [["test", ["test1", "test11"]], "test2"],
                "data.data2[0][1][2]",
                "invalid",
            ),
        ],
    )
    def test_get_attr_class(attr_value, attr_name, result):
        class A:
            def __init__(self, _data2: str):
                self.data2 = _data2

        _node = node.Node("a", data=A(attr_value))
        assert common.get_attr(_node, attr_name, "invalid") == result

    @staticmethod
    def test_get_attr_callable():
        _node = node.Node("a")
        assert common.get_attr(_node, lambda x: "test") == "test"


class TestAssembleAttributes(unittest.TestCase):
    def setUp(self):
        self.node = node.Node("a", data="test", age=1)
        self.b = node.Node("b", parent=self.node)

    def tearDown(self):
        self.node = None
        self.b = None

    def test_assemble_attributes(self):
        assert common.assemble_attributes(self.node) == {"data": "test", "age": 1}

    def test_assemble_attributes_attr_dict(self):
        assert common.assemble_attributes(
            self.node, attr_dict={"data": "title", "age": "age"}, all_attrs=False
        ) == {"title": "test", "age": 1}

    def test_assemble_attributes_all_attrs(self):
        assert common.assemble_attributes(
            self.node, attr_dict={"data": "title"}, all_attrs=False
        ) == {"title": "test"}

    def test_assemble_attributes_path_key(self):
        assert common.assemble_attributes(self.node, path_key="path_test") == {
            "data": "test",
            "age": 1,
            "path_test": "/a",
        }

    def test_assemble_attributes_parent_key(self):
        assert common.assemble_attributes(self.node, parent_key="parent_test") == {
            "data": "test",
            "age": 1,
            "parent_test": None,
        }
        assert common.assemble_attributes(self.b, parent_key="parent_test") == {
            "parent_test": "a"
        }

    @staticmethod
    def test_assemble_attributes_dict_attr():
        _node = node.Node("a", data={"a": 1, "b": 2})
        assert common.assemble_attributes(_node) == {"data": {"a": 1, "b": 2}}

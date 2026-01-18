import pytest

from bigtree.node import node
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
    def test_get_attr_nested_parent(attr_name, result):
        _node = node.Node("a", data="test")
        _child = node.Node("b", parent=_node)
        assert common.get_attr(_child, attr_name, "invalid") == result

    @staticmethod
    def test_get_attr_nested_attr():
        _node = node.Node("a", data=node.Node("b", data2="test"))
        assert common.get_attr(_node, "data.data2") == "test"

    @staticmethod
    def test_get_attr_nested_class():
        class A:
            def __init__(self, _data2: str):
                self.data2 = _data2

        _node = node.Node("a", data=A("test"))
        assert common.get_attr(_node, "data.data2") == "test"

    @staticmethod
    def test_get_attr_callable():
        _node = node.Node("a")
        assert common.get_attr(_node, lambda x: "test") == "test"

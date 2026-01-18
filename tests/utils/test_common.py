from bigtree.node import node
from bigtree.utils import common


class TestGetAttr:
    @staticmethod
    def test_get_attr():
        _node = node.Node("a", data="test")
        assert common.get_attr(_node, "data") == "test"

    @staticmethod
    def test_get_attr_children():
        _node = node.Node("a", children=[node.Node("b", data="test")])
        assert common.get_attr(_node, "children[0].data") == "test"

    @staticmethod
    def test_get_attr_nested_parent():
        _node = node.Node("a", data="test")
        _child = node.Node("b", parent=_node)
        assert common.get_attr(_child, "parent.data") == "test"

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

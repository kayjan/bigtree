from bigtree.node import node


class NodeA(node.Node):
    pass


class CustomNode(node.Node):
    def __init__(self, name: str, custom_field: int, custom_field_str: str, **kwargs):
        super().__init__(name, **kwargs)
        self.custom_field = custom_field
        self.custom_field_str = custom_field_str

import pytest

from bigtree.node import node


class NodeA(node.Node):
    pass


class CustomNode(node.Node):
    def __init__(self, name: str, custom_field: int, custom_field_str: str, **kwargs):
        super().__init__(name, **kwargs)
        self.custom_field = custom_field
        self.custom_field_str = custom_field_str


@pytest.fixture
def rich_root():
    from rich.text import Text
    from rich.tree import Tree as RichTree

    rich_root = RichTree(Text("Grandparent", style="magenta"))
    child = rich_root.add("Child")
    _ = child.add(Text("Grandchild", style="red"))
    _ = rich_root.add("Child 2")
    return rich_root

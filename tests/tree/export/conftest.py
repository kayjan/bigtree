import pytest

from bigtree.node import node


@pytest.fixture
def tree_node_rich():
    """
    Root
    ├── Child 1
    │   └── Grandchild 1
    └── Child 2
    """
    tree_node = node.Node("[magenta]Root[/]")
    child_node = node.Node("Child [red]1[/red]", parent=tree_node)
    _ = node.Node("Grand[blue]child[/] 1", parent=child_node)
    _ = node.Node("[blue]Child[/] [red]2[/]", parent=tree_node)
    return tree_node


@pytest.fixture
def tree_node_rich_str():
    return (
        """Root\n"""
        """├── Child 1\n"""
        """│   └── Grandchild 1\n"""
        """└── Child 2\n"""
    )

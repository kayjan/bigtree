from typing import Any

from bigtree.node import node
from bigtree.tree import tree
from bigtree.utils import common

try:
    from textual.widgets import Tree
    from textual.widgets._tree import TreeNode

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    Tree = MagicMock()
    TreeNode = MagicMock()


__all__ = [
    "get_corresponding_bt_node",
    "get_attr_bt_node",
    "assemble_data",
    "populate_textual_tree",
    "update_details",
    "expand_parents",
    "select_edit_attr",
]


# Shortcut, key binding function, footer description, help description
HELP: dict[str, list[tuple[str, ...]]] = {
    "Navigation": [
        ("↑ / ↓", "Move selection"),
        ("Enter / Click", "View node attributes"),
        ("Space / Double Click", "Expand or collapse node"),
    ],
    "Editing": [
        ("a", "add_node", "Add Child", "Add child node"),
        ("A", "add_sibling", "Add Sibling", "Add sibling node"),
        ("r", "rename_node", "Rename", "Rename selected node"),
        ("d", "delete_node", "Delete", "Delete selected node"),
        ("t", "edit_attr", "Edit Attributes", "Edit attributes"),
    ],
    "Search": [
        ("/", "search", "Search", "Search"),
        ("n", "next_match", "Next", "Next search result"),
        ("N", "prev_match", "Prev", "Previous search result"),
    ],
    "View": [
        ("e", "toggle_expand", "Expand", "Toggle expand"),
        ("E", "expand_all", "Expand All", "Expand all"),
        ("z", "collapse_all", "Collapse All", "Collapse all"),
    ],
    "File": [
        ("S", "save_as", "Save As", "Save As"),
        ("q", "quit", "Quit", "Quit Studio"),
    ],
}

BINDINGS = [
    # enter / single click: View attribute
    # space / double click: Expand or collapse
    *(
        (item[0], item[1], item[2])
        for section, items in HELP.items()
        if section in ["Editing", "Search", "View", "File"]
        for item in items
    ),
    ("?", "help", "Help"),
]


SEARCH_EXAMPLES = """[b]Examples[/]
[cyan]alice[/]                                    Exact name
[cyan]name:^ali.*[/]                              Regex name
[cyan]query:age >= 30 OR node_name LIKE ".*e"[/]  Advanced query"""


def _get_textual_node_path(textual_node: TreeNode) -> list[str]:
    """Get node path of textual TreeNode, reads the node name recursively until root node.

    Args:
        textual_node: textual tree node
        sep: tree separator

    Returns:
        node path
    """
    path = [str(textual_node.label)]
    parent = textual_node.parent
    while parent:
        path.append(str(parent.label))
        parent = parent.parent
    return path[::-1]


def get_corresponding_bt_node(bt_tree: tree.Tree, textual_node: TreeNode) -> node.Node:
    """Get corresponding bigtree node from textual node.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node

    Returns:
        bigtree tree node
    """
    node_path = _get_textual_node_path(textual_node)
    for next_path in node_path[1:]:
        bt_tree = bt_tree[next_path]
    return bt_tree.node


def get_attr_bt_node(
    bt_tree: tree.Tree, textual_node: TreeNode, **kwargs: Any
) -> dict[str, Any]:
    """Get attribute of bigtree node from textual node.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node

    Returns:
        bigtree tree node
    """
    bt_node = get_corresponding_bt_node(bt_tree, textual_node)
    return common.assemble_attributes(bt_node, **kwargs)


def assemble_data(bt_node: node.Node) -> dict[str, str]:
    """Assemble data for textual node from bigtree node

    Args:
        bt_node: bigtree node

    Returns:
        data dictionary
    """
    return {"path_name": bt_node.path_name}


def populate_textual_tree(
    bt_tree: tree.Tree,
    textual_tree: Tree,
    max_depth: int = 2,
) -> None:
    """Populate textual tree with bigtree tree.

    Args:
        bt_tree: bigtree tree
        textual_tree: textual tree
        max_depth: maximum depth of tree to expand
    """

    def add(bt_parent: node.Node, textual_parent: TreeNode, depth: int = 1) -> None:
        # Depth + 1 because we are calculating the depth of children
        expand = True if depth + 1 < max_depth else False
        for bt_child in bt_parent.children:
            textual_child = textual_parent.add(
                bt_child.node_name, data=assemble_data(bt_child), expand=expand
            )
            add(bt_child, textual_child, depth + 1)

    textual_tree.clear()
    textual_tree.root.label = bt_tree.node.name
    textual_tree.root.data = assemble_data(bt_tree.node)
    textual_tree.root.expand()
    add(bt_tree.node, textual_tree.root)


def update_details(bt_tree: tree.Tree, textual_node: TreeNode) -> str:
    """Get details from selected textual_node by retrieving attributes from the corresponding bigtree node.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node

    Returns:
        Formatted attribute details
    """
    attrs = get_attr_bt_node(
        bt_tree, textual_node, name_key="__name", path_key="__path"
    )
    attr_text = "\n".join(
        f"{k}: {v}" for k, v in attrs.items() if k not in ["__name", "__path"]
    )
    return (
        f"[b]Name:[/] {attrs['__name']}\n"
        f"[b]Path:[/] {attrs['__path']}\n\n"
        f"[b]Attributes:[/]\n{attr_text or 'None'}"
    )


def expand_parents(textual_node: TreeNode) -> None:
    """Recursively expand parents

    Args:
        textual_node: textual tree node
    """
    parent = textual_node.parent

    while parent is not None:
        parent.expand()
        parent = parent.parent


def select_edit_attr(bt_tree: tree.Tree, textual_node: TreeNode) -> str:
    """Get existing attribute of bigtree node from textual node.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node

    Returns:
        Formatted attribute (e.g., key=value,key1=value1)
    """
    attrs = get_attr_bt_node(bt_tree, textual_node)
    return ",".join(f"{k}={repr(v)}" for k, v in attrs.items())

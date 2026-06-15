from typing import Any

from bigtree.node import node
from bigtree.tree import tree
from bigtree.utils import common

try:
    import json
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    json = MagicMock()

try:
    from textual.widgets import Static
    from textual.widgets._tree import TreeNode

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    TreeNode = MagicMock()
    Static = MagicMock()


__all__ = [
    "populate_textual_tree",
    "update_details",
    "expand_parents",
    "action_add_node",
    "action_add_sibling",
    "action_delete_node",
    "action_rename_node",
    "select_edit_attr",
    "action_edit_attr",
    "action_save_as",
]


def _get_textual_node_path(textual_node: TreeNode, sep: str = "/") -> str:
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
    return sep.join(path[::-1])


def _get_corresponding_bt_node(bt_tree: tree.Tree, textual_node: TreeNode) -> node.Node:
    """Get corresponding bigtree node from textual node.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node

    Returns:
        bigtree tree node
    """
    node_path = _get_textual_node_path(textual_node)
    return bt_tree.find_full_path(node_path)  # type: ignore[attr-defined, no-any-return]


def _get_attr_bt_node(
    bt_tree: tree.Tree, textual_node: TreeNode, **kwargs: Any
) -> dict[str, Any]:
    """Get attribute of bigtree node from textual node.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node

    Returns:
        bigtree tree node
    """
    bt_node = _get_corresponding_bt_node(bt_tree, textual_node)
    return common.assemble_attributes(bt_node, **kwargs)


def populate_textual_tree(
    bt_tree: tree.Tree,
    textual_tree: TreeNode,
    max_depth: int,
) -> None:
    """Populate textual tree with bigtree tree.

    Args:
        bt_tree: bigtree tree
        textual_tree: textual tree
        max_depth: maximum depth of tree to expand
    """
    textual_tree.clear()
    textual_tree.root.label = bt_tree.node.name
    textual_tree.root.expand()

    def add(bt_parent: node.Node, textual_parent: TreeNode, depth: int = 1) -> None:
        # Depth + 1 because we are calculating the depth of children
        expand = True if depth + 1 < max_depth else False
        for bt_child in bt_parent.children:
            textual_child = textual_parent.add(bt_child.node_name, expand=expand)
            add(bt_child, textual_child, depth + 1)

    add(bt_tree.node, textual_tree.root)


def update_details(bt_tree: tree.Tree, textual_node: TreeNode) -> str:
    """Get details from selected textual_node by retrieving attributes from the corresponding bigtree node.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node

    Returns:
        Formatted attribute details
    """
    attrs = _get_attr_bt_node(
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


def action_add_node(
    bt_tree: tree.Tree, textual_node: TreeNode, value: str | None
) -> None:
    """Add new child node to existing node, implements for bigtree tree and textual tree in-place.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node
        value: name of node to add
    """
    if not value or not textual_node:
        return
    bt_node = _get_corresponding_bt_node(bt_tree, textual_node)
    node.Node(value, parent=bt_node)
    textual_node.add(value)
    textual_node.expand()


def action_add_sibling(
    bt_tree: tree.Tree, textual_node: TreeNode, value: str | None
) -> None:
    """Add new sibling node to existing node, implements for bigtree tree and textual tree in-place.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node
        value: name of node to add
    """
    if not textual_node.parent:
        raise ValueError("Cannot add sibling for root node.")
    if not value or not textual_node:
        return
    bt_node = _get_corresponding_bt_node(bt_tree, textual_node)
    node.Node(value, parent=bt_node.parent)
    textual_node.parent.add(value)


def action_delete_node(bt_tree: tree.Tree, textual_node: TreeNode) -> None:
    """Delete node, implements for bigtree tree and textual tree in-place.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node
    """
    if not textual_node:
        return
    bt_node = _get_corresponding_bt_node(bt_tree, textual_node)
    bt_node.parent = None
    textual_node.remove()


def action_rename_node(
    bt_tree: tree.Tree, textual_node: TreeNode, value: str | None
) -> None:
    """Delete node, implements for bigtree tree and textual tree in-place.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node
        value: new node name
    """
    if not textual_node or not value:
        return
    bt_node = _get_corresponding_bt_node(bt_tree, textual_node)
    bt_node.rename(value)
    textual_node.set_label(value)


def select_edit_attr(bt_tree: tree.Tree, textual_node: TreeNode) -> str:
    """Get existing attribute of bigtree node from textual node.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node

    Returns:
        Formatted attribute (e.g., key=value,key1=value1)
    """
    attrs = _get_attr_bt_node(bt_tree, textual_node)
    return ",".join(f"{k}={v}" for k, v in attrs.items())


def action_edit_attr(
    bt_tree: tree.Tree, textual_node: TreeNode, value: str | None
) -> None:
    """Delete node, implements for bigtree tree and textual tree in-place.

    Args:
        bt_tree: bigtree tree
        textual_node: textual tree node
        value: new node name
    """
    if not textual_node or not value:
        return
    kv_pairs = [kv.strip().split("=") for kv in value.split(",")]
    try:
        new_attrs = dict(kv_pairs)
    except ValueError as err:
        raise ValueError(f"Input malformed, check `{value}`") from err
    bt_node = _get_corresponding_bt_node(bt_tree, textual_node)
    existing_attrs = _get_attr_bt_node(bt_tree, textual_node)
    attrs_to_remove = set(existing_attrs) - set(new_attrs)
    for attr_to_remove in attrs_to_remove:
        del bt_node.__dict__[attr_to_remove]
    bt_node.set_attrs(new_attrs)


def action_save_as(bt_tree: tree.Tree, value: str | None) -> None:
    """Save tree as json file.

    Args:
        bt_tree: bigtree tree
        value: save path
    """
    if not value:
        return
    data = bt_tree.to_dict(name_key=None, all_attrs=True)  # type: ignore[attr-defined]
    with open(value, "w") as f:
        json.dump(data, f, indent=2)

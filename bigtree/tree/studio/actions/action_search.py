from typing import Any

from bigtree.tree import tree
from bigtree.tree.studio.actions.action import Action

try:
    from textual.widgets._tree import TreeNode

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    TreeNode = MagicMock()


__all__ = ["ActionSearch"]


class ActionSearch(Action):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def _run(self) -> list[TreeNode]:
        """Search tree, for full/partial/regex match in name or queries"""
        if self.value.startswith("query:"):
            bt_matches = self.bt_tree.query(self.value[6:])  # type: ignore[attr-defined]
        elif self.value.startswith("name:"):
            bt_matches = self.bt_tree.find_names(self.value[5:], regex=True)  # type: ignore[attr-defined]
        else:
            bt_matches = self.bt_tree.find_names(self.value)  # type: ignore[attr-defined]

        bt_matches_path = [bt_node.path_name for bt_node in bt_matches]
        return _get_corresponding_textual_nodes(self.textual_node, bt_matches_path)


def _get_corresponding_textual_nodes(
    textual_tree: tree.Tree, paths: list[str]
) -> list[TreeNode]:
    """Get textual nodes that matches paths

    Args:
        paths: list of tree paths to retrieve textual nodes

    Returns:
        list of textual nodes that matches paths
    """
    matches = []

    def walk(item: TreeNode) -> None:
        if item.data["path_name"] in paths:
            matches.append(item)
        for _child in item.children:
            walk(_child)

    for child in textual_tree.root.children:  # type: ignore[attr-defined]
        walk(child)
    return matches

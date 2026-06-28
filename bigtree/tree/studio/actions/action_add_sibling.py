from typing import Any

import bigtree.tree.studio.utils as studio_utils
from bigtree.node import node
from bigtree.tree.studio.actions.action import Action

__all__ = ["ActionAddSibling"]


class ActionAddSibling(Action):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def validate(self) -> bool:
        """Validation before performing action"""
        if not self.value or not self.textual_node:
            return False
        if not self.textual_node.parent:
            raise ValueError("Cannot add sibling for root node.")
        return True

    def _run(self) -> None:
        """Add new sibling node to existing node, implements for bigtree tree and textual tree in-place."""
        bt_node = studio_utils.get_corresponding_bt_node(
            self.bt_tree, self.textual_node
        )
        bt_child = node.Node(self.value, parent=bt_node.parent)
        self.textual_node.parent.add(
            self.value, data=studio_utils.assemble_data(bt_child)
        )

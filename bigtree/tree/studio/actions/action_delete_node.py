from typing import Any

import bigtree.tree.studio.utils as studio_utils
from bigtree.tree.studio.actions.action import Action

__all__ = ["ActionDeleteNode"]


class ActionDeleteNode(Action):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def validate(self) -> bool:
        """Validation before performing action"""
        if not self.textual_node:
            return False
        return True

    def _run(self) -> None:
        """Delete node, implements for bigtree tree and textual tree in-place"""
        bt_node = studio_utils.get_corresponding_bt_node(
            self.bt_tree, self.textual_node
        )
        bt_node.parent = None
        self.textual_node.remove()

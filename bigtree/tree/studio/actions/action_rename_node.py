from typing import Any

import bigtree.tree.studio.utils as studio_utils
from bigtree.tree.studio.actions.action import Action

__all__ = ["ActionRenameNode"]


class ActionRenameNode(Action):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def _run(self) -> None:
        """Rename node, implements for bigtree tree and textual tree in-place"""
        bt_node = studio_utils.get_corresponding_bt_node(
            self.bt_tree, self.textual_node
        )
        bt_node.rename(self.value)
        self.textual_node.set_label(self.value)
        self.textual_node.data = studio_utils.assemble_data(bt_node)

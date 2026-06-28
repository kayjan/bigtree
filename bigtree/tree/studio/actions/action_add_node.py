from typing import Any

import bigtree.tree.studio.utils as studio_utils
from bigtree.node import node
from bigtree.tree.studio.actions.action import Action

__all__ = ["ActionAddNode"]


class ActionAddNode(Action):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def _run(self) -> None:
        """Add new child node to existing node, implements for bigtree tree and textual tree in-place."""
        bt_node = studio_utils.get_corresponding_bt_node(
            self.bt_tree, self.textual_node
        )
        bt_child = node.Node(self.value, parent=bt_node)
        self.textual_node.add(self.value, data=studio_utils.assemble_data(bt_child))
        self.textual_node.expand()

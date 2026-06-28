from typing import Any

import bigtree.tree.studio.utils as studio_utils
from bigtree.tree.studio.actions.action import Action

try:
    import ast
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    ast = MagicMock()


__all__ = ["ActionEditAttr"]


class ActionEditAttr(Action):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def _run(self) -> None:
        """Edit attribute of node, implements for bigtree tree in-place. Textual tree data only maintains path_name"""
        try:
            kv_pairs = [kv.strip().split("=") for kv in self.value.split(",")]
            kv_pairs_eval = [(k, ast.literal_eval(v)) for k, v in kv_pairs]
            new_attrs = dict(kv_pairs_eval)
        except (ValueError, SyntaxError) as err:
            raise ValueError(f"Input malformed, check `{self.value}`") from err
        bt_node = studio_utils.get_corresponding_bt_node(
            self.bt_tree, self.textual_node
        )
        existing_attrs = studio_utils.get_attr_bt_node(self.bt_tree, self.textual_node)
        attrs_to_remove = set(existing_attrs) - set(new_attrs)
        for attr_to_remove in attrs_to_remove:
            del bt_node.__dict__[attr_to_remove]
        bt_node.set_attrs(new_attrs)
        # Sync textual_node to bt_node
        self.textual_node.label = bt_node.name
        self.textual_node.data = studio_utils.assemble_data(bt_node)

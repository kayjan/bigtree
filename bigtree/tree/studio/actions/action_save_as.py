from typing import Any

from bigtree.tree.studio.actions.action import Action

try:
    import json
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    json = MagicMock()
try:
    from textual.widgets._tree import TreeNode

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    TreeNode = MagicMock()

__all__ = ["ActionSaveAs"]


class ActionSaveAs(Action):  # pragma: no cover
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def validate(self) -> bool:
        """Validation before performing action"""
        if not self.value:
            return False
        return True

    def _run(self) -> None:
        """Save tree as json file"""
        data = self.bt_tree.to_dict(name_key=None, all_attrs=True)  # type: ignore[attr-defined]
        with open(self.value, "w") as f:
            json.dump(data, f, indent=2)

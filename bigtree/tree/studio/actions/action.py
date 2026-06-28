from bigtree.tree import tree

try:
    from textual.widgets._tree import TreeNode

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    Static = MagicMock()


class Action:  # pragma: no cover
    def __init__(
        self,
        bt_tree: tree.Tree,
        textual_node: TreeNode | None = None,
        value: str | None = None,
    ):
        self.bt_tree = bt_tree
        self.textual_node = textual_node
        self.value = value

    def validate(self) -> bool:
        """Validation before performing action"""
        if not self.value or not self.textual_node:
            return False
        return True

    def _run(self) -> None | list[TreeNode]:
        """Custom run command in subclass"""
        raise NotImplementedError()

    def run(self) -> None | list[TreeNode]:
        """Validate and run command"""
        if not self.validate():
            return None
        return self._run()

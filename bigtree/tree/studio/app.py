"""
```
██████╗ ██╗ ██████╗ ████████╗██████╗ ███████╗███████╗
██╔══██╗██║██╔════╝ ╚══██╔══╝██╔══██╗██╔════╝██╔════╝
██████╔╝██║██║  ███╗   ██║   ██████╔╝█████╗  █████╗
██╔══██╗██║██║   ██║   ██║   ██╔══██╗██╔══╝  ██╔══╝
██████╔╝██║╚██████╔╝   ██║   ██║  ██║███████╗███████╗
╚═════╝ ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝
```
Visualise and interact with trees using terminal interface.

Usage:
    Start the terminal interface
    ```
    bigtree-studio
    ```

    Open an existing tree
    ```
    bigtree-studio tree.json --depth 2
    ```
    Sample json file:
    ```
    {
      "/Company/Engineering/Product": {
        "owner": "alice",
        "size": 123
      },
      "/Company/Engineering/Data": {},
      "/Company/Finance": {}
    }
    ```

Example Terminal layout:
```
┌───────────────────────────────────────────────────────────┐
│                       Bigtree Studio                      │
├─────────────────────┬─────────────────────────────────────┤
│ Tree View           │ Node Details                        │
│                     │                                     │
│ Company             │ Name: Product                       │
│ ├─ Engineering      │ Path: /Company/Engineering/Product  │
│ │  ├─ Product       │                                     │
│ │  └─ Data          │ Attributes                          │
│ └─ Finance          │ owner = alice                       │
│                     │ size = 123                          │
│                     │                                     │
├─────────────────────┴─────────────────────────────────────┤
│ a: Add Child A: Add Sibling d: Delete r: Rename           │
│ t: Edit attribute /: Search n: Next N: Prev               │
│ e: Expand E: Expand All z: Collapse All                   │
│ S: Save As q: Quit                                        │
└───────────────────────────────────────────────────────────┘
```
"""

from typing import List, Optional

import bigtree.tree.studio.utils as studio_utils
from bigtree.tree.studio.details import Details
from bigtree.tree.studio.prompt import Prompt
from bigtree.tree.tree import Tree as BTTree
from bigtree.utils import exceptions

try:
    import json

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    json = MagicMock()

try:
    import time

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    time = MagicMock()

try:
    import argparse

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    argparse = MagicMock()

try:
    from textual.app import App, ComposeResult
    from textual.containers import Horizontal
    from textual.widgets import Footer, Header, Static, Tree
    from textual.widgets._tree import TreeNode

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    App = ComposeResult = MagicMock()
    Horizontal = MagicMock()
    Footer = Header = Static = Tree = MagicMock()
    TreeNode = MagicMock()


__all__ = ["run_app"]


class Studio(App):  # type: ignore[misc]
    CSS = """
    Tree {
        width: 2fr;
    }

    .details {
        width: 1fr;
        padding: 1;
    }
    """

    BINDINGS = [
        # space: Expand
        # single click: view attribute
        # double click: Expand
        ("a", "add_node", "Add Child"),
        ("A", "add_sibling", "Add Sibling"),
        ("d", "delete_node", "Delete"),
        ("r", "rename_node", "Rename"),
        ("t", "edit_attr", "Edit Attribute"),
        ("/", "search", "Search"),
        ("n", "next_match", "Next"),
        ("N", "prev_match", "Prev"),
        ("e", "toggle_expand", "Expand"),
        ("E", "expand_all", "Expand All"),
        ("z", "collapse_all", "Collapse All"),
        ("S", "save_as", "Save As"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, tree: BTTree, depth: int = 2):
        super().__init__()
        self.bt_tree = tree
        self.depth = depth

        self.textual_tree: Optional[Tree] = None
        self._last_node = None
        self._last_click_time = time.time()
        self.search_matches: List[TreeNode] = []
        self.search_index: int = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield Details()
        with Horizontal():
            yield Tree("Tree", id="tree")
            yield Static("Select a node", classes="details", id="details")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Bigtree Studio"
        self.theme = "textual-dark"
        self.textual_tree = self.query_one(Tree)
        studio_utils.populate_textual_tree(self.bt_tree, self.textual_tree, self.depth)

    def _update_details(self, textual_node: TreeNode) -> None:
        details = self.query_one("#details", Static)
        attr_details = studio_utils.update_details(self.bt_tree, textual_node)
        details.update(attr_details)

    def _get_selected(self) -> Optional[TreeNode]:
        return self.textual_tree.cursor_node

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        event_node: TreeNode = event.node
        # Keep expand/collapse state
        if event_node.is_expanded:
            event_node.collapse()
        else:
            event_node.expand()

        # Double click event
        now = time.time()
        if self._last_node == event.node and now - self._last_click_time < 0.35:
            if event_node.is_expanded:
                event_node.collapse()
            else:
                event_node.expand()

        self._last_click_time = now
        self._last_node = event.node

        # Show details
        self._update_details(event_node)

    # ----------------------------
    # Key-binding actions
    # ----------------------------

    def action_add_node(self) -> None:
        self.push_screen(Prompt("Add child node"), self._add_node)

    @exceptions.safe_action
    def _add_node(self, value: str | None) -> None:
        sel = self._get_selected()
        studio_utils.action_add_node(self.bt_tree, sel, value)

    def action_add_sibling(self) -> None:
        self.push_screen(Prompt("Add sibling node"), self._add_sibling)

    @exceptions.safe_action
    def _add_sibling(self, value: Optional[str]) -> None:
        sel = self._get_selected()
        studio_utils.action_add_sibling(self.bt_tree, sel, value)

    def action_delete_node(self) -> None:
        sel = self._get_selected()
        studio_utils.action_delete_node(self.bt_tree, sel)

    def action_rename_node(self) -> None:
        self.push_screen(Prompt("Rename node"), self._rename_node)

    @exceptions.safe_action
    def _rename_node(self, value: Optional[str]) -> None:
        sel = self._get_selected()
        studio_utils.action_rename_node(self.bt_tree, sel, value)

    def action_edit_attr(self) -> None:
        sel = self._get_selected()
        existing_attrs = studio_utils.select_edit_attr(self.bt_tree, sel)
        self.push_screen(
            Prompt(
                "Edit attribute (key=value,key1=value1)",
                value=existing_attrs,
            ),
            self._edit_attr,
        )

    @exceptions.safe_action
    def _edit_attr(self, value: Optional[str]) -> None:
        sel = self._get_selected()
        studio_utils.action_edit_attr(self.bt_tree, sel, value)
        self._update_details(sel)

    def action_search(self) -> None:
        self.push_screen(
            Prompt(
                "Search by name, attribute, or query",
                additional_context=studio_utils.SEARCH_EXAMPLES,
            ),
            self._search,
        )

    @exceptions.safe_action
    def _search(self, value: Optional[str]) -> None:
        if not value:
            return

        matches = studio_utils.action_search(self.bt_tree, self.textual_tree, value)
        self.search_matches = matches
        self.search_index = 0

        if matches:
            self._focus_match()

    def action_next_match(self) -> None:
        if not self.search_matches:
            return
        self.search_index = (self.search_index + 1) % len(self.search_matches)
        self._focus_match()

    def action_prev_match(self) -> None:
        if not self.search_matches:
            return
        self.search_index = (self.search_index - 1) % len(self.search_matches)
        self._focus_match()

    def _focus_match(
        self,
    ) -> None:
        node = self.search_matches[self.search_index]
        studio_utils.expand_parents(node)
        self.textual_tree.select_node(node)

    def action_toggle_expand(self) -> None:
        sel = self._get_selected()
        if sel:
            sel.toggle()

    def action_expand_all(self) -> None:
        self.textual_tree.root.expand_all()

    def action_collapse_all(self) -> None:
        self.textual_tree.root.collapse_all()

    def action_save_as(self) -> None:
        self.push_screen(Prompt("Save tree"), self._save_as)

    @exceptions.safe_action
    def _save_as(self, value: Optional[str]) -> None:
        studio_utils.action_save_as(self.bt_tree, value)
        self.notify(
            f"Saved to {value}", title="Save Successful", severity="information"
        )


def run_app_cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Input JSON file in a flattened tree format. If not specified, a blank tree will be created",
    )
    parser.add_argument(
        "--depth",
        type=int,
        help="Initial tree depth to display, defaults to 2",
        default=2,
    )
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            data = json.load(f)
        tree = BTTree.from_dict(data)  # type: ignore[attr-defined]
    else:
        tree = BTTree.from_str("Root")  # type: ignore[attr-defined]

    run_app(tree, args.depth)


@exceptions.optional_dependencies_studio
def run_app(tree: BTTree, depth: int = 2) -> None:
    app = Studio(tree, depth)
    app.run()


if __name__ == "__main__":
    run_app_cli()

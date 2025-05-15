from typing import TYPE_CHECKING, Any, Optional

from bigtree.node import node

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    tk = MagicMock()
    ttk = MagicMock()

if TYPE_CHECKING:
    TkEvent = tk.Event[tk.Widget]
else:
    TkEvent = Any

__all__ = ["render_tree"]


class DragDropTree(ttk.Treeview):
    def __init__(self, master: tk.Tk, **kwargs: Any):
        super().__init__(master, **kwargs)
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_motion)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.tag_configure("highlight", background="lightblue")

        self._dragging_item: Optional[str] = None
        self._drop_target: Optional[str] = None

    def on_button_press(self, event: TkEvent) -> None:
        """Assign dragging item to pressed object"""
        item = self.identify_row(event.y)
        if item:
            self._dragging_item = item

    def on_motion(self, event: TkEvent) -> None:
        """Highlight drop target"""
        if not self._dragging_item:
            return

        # Highlight drop target
        new_target = self.identify_row(event.y)
        if new_target != self._drop_target:
            self._clear_highlight()
            if new_target and new_target != self._dragging_item:
                self.item(new_target, tags=("highlight",))
                self._drop_target = new_target

    def _clear_highlight(self) -> None:
        """Clear highlight"""
        if self._drop_target:
            self.item(self._drop_target, tags=())
            self._drop_target = None

    def on_button_release(self, event: TkEvent) -> None:
        """Assign dragging item to first child of drop target"""
        if not self._dragging_item:
            return

        target = self.identify_row(event.y)
        if target and target != self._dragging_item:
            self.item(target, open=True)
            self.move(self._dragging_item, target, 0)

        self._clear_highlight()
        self._dragging_item = None
        self._drop_target = None


class TkinterTree:
    def __init__(
        self,
        root: tk.Tk,
        title: str = "Tree Render",
        root_name: str = "Root",
    ):
        """Tree render using Tkinter.

        Args:
            root: existing Tkinter object
            title: title of render for window pop-up
            root_name: initial root name of tree
        """
        self.counter = 0

        root.title(title)
        root.minsize(width=400, height=200)
        tree = DragDropTree(root)
        tree.pack(fill=tk.BOTH, expand=True)

        entry = tk.Entry(root)
        entry.bind("<FocusOut>", lambda e: entry.place_forget())
        entry.bind("<Return>", self.on_return)
        entry.bind("<plus>", self.on_plus)
        tree.bind("<plus>", self.on_plus)
        tree.bind("<Delete>", self.on_delete)
        tree.bind("<Double-1>", self.on_double_click)

        # Insert nodes
        tree_root = tree.insert("", "end", iid=self.get_iid(), text=root_name)

        # Add buttons
        button_frame = tk.Frame(root)
        button_frame.pack()
        b_add = tk.Button(button_frame, text="Add Child", command=self.on_plus)
        b_print = tk.Button(button_frame, text="Print Tree", command=self.print_tree)
        b_export = tk.Button(button_frame, text="Export Tree", command=self.export_tree)
        for button in [b_add, b_print, b_export]:
            button.pack(side="left", padx=5)

        self.tree = tree
        self.tree_root = tree_root
        self.entry = entry

    def get_iid(self) -> str:
        """Get iid of item

        Returns:
            iid
        """
        self.counter += 1
        return str(self.counter)

    def validate_name(self, parent: str, name: str) -> None:
        """Validate name to ensure it is not empty and there is no duplicated name.

        Args:
            parent: parent iid
            name: name of child to be validate
        """
        if not name:
            raise ValueError("No text detected. Please key in a valid entry.")
        for child in self.tree.get_children(parent):
            if self.tree.item(child, "text") == name:
                raise ValueError("No duplicate names allowed")

    def entry_place_forget(self) -> None:
        """Reset self.entry"""
        self.entry.place_forget()
        self.entry._target_parent = None  # type: ignore
        self.entry._current_item = None  # type: ignore

    def get_tree(self) -> node.Node:
        """Get bigtree node.Node from tkinter tree"""

        def _add_child(_node: node.Node, node_iid: str) -> None:
            for child_iid in self.tree.get_children(node_iid):
                child_name = self.tree.item(child_iid)["text"]
                child_node = node.Node(child_name, parent=_node)
                _add_child(child_node, child_iid)

        root = node.Node(self.tree.item(self.tree_root)["text"])
        _add_child(root, self.tree_root)
        return root

    def print_tree(self) -> None:
        """Export tree, print tree to console. Tree can be constructed into a bigtree object using
        `bigtree.tree.construct.str_to_tree`."""
        tree = self.get_tree()
        tree.show()

    def export_tree(self) -> None:
        """Export tree, print tree dictionary to console. Tree can be constructed into a bigtree object using
        `bigtree.tree.construct.dict_to_tree`"""
        from pprint import pprint

        from bigtree.tree import export

        tree = self.get_tree()
        pprint(export.tree_to_dict(tree))

    def on_return(self, event: TkEvent) -> None:
        """Add or rename node"""
        item_id = getattr(self.entry, "_current_item", None)
        parent = getattr(self.entry, "_target_parent", None)
        name = self.entry.get().strip()
        if item_id:
            # Rename node
            self.validate_name(self.tree.parent(item_id), name)
            self.tree.item(item_id, text=name)
        elif parent:
            # Add node
            self.validate_name(parent, name)
            self.tree.insert(parent, "end", iid=self.get_iid(), text=name)
        self.entry_place_forget()

    def on_plus(self, event: TkEvent = None) -> None:
        """Add node, assigns _target_parent to entry"""
        parent = self.tree.selection()[0] if self.tree.selection() else self.tree_root
        self.tree.item(parent, open=True)

        # Focus entry below parent
        bbox = self.tree.bbox(parent)
        if bbox:
            cum_height = sum(
                [self.tree.bbox(child)[3] for child in self.tree.get_children(parent)]  # type: ignore
            )
            x, y, width, height = bbox
            self.entry.place(
                x=x + 20, y=y + cum_height + height, width=120, height=height
            )
            self.entry.delete(0, tk.END)
            self.entry.focus()
            self.entry._target_parent = parent  # type: ignore

    def on_delete(self, event: TkEvent) -> None:
        """Delete selected node(s)"""
        for item in self.tree.selection():
            if item is not self.tree_root:
                self.tree.delete(item)

    def on_double_click(self, event: TkEvent) -> None:
        """Rename node, assigns _current_item to entry"""
        # Identify item
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return

        # Focus entry on item
        bbox = self.tree.bbox(item_id)
        if bbox:
            x, y, width, height = bbox
            self.entry.place(x=x, y=y, width=width, height=height)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.tree.item(item_id, "text"))
            self.entry.focus()
            self.entry._current_item = item_id  # type: ignore


def render_tree(
    title: str = "Tree Render",
    root_name: str = "Root",
) -> None:
    """Renders tree in windows pop-up, powered by tkinter. Able to export tree to console.

    Viewing Interaction:

    - Expand/Hide Children: Press "Enter" (might have to re-click on item to expand/hide)

    Editing Interaction:

    - Add node: Press "+" / Click "Add Child" button
    - Delete node: Press "Delete"
    - Rename node: Double click
    - Move node: Drag-and-drop to assign as (first) child

    Export Interaction:

    - Print tree to console: Click "Print Tree" button
    - Print tree dictionary to console: Click "Export Tree" button

    Args:
        title: title of render for window pop-up
        root_name: initial root name of tree

    Returns:
        Tree rendered in window pop-up
    """
    root = tk.Tk()
    TkinterTree(root, title, root_name)
    root.mainloop()


if __name__ == "__main__":
    render_tree()

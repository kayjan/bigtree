import tkinter as tk
from tkinter import ttk
from typing import Any

__all__ = ["render_tree"]


class TkinterTree:
    def __init__(
        self,
        root: tk.Tk,
        title: str = "Tree Render",
        root_name: str = "Root",
    ):
        self.counter = 0

        root.title(title)

        tree = ttk.Treeview(root)
        tree.pack(fill=tk.BOTH, expand=True)

        # Hidden entry for inline editing
        entry = tk.Entry(root)
        entry.bind("<Return>", self.on_return)
        entry.bind("<FocusOut>", lambda e: entry.place_forget())
        tree.bind("<Double-1>", self.on_double_click)

        # Insert nodes
        tree_root = tree.insert("", "end", iid=self.get_iid(), text=root_name)
        tree.insert(tree_root, "end", iid=self.get_iid(), text="Child 1")

        # Add button
        tk.Button(root, text="Add Child", command=self.add_node).pack()
        tk.Button(root, text="Delete Child", command=self.delete_node).pack()
        tk.Button(root, text="Export Tree", command=self.export_tree).pack()

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

    def entry_place_forget(self) -> None:
        """Reset self.entry"""
        self.entry.place_forget()
        self.entry._target_parent = None  # type: ignore
        self.entry._current_item = None  # type: ignore

    def add_node(self) -> None:
        """Add node, assigns _target_parent to entry"""
        parent = self.tree.selection()[0] if self.tree.selection() else self.tree_root
        # tree.insert(parent, 'end', text="hello")
        # Position the entry field inline below the parent
        bbox = self.tree.bbox(parent)
        if bbox:
            cum_height = sum(
                [
                    self.tree.bbox(child)[3] if self.tree.bbox(child) else 0  # type: ignore
                    for child in self.tree.get_children(parent)
                ]
            )
            x, y, width, height = bbox
            self.entry.place(
                x=x + 20, y=y + cum_height + height, width=120, height=height
            )
            self.entry.delete(0, tk.END)
            self.entry.focus()
            self.entry._target_parent = parent  # type: ignore

    def delete_node(self) -> None:
        """Delete node"""
        if self.tree.selection():
            self.tree.delete(self.tree.selection()[0])

    def export_tree(self) -> None:
        """Export tree"""
        print(self.tree)

    def on_double_click(self, event: tk.Event[Any]) -> None:
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

    def on_return(self, event: tk.Event[Any]) -> None:
        """Add or rename node"""
        item_id = getattr(self.entry, "_current_item", None)
        name = self.entry.get().strip()
        if not name:
            self.entry_place_forget()
            return
        if item_id:
            # Rename node
            self.tree.item(item_id, text=name)
            self.entry_place_forget()
        else:
            # Add node
            parent = getattr(self.entry, "_target_parent")
            self.tree.insert(parent, "end", text=name, iid=self.get_iid())
            self.entry_place_forget()


def render_tree(
    title: str = "Tree Render",
    root_name: str = "Root",
) -> None:
    """Renders tree with tkinter, exports tree to JSON file.

    Interaction:

    - Add node: Press "Enter" / Click "Add Child" button
    - Rename node: Double click
    - Delete node: Press "Delete"

    Args:
        title: title of tkinter render for window pop-up
        root_name: initial root name of tree

    Returns:
        Tree render in window pop-up
    """
    root = tk.Tk()
    TkinterTree(root, title, root_name)
    root.mainloop()


if __name__ == "__main__":
    """
    Action	Method
    Add item	tree.insert()
    Modify item	tree.item(item_id, ...)
    Delete item	tree.delete(item_id) with Allow deleting nodes with a button or keyboard key
    Move item	tree.move(item_id, new_parent, index)
    Get children	tree.get_children(item_id)
    Set focus / selection	tree.focus(), tree.selection()

    Prevent duplicated names
    Add right click for renaming or deleting or adding nodes
    Add adding nodes via Enter button tree.selection()
    """

    render_tree()

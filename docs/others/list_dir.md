# List Directory

> Topic: construct

Display folder and file directories in a tree representation using bigtree.

To list all directories recursively, we can use the `glob` built-in Python package to extract a list of paths.

```python
import glob
from bigtree import Tree

# Get all directories recursively
path_list = []
for f in glob.glob("./**/*.py", recursive=True):
    path_list.append(f)

# Construct tree
tree = Tree.from_list(sorted(path_list))

# View tree
tree.show(max_depth=3)
```

Alternatively, you can construct the tree using parent-children relation using `pathlib` built-in Python package.

```python
from pathlib import Path
from bigtree import Node


def build_tree(path: Path, depth: int, parent: Node | None = None):
    if depth:
        new_parent = Node(
            path.name if parent else str(root_folder),
            parent=parent,
        )

        if path.is_dir():
            new_parent.set_attrs({"icon": ":open_file_folder:"})
            try:
                for child_path in sorted(
                    path.iterdir(),
                    key=lambda p: (p.is_file(), p.name.lower())
                ):
                    build_tree(child_path, depth - 1, new_parent)
            except PermissionError:
                new_parent.set_attrs({"colour": "red"})
        else:
            new_parent.set_attrs({"icon": ":memo:"})
        return new_parent
    return parent

root_folder = Path(".")
tree = build_tree(root_folder, depth=3)
tree.show(rich=True, node_format_attr="colour", icon_prefix_attr="icon")
```

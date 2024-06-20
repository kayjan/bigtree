# Merging Trees

To merge two separate trees into one, we can use the tree modify module.

In this example, we are merging two trees that have similar node `Pictures`.
Children of node `Pictures` from both trees are retained as long as `merge_children=True` is set.
If only children of the other tree are desired, set `overriding=True` instead.

```python hl_lines="18-24"
from bigtree import copy_nodes_from_tree_to_tree, str_to_tree

# Construct trees
downloads_folder = str_to_tree("""
Downloads
├── Pictures
│   └── photo1.jpg
└── file1.doc
""")

documents_folder = str_to_tree("""
Documents
└── Pictures
    └── photo2.jpg
""")

# Merge trees
copy_nodes_from_tree_to_tree(
    from_tree=documents_folder,
    to_tree=downloads_folder,
    from_paths=["Documents/Pictures"],
    to_paths=["Downloads/Pictures"],
    merge_children=True,  # set overriding=True to override existing children
)

# Validate tree structure
downloads_folder.show()
# Downloads
# ├── Pictures
# │   ├── photo1.jpg
# │   └── photo2.jpg
# └── file1.doc
```

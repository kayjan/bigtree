# Merging Trees

To merge two separate trees into one, we can use the tree modify module.

In this example, we are merging two trees that have similar node `b`.
Children of node `b` from both trees are retained as long as `merge_children=True` is set.
If only children of other tree is desired, set `overriding=True` instead.

```python
from bigtree import Node, copy_nodes_from_tree_to_tree

# Construct trees
downloads_folder = Node("Downloads")
pictures_folder = Node("Pictures", parent=downloads_folder)
photo1 = Node("photo1.jpg", parent=pictures_folder)
file1 = Node("file1.doc", parent=downloads_folder)

documents_folder = Node("Documents")
pictures_folder = Node("Pictures", parent=documents_folder)
photo2 = Node("photo2.jpg", parent=pictures_folder)

# Validate tree structure
downloads_folder.show()
# Downloads
# ├── Pictures
# │   └── photo1.jpg
# └── file1.doc

documents_folder.show()
# Documents
# └── Pictures
#     └── photo2.jpg

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

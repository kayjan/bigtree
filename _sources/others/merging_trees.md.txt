# Merging Trees

To merge two separate trees into one, we can use the tree modify module.

In this example, we are merging two trees that have similar node `b`.
Children of node `b` from both trees are retained as long as `merge_children=True` is set.
If only children of other tree is desired, set `overriding=True` instead.

```python
from bigtree import Node, print_tree, copy_nodes_from_tree_to_tree

# Construct trees
root1 = Node("a")
b1 = Node("b", parent=root1)
c1 = Node("c", parent=root1)
d1 = Node("d", parent=b1)

b2 = Node("b")
e2 = Node("e", parent=b2)

# Validate tree structure
print_tree(root1)
# a
# ├── b
# │   └── d
# └── c

print_tree(b2)
# b
# └── e

# Merge trees
copy_nodes_from_tree_to_tree(
    from_tree=b2,
    to_tree=root1,
    from_paths=["b"],
    to_paths=["a/b"],
    merge_children=True,  # set overriding=True to override existing children
)

# Validate tree structure
print_tree(root1)
# a
# ├── b
# │   ├── d
# │   └── e
# └── c
```

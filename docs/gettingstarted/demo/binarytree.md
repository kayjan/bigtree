---
title: Binary Tree Demonstration
---

# 📋 Binary Tree Demonstration

Conceptually, binary trees are made up of binary nodes, and they are synonymous; a tree is a node. In bigtree
implementation, node refers to the `BinaryNode` class, whereas tree refers to the `BinaryTree` class. BinaryTree is
implemented as a wrapper around a BinaryNode to implement tree-level methods for a more intuitive API.

Compared to nodes in tree, nodes in Binary Tree are only allowed maximum of 2 children.
Since BinaryNode extends from Node, construct, traverse, search, export methods from Node are applicable to
Binary Tree as well.

## Construct Binary Tree

### 1. From BinaryNode

BinaryNode can be linked to each other with `parent`, `children`, `left`, and `right` setter methods,
or using bitshift operator with the convention `parent_node >> child_node` or `child_node << parent_node`.

```python hl_lines="6-10"
from bigtree import BinaryNode, BinaryTree

e = BinaryNode(5)
d = BinaryNode(4)
c = BinaryNode(3)
b = BinaryNode(2, left=d, right=e)
a = BinaryNode(1, children=[b, c])
f = BinaryNode(6, parent=c)
g = BinaryNode(7, parent=c)
h = BinaryNode(8, parent=d)

graph = BinaryTree(a).to_dot(node_colour="gold")
graph.write_png("assets/demo/binarytree.png")
```

![Sample Binary Tree Output](https://github.com/kayjan/bigtree/raw/master/assets/demo/binarytree.png "Sample Binary Tree Output")

### 2. From list

Construct nodes only, list has similar format as `heapq` list.

```python hl_lines="4"
from bigtree import BinaryTree

nums_list = [1, 2, 3, 4, 5, 6, 7, 8]
tree = BinaryTree.from_heapq_list(nums_list)
tree.show()
# 1
# ├── 2
# │   ├── 4
# │   │   └── 8
# │   └── 5
# └── 3
#     ├── 6
#     └── 7
```

## Traverse Binary Tree

In addition to the traversal methods in the usual tree, binary tree includes in-order traversal method.

```python hl_lines="15 18 21 24 27 30 33"
from bigtree import BinaryTree

nums_list = [1, 2, 3, 4, 5, 6, 7, 8]
tree = tree.from_heapq_list(nums_list)
tree.show()
# 1
# ├── 2
# │   ├── 4
# │   │   └── 8
# │   └── 5
# └── 3
#     ├── 6
#     └── 7

[node.node_name for node in tree.inorder_iter()]
# ['8', '4', '2', '5', '1', '6', '3', '7']

[node.node_name for node in tree.preorder_iter()]
# ['1', '2', '4', '8', '5', '3', '6', '7']

[node.node_name for node in tree.postorder_iter()]
# ['8', '4', '5', '2', '6', '7', '3', '1']

[node.node_name for node in tree.levelorder_iter()]
# ['1', '2', '3', '4', '5', '6', '7', '8']

[[node.node_name for node in node_group] for node_group in tree.levelordergroup_iter()]
# [['1'], ['2', '3'], ['4', '5', '6', '7'], ['8']]

[node.node_name for node in tree.zigzag_iter()]
# ['1', '3', '2', '4', '5', '6', '7', '8']

[[node.node_name for node in node_group] for node_group in tree.zigzaggroup_iter()]
# [['1'], ['3', '2'], ['4', '5', '6', '7'], ['8']]
```

# 📋 Binary Tree Demonstration

Compared to nodes in tree, nodes in Binary Tree are only allowed maximum of 2 children.
Since BinaryNode extends from Node, construct, traverse, search, export methods from Node are applicable to
Binary Tree as well.

## Construct Binary Tree

### 1. From BinaryNode

BinaryNode can be linked to each other with `parent`, `children`, `left`, and `right` setter methods,
or using bitshift operator with the convention `parent_node >> child_node` or `child_node << parent_node`.

{emphasize-lines="6-10"}
```python
from bigtree import BinaryNode, tree_to_dot

e = BinaryNode(5)
d = BinaryNode(4)
c = BinaryNode(3)
b = BinaryNode(2, left=d, right=e)
a = BinaryNode(1, children=[b, c])
f = BinaryNode(6, parent=c)
g = BinaryNode(7, parent=c)
h = BinaryNode(8, parent=d)

graph = tree_to_dot(a, node_colour="gold")
graph.write_png("assets/demo/binarytree.png")
```

![Sample DAG Output](https://github.com/kayjan/bigtree/raw/master/assets/demo/binarytree.png)

### 2. From list

Construct nodes only, list has similar format as `heapq` list.

{emphasize-lines="4"}
```python
from bigtree import list_to_binarytree

nums_list = [1, 2, 3, 4, 5, 6, 7, 8]
root = list_to_binarytree(nums_list)
root.show()
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

{emphasize-lines="24,27,30,33,36,39,42"}
```python
from bigtree import (
    inorder_iter,
    levelorder_iter,
    levelordergroup_iter,
    list_to_binarytree,
    postorder_iter,
    preorder_iter,
    zigzag_iter,
    zigzaggroup_iter,
)

nums_list = [1, 2, 3, 4, 5, 6, 7, 8]
root = list_to_binarytree(nums_list)
root.show()
# 1
# ├── 2
# │   ├── 4
# │   │   └── 8
# │   └── 5
# └── 3
#     ├── 6
#     └── 7

[node.node_name for node in inorder_iter(root)]
# ['8', '4', '2', '5', '1', '6', '3', '7']

[node.node_name for node in preorder_iter(root)]
# ['1', '2', '4', '8', '5', '3', '6', '7']

[node.node_name for node in postorder_iter(root)]
# ['8', '4', '5', '2', '6', '7', '3', '1']

[node.node_name for node in levelorder_iter(root)]
# ['1', '2', '3', '4', '5', '6', '7', '8']

[[node.node_name for node in node_group] for node_group in levelordergroup_iter(root)]
# [['1'], ['2', '3'], ['4', '5', '6', '7'], ['8']]

[node.node_name for node in zigzag_iter(root)]
# ['1', '3', '2', '4', '5', '6', '7', '8']

[[node.node_name for node in node_group] for node_group in zigzaggroup_iter(root)]
# [['1'], ['3', '2'], ['4', '5', '6', '7'], ['8']]
```

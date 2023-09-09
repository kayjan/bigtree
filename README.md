# Big Tree Python Package

Tree Implementation for Python, integrated with Python list, dictionary, and pandas DataFrame.

It is pythonic, making it easy to learn and extendable to many types of workflows.

----

Related Links:
- [Documentation](https://bigtree.readthedocs.io/en/latest/)
- [GitHub](https://github.com/kayjan/bigtree/)
- [Changelog](https://github.com/kayjan/bigtree/blob/master/CHANGELOG.md)
- [Issues](https://github.com/kayjan/bigtree/issues)
- [Discussions](https://github.com/kayjan/bigtree/discussions)
- [Contributing](https://bigtree.readthedocs.io/en/latest/others/contributing.html)
- [PyPI](https://pypi.org/project/bigtree/)
- Articles
  - [Python Tree Implementation with BigTree](https://towardsdatascience.com/python-tree-implementation-with-bigtree-13cdabd77adc#245a-94ae81f0b3f1)
- <div><p>If you want to support bigtree, <a href="https://www.buymeacoffee.com/kayjan"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" style="vertical-align:middle"></a></p></div>

----

## Components
There are 3 segments to Big Tree consisting of Tree, Binary Tree, and Directed Acyclic Graph (DAG) implementation.


For **Tree** implementation, there are 9 main components.

1. [**Node**](https://bigtree.readthedocs.io/en/latest/node.html)
   1. ``BaseNode``, extendable class
   2. ``Node``, BaseNode with node name attribute
2. [**Constructing Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/construct.html)
   1. From *str*, using tree in string display format
   2. From *list*, using paths or parent-child tuples
   3. From *nested dictionary*, using path or recursive structure
   4. From *pandas DataFrame*, using paths or parent-child columns
   5. Add nodes to existing tree using path string
   6. Add nodes and attributes to existing tree using dictionary or pandas DataFrame, using path
   7. Add only attributes to existing tree using dictionary or pandas DataFrame, using node name
3. [**Traversing Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/iterators.html)
   1. Pre-Order Traversal
   2. Post-Order Traversal
   3. Level-Order Traversal
   4. Level-Order-Group Traversal
   5. ZigZag Traversal
   6. ZigZag-Group Traversal
4. [**Modifying Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/modify.html)
   1. Shift nodes from location to destination
   2. Copy nodes from location to destination
   3. Copy nodes from one tree to another
5. [**Tree Search**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/search.html)
   1. Find multiple nodes based on name, partial path, relative path, attribute value, user-defined condition
   2. Find single nodes based on name, partial path, relative path, full path, attribute value, user-defined condition
   3. Find multiple child nodes based on user-defined condition
   4. Find single child node based on name, user-defined condition
6. [**Helper Function**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/helper.html)
   1. Cloning tree to another `Node` type
   2. Prune tree
   3. Get difference between two trees
7. [**Plotting Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/plot.html)
   1. Enhanced Reingold Tilford Algorithm to retrieve (x, y) coordinates for a tree structure
8. [**Exporting Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/export.html)
   1. Print to console
   2. Export to *dictionary*, *nested dictionary*, or *pandas DataFrame*
   3. Export tree to dot (can save to .dot, .png, .svg, .jpeg files)
   4. Export tree to Pillow (can save to .png, .jpg)
9. [**Workflows**](https://bigtree.readthedocs.io/en/latest/workflows.html)
   1. Sample workflows for tree demonstration!

For **Binary Tree** implementation, there are 3 main components.
Binary Node inherits from Node, so the components in Tree implementation are also available in Binary Tree.

1. [**Node**](https://bigtree.readthedocs.io/en/latest/node.html)
   1. ``BinaryNode``, Node with binary tree rules
2. [**Constructing Binary Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/binarytree/construct.html)
   1. From *list*, using flattened list structure
3. [**Traversing Binary Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/iterators.html)
   1. In-Order Traversal

For **Directed Acyclic Graph (DAG)** implementation, there are 4 main components.

1. [**Node**](https://bigtree.readthedocs.io/en/latest/node.html)
   1. ``DAGNode``, extendable class for constructing Directed Acyclic Graph (DAG)
2. [**Constructing DAG**](https://bigtree.readthedocs.io/en/latest/bigtree/dag/construct.html)
   1. From *list*, containing parent-child tuples
   2. From *nested dictionary*
   3. From *pandas DataFrame*
3. [**Traversing DAG**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/iterators.html)
   1. Generic traversal method
4. [**Exporting DAG**](https://bigtree.readthedocs.io/en/latest/bigtree/dag/export.html)
   1. Export to *list*, *dictionary*, or *pandas DataFrame*
   2. Export DAG to dot (can save to .dot, .png, .svg, .jpeg files)

----

## Installation

To install `bigtree`, run the following line in command prompt:

```shell
$ pip install bigtree
```

If tree needs to use pandas methods, it requires additional dependencies.
Run the following line in command prompt:

```shell
$ pip install 'bigtree[pandas]'
```

If tree needs to be exported to image, it requires additional dependencies.
Run the following lines in command prompt:

```shell
$ pip install 'bigtree[image]'
$ brew install gprof2dot  # for MacOS
$ conda install graphviz  # for Windows
```

Alternatively, install all optional dependencies with the following line in command prompt:

```shell
$ pip install 'bigtree[all]'
```

----

## Tree Demonstration

Here are some codes to get started.

### Construct Tree

Nodes can have attributes if they are initialized from `Node`, *dictionary*, or *pandas DataFrame*.

1. **From `Node`**

Nodes can be linked to each other with `parent` and `children` setter methods,
or using bitshift operator with the convention `parent_node >> child_node` or `child_node << parent_node`.

```python
from bigtree import Node, tree_to_dot

root = Node("a")
b = Node("b")
c = Node("c")
d = Node("d")

root.children = [b, c]
d.parent = b

root.show()
# a
# ├── b
# │   └── d
# └── c

graph = tree_to_dot(root, node_colour="gold")
graph.write_png("assets/demo_tree.png")
```

![Sample Tree Output](https://github.com/kayjan/bigtree/raw/master/assets/demo_tree.png)

```python
from bigtree import Node

root = Node("a")
b = Node("b")
c = Node("c")
d = Node("d")

root >> b
root >> c
d << b

root.show()
# a
# ├── b
# │   └── d
# └── c
```

Alternatively, we can directly pass `parent` or `children` argument.

```python
from bigtree import Node

b = Node("b")
c = Node("c")
d = Node("d", parent=b)
root = Node("a", children=[b, c])

root.show(style="ascii")
# a
# |-- b
# |   +-- d
# +-- c
```

2. **From *str***

Construct nodes only.

```python
from bigtree import str_to_tree

tree_str = """
a
├── b
│   ├── d
│   └── e
│       ├── g
│       └── h
└── c
    └── f
"""
root = str_to_tree(tree_str, tree_prefix_list=["├──", "└──"])
root.show()
# a
# ├── b
# │   ├── d
# │   └── e
# │       ├── g
# │       └── h
# └── c
#     └── f
```

3. **From *list***

Construct nodes only, list can contain either full paths or tuples of parent-child names.

```python
from bigtree import list_to_tree, list_to_tree_by_relation

root = list_to_tree(["a/b/d", "a/c"])
root.show()
# a
# ├── b
# │   └── d
# └── c

root = list_to_tree_by_relation([("a", "b"), ("a", "c"), ("b", "d")])
root.show()
# a
# ├── b
# │   └── d
# └── c
```

4. **From *nested dictionary***

Construct nodes with attributes, `key`: path, `value`: dict of node attribute names and attribute values.

```python
from bigtree import dict_to_tree

path_dict = {
   "a": {"age": 90},
   "a/b": {"age": 65},
   "a/c": {"age": 60},
   "a/b/d": {"age": 40},
}

root = dict_to_tree(path_dict)
root.show(attr_list=["age"])
# a [age=90]
# ├── b [age=65]
# │   └── d [age=40]
# └── c [age=60]
```

5. **From *nested recursive dictionary***

Construct nodes with attributes, `key`: node attribute names, `value`: node attribute values, and list of
children (recursive).

```python
from bigtree import nested_dict_to_tree

path_dict = {
   "name": "a",
   "age": 90,
   "children": [
      {
         "name": "b",
         "age": 65,
         "children": [
            {"name": "d", "age": 40},
         ],
      },
      {"name": "c", "age": 60},
   ],
}

root = nested_dict_to_tree(path_dict)
root.show(attr_list=["age"])
# a [age=90]
# ├── b [age=65]
# │   └── d [age=40]
# └── c [age=60]
```

6. **From *pandas DataFrame***

Construct nodes with attributes, *pandas DataFrame* can contain either path column or parent-child columns,
and attribute columns.

```python
import pandas as pd

from bigtree import dataframe_to_tree, dataframe_to_tree_by_relation

data = pd.DataFrame(
   [
      ["a", 90],
      ["a/b", 65],
      ["a/c", 60],
      ["a/b/d", 40],
   ],
   columns=["path", "age"],
)

root = dataframe_to_tree(data)
root.show(attr_list=["age"])
# a [age=90]
# ├── b [age=65]
# │   └── d [age=40]
# └── c [age=60]

data = pd.DataFrame(
   [
      ["a", None, 90],
      ["b", "a", 65],
      ["c", "a", 60],
      ["d", "b", 40],
   ],
   columns=["child", "parent", "age"],
)

root = dataframe_to_tree_by_relation(data)
root.show(attr_list=["age"])
# a [age=90]
# ├── b [age=65]
# │   └── d [age=40]
# └── c [age=60]
```

> If tree is already created, attributes can still be added using dictionary or pandas DataFrame!

### Print Tree

After tree is constructed, it can be viewed by printing to console using `show` method directly.
Alternatively, the `print_tree` method can be used.

```python
from bigtree import Node, print_tree

root = Node("a", age=90, gender="F")
b = Node("b", age=65, gender="M", parent=root)
c = Node("c", age=60, gender="M", parent=root)
d = Node("d", age=40, gender="F", parent=b)
e = Node("e", age=35, gender="M", parent=b)
print_tree(root)
# a
# ├── b
# │   ├── d
# │   └── e
# └── c

# Print subtree
print_tree(root, node_name_or_path="b")
# b
# ├── d
# └── e

print_tree(root, max_depth=2)
# a
# ├── b
# └── c

# Print attributes
print_tree(root, attr_list=["age"])
# a [age=90]
# ├── b [age=65]
# │   ├── d [age=40]
# │   └── e [age=35]
# └── c [age=60]

print_tree(root, attr_list=["age"], attr_bracket=["*(", ")"])
# a *(age=90)
# ├── b *(age=65)
# │   ├── d *(age=40)
# │   └── e *(age=35)
# └── c *(age=60)

print_tree(root, all_attrs=True)
# a [age=90, gender=F]
# ├── b [age=65, gender=M]
# │   ├── d [age=40, gender=F]
# │   └── e [age=35, gender=M]
# └── c [age=60, gender=M]

# Available styles
print_tree(root, style="ansi")
# a
# |-- b
# |   |-- d
# |   `-- e
# `-- c

print_tree(root, style="ascii")
# a
# |-- b
# |   |-- d
# |   +-- e
# +-- c

print_tree(root, style="const")
# a
# ├── b
# │   ├── d
# │   └── e
# └── c

print_tree(root, style="const_bold")
# a
# ┣━━ b
# ┃   ┣━━ d
# ┃   ┗━━ e
# ┗━━ c

print_tree(root, style="rounded")
# a
# ├── b
# │   ├── d
# │   ╰── e
# ╰── c

print_tree(root, style="double")
# a
# ╠══ b
# ║   ╠══ d
# ║   ╚══ e
# ╚══ c

print_tree(
    root,
    style="custom",
    custom_style=("|   ", "|-- ", "+-- "),
)
# a
# |-- b
# |   |-- d
# |   +-- e
# +-- c
```

### Traverse Tree

Tree can be traversed using pre-order, post-order, level-order, level-order-group, zigzag, zigzag-group traversal methods.

```python
from bigtree import Node, preorder_iter, postorder_iter, levelorder_iter, levelordergroup_iter, zigzag_iter, zigzaggroup_iter

root = Node("a")
b = Node("b", parent=root)
c = Node("c", parent=root)
d = Node("d", parent=b)
e = Node("e", parent=b)
root.show()
# a
# ├── b
# │   ├── d
# │   └── e
# └── c

[node.name for node in preorder_iter(root)]
# ['a', 'b', 'd', 'e', 'c']

[node.name for node in postorder_iter(root)]
# ['d', 'e', 'b', 'c', 'a']

[node.name for node in levelorder_iter(root)]
# ['a', 'b', 'c', 'd', 'e']

[[node.name for node in node_group] for node_group in levelordergroup_iter(root)]
# [['a'], ['b', 'c'], ['d', 'e']]

[node.name for node in zigzag_iter(root)]
# ['a', 'c', 'b', 'd', 'e']

[[node.name for node in node_group] for node_group in zigzaggroup_iter(root)]
# [['a'], ['c', 'b'], ['d', 'e']]
```

### Modify Tree

Nodes can be shifted or copied from one path to another.

```python
from bigtree import Node, shift_nodes

root = Node("a")
b = Node("b", parent=root)
c = Node("c", parent=root)
d = Node("d", parent=root)
root.show()
# a
# ├── b
# ├── c
# └── d

shift_nodes(
   tree=root,
   from_paths=["a/c", "a/d"],
   to_paths=["a/b/c", "a/dummy/d"],
)
root.show()
# a
# ├── b
# │   └── c
# └── dummy
#     └── d
```

```python
from bigtree import Node, copy_nodes

root = Node("a")
b = Node("b", parent=root)
c = Node("c", parent=root)
d = Node("d", parent=root)
root.show()
# a
# ├── b
# ├── c
# └── d

copy_nodes(
   tree=root,
   from_paths=["a/c", "a/d"],
   to_paths=["a/b/c", "a/dummy/d"],
)
root.show()
# a
# ├── b
# │   └── c
# ├── c
# ├── d
# └── dummy
#     └── d
```

Nodes can also be copied between two different trees.

```python
from bigtree import Node, copy_nodes_from_tree_to_tree
root = Node("a")
b = Node("b", parent=root)
c = Node("c", parent=root)
d = Node("d", parent=root)
root.show()
# a
# ├── b
# ├── c
# └── d

root_other = Node("aa")
copy_nodes_from_tree_to_tree(
   from_tree=root,
   to_tree=root_other,
   from_paths=["a/b", "a/c", "a/d"],
   to_paths=["aa/b", "aa/b/c", "aa/dummy/d"],
)
root_other.show()
# aa
# ├── b
# │   └── c
# └── dummy
#     └── d
```

### Tree Search

One or multiple nodes can be search based on name, path, attribute value, or user-defined condition.

To find a single node,
```python
from bigtree import Node, find, find_name, find_path, find_relative_path, find_full_path, find_attr
root = Node("a", age=90)
b = Node("b", age=65, parent=root)
c = Node("c", age=60, parent=root)
d = Node("d", age=40, parent=c)
root.show(attr_list=["age"])
# a [age=90]
# ├── b [age=65]
# └── c [age=60]
#     └── d [age=40]

find(root, lambda node: node.age == 60)
# Node(/a/c, age=60)

find_name(root, "d")
# Node(/a/c/d, age=40)

find_path(root, "/c/d")  # partial path
# Node(/a/c/d, age=40)

find_relative_path(c, "../b")  # relative path
# (Node(/a/b, age=65),)

find_full_path(root, "a/c/d")  # full path
# Node(/a/c/d, age=40)

find_attr(root, "age", 40)
# Node(/a/c/d, age=40)
```

To find multiple nodes,
```python
from bigtree import Node, findall, find_names, find_relative_path, find_paths, find_attrs
root = Node("a", age=90)
b = Node("b", age=65, parent=root)
c = Node("c", age=60, parent=root)
d = Node("c", age=40, parent=c)
root.show(attr_list=["age"])
# a [age=90]
# ├── b [age=65]
# └── c [age=60]
#     └── c [age=40]

findall(root, lambda node: node.age >= 65)
# (Node(/a, age=90), Node(/a/b, age=65))

find_names(root, "c")
# (Node(/a/c, age=60), Node(/a/c/c, age=40))

find_relative_path(c, "../*")  # relative path
# (Node(/a/b, age=65), Node(/a/c, age=60))

find_paths(root, "/c")  # partial path
# (Node(/a/c, age=60), Node(/a/c/c, age=40))

find_attrs(root, "age", 40)
# (Node(/a/c/c, age=40),)
```

It is also possible to search for one or more child node(s) based on attributes, and the search will be faster as
this does not require traversing the whole tree to find the node(s).

```python
from bigtree import Node, find_children, find_child, find_child_by_name
root = Node("a", age=90)
b = Node("b", age=65, parent=root)
c = Node("c", age=60, parent=root)
d = Node("c", age=40, parent=c)
root.show(attr_list=["age"])
# a [age=90]
# ├── b [age=65]
# └── c [age=60]
#     └── c [age=40]

find_children(root, lambda node: node.age >= 60)
# (Node(/a/b, age=65), Node(/a/c, age=60))

find_child(root, lambda node: node.name == "c")
# Node(/a/c, age=60)

find_child_by_name(root, "c")
# Node(/a/c, age=60)

find_child_by_name(c, "c")
# Node(/a/c/c, age=40)
```

### Helper Utility

There following are helper functions for cloning tree to another `Node` type, pruning tree, and getting difference
between two trees.

```python
from bigtree import BaseNode, Node, clone_tree, prune_tree, get_tree_diff

# Cloning tree from `BaseNode` to `Node` type
root = BaseNode(name="a")
b = BaseNode(name="b", parent=root)
clone_tree(root, Node)
# Node(/a, )

# Prune tree to only path a/b
root = Node("a")
b = Node("b", parent=root)
c = Node("c", parent=root)
root.show()
# a
# ├── b
# └── c

root_pruned = prune_tree(root, "a/b")
root_pruned.show()
# a
# └── b

# Get difference between two trees
root = Node("a")
b = Node("b", parent=root)
c = Node("c", parent=root)
root.show()
# a
# ├── b
# └── c

root_other = Node("a")
b_other = Node("b", parent=root_other)
root_other.show()
# a
# └── b

tree_diff = get_tree_diff(root, root_other)
tree_diff.show()
# a
# └── c (-)

tree_diff = get_tree_diff(root, root_other, only_diff=False)
tree_diff.show()
# a
# ├── b
# └── c (-)
```

### Export Tree

Tree can be exported to another data type.

1. *Export to **nested dictionary***
2. *Export to **nested recursive dictionary***
3. *Export to **pandas DataFrame***
4. *Export to **dot** (and png)*
5. *Export to **Pillow** (and png)*

```python
from bigtree import Node, tree_to_dict, tree_to_nested_dict, tree_to_dataframe, tree_to_dot, tree_to_pillow

root = Node("a", age=90)
b = Node("b", age=65, parent=root)
c = Node("c", age=60, parent=root)
d = Node("d", age=40, parent=b)
e = Node("e", age=35, parent=b)
root.show()
# a
# ├── b
# │   ├── d
# │   └── e
# └── c

tree_to_dict(
   root,
   name_key="name",
   parent_key="parent",
   attr_dict={"age": "person age"}
)
# {
#    '/a': {'name': 'a', 'parent': None, 'person age': 90},
#    '/a/b': {'name': 'b', 'parent': 'a', 'person age': 65},
#    '/a/b/d': {'name': 'd', 'parent': 'b', 'person age': 40},
#    '/a/b/e': {'name': 'e', 'parent': 'b', 'person age': 35},
#    '/a/c': {'name': 'c', 'parent': 'a', 'person age': 60}
# }

tree_to_nested_dict(root, all_attrs=True)
# {
#    'name': 'a',
#    'age': 90,
#    'children': [
#       {
#          'name': 'b',
#          'age': 65,
#          'children': [
#             {
#                'name': 'd',
#                'age': 40
#             },
#             {
#                'name': 'e',
#                'age': 35
#             }
#          ]
#       },
#       {
#          'name': 'c',
#          'age': 60
#       }
#    ]
# }

tree_to_dataframe(
   root,
   name_col="name",
   parent_col="parent",
   path_col="path",
   attr_dict={"age": "person age"}
)
#      path name parent  person age
# 0      /a    a   None          90
# 1    /a/b    b      a          65
# 2  /a/b/d    d      b          40
# 3  /a/b/e    e      b          35
# 4    /a/c    c      a          60

graph = tree_to_dot(root, node_colour="gold")
graph.write_png("assets/demo.png")

pillow_image = tree_to_pillow(root)
pillow_image.save("assets/demo_pillow.png")
```

- demo.png

![Sample Dot Image Output](https://github.com/kayjan/bigtree/raw/master/assets/demo.png)

- demo_pillow.png

![Sample Pillow Image Output](https://github.com/kayjan/bigtree/raw/master/assets/demo_pillow.png)

----

## Binary Tree Demonstration

Compared to nodes in tree, nodes in Binary Tree are only allowed maximum of 2 children.
Since BinaryNode extends from Node, construct, traverse, search, export methods from Node are applicable to
Binary Tree as well.

### Construct Binary Tree

1. **From `BinaryNode`**

BinaryNode can be linked to each other with `parent`, `children`, `left`, and `right` setter methods,
or using bitshift operator with the convention `parent_node >> child_node` or `child_node << parent_node`.

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
graph.write_png("assets/demo_binarytree.png")
```

![Sample DAG Output](https://github.com/kayjan/bigtree/raw/master/assets/demo_binarytree.png)

2. **From *list***

Construct nodes only, list has similar format as `heapq` list.

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

### Traverse Binary Tree

In addition to the traversal methods in the usual tree, binary tree includes in-order traversal method.

```python
from bigtree import list_to_binarytree, inorder_iter, preorder_iter, postorder_iter, levelorder_iter, levelordergroup_iter, zigzag_iter, zigzaggroup_iter

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

[node.name for node in inorder_iter(root)]
# ['8', '4', '2', '5', '1', '6', '3', '7']

[node.name for node in preorder_iter(root)]
# ['1', '2', '4', '8', '5', '3', '6', '7']

[node.name for node in postorder_iter(root)]
# ['8', '4', '5', '2', '6', '7', '3', '1']

[node.name for node in levelorder_iter(root)]
# ['1', '2', '3', '4', '5', '6', '7', '8']

[[node.name for node in node_group] for node_group in levelordergroup_iter(root)]
# [['1'], ['2', '3'], ['4', '5', '6', '7'], ['8']]

[node.name for node in zigzag_iter(root)]
# ['1', '3', '2', '4', '5', '6', '7', '8']

[[node.name for node in node_group] for node_group in zigzaggroup_iter(root)]
# [['1'], ['3', '2'], ['4', '5', '6', '7'], ['8']]
```

----

## DAG Demonstration

Compared to nodes in tree, nodes in DAG are able to have multiple parents.

### Construct DAG

1. **From `DAGNode`**

DAGNode can be linked to each other with `parents` and `children` setter methods,
or using bitshift operator with the convention `parent_node >> child_node` or `child_node << parent_node`.

```python
from bigtree import DAGNode, dag_to_dot

a = DAGNode("a")
b = DAGNode("b")
c = DAGNode("c", parents=[a, b])
d = DAGNode("d", parents=[a, c])
e = DAGNode("e", parents=[d])
f = DAGNode("f", parents=[c, d])
h = DAGNode("h")
g = DAGNode("g", parents=[c], children=[h])

graph = dag_to_dot(a, node_colour="gold")
graph.write_png("assets/demo_dag.png")
```

![Sample DAG Output](https://github.com/kayjan/bigtree/raw/master/assets/demo_dag.png)

2. **From *list***

Construct nodes only, list contains parent-child tuples.

```python
from bigtree import list_to_dag, dag_iterator

relations_list = [
   ("a", "c"),
   ("a", "d"),
   ("b", "c"),
   ("c", "d"),
   ("d", "e")
]
dag = list_to_dag(relations_list)
print([(parent.node_name, child.node_name) for parent, child in dag_iterator(dag)])
# [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]
```

3. **From *nested dictionary***

Construct nodes with attributes, `key`: child name, `value`: dict of parent name, child node attributes.

```python
from bigtree import dict_to_dag, dag_iterator

relation_dict = {
   "a": {"step": 1},
   "b": {"step": 1},
   "c": {"parents": ["a", "b"], "step": 2},
   "d": {"parents": ["a", "c"], "step": 2},
   "e": {"parents": ["d"], "step": 3},
}
dag = dict_to_dag(relation_dict, parent_key="parents")
print([(parent.node_name, child.node_name) for parent, child in dag_iterator(dag)])
# [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]
```

4. **From *pandas DataFrame***

Construct nodes with attributes, *pandas DataFrame* contains child column, parent column, and attribute columns.

```python
import pandas as pd
from bigtree import dataframe_to_dag, dag_iterator

path_data = pd.DataFrame([
   ["a", None, 1],
   ["b", None, 1],
   ["c", "a", 2],
   ["c", "b", 2],
   ["d", "a", 2],
   ["d", "c", 2],
   ["e", "d", 3],
],
   columns=["child", "parent", "step"]
)
dag = dataframe_to_dag(path_data)
print([(parent.node_name, child.node_name) for parent, child in dag_iterator(dag)])
# [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]
```

----

## Demo Usage

There are existing implementations of workflows to showcase how `bigtree` can be used!

### To Do Application
There are functions to:
- Add or remove list to To-Do application
- Add or remove item to list, default list is the 'General' list
- Prioritize a list/item by reordering them as first list/item
- Save and import To-Do application to and from an external JSON file
- Show To-Do application, which prints tree to console

```python
from bigtree import AppToDo
app = AppToDo("To Do App")
app.add_item(item_name="Homework 1", list_name="School")
app.add_item(item_name=["Milk", "Bread"], list_name="Groceries", description="Urgent")
app.add_item(item_name="Cook")
app.show()
# To Do App
# ├── School
# │   └── Homework 1
# ├── Groceries
# │   ├── Milk [description=Urgent]
# │   └── Bread [description=Urgent]
# └── General
#   └── Cook

app.save("list.json")
app2 = AppToDo.load("list.json")
```

### Calendar Application

There are functions to:
- Add or remove event from Calendar
- Find event by name, or name and date
- Display calendar, which prints events to console
- Export calendar to pandas DataFrame

```python
import datetime as dt
from bigtree import Calendar
calendar = Calendar("My Calendar")
calendar.add_event("Gym", "2023-01-01 18:00")
calendar.add_event("Dinner", "2023-01-01", date_format="%Y-%m-%d", budget=20)
calendar.add_event("Gym", "2023-01-02 18:00")
calendar.show()
# My Calendar
# 2023-01-01 00:00:00 - Dinner (budget: 20)
# 2023-01-01 18:00:00 - Gym
# 2023-01-02 18:00:00 - Gym

calendar.find_event("Gym")
# 2023-01-01 18:00:00 - Gym
# 2023-01-02 18:00:00 - Gym

calendar.delete_event("Gym", dt.date(2023, 1, 1))
calendar.show()
# My Calendar
# 2023-01-01 00:00:00 - Dinner (budget: 20)
# 2023-01-02 18:00:00 - Gym

data_calendar = calendar.to_dataframe()
data_calendar
#                              path    name        date      time  budget
# 0  /My Calendar/2023/01/01/Dinner  Dinner  2023-01-01  00:00:00    20.0
# 1     /My Calendar/2023/01/02/Gym     Gym  2023-01-02  18:00:00     NaN
```

# Big Tree Python Package

Tree Implementation and Methods for Python, integrated with Python list, dictionary, and pandas DataFrame.

It is pythonic, making it easy to learn and extendable to many types of workflows.

----

Related Links:
- [Documentation](https://bigtree.readthedocs.io/en/latest/)
- [GitHub](https://github.com/kayjan/bigtree/)
- Community
  - [Issues](https://github.com/kayjan/bigtree/issues)
  / [Discussions](https://github.com/kayjan/bigtree/discussions)
  / [Changelog](https://github.com/kayjan/bigtree/blob/master/CHANGELOG.md)
  / [Contributing](https://bigtree.readthedocs.io/en/latest/others/contributing.html)
- Package
  - [PyPI](https://pypi.org/project/bigtree/)
  / [Conda](https://anaconda.org/conda-forge/bigtree)
- Articles
  - [Python Tree Implementation with BigTree](https://towardsdatascience.com/python-tree-implementation-with-bigtree-13cdabd77adc#245a-94ae81f0b3f1)
  - [The Reingold Tilford Algorithm Explained, with Walkthrough](https://towardsdatascience.com/reingold-tilford-algorithm-explained-with-walkthrough-be5810e8ed93?sk=2db8e10398cee76c486c4b06b0b33322)
- <div><p>If you want to support bigtree, <a href="https://www.buymeacoffee.com/kayjan"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" style="vertical-align:middle"></a></p></div>

----

## Components
There are 3 segments to Big Tree consisting of Tree, Binary Tree, and Directed Acyclic Graph (DAG) implementation.

For **Tree** implementation, there are 9 main components.

1. [**🌺 Node**](https://bigtree.readthedocs.io/en/latest/node.html)
   1. ``BaseNode``, extendable class
   2. ``Node``, BaseNode with node name attribute
2. [**✨ Constructing Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/construct.html)
   1. From `Node`, using parent and children constructors
   2. From *str*, using tree display or Newick string notation
   3. From *list*, using paths or parent-child tuples
   4. From *nested dictionary*, using path-attribute key-value pairs or recursive structure
   5. From *pandas DataFrame*, using paths or parent-child columns
   6. Add nodes to existing tree using path string
   7. Add nodes and attributes to existing tree using *dictionary* or *pandas DataFrame*, using path
   8. Add only attributes to existing tree using *dictionary* or *pandas DataFrame*, using node name
3. [**➰ Traversing Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/iterators.html)
   1. Pre-Order Traversal
   2. Post-Order Traversal
   3. Level-Order Traversal
   4. Level-Order-Group Traversal
   5. ZigZag Traversal
   6. ZigZag-Group Traversal
4. [**📝 Modifying Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/modify.html)
   1. Copy nodes from location to destination
   2. Shift nodes from location to destination
   3. Shift and replace nodes from location to destination
   4. Copy nodes from one tree to another
   5. Copy and replace nodes from one tree to another
5. [**🔍 Tree Search**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/search.html)
   1. Find multiple nodes based on name, partial path, relative path, attribute value, user-defined condition
   2. Find single nodes based on name, partial path, relative path, full path, attribute value, user-defined condition
   3. Find multiple child nodes based on user-defined condition
   4. Find single child node based on name, user-defined condition
6. [**🔧 Helper Function**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/helper.html)
   1. Cloning tree to another `Node` type
   2. Get subtree (smaller tree with different root)
   3. Prune tree (smaller tree with same root)
   4. Get difference between two trees
7. [**📊 Plotting Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/plot.html)
   1. Enhanced Reingold Tilford Algorithm to retrieve (x, y) coordinates for a tree structure
8. [**🔨 Exporting Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/export.html)
   1. Print to console, in vertical or horizontal orientation
   2. Export to *Newick string notation*, *dictionary*, *nested dictionary*, or *pandas DataFrame*
   3. Export tree to *dot* (can save to .dot, .png, .svg, .jpeg files)
   4. Export tree to *Pillow* (can save to .png, .jpg)
   5. Export tree to *Mermaid Flowchart* (can display on .md)
9. [**✔️ Workflows**](https://bigtree.readthedocs.io/en/latest/workflows.html)
   1. Sample workflows for tree demonstration!

--------

For **Binary Tree** implementation, there are 3 main components.
Binary Node inherits from Node, so the components in Tree implementation are also available in Binary Tree.

1. [**🌿 Node**](https://bigtree.readthedocs.io/en/latest/node.html)
   1. ``BinaryNode``, Node with binary tree rules
2. [**✨ Constructing Binary Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/binarytree/construct.html)
   1. From *list*, using flattened list structure
3. [**➰ Traversing Binary Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/iterators.html)
   1. In-Order Traversal

--------

For **Directed Acyclic Graph (DAG)** implementation, there are 4 main components.

1. [**🌼 Node**](https://bigtree.readthedocs.io/en/latest/node.html)
   1. ``DAGNode``, extendable class for constructing Directed Acyclic Graph (DAG)
2. [**✨ Constructing DAG**](https://bigtree.readthedocs.io/en/latest/bigtree/dag/construct.html)
   1. From *list*, containing parent-child tuples
   2. From *nested dictionary*
   3. From *pandas DataFrame*
3. [**➰ Traversing DAG**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/iterators.html)
   1. Generic traversal method
4. [**🔨 Exporting DAG**](https://bigtree.readthedocs.io/en/latest/bigtree/dag/export.html)
   1. Export to *list*, *dictionary*, or *pandas DataFrame*
   2. Export DAG to *dot* (can save to .dot, .png, .svg, .jpeg files)

----

## Installation

There are two ways to install `bigtree`, with pip (from PyPI) or conda (from conda-forge).

### a) Installation with pip (recommended)

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

### b) Installation with conda

To install `bigtree` with conda, run the following line in command prompt:

```shell
$ conda install -c conda-forge bigtree
```

----

## Tree Demonstration

Here are some codes to get started.

### Construct Tree

Nodes can have attributes if they are initialized from `Node`, *dictionary*, or *pandas DataFrame*.

#### 1. **From `Node`**

Nodes can be linked to each other in the following ways:
  - Using `parent` and `children` setter methods
  - Directly passing `parent` or `children` argument
  - Using bitshift operator with the convention `parent >> child` or `child << parent`
  - Using `.append(child)` or `.extend([child1, child2])` methods

{emphasize-lines="8-9"}
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

root.hshow()
#      ┌─ b ─── d
# ─ a ─┤
#      └─ c

graph = tree_to_dot(root, node_colour="gold")
graph.write_png("assets/docs/demo_tree.png")
```

![Sample Tree Output](https://github.com/kayjan/bigtree/raw/master/assets/docs/demo_tree.png)

{emphasize-lines="8-10"}
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

{emphasize-lines="5-6"}
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

#### 2. **From *str***

Construct nodes only. Newick string notation supports parsing attributes.

{emphasize-lines="13,25"}
```python
from bigtree import str_to_tree, newick_to_tree

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
root = str_to_tree(tree_str)
root.show()
# a
# ├── b
# │   ├── d
# │   └── e
# │       ├── g
# │       └── h
# └── c
#     └── f

newick_str = "((d,(g,h)e)b,(f)c)a"
root = newick_to_tree(newick_str)
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

#### 3. **From *list***

Construct nodes only, list can contain either full paths or tuples of parent-child names.

{emphasize-lines="3,10"}
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

#### 4. **From *nested dictionary***

Construct nodes using path where `key` is path and `value` is dict of node attribute names and attribute values.
Dictionary can also be a recursive structure where `key` is node attribute names and `value` is node attribute values,
and list of children (recursive).

{emphasize-lines="10,32"}
```python
from bigtree import dict_to_tree, nested_dict_to_tree

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

#### 5. **From *pandas DataFrame***

Construct nodes with attributes, *pandas DataFrame* can contain either path column or parent-child columns,
and attribute columns.

{emphasize-lines="15,32"}
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

> If tree is already created, nodes can still be added using path string, dictionary, and pandas DataFrame!
> Attributes can be added to existing nodes using a dictionary or pandas DataFrame.

### Print Tree

After tree is constructed, it can be viewed by printing to console using `show` or `hshow` method directly,
for vertical and horizontal orientation respectively.
Alternatively, the `print_tree` or `hprint_tree` method can be used.

{emphasize-lines="8,15,22,27,33,40,47,55,62,69,76,83,90,97-101"}
```python
from bigtree import Node, print_tree, hprint_tree

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

hprint_tree(root)
#            ┌─ d
#      ┌─ b ─┤
# ─ a ─┤     └─ e
#      └─ c

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
    custom_style=("│  ", "├→ ", "╰→ "),
)
# a
# ├→ b
# │  ├→ d
# │  ╰→ e
# ╰→ c
```

### Tree Attributes and Operations

Note that using `BaseNode` or `Node` as superclass inherits the default class attributes (properties)
and operations (methods).

```python
from bigtree import str_to_tree

# Initialize tree
tree_str = """
a
├── b
│   ├── d
│   ├── e
│   └── f
│       ├── h
│       └── i
└── c
    └── g
"""
root = str_to_tree(tree_str)

# Accessing children
node_b = root["b"]
node_e = root["b"]["e"]
```

Below are the tables of attributes available to `BaseNode` and `Node` classes.

| Attributes wrt self                  | Code               | Returns                    |
|--------------------------------------|--------------------|----------------------------|
| Check if root                        | `root.is_root`     | True                       |
| Check if leaf node                   | `root.is_leaf`     | False                      |
| Check depth of node                  | `node_b.depth`     | 2                          |
| Check depth of tree                  | `node_b.max_depth` | 4                          |
| Get root of tree                     | `node_b.root`      | Node(/a, )                 |
| Get node path                        | `node_b.node_path` | (Node(/a, ), Node(/a/b, )) |
| Get node name (only for `Node`)      | `node_b.node_name` | 'b'                        |
| Get node path name (only for `Node`) | `node_b.path_name` | '/a/b'                     |

| Attributes wrt structure          | Code                       | Returns                                                                              |
|-----------------------------------|----------------------------|--------------------------------------------------------------------------------------|
| Get child/children                | `root.children`            | (Node(/a/b, ), Node(/a/c, ))                                                         |
| Get parent                        | `node_e.parent`            | Node(/a/b, )                                                                         |
| Get siblings                      | `node_e.siblings`          | (Node(/a/b/d, ), Node(/a/b/f, ))                                                     |
| Get left sibling                  | `node_e.left_sibling`      | Node(/a/b/d, )                                                                       |
| Get right sibling                 | `node_e.left_sibling`      | Node(/a/b/f, )                                                                       |
| Get ancestors (lazy evaluation)   | `list(node_e.ancestors)`   | [Node(/a/b, ), Node(/a, )]                                                           |
| Get descendants (lazy evaluation) | `list(node_b.descendants)` | [Node(/a/b/d, ), Node(/a/b/e, ), Node(/a/b/f, ), Node(/a/b/f/h, ), Node(/a/b/f/i, )] |
| Get leaves (lazy evaluation)      | `list(node_b.leaves)`      | [Node(/a/b/d, ), Node(/a/b/e, ), Node(/a/b/f/h, ), Node(/a/b/f/i, )]                 |

Below is the table of operations available to `BaseNode` and `Node` classes.

| Operations                                      | Code                                                       | Returns                                    |
|-------------------------------------------------|------------------------------------------------------------|--------------------------------------------|
| Visualize tree (only for `Node`)                | `root.show()`                                              | None                                       |
| Visualize tree (horizontally) (only for `Node`) | `root.hshow()`                                             | None                                       |
| Get node information                            | `root.describe(exclude_prefix="_")`                        | [('name', 'a')]                            |
| Find path from one node to another              | `root.go_to(node_e)`                                       | [Node(/a, ), Node(/a/b, ), Node(/a/b/e, )] |
| Add child to node                               | `root.append(Node("j"))`                                   | None                                       |
| Add multiple children to node                   | `root.extend([Node("k"), Node("l")])`                      | None                                       |
| Set attribute(s)                                | `root.set_attrs({"description": "root-tag"})`              | None                                       |
| Get attribute                                   | `root.get_attr("description")`                             | 'root-tag'                                 |
| Copy tree                                       | `root.copy()`                                              | None                                       |
| Sort children                                   | `root.sort(key=lambda node: node.node_name, reverse=True)` | None                                       |

### Traverse Tree

Tree can be traversed using the following traversal methods.

{emphasize-lines="23,26,29,32,35,38"}
```python
from bigtree import (
    Node,
    levelorder_iter,
    levelordergroup_iter,
    postorder_iter,
    preorder_iter,
    zigzag_iter,
    zigzaggroup_iter,
)

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

Nodes can be shifted (with or without replacement) or copied from one path to another, changes the tree in-place.

{emphasize-lines="10-14,22-26"}
```python
from bigtree import list_to_tree, shift_nodes, shift_and_replace_nodes

root = list_to_tree(["Downloads/Pictures", "Downloads/photo1.jpg", "Downloads/file1.doc"])
root.show()
# Downloads
# ├── Pictures
# ├── photo1.jpg
# └── file1.doc

shift_nodes(
   tree=root,
   from_paths=["photo1.jpg", "Downloads/file1.doc"],
   to_paths=["Downloads/Pictures/photo1.jpg", "Downloads/Files/file1.doc"],
)
root.show()
# Downloads
# ├── Pictures
# │   └── photo1.jpg
# └── Files
#     └── file1.doc

shift_and_replace_nodes(
   tree=root,
   from_paths=["Downloads/Files"],
   to_paths=["Downloads/Pictures/photo1.jpg"],
)
root.show()
# Downloads
# └── Pictures
#     └── Files
#         └── file1.doc
```

{emphasize-lines="10-14"}
```python
from bigtree import list_to_tree, copy_nodes

root = list_to_tree(["Downloads/Pictures", "Downloads/photo1.jpg", "Downloads/file1.doc"])
root.show()
# Downloads
# ├── Pictures
# ├── photo1.jpg
# └── file1.doc

copy_nodes(
   tree=root,
   from_paths=["photo1.jpg", "Downloads/file1.doc"],
   to_paths=["Downloads/Pictures/photo1.jpg", "Downloads/Files/file1.doc"],
)
root.show()
# Downloads
# ├── Pictures
# │   └── photo1.jpg
# ├── photo1.jpg
# ├── file1.doc
# └── Files
#     └── file1.doc
```

Nodes can also be copied (with or without replacement) between two different trees.

{emphasize-lines="10-15,33-38"}
```python
from bigtree import Node, copy_nodes_from_tree_to_tree, copy_and_replace_nodes_from_tree_to_tree, list_to_tree
root = list_to_tree(["Downloads/Pictures", "Downloads/photo1.jpg", "Downloads/file1.doc"])
root.show()
# Downloads
# ├── Pictures
# ├── photo1.jpg
# └── file1.doc

root_other = Node("Documents")
copy_nodes_from_tree_to_tree(
   from_tree=root,
   to_tree=root_other,
   from_paths=["Downloads/Pictures", "photo1.jpg", "file1.doc"],
   to_paths=["Documents/Pictures", "Documents/Pictures/photo1.jpg", "Documents/Files/file1.doc"],
)
root_other.show()
# Documents
# ├── Pictures
# │   └── photo1.jpg
# └── Files
#     └── file1.doc

root_other = Node("Documents")
picture_folder = Node("Pictures", parent=root_other)
photo2 = Node("photo2.jpg", parent=picture_folder)
file2 = Node("file2.doc", parent=root_other)
root_other.show()
# Documents
# ├── Pictures
# │   └── photo2.jpg
# └── file2.doc

copy_and_replace_nodes_from_tree_to_tree(
   from_tree=root,
   to_tree=root_other,
   from_paths=["Downloads/photo1.jpg", "Downloads/file1.doc"],
   to_paths=["Documents/Pictures/photo2.jpg", "Documents/file2.doc"],
)
root_other.show()
# Documents
# ├── Pictures
# │   └── photo1.jpg
# └── file1.doc
```

### Tree Search

One or multiple nodes can be searched based on name, path, attribute value, or user-defined condition.

To find a single node:

{emphasize-lines="12,15,18,21,24,27"}
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

find_relative_path(c, "../b")  # relative path
# (Node(/a/b, age=65),)

find_path(root, "/c/d")  # partial path
# Node(/a/c/d, age=40)

find_full_path(root, "a/c/d")  # full path
# Node(/a/c/d, age=40)

find_attr(root, "age", 40)
# Node(/a/c/d, age=40)
```

To find multiple nodes:

{emphasize-lines="12,15,18,21,24"}
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

{emphasize-lines="12,15,18,21"}
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

There following are helper functions for
1. Cloning tree to another `Node` type
2. Getting subtree (smaller tree with different root)
3. Pruning tree (smaller tree with same root)
4. Getting difference between two trees

{emphasize-lines="6,20,27,35,49,58"}
```python
from bigtree import BaseNode, Node, clone_tree, get_subtree, get_tree_diff, prune_tree, str_to_tree

# 1. Cloning tree from `BaseNode` to `Node` type
root = BaseNode(name="a")
b = BaseNode(name="b", parent=root)
clone_tree(root, Node)
# Node(/a, )

# Create a tree for future sections
root = str_to_tree("""
a
├── b
│   ├── d
│   └── e
└── c
    └── f
""")

# 2. Getting subtree with root b
root_subtree = get_subtree(root, "b")
root_subtree.show()
# b
# ├── d
# └── e

# 3.1 Prune tree to only path a/b
root_pruned = prune_tree(root, "a/b")
root_pruned.show()
# a
# └── b
#     ├── d
#     └── e

# 3.1 Prune tree to exactly path a/b
root_pruned = prune_tree(root, "a/b", exact=True)
root_pruned.show()
# a
# └── b

# 4. Get difference between two trees
root_other = str_to_tree("""
a
├── b
│   └── d
└── c
    └── g
""")

tree_diff = get_tree_diff(root, root_other)
tree_diff.show()
# a
# ├── b
# │   └── e (-)
# └── c
#     ├── f (-)
#     └── g (+)

tree_diff = get_tree_diff(root, root_other, only_diff=False)
tree_diff.show()
# a
# ├── b
# │   ├── d
# │   └── e (-)
# └── c
#     ├── f (-)
#     └── g (+)
```

### Export Tree

Tree can be exported to another data type.

1. *Export to **Newick string notation***
2. *Export to **nested dictionary***
3. *Export to **nested recursive dictionary***
4. *Export to **pandas DataFrame***
5. *Export to **dot** (and png)*
6. *Export to **Pillow** (and png)*
7. *Export to **Mermaid Flowchart** (and md)*

{emphasize-lines="24, 27-32,41,67-73,81,84,87"}
```python
from bigtree import (
    Node,
    tree_to_dataframe,
    tree_to_dict,
    tree_to_dot,
    tree_to_mermaid,
    tree_to_newick,
    tree_to_nested_dict,
    tree_to_pillow,
)

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

tree_to_newick(root)
# '((d,e)b,c)a'

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
graph.write_png("assets/docs/demo_dot.png")

pillow_image = tree_to_pillow(root)
pillow_image.save("assets/docs/demo_pillow.png")

mermaid_md = tree_to_mermaid(root)
print(mermaid_md)
```

- demo_dot.png

![Sample Dot Image Output](https://github.com/kayjan/bigtree/raw/master/assets/docs/demo_dot.png)

- demo_pillow.png

![Sample Pillow Image Output](https://github.com/kayjan/bigtree/raw/master/assets/docs/demo_pillow.png)

- Mermaid flowchart
```mermaid
%%{ init: { 'flowchart': { 'curve': 'basis' } } }%%
flowchart TB
0("a") --> 0-0("b")
0-0 --> 0-0-0("d")
0-0 --> 0-0-1("e")
0("a") --> 0-1("c")
classDef default stroke-width:1
```

----

## Binary Tree Demonstration

Compared to nodes in tree, nodes in Binary Tree are only allowed maximum of 2 children.
Since BinaryNode extends from Node, construct, traverse, search, export methods from Node are applicable to
Binary Tree as well.

### Construct Binary Tree

1. **From `BinaryNode`**

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
graph.write_png("assets/docs/demo_binarytree.png")
```

![Sample DAG Output](https://github.com/kayjan/bigtree/raw/master/assets/docs/demo_binarytree.png)

2. **From *list***

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

### Traverse Binary Tree

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

{emphasize-lines="5-8,10"}
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
graph.write_png("assets/docs/demo_dag.png")
```

![Sample DAG Output](https://github.com/kayjan/bigtree/raw/master/assets/docs/demo_dag.png)

2. **From *list***

Construct nodes only, list contains parent-child tuples.

{emphasize-lines="10"}
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

{emphasize-lines="10"}
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

{emphasize-lines="15"}
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

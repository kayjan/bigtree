---
title: DAG Demonstration
---

# 📋 DAG Demonstration

Conceptually, DAGs are made up of nodes, and they are synonymous; a dag is a node. In bigtree implementation, node
refers to the `DAGNode` class, whereas dag refers to the `DAG` class. DAG is implemented as a wrapper around a DAGNode
to implement dag-level methods (for construct/export etc.) for a more intuitive API.

Compared to nodes in tree, nodes in DAG are able to have multiple parents.

## Construct DAG

### 1. From DAGNode

DAGNodes can be linked to each other in the following ways:

- Using `parents` and `children` setter methods
- Directly passing `parents` or `children` argument
- Using bitshift operator with the convention `parent_node >> child_node` or `child_node << parent_node`
- Using `.append(child)` or `.extend([child1, child2])` methods

```python hl_lines="5-8 10"
from bigtree import DAGNode, DAG

a = DAGNode("a")
b = DAGNode("b")
c = DAGNode("c", parents=[a, b])
d = DAGNode("d", parents=[a, c])
e = DAGNode("e", parents=[d])
f = DAGNode("f", parents=[c, d])
h = DAGNode("h")
g = DAGNode("g", parents=[c], children=[h])

graph = DAG(a).to_dot(node_colour="gold")
graph.write_png("assets/demo/dag.png")
```

![Sample DAG Output](https://github.com/kayjan/bigtree/raw/master/assets/demo/dag.png "Sample DAG Output")

### 2. From list

Construct nodes only, list contains parent-child tuples.

```python hl_lines="4"
from bigtree import DAG

relations_list = [("a", "c"), ("a", "d"), ("b", "c"), ("c", "d"), ("d", "e")]
dag = DAG.from_list(relations_list)

print([(parent.node_name, child.node_name) for parent, child in dag.iterate()])
# [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]
```

### 3. From nested dictionary

Construct nodes with attributes, `key`: child name, `value`: dict of parent name, child node attributes.

```python hl_lines="10"
from bigtree import DAG

relation_dict = {
    "a": {"step": 1},
    "b": {"step": 1},
    "c": {"parents": ["a", "b"], "step": 2},
    "d": {"parents": ["a", "c"], "step": 2},
    "e": {"parents": ["d"], "step": 3},
}
dag = DAG.from_dict(relation_dict, parent_key="parents")

print([(parent.node_name, child.node_name) for parent, child in dag.iterate()])
# [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]
```

### 4. From pandas DataFrame

Construct nodes with attributes, *pandas DataFrame* contains child column, parent column, and attribute columns.

```python hl_lines="16"
import pandas as pd
from bigtree import DAG

path_data = pd.DataFrame(
    [
        ["a", None, 1],
        ["b", None, 1],
        ["c", "a", 2],
        ["c", "b", 2],
        ["d", "a", 2],
        ["d", "c", 2],
        ["e", "d", 3],
    ],
    columns=["child", "parent", "step"],
)
dag = DAG.from_dataframe(path_data)

print([(parent.node_name, child.node_name) for parent, child in dag.iterate()])
# [('a', 'd'), ('c', 'd'), ('d', 'e'), ('a', 'c'), ('b', 'c')]
```

## DAG Attributes and Operations

Note that using `DAGNode` as superclass inherits the default class attributes (properties) and operations (methods).

```python
from bigtree import DAG

relations_list = [("a", "c"), ("a", "d"), ("b", "c"), ("c", "d"), ("d", "e")]
dag = DAG.from_list(relations_list).dag
dag
# DAGNode(d, )

# Accessing children
node_e = dag["e"]
node_a = dag.parents[0]
```

Below are the tables of attributes available to `DAGNode` class.

| Attributes wrt self             | Code             | Returns |
|---------------------------------|------------------|---------|
| Check if root                   | `node_a.is_root` | True    |
| Check if leaf node              | `dag.is_leaf`    | False   |
| Get node name (only for `Node`) | `dag.node_name`  | 'd'     |

| Attributes wrt structure | Code               | Returns                                    |
|--------------------------|--------------------|--------------------------------------------|
| Get child/children       | `node_a.children`  | (DAGNode(c, ), DAGNode(d, ))               |
| Get parents              | `dag.parents`      | (DAGNode(a, ), DAGNode(c, ))               |
| Get siblings             | `dag.siblings`     | (DAGNode(c, ),)                            |
| Get ancestors            | `dag.ancestors`    | [DAGNode(a, ), DAGNode(b, ), DAGNode(c, )] |
| Get descendants          | `dag.descendants`  | [DAGNode(e, )]                             |

Below is the table of operations available to `DAGNode` class.

| Operations                            | Code                                          | Returns                                                                    |
|---------------------------------------|-----------------------------------------------|----------------------------------------------------------------------------|
| Get node information                  | `dag.describe(exclude_prefix="_")`            | [('name', 'd')]                                                            |
| Find path(s) from one node to another | `node_a.go_to(dag)`                           | [[DAGNode(a, ), DAGNode(c, ), DAGNode(d, )], [DAGNode(a, ), DAGNode(d, )]] |
| Add child to node                     | `node_a.append(DAGNode("j"))`                 | DAGNode(a, )                                                               |
| Add multiple children to node         | `node_a.extend([DAGNode("k"), DAGNode("l")])` | DAGNode(a, )                                                               |
| Set attribute(s)                      | `dag.set_attrs({"description": "dag-tag"})`   | None                                                                       |
| Get attribute                         | `dag.get_attr("description")`                 | 'dag-tag'                                                                  |
| Copy DAG                              | `dag.copy()`                                  | None                                                                       |

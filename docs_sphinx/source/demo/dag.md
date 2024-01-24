# 📋 DAG Demonstration

Compared to nodes in tree, nodes in DAG are able to have multiple parents.

## Construct DAG

### 1. From DAGNode

DAGNodes can be linked to each other in the following ways:
  - Using `parents` and `children` setter methods
  - Directly passing `parents` or `children` argument
  - Using bitshift operator with the convention `parent_node >> child_node` or `child_node << parent_node`

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
graph.write_png("assets/demo/dag.png")
```

![Sample DAG Output](https://github.com/kayjan/bigtree/raw/master/assets/demo/dag.png)

### 2. From list

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

### 3. From nested dictionary

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

### 4. From pandas DataFrame

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

## DAG Attributes and Operations

Note that using `DAGNode` as superclass inherits the default class attributes (properties) and operations (methods).

```python
from bigtree import list_to_dag

relations_list = [
   ("a", "c"),
   ("a", "d"),
   ("b", "c"),
   ("c", "d"),
   ("d", "e")
]
dag = list_to_dag(relations_list)
dag
# DAGNode(d, )

# Accessing children
node_e = dag["e"]
node_a = dag.parents[0]
```

Below are the tables of attributes available to `DAGNode` class.

| Attributes wrt self                  | Code             | Returns |
|--------------------------------------|------------------|---------|
| Check if root                        | `node_a.is_root` | True    |
| Check if leaf node                   | `dag.is_leaf`    | False   |
| Get node name (only for `Node`)      | `dag.node_name`  | 'd'     |

| Attributes wrt structure     | Code                  | Returns                                                              |
|------------------------------|-----------------------|----------------------------------------------------------------------|
| Get child/children           | `node_a.children`     | (DAGNode(c, ), DAGNode(d, ))                                         |
| Get parents                  | `dag.parents`         | (DAGNode(a, ), DAGNode(c, ))                                         |
| Get siblings                 | `dag.siblings`        | (DAGNode(c, ),)                                                      |
| Get ancestors                | `dag.ancestors`       | [DAGNode(a, ), DAGNode(b, ), DAGNode(c, )]                           |
| Get descendants              | `dag.descendants`     | [DAGNode(e, )]                                                       |

Below is the table of operations available to `DAGNode` class.

| Operations                            | Code                                                       | Returns                                                                                                          |
|---------------------------------------|------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| Get node information                  | `dag.describe(exclude_prefix="_")`                         | [('name', 'd')]                                                                                                  |
| Find path(s) from one node to another | `node_a.go_to(dag)`                                        | [[DAGNode(a, ), DAGNode(c, ), DAGNode(d, description=dag-tag)], [DAGNode(a, ), DAGNode(d, description=dag-tag)]] |
| Set attribute(s)                      | `dag.set_attrs({"description": "dag-tag"})`                | None                                                                                                             |
| Get attribute                         | `dag.get_attr("description")`                              | 'dag-tag'                                                                                                        |
| Copy DAG                              | `dag.copy()`                                               | None                                                                                                             |

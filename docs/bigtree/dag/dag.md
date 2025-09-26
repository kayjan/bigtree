---
title: DAG
---

# 🎄 DAG

Conceptually, DAGs are made up of nodes, and they are synonymous; a dag is a node. In bigtree implementation, node
refers to the `DAGNode` class, whereas dag refers to the `DAG` class. DAG is implemented as a wrapper around a DAGNode
to implement dag-level methods (for construct/export etc.) for a more intuitive API.

Construct, export, and iterator methods encapsulated in DAG class.

## DAG Construct Methods

| Construct DAG from | Using parent-child relation | Add node attributes |
|--------------------|-----------------------------|---------------------|
| List               | `DAG.from_list`             | No                  |
| Dictionary         | `DAG.from_dict`             | Yes                 |
| DataFrame          | `DAG.from_dataframe`        | Yes                 |

## DAG Export Methods

| Export DAG to                           | Method         | Extract node attributes             |
|-----------------------------------------|----------------|-------------------------------------|
| List                                    | `to_list`      | No                                  |
| Dictionary                              | `to_dict`      | Yes with `attr_dict` or `all_attrs` |
| DataFrame                               | `to_dataframe` | Yes with `attr_dict` or `all_attrs` |
| Dot (for .dot, .png, .svg, .jpeg, etc.) | `to_dot`       | No                                  |

## Iterator Methods

| Data Structure | Algorithm                   | Description             |
|----------------|-----------------------------|-------------------------|
| DAG            | `iterate`                   | Depth-First Search      |

-----
::: bigtree.dag.dag

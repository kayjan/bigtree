---
title: Tree
---

# 🎄 Tree

Conceptually, trees are made up of nodes, and they are synonymous; a tree is a node. In bigtree implementation, node
refers to the `Node` class, whereas tree refers to the `Tree` class. Tree is implemented as a wrapper around a Node to
implement tree-level methods for a more intuitive API.

Construct, export, helper, query, search, and iterator methods encapsulated in Tree class.

## Tree Construct Methods

Construct Tree from list, dictionary, and pandas DataFrame.

To decide which method to use, consider your data type and data values.

| Construct tree from | Using full path       | Using parent-child relation                          | Using notation     | Add node attributes                                      |
|---------------------|-----------------------|------------------------------------------------------|--------------------|----------------------------------------------------------|
| String              | `Tree.from_str`       | NA                                                   | `Tree.from_newick` | No (for `Tree.from_str`)<br>Yes (for `Tree.from_newick`) |
| List                | `Tree.from_list`      | `Tree.from_list_relation`                            | NA                 | No                                                       |
| Dictionary          | `Tree.from_dict`      | `Tree.from_nested_dict`, `Tree.from_nested_dict_key` | NA                 | Yes                                                      |
| pandas DataFrame    | `Tree.from_dataframe` | `Tree.from_dataframe_relation`                       | NA                 | Yes                                                      |
| polars DataFrame    | `Tree.from_polars`    | `Tree.from_polars_relation`                          | NA                 | Yes                                                      |

To add attributes to an existing tree,

| Add attributes from | Using full path              | Using node name              |
|---------------------|------------------------------|------------------------------|
| Dictionary          | `Tree.add_dict_by_path`      | `Tree.add_dict_by_name`      |
| pandas DataFrame    | `Tree.add_dataframe_by_path` | `Tree.add_dataframe_by_name` |
| polars DataFrame    | `Tree.add_polars_by_path`    | `Tree.add_polars_by_name`    |

!!! note

    If attributes are added to existing tree using **full path**, paths that previously did not exist will be added.<br>
    If attributes are added to existing tree using **node name**, names that previously did not exist will not be created.

## Tree Export Methods

Export Tree to list, dictionary, pandas/polars DataFrame, and various formats.

| Export Tree to                          | Method                                            |
|-----------------------------------------|---------------------------------------------------|
| Command Line / Print                    | `show`, `hshow`, `vshow`                          |
| String                                  | `to_newick`                                       |
| Dictionary                              | `to_dict`, `to_nested_dict`, `to_nested_dict_key` |
| DataFrame (pandas, polars)              | `to_dataframe`, `to_polars`                       |
| Dot (for .dot, .png, .svg, .jpeg, etc.) | `to_dot`                                          |
| Pillow (for .png, .jpg, .jpeg, etc.)    | `to_pillow`, `to_pillow_graph`                    |
| Mermaid Markdown (for .md)              | `to_mermaid`                                      |
| Visualization                           | `to_vis`                                          |

## Tree Helper Methods

Helper functions that can come in handy.

| Description   | Method                   |
|---------------|--------------------------|
| Clone tree    | `clone`                  |
| Prune tree    | `prune`                  |
| Compare trees | `diff_dataframe`, `diff` |

## Tree Query and Search Methods

Query and search to find nodes.

| Search by       | One node                                            | One or more nodes                   |
|-----------------|-----------------------------------------------------|-------------------------------------|
| Query string    | `query`                                             |                                     |
| General method  | `find`, `find_child`                                | `findall`, `find_children`          |
| Node name       | `find_name`, `find_child_by_name`                   | `find_names`                        |
| Node path       | `find_path`, `find_full_path`, `find_relative_path` | `find_paths`, `find_relative_paths` |
| Node attributes | `find_attr`                                         | `find_attrs`                        |

## Iterator Methods

| Data Structure | Algorithm                                 | Description             |
|----------------|-------------------------------------------|-------------------------|
| Tree           | `preorder_iter`                           | Depth-First Search, NLR |
| Tree           | `postorder_iter`                          | Depth-First Search, LRN |
| Tree           | `levelorder_iter`, `levelordergroup_iter` | Breadth-First Search    |
| Tree           | `zigzag_iter`, `zigzaggroup_iter`         | Breadth-First Search    |

-----
::: bigtree.tree.tree

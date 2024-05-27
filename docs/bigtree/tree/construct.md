---
title: Tree Construct
---

# ✨ Construct

## Tree Construct Methods

Construct Tree from list, dictionary, and pandas DataFrame.

To decide which method to use, consider your data type and data values.

| Construct tree from | Using full path     | Using parent-child relation     | Using notation      | Add node attributes                                       |
|---------------------|---------------------|---------------------------------|---------------------|-----------------------------------------------------------|
| String              | ` str_to_tree`      | NA                              | ` newick_to_tree`   | No (for ` str_to_tree `)<br>Yes (for  `newick_to_tree`)   |
| List                | ` list_to_tree`     | ` list_to_tree_by_relation`     | NA                  | No                                                        |
| Dictionary          | ` dict_to_tree`     | ` nested_dict_to_tree`          | NA                  | Yes                                                       |
| pandas DataFrame    | `dataframe_to_tree` | `dataframe_to_tree_by_relation` | NA                  | Yes                                                       |
| polars DataFrame    | `polars_to_tree`    | `polars_to_tree_by_relation`    | NA                  | Yes                                                       |

## Tree Add Attributes Methods

To add attributes to an existing tree,

| Add attributes from | Using full path                  | Using node name                   |
|---------------------|----------------------------------|-----------------------------------|
| String              | ` add_path_to_tree`              | NA                                |
| Dictionary          | ` add_dict_to_tree_by_path`      | ` add_dict_to_tree_by_name`       |
| pandas DataFrame    | ` add_dataframe_to_tree_by_path` | ` add_dataframe_to_tree_by_name ` |
| polars DataFrame    | ` add_polars_to_tree_by_path`    | ` add_polars_to_tree_by_name `    |

!!! note

    If attributes are added to existing tree using **full path**, paths that previously did not exist will be added.<br>
    If attributes are added to existing tree using **node name**, names that previously did not exist will not be created.

These functions are not standalone functions.
Under the hood, they have the following dependency,

![Tree Constructor Dependency Diagram](https://github.com/kayjan/bigtree/raw/master/assets/docs/tree_construct.png "Tree Constructor Dependency Diagram")

-----

::: bigtree.tree.construct

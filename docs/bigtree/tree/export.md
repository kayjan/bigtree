---
title: Tree Export
---

# 🔨 Export

## Tree Export Methods

Export Tree to list, dictionary, and pandas DataFrame.

| Export Tree to                          | Method                                     |
|-----------------------------------------|--------------------------------------------|
| Command Line / Print                    | `print_tree`, `hprint_tree`, `vprint_tree` |
| Generator (versatile)                   | `yield_tree`, `hyield_tree`, `vyield_tree` |
| String                                  | `tree_to_newick`                           |
| Dictionary                              | `tree_to_dict`, `tree_to_nested_dict`      |
| DataFrame (pandas, polars)              | `tree_to_dataframe`, `tree_to_polars`      |
| Dot (for .dot, .png, .svg, .jpeg, etc.) | `tree_to_dot`                              |
| Pillow (for .png, .jpg, .jpeg, etc.)    | `tree_to_pillow`, `tree_to_pillow_graph`   |
| Mermaid Markdown (for .md)              | `tree_to_mermaid`                          |


## Tree Export Customisations

While exporting to another data type, methods can take in arguments to determine what information to extract.

| Method                 | Extract node attributes             | Specify maximum depth | Skip depth | Extract leaves only                   | Others                                                |
|------------------------|-------------------------------------|-----------------------|------------|---------------------------------------|-------------------------------------------------------|
| `print_tree`           | Yes with `attr_list` or `all_attrs` | Yes                   | No         | No                                    | Tree style                                            |
| `yield_tree`           | No, returns node                    | Yes                   | No         | No                                    | Tree style                                            |
| `hprint_tree`          | No                                  | Yes                   | No         | Yes, by hiding intermediate node name | Tree style, border style                              |
| `hyield_tree`          | No                                  | Yes                   | No         | Yes, by hiding intermediate node name | Tree style, border style                              |
| `vprint_tree`          | No                                  | Yes                   | No         | Yes, by hiding intermediate node name | Tree style, border style                              |
| `vyield_tree`          | No                                  | Yes                   | No         | Yes, by hiding intermediate node name | Tree style, border style                              |
| `tree_to_newick`       | Yes with `attr_list`                | No                    | No         | Yes, by hiding intermediate node name | Length separator and attribute prefix and separator   |
| `tree_to_dict`         | Yes with `attr_dict` or `all_attrs` | Yes                   | Yes        | Yes with `leaf_only`                  | Dict key for parent                                   |
| `tree_to_nested_dict`  | Yes with `attr_dict` or `all_attrs` | Yes                   | No         | No                                    | Dict key for node name and node children              |
| `tree_to_dataframe`    | Yes with `attr_dict` or `all_attrs` | Yes                   | Yes        | Yes with `leaf_only`                  | Column name for path, node name, node parent          |
| `tree_to_polars`       | Yes with `attr_dict` or `all_attrs` | Yes                   | Yes        | Yes with `leaf_only`                  | Column name for path, node name, node parent          |
| `tree_to_dot`          | No                                  | No                    | No         | No                                    | Graph attributes, background, node, edge colour, etc. |
| `tree_to_pillow_graph` | Yes with `node_content`             | Yes                   | No         | No                                    | Font (family, size, colour), background colour, etc.  |
| `tree_to_pillow`       | No                                  | Yes                   | No         | No                                    | Font (family, size, colour), background colour, etc.  |
| `tree_to_mermaid`      | No                                  | Yes                   | No         | No                                    | Node shape, node fill, edge arrow, edge label etc.    |

-----

::: bigtree.tree.export

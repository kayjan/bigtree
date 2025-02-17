---
title: Tree Export
---

# 🔨 Export

## Tree Export Methods

Export Tree to list, dictionary, and pandas DataFrame.

| Export Tree to                          | Method                                                   |
|-----------------------------------------|----------------------------------------------------------|
| Command Line / Others                   | `print_tree`, `yield_tree`, `hprint_tree`, `hyield_tree` |
| String                                  | `tree_to_newick`                                         |
| Dictionary                              | `tree_to_dict`, `tree_to_nested_dict`                    |
| DataFrame (pandas, polars)              | `tree_to_dataframe`, `tree_to_polars`                    |
| Dot (for .dot, .png, .svg, .jpeg, etc.) | `tree_to_dot`                                            |
| Pillow (for .png, .jpg, .jpeg, etc.)    | `tree_to_pillow`, `tree_to_pillow_graph`                 |
| Mermaid Markdown (for .md)              | `tree_to_mermaid`                                        |


## Tree Export Customizations

While exporting to another data type, methods can take in arguments to determine what information to extract.

| Method                 | Extract node attributes             | Specify maximum depth                                | Skip depth                  | Extract leaves only  | Others                                                |
|------------------------|-------------------------------------|------------------------------------------------------|-----------------------------|----------------------|-------------------------------------------------------|
| `print_tree`           | Yes with `attr_list` or `all_attrs` | Yes with `max_depth`                                 | No, but can specify subtree | No                   | Tree style                                            |
| `yield_tree`           | No, returns node                    | Yes with `max_depth`                                 | No, but can specify subtree | No                   | Tree style                                            |
| `tree_to_newick`       | Yes with `attr_list`                | No                                                   | No                          | No                   | Length separator and attribute prefix and separator   |
| `tree_to_dict`         | Yes with `attr_dict` or `all_attrs` | Yes with `max_depth`                                 | Yes with `skip_depth`       | Yes with `leaf_only` | Dict key for parent                                   |
| `tree_to_nested_dict`  | Yes with `attr_dict` or `all_attrs` | Yes with `max_depth`                                 | No                          | No                   | Dict key for node name and node children              |
| `tree_to_dataframe`    | Yes with `attr_dict` or `all_attrs` | Yes with `max_depth`                                 | Yes with `skip_depth`       | Yes with `leaf_only` | Column name for path, node name, node parent          |
| `tree_to_polars`       | Yes with `attr_dict` or `all_attrs` | Yes with `max_depth`                                 | Yes with `skip_depth`       | Yes with `leaf_only` | Column name for path, node name, node parent          |
| `tree_to_dot`          | No                                  | No                                                   | No                          | No                   | Graph attributes, background, node, edge colour, etc. |
| `tree_to_pillow_graph` | Yes with `node_content`             | No                                                   | No                          | No                   | Font (family, size, colour), background colour, etc.  |
| `tree_to_pillow`       | No                                  | Yes, using keyword arguments similar to `yield_tree` | No                          | No                   | Font (family, size, colour), background colour, etc.  |
| `tree_to_mermaid`      | No                                  | Yes, using keyword arguments similar to `yield_tree` | No                          | No                   | Node shape, node fill, edge arrow, edge label etc.    |

-----

::: bigtree.tree.export

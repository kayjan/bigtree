---
title: DAG Export
---

# 🔨 Export

Export Directed Acyclic Graph (DAG) to list, dictionary, and pandas DataFrame.

## DAG Export Methods

| Export DAG to                           | Method             | Extract node attributes             |
|-----------------------------------------|--------------------|-------------------------------------|
| List                                    | `dag_to_list`      | No                                  |
| Dictionary                              | `dag_to_dict`      | Yes with `attr_dict` or `all_attrs` |
| DataFrame                               | `dag_to_dataframe` | Yes with `attr_dict` or `all_attrs` |
| Dot (for .dot, .png, .svg, .jpeg, etc.) | `dag_to_dot`       | No                                  |

-----

::: bigtree.dag.export

---
title: DAG Construct
---

# ✨ Construct

Construct Directed Acyclic Graph (DAG) from list, dictionary, and pandas DataFrame.

## DAG Construct Methods

| Construct DAG from | Using parent-child relation | Add node attributes |
|--------------------|-----------------------------|---------------------|
| List               | `list_to_dag`               | No                  |
| Dictionary         | `dict_to_dag`               | Yes                 |
| DataFrame          | `dataframe_to_dag`          | Yes                 |

These functions are not standalone functions. Under the hood, they have the following dependency,

![DAG Constructor Dependency Diagram](https://github.com/kayjan/bigtree/raw/master/assets/docs/dag_construct.png "DAG Constructor Dependency Diagram")

-----

::: bigtree.dag.construct

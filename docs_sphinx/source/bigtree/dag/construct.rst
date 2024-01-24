|:sparkles:| Construct
============================================

Construct Directed Acyclic Graph (DAG) from list, dictionary, and pandas DataFrame.

.. list-table:: DAG Construct Methods
   :widths: 30 40 30
   :header-rows: 1

   * - Construct DAG from
     - Using parent-child relation
     - Add node attributes
   * - List
     - `list_to_dag`
     - No
   * - Dictionary
     - `dict_to_dag`
     - Yes
   * - DataFrame
     - `dataframe_to_dag`
     - Yes

These functions are not standalone functions.
Under the hood, they have the following dependency,

.. image:: https://github.com/kayjan/bigtree/raw/master/assets/docs/dag_construct.png
   :target: https://github.com/kayjan/bigtree/raw/master/assets/docs/dag_construct.png
   :alt: DAG Constructor Dependency Diagram

.. automodule:: bigtree.dag.construct
   :members:
   :show-inheritance:

|:hammer:| Export
============================================

Export Directed Acyclic Graph (DAG) to list, dictionary, and pandas DataFrame.

.. list-table:: DAG Export Methods
   :widths: 40 25 30
   :header-rows: 1

   * - Export DAG to
     - Method
     - Extract node attributes
   * - List
     - `dag_to_list`
     - No
   * - Dictionary
     - `dag_to_dict`
     - Yes with `attr_dict` or `all_attrs`
   * - DataFrame
     - `dag_to_dataframe`
     - Yes with `attr_dict` or `all_attrs`
   * - Dot (for .dot, .png, .svg, .jpeg, etc.)
     - `dag_to_dot`
     - No

.. automodule:: bigtree.dag.export
   :members:
   :show-inheritance:

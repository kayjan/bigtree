Export
===================

Export Tree to list, dictionary, and pandas DataFrame.

.. list-table:: Tree Export Methods
   :widths: 40 30 30
   :header-rows: 1

   * - Export Tree to
     - Method
     - Extract node attributes
   * - Command Line / Others
     - `print_tree`, `yield_tree`
     - Yes
   * - Dictionary
     - `tree_to_dict`, `tree_to_nested_dict`
     - Yes with `attr_dict` or `all_attrs`
   * - DataFrame
     - `tree_to_dataframe`
     - Yes with `attr_dict` or `all_attrs`
   * - Dot (for .dot, .png, .svg, .jpeg, etc.)
     - `tree_to_dot`
     - No

.. automodule:: bigtree.tree.export
   :members:
   :show-inheritance:

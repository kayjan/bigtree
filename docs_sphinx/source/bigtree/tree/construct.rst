|:sparkles:| Construct
============================================

Construct Tree from list, dictionary, and pandas DataFrame.

To decide which method to use, consider your data type and data values.

.. list-table:: Tree Construct Methods
   :widths: 35 30 50 30 40
   :header-rows: 1

   * - Construct Tree from
     - Using full path
     - Using parent-child relation
     - Using notation
     - Add node attributes
   * - String
     - `str_to_tree`
     - NA
     - `newick_to_tree`
     - | No (for `str_to_tree`)
       | Yes (for `newick_to_tree`)
   * - List
     - `list_to_tree`
     - `list_to_tree_by_relation`
     - NA
     - No
   * - Dictionary
     - `dict_to_tree`
     - `nested_dict_to_tree`
     - NA
     - Yes
   * - DataFrame
     - `dataframe_to_tree`
     - `dataframe_to_tree_by_relation`
     - NA
     - Yes


To add attributes to existing tree,

.. list-table:: Tree Add Attributes Methods
   :widths: 30 40 30
   :header-rows: 1

   * - Add attributes from
     - Using full path
     - Using node name
   * - String
     - `add_path_to_tree`
     - NA
   * - Dictionary
     - `add_dict_to_tree_by_path`
     - `add_dict_to_tree_by_name`
   * - DataFrame
     - `add_dataframe_to_tree_by_path`
     - `add_dataframe_to_tree_by_name`

.. note::
 | If attributes are added to existing tree using **full path**, paths that previously did not exist will be added.
 | If attributes are added to existing tree using **node name**, names that previously did not exist will not be created.

These functions are not standalone functions.
Under the hood, they have the following dependency,

.. image:: https://github.com/kayjan/bigtree/raw/master/assets/docs/tree_construct.png
   :target: https://github.com/kayjan/bigtree/raw/master/assets/docs/tree_construct.png
   :alt: Tree Constructor Dependency Diagram

.. automodule:: bigtree.tree.construct
   :members:
   :show-inheritance:

|:memo:| Modify
============================================

There are two types of modification available,

  1. **Non-replacing scenario**: Shift or copy nodes within same tree or between two trees using `from_paths` (list of paths) and `to_paths` (list of paths).
  2. **Replacing scenario**: Shift or copy nodes within same tree or between two trees *while replacing the to-node* using `from_paths` (list of paths) and `to_paths` (list of paths).

In **non-replacing scenario**, there are several configurations available for customisation.

.. list-table:: Available Configurations for Customisation
   :widths: 20 40 40
   :header-rows: 1

   * - Configuration
     - Description
     - Default Value
   * - `copy`
     - Indicates whether it is to shift the nodes, or copy the nodes
     - False (nodes are shifted, not copied)
   * - `to_tree`
     - Indicates whether shifting/copying is within the same tree, or between different trees
     - None (nodes are shifted/copied within the same tree)
   * - `skippable`
     - Skip shifting/copying of nodes if from_path cannot be found
     - False (from-node must be found)
   * - `overriding`
     - Override existing node if it exists
     - False (to-node must not exist)
   * - `merge_children`
     - Shift/copy children of from-node and remove intermediate parent node
     - False (children are not merged)
   * - `merge_leaves`
     - Shift/copy leaves of from-node and remove all intermediate nodes
     - False (leaves are not merged)
   * - `delete_children`
     - Shift/copy node only and delete its children
     - False (nodes are shifted/copied together with children)

In **replacing scenario**, all the configurations are also available except `overriding`, `merge_children`, and `merge_leaves` as it is doing a one-to-one replacement.
It is by default overriding, and there is nothing to merge.

.. note:: `merge_children` and `merge_leaves` cannot be simultaneously set to `True`.

.. note:: Error will always be thrown if multiple from-nodes are found, paths in `from_paths` must be unique.

Tree Modification Permutations
----------------------------------

There are several ways you can mix and match the tree modification methods.
If you know all the parameters to choose, feel free to use ``copy_or_shift_logic`` or ``replace_logic`` methods as they are the most customizable.
All other methods calls these 2 methods directly.

.. list-table:: Tree Modification Methods
   :widths: 10 20 10 20
   :header-rows: 1

   * - Shift / Copy?
     - Same tree / Between two trees?
     - Replace destination node?
     - Method to use
   * - Shift
     - Same tree
     - No
     - ``shift_nodes``
   * - Copy
     - Same tree
     - No
     - ``copy_nodes``
   * - Copy
     - Between two trees
     - No
     - ``copy_nodes_from_tree_to_tree``
   * - Any
     - Any
     - No
     - ``copy_or_shift_logic``
   * - Shift
     - Same tree
     - Yes
     - ``shift_and_replace_nodes``
   * - Copy
     - Between two trees
     - Yes
     - ``copy_and_replace_nodes_from_tree_to_tree``
   * - Any
     - Any
     - Yes
     - ``replace_logic``

Tree Modification Illustration
----------------------------------

.. image:: https://github.com/kayjan/bigtree/raw/master/assets/docs/modify_shift_and_copy.png
   :target: https://github.com/kayjan/bigtree/raw/master/assets/docs/modify_shift_and_copy.png
   :width: 80%
   :align: center
   :alt: Shift and Copy Example

.. list-table:: Sample Tree Modification (Shift, Copy, Delete)
   :widths: 20 20 20 50
   :header-rows: 1

   * - Setting
     - Sample path in `from_paths`
     - Sample path in `to_paths`
     - Description
   * - Default
     - "/a/c"
     - "/a/b/c"
     - Shift/copy node `c`
   * - Default
     - "/c"
     - "/a/b/c"
     - Shift/copy node `c`
   * - Default
     - "c"
     - "/a/b/c"
     - Shift/copy node `c`
   * - Default
     - "/a/e"
     - None
     - Delete node `e`
   * - skippable
     - "/a/c"
     - "/a/b/c"
     - Shift/copy node `c`, skip if "/a/c" cannot be found

.. image:: https://github.com/kayjan/bigtree/raw/master/assets/docs/modify_advanced.png
   :target: https://github.com/kayjan/bigtree/raw/master/assets/docs/modify_advanced.png
   :alt: Advanced Shift Example

.. list-table:: Sample Tree Modification (Advanced)
   :widths: 20 20 20 50
   :header-rows: 1

   * - Setting
     - Sample path in `from_paths`
     - Sample path in `to_paths`
     - Description
   * - overriding
     - "a/b/c"
     - "a/d/c"
     - Shift/copy node `c`, override if "a/d/c" exists
   * - merge_children
     - "a/b/c"
     - "a/d/c"
     - | **If path not present**: Shift/copy children of node `c` to be children of node `d`, removing node `c`
       | **If path present**: Shift/copy children of node `c` to be merged with existing "a/d/c" children
   * - merge_children + overriding
     - "a/b/c"
     - "a/d/c"
     - | **If path not present**: Behaves like merge_children
       | **If path present**: Behaves like overriding
   * - merge_leaves
     - "a/b/c"
     - "a/d/c"
     - | **If path not present**: Shift/copy leaves of node `c` to be children of node `d`
       | **If path present**: Shift/copy leaves of node `c` to be merged with existing "a/d/c" children
   * - merge_leaves + overriding
     - "a/b/c"
     - "a/d/c"
     - | **If path not present**: Behaves like merge_leaves
       | **If path present**: Behaves like overriding, but original node `c` remains
   * - delete_children
     - "a/b"
     - "a/d/b"
     - Shift/copy node `b` only without any node `b` children

.. automodule:: bigtree.tree.modify
   :members:
   :show-inheritance:

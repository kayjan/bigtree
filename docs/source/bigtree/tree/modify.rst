|:memo:| Modify
===================

Shift or copy nodes within same tree or between two trees using
`from_paths` (list of paths) and `to_paths` (list of paths).

There are several configurations available for more customization

- `skippable`: Skip shifting/copying of nodes if from_path cannot be found, defaults to False (from node must be found)
- `overriding`: Override existing node if it exists, defaults to False (to node must not exist)
- `merge_children`: Merge children and remove intermediate parent node, defaults to False (children are not merged)
- `merge_leaves`: Merge leaves and remove all intermediate nodes, defaults to False (leaves are not merged)
- `delete_children`: Shift/copy node only and delete its children, defaults to False (nodes are shifted/copied together with children)

.. note:: `merge_children` and `merge_leaves` cannot be simultaneously set to `True`

.. note:: Error will always be thrown if multiple from-nodes are found, paths in `from_paths` must be unique.

Tree Modification Illustration
----------------------------------

.. image:: https://github.com/kayjan/bigtree/raw/master/assets/modify_shift_and_copy.png
   :target: https://github.com/kayjan/bigtree/raw/master/assets/modify_shift_and_copy.png
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

.. image:: https://github.com/kayjan/bigtree/raw/master/assets/modify_advanced.png
   :target: https://github.com/kayjan/bigtree/raw/master/assets/modify_advanced.png
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

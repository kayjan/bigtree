|:memo:| Modify
===================

Shift or copy nodes within same tree or between two trees using
`from_paths` (list of paths) and `to_paths` (list of paths).

There are several configurations available for more customization

- `skippable`: Skip shifting/copying of nodes if from_path cannot be found, defaults to False (from node must be found)
- `overriding`: Override existing node if it exists, defaults to False (to node must not exist)
- `merge_children`: Merge children and remove intermediate parent node, defaults to False (nodes are not merged)
- `delete_children`: Shift/copy node-only and delete its children

.. note:: Error will always be thrown if multiple from-nodes are found, paths in `from_paths` must be unique.

.. list-table:: Sample Tree Modification
   :widths: 20 20 20 50
   :header-rows: 1

   * - Setting
     - Sample path in `from_paths`
     - Sample path in `to_paths`
     - Description
   * - Default
     - "/a/b/c"
     - "/a/b/d/c"
     - Shift/copy node `c`
   * - Default
     - "/c"
     - "/a/b/d/c"
     - Shift/copy node `c`
   * - Default
     - "c"
     - "/a/b/d/c"
     - Shift/copy node `c`
   * - Default
     - "/a/b/c"
     - None
     - Delete node `c`
   * - skippable
     - "/a/b/c"
     - "/a/b/d/c"
     - Shift/copy node `c`, skip if "/a/b/c" cannot be found
   * - overriding
     - "/a/b/c"
     - "/a/b/d/c"
     - Shift/copy node `c`, override if "/a/b/d/c" exists
   * - merge_children
     - "/a/b/c"
     - "/a/b/d/c"
     - | **If path not present**: Shift/copy children of node `c` to be children of node `d`, removing node `c`.
       | **If path present**: Shift/copy children of node `c` to be merged with existing "/a/b/d/c" children
   * - merge_children + overriding
     - "/a/b/c"
     - "/a/b/d/c"
     - | **If path not present**: Behaves like merge_children
       | **If path present**: Behaves like overriding
   * - delete_children
     - "/a/b/c"
     - "/a/b/d/c"
     - Shift/copy node `c` only without any node `c` children

.. automodule:: bigtree.tree.modify
   :members:
   :show-inheritance:

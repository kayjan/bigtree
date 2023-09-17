# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.12.3] - 2023-09-17
### Changed
- Clearer documentation, fixed docstring phrasing and spelling.
- Clearer error messages, standardized error messages.

## [0.12.2] - 2023-09-12
### Changed
- Tree Plot: Reingold Tilford Algorithm code for succinctness and docstring.

## [0.12.1] - 2023-09-11
### Fixed
- Tree Plot: Reingold Tilford Algorithm to handle cases of negative x-coordinates with adjustment parameter.

## [0.12.0] - 2023-09-09
### Changed
- Tree/DAG Constructor, Tree/DAG Exporter: Make `pandas` optional dependency.
### Fixed
- Misc: Fixed Calendar workflow to throw error when `to_dataframe` method is called on empty calendar.
- Tree/DAGNode Exporter, Tree Helper, Tree Search: Relax type hinting using TypeVar.

## [0.11.0] - 2023-09-08
### Added
- Tree Helper: Pruning tree to allow pruning by `prune_path` and `max_depth`.
- Tree Plot: Implement Enhanced Reingold Tilford Algorithm to retrieve (x, y) coordinates for a tree structure.
### Changed
- BaseNode/DAGNode: `get_attr` method to allow default return value.
### Fixed
- Utility Iterator: Relax type hinting using TypeVar.

## [0.10.3] - 2023-08-12
### Added
- Tree Constructor: `add_path_to_tree`, `dataframe_to_tree`, `dataframe_to_tree_by_relation` to allow custom node types that takes in constructor arguments.
### Changed
- Binary Tree: Able to accept node val of `str` type besides `int` type.

## [0.10.2] - 2023-08-11
### Fixed
- Tree Constructor: `nested_dict_to_tree` to throw TypeError if child_key is not list type.

## [0.10.1] - 2023-07-27
### Added
- [#71] Node: `path_name` to allow different node name of different dtypes; map everything to string type.

## [0.10.0] - 2023-07-15
### Added
- [#65] Tree Search: Implement `find_relative_path` to find relative path from node.
- [#65] Utility Iterator: Implement `zigzag_iter` and `zigzaggroup_iter` Tree traversal methods.

## [0.9.5] - 2023-07-13
### Added
- Misc: Added init files, add link to discussions to README and pyproject, add sphinx coverage shortcuts.
### Fixed
- [#66] DAGNode/Node: Children constructor to allow Iterable types, fixed issue of lists being mutable.
- [#67] Node: `path_name` to reduce number of recursive calls to root node for `sep`.

## [0.9.4] - 2023-06-18
### Added
- Tree Constructor: `list_to_tree_by_relation` and `dataframe_to_tree_by_relation` method to allow duplicate intermediate nodes (default is false).
- DAG Exporter: Added `node_shape` parameter in `dag_to_dot` export function for easier way to customize node shape.
- Misc: More test cases.
- Misc: Added security instructions on how to raise vulnerabilities.
- Misc: Added Calendar workflow to documentation.
### Changed
- Tree Constructor: `add_dict_to_tree_by_name` method rename argument from `path_attrs` to `name_attrs`.
- Misc: Modified contributing instructions.
### Fixed
- Tree Exporter: `tree_to_dot` to handle cases when not all nodes have `edge_attr`.
- DAG Exporter: `dag_to_dot` to perform dictionary copy to prevent style from being overridden for child nodes.
- Tree Constructor: `dataframe_to_tree` to handle case when path column is not the first column.

## [0.9.3] - 2023-05-28
### Changed
- Tree Constructor: Relax type hint to `Iterable` instead of `List` for `list_to_tree` and `list_to_tree_by_relation` methods.
### Fixed
- Node: Fix error message when trees have different `sep`.

## [0.9.2] - 2023-04-09
### Added
- Node: Added `show` method to print tree to console.
- Workflow Calendar: Tree use case with calendar implementation.

## [0.9.1] - 2023-03-30
### Changed
- Node: Added `sep` parameter to constructor instead of using getter and setter methods to set `sep`.

## [0.9.0] - 2023-03-29
### Added
- Tree Modifier: Ability to copy/shift nodes with full path in `from_paths` for faster search performance, added `with_full_path` parameter.
### Changed
- Tree Modifier: Enforced paths in `to_paths` to be full path for faster search performance.
- Tree Modifier: Faster creation of intermediate parent nodes in `to_paths`.
- Tree Modifier: Better handling of `sep` in paths by performing string replacement at the start.
- Tree Modifier: Check and throw error for invalid parameters, case when node is meant to be deleted but `copy=True`.
### Fixed
- Tree Modifier: Fix issue trailing `sep` differing in `from_paths` and `to_paths` which should not throw error.

## [0.8.4] - 2023-03-24
### Added
- Tree Search: Implement `find_child` and `find_children` to find single child or multiple children based on user-defined condition.
### Changed
- Tree and DAG Constructor: Reduce reliance on `numpy` package, only reject `None` attributes when creating tree from DataFrame (previously it rejects `[None]`).
- Tree Helper: Get difference between two trees reduce reliance on `numpy` package, enhance test cases.
- Tree Search: Renamed `find_children` to `find_child_by_name` for clarity.
- Misc: Fix README for Windows installation.

## [0.8.3] - 2023-03-16
### Changed
- Workflow: Misc refactor and update log statements.
- Misc: Fix coverage report.

## [0.8.2] - 2023-03-16
### Changed
- Misc: Type checking to remove optional requirement for `mypy`.
- Misc: Shift .flake8, .mypy.ini, and pytest.ini files to pyproject.toml.

## [0.8.1] - 2023-03-10
### Fixed
- Tree Modifier: Fix issue of `sep` of tree differing from the `sep` in `from_paths` and `to_paths`.

## [0.8.0] - 2023-03-10
### Added
- Misc: Type checking with `mypy`, added type checks to pre-commit hooks.
### Changed
- DAGNode: `go_to` method to be consistent with `List[List[DAGNode]]` type.
### Fixed
- Tree Exporter: Exception handling in `yield_tree` if `node_name_or_path` is not found.
- Workflow: Exception handling in prioritizing item/list if item/list is not the correct tree depth.
- Workflow: Exception handling in removing item/list if item/list is not found.

## [0.7.4] - 2023-02-27
### Fixed
- Tree Constructor: Fixed pandas SettingwithCopyWarning when performing dataframe operations.

## [0.7.3] - 2023-02-25
### Added
- Tree Exporter: Fixed `print_tree` checking attributes with `hasattr` to handle cases of null or 0 value attributes, add more test cases.
- Misc: Added more description to Contributing.

## [0.7.2] - 2023-02-18
### Added
- Tree Exporter: Added `node_shape` parameter in `tree_to_dot` export function for easier way to customize node shape.

## [0.7.1] - 2023-02-18
### Added
- BaseNode/Node: Added `go_to` BaseNode method to travel from one node to another node from the same tree.
- DAGNode: Added `go_to` DAGNode method to travel from one node to another node from the same DAG.

## [0.7.0] - 2023-02-18
### Added
- Tree Modifier: Accept `merge_leaves` type of modification, enhance documentation to provide more examples and illustrations.

## [0.6.10] - 2023-01-23
### Fixed
- Tree Constructor: `str_to_tree` accept prefixes to support unicode characters in node names.

## [0.6.9] - 2023-01-22
### Added
- Tree Construct: `str_to_tree` to construct tree from tree string.

## [0.6.8] - 2023-01-14
### Fixed
- Tree Exporter: `tree_to_dot` to perform dictionary copy to prevent style from being overridden for child nodes.

## [0.6.7] - 2023-01-09
### Changed
- Binary Tree: Changed `BNode` to `BinaryNode`, and construct method `list_to_btree` to `list_to_binarytree`.

## [0.6.6] - 2022-12-15
### Added
- Tree Exporter: Export `print_tree` output to image using Pillow package.

## [0.6.5] - 2022-12-07
### Added
- Tree Modifier: Shift/copy nodes able to shift node-only and delete the children (backwards-compatible).

## [0.6.4] - 2022-11-16
### Fixed
- BNode: Minor fix on rollback functionality when original children includes None.

## [0.6.3] - 2022-11-15
### Added
- DAGNode: Rollback functionality to original state when there is error setting parent and children (backwards-compatible).
### Changed
- BaseNode, BNode, DAGNode: Refactor by abstracting checks.
### Fixed
- BaseNode: Fix rollback logic to handle failure in pre-assign checks and reassigning same child / parent.
- BNode: Fix issue of reassigning children shifting existing child from right to left.

## [0.6.2] - 2022-11-15
### Changed
- Tree Modifier: Shorter logging messages.

## [0.6.1] - 2022-11-14
### Changed
- Tree Modifier: Handle shifting/copying that removes intermediate layer (backwards-compatible).

## [0.6.0] - 2022-11-13
### Added
- BaseNode: Rollback functionality to original state when there is error setting parent and children (backwards-compatible).
- BaseNode and DAGNode: Type hints.
- BNode: Node class for Binary Tree.
- BTree Constructor: From list.
- BNode Iterator: Level-Order Iterator.
- Misc: Add Tips and Tricks to documentation (List Directory).
### Fixed
- DAGNode: Fix issue of duplicate parent constructor creating duplicate children.

## [0.5.5] - 2022-11-12
### Added
- Misc: More docstring examples.
- Misc: More test cases.
### Fixed
- Tree Modifier: Fix issue with `merge_children` argument not working as expected.

## [0.5.4] - 2022-11-12
### Added
- BaseNode: Add sort() to sort children.
- Node: Made more extendable with pre-/post-assign checks.
- Misc: Add Tips and Tricks to documentation (Extending Nodes).
- Misc: More test cases.
### Fixed
- Tree Search: Type hints.

## [0.5.3] - 2022-11-11
### Added
- DAG and Tree Exporter: More customizations allowed on edges.
- Add Tips and Tricks to documentation (Weighted Trees, Merging Trees).
### Fixed
- Tree Modifier: Fix issue with `merge_children` argument not working as expected.

## [0.5.2] - 2022-11-10
### Fixed
- Tree Constructor: Fix issue `dataframe_to_tree_by_relation` unable to find parent node.

## [0.5.1] - 2022-11-09
### Added
- Misc: Clean codes and documentation.

## [0.5.0] - 2022-11-09
### Added
- Misc: Clean codes and documentation.
### Changed
- Tree Exporter: Printing tree to group multiple arguments together.
- DAG and Tree Exporter: Export to dot able to plot multiple disjointed trees/dags, rename `bgcolor` to `bg_colour`.

## [0.4.6] - 2022-11-09
### Added
- Tree Constructor: From DataFrame of parent-child columns.
### Changed
- Tree Exporter: Printing tree to define node name or path, and default to const style.
- Tree Constructor: Rename `list_to_tree_tuples` to `list_to_tree_by_relation`.
- Tree Constructor: Remove parameter `sep` for `nested_dict_to_tree`.

## [0.4.5] - 2022-11-08
### Changed
- Tree Exporter: Printing tree with added ability to omit null attributes.

## [0.4.4] - 2022-11-08
### Fixed
- Tree Constructor: Handle adding attributes that are array-like - add array even when one of the items is null.

## [0.4.3] - 2022-11-08
### Added
- Node: Print format for BaseNode.

## [0.4.2] - 2022-11-08
### Fixed
- Tree Constructor: For list of tuples, handle cases where parent name is None.

## [0.4.1] - 2022-11-07
### Fixed
- Tree Constructor: Handle adding attributes that are array-like - error in drop_duplicate() and pd.isnull().

## [0.4.0] - 2022-11-07
### Added
- Tree Constructor: From list of tuples of parent-child.

## [0.3.3] - 2022-11-07
### Added
- DAG Exporter: To list, nested dictionary, pandas DataFrame.
### Changed
- BaseNode and DAGNode: Modify docstring.
- Tree Exporter: Support Nodes with same name.
- Tree Modifier: Modify docstring.
- Utility Iterator: Modify docstring.

## [0.3.2] - 2022-11-07
### Fixed
- Tree Exporter: Fix edge direction error.

## [0.3.1] - 2022-11-07
### Added
- Tree and DAG Exporter: More customizations for Node to dot and DAGNode to dot.

## [0.3.0] - 2022-11-05
### Added
- DAG Constructor: From list, nested dictionary, pandas DataFrame.
- Utility Iterator: DAG traversal methods.

### Changed
- Tree Exporter and DAG Exporter: More customizations for Node to dot and DAGNode to dot.

## [0.2.0] - 2022-11-03
### Added
- Node: DAGNode for creating DAG graph.
- Tree Exporter: Support Node to dot which can export to png, svg, jpeg, dot files.
- DAG Exporter: Support DAGNode to dot.

## [0.1.0] - 2022-11-01
### Added
- Node: Node and BaseNode.
- Tree Constructor: From list, nested dictionary, pandas DataFrame.
- Tree Exporter: To list, nested dictionary, pandas DataFrame.
- Tree Helper: Cloning, pruning trees, get difference between two trees.
- Tree Modifier: Shift and copy nodes within tree and between trees.
- Tree Search: Find single or multiple nodes based on name, attribute, or custom criteria.
- Utility Iterator: Tree traversal methods.
- Workflow To Do App: Tree use case with to-do list implementation.

[0.12.3]: https://github.com/kayjan/bigtree/compare/0.12.2...0.12.3
[0.12.2]: https://github.com/kayjan/bigtree/compare/0.12.1...0.12.2
[0.12.1]: https://github.com/kayjan/bigtree/compare/0.12.0...0.12.1
[0.12.0]: https://github.com/kayjan/bigtree/compare/0.11.0...0.12.0
[0.11.0]: https://github.com/kayjan/bigtree/compare/0.10.3...0.11.0
[0.10.3]: https://github.com/kayjan/bigtree/compare/0.10.2...0.10.3
[0.10.2]: https://github.com/kayjan/bigtree/compare/0.10.1...0.10.2
[0.10.1]: https://github.com/kayjan/bigtree/compare/0.10.0...0.10.1
[0.10.0]: https://github.com/kayjan/bigtree/compare/0.9.5...0.10.0
[0.9.5]: https://github.com/kayjan/bigtree/compare/0.9.4...0.9.5
[0.9.4]: https://github.com/kayjan/bigtree/compare/0.9.3...0.9.4
[0.9.3]: https://github.com/kayjan/bigtree/compare/0.9.2...0.9.3
[0.9.2]: https://github.com/kayjan/bigtree/compare/0.9.1...0.9.2
[0.9.1]: https://github.com/kayjan/bigtree/compare/0.9.0...0.9.1
[0.9.0]: https://github.com/kayjan/bigtree/compare/0.8.4...0.9.0
[0.8.4]: https://github.com/kayjan/bigtree/compare/0.8.3...0.8.4
[0.8.3]: https://github.com/kayjan/bigtree/compare/0.8.2...0.8.3
[0.8.2]: https://github.com/kayjan/bigtree/compare/0.8.1...0.8.2
[0.8.1]: https://github.com/kayjan/bigtree/compare/0.8.0...0.8.1
[0.8.0]: https://github.com/kayjan/bigtree/compare/0.7.4...0.8.0
[0.7.4]: https://github.com/kayjan/bigtree/compare/0.7.3...0.7.4
[0.7.3]: https://github.com/kayjan/bigtree/compare/0.7.2...0.7.3
[0.7.2]: https://github.com/kayjan/bigtree/compare/0.7.1...0.7.2
[0.7.1]: https://github.com/kayjan/bigtree/compare/0.7.0...0.7.1
[0.7.0]: https://github.com/kayjan/bigtree/compare/0.6.10...0.7.0
[0.6.10]: https://github.com/kayjan/bigtree/compare/0.6.9...0.6.10
[0.6.9]: https://github.com/kayjan/bigtree/compare/0.6.8...0.6.9
[0.6.8]: https://github.com/kayjan/bigtree/compare/0.6.7...0.6.8
[0.6.7]: https://github.com/kayjan/bigtree/compare/0.6.6...0.6.7
[0.6.6]: https://github.com/kayjan/bigtree/compare/0.6.5...0.6.6
[0.6.5]: https://github.com/kayjan/bigtree/compare/0.6.4...0.6.5
[0.6.4]: https://github.com/kayjan/bigtree/compare/0.6.3...0.6.4
[0.6.3]: https://github.com/kayjan/bigtree/compare/0.6.2...0.6.3
[0.6.2]: https://github.com/kayjan/bigtree/compare/0.6.1...0.6.2
[0.6.1]: https://github.com/kayjan/bigtree/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/kayjan/bigtree/compare/0.5.5...0.6.0
[0.5.5]: https://github.com/kayjan/bigtree/compare/0.5.4...0.5.5
[0.5.4]: https://github.com/kayjan/bigtree/compare/0.5.3...0.5.4
[0.5.3]: https://github.com/kayjan/bigtree/compare/0.5.2...0.5.3
[0.5.2]: https://github.com/kayjan/bigtree/compare/0.5.1...0.5.2
[0.5.1]: https://github.com/kayjan/bigtree/compare/0.5.0...0.5.1
[0.5.0]: https://github.com/kayjan/bigtree/compare/0.4.6...0.5.0
[0.4.6]: https://github.com/kayjan/bigtree/compare/0.4.5...0.4.6
[0.4.5]: https://github.com/kayjan/bigtree/compare/0.4.4...0.4.5
[0.4.4]: https://github.com/kayjan/bigtree/compare/0.4.3...0.4.4
[0.4.3]: https://github.com/kayjan/bigtree/compare/0.4.2...0.4.3
[0.4.2]: https://github.com/kayjan/bigtree/compare/0.4.1...0.4.2
[0.4.1]: https://github.com/kayjan/bigtree/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/kayjan/bigtree/compare/0.3.3...0.4.0
[0.3.3]: https://github.com/kayjan/bigtree/compare/0.3.2...0.3.3
[0.3.2]: https://github.com/kayjan/bigtree/compare/0.3.1...0.3.2
[0.3.1]: https://github.com/kayjan/bigtree/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/kayjan/bigtree/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/kayjan/bigtree/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/kayjan/bigtree/releases/tag/0.1.0

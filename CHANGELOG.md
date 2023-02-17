# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.0] - 2023-02-18
### Added
- Tree Modify: Accept `merge_leaves` type of modification, enhance documentation to provide more examples and illustrations.

## [0.6.10] - 2023-01-23
### Fixed
- Tree Construct: `str_to_tree` accept prefixes to support unicode characters in node names.

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
- Add Tips and Tricks to documentation (List Directory).

### Fixed
- DAGNode: Fix issue of duplicated parent constructor creating duplicated children.

## [0.5.5] - 2022-11-12
### Added
- More docstring examples.
- More test cases.

### Fixed
- Tree Modifier: Fix issue with `merge_children` argument not working as expected.

## [0.5.4] - 2022-11-12
### Added
- BaseNode: Add sort() to sort children.
- Node: Made more extendable with pre-/post-assign checks.
- Add Tips and Tricks to documentation (Extending Nodes).
- More test cases.

### Fixed
- Tree Search: Type hints

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
- Clean codes and documentation.

## [0.5.0] - 2022-11-09
### Added
- Clean codes and documentation.

### Changed
- Tree Exporter: Printing tree to group multiple arguments together.
- DAG and Tree Exporter: Export to dot able to plot multiple disjointed trees/dags, rename `bgcolor` to `bg_colour`

## [0.4.6] - 2022-11-09
### Added
- Tree Constructor: From DataFrame of parent-child columns.

### Changed
- Tree Exporter: Printing tree to define node name or path, and default to const style.
- Tree Constructor: Rename `list_to_tree_tuples` to `list_to_tree_by_relation`
- Tree Constructor: Remove parameter `sep` for `nested_dict_to_tree`

## [0.4.5] - 2022-11-08
### Changed
- Tree Exporter: Printing tree with added ability to omit null attributes.

## [0.4.4] - 2022-11-08
### Fixed
- Tree Constructor: Handle adding attributes that are array-like - add array even when one of the items is null

## [0.4.3] - 2022-11-08
### Added
- Node: Print format for BaseNode.

## [0.4.2] - 2022-11-08
### Fixed
- Tree Constructor: For list of tuples, handle cases where parent name is None

## [0.4.1] - 2022-11-07
### Fixed
- Tree Constructor: Handle adding attributes that are array-like - error in drop_duplicate() and pd.isnull()

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
- Tree Exporter and DAG Exporter: More customizations for Node to dot and DAGNode to dot.

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

[0.7.0]: https://github.com/kayjan/bigtree/compare/v0.6.10...v0.7.0
[0.6.10]: https://github.com/kayjan/bigtree/compare/v0.6.9...v0.6.10
[0.6.9]: https://github.com/kayjan/bigtree/compare/v0.6.8...v0.6.9
[0.6.8]: https://github.com/kayjan/bigtree/compare/v0.6.7...v0.6.8
[0.6.7]: https://github.com/kayjan/bigtree/compare/v0.6.6...v0.6.7
[0.6.6]: https://github.com/kayjan/bigtree/compare/v0.6.5...v0.6.6
[0.6.5]: https://github.com/kayjan/bigtree/compare/v0.6.4...v0.6.5
[0.6.4]: https://github.com/kayjan/bigtree/compare/v0.6.3...v0.6.4
[0.6.3]: https://github.com/kayjan/bigtree/compare/v0.6.2...v0.6.3
[0.6.2]: https://github.com/kayjan/bigtree/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/kayjan/bigtree/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/kayjan/bigtree/compare/v0.5.5...v0.6.0
[0.5.5]: https://github.com/kayjan/bigtree/compare/v0.5.4...v0.5.5
[0.5.4]: https://github.com/kayjan/bigtree/compare/v0.5.3...v0.5.4
[0.5.3]: https://github.com/kayjan/bigtree/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/kayjan/bigtree/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/kayjan/bigtree/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/kayjan/bigtree/compare/v0.4.6...v0.5.0
[0.4.6]: https://github.com/kayjan/bigtree/compare/v0.4.5...v0.4.6
[0.4.5]: https://github.com/kayjan/bigtree/compare/v0.4.4...v0.4.5
[0.4.4]: https://github.com/kayjan/bigtree/compare/v0.4.3...v0.4.4
[0.4.3]: https://github.com/kayjan/bigtree/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/kayjan/bigtree/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/kayjan/bigtree/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/kayjan/bigtree/compare/v0.3.3...v0.4.0
[0.3.3]: https://github.com/kayjan/bigtree/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/kayjan/bigtree/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/kayjan/bigtree/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/kayjan/bigtree/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/kayjan/bigtree/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kayjan/bigtree/releases/tag/v0.1.0

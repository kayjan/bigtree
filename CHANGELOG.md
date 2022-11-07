# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Work In Progress
- Node: WeightedNode for weighted edge tree implementation.

## [0.4.2] - 2022-11-08
### Fixed
- Tree Constructors: For list of tuples, handle cases where parent name is None

## [0.4.1] - 2022-11-07
### Fixed
- Tree Constructors: Able to handle adding attributes that are list - error in drop_duplicate() and pd.isnull()

## [0.4.0] - 2022-11-07
### Added
- Tree Constructors: From list of tuples of parent-child.

## [0.3.3] - 2022-11-07
### Added
- DAG Exporter: To list, nested dictionary, pandas DataFrame.

### Changed
- BaseNode and DAGNode: Modify docstring.
- Tree Exporter: Support Nodes with same name.
- Tree Modifier: Modify docstring.
- Utility Iterators: Modify docstring.

## [0.3.2] - 2022-11-07
### Fixed
- Tree Exporter: Fix edge direction error.

## [0.3.1] - 2022-11-07
### Added
- Tree Exporter and DAG Exporter: More customizations for Node to dot and DAGNode to dot.

## [0.3.0] - 2022-11-05
### Added
- DAG Constructors: From list, nested dictionary, pandas DataFrame.
- Utility Iterators: DAG traversal methods.

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
- Tree Constructors: From list, nested dictionary, pandas DataFrame.
- Tree Exporter: To list, nested dictionary, pandas DataFrame.
- Tree Helper: Cloning, pruning trees, get difference between two trees.
- Tree Modifier: Shift and copy nodes within tree and between trees.
- Tree Search: Find single or multiple nodes based on name, attribute, or custom criteria.
- Utility Iterators: Tree traversal methods.
- Workflow To Do App: Tree use case with to-do list implementation.

[0.4.2]: https://github.com/kayjan/bigtree/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/kayjan/bigtree/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/kayjan/bigtree/compare/v0.3.3...v0.4.0
[0.3.3]: https://github.com/kayjan/bigtree/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/kayjan/bigtree/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/kayjan/bigtree/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/kayjan/bigtree/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/kayjan/bigtree/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kayjan/bigtree/releases/tag/v0.1.0

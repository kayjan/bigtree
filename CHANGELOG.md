# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Node: DAGNode for creating DAG graph.
- Tree Exporter: To dot which can export to png, jpeg, dot files.

### Work In Progress
- Node: WeightedNode for weighted edge tree implementation.
- Tree Exporter: Support DAGNode to dot.

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

[Unreleased]: https://github.com/kayjan/bigtree/compare/HEAD...v0.2.0
[0.2.0]: https://github.com/kayjan/bigtree/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kayjan/bigtree/releases/tag/v0.1.0

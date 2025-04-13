# 🍂 Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.27.0] - 2025-14-13
### Added:
- DAG/Tree Parsing: Add parsing module to get path from origin node to destination node, this was already available in
`.go_to()` function, but abstracted out to a parsing module. Tree parsing module has another method of getting common
ancestors between multiple branches of the same tree.

## [0.26.0] - 2025-14-13
### Added:
- Tree Modify: Merge trees to merge multiple trees/branches into a single tree.

## [0.25.4] - 2025-04-04
- Docs: Clean up docstring where possible and relevant.

## [0.25.3] - 2025-03-30
### Changed:
- Docs: Deduplicate type hint and default value in docstrings.
- Misc: Clean up repository by abstracting functions into inheritable classes.

## [0.25.2] - 2025-03-14
### Added:
- Tree Exporter: `hprint_tree` and `hyield_tree` to support spacing parameter.
### Fixed:
- Tree Exporter: Case when parent is longer than child in `vprint_tree` and `vyield_tree`.

## [0.25.1] - 2025-02-28
### Added:
- Tree Exporter: `vprint_tree` to have same arguments as `vyield_tree`, add more test cases.
- Tree Exporter: `hprint_tree` to support multiline node name, alias, and border style.

## [0.25.0] - 2025-02-25
### Added:
- Tree Exporter: `tree_to_pillow_graph` method to allow cmap for node background and generic kwargs for yield_tree.
- Tree Exporter: `vprint_tree` method to print trees vertically, able to use `.vshow()` as well.
### Changed:
- Tree Exporter: Minor refactoring to deduplicate code in export module.

## [0.24.0] - 2025-02-09
### Added:
- Docs: Tips for setting custom coordinates for plots.
- Tree Exporter: `tree_to_pillow_graph` method to export tree to pillow image in graph format.
### Changed:
- Plot: Allow `reverse` argument to allow top-bottom y coordinates in Reingold Tilford algorithm.
- Docs: Add more elaboration for exporting to image for tree and dag.
- Misc: Split tree/construct and tree/export into multiple files.

## [0.23.1] - 2025-01-22
### Changed:
- Tree Search: Search relative path allows unix folder expression for leading sep symbol.
- Node: Updated Node signature to reflect that name is mandatory.

## [0.23.0] - 2024-12-26
### Changed:
- Tree Modify: Update documentation and docstring with some rephrasing.
- Tree Modify: Clean up test cases.
### Added:
- Tree Modify: Add parameter `merge_attribute` to allow from-node and to-node attributes to be merged if there are clashes.
### Fixed:
- Tree Modify: Fixed bug when `merge_children` is used with `overriding` as the `merge_children` value is changed in
for-loop (bad move, literally). Modified the logic such that if there are clashes for `merge_children=True, overriding=True`,
the origin node parent and destination node children are preserved. The origin node's children are overridden.
**This might not be backwards-compatible!**

## [0.22.3] - 2024-11-14
### Added:
- Tree Helper: `get_tree_diff_dataframe` to get tree differences in pd.DataFrame for customised processing and handling.
### Changed:
- Tree Helper: Get tree diff logic to be faster to compare all attribute list and data at once (for attr diff).
- Tree Helper: Get tree diff logic to be faster to add suffix at the end (for path diff).
- Tree Helper: Get tree diff logic to be faster to detect moved indicator using dataframe operations (for detail).

## [0.22.2] - 2024-11-11
### Added:
- Tree Export: Print tree to allow alias.
- Tree Export: Mermaid diagram to include theme.
- Tree Helper: Get tree diff to take in `aggregate` parameter to indicate differences at the top-level node.
- Misc: Documentation to include tips and tricks on working with custom classes.
### Changed:
- Misc: Docstring to indicate usage prefers `node_name` to `name`.
- Misc: Standardise testing fixtures.
### Fixed:
- Misc: Polars set up to work on laptop with M1 chip.
- Misc: Indentation in documentation.
- Tree Export: Mermaid diagram title to add newline.
- Tree Export: Polars unit test to work with old (<=1.9.0) and new polars version.
- Tree Helper: Get tree diff string replacement bug when the path change is substring of another path.

## [0.22.1] - 2024-11-03
### Added:
- Misc: Documentation to rely on jupyter notebook.
### Changed:
- Tree Export: Exporting to dot allow node_attr and edge_attr to modify node before retrieving node name.
- Misc: All code reference to node_name (immutable) instead of name (mutable).

## [0.22.0] - 2024-11-03
### Added:
- Tree Helper: Accept parameter `detail` to show the different types of shift e.g., moved / added / removed. By default
it is false.

## [0.21.3] - 2024-10-16
### Added:
- Tree Node: Docstring indentation and additional information for Node creation.
- Misc: GitHub star diagram to README file.
### Changed:
- Tree Helper: Get tree diff to handle `sep` that are different for tree and other_tree, this will throw error now.
- Tree Helper: Get tree diff to handle `sep` that contains forbidden symbols, this will change the `sep` to a fallback sep.
- Tree Helper: Get tree diff to sort tree before returning the tree diff.
### Fixed:
- [#306] Tree Helper: Get tree diff to handle `sep` that is different from default.

## [0.21.2] - 2024-10-14
### Added:
- Misc: Pull request template.
### Fixed:
- Tree Helper: Subtree to inherit `sep` property from root node.

## [0.21.1] - 2024-08-29
### Changed:
- Misc: Import module instead of functions, following Google Python Style Guide.
- Docs: Documentation of `plot_tree` in tree demonstration and installation instructions.

## [0.21.0] - 2024-08-26
### Added:
- Tree Plot: Plot tree using matplotlib library, added matplotlib as optional dependency.
- BaseNode: Add plot method.
### Changed:
- Misc: Rename assertion function.
- Misc: Optional dependencies imported as MagicMock

## [0.20.1] - 2024-08-24
### Changed:
- Misc: Documentation update contributing instructions.

## [0.20.0] - 2024-08-24
### Added:
- [#285] Tree Exporter: `print_tree` and `hprint_tree` to accept keyword arguments for printing.
- Misc: Template for release notes.
### Changed:
- Misc: Enhanced template for issues (bugfix/feature release).
### Fixed:
- Tree Exporter: `tree_to_mermaid` fix for root node to have node attribute.

## [0.19.4] - 2024-08-15
### Changed:
- Docs: Clean CSS for playground.
- Misc: Refactor tests for `tree_to_mermaid`.
- Misc: Allow untyped calls in mypy type checking due to ImageFont.truetype call.
### Fixed:
- Tree Exporter: `tree_to_mermaid` fix where the node attribute is added wrongly to the wrong node.
- Misc: Fix and update code examples in docstring.
- Misc: Fix test cases for pydot due to code upgrade.

## [0.19.3] - 2024-07-09
### Fixed:
- Docs: Update links in README and rtd docs.

## [0.19.2] - 2024-06-28
### Added:
- Docs: Add description and credits to playground.
- Misc: Add template for asking question in Discussions.
### Changed:
- Docs: Homepage to include links to playground, modify emoji location.
- Docs: Playground modify code and code snippet layout.
### Fixed:
- Misc: Skip codecov github action for PR from other users.

## [0.19.1] - 2024-06-26
### Changed:
- Docs: Add playground and glossary section to documentation.

## [0.19.0] - 2024-06-15
### Changed:
- Tree Exporter: Print functions to accept custom style that is implemented as dataclass, this is a more  object-oriented
way of parsing arguments. This affects functions `print_tree`, `yield_tree`, `hprint_tree`, and `hyield_tree`. The
argument `custom_style` is deprecated, and argument `style` is used instead.
**This might not be backwards-compatible!**
- Misc: Update docstrings to be more comprehensive for tree constructor and tree exporter.
- Misc: Update documentation badges and conda information.

## [0.18.3] - 2024-06-05
### Changed:
- Binary Tree Constructor: Type hints to return more generic TypeVar for use with subclasses.
- DAG Constructor: Type hints to return more generic TypeVar for use with subclasses.
- [#247] Tree Construct: Type hints to return more generic TypeVar for use with subclasses.
- Tree Modifier: Type hints to return more generic TypeVar for use with subclasses.
- Misc: Documentation to include more contribution information and guidelines.

## [0.18.2] - 2024-06-01
### Changed:
- Tree Search: Standardize handling of singular and plural search.
- Tree Search: Add `find_relative_path` that return a single node from search and
rename existing `find_relative_path` to `find_relative_paths`.
**This might not be backwards-compatible!**

## [0.18.1] - 2024-05-30
### Changed:
- Misc: Remove support of Python 3.7 due to incompatibility with polars.
### Fixed:
- Tree Constructor and Exporter: Error handling when user only partially download optional dependencies of pandas/polars.

## [0.18.0] - 2024-05-28
### Added:
- Tree Constructor: Polars method `polars_to_tree`, `polars_to_tree_by_relation`, `add_polars_to_tree_by_path`,
and `add_polars_to_tree_by_name`.
- Tree Exporter: Polars method `tree_to_polars`.
### Fixed:
- Misc: Documentation to update mkdocs-material version for social plugin.
- Misc: Update links in README.
- Misc: Fix mypy typing.

## [0.17.2] - 2024-04-24
### Changed:
- DAG Constructor: `list_to_dag` and `dict_to_dag` does not rely on `dataframe_to_dag` as pandas dataframe operation
is phased out.
### Fixed:
- DAG Constructor: Handle cases where reserved keywords are part of attribute upon creation and throw error accordingly.
- [#224] Tree/DAG Constructor: Null checks to not interpret 0 as null, this affects `dataframe_to_tree_by_relation`,
`add_dataframe_to_tree_by_path`, `add_dataframe_to_tree_by_name`, `dataframe_to_tree`, and `dataframe_to_dag`.
This will also affect showing/printing of trees when `attr_omit_null` is set to True.

## [0.17.1] - 2024-04-23
### Fixed
- [#222] Tree Constructor: `dataframe_to_tree_by_relation` duplicate root node name error message to handle
different data types.
- Misc: Update links in README.

## [0.17.0] - 2024-04-04
### Added
- Misc: Group tests for benchmark timings to compare the timings by multiplier more effectively.
### Changed
- Tree Constructor: `add_dict_to_tree_by_name` and `add_dataframe_to_tree_by_name` modifies tree in-place instead
of returning new tree, and does not accept `join_type` as argument as pandas dataframe operation is phased out.
If there are clashing attributes, only those that have values will be replaced.
**This might not be backwards-compatible!**
- Tree Constructor: `dataframe_to_tree` no longer relies on `add_dataframe_to_tree_by_path` as it performs
assertion checks twice. This leads to 5% improvement in timings for a tree with 10000 nodes, averaged across 10 runs.
- Misc: Abstract out assertion checks for empty dataframe and duplicate attribute.
- Misc: Abstract out logic for checking null and filtering attributes.
- Misc: Optimisation in dictionary and dataframe operations.
### Fixed
- Tree Constructor: `dict_to_tree` no longer uses dataframe operations, leading to 33% improvement in timings for
a tree with 10000 nodes, averaged across 10 runs. The resulting data type of node follows the dictionary exactly,
compared to the previous dataframe operations that may change the dtypes for certain columns.
**This might not be backwards-compatible!**
- Tree Constructor: `dataframe_to_tree_by_relation` fix root node detection logic, ignore existing name column,
ignore non-attribute columns, ignore null attribute columns.
- Tree Constructor: `add_dataframe_to_tree_by_path` ignore existing name column, ignore non-attribute columns,
ignore null attribute columns.
- Tree Constructor: `add_dataframe_to_tree_by_name` ignore existing name column, ignore non-attribute columns,
ignore null attribute columns.
- Tree Constructor: `dataframe_to_tree` ignore existing name column, ignore non-attribute columns,
ignore null attribute columns.
- DAG Constructor: `dataframe_to_dag` ignore existing name column, ignore non-attribute columns,
ignore null attribute columns.

## [0.16.4] - 2024-03-14
### Fixed
- [#216] Tree Exporter: Fix nan checker when printing trees.

## [0.16.3] - 2024-03-14
### Added
- BaseNode: Add diameter property.
- Misc: Tests to include benchmark timings for tree creation, compare benchmark tests across commits, reject pull request if benchmark tests fails.
- Misc: Documentation to include benchmark results.
### Changed
- Misc: Documentation to enable zooming in of images, add navigation section headers, remove some meta tags.
- Misc: Split up testing into multiple conftest files.
### Fixed
- Tree Constructor: Tree creation from dictionary adds None for empty attributes instead of np.nan.
- [#216] Tree Exporter: `attr_omit_null` to handle nan/null values in addition to checking for None.

## [0.16.2] - 2024-02-06
### Added
- Misc: Documentation plugin Termynal for code animation.
- Misc: Usage of `docstr-coverage`.
- Misc: Docstrings for nested functions to pass `docstr-coverage`.
### Changed
- [#185] BaseNode: Make assertion checks optional.
- Misc: Documentation CSS for h1 display for windows compatibility, modify the related links on main page.

## [0.16.1] - 2024-01-29
### Fixed
- Misc: Compatibility of mkdocs with readthedocs.

## [0.16.0] - 2024-01-28
### Added
- Misc: Documentation using mkdocs.
### Changed
- Misc: Markdown edit for README, CHANGELOG.
- Misc: Docstring to indicate Examples, to indicate exceptions for BaseNode and DAGNode, simplify code for tree modification.
### Fixed
- Misc: Docstring bullet point alignment, images compatibility with markdown.

## [0.15.7] - 2024-01-26
### Added
- Misc: Sphinx documentation to support mermaid markdown images, reflect CHANGELOG section, add more emojis.
### Changed
- Misc: Update SEO image.
- Misc: Fix Sphinx documentation font size difference between web and mobile, include last updated date.
- Misc: Upgrade package versions in pre-commit hook.
### Fixed
- Tree Exporter: `hprint_tree` and `hyield_tree` to be compatible with `BinaryNode` where child nodes can be None type.

## [0.15.6] - 2024-01-20
### Added
- DAGNode: Able to access and delete node children via name with square bracket accessor with `__getitem__` and `__delitem__` magic methods.
- DAGNode: Able to delete all children for a node.
- DAGNode: Able to check if node contains child node with `__contains__` magic method.
- DAGNode: Able to iterate the node to access children with `__iter__` magic method.
### Changed
- Tree Search: Modify type hints to include DAGNode for `find_children`, `find_child`, and `find_child_by_name`.
- Misc: Neater handling of strings for tests.
- Misc: Documentation enhancement to split README into multiple files.
- Misc: New Sphinx documentation theme.

## [0.15.5] - 2024-01-17
### Changed
- Misc: Neater handling of strings for tests.
- Misc: Better examples for merging trees and weighted trees in Sphinx documentation.
- Misc: Fix links and introduce unreleased segment in CHANGELOG.

## [0.15.4] - 2024-01-11
### Changed
- Tree Exporter: `hprint_tree` and `hyield_tree` to allow hiding names of intermediate node.
### Fixed
- Tree Constructor: `newick_to_tree` to handle invalid closing and use of apostrophe.
- Tree Exporter: `tree_to_newick` to handle special characters by wrapping them in apostrophe.

## [0.15.3] - 2024-01-08
### Added
- Tree Helper: `get_subtree` method to retrieve subtree.

## [0.15.2] - 2024-01-08
### Added
- Tree Exporter: `hprint_tree` and `hyield_tree` to print and retrieve results for tree in horizontal orientation.
- Node: Add `hshow` method to print tree in horizontal orientation to console.

## [0.15.1] - 2024-01-05
### Added
- Tree Constructor: `newick_to_tree` to convert Newick notation to tree.
### Changed
- Tree Exporter: `tree_to_newick` to accept more parameters to parse length and attributes.
### Fixed
- Misc: Automate doctest setup to use os operations instead of string operations.

## [0.15.0] - 2024-01-02
### Added
- Tree Exporter: Export to Newick notation with `tree_to_newick`.
### Changed
- Tree Helper: Pruning tree to support pruning of multiple paths (accepts list of string).
- Tree Helper: Pruning tree to support pruning of an exact path (i.e., remove descendants) with `exact` parameter, default is prune and keep descendants.

## [0.14.8] - 2023-12-25
### Changed
- Tree Modifier: Enhance documentation examples.
- Workflow To Do App: Change import and export logic.
- Misc: Organize assets folder based on whether it originated from README, docstrings, or sphinx documentation.
- Misc: Rename functions in `plot.py` utils file for coverage report.
### Fixed
- Misc: Fix doctests and automate doctest checks.

## [0.14.7] - 2023-12-22
### Changed
- Tree Helper: Enhance `get_tree_diff` to compare tree attributes by taking in `attr_list` parameter, and indicates difference with `(~)`.
### Fixed
- Tree Helper: `get_tree_diff` compare tree structure by considering all nodes (previously only consider leaf nodes).

## [0.14.6] - 2023-12-14
### Added
- Node: Able to access and delete node children via name with square bracket accessor with `__getitem__` and `__delitem__` magic methods.
- BaseNode/Node/BinaryNode: Able to add one or more children with `append` and `extend` methods.
- BaseNode/Node/BinaryNode: Able to check if node contains child node with `__contains__` magic method.
- BaseNode/Node/BinaryNode: Able to iterate the node to access children with `__iter__` magic method. Results in children setter to only accept list/tuple/set instead of iterable types.
### Changed
- Tree Exporter: `tree_to_dot` accepts callable to set node and edge attrs for custom node (backward-compatible).
- Tree Exporter: `tree_to_mermaid` accepts callable to set node shape attr, edge arrow attr and node attr for custom node (backward-compatible).
- Tree Exporter: Change delimiter for `tree_to_mermaid` to prevent possible path confusion (backward-compatible).
- Misc: Code abstraction for assertion checks and constants.
- Misc: Documentation for exporting tree/dag to dot.

## [0.14.5] - 2023-11-24
### Changed
- Misc: Update SECURITY file.
- Misc: Enhance documentation to add more emoji and highlight code blocks.

## [0.14.4] - 2023-11-04
### Changed
- Misc: Clean up github actions.

## [0.14.3] - 2023-10-31
### Added
- Misc: Publish to conda, enable automated publishing to conda-forge in addition to existing PyPI.
- Misc: Tree demonstration code for `shift_and_replace_nodes` and `copy_and_replace_nodes_from_tree_to_tree` in README.

## [0.14.2] - 2023-10-21
### Added
- Misc: RTD integration.
- Misc: Enable manual publishing of python package.

## [0.14.1] - 2023-10-18
### Added
- Misc: Change main branch checks if the latest version exists (using git tag) before publishing package and building documentation.

## [0.14.0] - 2023-10-18
### Added
- Tree Modifier: Shift nodes with replacement of to-node with `shift_and_replace_nodes`.
- Tree Modifier: Copy nodes from tree to tree with replacement of to-node with `copy_and_replace_nodes_from_tree_to_tree`.
- Tree Modifier: Any permutation of configuration with replacement of to-node with `replace_logic`.
- Tree Modifier: Add relevant test cases and documentations accordingly.

## [0.13.3] - 2023-10-17
### Added
- Misc: Add automatic release notes with content into GitHub workflow.

## [0.13.2] - 2023-10-17
### Added
- Misc: Add automatic release notes into GitHub workflow.

## [0.13.1] - 2023-10-15
### Added
- Misc: Add automatic comment on code coverage to pull requests into GitHub workflow.
- Misc: Add more checks into pre-commit.

## [0.13.0] - 2023-09-29
### Added
- Tree Exporter: Export tree to flowchart diagram in mermaid markdown format using `tree_to_mermaid`.
### Changed
- Tree Exporter: Relax type hinting using TypeVar for `clone_tree`.
- Tree Helper: Accept Iterable instead of List for custom_style attribute of `yield_tree` and `print_tree`.
- Misc: Fix docstring for better presentation of code vs variable vs normal text.

## [0.12.5] - 2023-09-26
### Added
- Utility Groot: Add test cases.
### Fixed
- Tree Exporter: `tree_to_pillow` function to reference online font file instead of relative path.

## [0.12.4] - 2023-09-25
### Added
- Utility Groot: Add groot utility functions.

## [0.12.3] - 2023-09-17
### Changed
- Clearer documentation, fix docstring phrasing and spelling.
- Clearer error messages, standardize error messages.

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
- Misc: Fix Calendar workflow to throw error when `to_dataframe` method is called on empty calendar.
- Tree/DAGNode Exporter, Tree Helper, Tree Search: Relax type hinting using TypeVar.

## [0.11.0] - 2023-09-08
### Added
- Tree Helper: `prune_tree` to allow pruning by `prune_path` and `max_depth`.
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
- Misc: Add init files, add link to discussions to README and pyproject, add sphinx coverage shortcuts.
### Fixed
- [#66] DAGNode/Node: Children constructor to allow Iterable types, fix issue of lists being mutable.
- [#67] Node: `path_name` to reduce number of recursive calls to root node for `sep`.

## [0.9.4] - 2023-06-18
### Added
- Tree Constructor: `list_to_tree_by_relation` and `dataframe_to_tree_by_relation` method to allow duplicate intermediate nodes (default is false).
- DAG Exporter: Add `node_shape` parameter in `dag_to_dot` export function for easier way to customize node shape.
- Misc: More test cases.
- Misc: Add security instructions on how to raise vulnerabilities.
- Misc: Add Calendar workflow to documentation.
### Changed
- Tree Constructor: `add_dict_to_tree_by_name` method rename argument from `path_attrs` to `name_attrs`.
- Misc: Modify contributing instructions.
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
- Node: Add `show` method to print tree to console.
- Workflow Calendar: Tree use case with calendar implementation.

## [0.9.1] - 2023-03-30
### Changed
- Node: Add `sep` parameter to constructor instead of using getter and setter methods to set `sep`.

## [0.9.0] - 2023-03-29
### Added
- Tree Modifier: Ability to copy/shift nodes with full path in `from_paths` for faster search performance, add `with_full_path` parameter.
### Changed
- Tree Modifier: Enforce paths in `to_paths` to be full path for faster search performance.
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
- Tree Search: Rename `find_children` to `find_child_by_name` for clarity.
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
- Misc: Type checking with `mypy`, add type checks to pre-commit hooks.
### Changed
- DAGNode: `go_to` method to be consistent with `List[List[DAGNode]]` type.
### Fixed
- Tree Exporter: Exception handling in `yield_tree` if `node_name_or_path` is not found.
- Workflow: Exception handling in prioritizing item/list if item/list is not the correct tree depth.
- Workflow: Exception handling in removing item/list if item/list is not found.

## [0.7.4] - 2023-02-27
### Fixed
- Tree Constructor: Fix pandas SettingwithCopyWarning when performing dataframe operations.

## [0.7.3] - 2023-02-25
### Added
- Tree Exporter: Fix `print_tree` checking attributes with `hasattr` to handle cases of null or 0 value attributes, add more test cases.
- Misc: Add more description to Contributing.

## [0.7.2] - 2023-02-18
### Added
- Tree Exporter: Add `node_shape` parameter in `tree_to_dot` export function for easier way to customize node shape.

## [0.7.1] - 2023-02-18
### Added
- BaseNode/Node: Add `go_to` BaseNode method to travel from one node to another node from the same tree.
- DAGNode: Add `go_to` DAGNode method to travel from one node to another node from the same DAG.

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
- Binary Tree: Change `BNode` to `BinaryNode`, and construct method `list_to_btree` to `list_to_binarytree`.

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
- Node: Make class more extendable with pre-/post-assign checks.
- Misc: Add Tips and Tricks to documentation (Extending Nodes).
- Misc: More test cases.
### Fixed
- Tree Search: Type hints.

## [0.5.3] - 2022-11-11
### Added
- DAG and Tree Exporter: More customisations allowed on edges.
- Misc: Add Tips and Tricks to documentation (Weighted Trees, Merging Trees).
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
- Tree Exporter: Print tree to group multiple arguments together.
- DAG and Tree Exporter: Export to dot able to plot multiple disjointed trees/dags, rename `bgcolor` to `bg_colour`.

## [0.4.6] - 2022-11-09
### Added
- Tree Constructor: From DataFrame of parent-child columns.
### Changed
- Tree Exporter: Print tree to define node name or path, and default to const style.
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
- Tree and DAG Exporter: More customisations for Node to dot and DAGNode to dot.

## [0.3.0] - 2022-11-05
### Added
- DAG Constructor: From list, nested dictionary, pandas DataFrame.
- Utility Iterator: DAG traversal methods.

### Changed
- Tree Exporter and DAG Exporter: More customisations for Node to dot and DAGNode to dot.

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
- Tree Helper: Clone, prune trees, get difference between two trees.
- Tree Modifier: Shift and copy nodes within tree and between trees.
- Tree Search: Find single or multiple nodes based on name, attribute, or custom criteria.
- Utility Iterator: Tree traversal methods.
- Workflow To Do App: Tree use case with to-do list implementation.

[Unreleased]: https://github.com/kayjan/bigtree/compare/0.27.0...HEAD
[0.27.0]: https://github.com/kayjan/bigtree/compare/0.26.4...0.27.0
[0.26.0]: https://github.com/kayjan/bigtree/compare/0.25.4...0.26.0
[0.25.4]: https://github.com/kayjan/bigtree/compare/0.25.3...0.25.4
[0.25.3]: https://github.com/kayjan/bigtree/compare/0.25.2...0.25.3
[0.25.2]: https://github.com/kayjan/bigtree/compare/0.25.1...0.25.2
[0.25.1]: https://github.com/kayjan/bigtree/compare/0.25.0...0.25.1
[0.25.0]: https://github.com/kayjan/bigtree/compare/0.24.0...0.25.0
[0.24.0]: https://github.com/kayjan/bigtree/compare/0.23.1...0.24.0
[0.23.1]: https://github.com/kayjan/bigtree/compare/0.23.0...0.23.1
[0.23.0]: https://github.com/kayjan/bigtree/compare/0.22.3...0.23.0
[0.22.3]: https://github.com/kayjan/bigtree/compare/0.22.2...0.22.3
[0.22.2]: https://github.com/kayjan/bigtree/compare/0.22.1...0.22.2
[0.22.1]: https://github.com/kayjan/bigtree/compare/0.22.0...0.22.1
[0.22.0]: https://github.com/kayjan/bigtree/compare/0.21.3...0.22.0
[0.21.3]: https://github.com/kayjan/bigtree/compare/0.21.2...0.21.3
[0.21.2]: https://github.com/kayjan/bigtree/compare/0.21.1...0.21.2
[0.21.1]: https://github.com/kayjan/bigtree/compare/0.21.0...0.21.1
[0.21.0]: https://github.com/kayjan/bigtree/compare/0.20.1...0.21.0
[0.20.1]: https://github.com/kayjan/bigtree/compare/0.20.0...0.20.1
[0.20.0]: https://github.com/kayjan/bigtree/compare/0.19.4...0.20.0
[0.19.4]: https://github.com/kayjan/bigtree/compare/0.19.3...0.19.4
[0.19.3]: https://github.com/kayjan/bigtree/compare/0.19.2...0.19.3
[0.19.2]: https://github.com/kayjan/bigtree/compare/0.19.1...0.19.2
[0.19.1]: https://github.com/kayjan/bigtree/compare/0.19.0...0.19.1
[0.19.0]: https://github.com/kayjan/bigtree/compare/0.18.3...0.19.0
[0.18.3]: https://github.com/kayjan/bigtree/compare/0.18.2...0.18.3
[0.18.2]: https://github.com/kayjan/bigtree/compare/0.18.1...0.18.2
[0.18.1]: https://github.com/kayjan/bigtree/compare/0.18.0...0.18.1
[0.18.0]: https://github.com/kayjan/bigtree/compare/0.17.2...0.18.0
[0.17.2]: https://github.com/kayjan/bigtree/compare/0.17.1...0.17.2
[0.17.1]: https://github.com/kayjan/bigtree/compare/0.17.0...0.17.1
[0.17.0]: https://github.com/kayjan/bigtree/compare/0.16.4...0.17.0
[0.16.4]: https://github.com/kayjan/bigtree/compare/0.16.3...0.16.4
[0.16.3]: https://github.com/kayjan/bigtree/compare/0.16.2...0.16.3
[0.16.2]: https://github.com/kayjan/bigtree/compare/0.16.1...0.16.2
[0.16.1]: https://github.com/kayjan/bigtree/compare/0.16.0...0.16.1
[0.16.0]: https://github.com/kayjan/bigtree/compare/0.15.7...0.16.0
[0.15.7]: https://github.com/kayjan/bigtree/compare/0.15.6...0.15.7
[0.15.6]: https://github.com/kayjan/bigtree/compare/0.15.5...0.15.6
[0.15.5]: https://github.com/kayjan/bigtree/compare/0.15.4...0.15.5
[0.15.4]: https://github.com/kayjan/bigtree/compare/0.15.3...0.15.4
[0.15.3]: https://github.com/kayjan/bigtree/compare/0.15.2...0.15.3
[0.15.2]: https://github.com/kayjan/bigtree/compare/0.15.1...0.15.2
[0.15.1]: https://github.com/kayjan/bigtree/compare/0.15.0...0.15.1
[0.15.0]: https://github.com/kayjan/bigtree/compare/0.14.8...0.15.0
[0.14.8]: https://github.com/kayjan/bigtree/compare/0.14.7...0.14.8
[0.14.7]: https://github.com/kayjan/bigtree/compare/0.14.6...0.14.7
[0.14.6]: https://github.com/kayjan/bigtree/compare/0.14.5...0.14.6
[0.14.5]: https://github.com/kayjan/bigtree/compare/0.14.4...0.14.5
[0.14.4]: https://github.com/kayjan/bigtree/compare/0.14.3...0.14.4
[0.14.3]: https://github.com/kayjan/bigtree/compare/0.14.2...0.14.3
[0.14.2]: https://github.com/kayjan/bigtree/compare/0.14.1...0.14.2
[0.14.1]: https://github.com/kayjan/bigtree/compare/0.14.0...0.14.1
[0.14.0]: https://github.com/kayjan/bigtree/compare/0.13.3...0.14.0
[0.13.3]: https://github.com/kayjan/bigtree/compare/0.13.2...0.13.3
[0.13.2]: https://github.com/kayjan/bigtree/compare/0.13.1...0.13.2
[0.13.1]: https://github.com/kayjan/bigtree/compare/0.13.0...0.13.1
[0.13.0]: https://github.com/kayjan/bigtree/compare/0.12.5...0.13.0
[0.12.5]: https://github.com/kayjan/bigtree/compare/0.12.4...0.12.5
[0.12.4]: https://github.com/kayjan/bigtree/compare/0.12.3...0.12.4
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

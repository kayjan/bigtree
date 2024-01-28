---
title: Tree
---

# 🌲 Tree

For **Tree** implementation, there are 9 main components.

## [**🌺 Node**](bigtree/node/index.md)
- ``BaseNode``, extendable class
- ``Node``, BaseNode with node name attribute

## [**✨ Constructing Tree**](bigtree/tree/construct.md)
- From `Node`, using parent and children constructors
- From *str*, using tree display or Newick string notation
- From *list*, using paths or parent-child tuples
- From *nested dictionary*, using path-attribute key-value pairs or recursive structure
- From *pandas DataFrame*, using paths or parent-child columns
- Add nodes to existing tree using path string
- Add nodes and attributes to existing tree using *dictionary* or *pandas DataFrame*, using path
- Add only attributes to existing tree using *dictionary* or *pandas DataFrame*, using node name

## [**➰ Traversing Tree**](bigtree/utils/iterators.md)
- Pre-Order Traversal
- Post-Order Traversal
- Level-Order Traversal
- Level-Order-Group Traversal
- ZigZag Traversal
- ZigZag-Group Traversal

## [**📝 Modifying Tree**](bigtree/tree/modify.md)
- Copy nodes from location to destination
- Shift nodes from location to destination
- Shift and replace nodes from location to destination
- Copy nodes from one tree to another
- Copy and replace nodes from one tree to another

## [**🔍 Tree Search**](bigtree/tree/search.md)
- Find multiple nodes based on name, partial path, relative path, attribute value, user-defined condition
- Find single nodes based on name, partial path, relative path, full path, attribute value, user-defined condition
- Find multiple child nodes based on user-defined condition
- Find single child node based on name, user-defined condition

## [**🔧 Helper Function**](bigtree/tree/helper.md)
- Cloning tree to another `Node` type
- Get subtree (smaller tree with different root)
- Prune tree (smaller tree with same root)
- Get difference between two trees

## [**📊 Plotting Tree**](bigtree/utils/plot.md)
- Enhanced Reingold Tilford Algorithm to retrieve (x, y) coordinates for a tree structure

## [**🔨 Exporting Tree**](bigtree/tree/export.md)
- Print to console, in vertical or horizontal orientation
- Export to *Newick string notation*, *dictionary*, *nested dictionary*, or *pandas DataFrame*
- Export tree to *dot* (can save to .dot, .png, .svg, .jpeg files)
- Export tree to *Pillow* (can save to .png, .jpg)
- Export tree to *Mermaid Flowchart* (can display on .md)

## [**✔️ Workflows**](bigtree/workflows/index.md)
- Sample workflows for tree demonstration!

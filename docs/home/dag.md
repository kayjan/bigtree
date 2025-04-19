---
title: Directed Acyclic Graph (DAG)
---

# 🌴 Directed Acyclic Graph (DAG)

For **Directed Acyclic Graph (DAG)** implementation, there are 5 main components.

## [**🌼 Node**](../bigtree/node/dagnode.md)
- ``DAGNode``, extendable class for constructing Directed Acyclic Graph (DAG)

## [**✨ Constructing DAG**](../bigtree/dag/construct.md)
- From *list*, containing parent-child tuples
- From *nested dictionary*
- From *pandas DataFrame*

## [**➰ Traversing DAG**](../bigtree/utils/iterators.md)
- Generic traversal method

## [**➰ Parsing Tree**](../bigtree/dag/parsing.md)
- Get possible paths from one node to another node

## [**🔨 Exporting DAG**](../bigtree/dag/export.md)
- Export to *list*, *dictionary*, or *pandas DataFrame*
- Export DAG to *dot* (can save to .dot, .png, .svg, .jpeg files)

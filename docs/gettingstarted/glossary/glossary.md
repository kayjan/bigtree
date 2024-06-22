---
title: Glossary
---

# ☎️ Glossary

Trees are non-linear data structures that store data hierarchically and are made up of nodes
connected by edges. For example in a family tree, a node would represent a person and an edge
would represent the relationship between two nodes.

## Terminology

After knowing the components that make up a tree, there are a few terminologies
that extend to these components:

### Tree structure

- **Root**: Node that does not have any parent and the entire tree originates from it,
each tree only has one root!
- **Leaf**: Node(s) that do not have any child
- **Height/Max Depth**: Maximum depth of root to a leaf node

![Sample Tree Output](https://github.com/kayjan/bigtree/raw/master/assets/demo/tree.png "Sample tree output")

In the diagram above, the root node is `a` and the leaf nodes are `c`, `d`, and `e`.
The height of the tree is 3.

### Relative tree structure

- **Parent Node**: Immediate predecessor of a node
- **Child Node(s)**: Immediate successor(s) of a node
- **Ancestors**: All predecessors of a node, excluding itself
- **Descendants**: All successors of a node, excluding itself
- **Siblings**: Nodes that have the same parent
- **Left Sibling**: Sibling to the left of the node
- **Right Sibling**: Sibling to the right of the node
- **Depth**: Length of the path from Node to root

## Tree Traversal Algorithms

There are two types of tree traversal, Depth-First Search (DFS) and Breadth-First Search (BFS).

- **Depth-First Search** starts at the root and explores each branch to its leaf node before
moving to the next branch
- **Breadth-First Search** starts at the root and explores every child node, and recursively
does so for every node

### Pre-Order Traversal

Pre-Order Traversal is a Depth-First Search (DFS) method that performs 3 steps recursively,

1. Visit the current node (N)
2. Recursively traversal the current node’s left subtree (L)
3. Recursively traverse the current node’s right subtree (R)

### Post-Order Traversal
Post-Order Traversal is a Depth-First Search (DFS) method that performs 3 steps recursively,

1. Recursively traverse the current node’s left subtree (L)
2. Recursively traverse the current node’s right subtree (R)
3. Visit the current node (N)

### In-Order Traversal

In-Order Traversal is a Depth-First Search (DFS) method that is only applicable to binary trees.

1. Recursively traverse the current node’s left subtree (L)
2. Visit the current node (N)
3. Recursively traverse the current node’s right subtree (R)

### Level-Order Traversal

Level-Order Traversal is a Breadth-First Search method.
In `bigtree`, we have level-order traversal and level-order group traversal methods.

### Zig Zag Traversal

Zig Zag Traversal is similar to level-order traversal, but in a zigzag manner across different levels.
In `bigtree`, we have zig zag traversal and zig zag group traversal methods.

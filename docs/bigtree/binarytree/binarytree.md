---
title: Binary Tree
---

# 🎄 Binary Tree

Conceptually, binary trees are made up of binary nodes, and they are synonymous; a tree is a node. In bigtree
implementation, node refers to the `BinaryNode` class, whereas tree refers to the `BinaryTree` class. BinaryTree is
implemented as a wrapper around a BinaryNode to implement tree-level methods for a more intuitive API.

Construct, export, helper, query, search, and iterator methods encapsulated in BinaryTree class. Binary Tree is a type
of Tree and inherits from Tree, hence all Tree methods are also available in BinaryTree class.

## Binary Tree Construct Methods

| Construct Binary Tree from | Using heapq structure        | Add node attributes |
|----------------------------|------------------------------|---------------------|
| List                       | `BinaryTree.from_heapq_list` | No                  |

## Iterator Methods

| Data Structure | Algorithm      | Description             |
|----------------|----------------|-------------------------|
| Binary Tree    | `inorder_iter` | Depth-First Search, LNR |

-----
::: bigtree.binarytree.binarytree

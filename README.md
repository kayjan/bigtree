# Big Tree Python Package

Tree Implementation and Methods for Python, integrated with Python list, dictionary, and pandas DataFrame.

It is pythonic, making it easy to learn and extendable to many types of workflows.

----

Related Links:
- [Documentation](https://bigtree.readthedocs.io/en/latest/)
- [GitHub](https://github.com/kayjan/bigtree/)
- Community
  - [Issues](https://github.com/kayjan/bigtree/issues)
  / [Discussions](https://github.com/kayjan/bigtree/discussions)
  / [Changelog](https://github.com/kayjan/bigtree/blob/master/CHANGELOG.md)
  / [Contributing](https://bigtree.readthedocs.io/en/latest/contributing/)
- Package
  - [PyPI](https://pypi.org/project/bigtree/)
  / [Conda](https://anaconda.org/conda-forge/bigtree)
- Articles
  - [Python Tree Implementation with BigTree](https://towardsdatascience.com/python-tree-implementation-with-bigtree-13cdabd77adc#245a-94ae81f0b3f1)
  - [The Reingold Tilford Algorithm Explained, with Walkthrough](https://towardsdatascience.com/reingold-tilford-algorithm-explained-with-walkthrough-be5810e8ed93?sk=2db8e10398cee76c486c4b06b0b33322)
- <div><p>If you want to support bigtree, <a href="https://www.buymeacoffee.com/kayjan"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" style="vertical-align:middle"></a></p></div>

-----

## Components
There are 3 segments to Big Tree consisting of Tree, Binary Tree, and Directed Acyclic Graph (DAG) implementation.

For **Tree** implementation, there are 9 main components.

1. [**🌺 Node**](https://bigtree.readthedocs.io/en/latest/node.html)
   1. ``BaseNode``, extendable class
   2. ``Node``, BaseNode with node name attribute
2. [**✨ Constructing Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/construct.html)
   1. From `Node`, using parent and children constructors
   2. From *str*, using tree display or Newick string notation
   3. From *list*, using paths or parent-child tuples
   4. From *nested dictionary*, using path-attribute key-value pairs or recursive structure
   5. From *pandas DataFrame*, using paths or parent-child columns
   6. Add nodes to existing tree using path string
   7. Add nodes and attributes to existing tree using *dictionary* or *pandas DataFrame*, using path
   8. Add only attributes to existing tree using *dictionary* or *pandas DataFrame*, using node name
3. [**➰ Traversing Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/iterators.html)
   1. Pre-Order Traversal
   2. Post-Order Traversal
   3. Level-Order Traversal
   4. Level-Order-Group Traversal
   5. ZigZag Traversal
   6. ZigZag-Group Traversal
4. [**📝 Modifying Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/modify.html)
   1. Copy nodes from location to destination
   2. Shift nodes from location to destination
   3. Shift and replace nodes from location to destination
   4. Copy nodes from one tree to another
   5. Copy and replace nodes from one tree to another
5. [**🔍 Tree Search**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/search.html)
   1. Find multiple nodes based on name, partial path, relative path, attribute value, user-defined condition
   2. Find single nodes based on name, partial path, relative path, full path, attribute value, user-defined condition
   3. Find multiple child nodes based on user-defined condition
   4. Find single child node based on name, user-defined condition
6. [**🔧 Helper Function**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/helper.html)
   1. Cloning tree to another `Node` type
   2. Get subtree (smaller tree with different root)
   3. Prune tree (smaller tree with same root)
   4. Get difference between two trees
7. [**📊 Plotting Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/plot.html)
   1. Enhanced Reingold Tilford Algorithm to retrieve (x, y) coordinates for a tree structure
8. [**🔨 Exporting Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/tree/export.html)
   1. Print to console, in vertical or horizontal orientation
   2. Export to *Newick string notation*, *dictionary*, *nested dictionary*, or *pandas DataFrame*
   3. Export tree to *dot* (can save to .dot, .png, .svg, .jpeg files)
   4. Export tree to *Pillow* (can save to .png, .jpg)
   5. Export tree to *Mermaid Flowchart* (can display on .md)
9. [**✔️ Workflows**](https://bigtree.readthedocs.io/en/latest/workflows.html)
   1. Sample workflows for tree demonstration!

--------

For **Binary Tree** implementation, there are 3 main components.
Binary Node inherits from Node, so the components in Tree implementation are also available in Binary Tree.

1. [**🌿 Node**](https://bigtree.readthedocs.io/en/latest/node.html)
   1. ``BinaryNode``, Node with binary tree rules
2. [**✨ Constructing Binary Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/binarytree/construct.html)
   1. From *list*, using flattened list structure
3. [**➰ Traversing Binary Tree**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/iterators.html)
   1. In-Order Traversal

-----

For **Directed Acyclic Graph (DAG)** implementation, there are 4 main components.

1. [**🌼 Node**](https://bigtree.readthedocs.io/en/latest/node.html)
   1. ``DAGNode``, extendable class for constructing Directed Acyclic Graph (DAG)
2. [**✨ Constructing DAG**](https://bigtree.readthedocs.io/en/latest/bigtree/dag/construct.html)
   1. From *list*, containing parent-child tuples
   2. From *nested dictionary*
   3. From *pandas DataFrame*
3. [**➰ Traversing DAG**](https://bigtree.readthedocs.io/en/latest/bigtree/utils/iterators.html)
   1. Generic traversal method
4. [**🔨 Exporting DAG**](https://bigtree.readthedocs.io/en/latest/bigtree/dag/export.html)
   1. Export to *list*, *dictionary*, or *pandas DataFrame*
   2. Export DAG to *dot* (can save to .dot, .png, .svg, .jpeg files)

-----

## Installation

There are two ways to install `bigtree`, with pip (recommended) or conda.

### a) Installation with pip

To install `bigtree`, run the following line in command prompt:

```console
$ pip install bigtree
```

If tree needs to use pandas methods, it requires additional dependencies.
Run the following line in command prompt:

```console
$ pip install 'bigtree[pandas]'
```

If tree needs to be exported to image, it requires additional dependencies.
Run the following lines in command prompt:

```console
$ pip install 'bigtree[image]'
$ brew install gprof2dot  # for MacOS
$ conda install graphviz  # for Windows
```

Alternatively, install all optional dependencies with the following line in command prompt:

```console
$ pip install 'bigtree[all]'
```

### b) Installation with conda

To install `bigtree` with conda, run the following line in command prompt:

```console
$ conda install -c conda-forge bigtree
```

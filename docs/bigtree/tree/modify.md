---
title: Tree Modify
---

# 📝 Modify

## Merging trees modification

There are two types of merging available

1. Merge all nodes of multiple trees together
   - The root node name of the trees can be different, resulting tree will take the root name of the first tree
   - Attributes are also merged, if there are clashes in attributes, it will take the attribute of the latter tree
2. Create a tree with only branches provided (`exact=True`)
   - The root node name of the tree must be the same
   - Attributes, if any, exist only for the branches provided. Intermediate node(s) will be created, but without attributes

## Shifting and copying node modification

There are two types of modification available

1. **Non-replacing scenario**: Shift or copy nodes within same tree or between two trees using `from_paths` (list of paths) and `to_paths` (list of paths)
2. **Replacing scenario**: Shift or copy nodes within same tree or between two trees *while replacing the to-node* using `from_paths` (list of paths) and `to_paths` (list of paths)

## Available Configurations for Customisation

In **non-replacing scenario**, there are several configurations available for customisation.

| Configuration     | Description                                                                            | Default Value                                             |
|-------------------|----------------------------------------------------------------------------------------|-----------------------------------------------------------|
| `copy`            | Indicates whether it is to shift the nodes, or copy the nodes                          | False (nodes are shifted, not copied)                     |
| `to_tree`         | Indicates whether shifting/copying is within the same tree, or between different trees | None (nodes are shifted/copied within the same tree)      |
| `skippable`       | Skip shifting/copying of nodes if from_path cannot be found                            | False (from-node must be found)                           |
| `overriding`      | Override existing node if it exists                                                    | False (to-node must not exist)                            |
| `merge_attribute` | Merge attributes of existing node if it exists                                         | False (to-node must not exist, attributes are not merged) |
| `merge_children`  | Shift/copy children of from-node and remove intermediate parent node                   | False (children are not merged)                           |
| `merge_leaves`    | Shift/copy leaves of from-node and remove all intermediate nodes                       | False (leaves are not merged)                             |
| `delete_children` | Shift/copy node only and delete its children                                           | False (nodes are shifted/copied together with children)   |

In **replacing scenario**, all the configurations are also available except `overriding`, `merge_attribute`,
`merge_children`, and `merge_leaves` as it is doing a one-to-one replacement. It is by default overriding, and there is
nothing to merge.

!!! note

    `overriding` and `merge_attribute` cannot be simultaneously set to `True`. One deals with clashing nodes by
    overriding, another deals with it by merging attributes of both nodes.

!!! note

    `merge_children` and `merge_leaves` cannot be simultaneously set to `True`.

!!! note

    Error will always be thrown if multiple from-nodes are found, paths in `from_paths` must be unique.

## Tree Modification Permutations

There are several ways you can mix and match the tree modification methods. If you know all the parameters to choose,
feel free to use ``copy_or_shift_logic`` or ``replace_logic`` methods as they are the most customizable. All other
methods call these 2 methods directly.

| Shift / Copy? | Same tree / Between two trees? | Replace destination node? | Method to use                                |
|---------------|--------------------------------|---------------------------|----------------------------------------------|
| Shift         | Same tree                      | No                        | ``shift_nodes``                              |
| Copy          | Same tree                      | No                        | ``copy_nodes``                               |
| Copy          | Between two trees              | No                        | ``copy_nodes_from_tree_to_tree``             |
| Any           | Any                            | No                        | ``copy_or_shift_logic``                      |
| Shift         | Same tree                      | Yes                       | ``shift_and_replace_nodes``                  |
| Copy          | Between two trees              | Yes                       | ``copy_and_replace_nodes_from_tree_to_tree`` |
| Any           | Any                            | Yes                       | ``replace_logic``                            |

## Tree Modification Illustration

### Shift, Copy, Delete

![Shift and Copy Example](https://github.com/kayjan/bigtree/raw/master/assets/docs/modify_shift_and_copy.png "Shift and Copy Example")

<details>
<summary>Click to expand code</summary>

```python hl_lines="18 27"
from bigtree import Node
from bigtree.tree import modify

tree = Node(
    "a",
    colour="yellow",
    children=[
        Node("b", colour="yellow"),
        Node("c", colour="red"),
        Node("d", colour="blue"),
        Node("e"),
    ],
)
tree.show(rich=True, node_format_attr="colour")

# Shift
tree_shift = tree.copy()
modify.shift_nodes(
    tree_shift,
    from_paths=["a/c", "a/d", "a/e"],
    to_paths=["a/b/c", "a/f/d", None],
)
tree_shift.show(rich=True, node_format_attr="colour")

# Copy
tree_copy = tree.copy()
modify.copy_nodes(
    tree_copy,
    from_paths=["a/c"],
    to_paths=["a/b/c"],
)
tree_copy.show(rich=True, node_format_attr="colour")
```
</details>

| Setting   | Sample path in `from_paths` | Sample path in `to_paths` | Description                                         |
|-----------|-----------------------------|---------------------------|-----------------------------------------------------|
| Default   | "/a/c"                      | "/a/b/c"                  | Shift/copy node `c`                                 |
| Default   | "/c"                        | "/a/b/c"                  | Shift/copy node `c`                                 |
| Default   | "c"                         | "/a/b/c"                  | Shift/copy node `c`                                 |
| Default   | "/a/e"                      | None                      | Delete node `e`                                     |
| skippable | "/a/c"                      | "/a/b/c"                  | Shift/copy node `c`, skip if "/a/c" cannot be found |

---

### Advanced

![Advanced Shift Example](https://github.com/kayjan/bigtree/raw/master/assets/docs/modify_advanced.png "Advanced Shift Example")

<details>
<summary>Click to expand code</summary>

```python hl_lines="23 32 41 50"
from bigtree import Tree
from bigtree.tree import modify

tree = Tree.from_dict(
    {
        "a": dict(colour="yellow"),
        "a/b": dict(colour="yellow"),
        "a/b/c": dict(colour="red"),
        "a/b/c/e": dict(colour="red"),
        "a/d": dict(colour="blue"),
        "a/d/c": dict(colour="blue"),
        "a/d/c/f": dict(colour="blue"),
        "a/d/g": dict(colour="blue"),
    }
)
tree.show(rich=True, node_format_attr="colour")

# Overriding
tree_overriding = tree.copy()
tree_overriding.shift_nodes(
    from_paths=["a/b/c"],
    to_paths=["a/d/c"],
    overriding=True,
)
tree_overriding.show(rich=True, node_format_attr="colour")

# Merge children
tree_merge_children = tree.copy()
tree_merge_children.shift_nodes(
    from_paths=["a/b/c"],
    to_paths=["a/d/c"],
    merge_children=True,
)
tree_merge_children.show(rich=True, node_format_attr="colour")

# Merge leaves
tree_merge_leaves = tree.copy()
tree_merge_leaves.shift_nodes(
    from_paths=["a/b/c"],
    to_paths=["a/d/c"],
    merge_leaves=True,
)
tree_merge_leaves.show(rich=True, node_format_attr="colour")

# Delete children
tree_delete_children = tree.copy()
tree_delete_children.shift_nodes(
    from_paths=["a/b"],
    to_paths=["a/d/b"],
    delete_children=True,
)
tree_delete_children.show(rich=True, node_format_attr="colour")
```
</details>

| Setting                                     | Sample path in `from_paths` | Sample path in `to_paths` | Description                                                                                                                                                                                                |
|---------------------------------------------|-----------------------------|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| overriding                                  | "a/b/c"                     | "a/d/c"                   | Shift/copy node `c`, override if "a/d/c" exists                                                                                                                                                            |
| merge_children                              | "a/b/c"                     | "a/d/c"                   | **If path not present**: Shift/copy children of node `c` to be children of node `d`, removing node `c`<br>**If path present**: Shift/copy children of node `c` to be merged with existing "a/d/c" children |
| merge_children + overriding/merge_attribute | "a/b/c"                     | "a/d/c"                   | **If path not present**: Behaves like merge_children<br>**If path present**: Behaves like overriding/merge_attribute                                                                                       |
| merge_leaves                                | "a/b/c"                     | "a/d/c"                   | **If path not present**: Shift/copy leaves of node `c` to be children of node `d`<br>**If path present**: Shift/copy leaves of node `c` to be merged with existing "a/d/c" children                        |
| merge_leaves + overriding/merge_attribute   | "a/b/c"                     | "a/d/c"                   | **If path not present**: Behaves like merge_leaves<br>**If path present**: Behaves like overriding/merge_attribute, but original node `c` remains                                                          |
| delete_children                             | "a/b"                       | "a/d/b"                   | Shift/copy node `b` only without any node `b` children                                                                                                                                                     |

## Guideline

If you're still feeling lost over the parameters, here are some guiding questions to ask yourself.

- Do I want to retain the original node where they are?
  - Yes: Set `copy=True`
  - Default performs a shift instead of copy
- Am I unsure of what nodes I am going to copy/shift, they may or may not exist and this is perfectly fine?
  - Yes: Set `skippable=True`
  - Default throws error if origin node is not found
- The origin node (and its descendants) may clash with the destination node(s), how do I want to handle it?
  - Set `overriding=True` to overwrite origin node
  - Set `merge_attribute=True` to combine both nodes' attributes
  - Default throws error about the clash in node name
- I want to copy/shift everything under the node, but not the node itself
  - Set `merge_children=True` or `merge_leaves=True` to shift the children and leaf nodes respectively
  - Default shifts the node itself, and everything under it
- I want to copy/shift the node and only the node, and not everything under it
  - Yes: Set `delete_children=True`
  - Default shifts the node itself, and everything under it
- I want to copy/shift things from one tree to another tree
  - Specify `to_tree`
  - Default shifts nodes within the same tree

What about the permutations between the parameters?

- These parameters are standalone and do not produce any interaction effect
  - `copy`, `skippable`, `delete_children`
- These parameters have some interaction:
  - `overriding` and `merge_attribute` with `merge_children` and `merge_leaves`
  - `overriding` + `merge_children`: Behaves like `merge_children` when there is no clash in node name, otherwise behaves like `overriding`
  Note that clashes will preserve origin node parent and destination nodes' children
  - `overriding` + `merge_leaves`: Behaves like `merge_leaves` when there is no clash in node name, otherwise behaves like `overriding`
  Note that clashes will preserve origin node parent and destination nodes' leaves
  - `merge_attribute` + `merge_children`: Behaves like `merge_children` when there is no clash in node name, otherwise behaves like `merge_attribute`
  Note that attributes will be merged for node and all descendants, and will preserve origin and destination nodes' children
  - `merge_attribute` + `merge_leaves`: Behaves like `merge_leaves` when there is no clash in node name, otherwise behaves like `merge_attribute`
  Note that attributes will be merged for node and all descendants, and will preserve origin nodes' children and destination nodes' leaves

-----

::: bigtree.tree.modify

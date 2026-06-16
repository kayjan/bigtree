---
title: Tree Studio Demonstration
---

# 🎬 Tree Studio Demonstration

Construct, modify, search, export tree with a Terminal interface!

![Tree Studio Sample](https://github.com/kayjan/bigtree/raw/master/assets/docs/studio.png "Tree Studio Sample")

!!! note

    Available from version 1.5.0 onwards, requires `pip install 'bigtree[studio]'`


## Launching Studio

Start the terminal interface with:

```bash
bigtree-studio
```

To open an existing tree:

```bash
bigtree-studio tree.json
```

To limit the initial tree depth:

```bash
bigtree-studio --depth 3 tree.json
```

For the full list of available options:

```bash
bigtree-studio --help
```

## Basic Interactions

- **Single click** a node to view its attributes
- **Double click** or press **Space** to expand or collapse a node
- Use the **arrow keys** to navigate the tree

## Keyboard shortcuts

| Key | Action                        |
|-----|-------------------------------|
| `a` | Add child node                |
| `A` | Add sibling node              |
| `d` | Delete selected node          |
| `r` | Rename selected node          |
| `t` | Edit node attributes          |
| `/` | Search nodes                  |
| `n` | Next search result            |
| `N` | Previous search result        |
| `e` | Expand/collapse selected node |
| `E` | Expand all nodes              |
| `z` | Collapse all nodes            |
| `S` | Save As (json file)           |
| `q` | Quit Studio                   |

!!! tip

    Most actions operate on the currently selected node

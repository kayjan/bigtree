# Trees with Custom Coordinates

> Topic: export

Trees can be plotted with `root.plot()` for a simple matplotlib. For more sophisticated plots, it is recommended to
export the tree to dot (supports pydot, graphviz), mermaid, or pillow. To set your own x- and y- coordinates, this
utilises and builds on top of the existing pydot package.

There are 3 ways to get the x- and y- coordinates for each node

1. Use [reingold tilford](../bigtree/utils/plot.md#bigtree.utils.plot.reingold_tilford) function (fastest and easiest)
2. Modify from the Reingold Tilford algorithm from (1)
3. Use your custom coordinates

Using these x- and y- coordinates, we can display it on a pydot plot using the `pos` node attribute. In the example
below, we will make use of option (2) to generate our tree plot with custom coordinates.

```python hl_lines="25"
from bigtree import Node, clone_tree, list_to_tree, reingold_tilford, tree_to_dot

# Create tree
root = list_to_tree(["a/b/d", "a/c"])

# Modify from the Reingold Tilford algorithm
reingold_tilford(root)


class CoordinateNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.y = 2 * self.y  # example


root_coordinate = clone_tree(root, CoordinateNode)


# Export tree to dot (pydot)
def node_pos(_node):
    return {"pos": f"{_node.x},{_node.y}!"}


graph = tree_to_dot(root_coordinate, node_attr=node_pos)
graph.write_png("assets/docs/coordinate_tree.png", prog="neato")
```

![Custom Coordinate Tree Output](https://github.com/kayjan/bigtree/raw/master/assets/docs/coordinate_tree.png "Custom Coordinate Tree Output")

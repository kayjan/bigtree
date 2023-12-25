# Trees with Weighted Edges

Edge weights should be defined in the child node for the parent-child edge since each node can only have one parent.

We can simply add `weight` attribute to the `Node` class.
However, if we want to visualize the weighted tree, we can create a `WeightedNode` class to generate the edge attribute dictionary.

```python
from bigtree import Node, tree_to_dot

class WeightedNode(Node):
    def __init__(self, name, weight=0, **kwargs):
        super().__init__(name, **kwargs)
        self.weight = weight

    @property
    def edge_attr(self):
        return {"label": self.weight}

# Construct weighted tree
root = WeightedNode("a")
b = WeightedNode("b", parent=root, weight=1)
c = WeightedNode("c", parent=root, weight=2)
d = WeightedNode("d", parent=b, weight=3)

graph = tree_to_dot(root, node_colour="gold", edge_attr="edge_attr")
graph.write_png("assets/sphinx/weighted_tree.png")
```

![Sample DAG Output](https://github.com/kayjan/bigtree/raw/master/assets/sphinx/weighted_tree.png)

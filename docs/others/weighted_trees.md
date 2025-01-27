# Trees with Weighted Edges

> Topic: export

Edge weights should be defined in the child node for the parent-child edge since each node can only have one parent.

We can simply add `weight` attribute to the `Node` class.
However, if we want to visualize the weighted tree, we can create a `WeightedNode` class to generate the edge attribute dictionary.

```python hl_lines="8-13"
from bigtree import Node, tree_to_dot

class WeightedNode(Node):
    def __init__(self, name, weight=0, **kwargs):
        super().__init__(name, **kwargs)
        self.weight = weight

    @property
    def edge_attr(self):
        """Edge attribute for pydot diagram
        Label for edge label, penwidth for edge width
        """
        return {"label": self.weight, "penwidth": self.weight}

# Construct weighted tree
root = WeightedNode("a")
b = WeightedNode("b", parent=root, weight=1)
c = WeightedNode("c", parent=root, weight=2)
d = WeightedNode("d", parent=b, weight=3)

graph = tree_to_dot(root, node_colour="gold", edge_attr="edge_attr")
graph.write_png("assets/docs/weighted_tree.png")
```

![Weighted Tree Output](https://github.com/kayjan/bigtree/raw/master/assets/docs/weighted_tree.png "Weighted Tree Output")

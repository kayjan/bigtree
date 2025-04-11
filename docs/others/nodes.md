# Extending Nodes

Nodes can be extended from `BaseNode` or `Node` class to have extended functionalities or add pre-/post-assign checks.

 - For example, `Node` class extends `BaseNode` and added the ``name`` functionality with pre-assign checks to ensure no duplicate path names

## Population Node (add functionality/method/property)

```python hl_lines="10-20"
from bigtree import Node, print_tree


class PopulationNode(Node):

    def __init__(self, name: str, population: int = 0, **kwargs):
        super().__init__(name, **kwargs)
        self._population = population

    @property
    def population(self):
        if self.is_leaf:
            return self._population
        return sum([child.population for child in self.children])

    @property
    def percentage(self):
        if self.is_root:
            return 1
        return round(self.population / self.root.population, 2)


root = PopulationNode("World")
b1 = PopulationNode("Country A", parent=root)
c1 = PopulationNode("State A1", 100, parent=b1)
c2 = PopulationNode("State A2", 50, parent=b1)
b2 = PopulationNode("Country B", 200, parent=root)
b3 = PopulationNode("Country C", 100, parent=root)

print_tree(root, attr_list=["population", "percentage"])
# World [population=450, percentage=1]
# ├── Country A [population=150, percentage=0.33]
# │   ├── State A1 [population=100, percentage=0.22]
# │   └── State A2 [population=50, percentage=0.11]
# ├── Country B [population=200, percentage=0.44]
# └── Country C [population=100, percentage=0.22]
```

## Read-Only Node (add pre-/post-assign checks)

```python hl_lines="14-20"
import pytest

from bigtree import Node
from typing import List


class ReadOnlyNode(Node):

    def __init__(self, *args, **kwargs):
        self.__readonly = False
        super().__init__(*args, **kwargs)
        self.__readonly = True

    def _Node__pre_assign_parent(self, new_parent: Node):
        if self.__readonly:
            raise RuntimeError("Nodes cannot be reassigned for ReadOnlyNode")

    def _Node__pre_assign_children(self, new_children: List[Node]):
        if self.__readonly:
            raise RuntimeError("Nodes cannot be reassigned for ReadOnlyNode")


a = ReadOnlyNode("a")
b = ReadOnlyNode("b", parent=a)
c = ReadOnlyNode("c", parent=a)

with pytest.raises(RuntimeError):
    c.parent = b

with pytest.raises(RuntimeError):
    a.children = [b, c]
```

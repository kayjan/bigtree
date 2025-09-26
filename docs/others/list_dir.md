# List Directory

> Topic: construct

To list directories recursively using bigtree, we can use the `glob` built-in Python package to extract a list of paths.

```python
import glob
from bigtree import Tree

# Get all directories recursively
path_list = []
for f in glob.glob("./**/*.py", recursive=True):
    path_list.append(f)

# Construct tree
tree = Tree.from_list(path_list)

# View tree
tree.show(max_depth=3)
```

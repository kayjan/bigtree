# List Directory

To list directories recursively using bigtree, we can use the `glob` built-in Python package to extract a list of paths.

```python
import glob
from bigtree import list_to_tree, print_tree

# Get all directories recursively
path_list = []
for f in glob.glob("./**/*.py", recursive=True):
    path_list.append(f)

# Construct tree
root = list_to_tree(path_list)

# View tree
print_tree(root, max_depth=3)
```

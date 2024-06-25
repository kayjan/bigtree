---
title: Playground
hide:
  - navigation
  - toc
---

# 🎡️ Playground

```py play
from bigtree import dict_to_tree

path_dict = {
   "a": {"age": 90},
   "a/b": {"age": 65},
   "a/c": {"age": 60},
   "a/b/d": {"age": 40},
}
root = dict_to_tree(path_dict)
root.show()
```

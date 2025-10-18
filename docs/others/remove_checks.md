# Remove Tree Checks

!!! note

    Available from version 0.16.2 onwards

When constructing trees, there are a few checks done in BaseNode class that slow down performance.
This slowness will be more apparent with very large trees. The checks are to

- Check parent/children data type
- Check for loops (expensive for trees that are deep as it checks the ancestors of node)

!!! note

    Available from version 1.0.1 onwards

The further checks are removed from Node class.

- Check for empty node name
- Check for duplicated paths (expensive for trees that are wide as it checks the siblings of node)

These checks are enabled by default. To turn off these checks, you can set environment variable before importing `bigtree`.

```python
import os
os.environ["BIGTREE_CONF_ASSERTIONS"] = ""

import bigtree
```

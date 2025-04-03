from typing import Any, Optional, TypeVar

from bigtree.node import basenode
from bigtree.utils import exceptions, iterators

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    plt = MagicMock()


__all__ = [
    "reingold_tilford",
    "plot_tree",
]

T = TypeVar("T", bound=basenode.BaseNode)


def reingold_tilford(
    tree_node: T,
    sibling_separation: float = 1.0,
    subtree_separation: float = 1.0,
    level_separation: float = 1.0,
    x_offset: float = 0.0,
    y_offset: float = 0.0,
    reverse: bool = False,
) -> None:
    """
    Algorithm for drawing tree structure, retrieves `(x, y)` coordinates for a tree structure. Adds `x` and `y`
    attributes to every node in the tree. Modifies tree in-place.

    This algorithm[1] is an improvement over Reingold Tilford algorithm[2].

    According to Reingold Tilford's paper, a tree diagram should satisfy the following aesthetic rules,

    1. Nodes at the same depth should lie along a straight line, and the straight lines defining the depths should be
    parallel
    2. A left child should be positioned to the left of its parent node and a right child to the right
    3. A parent should be centered over their children
    4. A tree and its mirror image should produce drawings that are reflections of one another; a subtree should be
    drawn the same way regardless of where it occurs in the tree

    Examples:
        >>> from bigtree import reingold_tilford, list_to_tree
        >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
        >>> root = list_to_tree(path_list)
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f

        >>> reingold_tilford(root)
        >>> root.show(attr_list=["x", "y"])
        a [x=1.25, y=3.0]
        ├── b [x=0.5, y=2.0]
        │   ├── d [x=0.0, y=1.0]
        │   └── e [x=1.0, y=1.0]
        │       ├── g [x=0.5, y=0.0]
        │       └── h [x=1.5, y=0.0]
        └── c [x=2.0, y=2.0]
            └── f [x=2.0, y=1.0]

    References

    - [1] Walker, J. (1991). Positioning Nodes for General Trees. https://www.drdobbs.com/positioning-nodes-for-general-trees/184402320?pgno=4
    - [2] Reingold, E., Tilford, J. (1981). Tidier Drawings of Trees. IEEE Transactions on Software Engineering. https://reingold.co/tidier-drawings.pdf

    Args:
        tree_node: tree to compute (x, y) coordinate
        sibling_separation: minimum distance between adjacent siblings of the tree
        subtree_separation: minimum distance between adjacent subtrees of the tree
        level_separation: fixed distance between adjacent levels of the tree
        x_offset: graph offset of x-coordinates
        y_offset: graph offset of y-coordinates
        reverse: graph begins bottom to top by default, set to True for top to bottom y coordinates
    """
    _first_pass(tree_node, sibling_separation, subtree_separation)
    x_adjustment = _second_pass(
        tree_node, level_separation, x_offset, y_offset, reverse
    )
    _third_pass(tree_node, x_adjustment)


@exceptions.optional_dependencies_matplotlib
def plot_tree(
    tree_node: T, *args: Any, ax: Optional[plt.Axes] = None, **kwargs: Any
) -> plt.Figure:
    """Plot tree in line form. Tree should have `x` and `y` attribute from Reingold Tilford. Accepts existing
    matplotlib Axes. Accepts args and kwargs for matplotlib.pyplot.plot() function.

    Examples:
        >>> import matplotlib.pyplot as plt
        >>> from bigtree import list_to_tree, plot_tree, reingold_tilford
        >>> path_list = ["a/b/d", "a/b/e/g", "a/b/e/h", "a/c/f"]
        >>> root = list_to_tree(path_list)
        >>> reingold_tilford(root)
        >>> plot_tree(root, "-ok")
        <Figure size 1280x960 with 1 Axes>

    Args:
        tree_node: tree to plot
        ax: axes to add Figure to
    """
    if ax:
        fig = ax.get_figure()
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    for node in iterators.preorder_iter(tree_node):
        if not node.is_root:
            try:
                ax.plot(
                    [node.x, node.parent.x],  # type: ignore
                    [node.y, node.parent.y],  # type: ignore
                    *args,
                    **kwargs,
                )
            except AttributeError:
                raise RuntimeError(
                    "No x or y coordinates detected. "
                    "Please run reingold_tilford algorithm to retrieve coordinates."
                )
    return fig


def _first_pass(
    tree_node: T, sibling_separation: float, subtree_separation: float
) -> None:
    """
    Performs post-order traversal of tree and assigns `x`, `mod` and `shift` values to each node. Modifies tree in-place.

    Notation:
      - `lsibling`: left-sibling of node
      - `lchild`: last child of node
      - `fchild`: first child of node
      - `midpoint`: midpoint of node wrt children, :math:`midpoint = (lchild.x + fchild.x) / 2`
      - `sibling distance`: sibling separation
      - `subtree distance`: subtree separation

    There are two parts in the first pass,

    1. In the first part, we assign `x` and `mod` values to each node

      `x` value is the initial x-position of each node purely based on the node's position
        - :math:`x = 0` for leftmost node and :math:`x = lsibling.x + sibling distance` for other nodes
        - Special case when leftmost node has children, then it will try to center itself, :math:`x = midpoint`

      `mod` value is the amount to shift the subtree (all descendant nodes excluding itself) to make the children
      centered with itself
        - :math:`mod = 0` for node does not have children (no need to shift subtree) or it is a leftmost node (parent
        is already centered, from above point)
        - Special case when non-leftmost nodes have children, :math:`mod = x - midpoint`

    2. In the second part, we assign `shift` value of nodes due to overlapping subtrees

      For each node on the same level, ensure that the leftmost descendant does not intersect with the rightmost
      descendant of any left sibling at every subsequent level. Intersection happens when the subtrees are not
      at least `subtree distance` apart.

      If there are any intersections, shift the whole subtree by a new `shift` value, shift any left sibling by a
      fraction of `shift` value, and shift any right sibling by `shift` + a multiple of the fraction of
      `shift` value to keep nodes centralized at the level.

    Args:
        tree_node: tree to compute (x, y) coordinate
        sibling_separation: minimum distance between adjacent siblings of the tree
        subtree_separation: minimum distance between adjacent subtrees of the tree
    """
    # Post-order iteration (LRN)
    for child in tree_node.children:
        _first_pass(child, sibling_separation, subtree_separation)

    _x = 0.0
    _mod = 0.0
    _shift = 0.0
    _midpoint = 0.0

    if tree_node.is_root:
        tree_node.set_attrs({"x": _get_midpoint_of_children(tree_node)})
        tree_node.set_attrs({"mod": _mod})
        tree_node.set_attrs({"shift": _shift})

    else:
        # First part - assign x and mod values

        if tree_node.children:
            _midpoint = _get_midpoint_of_children(tree_node)

        # Non-leftmost node
        if tree_node.left_sibling:
            _x = tree_node.left_sibling.get_attr("x") + sibling_separation
            if tree_node.children:
                _mod = _x - _midpoint
        # Leftmost node
        else:
            if tree_node.children:
                _x = _midpoint

        tree_node.set_attrs({"x": _x})
        tree_node.set_attrs({"mod": _mod})
        tree_node.set_attrs({"shift": tree_node.get_attr("shift", _shift)})

        # Second part - assign shift values due to overlapping subtrees

        parent_node = tree_node.parent
        tree_node_idx = parent_node.children.index(tree_node)
        if tree_node_idx:
            for idx_node in range(tree_node_idx):
                left_subtree = parent_node.children[idx_node]
                _shift = max(
                    _shift,
                    _get_subtree_shift(
                        left_subtree=left_subtree,
                        right_subtree=tree_node,
                        left_idx=idx_node,
                        right_idx=tree_node_idx,
                        subtree_separation=subtree_separation,
                    ),
                )

            # Shift siblings (left siblings, itself, right siblings) accordingly
            for multiple, sibling in enumerate(parent_node.children):
                sibling.set_attrs(
                    {
                        "shift": sibling.get_attr("shift", 0)
                        + (_shift * multiple / tree_node_idx)
                    }
                )


def _get_midpoint_of_children(tree_node: basenode.BaseNode) -> float:
    """Get midpoint of children of a node.

    Args:
        tree_node: tree node to obtain midpoint of their child/children

    Returns:
        Midpoint of children
    """
    if tree_node.children:
        first_child_x: float = tree_node.children[0].get_attr("x") + tree_node.children[
            0
        ].get_attr("shift")
        last_child_x: float = tree_node.children[-1].get_attr("x") + tree_node.children[
            -1
        ].get_attr("shift")
        return (last_child_x + first_child_x) / 2
    return 0.0


def _get_subtree_shift(
    left_subtree: T,
    right_subtree: T,
    left_idx: int,
    right_idx: int,
    subtree_separation: float,
    left_cum_shift: float = 0,
    right_cum_shift: float = 0,
    cum_shift: float = 0,
    initial_run: bool = True,
) -> float:
    """Get shift amount to shift the right subtree towards the right such that it does not overlap with the left subtree.

    Args:
        left_subtree: left subtree, with right contour to be traversed
        right_subtree (BaseNode): right subtree, with left contour to be traversed
        left_idx: index of left subtree, to compute overlap for relative shift (constant across iteration)
        right_idx: index of right subtree, to compute overlap for relative shift (constant across iteration)
        subtree_separation: minimum distance between adjacent subtrees of the tree (constant across iteration)
        left_cum_shift: cumulative `mod + shift` for left subtree from the ancestors
        right_cum_shift: cumulative `mod + shift` for right subtree from the ancestors
        cum_shift: cumulative shift amount for right subtree
        initial_run: indicates whether left_subtree and right_subtree are the main subtrees

    Returns:
        Amount to shift subtree
    """
    new_shift = 0.0

    if not initial_run:
        x_left = (
            left_subtree.get_attr("x") + left_subtree.get_attr("shift") + left_cum_shift
        )
        x_right = (
            right_subtree.get_attr("x")
            + right_subtree.get_attr("shift")
            + right_cum_shift
            + cum_shift
        )
        new_shift = max(
            (x_left + subtree_separation - x_right) / (1 - left_idx / right_idx), 0
        )

        # Search for a left sibling of left_subtree that has children
        while left_subtree and not left_subtree.children and left_subtree.left_sibling:
            left_subtree = left_subtree.left_sibling

        # Search for a right sibling of right_subtree that has children
        while (
            right_subtree and not right_subtree.children and right_subtree.right_sibling
        ):
            right_subtree = right_subtree.right_sibling

    if left_subtree.children and right_subtree.children:
        # Iterate down the level, for the rightmost child of left_subtree and the leftmost child of right_subtree
        return _get_subtree_shift(
            left_subtree=left_subtree.children[-1],
            right_subtree=right_subtree.children[0],
            left_idx=left_idx,
            right_idx=right_idx,
            subtree_separation=subtree_separation,
            left_cum_shift=(
                left_cum_shift
                + left_subtree.get_attr("mod")
                + left_subtree.get_attr("shift")
            ),
            right_cum_shift=(
                right_cum_shift
                + right_subtree.get_attr("mod")
                + right_subtree.get_attr("shift")
            ),
            cum_shift=cum_shift + new_shift,
            initial_run=False,
        )

    return cum_shift + new_shift


def _second_pass(
    tree_node: T,
    level_separation: float,
    x_offset: float,
    y_offset: float,
    reverse: bool,
    cum_mod: Optional[float] = 0.0,
    max_depth: Optional[int] = None,
    x_adjustment: Optional[float] = 0.0,
) -> float:
    """
    Performs pre-order traversal of tree and determines the final `x` and `y` values for each node. Modifies tree in-place.

    Notation:
      - `depth`: maximum depth of tree
      - `distance`: level separation
      - `x'`: x offset
      - `y'`: y offset

    Final position of each node
      - :math:`x = node.x + node.shift + sum(ancestor.mod) + x'`
      - :math:`y = (depth - node.depth) * distance + y'`

    Args:
        tree_node: tree to compute (x, y) coordinate
        level_separation: fixed distance between adjacent levels of the tree (constant across iteration)
        x_offset: graph offset of x-coordinates (constant across iteration)
        y_offset: graph offset of y-coordinates (constant across iteration)
        reverse: graph begins bottom to top by default, set to True for top to bottom y coordinates
        cum_mod: cumulative `mod + shift` for tree/subtree from the ancestors
        max_depth: maximum depth of tree (constant across iteration)
        x_adjustment: amount of x-adjustment for third pass, in case any x-coordinates goes below 0

    Returns
        Amount to shift the node by
    """
    if not max_depth:
        max_depth = tree_node.max_depth

    final_x: float = (
        tree_node.get_attr("x") + tree_node.get_attr("shift") + cum_mod + x_offset
    )
    if reverse:
        final_y: float = (tree_node.depth - 1) * level_separation + y_offset
    else:
        final_y = (max_depth - tree_node.depth) * level_separation + y_offset
    tree_node.set_attrs({"x": final_x, "y": final_y})

    # Pre-order iteration (NLR)
    if tree_node.children:
        return max(
            [
                _second_pass(
                    child,
                    level_separation,
                    x_offset,
                    y_offset,
                    reverse,
                    cum_mod + tree_node.get_attr("mod") + tree_node.get_attr("shift"),
                    max_depth,
                    x_adjustment,
                )
                for child in tree_node.children
            ]
        )
    return max(x_adjustment, -final_x)


def _third_pass(tree_node: basenode.BaseNode, x_adjustment: float) -> None:
    """Adjust all x-coordinates by an adjustment value so that every x-coordinate is greater than or equal to 0. Modifies
    tree in-place.

    Args:
        tree_node: tree to compute (x, y) coordinate
        x_adjustment: amount of adjustment for x-coordinates (constant across iteration)
    """
    if x_adjustment:
        tree_node.set_attrs({"x": tree_node.get_attr("x") + x_adjustment})

        # Pre-order iteration (NLR)
        for child in tree_node.children:
            _third_pass(child, x_adjustment)

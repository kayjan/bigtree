from typing import Optional, TypeVar

from bigtree.node.basenode import BaseNode

T = TypeVar("T", bound=BaseNode)

__all__ = [
    "reingold_tilford",
]


def reingold_tilford(
    tree_node: T,
    sibling_separation: float = 1.0,
    subtree_separation: float = 1.0,
    level_separation: float = 1.0,
    x_offset: float = 0.0,
    y_offset: float = 0.0,
) -> None:
    """
    Algorithm for drawing tree structure, retrieves `(x, y)` coordinates for a tree structure.
    Modifies tree in-place.

    This algorithm[1] is an improvement over Reingold Tilford algorithm[2].

    According to Reingold Tilford paper, a tree diagram should satisfy the following aesthetic rules,

    1. Nodes at the same depth should lie along a straight line, and the straight lines defining the depths should be parallel.
    2. A left child should be positioned to the left of its parent node and a right child to the right.
    3. A parent should be centered over its children.
    4. A tree and its mirror image should produce drawings that are reflection of one another; a subtree should be drawn the same way regardless of where it occurs in the tree.

    References
      [1] Walker, J. (1991). Positioning Nodes for General Trees. https://www.drdobbs.com/positioning-nodes-for-general-trees/184402320?pgno=4

      [2] Reingold, E., Tilford, J. (1981). Tidier Drawings of Trees. IEEE Transactions on Software Engineering. https://reingold.co/tidier-drawings.pdf

    Args:
        tree_node (BaseNode): tree to compute (x, y) coordinate
        sibling_separation (float): minimum distance between adjacent siblings of the tree
        subtree_separation (float): minimum distance between adjacent subtrees of the tree
        level_separation (float): fixed distance between adjacent levels of the tree
        x_offset (float): graph offset of x-coordinates
        y_offset (float): graph offset of y-coordinates
    """
    first_pass(tree_node, sibling_separation)
    second_pass(tree_node, subtree_separation)
    third_pass(tree_node, level_separation, x_offset, y_offset)


def first_pass(tree_node: T, sibling_separation: float) -> None:
    """
    Performs post-order traversal of tree and assigns `x` and `mod` value to each node.
    Modifies tree in-place.

    Notation:
      - `lsibling`: left-sibling of node
      - `lchild`: last child of node
      - `fchild`: first child of node
      - `midpoint`: midpoint of node wrt children, :math:`midpoint = (lchild.x + fchild.x) / 2`
      - `distance`: sibling separation

    `x` value is the initial x-position of each node purely based on the node's position
      - :math:`x = 0` for leftmost node and :math:`x = lsibling.x + distance` for other nodes
      - Special case when leftmost node has children, then it will try to center itself, :math:`x = midpoint`

    `mod` value is the amount to shift the subtree (all descendant nodes excluding itself) to make the children centered with itself
      - :math:`mod = 0` for node does not have children (no need to shift subtree) or it is a leftmost node (parent is already centered, from above point)
      - Special case when non-leftmost nodes have children, :math:`mod = x - midpoint`

    Args:
        tree_node (BaseNode): tree to compute (x, y) coordinate
        sibling_separation (float): minimum distance between adjacent siblings of the tree
    """
    # Post-order iteration (LRN)
    for child in tree_node.children:
        first_pass(child, sibling_separation)

    _x = 0.0
    _mod = 0.0
    _midpoint = 0.0

    if not tree_node.is_root:
        if tree_node.children:
            _midpoint = (
                tree_node.children[-1].get_attr("x")
                + tree_node.children[0].get_attr("x")
            ) / 2

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


def second_pass(
    tree_node: T, subtree_separation: float, cum_mod: Optional[float] = 0.0
) -> None:
    """
    Performs level-order traversal of tree and updates `mod` value of nodes due to overlapping subtrees.
    Modifies tree in-place.

    Notation:
      - `distance`: subtree separation

    For each node on the same level, ensure that the leftmost descendant does not intersect with the rightmost
    descendant of any left sibling at every subsequent level. Intersection happens when the subtrees are not
    at least `distance` apart.

    If there are any intersection, shift the whole subtree by a new `_mod` value, shift any left sibling by a
    fraction of `_mod` value, and shift any right sibling by a multiple of the fraction of `_mod` value
    to keep nodes centralized at the level.

    Args:
        tree_node (BaseNode): tree to compute (x, y) coordinate
        subtree_separation (float): minimum distance between adjacent subtrees of the tree
        cum_mod (Optional[float]): cumulative mod for tree/subtree, used during iteration
    """

    def get_subtree_shift(
        left_subtree: T,
        right_subtree: T,
        cum_mod_left: float,
        cum_mod_right: float,
        cum_shift: float,
        initial_run: bool = False,
    ) -> float:
        """Get _mod to shift the right subtree towards the right

        Args:
            left_subtree (BaseNode): left subtree, with right contour to be traversed
            right_subtree (BaseNode): right subtree, with left contour to be traversed
            cum_mod_left (float): cumulative mod for left subtree
            cum_mod_right (float): cumulative mod for right subtree
            cum_shift (float): cumulative shift for right subtree
            initial_run (bool): indicates whether left_subtree and right_subtree are top-level subtree

        Returns:
            (float)
        """
        x_left = left_subtree.get_attr("x") + cum_mod_left
        x_right = right_subtree.get_attr("x") + cum_mod_right
        shift_amount: float = max(x_left + subtree_separation - x_right, 0)

        if not initial_run:
            # Search for a left sibling of left_subtree that has children
            while (
                left_subtree and not left_subtree.children and left_subtree.left_sibling
            ):
                left_subtree = left_subtree.left_sibling
            # Search for a right sibling of right_subtree that has children
            while (
                right_subtree
                and not right_subtree.children
                and right_subtree.right_sibling
            ):
                right_subtree = right_subtree.right_sibling
        if left_subtree.children and right_subtree.children:
            # Iterate down the level, for the rightmost child of left_subtree and the leftmost child of right_subtree
            return get_subtree_shift(
                left_subtree=left_subtree.children[-1],
                right_subtree=right_subtree.children[0],
                cum_mod_left=cum_mod_left + left_subtree.get_attr("mod"),
                cum_mod_right=cum_mod_right + right_subtree.get_attr("mod"),
                cum_shift=cum_shift + shift_amount,
            )
        return cum_shift + shift_amount

    for idx_node, right_node in enumerate(tree_node.children[1:], 1):
        _mod = get_subtree_shift(
            left_subtree=tree_node.children[0],
            right_subtree=right_node,
            cum_mod_left=tree_node.get_attr("mod"),
            cum_mod_right=tree_node.get_attr("mod"),
            cum_shift=cum_mod,
            initial_run=True,
        )
        _shift = _mod - cum_mod
        attrs = ["x", "mod"]

        # Shift the node itself
        right_node.set_attrs(
            {attr: right_node.get_attr(attr) + _shift for attr in attrs}
        )

        # Shift the nodes between leftmost subtree and right_node
        for left_sibling in tree_node.children[1:idx_node]:
            left_sibling.set_attrs(
                {
                    attr: left_sibling.get_attr(attr) + (_shift / idx_node)
                    for attr in attrs
                }
            )

        # Shift the nodes to the right of right_node
        for multiple, right_sibling in enumerate(tree_node.children[idx_node:]):
            right_sibling.set_attrs(
                {
                    attr: right_sibling.get_attr(attr) + (multiple * _shift)
                    for attr in attrs
                }
            )

    # Level-order iteration
    for child in tree_node.children:
        second_pass(child, subtree_separation, cum_mod + child.get_attr("mod"))


def third_pass(
    tree_node: T,
    level_separation: float,
    x_offset: float,
    y_offset: float,
    cum_mod: Optional[float] = 0.0,
    max_depth: Optional[int] = None,
) -> None:
    """
    Performs pre-order traversal of tree and determine the final `x` and `y` values for each node.
    Modifies tree in-place.

    Notation:
      - `depth`: maximum depth of tree
      - `distance`: level separation
      - `x'`: x offset
      - `y'`: y offset

    Final position of each node
      - :math:`x = node.x + sum(ancestor.x) + x'`
      - :math:`y = (depth - node.depth) * distance + y'`

    Args:
        tree_node (BaseNode): tree to assign x and mod value
        level_separation (float): fixed distance between adjacent levels of the tree
        x_offset (float): graph offset of x-coordinates
        y_offset (float): graph offset of y-coordinates
        cum_mod (Optional[float]): cumulative mod for tree/subtree, used during iteration
        max_depth (Optional[int]): maximum depth of tree
    """
    if not max_depth:
        max_depth = tree_node.max_depth

    final_x = tree_node.get_attr("x") + cum_mod + x_offset
    if tree_node.is_root:
        final_x = (
            tree_node.children[-1].get_attr("x") + tree_node.children[0].get_attr("x")
        ) / 2 + x_offset
    final_y = (max_depth - tree_node.depth) * level_separation + y_offset
    tree_node.set_attrs({"x": final_x, "y": final_y})

    # Pre-order iteration (NLR)
    for child in tree_node.children:
        third_pass(
            child,
            level_separation,
            x_offset,
            y_offset,
            cum_mod + tree_node.get_attr("mod"),
            max_depth,
        )

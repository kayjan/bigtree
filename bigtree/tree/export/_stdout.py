from __future__ import annotations

from typing import List, Optional, TypeVar

from bigtree.node import node
from bigtree.utils.constants import BorderStyle

__all__ = [
    "format_node",
]

T = TypeVar("T", bound=node.Node)


def calculate_stem_pos(length: int) -> int:
    """Calculate stem position based on length

    Args:
        length (int): length of node

    Returns:
        (int) Stem position
    """
    if length % 2:
        return length // 2
    return length // 2 - 1


def format_node(
    _node: T,
    alias: str,
    intermediate_node_name: bool = True,
    border_style: Optional[BorderStyle] = None,
) -> List[str]:
    """Format node to be same width, able to customise whether to add border

    Args:
        _node (Node): node to format
        alias (str): node attribute to use for node name in tree as alias to `node_name`, if present.
            Otherwise, it will default to `node_name` of node.
        intermediate_node_name (bool): indicator if intermediate nodes have node names, defaults to True
        border_style (BorderStyle): border style to format node

    Returns:
        List of str that makes up the node display
    """
    node_title: str = (
        _node.get_attr(alias) or _node.node_name if intermediate_node_name else ""
    )
    node_title_lines = node_title.split("\n")
    width = max([len(node_title_lines) for node_title_lines in node_title_lines])

    node_display_lines: List[str] = []
    if border_style:
        width += 2
        node_display_lines.append(
            f"{border_style.TOP_LEFT}{border_style.HORIZONTAL * width}{border_style.TOP_RIGHT}"
        )
        for node_title_line in node_title_lines:
            node_display_lines.append(
                f"{border_style.VERTICAL} {node_title_line.center(width - 2)} {border_style.VERTICAL}"
            )
        node_display_lines.append(
            f"{border_style.BOTTOM_LEFT}{border_style.HORIZONTAL * width}{border_style.BOTTOM_RIGHT}"
        )
    else:
        for node_title_line in node_title_lines:
            node_display_lines.append(f"{node_title_line.center(width)}")
    return node_display_lines


def horizontal_join(node_displays: List[List[str]], spacing: int = 2) -> List[str]:
    """Horizontally join multiple node displays

    Args:
        node_displays (List[List[str]]): multiple node displays belonging to the same row
        spacing (int): spacing between node displays

    Returns:
        (List[str]) node display of the row
    """
    space = " "
    height = max([len(node_display) for node_display in node_displays])
    row_display = {idx: "" for idx in range(height)}
    for node_display_idx, node_display in enumerate(node_displays):
        width = len(node_display[0])

        # Add node content
        for row_idx, node_display_row in enumerate(node_display):
            if node_display_idx:
                row_display[row_idx] += spacing * space
            row_display[row_idx] += node_display_row

        # Add node buffer
        for row_idx_buffer in range(len(node_display), height):
            if node_display_idx:
                row_display[row_idx] += spacing * space
            row_display[row_idx_buffer] += " " * width
    return [row_display[k] for k in sorted(row_display)]

from __future__ import annotations

from typing import List, Optional, TypeVar

from bigtree.node import node
from bigtree.utils.constants import BaseVPrintStyle, BorderStyle

__all__ = [
    "calculate_stem_pos",
    "format_node",
    "horizontal_join",
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
    style: BaseVPrintStyle = BaseVPrintStyle.from_style("const"),
    border_style: Optional[BorderStyle] = None,
) -> List[str]:
    """Format node to be same width, able to customise whether to add border

    Args:
        _node (Node): node to format
        alias (str): node attribute to use for node name in tree as alias to `node_name`, if present.
            Otherwise, it will default to `node_name` of node.
        intermediate_node_name (bool): indicator if intermediate nodes have node names, defaults to True
        style (BaseVPrintStyle): style to format node, used only if border_style is None
        border_style (BorderStyle): border style to format node

    Returns:
        (List[str]) node display
    """
    if not intermediate_node_name and _node.children:
        if border_style is None:
            node_title: str = style.BRANCH
            if _node.is_root:
                node_title = style.SUBSEQUENT_CHILD
        else:
            node_title = ""
    else:
        node_title = _node.get_attr(alias) or _node.node_name
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
        node_mid = calculate_stem_pos(width + 2)
        # If there is a parent
        if _node.parent:
            node_display_lines[0] = (
                node_display_lines[0][:node_mid]
                + style.SPLIT_BRANCH
                + node_display_lines[0][node_mid + 1 :]  # noqa
            )
        # If there are subsequent children
        if any(_node.children):
            node_display_lines[-1] = (
                node_display_lines[-1][:node_mid]
                + style.SUBSEQUENT_CHILD
                + node_display_lines[-1][node_mid + 1 :]  # noqa
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
                row_display[row_idx_buffer] += spacing * space
            row_display[row_idx_buffer] += width * space
    return [row_display[k] for k in sorted(row_display)]

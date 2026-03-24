from __future__ import annotations

from typing import Any, Iterable, TypeVar

from bigtree.node import node
from bigtree.tree.export._html import TREE_HTML_TEMPLATE

try:
    import json
    import uuid

    from IPython.display import HTML, display
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    uuid = MagicMock()
    HTML = MagicMock()
    display = MagicMock()


__all__ = [
    "iprint_tree",
    "tree_to_html",
]

T = TypeVar("T", bound=node.Node)


def iprint_tree(
    tree: T,
    **kwargs: Any,
) -> None:
    """Display tree interactively on jupyter notebook.

    Refer to ``tree_to_html`` for full list of parameters.

    Customisations that applies to whole tree include

    - Node colour, width
    - Border colour, radius, width
    - Edge colour, width
    - Font colour, title size, size

    Customisations available on a per-node basis include

    - Node colour
    - Border colour, width
    - Font colour

    Examples:
        >>> from bigtree import Node
        >>> root = Node("a", species="human")
        >>> b = Node("b", age=65, species="human", parent=root)
        >>> c = Node("c", age=60, species="human", parent=root)
        >>> d = Node("d", age=40, species="human", parent=b)
        >>> e = Node("e", age=35, species="human", parent=b)
        >>> root.ishow(all_attrs=True)
        <IPython.core.display.HTML object>

    Args:
        tree: tree to display
        **kwargs: refer to ``tree_to_html`` for list of parameters
    """
    tree_html = tree_to_html(
        tree,
        **kwargs,
    )
    display(HTML(tree_html))


DEFAULT_NODE_COLOUR = "#f8f9fa"
DEFAULT_BORDER_COLOUR = "#dee2e6"
DEFAULT_FONT_COLOUR = "#333"
DEFAULT_BORDER_WIDTH = 1


def tree_to_html(
    tree: T,
    all_attrs: bool = False,
    attr_list: Iterable[str] | None = None,
    node_colour: str = "#f8f9fa",
    node_width: int = 160,
    border_colour: str = "#dee2e6",
    border_radius: int = 12,
    border_width: float | int | str = 1,
    edge_colour: str = "#ccc",
    edge_width: float | int = 1.5,
    font_colour: str = "#333",
    font_title_size: int = 13,
    font_size: int = 11,
    height: int = 500,
    width: int = 900,
) -> str:
    """Get html tree diagram.

    Args:
        tree: tree to display
        all_attrs: indicator to show all attributes, overrides `attr_list`
        attr_list: node attributes to print
        node_colour: fill colour of nodes, accepts hexcode (starts with #), otherwise will be
            interpreted as the ``Node`` attribute for node_colour
        node_width: node width of nodes
        border_colour: colour of node borders, accepts hexcode (starts with #), otherwise will be
            interpreted as the ``Node`` attribute for custom border_colour
        border_radius: node radius of nodes
        border_width: width of node borders, accepts int/float, otherwise if it is string it will
            be interpreted as the ``Node`` attribute for custom border_width
        edge_colour: colour of edges
        edge_width: width of edges
        font_colour: font colour, accepts hexcode (starts with #), otherwise will be
            interpreted as the ``Node`` attribute for custom font_colour
        font_title_size: font size of title text in node
        font_size: font size of attribute text in node
        height: height of diagram
        width: width of diagram

    Returns:
        HTML string to display
    """
    from bigtree.tree.export import tree_to_nested_dict

    tree_id = f"tree_{uuid.uuid4().hex[:6]}"
    attr_list = list(attr_list) if attr_list else []

    additional_attr_list: list[str] = []

    def _get_colour_or_attr(colour_param: str, default_param: str) -> tuple[str, str]:
        colour_attr: str | None = None
        if not colour_param.startswith("#"):
            colour_attr = colour_param
            additional_attr_list.append(colour_param)
            colour_param = default_param
        return colour_param, colour_attr

    def _get_int_or_attr(
        int_param: int | float | str, default_param: int | float
    ) -> tuple[int | float, str]:
        param_attr: str | None = None
        if isinstance(int_param, str):
            param_attr = int_param
            additional_attr_list.append(int_param)
            int_param = default_param
        return int_param, param_attr

    # Evaluate whether customisations are generic or from node attribute
    node_colour, node_colour_attr = _get_colour_or_attr(
        node_colour, DEFAULT_NODE_COLOUR
    )
    border_colour, border_colour_attr = _get_colour_or_attr(
        border_colour, DEFAULT_BORDER_COLOUR
    )
    font_colour, font_colour_attr = _get_colour_or_attr(
        font_colour, DEFAULT_FONT_COLOUR
    )
    border_width, border_width_attr = _get_int_or_attr(
        border_width, DEFAULT_BORDER_WIDTH
    )

    attr_dict: dict[str, str] = dict(
        zip(attr_list + additional_attr_list, attr_list + additional_attr_list)
    )
    tree_information = tree_to_nested_dict(
        tree, attr_dict=attr_dict, all_attrs=all_attrs
    )
    tree_data = json.dumps(tree_information)
    return TREE_HTML_TEMPLATE.format(
        tree_id=tree_id,
        tree_data=tree_data,
        node_width=node_width,
        node_radius=border_radius,
        node_colour=node_colour,
        node_colour_attr=node_colour_attr,
        border_width=border_width,
        border_width_attr=border_width_attr,
        border_colour=border_colour,
        border_colour_attr=border_colour_attr,
        edge_width=edge_width,
        edge_colour=edge_colour,
        font_colour=font_colour,
        font_colour_attr=font_colour_attr,
        font_title_size=font_title_size,
        font_size=font_size,
        height=height,
        width=width,
        attr_to_ignore=f""", '{"', '".join(additional_attr_list)}'""",
    )

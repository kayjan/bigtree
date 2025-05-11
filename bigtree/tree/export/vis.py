from __future__ import annotations

from typing import Any, Dict, Optional, TypeVar

from bigtree.node import node
from bigtree.tree.export.stdout import yield_tree
from bigtree.utils import constants, exceptions, plot

try:
    import pyvis
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pyvis = MagicMock()


__all__ = [
    "tree_to_vis",
]

T = TypeVar("T", bound=node.Node)


@exceptions.optional_dependencies_vis
def tree_to_vis(
    tree: T,
    alias: str = "node_name",
    plot_kwargs: Optional[Dict[str, Any]] = None,
    custom_node_kwargs: Optional[Dict[str, str]] = None,
    node_kwargs: Optional[Dict[str, Any]] = None,
    custom_edge_kwargs: Optional[Dict[str, str]] = None,
    edge_kwargs: Optional[Dict[str, Any]] = None,
    network_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> pyvis.network.Network:
    """Export tree to pyvis for visualisations.

    - Able to have alias for node name if alias attribute is present, else it falls back to node_name, using `alias`
    - Able to control the spacing of nodes using `plot_kwargs`
    - Able to have generic node attributes using `node_kwargs`, and individualised node attributes using `custom_node_kwargs`
    - Able to have generic edge attributes using `edge_kwargs`, and individualised edge attributes using `custom_edge_kwargs`
    - Able to have generic network attributes using `network_kwargs`

    Refer to pyvis [documentation](https://pyvis.readthedocs.io/en/latest/documentation.html) for more information.

    Examples:
        >>> from bigtree import Node, tree_to_vis
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> net = tree_to_vis(root)

        Export to visualisation (html) file, etc.

        >>> net.save_graph("myvis.html")  # save only
        >>> net.show_buttons(filter_=["physics"])
        >>> net.prep_notebook()
        >>> net.show("myvis.html")  # save and show
        myvis.html
        <IPython.lib.display.IFrame object at ...>

    Args:
        tree: tree to be exported
        alias: node attribute to use for node name in tree as alias to `node_name`
        plot_kwargs: kwargs for reingold_tilford function to retrieve x, y coordinates
        custom_node_kwargs: mapping of pyvis Node kwarg to tree node attribute if present. This allows custom node
            attributes to be set. Possible keys include value (for node size), color (for node colour)
        node_kwargs: kwargs for Node for all nodes, accepts keys: color etc.
        custom_edge_kwargs: mapping of pyvis Edge kwarg to tree node attribute if present. This allows custom edge
            attributes to be set. Possible keys include width (for edge weight)
        edge_kwargs: kwargs for Edge for all edges, accept keys: weight etc.
        network_kwargs: kwargs for Network, accepts keys: height, width, bgcolor, font_color, notebook, select_menu etc.

    Returns:
        pyvis object for display
    """
    pyvis_params = constants.PyVisParameters
    plot_kwargs = {**pyvis_params.DEFAULT_PLOT_KWARGS, **(plot_kwargs or {})}
    custom_node_kwargs = {
        **pyvis_params.DEFAULT_CUSTOM_NODE_KWARGS,
        **(custom_node_kwargs or {}),
    }

    plot_kwargs = {**pyvis_params.DEFAULT_PLOT_KWARGS, **(plot_kwargs or {})}
    custom_node_kwargs = {
        **pyvis_params.DEFAULT_CUSTOM_NODE_KWARGS,
        **(custom_node_kwargs or {}),
    }
    node_kwargs = {**pyvis_params.DEFAULT_NODE_KWARGS, **(node_kwargs or {})}
    custom_edge_kwargs = custom_edge_kwargs or {}
    edge_kwargs = edge_kwargs or {}
    network_kwargs = network_kwargs or {}

    # Get x, y, coordinates of diagram
    plot.reingold_tilford(tree, reverse=True, **plot_kwargs)

    from pyvis.network import Network

    _net = Network(**network_kwargs)

    for _, _, _node in yield_tree(tree, **kwargs):
        name_str = _node.get_attr(alias) or _node.node_name
        _custom_node_kwargs = {
            k: _node.get_attr(v)
            for k, v in custom_node_kwargs.items()
            if v and _node.get_attr(v)
        }
        _node_kwargs = {**node_kwargs, **_custom_node_kwargs}

        _custom_edge_kwargs = {
            k: _node.get_attr(v)
            for k, v in custom_edge_kwargs.items()
            if v and _node.get_attr(v)
        }
        _edge_kwargs = {**edge_kwargs, **_custom_edge_kwargs}

        _net.add_node(
            _node.path_name,
            label=name_str,
            x=_node.get_attr("x"),
            y=_node.get_attr("y"),
            **_node_kwargs,
        )
        # Add edge to parent
        if _node.parent:
            _net.add_edge(_node.path_name, _node.parent.path_name, **_edge_kwargs)

    # Pyvis settings
    _net.toggle_physics(False)  # stick to x, y coordinates
    return _net

from bigtree.node.dagnode import DAGNode

__all__ = ["dag_to_dot"]


def dag_to_dot(
    tree: DAGNode,
    bgcolor: str = None,
    node_colour: str = None,
    edge_colour: str = None,
    node_attr: str = None,
):
    r"""Export DAG tree to image.
    Note that node names must be unique.
    Posible node attributes include style, fillcolor, shape.

    >>> from bigtree import DAGNode, dag_to_dot
    >>> a = DAGNode("a", step=1)
    >>> b = DAGNode("b", step=1)
    >>> c = DAGNode("c", step=2, parents=[a, b])
    >>> d = DAGNode("d", step=2, parents=[a, c])
    >>> e = DAGNode("e", step=3, parents=[d])
    >>> dag_graph = dag_to_dot(a)

    Export to image, dot file, etc.

    >>> dag_graph.write_png("tree_dag.png")
    >>> dag_graph.write_dot("tree_dag.dot")

    Export to string

    >>> dag_graph.to_string()
    'strict digraph G {\na [label=a];\nc [label=c];\na -> c;\nd [label=d];\na -> d;\nc [label=c];\na [label=a];\na -> c;\nb [label=b];\nb -> c;\nd [label=d];\nc -> d;\nd [label=d];\na [label=a];\na -> d;\nc [label=c];\nc -> d;\ne [label=e];\nd -> e;\ne [label=e];\nd [label=d];\nd -> e;\nb [label=b];\nc [label=c];\nb -> c;\n}\n'

    Args:
        tree (DAGNode): tree to be exported
        bgcolor (str): background color of image, defaults to None
        node_colour (str): fill colour of nodes, defaults to None
        edge_colour (str): colour of edges, defaults to None
        node_attr (str): node attribute for style, overrides node_colour, defaults to None

    Returns:
        (pydot.Dot)
    """
    try:
        import pydot
    except ImportError:  # pragma: no cover
        raise ImportError(
            "pydot not available. Please perform a `pip install bigtree[graph]` to install required dependencies"
        )

    if not isinstance(tree, DAGNode):
        raise ValueError("Tree should be of type `DAGNode`, or inherit from `DAGNode`")

    # Get style
    if bgcolor:
        graph_style = dict(bgcolor=bgcolor)
    else:
        graph_style = dict()

    if node_colour:
        node_style = dict(style="filled", fillcolor=node_colour)
    else:
        node_style = dict()

    if edge_colour:
        edge_style = dict(color=edge_colour)
    else:
        edge_style = dict()

    tree = tree.copy()

    _graph = pydot.Dot(graph_type="digraph", strict=True, **graph_style)
    visited_nodes = set()

    def recursive_create_node_and_edges(
        node: DAGNode, node_from_name: str, direction: int
    ):
        node = node.copy()
        node_name = node.node_name
        if node_name not in visited_nodes:
            visited_nodes.add(node_name)
            if node_attr and node.get_attr(node_attr):
                node_style.update(node.get_attr(node_attr))
            pydot_node = pydot.Node(name=node_name, label=node_name, **node_style)
            _graph.add_node(pydot_node)

            # Parse upwards
            for parent in node.parents:
                parent_name = parent.node_name
                pydot_parent_node = pydot.Node(
                    name=parent_name, label=parent_name, **node_style
                )
                edge = pydot.Edge(parent_name, node_name, **edge_style)
                _graph.add_node(pydot_parent_node)
                _graph.add_edge(edge)

            # Parse downwards
            for child in node.children:
                child_name = child.node_name
                pydot_child_node = pydot.Node(
                    name=child_name, label=child_name, **node_style
                )
                edge = pydot.Edge(node_name, child_name, **edge_style)
                _graph.add_node(pydot_child_node)
                _graph.add_edge(edge)

            # Came from parent
            if direction == 1:
                children = list(node.children)
                parents = list(node.parents)
                if node_from_name is not None:
                    parents = [
                        parent
                        for parent in parents
                        if parent.node_name != node_from_name
                    ]
                for child in children:
                    recursive_create_node_and_edges(child, node_name, 1)
                for parent in parents:
                    recursive_create_node_and_edges(parent, node_name, 0)

            # Came from child
            else:
                children = list(node.children)
                parents = list(node.parents)
                children = [
                    child for child in children if child.node_name != node_from_name
                ]
                for child in children:
                    recursive_create_node_and_edges(child, node_name, 0)
                for parent in parents:
                    recursive_create_node_and_edges(parent, node_name, 1)

    recursive_create_node_and_edges(tree, None, 1)
    return _graph

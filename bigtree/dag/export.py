from bigtree.node.dagnode import DAGNode
from bigtree.utils.iterators import dag_iterator

__all__ = ["dag_to_dot"]


def dag_to_dot(
    dag: DAGNode,
    rankdir: str = "TB",
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
    'strict digraph G {\na [label=a];\nc [label=c];\na -> c;\na [label=a];\nd [label=d];\na -> d;\nb [label=b];\nc [label=c];\nb -> c;\nc [label=c];\nd [label=d];\nc -> d;\nd [label=d];\ne [label=e];\nd -> e;\n}\n'

    Args:
        dag (DAGNode): tree to be exported
        rankdir (str): set direction of graph layout, defaults to 'TB', can be 'BT, 'LR', 'RL'
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
            "pydot not available. Please perform a\n\npip install 'bigtree[image]'\n\nto install required dependencies"
        )

    if not isinstance(dag, DAGNode):
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

    dag = dag.copy()

    _graph = pydot.Dot(
        graph_type="digraph", strict=True, rankdir=rankdir, **graph_style
    )

    for parent_node, child_node in dag_iterator(dag):
        parent_name = parent_node.name
        parent_node_style = node_style.copy()
        if node_attr and parent_node.get_attr(node_attr):
            parent_node_style.update(parent_node.get_attr(node_attr))
        pydot_parent = pydot.Node(
            name=parent_name, label=parent_name, **parent_node_style
        )
        _graph.add_node(pydot_parent)

        child_name = child_node.name
        child_node_style = node_style.copy()
        if node_attr and child_node.get_attr(node_attr):
            child_node_style.update(child_node.get_attr(node_attr))
        pydot_child = pydot.Node(name=child_name, label=child_name, **parent_node_style)
        _graph.add_node(pydot_child)

        edge = pydot.Edge(parent_name, child_name, **edge_style)
        _graph.add_edge(edge)

    return _graph

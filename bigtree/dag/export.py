from __future__ import annotations

from typing import Any, Dict, List, Tuple, TypeVar, Union

from bigtree.node import dagnode
from bigtree.utils import assertions, exceptions, iterators

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pd = MagicMock()

try:
    import pydot
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pydot = MagicMock()

__all__ = ["dag_to_list", "dag_to_dict", "dag_to_dataframe", "dag_to_dot"]


T = TypeVar("T", bound=dagnode.DAGNode)


def dag_to_list(
    dag: T,
) -> List[Tuple[str, str]]:
    """Export DAG to list of tuples containing parent-child names.

    Examples:
        >>> from bigtree import DAGNode, dag_to_list
        >>> a = DAGNode("a", step=1)
        >>> b = DAGNode("b", step=1)
        >>> c = DAGNode("c", step=2, parents=[a, b])
        >>> d = DAGNode("d", step=2, parents=[a, c])
        >>> e = DAGNode("e", step=3, parents=[d])
        >>> dag_to_list(a)
        [('a', 'c'), ('a', 'd'), ('b', 'c'), ('c', 'd'), ('d', 'e')]

    Args:
        dag: DAG to be exported

    Returns:
        List of tuples containing parent-child names
    """
    relations = []
    for parent_node, child_node in iterators.dag_iterator(dag):
        relations.append((parent_node.node_name, child_node.node_name))
    return relations


def dag_to_dict(
    dag: T,
    parent_key: str = "parents",
    attr_dict: Dict[str, str] = {},
    all_attrs: bool = False,
) -> Dict[str, Any]:
    """Export DAG to dictionary. Exported dictionary will have key as child name, and values as a dictionary of parent
    names and node attributes.

    Examples:
        >>> from bigtree import DAGNode, dag_to_dict
        >>> a = DAGNode("a", step=1)
        >>> b = DAGNode("b", step=1)
        >>> c = DAGNode("c", step=2, parents=[a, b])
        >>> d = DAGNode("d", step=2, parents=[a, c])
        >>> e = DAGNode("e", step=3, parents=[d])
        >>> dag_to_dict(a, parent_key="parent", attr_dict={"step": "step no."})
        {'a': {'step no.': 1}, 'c': {'parent': ['a', 'b'], 'step no.': 2}, 'd': {'parent': ['a', 'c'], 'step no.': 2}, 'b': {'step no.': 1}, 'e': {'parent': ['d'], 'step no.': 3}}

    Args:
        dag: DAG to be exported
        parent_key: dictionary key for `node.parent.node_name`
        attr_dict: dictionary mapping node attributes to dictionary key, key: node attributes, value: corresponding
            dictionary key
        all_attrs: indicator whether to retrieve all `Node` attributes

    Returns:
        Dictionary of node names to their attributes
    """
    dag = dag.copy()
    data_dict = {}

    for parent_node, child_node in iterators.dag_iterator(dag):
        if parent_node.is_root:
            data_parent: Dict[str, Any] = {}
            if all_attrs:
                data_parent.update(
                    parent_node.describe(
                        exclude_attributes=["name"], exclude_prefix="_"
                    )
                )
            else:
                for k, v in attr_dict.items():
                    data_parent[v] = parent_node.get_attr(k)
            data_dict[parent_node.node_name] = data_parent

        if data_dict.get(child_node.node_name):
            data_dict[child_node.node_name][parent_key].append(parent_node.node_name)
        else:
            data_child = {parent_key: [parent_node.node_name]}
            if all_attrs:
                data_child.update(
                    child_node.describe(exclude_attributes=["name"], exclude_prefix="_")
                )
            else:
                for k, v in attr_dict.items():
                    data_child[v] = child_node.get_attr(k)
            data_dict[child_node.node_name] = data_child
    return data_dict


@exceptions.optional_dependencies_pandas
def dag_to_dataframe(
    dag: T,
    name_col: str = "name",
    parent_col: str = "parent",
    attr_dict: Dict[str, str] = {},
    all_attrs: bool = False,
) -> pd.DataFrame:
    """Export DAG to pandas DataFrame.

    Examples:
        >>> from bigtree import DAGNode, dag_to_dataframe
        >>> a = DAGNode("a", step=1)
        >>> b = DAGNode("b", step=1)
        >>> c = DAGNode("c", step=2, parents=[a, b])
        >>> d = DAGNode("d", step=2, parents=[a, c])
        >>> e = DAGNode("e", step=3, parents=[d])
        >>> dag_to_dataframe(a, name_col="name", parent_col="parent", attr_dict={"step": "step no."})
          name parent  step no.
        0    a   None         1
        1    c      a         2
        2    d      a         2
        3    b   None         1
        4    c      b         2
        5    d      c         2
        6    e      d         3

    Args:
        dag: DAG to be exported
        name_col: column name for `node.node_name`
        parent_col: column name for `node.parent.node_name`
        attr_dict: dictionary mapping node attributes to column name, key: node attributes, value: corresponding column
            in dataframe
        all_attrs: indicator whether to retrieve all `Node` attributes

    Returns:
        pandas DataFrame of DAG information
    """
    dag = dag.copy()
    data_list: List[Dict[str, Any]] = []

    for parent_node, child_node in iterators.dag_iterator(dag):
        if parent_node.is_root:
            data_parent = {name_col: parent_node.node_name, parent_col: None}
            if all_attrs:
                data_parent.update(
                    parent_node.describe(
                        exclude_attributes=["name"], exclude_prefix="_"
                    )
                )
            else:
                for k, v in attr_dict.items():
                    data_parent[v] = parent_node.get_attr(k)
            data_list.append(data_parent)

        data_child = {name_col: child_node.node_name, parent_col: parent_node.node_name}
        if all_attrs:
            data_child.update(
                child_node.describe(exclude_attributes=["name"], exclude_prefix="_")
            )
        else:
            for k, v in attr_dict.items():
                data_child[v] = child_node.get_attr(k)
        data_list.append(data_child)
    return pd.DataFrame(data_list).drop_duplicates().reset_index(drop=True)


@exceptions.optional_dependencies_image("pydot")
def dag_to_dot(
    dag: Union[T, List[T]],
    rankdir: str = "TB",
    bg_colour: str = "",
    node_colour: str = "",
    node_shape: str = "",
    edge_colour: str = "",
    node_attr: str = "",
    edge_attr: str = "",
) -> pydot.Dot:
    r"""Export DAG or list of DAGs to image. Note that node names must be unique. Possible node attributes include style,
    fillcolor, or shape.

    Examples:
        >>> from bigtree import DAGNode, dag_to_dot
        >>> a = DAGNode("a", step=1)
        >>> b = DAGNode("b", step=1)
        >>> c = DAGNode("c", step=2, parents=[a, b])
        >>> d = DAGNode("d", step=2, parents=[a, c])
        >>> e = DAGNode("e", step=3, parents=[d])
        >>> dag_graph = dag_to_dot(a)

        Display image directly without saving (requires IPython)

        >>> from IPython.display import Image, display
        >>> plt = Image(dag_graph.create_png())
        >>> display(plt)
        <IPython.core.display.Image object>

        Export to image, dot file, etc.

        >>> dag_graph.write_png("assets/tree_dag.png")
        >>> dag_graph.write_dot("assets/tree_dag.dot")

        ![Export to Dot](https://github.com/kayjan/bigtree/raw/master/assets/tree_dag.png)

        Export to string

        >>> dag_graph.to_string()
        'strict digraph G {\nrankdir=TB;\nc [label=c];\na [label=a];\na -> c;\nd [label=d];\na [label=a];\na -> d;\nc [label=c];\nb [label=b];\nb -> c;\nd [label=d];\nc [label=c];\nc -> d;\ne [label=e];\nd [label=d];\nd -> e;\n}\n'

    Args:
        dag: DAG or list of DAGs to be exported
        rankdir: set direction of graph layout, accepts 'TB', 'BT, 'LR', or 'RL'
        bg_colour: background color of image
        node_colour: fill colour of nodes
        node_shape: shape of nodes. Possible node_shape include "circle", "square", "diamond", "triangle"
        edge_colour: colour of edges
        node_attr: node attribute for style, overrides node_colour. Possible node attributes include {"style": "filled",
            "fillcolor": "gold"}
        edge_attr: edge attribute for style, overrides edge_colour. Possible edge attributes include {"style": "bold",
            "label": "edge label", "color": "black"}

    Returns:
        pydot object of DAG
    """
    # Get style
    graph_style = dict(bgcolor=bg_colour) if bg_colour else {}
    node_style = dict(style="filled", fillcolor=node_colour) if node_colour else {}
    node_style.update({"shape": node_shape} if node_shape else {})
    edge_style = dict(color=edge_colour) if edge_colour else {}

    _graph = pydot.Dot(
        graph_type="digraph", strict=True, rankdir=rankdir, **graph_style
    )

    if not isinstance(dag, list):
        dag = [dag]

    for _dag in dag:
        assertions.assert_tree_type(_dag, dagnode.DAGNode, "DAGNode")
        _dag = _dag.copy()

        for parent_node, child_node in iterators.dag_iterator(_dag):
            _node_style = node_style.copy()
            _edge_style = edge_style.copy()

            child_name = child_node.node_name
            if node_attr and child_node.get_attr(node_attr):
                _node_style.update(child_node.get_attr(node_attr))
            if edge_attr and child_node.get_attr(edge_attr):
                _edge_style.update(child_node.get_attr(edge_attr))
            pydot_child = pydot.Node(name=child_name, label=child_name, **_node_style)
            _graph.add_node(pydot_child)

            parent_name = parent_node.node_name
            parent_node_style = node_style.copy()
            if node_attr and parent_node.get_attr(node_attr):
                parent_node_style.update(parent_node.get_attr(node_attr))
            pydot_parent = pydot.Node(
                name=parent_name, label=parent_name, **parent_node_style
            )
            _graph.add_node(pydot_parent)

            edge = pydot.Edge(parent_name, child_name, **_edge_style)
            _graph.add_edge(edge)

    return _graph

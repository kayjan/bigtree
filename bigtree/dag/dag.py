from __future__ import annotations

import copy
from typing import Any, Collection, Iterable, Mapping, TypeVar

from bigtree.dag import construct, export
from bigtree.node import dagnode
from bigtree.utils import exceptions, iterators

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


class DAG:
    """
    DAG wraps around DAGNode class to provide a quick, intuitive, Pythonic API for

        * Construction with dataframe, dictionary, or list
        * Export to dataframe, dictionary, list, or images

    Do refer to the various modules respectively on the keyword parameters.
    """

    construct_kwargs: dict[str, Any] = dict()

    def __init__(self, dag: dagnode.DAGNode):
        self.dag = dag

    # Construct methods
    @classmethod
    def from_dataframe(cls, data: pd.DataFrame, **kwargs: Any) -> "DAG":
        """See `dataframe_to_dag` for full details.

        Accepts the same arguments as `dataframe_to_dag`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.dataframe_to_dag(data, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_dict(cls, relation_attrs: Mapping[str, Any], **kwargs: Any) -> "DAG":
        """See `dict_to_dag` for full details.

        Accepts the same arguments as `dict_to_dag`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.dict_to_dag(relation_attrs, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_list(cls, relations: Collection[tuple[str, str]], **kwargs: Any) -> "DAG":
        """See `list_to_dag` for full details.

        Accepts the same arguments as `list_to_dag`.
        """
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.list_to_dag(relations, **construct_kwargs)
        return cls(root_node)

    # Export methods
    def to_dataframe(self, *args: Any, **kwargs: Any) -> pd.DataFrame:
        """See `dag_to_dataframe` for full details.

        Accepts the same arguments as `dag_to_dataframe`.
        """
        return export.dag_to_dataframe(self.dag, *args, **kwargs)

    def to_dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """See `dag_to_dict` for full details.

        Accepts the same arguments as `dag_to_dict`.
        """
        return export.dag_to_dict(self.dag, *args, **kwargs)

    def to_list(self) -> list[tuple[str, str]]:
        """See `dag_to_list` for full details."""
        return export.dag_to_list(self.dag)

    @exceptions.optional_dependencies_image("pydot")
    def to_dot(self, *args: Any, **kwargs: Any) -> pydot.Dot:
        """See `dag_to_dot` for full details.

        Accepts the same arguments as `dag_to_dot`.
        """
        return export.dag_to_dot(self.dag, *args, **kwargs)

    # Iterator methods
    def iterate(self) -> Iterable[tuple[dagnode.DAGNode, dagnode.DAGNode]]:
        """See `dag_iterator` for full details."""
        return iterators.dag_iterator(self.dag)

    # Magic methods
    def __getitem__(self, child_name: str) -> "DAG":
        """Get child by name identifier.

        Args:
            child_name: name of child node

        Returns:
            Child node
        """
        from bigtree.tree.search import find_child_by_name

        return type(self)(find_child_by_name(self.dag, child_name))

    def __delitem__(self, child_name: str) -> None:
        """Delete child by name identifier, will not throw error if child does not exist.

        Args:
            child_name: name of child node
        """
        from bigtree.tree.search import find_child_by_name

        child = find_child_by_name(self.dag, child_name)
        if child:
            self.dag._DAGNode__children.remove(child)  # type: ignore
            child._DAGNode__parents.remove(self.dag)  # type: ignore

    def copy(self: T) -> T:
        """Deep copy self; clone DAG.

        Returns:
            Cloned copy of DAG
        """
        return copy.deepcopy(self)

    def __copy__(self: T) -> T:
        """Shallow copy self.

        Returns:
            Shallow copy of DAG
        """
        obj: T = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __repr__(self) -> str:
        """Print format of DAGNode.

        Returns:
            Print format of DAGNode
        """
        class_name = self.__class__.__name__
        node_dict = self.dag.describe(exclude_attributes=["name"])
        node_description = ", ".join(
            [f"{k}={v}" for k, v in node_dict if not k.startswith("_")]
        )
        return f"{class_name}({self.dag.node_name}, {node_description})"


T = TypeVar("T", bound=DAG)

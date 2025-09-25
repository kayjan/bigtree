from typing import Any, Collection, Mapping

import pandas as pd

from bigtree.dag import construct, export
from bigtree.node import dagnode
from bigtree.utils import exceptions

try:
    import pydot
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pydot = MagicMock()


class DAG:
    """
    DAG wraps around DAGNode class to provide a quick, intuitive, Pythonic API for
        - Construction with dataframe, dictionary, or list
        - Export to dataframe, dictionary, list, or images

    Do refer to the various modules respectively on the keyword parameters.
    """

    construct_kwargs: dict[str, Any] = dict()

    def __init__(self, dag: dagnode.DAGNode):
        self.dag = dag

    # Construct methods
    @classmethod
    def from_dataframe(cls, data: pd.DataFrame, **kwargs: Any) -> "DAG":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.dataframe_to_dag(data, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_dict(cls, relation_attrs: Mapping[str, Any], **kwargs: Any) -> "DAG":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.dict_to_dag(relation_attrs, **construct_kwargs)
        return cls(root_node)

    @classmethod
    def from_list(cls, relations: Collection[tuple[str, str]], **kwargs: Any) -> "DAG":
        construct_kwargs = {**cls.construct_kwargs, **kwargs}
        root_node = construct.list_to_dag(relations, **construct_kwargs)
        return cls(root_node)

    # Export methods
    def to_dataframe(self, *args: Any, **kwargs: Any) -> pd.DataFrame:
        return export.dag_to_dataframe(self.dag, *args, **kwargs)

    def to_dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return export.dag_to_dict(self.dag, *args, **kwargs)

    def to_list(self, *args: Any, **kwargs: Any) -> list[tuple[str, str]]:
        return export.dag_to_list(self.dag, *args, **kwargs)

    @exceptions.optional_dependencies_image("pydot")
    def to_dot(self, *args: Any, **kwargs: Any) -> pydot.Dot:
        return export.dag_to_dot(self.dag, *args, **kwargs)

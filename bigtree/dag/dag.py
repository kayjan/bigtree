from __future__ import annotations

import copy
import functools
from typing import Any, Callable, Literal, TypeVar

from bigtree.dag import construct, export
from bigtree.node import dagnode
from bigtree.utils import iterators


class DAG:
    """
    DAG wraps around DAGNode class to provide a quick, intuitive, Pythonic API for

        * Construction with dataframe, dictionary, or list
        * Export to dataframe, dictionary, list, or images

    Do refer to the various modules respectively on the keyword parameters.
    """

    _plugins: dict[str, Callable[..., Any]] = {}
    construct_kwargs: dict[str, Any] = dict()

    def __init__(self, dag: dagnode.DAGNode):
        self.dag = dag

    @classmethod
    def register_plugin(
        cls, name: str, func: Callable[..., Any], method: Literal["default", "class"]
    ) -> None:
        base_func = func.func if isinstance(func, functools.partial) else func

        if method == "default":

            def wrapper(self, *args, **kwargs):  # type: ignore
                return func(self.dag, *args, **kwargs)

        else:

            def wrapper(cls, *args, **kwargs):  # type: ignore
                construct_kwargs = {**cls.construct_kwargs, **kwargs}
                root_node = func(*args, **construct_kwargs)
                return cls(root_node)

        functools.update_wrapper(wrapper, base_func)
        wrapper.__name__ = name
        if method == "class":
            setattr(cls, name, classmethod(wrapper))  # type: ignore
        else:
            setattr(cls, name, wrapper)
        cls._plugins[name] = func

    @classmethod
    def register_plugins(
        cls,
        mapping: dict[str, Callable[..., Any]],
        method: Literal["default", "class"] = "default",
    ) -> None:
        for name, func in mapping.items():
            cls.register_plugin(name, func, method)

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

DAG.register_plugins(
    {
        # Construct methods
        "from_dataframe": construct.dataframe_to_dag,
        "from_dict": construct.dict_to_dag,
        "from_list": construct.list_to_dag,
    },
    method="class",
)
DAG.register_plugins(
    {
        # Export methods
        "to_dataframe": export.dag_to_dataframe,
        "to_dict": export.dag_to_dict,
        "to_list": export.dag_to_list,
        "to_dot": export.dag_to_dot,
        # Iterator methods
        "iterate": iterators.dag_iterator,
    },
)

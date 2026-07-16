from typing import TYPE_CHECKING, Any, Callable, Iterable, Literal, Sequence, TypeVar

from bigtree.tree.tree import Tree

if TYPE_CHECKING:
    from bigtree.node import binarynode

    T = TypeVar("T", bound=binarynode.BinaryNode)

class BinaryTree(Tree):

    _plugins: dict[str, Callable[..., Any]] = {}
    construct_kwargs: dict[str, Any] = dict()

    @classmethod
    def from_heapq_list(
        cls,
        heapq_list: Sequence[int],
        node_type: type[T] = binarynode.BinaryNode,  # type: ignore[assignment]
    ) -> BinaryTree: ...
    def inorder_iter(
        self,
        filter_condition: Callable[[T], bool] | None = None,
        max_depth: int = 0,
    ) -> Iterable[T]: ...

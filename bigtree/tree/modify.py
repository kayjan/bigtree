import logging
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

from bigtree.node import node
from bigtree.tree import construct, search
from bigtree.utils import exceptions

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "merge_trees",
    "shift_nodes",
    "copy_nodes",
    "shift_and_replace_nodes",
    "copy_nodes_from_tree_to_tree",
    "copy_and_replace_nodes_from_tree_to_tree",
    "copy_or_shift_logic",
    "replace_logic",
]

T = TypeVar("T", bound=node.Node)


def merge_trees(
    trees: Union[List[T], Tuple[T, ...]],
    exact: bool = False,
) -> T:
    """Merge multiple trees into a single tree. Returns a new tree.

    If trees have different root names, it will take the root name of the first tree. If same path exists, the
    attributes of both nodes will be combined, with priority given to the later tree.

    - Able to merge only the tree/branches provided exactly, defaults to False (the whole tree is merged), in the case
        when it is True, it is meant to merge tree branches and only the paths and attributes in the branches are retained.
        All branches must have the same root name

    Examples:
        >>> from bigtree import list_to_tree, merge_trees
        >>> downloads_folder = list_to_tree(["Downloads/Pictures/photo1.jpg", "Downloads/file1.doc"])
        >>> downloads_folder.show()
        Downloads
        ├── Pictures
        │   └── photo1.jpg
        └── file1.doc

        >>> documents_folder = list_to_tree(["Documents/Pictures/photo2.jpg", "Documents/file1.doc"])
        >>> documents_folder["file1.doc"].size = 100
        >>> documents_folder.show(all_attrs=True)
        Documents
        ├── Pictures
        │   └── photo2.jpg
        └── file1.doc [size=100]

        >>> root = merge_trees([downloads_folder, documents_folder])
        >>> root.show(all_attrs=True)
        Downloads
        ├── Pictures
        │   ├── photo1.jpg
        │   └── photo2.jpg
        └── file1.doc [size=100]

        In ``exact=True`` case, only path and attributes of branches are retained.

        >>> from bigtree import dict_to_tree, merge_trees, find_attrs
        >>> path_dict = {
        ...     "a": {"age": 90},
        ...     "a/b": {"age": 65},
        ...     "a/c": {"age": 60},
        ...     "a/b/d": {"age": 40},
        ...     "a/b/e": {"age": 35},
        ...     "a/c/f": {"age": 10},
        ...     "a/b/e/g": {"age": 10},
        ...     "a/b/e/h": {"age": 6},
        ... }
        >>> root = dict_to_tree(path_dict)
        >>> root.show(attr_list=["age"])
        a [age=90]
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        │       ├── g [age=10]
        │       └── h [age=6]
        └── c [age=60]
            └── f [age=10]

        >>> nodes = find_attrs(root, "age", 10)
        >>> nodes
        (Node(/a/b/e/g, age=10), Node(/a/c/f, age=10))
        >>> root_filtered = merge_trees(nodes, exact=True)
        >>> root_filtered.show(attr_list=["age"])
        a
        ├── b
        │   └── e
        │       └── g [age=10]
        └── c
            └── f [age=10]

    Args:
        trees: trees to merge, it can be the tree root or a branch of the tree
        exact: whether to merge the trees provided exactly; only the paths and attributes of the trees/branches are used.
            If false, the whole tree is merged

    Returns:
        Merged tree
    """
    if not exact:
        merged_tree = trees[0].copy()
        root_name = merged_tree.root.node_name
        for _tree in trees[1:]:
            _tree = _tree.root
            child_names = [_child.node_name for _child in _tree.children]
            for child_name in child_names:
                path = f"{root_name}/{child_name}"
                kwargs = (
                    {"merge_children": True}
                    if search.find_full_path(merged_tree, path)
                    else {}
                )
                copy_nodes_from_tree_to_tree(
                    from_tree=_tree,
                    to_tree=merged_tree,
                    from_paths=[f"{_tree.node_name}/{child_name}"],
                    to_paths=[f"{root_name}/{child_name}"],
                    merge_attribute=True,
                    **kwargs,  # type: ignore
                )
    else:
        path_attrs: Dict[str, Dict[str, Any]] = {}
        for tree in trees:
            tree_attr = dict(tree.describe(exclude_prefix="_"))
            path_attrs[tree.path_name] = {
                **path_attrs.get(tree.path_name, {}),
                **tree_attr,
            }
        merged_tree = construct.dict_to_tree(path_attrs)
    return merged_tree


def shift_nodes(
    tree: T,
    from_paths: List[str],
    to_paths: List[Optional[str]],
    sep: str = "/",
    skippable: bool = False,
    overriding: bool = False,
    merge_attribute: bool = False,
    merge_children: bool = False,
    merge_leaves: bool = False,
    delete_children: bool = False,
    with_full_path: bool = False,
) -> None:
    """Shift nodes from `from_paths` to `to_paths` *in-place*.

    - Creates intermediate nodes if to-path is not present
    - Able to skip nodes if from-path is not found, defaults to False (from-nodes must be found; not skippable)
    - Able to override existing node if it exists, defaults to False (to-nodes must not exist; not overridden)
    - Able to merge attributes of node if it exists, defaults to False (to-nodes must not exist; no attributes to merge)
    - Able to merge children and remove intermediate parent node, defaults to False (nodes are shifted; not merged)
    - Able to merge leaf nodes and remove all intermediate nodes, defaults to False (nodes are shifted; not merged)
    - Able to shift node only and delete children, defaults to False (nodes are shifted together with children)

    For paths in `from_paths` and `to_paths`,

    - Path name can be with or without leading tree path separator symbol

    For paths in `from_paths`,

    - Path name can be partial path (trailing part of path) or node name
    - If ``with_full_path=True``, path name must be full path
    - Path name must be unique to one node

    For paths in `to_paths`,

    - Path name must be full path
    - Can set to empty string or None to delete the path in `from_paths`, note that ``copy`` must be set to False

    If ``merge_children=True``,

    - If `to_path` is not present, it shifts children of `from_path`
    - If `to_path` is present, and ``overriding=False``, original and new children are merged
    - If `to_path` is present and ``overriding=True``, it behaves like overriding and only new children are retained

    If ``merge_leaves=True``,

    - If `to_path` is not present, it shifts leaves of `from_path`
    - If `to_path` is present, and ``overriding=False``, original children and leaves are merged
    - If `to_path` is present and ``overriding=True``, it behaves like overriding and only new leaves are retained,
        original child nodes in `from_path` are retained

    Note:

    - `merge_children` and `merge_leaves` cannot be both True at the same time
    - `overriding` and `merge_attribute` cannot be both True at the same time

    Examples:
        >>> from bigtree import list_to_tree, str_to_tree, shift_nodes
        >>> root = list_to_tree(["Downloads/photo1.jpg", "Downloads/file1.doc"])
        >>> root.show()
        Downloads
        ├── photo1.jpg
        └── file1.doc

        >>> shift_nodes(
        ...     tree=root,
        ...     from_paths=["Downloads/photo1.jpg", "Downloads/file1.doc"],
        ...     to_paths=["Downloads/Pictures/photo1.jpg", "Downloads/Files/file1.doc"],
        ... )
        >>> root.show()
        Downloads
        ├── Pictures
        │   └── photo1.jpg
        └── Files
            └── file1.doc

        To delete node,

        >>> root = list_to_tree(["Downloads/photo1.jpg", "Downloads/file1.doc"])
        >>> root.show()
        Downloads
        ├── photo1.jpg
        └── file1.doc

        >>> shift_nodes(root, ["Downloads/photo1.jpg"], [None])
        >>> root.show()
        Downloads
        └── file1.doc

        In overriding case,

        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── Misc\\n"
        ... "│   └── Pictures\\n"
        ... "│       └── photo1.jpg\\n"
        ... "└── Pictures\\n"
        ... "    └── photo2.jpg"
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        │   └── Pictures
        │       └── photo1.jpg
        └── Pictures
            └── photo2.jpg

        >>> shift_nodes(root, ["Downloads/Misc/Pictures"], ["Downloads/Pictures"], overriding=True)
        >>> root.show()
        Downloads
        ├── Misc
        └── Pictures
            └── photo1.jpg

        In ``merge_children=True`` case, child nodes are shifted instead of the parent node.

        - If the path already exists, child nodes are merged with existing children
        - Otherwise, the child nodes of the node are merged with the node's parent

        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── Misc\\n"
        ... "│   ├── Pictures\\n"
        ... "│   │   └── photo2.jpg\\n"
        ... "│   └── Applications\\n"
        ... "│       └── Chrome.exe\\n"
        ... "├── Pictures\\n"
        ... "│   └── photo1.jpg\\n"
        ... "└── dummy\\n"
        ... "    └── Files\\n"
        ... "        └── file1.doc"
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        │   ├── Pictures
        │   │   └── photo2.jpg
        │   └── Applications
        │       └── Chrome.exe
        ├── Pictures
        │   └── photo1.jpg
        └── dummy
            └── Files
                └── file1.doc

        >>> shift_nodes(
        ...     root,
        ...     ["Downloads/Misc/Pictures", "Applications", "Downloads/dummy"],
        ...     ["Downloads/Pictures", "Downloads/Applications", "Downloads/dummy"],
        ...     merge_children=True,
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        ├── Pictures
        │   ├── photo1.jpg
        │   └── photo2.jpg
        ├── Chrome.exe
        └── Files
            └── file1.doc

        In ``merge_leaves=True`` case, leaf nodes are shifted instead of the parent node.

        - If the path already exists, leaf nodes are merged with existing children
        - Otherwise, the leaf nodes of the node are merged with the node's parent

        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── Misc\\n"
        ... "│   ├── Pictures\\n"
        ... "│   │   └── photo2.jpg\\n"
        ... "│   └── Applications\\n"
        ... "│       └── Chrome.exe\\n"
        ... "├── Pictures\\n"
        ... "│   └── photo1.jpg\\n"
        ... "└── dummy\\n"
        ... "    └── Files\\n"
        ... "        └── file1.doc"
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        │   ├── Pictures
        │   │   └── photo2.jpg
        │   └── Applications
        │       └── Chrome.exe
        ├── Pictures
        │   └── photo1.jpg
        └── dummy
            └── Files
                └── file1.doc

        >>> shift_nodes(
        ...     root,
        ...     ["Downloads/Misc/Pictures", "Applications", "Downloads/dummy"],
        ...     ["Downloads/Pictures", "Downloads/Applications", "Downloads/dummy"],
        ...     merge_leaves=True,
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        │   ├── Pictures
        │   └── Applications
        ├── Pictures
        │   ├── photo1.jpg
        │   └── photo2.jpg
        ├── dummy
        │   └── Files
        ├── Chrome.exe
        └── file1.doc

        In ``delete_children=True`` case, only the node is shifted without its accompanying children/descendants.

        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── Misc\\n"
        ... "│   └── Applications\\n"
        ... "│       └── Chrome.exe\\n"
        ... "└── Pictures\\n"
        ... "    └── photo1.jpg"
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        │   └── Applications
        │       └── Chrome.exe
        └── Pictures
            └── photo1.jpg

        >>> shift_nodes(root, ["Applications"], ["Downloads/Applications"], delete_children=True)
        >>> root.show()
        Downloads
        ├── Misc
        ├── Pictures
        │   └── photo1.jpg
        └── Applications

    Args:
        tree: tree to modify
        from_paths: original paths to shift nodes from
        to_paths: new paths to shift nodes to
        sep: path separator for input paths, applies to `from_path` and `to_path`
        skippable: indicator to skip if from-path is not found
        overriding: indicator to override existing to-path if there are clashes
        merge_attribute: indicator to merge attributes of from-path and to-path if there are clashes
        merge_children: indicator to merge from-path's children and remove intermediate parent node
        merge_leaves: indicator to merge from-path's leaf nodes and remove intermediate parent node(s)
        delete_children: indicator to shift node only without children
        with_full_path: indicator to shift node with full path in `from_paths`, results in faster search
    """
    return copy_or_shift_logic(
        tree=tree,
        from_paths=from_paths,
        to_paths=to_paths,
        sep=sep,
        copy=False,
        skippable=skippable,
        overriding=overriding,
        merge_attribute=merge_attribute,
        merge_children=merge_children,
        merge_leaves=merge_leaves,
        delete_children=delete_children,
        to_tree=None,
        with_full_path=with_full_path,
    )  # pragma: no cover


def copy_nodes(
    tree: T,
    from_paths: List[str],
    to_paths: List[Optional[str]],
    sep: str = "/",
    skippable: bool = False,
    overriding: bool = False,
    merge_attribute: bool = False,
    merge_children: bool = False,
    merge_leaves: bool = False,
    delete_children: bool = False,
    with_full_path: bool = False,
) -> None:
    """Copy nodes from `from_paths` to `to_paths` *in-place*.

    - Creates intermediate nodes if to-path is not present
    - Able to skip nodes if from-path is not found, defaults to False (from-nodes must be found; not skippable)
    - Able to override existing node if it exists, defaults to False (to-nodes must not exist; not overridden)
    - Able to merge attributes of node if it exists, defaults to False (to-nodes must not exist; no attributes to merge)
    - Able to merge children and remove intermediate parent node, defaults to False (nodes are copied; not merged)
    - Able to merge only leaf nodes and remove all intermediate nodes, defaults to False (nodes are copied; not merged)
    - Able to copy node only and delete children, defaults to False (nodes are copied together with children)

    For paths in `from_paths` and `to_paths`,

    - Path name can be with or without leading tree path separator symbol

    For paths in `from_paths`,

    - Path name can be partial path (trailing part of path) or node name
    - If ``with_full_path=True``, path name must be full path
    - Path name must be unique to one node

    For paths in `to_paths`,

    - Path name must be full path

    If ``merge_children=True``,

    - If `to_path` is not present, it copies children of `from_path`
    - If `to_path` is present, and ``overriding=False``, original and new children are merged
    - If `to_path` is present and ``overriding=True``, it behaves like overriding and only new children are retained

    If ``merge_leaves=True``,

    - If `to_path` is not present, it copies leaves of `from_path`
    - If `to_path` is present, and ``overriding=False``, original children and leaves are merged
    - If `to_path` is present and ``overriding=True``, it behaves like overriding and only new leaves are retained,
        original child nodes in `from_path` are retained

    Note:

    - `merge_children` and `merge_leaves` cannot be both True at the same time
    - `overriding` and `merge_attribute` cannot be both True at the same time

    Examples:
        >>> from bigtree import list_to_tree, str_to_tree, copy_nodes
        >>> root = list_to_tree(["Downloads/Pictures", "Downloads/photo1.jpg", "Downloads/file1.doc"])
        >>> root.show()
        Downloads
        ├── Pictures
        ├── photo1.jpg
        └── file1.doc

        >>> copy_nodes(
        ...     tree=root,
        ...     from_paths=["Downloads/photo1.jpg", "Downloads/file1.doc"],
        ...     to_paths=["Downloads/Pictures/photo1.jpg", "Downloads/Files/file1.doc"],
        ... )
        >>> root.show()
        Downloads
        ├── Pictures
        │   └── photo1.jpg
        ├── photo1.jpg
        ├── file1.doc
        └── Files
            └── file1.doc

        In overriding case,

        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── Misc\\n"
        ... "│   └── Pictures\\n"
        ... "│       └── photo1.jpg\\n"
        ... "└── Pictures\\n"
        ... "    └── photo2.jpg"
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        │   └── Pictures
        │       └── photo1.jpg
        └── Pictures
            └── photo2.jpg

        >>> copy_nodes(root, ["Downloads/Misc/Pictures"], ["Downloads/Pictures"], overriding=True)
        >>> root.show()
        Downloads
        ├── Misc
        │   └── Pictures
        │       └── photo1.jpg
        └── Pictures
            └── photo1.jpg

        In ``merge_children=True`` case, child nodes are copied instead of the parent node.

        - If the path already exists, child nodes are merged with existing children
        - Otherwise, the child nodes of the node are merged with the node's parent

        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── Misc\\n"
        ... "│   ├── Pictures\\n"
        ... "│   │   └── photo2.jpg\\n"
        ... "│   └── Applications\\n"
        ... "│       └── Chrome.exe\\n"
        ... "├── Pictures\\n"
        ... "│   └── photo1.jpg\\n"
        ... "└── dummy\\n"
        ... "    └── Files\\n"
        ... "        └── file1.doc"
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        │   ├── Pictures
        │   │   └── photo2.jpg
        │   └── Applications
        │       └── Chrome.exe
        ├── Pictures
        │   └── photo1.jpg
        └── dummy
            └── Files
                └── file1.doc

        >>> copy_nodes(
        ...     root,
        ...     ["Downloads/Misc/Pictures", "Applications", "Downloads/dummy"],
        ...     ["Downloads/Pictures", "Downloads/Applications", "Downloads/dummy"],
        ...     merge_children=True,
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        │   ├── Pictures
        │   │   └── photo2.jpg
        │   └── Applications
        │       └── Chrome.exe
        ├── Pictures
        │   ├── photo1.jpg
        │   └── photo2.jpg
        ├── Chrome.exe
        └── Files
            └── file1.doc

        In ``merge_leaves=True`` case, leaf nodes are copied instead of the parent node.

        - If the path already exists, leaf nodes are merged with existing children
        - Otherwise, the leaf nodes of the node are merged with the node's parent

        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── Misc\\n"
        ... "│   ├── Pictures\\n"
        ... "│   │   └── photo2.jpg\\n"
        ... "│   └── Applications\\n"
        ... "│       └── Chrome.exe\\n"
        ... "├── Pictures\\n"
        ... "│   └── photo1.jpg\\n"
        ... "└── dummy\\n"
        ... "    └── Files\\n"
        ... "        └── file1.doc"
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        │   ├── Pictures
        │   │   └── photo2.jpg
        │   └── Applications
        │       └── Chrome.exe
        ├── Pictures
        │   └── photo1.jpg
        └── dummy
            └── Files
                └── file1.doc

        >>> copy_nodes(
        ...     root,
        ...     ["Downloads/Misc/Pictures", "Applications", "Downloads/dummy"],
        ...     ["Downloads/Pictures", "Downloads/Applications", "Downloads/dummy"],
        ...     merge_leaves=True,
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        │   ├── Pictures
        │   │   └── photo2.jpg
        │   └── Applications
        │       └── Chrome.exe
        ├── Pictures
        │   ├── photo1.jpg
        │   └── photo2.jpg
        ├── dummy
        │   └── Files
        │       └── file1.doc
        ├── Chrome.exe
        └── file1.doc

        In ``delete_children=True`` case, only the node is copied without its accompanying children/descendants.

        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── Misc\\n"
        ... "│   └── Applications\\n"
        ... "│       └── Chrome.exe\\n"
        ... "└── Pictures\\n"
        ... "    └── photo1.jpg"
        ... )
        >>> root.show()
        Downloads
        ├── Misc
        │   └── Applications
        │       └── Chrome.exe
        └── Pictures
            └── photo1.jpg

        >>> copy_nodes(root, ["Applications"], ["Downloads/Applications"], delete_children=True)
        >>> root.show()
        Downloads
        ├── Misc
        │   └── Applications
        │       └── Chrome.exe
        ├── Pictures
        │   └── photo1.jpg
        └── Applications

    Args:
        tree: tree to modify
        from_paths: original paths to copy nodes from
        to_paths: new paths to copy nodes to
        sep: path separator for input paths, applies to `from_path` and `to_path`
        skippable: indicator to skip if from-path is not found
        overriding: indicator to override existing to-path if there are clashes
        merge_attribute: indicator to merge attributes of from-path and to-path if there are clashes
        merge_children: indicator to merge from-path's children and remove intermediate parent node
        merge_leaves: indicator to merge from-path's leaf nodes and remove intermediate parent node(s)
        delete_children: indicator to copy node only without children
        with_full_path: indicator to copy node with full path in `from_paths`, results in faster search
    """
    return copy_or_shift_logic(
        tree=tree,
        from_paths=from_paths,
        to_paths=to_paths,
        sep=sep,
        copy=True,
        skippable=skippable,
        overriding=overriding,
        merge_attribute=merge_attribute,
        merge_children=merge_children,
        merge_leaves=merge_leaves,
        delete_children=delete_children,
        to_tree=None,
        with_full_path=with_full_path,
    )  # pragma: no cover


def shift_and_replace_nodes(
    tree: T,
    from_paths: List[str],
    to_paths: List[str],
    sep: str = "/",
    skippable: bool = False,
    delete_children: bool = False,
    with_full_path: bool = False,
) -> None:
    """Shift nodes from `from_paths` to *replace* `to_paths` *in-place*.

    - Creates intermediate nodes if to-path is not present
    - Able to skip nodes if from-path is not found, defaults to False (from-nodes must be found; not skippable)
    - Able to shift node only and delete children, defaults to False (nodes are shifted together with children)

    For paths in `from_paths` and `to_paths`,

    - Path name can be with or without leading tree path separator symbol

    For paths in `from_paths`,

    - Path name can be partial path (trailing part of path) or node name
    - If ``with_full_path=True``, path name must be full path
    - Path name must be unique to one node

    For paths in `to_paths`,

    - Path name must be full path
    - Path must exist, node-to-be-replaced must be present

    Examples:
        >>> from bigtree import str_to_tree, shift_and_replace_nodes
        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── Pictures\\n"
        ... "│   └── photo1.jpg\\n"
        ... "└── Misc\\n"
        ... "    └── dummy"
        ... )
        >>> root.show()
        Downloads
        ├── Pictures
        │   └── photo1.jpg
        └── Misc
            └── dummy

        >>> shift_and_replace_nodes(root, ["Downloads/Pictures"], ["Downloads/Misc/dummy"])
        >>> root.show()
        Downloads
        └── Misc
            └── Pictures
                └── photo1.jpg

        In ``delete_children=True`` case, only the node is shifted without its accompanying children/descendants.

        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── Pictures\\n"
        ... "│   └── photo1.jpg\\n"
        ... "└── Misc\\n"
        ... "    └── dummy"
        ... )
        >>> root.show()
        Downloads
        ├── Pictures
        │   └── photo1.jpg
        └── Misc
            └── dummy

        >>> shift_and_replace_nodes(root, ["Downloads/Pictures"], ["Downloads/Misc/dummy"], delete_children=True)
        >>> root.show()
        Downloads
        └── Misc
            └── Pictures

    Args:
        tree: tree to modify
        from_paths: original paths to shift nodes from
        to_paths: new paths to shift nodes to
        sep: path separator for input paths, applies to `from_path` and `to_path`
        skippable: indicator to skip if from-path is not found
        delete_children: indicator to shift node only without children
        with_full_path: indicator to shift node with full path in `from_paths`, results in faster search
    """
    return replace_logic(
        tree=tree,
        from_paths=from_paths,
        to_paths=to_paths,
        sep=sep,
        copy=False,
        skippable=skippable,
        delete_children=delete_children,
        to_tree=None,
        with_full_path=with_full_path,
    )  # pragma: no cover


def copy_nodes_from_tree_to_tree(
    from_tree: T,
    to_tree: T,
    from_paths: List[str],
    to_paths: List[Optional[str]],
    sep: str = "/",
    skippable: bool = False,
    overriding: bool = False,
    merge_attribute: bool = False,
    merge_children: bool = False,
    merge_leaves: bool = False,
    delete_children: bool = False,
    with_full_path: bool = False,
) -> None:
    """Copy nodes from `from_paths` to `to_paths` *in-place*.

    - Creates intermediate nodes if to-path is not present
    - Able to skip nodes if from-path is not found, defaults to False (from-nodes must be found; not skippable)
    - Able to override existing node if it exists, defaults to False (to-nodes must not exist; not overridden)
    - Able to merge attributes of node if it exists, defaults to False (to-nodes must not exist; no attributes to merge)
    - Able to merge children and remove intermediate parent node, defaults to False (nodes are shifted; not merged)
    - Able to merge leaf nodes and remove all intermediate nodes, defaults to False (nodes are shifted; not merged)
    - Able to copy node only and delete children, defaults to False (nodes are copied together with children)

    For paths in `from_paths` and `to_paths`,

    - Path name can be with or without leading tree path separator symbol

    For paths in `from_paths`,

    - Path name can be partial path (trailing part of path) or node name
    - If ``with_full_path=True``, path name must be full path
    - Path name must be unique to one node

    For paths in `to_paths`,

    - Path name must be full path

    If ``merge_children=True``,

    - If `to_path` is not present, it copies children of `from_path`
    - If `to_path` is present, and ``overriding=False``, original and new children are merged
    - If `to_path` is present and ``overriding=True``, it behaves like overriding and only new children are retained

    If ``merge_leaves=True``,

    - If `to_path` is not present, it copies leaves of `from_path`
    - If `to_path` is present, and ``overriding=False``, original children and leaves are merged
    - If `to_path` is present and ``overriding=True``, it behaves like overriding and only new leaves are retained,
        original child nodes in `from_path` are retained

    Note:

    - `merge_children` and `merge_leaves` cannot be both True at the same time
    - `overriding` and `merge_attribute` cannot be both True at the same time

    Examples:
        >>> from bigtree import Node, str_to_tree, copy_nodes_from_tree_to_tree
        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── file1.doc\\n"
        ... "├── Pictures\\n"
        ... "│   └── photo1.jpg\\n"
        ... "└── Misc\\n"
        ... "    └── dummy\\n"
        ... "        └── photo2.jpg"
        ... )
        >>> root.show()
        Downloads
        ├── file1.doc
        ├── Pictures
        │   └── photo1.jpg
        └── Misc
            └── dummy
                └── photo2.jpg

        >>> root_other = Node("Documents")
        >>> copy_nodes_from_tree_to_tree(
        ...     from_tree=root,
        ...     to_tree=root_other,
        ...     from_paths=["Downloads/Pictures", "Downloads/Misc"],
        ...     to_paths=["Documents/Pictures", "Documents/New Misc/Misc"],
        ... )
        >>> root_other.show()
        Documents
        ├── Pictures
        │   └── photo1.jpg
        └── New Misc
            └── Misc
                └── dummy
                    └── photo2.jpg

        In overriding case,

        >>> root_other = str_to_tree(
        ... "Documents\\n"
        ... "└── Pictures\\n"
        ... "    └── photo3.jpg"
        ... )
        >>> root_other.show()
        Documents
        └── Pictures
            └── photo3.jpg

        >>> copy_nodes_from_tree_to_tree(
        ...     root,
        ...     root_other,
        ...     ["Downloads/Pictures", "Downloads/Misc"],
        ...     ["Documents/Pictures", "Documents/Misc"],
        ...     overriding=True,
        ... )
        >>> root_other.show()
        Documents
        ├── Pictures
        │   └── photo1.jpg
        └── Misc
            └── dummy
                └── photo2.jpg

        In ``merge_children=True`` case, child nodes are copied instead of the parent node.

        - If the path already exists, child nodes are merged with existing children
        - Otherwise, the child nodes of the node are merged with the node's parent

        >>> root_other = str_to_tree(
        ... "Documents\\n"
        ... "└── Pictures\\n"
        ... "    └── photo3.jpg"
        ... )
        >>> root_other.show()
        Documents
        └── Pictures
            └── photo3.jpg

        >>> copy_nodes_from_tree_to_tree(
        ...     root,
        ...     root_other,
        ...     ["Downloads/Pictures", "Downloads/Misc"],
        ...     ["Documents/Pictures", "Documents/Misc"],
        ...     merge_children=True,
        ... )
        >>> root_other.show()
        Documents
        ├── Pictures
        │   ├── photo3.jpg
        │   └── photo1.jpg
        └── dummy
            └── photo2.jpg

        In ``merge_leaves=True`` case, leaf nodes are copied instead of the parent node.

        - If the path already exists, leaf nodes are merged with existing children
        - Otherwise, the leaf nodes of the node are merged with the node's parent

        >>> root_other = str_to_tree(
        ... "Documents\\n"
        ... "└── Pictures\\n"
        ... "    └── photo3.jpg"
        ... )
        >>> root_other.show()
        Documents
        └── Pictures
            └── photo3.jpg

        >>> copy_nodes_from_tree_to_tree(
        ...     root,
        ...     root_other,
        ...     ["Downloads/Pictures", "Downloads/Misc"],
        ...     ["Documents/Pictures", "Documents/Misc"],
        ...     merge_leaves=True,
        ... )
        >>> root_other.show()
        Documents
        ├── Pictures
        │   ├── photo3.jpg
        │   └── photo1.jpg
        └── photo2.jpg

        In ``delete_children=True`` case, only the node is copied without its accompanying children/descendants.

        >>> root_other = Node("Documents")
        >>> root_other.show()
        Documents

        >>> copy_nodes_from_tree_to_tree(
        ...     root,
        ...     root_other,
        ...     ["Downloads/Pictures", "Downloads/Misc"],
        ...     ["Documents/Pictures", "Documents/Misc"],
        ...     delete_children=True,
        ... )
        >>> root_other.show()
        Documents
        ├── Pictures
        └── Misc

    Args:
        from_tree: tree to copy nodes from
        to_tree: tree to copy nodes to
        from_paths: original paths to copy nodes from
        to_paths: new paths to copy nodes to
        sep: path separator for input paths, applies to `from_path` and `to_path`
        skippable: indicator to skip if from path is not found
        overriding: indicator to override existing to path if there is clashes
        merge_attribute: indicator to merge attributes of from-path and to-path if there are clashes
        merge_children: indicator to merge from-path's children and remove intermediate parent node
        merge_leaves: indicator to merge from-path's leaf nodes and remove intermediate parent node(s)
        delete_children: indicator to copy node only without children
        with_full_path: indicator to copy node with full path in `from_paths`, results in faster search
    """
    return copy_or_shift_logic(
        tree=from_tree,
        from_paths=from_paths,
        to_paths=to_paths,
        sep=sep,
        copy=True,
        skippable=skippable,
        overriding=overriding,
        merge_attribute=merge_attribute,
        merge_children=merge_children,
        merge_leaves=merge_leaves,
        delete_children=delete_children,
        to_tree=to_tree,
        with_full_path=with_full_path,
    )  # pragma: no cover


def copy_and_replace_nodes_from_tree_to_tree(
    from_tree: T,
    to_tree: T,
    from_paths: List[str],
    to_paths: List[str],
    sep: str = "/",
    skippable: bool = False,
    delete_children: bool = False,
    with_full_path: bool = False,
) -> None:
    """Copy nodes from `from_paths` to *replace* `to_paths` *in-place*.

    - Creates intermediate nodes if to-path is not present
    - Able to skip nodes if from-path is not found, defaults to False (from-nodes must be found; not skippable)
    - Able to copy node only and delete children, defaults to False (nodes are copied together with children)

    For paths in `from_paths` and `to_paths`,

    - Path name can be with or without leading tree path separator symbol

    For paths in `from_paths`,

    - Path name can be partial path (trailing part of path) or node name
    - If ``with_full_path=True``, path name must be full path
    - Path name must be unique to one node

    For paths in `to_paths`,

    - Path name must be full path
    - Path must exist, node-to-be-replaced must be present

    Examples:
        >>> from bigtree import str_to_tree, copy_and_replace_nodes_from_tree_to_tree
        >>> root = str_to_tree(
        ... "Downloads\\n"
        ... "├── file1.doc\\n"
        ... "├── Pictures\\n"
        ... "│   └── photo1.jpg\\n"
        ... "└── Misc\\n"
        ... "    └── dummy\\n"
        ... "        └── photo2.jpg"
        ... )
        >>> root.show()
        Downloads
        ├── file1.doc
        ├── Pictures
        │   └── photo1.jpg
        └── Misc
            └── dummy
                └── photo2.jpg

        >>> root_other = str_to_tree(
        ... "Documents\\n"
        ... "├── Pictures2\\n"
        ... "│   └── photo2.jpg\\n"
        ... "└── Misc2"
        ... )
        >>> root_other.show()
        Documents
        ├── Pictures2
        │   └── photo2.jpg
        └── Misc2

        >>> copy_and_replace_nodes_from_tree_to_tree(
        ...     from_tree=root,
        ...     to_tree=root_other,
        ...     from_paths=["Downloads/Pictures", "Downloads/Misc"],
        ...     to_paths=["Documents/Pictures2/photo2.jpg", "Documents/Misc2"],
        ... )
        >>> root_other.show()
        Documents
        ├── Pictures2
        │   └── Pictures
        │       └── photo1.jpg
        └── Misc
            └── dummy
                └── photo2.jpg

        In ``delete_children=True`` case, only the node is copied without its accompanying children/descendants.

        >>> root_other = str_to_tree(
        ... "Documents\\n"
        ... "├── Pictures2\\n"
        ... "│   └── photo2.jpg\\n"
        ... "└── Misc2"
        ... )
        >>> root_other.show()
        Documents
        ├── Pictures2
        │   └── photo2.jpg
        └── Misc2

        >>> copy_and_replace_nodes_from_tree_to_tree(
        ...     from_tree=root,
        ...     to_tree=root_other,
        ...     from_paths=["Downloads/Pictures", "Downloads/Misc"],
        ...     to_paths=["Documents/Pictures2/photo2.jpg", "Documents/Misc2"],
        ...     delete_children=True,
        ... )
        >>> root_other.show()
        Documents
        ├── Pictures2
        │   └── Pictures
        └── Misc

    Args:
        from_tree: tree to copy nodes from
        to_tree: tree to copy nodes to
        from_paths: original paths to copy nodes from
        to_paths: new paths to copy nodes to
        sep: path separator for input paths, applies to `from_path` and `to_path`
        skippable: indicator to skip if from path is not found
        delete_children: indicator to copy node only without children
        with_full_path: indicator to copy node with full path in `from_paths`, results in faster search
    """
    return replace_logic(
        tree=from_tree,
        from_paths=from_paths,
        to_paths=to_paths,
        sep=sep,
        copy=True,
        skippable=skippable,
        delete_children=delete_children,
        to_tree=to_tree,
        with_full_path=with_full_path,
    )  # pragma: no cover


def _merge_attribute(
    from_node: T, to_node: T, copy: bool, merge_children: bool, merge_leaves: bool
) -> T:
    import pandas as pd

    from bigtree.tree import export

    if copy:
        from_node = from_node.copy()

    dummy_to_node = to_node.copy()
    dummy_to_node.parent = None
    to_node_data = export.tree_to_dataframe(dummy_to_node, all_attrs=True)

    dummy_from_node = from_node
    dummy_from_node.parent = None
    if merge_leaves:
        dummy_from_node.children = list(dummy_from_node.leaves)  # type: ignore
    from_node_data = export.tree_to_dataframe(dummy_from_node, all_attrs=True)

    common_attributes = set(to_node_data.columns).intersection(
        set(from_node_data.columns)
    ) - {"path", "name"}
    if merge_children or merge_leaves:
        merged_data = pd.merge(
            to_node_data,
            from_node_data,
            on=["path", "name"],
            how="outer",
            suffixes=("_x", "_y"),
        )
    else:
        merged_data = pd.merge(
            to_node_data,
            from_node_data,
            on=["path", "name"],
            how="left",
            suffixes=("_x", "_y"),
        )

    # Upsert data
    for common_attribute in common_attributes:
        merged_data[common_attribute] = merged_data[common_attribute + "_y"].fillna(
            merged_data[common_attribute + "_x"]
        )
        merged_data = merged_data.drop(
            columns=[
                common_attribute + "_x",
                common_attribute + "_y",
            ]
        )
    merged_data = merged_data.sort_values("path")
    return construct.dataframe_to_tree(merged_data)


def copy_or_shift_logic(
    tree: T,
    from_paths: List[str],
    to_paths: List[Optional[str]],
    sep: str = "/",
    copy: bool = False,
    skippable: bool = False,
    overriding: bool = False,
    merge_attribute: bool = False,
    merge_children: bool = False,
    merge_leaves: bool = False,
    delete_children: bool = False,
    to_tree: Optional[T] = None,
    with_full_path: bool = False,
) -> None:
    """Shift or copy nodes from `from_paths` to `to_paths` *in-place*.

    - Creates intermediate nodes if to-path is not present
    - Able to copy node, defaults to False (nodes are shifted; not copied)
    - Able to skip nodes if from-path is not found, defaults to False (from-nodes must be found; not skippable)
    - Able to override existing node if it exists, defaults to False (to-nodes must not exist; not overridden)
    - Able to merge attributes of node if it exists, defaults to False (to-nodes must not exist; no attributes to merge)
    - Able to merge children and remove intermediate parent node, defaults to False (nodes are shifted; not merged)
    - Able to merge only leaf nodes and remove all intermediate nodes, defaults to False (nodes are shifted; not merged)
    - Able to shift/copy node only and delete children, defaults to False (nodes are shifted/copied together with children)
    - Able to shift/copy nodes from one tree to another tree, defaults to None (shifting/copying happens within same tree)

    For paths in `from_paths` and `to_paths`,

    - Path name can be with or without leading tree path separator symbol

    For paths in `from_paths`,

    - Path name can be partial path (trailing part of path) or node name
    - If ``with_full_path=True``, path name must be full path
    - Path name must be unique to one node

    For paths in `to_paths`,

    - Path name must be full path
    - Can set to empty string or None to delete the path in `from_paths`, note that ``copy`` must be set to False

    If ``merge_children=True``,

    - If `to_path` is not present, it shifts/copies children of `from_path`
    - If `to_path` is present, and ``overriding=False``, original and new children are merged
    - If `to_path` is present and ``overriding=True``, it behaves like overriding and only new children are retained

    If ``merge_leaves=True``,

    - If `to_path` is not present, it shifts/copies leaves of `from_path`
    - If `to_path` is present, and ``overriding=False``, original children and leaves are merged
    - If `to_path` is present and ``overriding=True``, it behaves like overriding and only new leaves are retained,
        original child nodes in `from_path` are retained

    Note:

    - `merge_children` and `merge_leaves` cannot be both True at the same time
    - `overriding` and `merge_attribute` cannot be both True at the same time

    Args:
        tree: tree to modify
        from_paths: original paths to copy/shift nodes from
        to_paths: new paths to copy/shift nodes to
        sep: path separator for input paths, applies to `from_path` and `to_path`
        copy: indicator to copy node,
        skippable: indicator to skip if from-path is not found
        overriding: indicator to override existing to-path if there are clashes
        merge_attribute: indicator to merge attributes of from-path and to-path if there are clashes
        merge_children: indicator to merge from-path's children and remove intermediate parent node
        merge_leaves: indicator to merge from-path's leaf nodes and remove intermediate parent node(s)
        delete_children: indicator to copy/shift node only without children
        to_tree: tree to copy to
        with_full_path: indicator to copy/shift node with full path in `from_paths`, results in faster search
    """
    if merge_children and merge_leaves:
        raise ValueError(
            "Invalid shifting, can only specify one type of merging, check `merge_children` and `merge_leaves`"
        )
    if overriding and merge_attribute:
        raise ValueError(
            "Invalid shifting, can only specify one type of merging, check `overriding` and `merge_attribute`"
        )
    if not (isinstance(from_paths, list) and isinstance(to_paths, list)):
        raise ValueError(
            "Invalid type, `from_paths` and `to_paths` should be list type"
        )
    if len(from_paths) != len(to_paths):
        raise ValueError(
            f"Paths are different length, input `from_paths` have {len(from_paths)} entries, "
            f"while output `to_paths` have {len(to_paths)} entries"
        )
    if copy and (None in to_paths or "" in to_paths):
        raise ValueError(
            "Deletion of node will not happen if `copy=True`, check your `copy` parameter."
        )

    # Modify `sep` of from_paths and to_paths
    if not to_tree:
        to_tree = tree
    tree_sep = to_tree.sep
    from_paths = [path.rstrip(sep).replace(sep, tree.sep) for path in from_paths]
    to_paths = [
        path.rstrip(sep).replace(sep, tree_sep) if path else None for path in to_paths
    ]

    for from_path, to_path in zip(from_paths, to_paths):
        if to_path:
            if from_path.split(tree.sep)[-1] != to_path.split(tree_sep)[-1]:
                raise ValueError(
                    f"Unable to assign from_path {from_path} to to_path {to_path}\n"
                    f"Verify that `sep` is defined correctly for path\n"
                    f"Alternatively, check that `from_path` and `to_path` is reassigning the same node."
                )

    if with_full_path:
        if not all(
            [
                path.lstrip(tree.sep).split(tree.sep)[0] == tree.root.node_name
                for path in from_paths
            ]
        ):
            raise ValueError(
                "Invalid path in `from_paths` not starting with the root node. "
                "Check your `from_paths` parameter, alternatively set `with_full_path=False` to shift "
                "partial path instead of full path."
            )
    if not all(
        [
            path.lstrip(tree_sep).split(tree_sep)[0] == to_tree.root.node_name
            for path in to_paths
            if path
        ]
    ):
        raise ValueError(
            "Invalid path in `to_paths` not starting with the root node. Check your `to_paths` parameter."
        )

    # Perform shifting/copying
    for from_path, to_path in zip(from_paths, to_paths):
        if with_full_path:
            from_node = search.find_full_path(tree, from_path)
        else:
            from_node = search.find_path(tree, from_path)

        # From node not found
        if not from_node:
            if not skippable:
                raise exceptions.NotFoundError(
                    f"Unable to find from_path {from_path}\n"
                    f"Set `skippable` to True to skip shifting for nodes not found"
                )
            else:
                logging.info(f"Unable to find from_path {from_path}")

        # From node found
        else:
            # Node to be deleted
            if not to_path:
                to_node = None
            # Node to be copied/shifted
            else:
                to_node = search.find_full_path(to_tree, to_path)

                # To node found
                if to_node:
                    if from_node == to_node:
                        if merge_children:
                            parent = to_node.parent
                            to_node.parent = None
                            to_node = parent
                        elif merge_leaves:
                            to_node = to_node.parent
                        else:
                            raise exceptions.TreeError(
                                f"Attempting to shift the same node {from_node.node_name} back to the same position\n"
                                f"Check from path {from_path} and to path {to_path}\n"
                                f"Alternatively, set `merge_children` or `merge_leaves` to True if intermediate node is to be removed"
                            )
                    elif merge_children:
                        if overriding:
                            logging.info(
                                f"Path {to_path} already exists and its children be overridden by the merge"
                            )
                            del to_node.children
                        elif merge_attribute:
                            logging.info(
                                f"Path {to_path} already exists and their attributes will be merged"
                            )
                            from_node = _merge_attribute(
                                from_node,
                                to_node,
                                copy=copy,
                                merge_children=merge_children,
                                merge_leaves=merge_leaves,
                            )
                            to_node.set_attrs(
                                dict(from_node.describe(exclude_prefix="_"))
                            )
                            del to_node.children
                        else:
                            logging.info(
                                f"Path {to_path} already exists and children are merged"
                            )
                    elif merge_leaves:
                        if overriding:
                            logging.info(
                                f"Path {to_path} already exists and its leaves be overridden by the merge"
                            )
                            del to_node.children
                        elif merge_attribute:
                            logging.info(
                                f"Path {to_path} already exists and their attributes will be merged"
                            )
                            from_node = _merge_attribute(
                                from_node,
                                to_node,
                                copy=copy,
                                merge_children=merge_children,
                                merge_leaves=merge_leaves,
                            )
                            to_node.set_attrs(
                                dict(from_node.describe(exclude_prefix="_"))
                            )
                            del to_node.children
                        else:
                            logging.info(
                                f"Path {to_path} already exists and leaves are merged"
                            )
                    else:
                        if overriding:
                            logging.info(
                                f"Path {to_path} already exists and will be overridden"
                            )
                            parent = to_node.parent
                            to_node.parent = None
                            to_node = parent
                        elif merge_attribute:
                            logging.info(
                                f"Path {to_path} already exists and attributes will be upserted"
                            )
                            from_node = _merge_attribute(
                                from_node,
                                to_node,
                                copy=copy,
                                merge_children=merge_children,
                                merge_leaves=merge_leaves,
                            )
                            parent = to_node.parent
                            to_node.parent = None
                            to_node = parent
                        else:
                            raise exceptions.TreeError(
                                f"Path {to_path} already exists and unable to override\n"
                                f"Set `overriding` or `merge_attribute` to True to handle node name clashes\n"
                                f"Alternatively, set `merge_children` to True if nodes are to be merged"
                            )

                # To node not found
                else:
                    # Find parent node, create intermediate parent node if applicable
                    to_path_parent = tree_sep.join(to_path.split(tree_sep)[:-1])
                    to_node = construct.add_path_to_tree(
                        to_tree, to_path_parent, sep=tree_sep
                    )

            # Reassign from_node to new parent
            if copy:
                logging.debug(f"Copying {from_node.node_name}")
                from_node = from_node.copy()
            if merge_children:
                # overriding / merge_attribute handled merge_children, set merge_children=False
                logging.debug(
                    f"Reassigning children from {from_node.node_name} to {to_node.node_name}"
                )
                for children in from_node.children:
                    if delete_children:
                        del children.children
                    children.parent = to_node
                from_node.parent = None
            elif merge_leaves:
                logging.debug(
                    f"Reassigning leaf nodes from {from_node.node_name} to {to_node.node_name}"
                )
                for children in from_node.leaves:
                    children.parent = to_node
            else:
                if delete_children:
                    del from_node.children
                from_node.parent = to_node


def replace_logic(
    tree: T,
    from_paths: List[str],
    to_paths: List[str],
    sep: str = "/",
    copy: bool = False,
    skippable: bool = False,
    delete_children: bool = False,
    to_tree: Optional[T] = None,
    with_full_path: bool = False,
) -> None:
    """Shift or copy nodes from `from_paths` to *replace* `to_paths` *in-place*.

    - Creates intermediate nodes if to-path is not present
    - Able to copy node, defaults to False (nodes are shifted; not copied)
    - Able to skip nodes if from-path is not found, defaults to False (from-nodes must be found; not skippable)
    - Able to replace node only and delete children, defaults to False (nodes are shifted/copied together with children)
    - Able to shift/copy nodes from one tree to another tree, defaults to None (shifting/copying happens within same tree)

    For paths in `from_paths` and `to_paths`,

    - Path name can be with or without leading tree path separator symbol

    For paths in `from_paths`,

    - Path name can be partial path (trailing part of path) or node name
    - If ``with_full_path=True``, path name must be full path
    - Path name must be unique to one node

    For paths in `to_paths`,

    - Path name must be full path
    - Path must exist, node-to-be-replaced must be present

    Args:
        tree: tree to modify
        from_paths: original paths to copy/shift nodes from
        to_paths: new paths to copy/shift nodes to
        sep: path separator for input paths, applies to `from_path` and `to_path`
        copy: indicator to copy node
        skippable: indicator to skip if from-path is not found
        delete_children: indicator to copy/shift node only without children
        to_tree: tree to copy to
        with_full_path: indicator to copy/shift node with full path in `from_paths`, results in faster search
    """
    if not (isinstance(from_paths, list) and isinstance(to_paths, list)):
        raise ValueError(
            "Invalid type, `from_paths` and `to_paths` should be list type"
        )
    if len(from_paths) != len(to_paths):
        raise ValueError(
            f"Paths are different length, input `from_paths` have {len(from_paths)} entries, "
            f"while output `to_paths` have {len(to_paths)} entries"
        )

    # Modify `sep` of from_paths and to_paths
    if not to_tree:
        to_tree = tree
    tree_sep = to_tree.sep
    from_paths = [path.rstrip(sep).replace(sep, tree.sep) for path in from_paths]
    to_paths = [
        path.rstrip(sep).replace(sep, tree_sep) if path else None for path in to_paths
    ]

    if with_full_path:
        if not all(
            [
                path.lstrip(tree.sep).split(tree.sep)[0] == tree.root.node_name
                for path in from_paths
            ]
        ):
            raise ValueError(
                "Invalid path in `from_paths` not starting with the root node. Check your `from_paths` parameter, "
                "alternatively set `with_full_path=False` to shift partial path instead of full path."
            )
    if not all(
        [
            path.lstrip(tree_sep).split(tree_sep)[0] == to_tree.root.node_name
            for path in to_paths
            if path
        ]
    ):
        raise ValueError(
            "Invalid path in `to_paths` not starting with the root node. Check your `to_paths` parameter."
        )

    # Perform shifting/copying to replace destination node
    for from_path, to_path in zip(from_paths, to_paths):
        if with_full_path:
            from_node = search.find_full_path(tree, from_path)
        else:
            from_node = search.find_path(tree, from_path)

        # From node not found
        if not from_node:
            if not skippable:
                raise exceptions.NotFoundError(
                    f"Unable to find from_path {from_path}\nSet `skippable` to True to skip shifting for nodes not found"
                )
            else:
                logging.info(f"Unable to find from_path {from_path}")

        # From node found
        else:
            to_node = search.find_full_path(to_tree, to_path)

            # To node found
            if to_node:
                if from_node == to_node:
                    raise exceptions.TreeError(
                        f"Attempting to replace the same node {from_node.node_name}\nCheck from path {from_path} and to "
                        f"path {to_path}"
                    )

            # To node not found
            else:
                raise exceptions.NotFoundError(f"Unable to find to_path {to_path}")

            # Replace to_node with from_node
            if copy:
                logging.debug(f"Copying {from_node.node_name}")
                from_node = from_node.copy()
            if delete_children:
                del from_node.children
            parent = to_node.parent
            to_node_siblings = parent.children
            to_node_idx = to_node_siblings.index(to_node)
            for _node in to_node_siblings[to_node_idx:]:
                if _node == to_node:
                    to_node.parent = None
                    from_node.parent = parent
                else:
                    _node.parent = None
                    _node.parent = parent

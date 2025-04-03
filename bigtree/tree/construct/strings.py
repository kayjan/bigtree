from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar

from bigtree.node import node
from bigtree.tree import search
from bigtree.utils import assertions, constants, exceptions

__all__ = [
    "add_path_to_tree",
    "str_to_tree",
    "newick_to_tree",
]

T = TypeVar("T", bound=node.Node)


def add_path_to_tree(
    tree: T,
    path: str,
    sep: str = "/",
    duplicate_name_allowed: bool = True,
    node_attrs: Dict[str, Any] = {},
) -> T:
    """Add nodes and attributes to existing tree *in-place*, return node of path added. Adds to existing tree from list
    of path strings.

    Path should contain ``Node`` name, separated by `sep`.

    - For example: Path string "a/b" refers to Node("b") with parent Node("a")
    - Path separator `sep` is for the input `path` and can differ from existing tree

    Path can start from root node `name`, or start with `sep`.

    - For example: Path string can be "/a/b" or "a/b", if sep is "/"

    All paths should start from the same root node.

    - For example: Path strings should be "a/b", "a/c", "a/b/d" etc. and should not start with another root node

    All attributes in `node_attrs` will be added to the tree, including attributes with null values.

    Examples:
        >>> from bigtree import add_path_to_tree, Node
        >>> root = Node("a")
        >>> add_path_to_tree(root, "a/b/c")
        Node(/a/b/c, )
        >>> root.show()
        a
        └── b
            └── c

    Args:
        tree: existing tree
        path: path to be added to tree
        sep: path separator for input `path`
        duplicate_name_allowed: indicator if nodes with duplicate ``Node`` name is allowed
        node_attrs: attributes to add to node, key: attribute name, value: attribute value

    Returns:
        Node
    """
    assertions.assert_length_not_empty(path, "Path", "path")

    root_node = tree.root
    tree_sep = root_node.sep
    node_type = root_node.__class__
    branch = path.lstrip(sep).rstrip(sep).split(sep)
    if branch[0] != root_node.node_name:
        raise exceptions.TreeError(
            f"Path does not have same root node, expected {root_node.node_name}, received {branch[0]}\n"
            f"Check your input paths or verify that path separator `sep` is set correctly"
        )

    # Grow tree
    _node = root_node
    parent_node = root_node
    for idx in range(1, len(branch)):
        node_name = branch[idx]
        node_path = tree_sep.join(branch[: idx + 1])
        if not duplicate_name_allowed:
            _node = search.find_name(root_node, node_name)
            if _node and not _node.path_name.endswith(node_path):
                raise exceptions.DuplicatedNodeError(
                    f"Node {node_name} already exists, try setting `duplicate_name_allowed` to True "
                    f"to allow `Node` with same node name"
                )
        else:
            _node = search.find_child_by_name(parent_node, node_name)
        if not _node:
            if idx == len(branch) - 1:
                _node = node_type(node_name, **node_attrs)
            else:
                _node = node_type(node_name)
            _node.parent = parent_node
        parent_node = _node
    _node.set_attrs(node_attrs)
    return _node


def str_to_tree(
    tree_string: str,
    tree_prefix_list: List[str] = [],
    node_type: Type[T] = node.Node,  # type: ignore[assignment]
) -> T:
    r"""Construct tree from tree string.

    Examples:
        >>> from bigtree import str_to_tree
        >>> tree_str = 'a\n├── b\n│   ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f'
        >>> root = str_to_tree(tree_str, tree_prefix_list=["├──", "└──"])
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        │       ├── g
        │       └── h
        └── c
            └── f

    Args:
        tree_string: String to construct tree
        tree_prefix_list: List of prefix to mark the end of tree branch/stem and start of node name, optional. If not
            specified, it will infer unicode characters and whitespace as prefix
        node_type: node type of tree to be created

    Returns:
        Node
    """
    tree_string = tree_string.strip("\n")
    assertions.assert_length_not_empty(tree_string, "Tree string", "tree_string")
    tree_list = tree_string.split("\n")
    root_node = node_type(tree_list[0])

    # Infer prefix length
    prefix_length = None
    cur_parent = root_node
    for node_str in tree_list[1:]:
        if len(tree_prefix_list):
            node_name = re.split("|".join(tree_prefix_list), node_str)[-1].lstrip()
        else:
            node_name = node_str.encode("ascii", "ignore").decode("ascii").lstrip()

        # Find node parent
        if not prefix_length:
            prefix_length = node_str.index(node_name)
            if not prefix_length:
                raise ValueError(
                    f"Invalid prefix, prefix should be unicode character or whitespace, "
                    f"otherwise specify one or more prefixes in `tree_prefix_list`, check: {node_str}"
                )
        node_prefix_length = node_str.index(node_name)
        if node_prefix_length % prefix_length:
            raise ValueError(
                f"Tree string have different prefix length, check branch: {node_str}"
            )
        while cur_parent.depth > node_prefix_length / prefix_length:
            cur_parent = cur_parent.parent

        # Link node
        child_node = node_type(node_name)
        child_node.parent = cur_parent
        cur_parent = child_node

    return root_node


def newick_to_tree(
    tree_string: str,
    length_attr: str = "length",
    attr_prefix: str = "&&NHX:",
    node_type: Type[T] = node.Node,  # type: ignore[assignment]
) -> T:
    """Construct tree from Newick notation, return root of tree.

    In the Newick Notation (or New Hampshire Notation)

    - Tree is represented in round brackets i.e., `(child1,child2,child3)parent`
    - If there are nested trees, they will be in nested round brackets i.e., `((grandchild1)child1,(grandchild2,grandchild3)child2)parent`
    - If there is length attribute, they will be beside the name i.e., `(child1:0.5,child2:0.1)parent`
    - If there are other attributes, attributes are represented in square brackets i.e., `(child1:0.5[S:human],child2:0.1[S:human])parent[S:parent]`

    Variations supported

    - Support special characters (`[`, `]`, `(`, `)`, `:`, `,`) in node name, attribute name, and attribute values if
        they are enclosed in single quotes i.e., '(name:!)'
    - If there are no node names, it will be auto-filled with convention `nodeN` with N representing a number

    Examples:
        >>> from bigtree import newick_to_tree
        >>> root = newick_to_tree("((d,e)b,c)a")
        >>> root.show()
        a
        ├── b
        │   ├── d
        │   └── e
        └── c

        >>> root = newick_to_tree("((d:40,e:35)b:65,c:60)a", length_attr="age")
        >>> root.show(attr_list=["age"])
        a
        ├── b [age=65]
        │   ├── d [age=40]
        │   └── e [age=35]
        └── c [age=60]

        >>> root = newick_to_tree(
        ...     "((d:40[&&NHX:species=human],e:35[&&NHX:species=human])b:65[&&NHX:species=human],c:60[&&NHX:species=human])a[&&NHX:species=human]",
        ...     length_attr="age",
        ... )
        >>> root.show(all_attrs=True)
        a [species=human]
        ├── b [age=65, species=human]
        │   ├── d [age=40, species=human]
        │   └── e [age=35, species=human]
        └── c [age=60, species=human]

    Args:
        tree_string: Newick notation to construct tree
        length_attr: attribute name to store node length, optional
        attr_prefix: prefix before all attributes, within square bracket, used to detect attributes
        node_type: node type of tree to be created

    Returns:
        Node
    """
    assertions.assert_length_not_empty(tree_string, "Tree string", "tree_string")

    # Store results (for tracking)
    depth_nodes: Dict[int, List[T]] = defaultdict(list)
    unlabelled_node_counter: int = 0
    current_depth: int = 1
    tree_string_idx: int = 0

    # Store states (for assertions and checks)
    current_state: constants.NewickState = constants.NewickState.PARSE_STRING
    current_node: Optional[T] = None
    cumulative_string: str = ""
    cumulative_string_value: str = ""

    def _create_node(
        _new_node: Optional[T],
        _cumulative_string: str,
        _unlabelled_node_counter: int,
        _depth_nodes: Dict[int, List[T]],
        _current_depth: int,
    ) -> Tuple[T, int]:
        """Create node at checkpoint.

        Args:
            _new_node: existing node (to add length attribute), or nothing (to create a node)
            _cumulative_string: cumulative string, contains either node name or length attribute
            _unlabelled_node_counter: number of unlabelled nodes, updates and returns counter
            _depth_nodes: list of nodes at each depth
            _current_depth: depth of current node or node to be created

        Returns:
            Node and the current depth of node
        """
        if not _new_node:
            if not _cumulative_string:
                _cumulative_string = f"node{_unlabelled_node_counter}"
                _unlabelled_node_counter += 1
            _new_node = node_type(_cumulative_string)
            _depth_nodes[_current_depth].append(_new_node)
        elif _cumulative_string:
            _new_node.set_attrs(
                {
                    length_attr: (
                        int(_cumulative_string)
                        if _cumulative_string.isdigit()
                        else float(_cumulative_string)
                    )
                }
            )

        if len(_depth_nodes[_current_depth + 1]):
            _new_node.children = depth_nodes[_current_depth + 1]  # type: ignore
            del _depth_nodes[_current_depth + 1]
        return _new_node, _unlabelled_node_counter

    def _raise_value_error(tree_idx: int) -> None:
        """Raise value error.

        Raises:
            ValueError
        """
        raise ValueError(
            f"String not properly closed, check `tree_string` at index {tree_idx}"
        )

    while tree_string_idx < len(tree_string):
        character = tree_string[tree_string_idx]
        if character == constants.NewickCharacter.OPEN_BRACKET:
            # Check and/or change state
            state_title = "Node creation start"
            if current_state not in [constants.NewickState.PARSE_STRING]:
                _raise_value_error(tree_string_idx)
            # Logic
            current_depth += 1
            if current_node:
                _raise_value_error(tree_string_idx)
            if cumulative_string:
                _raise_value_error(tree_string_idx)
            assert (
                not cumulative_string_value
            ), f"{state_title}, should not have cumulative_string_value"
            tree_string_idx += 1
            continue

        if character in [
            constants.NewickCharacter.CLOSE_BRACKET,
            constants.NewickCharacter.ATTR_START,
            constants.NewickCharacter.NODE_SEP,
        ]:
            # Check and/or change state
            state_title = "Node creation end / Node attribute start"
            if current_state not in [
                constants.NewickState.PARSE_STRING,
                constants.NewickState.PARSE_ATTRIBUTE_NAME,
            ]:
                _raise_value_error(tree_string_idx)
            # Logic
            if character == constants.NewickCharacter.ATTR_START:
                current_state = constants.NewickState.PARSE_ATTRIBUTE_NAME
                if tree_string[tree_string_idx + 1 :].startswith(  # noqa: E203
                    attr_prefix
                ):
                    tree_string_idx += len(attr_prefix)
            current_node, unlabelled_node_counter = _create_node(
                current_node,
                cumulative_string,
                unlabelled_node_counter,
                depth_nodes,
                current_depth,
            )
            if character == constants.NewickCharacter.CLOSE_BRACKET:
                current_depth -= 1
                current_node = None
            if character == constants.NewickCharacter.NODE_SEP:
                current_node = None
            cumulative_string = ""
            assert (
                not cumulative_string_value
            ), f"{state_title}, should not have cumulative_string_value"
            tree_string_idx += 1
            continue

        if character == constants.NewickCharacter.ATTR_END:
            # Check and/or change state
            state_title = "Node attribute end"
            if current_state not in [constants.NewickState.PARSE_ATTRIBUTE_VALUE]:
                _raise_value_error(tree_string_idx)
            current_state = constants.NewickState.PARSE_STRING
            # Logic
            assert current_node, f"{state_title}, should have current_node"
            current_node.set_attrs({cumulative_string: cumulative_string_value})
            cumulative_string = ""
            cumulative_string_value = ""
            tree_string_idx += 1
            continue

        if character == constants.NewickCharacter.ATTR_KEY_VALUE:
            # Check and/or change state
            state_title = "Node attribute creation"
            if current_state not in [constants.NewickState.PARSE_ATTRIBUTE_NAME]:
                _raise_value_error(tree_string_idx)
            current_state = constants.NewickState.PARSE_ATTRIBUTE_VALUE
            # Logic
            assert current_node, f"{state_title}, should have current_node"
            if not cumulative_string:
                _raise_value_error(tree_string_idx)
            assert (
                not cumulative_string_value
            ), f"{state_title}, should not have cumulative_string_value"
            tree_string_idx += 1
            continue

        if character == constants.NewickCharacter.ATTR_QUOTE:
            # Logic
            quote_end_idx = tree_string.find(
                constants.NewickCharacter.ATTR_QUOTE, tree_string_idx + 1
            )
            if quote_end_idx == -1:
                _raise_value_error(tree_string_idx)
            if current_state in [
                constants.NewickState.PARSE_STRING,
                constants.NewickState.PARSE_ATTRIBUTE_NAME,
            ]:
                if cumulative_string:
                    _raise_value_error(tree_string_idx)
                cumulative_string = tree_string[
                    tree_string_idx + 1 : quote_end_idx  # noqa: E203
                ]
            else:
                if cumulative_string_value:
                    _raise_value_error(tree_string_idx)
                cumulative_string_value = tree_string[
                    tree_string_idx + 1 : quote_end_idx  # noqa: E203
                ]
            tree_string_idx = quote_end_idx + 1
            continue

        if character == constants.NewickCharacter.SEP:
            # Check and/or change state
            state_title = "Node length creation / Node attribute creation"
            if current_state not in [
                constants.NewickState.PARSE_STRING,
                constants.NewickState.PARSE_ATTRIBUTE_VALUE,
            ]:
                _raise_value_error(tree_string_idx)
            # Logic
            if current_state == constants.NewickState.PARSE_STRING:
                if current_node:
                    _raise_value_error(tree_string_idx)
                current_node, unlabelled_node_counter = _create_node(
                    current_node,
                    cumulative_string,
                    unlabelled_node_counter,
                    depth_nodes,
                    current_depth,
                )
                cumulative_string = ""
                assert (
                    not cumulative_string_value
                ), f"{state_title}, should not have cumulative_string_value"
                tree_string_idx += 1
                continue
            else:
                current_state = constants.NewickState.PARSE_ATTRIBUTE_NAME
                assert current_node, f"{state_title}, should not have current_node"
                current_node.set_attrs({cumulative_string: cumulative_string_value})
                cumulative_string = ""
                cumulative_string_value = ""
                tree_string_idx += 1
                continue

        if current_state == constants.NewickState.PARSE_ATTRIBUTE_VALUE:
            cumulative_string_value += character
        else:
            cumulative_string += character
        tree_string_idx += 1

    if current_depth != 1:
        _raise_value_error(tree_string_idx)

    # Final root node
    if len(depth_nodes[current_depth]):
        current_node = depth_nodes[current_depth][0]
    current_node, unlabelled_node_counter = _create_node(
        current_node,
        cumulative_string,
        unlabelled_node_counter,
        depth_nodes,
        current_depth,
    )
    return current_node

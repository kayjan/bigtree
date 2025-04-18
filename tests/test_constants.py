from dataclasses import dataclass


@dataclass
class Constants:
    """
    Constants and error messages sorted by segments, organized in order of,
    1. Exact match for error messages
    2. Partial match for error messages (startswith/endswith) - minimize if possible
    3. Error message to throw should assertion fail
    """

    LOCAL = False

    # binarytree/construct
    ERROR_BINARY_DAG_LIST_EMPTY = (
        "Input list does not contain any data, check `{parameter}`"
    )

    ERROR_CUSTOM_TYPE = "Node type is not `{type}`"

    # dag/construct
    ERROR_DAG_DICT_INVALID_KEY = "Invalid input, check `{parameter}` is not a valid key as it is a reserved keyword"
    ERROR_DAG_DICT_PARENT_KEY = "Parent key {parent_key} not in dictionary, check `relation_attrs` and `parent_key`"
    ERROR_DAG_DATAFRAME_EMPTY_CHILD = (
        "Child name cannot be empty, check column: {child_col}"
    )
    ERROR_DAG_DATAFRAME_PARENT_COL = (
        "Parent column not in data, check `parent_col`: {parent_col}"
    )
    ERROR_DAG_DATAFRAME_CHILD_COL = (
        "Child column not in data, check `child_col`: {child_col}"
    )

    ERROR_DAG_DATAFRAME_DUPLICATE_PARENT = (
        "There exists duplicate child name with different attributes\nCheck "
    )

    # node/basenode
    ERROR_NODE_CHILDREN_TYPE = (
        "Expect children to be {type} type, received input type {input_type}"
    )
    ERROR_NODE_CHILDREN_TYPE_NONE = "Expect children to be {type} type or NoneType, received input type {input_type}"
    ERROR_NODE_PARENT_TYPE = (
        "Expect parent to be {type} type, received input type {input_type}"
    )
    ERROR_NODE_PARENT_TYPE_NONE = (
        "Expect parent to be {type} type or NoneType, received input type {input_type}"
    )
    ERROR_NODE_SET_PARENTS_ATTR = (
        "Attempting to set `parents` attribute, do you mean `parent`?"
    )
    ERROR_NODE_GET_PARENTS_ATTR = (
        "Attempting to access `parents` attribute, do you mean `parent`?"
    )
    ERROR_NODE_LOOP_PARENT = "Error setting parent: Node cannot be parent of itself"
    ERROR_NODE_LOOP_ANCESTOR = "Error setting parent: Node cannot be ancestor of itself"
    ERROR_NODE_LOOP_CHILD = "Error setting child: Node cannot be child of itself"
    ERROR_NODE_LOOP_DESCENDANT = (
        "Error setting child: Node cannot be ancestor of itself"
    )
    ERROR_NODE_DUPLICATE_PARENT = (
        "Error setting parent: Node cannot be added multiple times as a parent"
    )
    ERROR_NODE_DUPLICATE_CHILD = (
        "Error setting child: Node cannot be added multiple times as a child"
    )

    # node/binarynode
    ERROR_BINARYNODE_CHILDREN_LENGTH = "Children input must have length 2"
    ERROR_BINARYNODE_LEFT_CHILDREN = "Error setting child: Attempting to set both left and children with mismatched values\nCheck left {left} and children {children}"
    ERROR_BINARYNODE_RIGHT_CHILDREN = "Error setting child: Attempting to set both right and children with mismatched values\nCheck right {right} and children {children}"

    # node/dagnode
    ERROR_NODE_SET_PARENT_ATTR = (
        "Attempting to set `parent` attribute, do you mean `parents`?"
    )
    ERROR_NODE_GET_PARENT_ATTR = (
        "Attempting to access `parent` attribute, do you mean `parents`?"
    )
    ERROR_NODE_GOTO = "It is not possible to go to {node}"
    ERROR_NODE_GOTO_TYPE = (
        "Expect node to be {type} type, received input type {input_type}"
    )
    ERROR_NODE_GOTO_SAME_TREE = "Nodes are not from the same tree. Check {a} and {b}"
    ERROR_DAGNODE_PARENTS_TYPE = (
        "Parents input should be list type, received input type {input_type}"
    )

    # node/node
    ERROR_NODE_NAME = "Node must have a `name` attribute"
    ERROR_NODE_SAME_PARENT_PATH = (
        "Duplicate node with same path\nThere exist a node with same path {path}"
    )
    ERROR_NODE_SAME_CHILDREN_PATH = (
        "Duplicate node with same path\nAttempting to add nodes with same path {path}"
    )

    # tree/construct
    ERROR_NODE_DATAFRAME_EMPTY_ROW = "Data does not contain any rows, check `data`"
    ERROR_NODE_DATAFRAME_EMPTY_COL = "Data does not contain any columns, check `data`"
    ERROR_NODE_DATAFRAME_MULTIPLE_ROOT = (
        "Unable to determine root node\nPossible root nodes: {root_nodes}"
    )
    ERROR_NODE_DICT_EMPTY = "Dictionary does not contain any data, check `{parameter}`"
    ERROR_NODE_DICT_CHILD_TYPE = (
        "child_key {child_key} should be List type, received {child}"
    )
    ERROR_NODE_LIST_EMPTY = "Path list does not contain any data, check `{parameter}`"
    ERROR_NODE_PATH_EMPTY = "Path does not contain any data, check `path`"
    ERROR_NODE_STRING_EMPTY = (
        "Tree string does not contain any data, check `tree_string`"
    )
    ERROR_NODE_STRING_PREFIX = "Invalid prefix, prefix should be unicode character or whitespace, otherwise specify one or more prefixes in `tree_prefix_list`, check: {node_str}"
    ERROR_NODE_STRING_PREFIX_LENGTH = (
        "Tree string have different prefix length, check branch: {branch}"
    )
    ERROR_NODE_JOIN_TYPE = "`join_type` must be one of 'inner' or 'left'"
    ERROR_NODE_DIFFERENT_ROOT = (
        "Path does not have same root node, expected {root1}, received {root2}\n"
        "Check your input paths or verify that path separator `sep` is set correctly"
    )
    ERROR_NODE_DUPLICATE_NAME = "Node {name} already exists, try setting `duplicate_name_allowed` to True to allow `Node` with same node name"
    ERROR_NODE_NEWICK_NOT_CLOSED = (
        "String not properly closed, check `tree_string` at index {index}"
    )

    ERROR_NODE_DATAFRAME_DUPLICATE_NAME = (
        "There exists duplicate name with different attributes\nCheck "
    )
    ERROR_NODE_DATAFRAME_DUPLICATE_PATH = (
        "There exists duplicate path with different attributes\nCheck "
    )
    ERROR_NODE_DUPLICATED_INTERMEDIATE_NODE = "There exists duplicate child with different parent where the child is also a parent node.\nDuplicated node names should not happen, but can only exist in leaf nodes to avoid confusion.\nCheck "

    # tree/export
    ERROR_NODE_TYPE = "Tree should be of type `{type}`, or inherit from `{type}`"
    ERROR_NODE_EXPORT_PRINT_ATTR_BRACKET = (
        "Expect open and close brackets in `attr_bracket`, received {attr_bracket}"
    )
    ERROR_NODE_EXPORT_PRINT_STYLE_SELECT = (
        "Please specify the style of 3 icons in `style`"
    )
    ERROR_NODE_EXPORT_HPRINT_STYLE_SELECT = (
        "Please specify the style of 7 icons in `style`"
    )
    ERROR_NODE_EXPORT_BORDER_STYLE_SELECT = (
        "Please specify the style of 6 icons in `border_style`"
    )
    ERROR_NODE_EXPORT_PRINT_CUSTOM_STYLE_DIFFERENT_LENGTH = (
        "`stem`, `branch`, and `stem_final` are of different length"
    )
    ERROR_NODE_EXPORT_HPRINT_CUSTOM_STYLE_DIFFERENT_LENGTH = (
        "All style icons must have length 1"
    )
    ERROR_NODE_EXPORT_PRINT_INVALID_PATH = (
        "Node name or path {node_name_or_path} not found"
    )
    ERROR_NODE_EXPORT_PILLOW_FONT_FAMILY = "Font file {font_family} is not found, set `font_family` parameter to point to a valid .ttf file."
    ERROR_NODE_EXPORT_PILLOW_CMAP = (
        "`rect_cmap_attr` cannot be None if rect_fill is mpl.colormaps"
    )
    ERROR_NODE_MERMAID_INVALID_STYLE = "Unable to construct style!"

    ERROR_NODE_EXPORT_PRINT_INVALID_STYLE = "Choose one of "
    ERROR_NODE_MERMAID_INVALID_ARGUMENT = (
        "Invalid input, check `{parameter}` should be one of "
    )
    ERROR_NODE_NEWICK_ATTR_INVALID = "Length attribute does not exist for node "

    # tree/helper
    ERROR_NODE_PRUNE_ARGUMENT = (
        "Please specify either `prune_path` or `max_depth` or both."
    )
    ERROR_NODE_PRUNE_NOT_FOUND = (
        "Cannot find any node matching path_name ending with {prune_path}"
    )
    ERROR_NODE_TREE_DIFF_DIFF_SEP = "`sep` must be the same for tree and other_tree"

    # tree/modify
    ERROR_MODIFY_PARAM_TYPE = (
        "Invalid type, `from_paths` and `to_paths` should be list type"
    )
    ERROR_MODIFY_PARAM_DIFFERENT_PATH_LENGTH = (
        "Paths are different length, input `from_paths` have {n1} entries, "
        "while output `to_paths` have {n2} entries"
    )
    ERROR_MODIFY_PARAM_OVERRIDING_OR_MERGE_ATTRIBUTE = "Invalid shifting, can only specify one type of merging, check `overriding` and `merge_attribute`"
    ERROR_MODIFY_PARAM_MERGE_CHILDREN_OR_LEAVES = "Invalid shifting, can only specify one type of merging, check `merge_children` and `merge_leaves`"
    ERROR_MODIFY_PARAM_DELETE_AND_COPY = (
        "Deletion of node will not happen if `copy=True`, check your `copy` parameter."
    )
    ERROR_MODIFY_FROM_PATH_NOT_FOUND = (
        "Unable to find from_path {from_path}\n"
        "Set `skippable` to True to skip shifting for nodes not found"
    )
    ERROR_MODIFY_TO_PATH_NOT_FOUND = "Unable to find to_path {to_path}"
    ERROR_MODIFY_INVALID_TO_PATH = "Invalid path in `to_paths` not starting with the root node. Check your `to_paths` parameter."
    ERROR_MODIFY_INVALID_FULL_PATH = (
        "Invalid path in `from_paths` not starting with the root node. "
        "Check your `from_paths` parameter, alternatively set `with_full_path=False` to shift "
        "partial path instead of full path."
    )
    ERROR_MODIFY_OVERRIDING = (
        "Path {to_path} already exists and unable to override\n"
        "Set `overriding` or `merge_attribute` to True to handle node name clashes\n"
        "Alternatively, set `merge_children` to True if nodes are to be merged"
    )

    ERROR_MODIFY_PATH_MISMATCH = "Unable to assign from_path "
    ERROR_MODIFY_SHIFT_SAME_NODE = "Attempting to shift the same node "
    ERROR_MODIFY_REPLACE_SAME_NODE = "Attempting to replace the same node "

    # tree/search
    ERROR_SEARCH_RELATIVE_INVALID_PATH = (
        "Invalid path name. Path goes beyond root node."
    )
    ERROR_SEARCH_RELATIVE_INVALID_NODE = (
        "Invalid path name. Node {component} cannot be found."
    )
    ERROR_SEARCH_FULL_PATH_INVALID_ROOT = (
        "Path {path_name} does not match the root node name {root_name}"
    )

    ERROR_SEARCH_LESS_THAN_N_ELEMENT = (
        "Expected less than or equal to {count} element(s), found "
    )
    ERROR_SEARCH_MORE_THAN_N_ELEMENT = (
        "Expected more than or equal to {count} element(s), found "
    )

    # tree/utils
    ERROR_PLOT = (
        "No x or y coordinates detected. "
        "Please run reingold_tilford algorithm to retrieve coordinates."
    )

    # workflow/todo
    ERROR_WORKFLOW_TODO_TYPE = "Invalid data type for item"

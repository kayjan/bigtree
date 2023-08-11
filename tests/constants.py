from dataclasses import dataclass


@dataclass
class Constants:
    LOCAL = False

    # binarytree/construct
    ERROR_BINARY_EMPTY_LIST = "Input list does not contain any data, check"
    ERROR_BINARY_NODE_TYPE = "Node type is not `BinaryNodeA`"

    # dag/construct
    ERROR_DAG_EMPTY_LIST = "Input list does not contain any data, check"
    ERROR_DAG_EMPTY_DICT = (
        "Dictionary does not contain any data, check `relation_attrs`"
    )
    ERROR_DAG_PARENT_KEY = (
        "Parent key parent not in dictionary, check `relation_attrs` and `parent_key`"
    )
    ERROR_DAG_PARENT_COL = "Parent column not in data, check `parent_col`"
    ERROR_DAG_CHILD_COL = "Child column not in data, check `child_col`"
    ERROR_DAG_ATTRIBUTE_COL = (
        "One or more attribute column(s) not in data, check `attribute_col`"
    )

    ERROR_DAG_EMPTY_CHILD = "Child name cannot be empty"
    ERROR_DAG_DUPLICATE_PARENT = (
        "There exists duplicate child name with different attributes"
    )
    ERROR_DAG_NODE_TYPE = "Node type is not `DAGNodeA`"

    # dag/export
    ERROR_DAG_TYPE = "Tree should be of type `DAGNode`, or inherit from `DAGNode`"

    # node/basenode
    ERROR_SET_PARENTS_ATTR = (
        "Attempting to set `parents` attribute, do you mean `parent`?"
    )
    ERROR_GET_PARENTS_ATTR = (
        "Attempting to access `parents` attribute, do you mean `parent`?"
    )
    ERROR_LOOP_PARENT = "Error setting parent: Node cannot be parent of itself"
    ERROR_LOOP_ANCESTOR = "Error setting parent: Node cannot be ancestor of itself"
    ERROR_LOOP_CHILD = "Error setting child: Node cannot be child of itself"
    ERROR_LOOP_DESCENDANT = "Error setting child: Node cannot be ancestor of itself"
    ERROR_SET_DUPLICATE_CHILD = (
        "Error setting child: Node cannot be added multiple times as a child"
    )
    ERROR_SET_DUPLICATE_PARENT = (
        "Error setting parent: Node cannot be added multiple times as a parent"
    )

    ERROR_CHILDREN_TYPE = "Children input should be Iterable type, received input type"
    ERROR_BASENODE_CHILDREN_TYPE = (
        "Expect input to be BaseNode type, received input type"
    )
    ERROR_BASENODE_PARENT_TYPE = (
        "Expect input to be BaseNode type or NoneType, received input type"
    )

    # node/binarynode
    ERROR_BINARYNODE_CHILDREN_LENGTH = "Children input must have length 2"

    ERROR_SET_LEFT_CHILDREN = (
        "Attempting to set both left and children with mismatched values"
    )
    ERROR_SET_RIGHT_CHILDREN = (
        "Attempting to set both right and children with mismatched values"
    )
    ERROR_BINARYNODE_TYPE = (
        "Expect input to be BinaryNode type or NoneType, received input type"
    )

    # node/dagnode
    ERROR_SET_PARENT_ATTR = (
        "Attempting to set `parent` attribute, do you mean `parents`?"
    )
    ERROR_GET_PARENT_ATTR = (
        "Attempting to access `parent` attribute, do you mean `parents`?"
    )

    ERROR_DAGNODE_PARENT_TYPE = "Parents input should be list type, received input type"
    ERROR_DAGNODE_TYPE = "Expect input to be DAGNode type, received input type"

    # node/node
    ERROR_NODE_NAME = "Node must have a `name` attribute"

    ERROR_SAME_PATH = "Duplicate node with same path"

    # tree/construct
    ERROR_EMPTY_PATH = "Path is empty, check `path`"
    ERROR_EMPTY_ROW = "Data does not contain any rows, check `data`"
    ERROR_EMPTY_COL = "Data does not contain any columns, check `data`"
    ERROR_EMPTY_STRING = "Tree string does not contain any data, check `tree_string`"

    ERROR_EMPTY_CHILD = "child_key children should be List type, received "
    ERROR_EMPTY_DICT = "Dictionary does not contain any data, check"
    ERROR_EMPTY_LIST = "Path list does not contain any data, check"
    ERROR_DIFFERENT_ROOT = "Path does not have same root node"
    ERROR_MULTIPLE_ROOT = "Unable to determine root node"
    ERROR_DUPLICATE_PATH = "There exists duplicate path with different attributes"
    ERROR_DUPLICATE_NAME = "There exists duplicate name with different attributes"
    ERROR_DUPLICATE_PARENT = "There exists duplicate child with different parent where the child is also a parent node"
    ERROR_NODE_TYPE = "Node type is not `NodeA`"
    ERROR_CUSTOM_NODE_TYPE = "Node type is not `CustomNode`"
    ERROR_PREFIX = "Invalid prefix, prefix should be unicode character or whitespace, otherwise specify one or more prefixes"
    ERROR_PREFIX_LENGTH = "Tree string have different prefix length, check branch"
    ERROR_JOIN_TYPE = "`join_type` must be one of 'inner' or 'left'"

    # tree/export
    ERROR_EXPORT_NODE_TYPE = "Tree should be of type `Node`, or inherit from `Node`"
    ERROR_CUSTOM_STYLE_SELECT = "Custom style selected, please specify the style of stem, branch, and final stem in `custom_style`"
    ERROR_CUSTOM_STYLE_DIFFERENT_LENGTH = (
        "`style_stem`, `style_branch`, and `style_stem_final` are of different length"
    )

    ERROR_ATTR_BRACKET = "Expect open and close brackets in `attr_bracket`, received"

    # tree/helper
    ERROR_NOT_FOUND = "Cannot find any node matching path_name ending with"
    ERROR_HELPER_BASENODE_TYPE = (
        "Tree should be of type `BaseNode`, or inherit from `BaseNode`"
    )

    # tree/modify
    ERROR_MERGE_CHILDREN_OR_LEAVES = "Invalid shifting, can only specify one type of merging, check `merge_children` and `merge_leaves`"
    ERROR_MODIFY_TYPE = "Invalid type, `from_paths` and `to_paths` should be list type"
    ERROR_DELETION_AND_COPY = (
        "Deletion of node will not happen if `copy=True`, check your `copy` parameter."
    )
    ERROR_INVALID_TO_PATH = "Invalid path in `to_paths` not starting with the root node. Check your `to_paths` parameter."

    ERROR_DIFFERENT_PATH_LENGTH = "Paths are different length"
    ERROR_PATH_MISMATCH = "Unable to assign from_path"
    ERROR_INVALID_FULL_PATH = (
        "Invalid path in `from_paths` not starting with the root node"
    )
    ERROR_FROM_PATH_NOT_FOUND = "Unable to find from_path"
    ERROR_SHIFT_SAME_NODE = "Attempting to shift the same node"

    # tree/search
    ERROR_PATH_NAME_INVALID_PATH = "Invalid path name. Path goes beyond root node."

    ERROR_PATH_NAME_INVALID_NODE = "Invalid path name. Node"
    ERROR_ONE_ELEMENT = "Expected less than 1 element(s), found"
    ERROR_TWO_ELEMENT = "Expected less than 2 element(s), found"
    ERROR_MORE_THAN_THREE_ELEMENT = "Expected more than 3 element(s), found"
    ERROR_MORE_THAN_FOUR_ELEMENT = "Expected more than 4 element(s), found"

    # workflow/todo
    ERROR_TODO_TYPE = "Invalid data type for item"

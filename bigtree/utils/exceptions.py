class TreeError(Exception):
    pass


class LoopError(TreeError):
    """Error during node creation"""

    pass


class CorruptedTreeError(TreeError):
    """Error during node creation or tree creation"""

    pass


class DuplicatedNodeError(TreeError):
    """Error during tree creation"""

    pass


class NotFoundError(TreeError):
    """Error during tree creation or tree search"""

    pass


class SearchError(TreeError):
    """Error during tree search"""

    pass

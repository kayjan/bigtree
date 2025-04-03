from functools import wraps
from typing import Any, Callable, TypeVar
from warnings import simplefilter, warn

T = TypeVar("T")


class TreeError(Exception):
    """Generic tree exception"""

    pass


class LoopError(TreeError):
    """Error during node creation"""

    pass


class CorruptedTreeError(TreeError):
    """Error during node creation"""

    pass


class DuplicatedNodeError(TreeError):
    """Error during tree creation"""

    pass


class NotFoundError(TreeError):
    """Error during tree pruning or modification"""

    pass


class SearchError(TreeError):
    """Error during tree search"""

    pass


def deprecated(
    alias: str,
) -> Callable[[Callable[..., T]], Callable[..., T]]:  # pragma: no cover
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        """
        This is a decorator which can be used to mark functions as deprecated. It will raise a DeprecationWarning when
        the function is used. Source: https://stackoverflow.com/a/30253848
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            simplefilter("always", DeprecationWarning)
            warn(
                "{old_func} is going to be deprecated, use {new_func} instead".format(
                    old_func=func.__name__,
                    new_func=alias,
                ),
                category=DeprecationWarning,
                stacklevel=2,
            )
            simplefilter("default", DeprecationWarning)  # reset filter
            return func(*args, **kwargs)

        return wrapper

    return decorator


def optional_dependencies_pandas(
    func: Callable[..., T],
) -> Callable[..., T]:  # pragma: no cover
    """
    This is a decorator which can be used to import optional pandas dependency. It will raise an ImportError if the
    module is not found.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            import pandas as pd  # noqa: F401
        except ImportError:
            raise ImportError(
                "pandas not available. Please perform a\n\n"
                "pip install 'bigtree[pandas]'\n\nto install required dependencies"
            ) from None
        return func(*args, **kwargs)

    return wrapper


def optional_dependencies_polars(
    func: Callable[..., T],
) -> Callable[..., T]:  # pragma: no cover
    """
    This is a decorator which can be used to import optional polars dependency. It will raise an ImportError if the
    module is not found.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            import polars as pl  # noqa: F401
        except ImportError:
            raise ImportError(
                "polars not available. Please perform a\n\n"
                "pip install 'bigtree[polars]'\n\nto install required dependencies"
            ) from None
        return func(*args, **kwargs)

    return wrapper


def optional_dependencies_matplotlib(
    func: Callable[..., T],
) -> Callable[..., T]:  # pragma: no cover
    """
    This is a decorator which can be used to import optional matplotlib dependency. It will raise an ImportError if the
    module is not found.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            import matplotlib.pyplot as plt  # noqa: F401
        except ImportError:
            raise ImportError(
                "matplotlib not available. Please perform a\n\n"
                "pip install 'bigtree[matplotlib]'\n\nto install required dependencies"
            ) from None
        return func(*args, **kwargs)

    return wrapper


def optional_dependencies_image(
    package_name: str = "",
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        """
        This is a decorator which can be used to import optional image dependency. It will raise an ImportError if the
        module is not found.
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            if not package_name or package_name == "pydot":
                try:
                    import pydot  # noqa: F401
                except ImportError:  # pragma: no cover
                    raise ImportError(
                        "pydot not available. Please perform a\n\n"
                        "pip install 'bigtree[image]'\n\nto install required dependencies"
                    ) from None
            if not package_name or package_name == "Pillow":
                try:
                    from PIL import Image, ImageDraw, ImageFont  # noqa: F401
                except ImportError:  # pragma: no cover
                    raise ImportError(
                        "Pillow not available. Please perform a\n\n"
                        "pip install 'bigtree[image]'\n\nto install required dependencies"
                    ) from None
            return func(*args, **kwargs)

        return wrapper

    return decorator

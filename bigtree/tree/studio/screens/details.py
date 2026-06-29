import bigtree

try:
    from textual.widgets import Static

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    Static = MagicMock()


DETAILS = f"""[green]Terminals for Trees[/] - [bold]Bigtree v{bigtree.__version__}[/]
"""


class Details(Static):  # type: ignore[misc]
    def __init__(self) -> None:
        super().__init__(DETAILS)

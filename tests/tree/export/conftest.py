import pytest
from rich.console import Console


@pytest.fixture
def rich_console():
    return Console(
        record=False,
        color_system=None,
        force_terminal=False,
    )

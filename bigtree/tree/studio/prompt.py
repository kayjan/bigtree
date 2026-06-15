try:
    from textual.app import ComposeResult
    from textual.containers import Vertical
    from textual.screen import ModalScreen
    from textual.widgets import Input, Label, Static

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    ComposeResult = MagicMock()
    Vertical = MagicMock()
    Static = Input = Label = MagicMock()
    ModalScreen = MagicMock()


class Prompt(ModalScreen[str]):  # type: ignore[misc]

    CSS = """
    Prompt {
        align: center middle;
        background: $background 50%
    }

    Vertical {
        width: 60;
        height: auto;
        padding: 1 2;
        background: $surface;
    }

    Input {
        width: 100%;
        border: round $primary;
    }
    """

    def __init__(self, title: str, placeholder: str = "", value: str = ""):
        super().__init__()
        self.title = title
        self.placeholder = placeholder
        self.value = value
        self.result: str | None = None

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(self.title),
            Input(
                placeholder=self.placeholder, value=self.value, select_on_focus=False
            ),
            Static("Enter to confirm, Esc to cancel", classes="hint"),
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)

    def on_key(self, event: Input.Submitted) -> None:
        if event.key == "escape":
            self.dismiss(None)

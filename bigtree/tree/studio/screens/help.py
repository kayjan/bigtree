import bigtree.tree.studio.utils as studio_utils

try:
    from textual.app import ComposeResult
    from textual.containers import Vertical
    from textual.screen import ModalScreen
    from textual.widgets import Input, Label, Rule, Static

except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    ComposeResult = MagicMock()
    Vertical = MagicMock()
    ModalScreen = MagicMock()
    Input = Label = Rule = Static = MagicMock()


class Help(ModalScreen[str]):  # type: ignore[misc]

    CSS = """
    Help {
        align: center middle;
        background: $background 50%
    }

    Vertical {
        width: 72;
        height: auto;
        padding: 1 2;
        background: $surface;
        border: round $primary;
    }

    .title {
        text-style: bold;
        content-align: center middle;
    }

    .section {
        text-style: bold;
        color: $accent;
        margin-top: 1;
    }

    .footer {
        margin-top: 1;
        color: $text-muted;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Keyboard Shortcuts", classes="title"),
            Rule(line_style="ascii"),
            *self._build_help(),
            Static("[dim]Press Esc to close[/]", classes="footer"),
        )

    @staticmethod
    def _build_help() -> list[Static]:
        widgets = []

        for section, bindings in studio_utils.HELP.items():
            widgets.append(Static(f"[b]{section}[/]", classes="section"))

            lines = []
            for key, *description in bindings:
                lines.append(f"[cyan]{key:<22}[/] {description[-1]}")
            widgets.append(Static("\n".join(lines)))
        return widgets

    def on_key(self, event: Input.Submitted) -> None:
        if event.key in ("escape", "q", "question_mark"):
            event.stop()
            self.dismiss(None)

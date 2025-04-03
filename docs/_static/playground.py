"""
Execute Python code in code blocks (Adapted from ColorAide).

This can be executed in either a Pyodide environment of a normal Python environment.
Transform Python code by executing it, transforming to a Python console output,
and finding and outputting color previews.
"""

import ast
import re
import sys
from collections.abc import Mapping, Sequence
from functools import partial
from io import StringIO

from pygments import highlight
from pygments.formatters import find_formatter_class
from pygments.lexers import get_lexer_by_name

PY310 = (3, 10) <= sys.version_info
PY311 = (3, 11) <= sys.version_info

WEBSPACE = "srgb"

AST_BLOCKS = (
    ast.If,
    ast.For,
    ast.While,
    ast.Try,
    ast.With,
    ast.FunctionDef,
    ast.ClassDef,
    ast.AsyncFor,
    ast.AsyncWith,
    ast.AsyncFunctionDef,
)

if PY310:
    AST_BLOCKS = AST_BLOCKS + (ast.Match,)


if PY311:
    AST_BLOCKS = AST_BLOCKS + (ast.TryStar,)


RE_INIT = re.compile(
    r"^\s*#\s*pragma:\s*init\n(.*?)#\s*pragma:\s*init\n", re.DOTALL | re.I
)

template = """<div class="playground" id="__playground_{el_id}">
<div class="playground-results" id="__playground-results_{el_id}">
{results}
</div>
<div class="playground-code hidden" id="__playground-code_{el_id}" data-search-exclude>
<form autocomplete="off">
<textarea class="playground-inputs" id="__playground-inputs_{el_id}" spellcheck="false">{raw_source}</textarea>
</form>
</div>
<div class="playground-footer" data-search-exclude>
<hr>
<button id="__playground-edit_{el_id}" class="playground-edit" title="Edit the code snippet">Edit</button>
<button id="__playground-share_{el_id}" style="display:none" class="playground-share" title="Copy code snippet">Share</button>
<button id="__playground-run_{el_id}" class="playground-run hidden" title="Run code">Run</button>
<button id="__playground-cancel_{el_id}" class="playground-cancel hidden" title="Cancel edit">Cancel</button>
<span class='gamut'>Powered by Pyodide. Gamut: {gamut}.</span>
</div>
</div>"""

code_id = 0


class Ramp(list):
    """Create a gradient from a list of colors."""


class Steps(list):
    """Create a special display of steps from a list of colors."""


class Row(list):
    """Restrict only the provided colors to a row."""


class AtomicString(str):
    """Atomic string."""


class BreakException(Exception):
    """Break exception."""


class ContinueException(Exception):
    """Continue exception."""


# Legacy names
HtmlGradient = Ramp
HtmlSteps = Steps
HtmlRow = Row


def _escape(txt):
    """Basic HTML escaping."""

    txt = txt.replace("&", "&amp;")
    txt = txt.replace("<", "&lt;")
    txt = txt.replace(">", "&gt;")
    return txt


class StreamOut:
    """Override the standard out."""

    def __init__(self):
        """Initialize."""
        self.old = sys.stdout
        self.stdout = StringIO()
        sys.stdout = self.stdout

    def read(self):
        """Read the stringIO buffer."""

        value = ""
        if self.stdout is not None:
            self.stdout.flush()
            value = self.stdout.getvalue()
            self.stdout = StringIO()
            sys.stdout = self.stdout
        return value

    def __enter__(self):
        """Enter."""
        return self

    def __exit__(self, type, value, traceback):  # noqa: A002
        """Exit."""

        sys.stdout = self.old
        self.old = None
        self.stdout = None


def evaluate_with(node, g, loop, index=0):
    """Evaluate with."""

    l = len(node.items) - 1  # noqa
    withitem = node.items[index]
    if withitem.context_expr:
        with eval(
            compile(ast.Expression(withitem.context_expr), "<string>", "eval"), g
        ) as w:
            g[withitem.optional_vars.id] = w
            if index < l:
                evaluate_with(node, g, loop, index + 1)
            else:
                for n in node.body:
                    yield from evaluate(n, g, loop)
    else:
        with eval(
            compile(ast.Expression(withitem.context_expr), "<string>", "eval"), g
        ):
            if index < l:
                evaluate_with(node, g, loop, index + 1)
            else:
                for n in node.body:
                    yield from evaluate(n, g, loop)


def compare_match(s, g, node):
    """Compare a match."""

    if isinstance(node, ast.MatchOr):
        for pattern in node.patterns:
            if compare_match(s, g, pattern):
                return True
    else:
        if isinstance(node, ast.MatchValue):
            p = eval(compile(ast.Expression(node.value), "<string>", "eval"), g)
            return s == p
        elif isinstance(node, ast.MatchSingleton):
            return s is node.value
        elif isinstance(node, ast.MatchSequence):
            if isinstance(s, Sequence):
                star = isinstance(node.patterns[-1], ast.MatchStar)
                l1, l2 = len(s), len(node.patterns)
                if (star and l1 >= l2 - 1) or (l1 == l2):
                    for e, p in enumerate(
                        node.patterns[:-1] if star else node.patterns
                    ):
                        if not compare_match(s[e], g, p):
                            return False
                    if star and node.patterns[-1].name:
                        g[node.patterns[-1].name] = s[l2 - 1 :]  # noqa
                    return True
            return False
        elif isinstance(node, ast.MatchMapping):
            if isinstance(s, Mapping):
                star = node.rest
                l1, l2 = len(s), len(node.patterns)
                if (star and l1 >= l2) or (l1 == l2):
                    keys = set()
                    for kp, vp in zip(node.keys, node.patterns):
                        key = eval(compile(ast.Expression(kp), "<string>", "eval"), g)
                        keys.add(key)
                        if key not in s:
                            return False
                        if not compare_match(s[key], g, vp):
                            return False
                    if star:
                        g[star] = {k: v for k, v in s.items() if k not in keys}
                    return True
            return False
        elif isinstance(node, ast.MatchClass):
            name = g.get(node.cls.id, None)
            if name is None:
                raise NameError("name '{}' is not defined".format(node.cls.id))
            if not isinstance(s, name):
                return False
            ma = getattr(s, "__match_args__", ())
            l1 = len(ma)
            l2 = len(node.patterns)
            if l1 < l2:
                raise TypeError(
                    "{}() accepts {} positional sub-patterns ({} given)".format(
                        name, l1, l2
                    )
                )
            for e, p in enumerate(node.patterns):
                if not hasattr(s, ma[e]):
                    return False
                if not compare_match(getattr(s, ma[e]), g, p):
                    return False
            for a, p in zip(node.kwd_attrs, node.kwd_patterns):
                if not hasattr(s, a):
                    return False
                if not compare_match(getattr(s, a), g, p):
                    return False
            return True
        elif isinstance(node, ast.MatchAs):
            if node.name is not None:
                g[node.name] = s
            if node.pattern:
                return compare_match(s, g, node.pattern)
            return True

    raise RuntimeError("Unknown Match pattern {}".format(str(node)))


def evaluate_except(node, e, g, loop=False):
    """Evaluate normal except block."""

    for n in node.handlers:
        if n.name:
            g[n.name] = e
        if n.type is None:
            for ne in n.body:
                yield from evaluate(ne, g, loop)
            break
        else:
            if isinstance(
                e, eval(compile(ast.Expression(n.type), "<string>", "eval"), g)
            ):
                for ne in n.body:
                    yield from evaluate(ne, g, loop)
                break
    else:
        raise


def evaluate(node, g, loop=False):
    """Evaluate."""

    if loop and isinstance(node, ast.Break):
        raise BreakException

    if loop and isinstance(node, ast.Continue):
        raise ContinueException

    if isinstance(node, ast.Expr):
        _eval = ast.Expression(node.value)
        yield eval(compile(_eval, "<string>", "eval"), g)
    elif isinstance(node, ast.If):
        if eval(compile(ast.Expression(node.test), "<string>", "eval"), g):
            for n in node.body:
                yield from evaluate(n, g, loop)
        elif node.orelse:
            for n in node.orelse:
                yield from evaluate(n, g, loop)
    elif isinstance(node, ast.While):
        while eval(compile(ast.Expression(node.test), "<string>", "eval"), g):
            try:
                for n in node.body:
                    yield from evaluate(n, g, True)
            except BreakException:  # noqa
                break
            except ContinueException:
                continue
        else:
            for n in node.orelse:
                yield from evaluate(n, g, loop)
    elif isinstance(node, ast.For):
        for x in eval(compile(ast.Expression(node.iter), "<string>", "eval"), g):
            if isinstance(node.target, ast.Tuple):
                for e, t in enumerate(node.target.dims):
                    g[t.id] = x[e]
            else:
                g[node.target.id] = x
            try:
                for n in node.body:
                    yield from evaluate(n, g, True)
            except BreakException:  # noqa
                break
            except ContinueException:
                continue
        else:
            for n in node.orelse:
                yield from evaluate(n, g, loop)
    elif isinstance(node, ast.Try):
        try:
            for n in node.body:
                yield from evaluate(n, g, loop)
        except Exception as e:
            yield from evaluate_except(node, e, g, loop)
        else:
            for n in node.orelse:
                yield from evaluate(n, g, loop)
        finally:
            for n in node.finalbody:
                yield from evaluate(n, g, loop)
    elif PY311 and isinstance(node, ast.TryStar):
        try:
            for n in node.body:
                yield from evaluate(n, g, loop)
        except ExceptionGroup as e:  # noqa
            for n in node.handlers:
                if n.name:
                    g[n.name] = e
                m, e = e.split(
                    eval(compile(ast.Expression(n.type), "<string>", "eval"), g)
                )
                if m is not None:
                    for ne in n.body:
                        yield from evaluate(ne, g, loop)
                if e is None:
                    break
            if e is not None:
                raise e
        except Exception as e:
            yield from evaluate_except(node, e, g, loop)
        else:
            for n in node.orelse:
                yield from evaluate(n, g, loop)
        finally:
            for n in node.finalbody:
                yield from evaluate(n, g, loop)
    elif PY310 and isinstance(node, ast.Match):
        s = eval(compile(ast.Expression(node.subject), "<string>", "eval"), g)
        for c in node.cases:
            if compare_match(s, g, c.pattern):
                if not c.guard or eval(
                    compile(ast.Expression(c.guard), "<string>", "eval"), g
                ):
                    for n in c.body:
                        yield from evaluate(n, g, loop)
                    break
    elif isinstance(node, ast.With):
        yield from evaluate_with(node, g, loop)
    else:
        _exec = ast.Module([node], [])
        exec(compile(_exec, "<string>", "exec"), g)
        yield None


def execute(cmd, no_except=True, inline=False, init="", g=None):
    """Execute color commands."""

    console = ""

    # Setup global initialisation
    if g is None:
        g = {
            "Ramp": Ramp,
            "Steps": Steps,
            "Row": Row,
            "HtmlRow": HtmlRow,
            "HtmlSteps": HtmlSteps,
            "HtmlGradient": HtmlGradient,
        }
    if init:
        execute(init.strip(), g=g)

    # Build AST tree
    m = RE_INIT.match(cmd)
    if m:
        block_init = m.group(1)
        src = cmd[m.end() :]  # noqa
        execute(block_init, g=g)
    else:
        src = cmd
    lines = src.split("\n")
    try:
        tree = ast.parse(src)
    except Exception as e:
        if no_except:
            if not inline:
                from pymdownx.superfences import SuperFencesException

                raise SuperFencesException from e
            else:
                from pymdownx.inlinehilite import InlineHiliteException

                raise InlineHiliteException from e
        import traceback

        return "{}".format(traceback.format_exc())

    for node in tree.body:
        result = []

        # Format source as Python console statements
        start = node.lineno
        end = node.end_lineno
        stmt = lines[start - 1 : end]  # noqa
        command = ""
        stmt = [
            f">>> {_stmt}" if not idx else f"... {_stmt}"
            for idx, _stmt in enumerate(stmt)
        ]
        command += "\n".join(stmt)
        if isinstance(node, AST_BLOCKS):
            command += "\n... "

        try:
            # Capture anything sent to standard out
            with StreamOut() as s:
                # Execute code
                for x in evaluate(node, g):
                    result.append(x)

                    # Output captured standard out after statements
                    text = s.read()
                    if text:
                        result.append(AtomicString(text))

                # Execution went well, so append command
                console += command

        except Exception as e:  # noqa:  PERF203
            if no_except:
                if not inline:
                    from pymdownx.superfences import SuperFencesException

                    raise SuperFencesException from e
                else:
                    from pymdownx.inlinehilite import InlineHiliteException

                    raise InlineHiliteException from e
            import traceback

            console += "{}\n{}".format(command, traceback.format_exc())
            # Failed for some reason, so quit
            break

        # If we got a result, output it as well
        result_text = "\n"
        for r in result:
            if r is None:
                continue
            result_text += "{}{}".format(
                (
                    repr(r)
                    if isinstance(r, str) and not isinstance(r, AtomicString)
                    else str(r)
                ),
                "\n" if not isinstance(r, AtomicString) else "",
            )
        console += result_text

    return console


def colorize(src, lang, **options):
    """Colorize."""

    HtmlFormatter = find_formatter_class("html")
    lexer = get_lexer_by_name(lang, **options)
    formatter = HtmlFormatter(cssclass="highlight", wrapcode=True)
    return highlight(src, lexer, formatter).strip()


def color_command_validator(language, inputs, options, attrs, md):
    """Color validator."""

    valid_inputs = {"exceptions", "play", "wheel"}

    for k, v in inputs.items():
        if k in valid_inputs:
            options[k] = True
            continue
        attrs[k] = v
    return True


def _color_command_formatter(
    src="", language="", class_name=None, options=None, md="", init="", **kwargs
):
    """Formatter wrapper."""

    global code_id

    # Support the new way
    gamut = kwargs.get("gamut", WEBSPACE)
    play = options.get("play", False) if options is not None else False
    # Support the old way
    if not play and language == "playground":
        play = True

    if not play:
        return md.preprocessors["fenced_code_block"].extension.superfences[0][
            "formatter"
        ](
            src=src,
            class_name=class_name,
            language="py",
            md=md,
            options=options,
            **kwargs,
        )

    if len(md.preprocessors["fenced_code_block"].extension.stash) == 0:
        code_id = 0

    # Check if we should allow exceptions
    exceptions = options.get("exceptions", False) if options is not None else False

    console = execute(src.strip(), not exceptions, init=init)

    el = md.preprocessors["fenced_code_block"].extension.superfences[0]["formatter"](
        src=console,
        class_name="highlight",
        language="pycon",
        md=md,
        options=options,
        **kwargs,
    )
    el = '<div class="color-command">{}</div>'.format(el)
    el = template.format(
        el_id=code_id, raw_source=_escape(src), results=el, gamut=gamut
    )
    code_id += 1
    return el


def color_command_formatter(init="", gamut=WEBSPACE):
    """Return a Python command formatter with the provided imports."""

    return partial(_color_command_formatter, init=init, gamut=gamut)


#############################
# Pyodide specific code
#############################
def _live_color_command_formatter(src, init="", gamut=WEBSPACE):
    """Formatter wrapper."""

    try:
        console = execute(src.strip(), False, init=init)
        el = colorize(console, "pycon", **{"python3": True, "stripnl": False})
        el = '<div class="color-command">{}</div>'.format(el)
    except Exception:
        import traceback

        return (
            '<div class="color-command"><div class="swatch-bar"></div>{}</div>'.format(
                colorize(traceback.format_exc(), "pycon")
            )
        )
    return el


def live_color_command_formatter(init="", gamut=WEBSPACE):
    """Return a Python command formatter with the provided imports."""

    return partial(_live_color_command_formatter, init=init, gamut=gamut)


def live_color_command_validator(language, inputs, options, attrs, md):
    """Color validator."""

    value = color_command_validator(language, inputs, options, attrs, md)
    # Live edit, we always allow exceptions so not to crash the service.
    options["exceptions"] = True
    return value

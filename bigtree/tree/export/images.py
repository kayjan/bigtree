from __future__ import annotations

import collections
import re
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, TypeVar, Union

from bigtree.node import node
from bigtree.tree.export.stdout import yield_tree
from bigtree.utils import assertions, constants, exceptions

try:
    import pydot
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pydot = MagicMock()

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    Image = ImageDraw = ImageFont = MagicMock()

try:
    import matplotlib as mpl
    from matplotlib.colors import Normalize
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    mpl = MagicMock()
    Normalize = MagicMock()


__all__ = [
    "tree_to_dot",
    "tree_to_pillow_graph",
    "tree_to_pillow",
    "tree_to_mermaid",
]

T = TypeVar("T", bound=node.Node)


@exceptions.optional_dependencies_image("pydot")
def tree_to_dot(
    tree: Union[T, List[T]],
    directed: bool = True,
    rankdir: str = "TB",
    bg_colour: str = "",
    node_colour: str = "",
    node_shape: str = "",
    edge_colour: str = "",
    node_attr: Callable[[T], Dict[str, Any]] | str = "",
    edge_attr: Callable[[T], Dict[str, Any]] | str = "",
) -> pydot.Dot:
    r"""Export tree or list of trees to pydot.Dot object. Object can be converted to other format, such as png, dot file
    or dot string. Dot string can be imported to work with networkx.

    Possible node attributes include style, fillcolor, shape.

    Examples:
        >>> from bigtree import Node, tree_to_dot
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> graph = tree_to_dot(root)

        Display image directly without saving (requires IPython)

        >>> from IPython.display import Image, display
        >>> plt = Image(graph.create_png())
        >>> display(plt)
        <IPython.core.display.Image object>

        Export to image, dot file, etc.

        >>> graph.write_png("assets/tree.png")
        >>> graph.write_dot("assets/tree.dot")

        ![Export to Dot](https://github.com/kayjan/bigtree/raw/master/assets/tree.png)

        Export to string

        >>> graph.to_string()
        'strict digraph G {\nrankdir=TB;\na0 [label=a];\nb0 [label=b];\na0 -> b0;\nd0 [label=d];\nb0 -> d0;\ne0 [label=e];\nb0 -> e0;\nc0 [label=c];\na0 -> c0;\n}\n'

        Defining node and edge attributes (using node attribute)

        >>> class CustomNode(Node):
        ...     def __init__(self, name, node_shape="", edge_label="", **kwargs):
        ...         super().__init__(name, **kwargs)
        ...         self.node_shape = node_shape
        ...         self.edge_label = edge_label
        ...
        ...     @property
        ...     def edge_attr(self):
        ...         if self.edge_label:
        ...             return {"label": self.edge_label}
        ...         return {}
        ...
        ...     @property
        ...     def node_attr(self):
        ...         if self.node_shape:
        ...             return {"shape": self.node_shape}
        ...         return {}
        >>>
        >>>
        >>> root = CustomNode("a", node_shape="circle")
        >>> b = CustomNode("b", edge_label="child", parent=root)
        >>> c = CustomNode("c", edge_label="child", parent=root)
        >>> d = CustomNode("d", node_shape="square", edge_label="child", parent=b)
        >>> e = CustomNode("e", node_shape="square", edge_label="child", parent=b)
        >>> graph = tree_to_dot(root, node_colour="gold", node_shape="diamond", node_attr="node_attr", edge_attr="edge_attr")
        >>> graph.write_png("assets/export_tree_dot.png")

        ![Export to dot](https://github.com/kayjan/bigtree/raw/master/assets/export_tree_dot.png)

        Alternative way to define node and edge attributes (using callable function)

        >>> def get_node_attribute(node: Node):
        ...     if node.is_leaf:
        ...         return {"shape": "square"}
        ...     return {"shape": "circle"}
        >>>
        >>>
        >>> root = CustomNode("a")
        >>> b = CustomNode("b", parent=root)
        >>> c = CustomNode("c", parent=root)
        >>> d = CustomNode("d", parent=b)
        >>> e = CustomNode("e", parent=b)
        >>> graph = tree_to_dot(root, node_colour="gold", node_attr=get_node_attribute)
        >>> graph.write_png("assets/export_tree_dot_callable.png")

        ![Export to dot (callable)](https://github.com/kayjan/bigtree/raw/master/assets/export_tree_dot_callable.png)

    Args:
        tree: tree or list of trees to be exported
        directed: indicator whether graph should be directed or undirected
        rankdir: layout direction, accepts 'TB' (top to bottom), 'BT' (bottom to top), 'LR' (left to right), or 'RL'
            (right to left)
        bg_colour: background color of image
        node_colour: fill colour of nodes
        node_shape: shape of nodes. Possible node_shape include "circle", "square", "diamond", "triangle"
        edge_colour: colour of edges
        node_attr: If string type, it refers to ``Node`` attribute for node style. If callable type, it takes in the
            node itself and returns the node style. This overrides `node_colour` and `node_shape`. Possible node styles
            include {"style": "filled", "fillcolor": "gold", "shape": "diamond"}
        edge_attr: If string type, it refers to ``Node`` attribute for edge style. If callable type, it takes in the
            node itself and returns the edge style. This overrides `edge_colour`. Possible edge styles include
            {"style": "bold", "label": "edge label", "color": "black"}

    Returns:
        Dot object of tree
    """
    # Get style
    graph_style = dict(bgcolor=bg_colour) if bg_colour else {}
    node_style = dict(style="filled", fillcolor=node_colour) if node_colour else {}
    node_style.update({"shape": node_shape} if node_shape else {})
    edge_style = dict(color=edge_colour) if edge_colour else {}

    tree = tree.copy()
    _graph = (
        pydot.Dot(graph_type="digraph", strict=True, rankdir=rankdir, **graph_style)
        if directed
        else pydot.Dot(graph_type="graph", strict=True, rankdir=rankdir, **graph_style)
    )

    if not isinstance(tree, list):
        tree = [tree]

    for _tree in tree:
        assertions.assert_tree_type(_tree, node.Node, "Node")

        name_dict: Dict[str, List[str]] = collections.defaultdict(list)

        def _recursive_append(parent_name: Optional[str], child_node: T) -> None:
            """Recursively iterate through node and its children to export to dot by creating node and edges.

            Args:
                parent_name: parent name
                child_node: current node
            """
            _node_style = node_style.copy()
            _edge_style = edge_style.copy()

            if node_attr:
                if isinstance(node_attr, str) and child_node.get_attr(node_attr):
                    _node_style.update(child_node.get_attr(node_attr))
                elif isinstance(node_attr, Callable):  # type: ignore
                    _node_style.update(node_attr(child_node))  # type: ignore
            if edge_attr:
                if isinstance(edge_attr, str) and child_node.get_attr(edge_attr):
                    _edge_style.update(child_node.get_attr(edge_attr))
                elif isinstance(edge_attr, Callable):  # type: ignore
                    _edge_style.update(edge_attr(child_node))  # type: ignore

            child_label = child_node.node_name
            if child_node.path_name not in name_dict[child_label]:  # pragma: no cover
                name_dict[child_label].append(child_node.path_name)
            child_name = child_label + str(
                name_dict[child_label].index(child_node.path_name)
            )
            pydot_child_node = pydot.Node(
                name=child_name, label=child_label, **_node_style
            )
            _graph.add_node(pydot_child_node)
            if parent_name is not None:
                edge = pydot.Edge(parent_name, child_name, **_edge_style)
                _graph.add_edge(edge)
            for _child in child_node.children:
                if _child:
                    _recursive_append(child_name, _child)

        _recursive_append(None, _tree.root)
    return _graph


def _load_font(font_family: str, font_size: int) -> ImageFont.truetype:
    if not font_family:
        from urllib.request import urlopen

        dejavusans_url = "https://github.com/kayjan/bigtree/raw/master/assets/DejaVuSans.ttf?raw=true"
        font_family = urlopen(dejavusans_url)
    try:
        font = ImageFont.truetype(font_family, font_size)
    except OSError:
        raise ValueError(
            f"Font file {font_family} is not found, set `font_family` parameter to point to a valid .ttf file."
        )
    return font


@exceptions.optional_dependencies_image("Pillow")
def tree_to_pillow_graph(
    tree: T,
    node_content: str = "{node_name}",
    *,
    margin: Optional[Dict[str, int]] = None,
    height_buffer: Union[int, float] = 20,
    width_buffer: Union[int, float] = 10,
    font_family: str = "",
    font_size: int = 12,
    font_colour: Union[Tuple[int, int, int], str] = "black",
    text_align: str = "center",
    bg_colour: Union[Tuple[int, int, int], str] = "white",
    rect_margin: Optional[Dict[str, int]] = None,
    rect_fill: Union[Tuple[int, int, int], str, mpl.colors.Colormap] = "white",
    rect_cmap_attr: Optional[str] = None,
    rect_outline: Union[Tuple[int, int, int], str] = "black",
    rect_width: int = 1,
    **kwargs: Any,
) -> Image.Image:
    r"""Export tree to PIL.Image.Image object. Object can be converted to other formats, such as jpg, or png. Image will
    look like a tree/graph-like structure, accepts additional keyword arguments as input to `yield_tree`.

    Customisations:

        - To change the margin of tree within diagram, vary `margin`
        - To change the margin of the text within node, vary `rect_margin`
        - For more separation between nodes, change `height_buffer` and `width_buffer`

    Examples:
        >>> from bigtree import Node, tree_to_pillow_graph
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> pillow_image = tree_to_pillow_graph(root, node_content="{node_name}\nAge: {age}")

        Export to image (PNG, JPG) file, etc.

        >>> pillow_image.save("assets/tree_pillow_graph.png")
        >>> pillow_image.save("assets/tree_pillow_graph.jpg")

        ![Export to Pillow Graph](https://github.com/kayjan/bigtree/raw/master/assets/tree_pillow_graph.png)

    Args:
        tree: tree to be exported
        node_content: display text in node
        margin: margin of diagram
        height_buffer: height buffer between node layers, in pixels
        width_buffer: width buffer between sibling nodes, in pixels
        font_family: file path of font family, requires .ttf file, defaults to DejaVuSans
        font_size: font size
        font_colour: font colour, accepts tuple of RGB values or string
        text_align: text align for multi-line text
        bg_colour: background of image, accepts tuple of RGB values or string
        rect_margin: (for rectangle) margin of text to rectangle, in pixels
        rect_fill: (for rectangle) colour to use for fill
        rect_cmap_attr: (for rectangle) if rect_fill is a colormap, attribute of node to retrieve fill from colormap,
            must be a float/int attribute
        rect_outline: (for rectangle) colour to use for outline
        rect_width: (for rectangle) line width, in pixels

    Returns:
        Pillow object of tree, in graph format
    """
    use_cmap = isinstance(rect_fill, mpl.colors.Colormap)
    if use_cmap and rect_cmap_attr is None:
        raise ValueError(
            "`rect_cmap_attr` cannot be None if rect_fill is mpl.colormaps"
        )

    default_margin = {"t": 10, "b": 10, "l": 10, "r": 10}
    default_rect_margin = {"t": 5, "b": 5, "l": 5, "r": 5}
    margin = {**default_margin, **(margin or {})}
    rect_margin = {**default_rect_margin, **(rect_margin or {})}

    # Initialize font
    font = _load_font(font_family, font_size)

    # Iterate tree once to obtain attributes
    # Calculate image dimension from text, get range for colourmap if applicable
    _max_text_width = 0
    _max_text_height = 0
    _image = Image.new("RGB", (0, 0))
    _draw = ImageDraw.Draw(_image)

    def get_node_text(_node: T, _node_content: str) -> str:
        pattern = re.compile(r"\{(.*)\}")
        matches = re.findall(pattern, _node_content)
        for match in matches:
            _node_content = _node_content.replace(
                f"{{{match}}}", str(_node.get_attr(match, ""))
            )
        return _node_content

    cmap_range: Set[Union[float, int]] = set()
    for _, _, _node in yield_tree(tree, **kwargs):
        l, t, r, b = _draw.multiline_textbbox(
            (0, 0), get_node_text(_node, node_content), font=font
        )
        _max_text_width = max(
            _max_text_width, l + r + rect_margin.get("l", 0) + rect_margin.get("r", 0)
        )
        _max_text_height = max(
            _max_text_height, t + b + rect_margin.get("t", 0) + rect_margin.get("b", 0)
        )
        if use_cmap:
            cmap_range.add(_node.get_attr(rect_cmap_attr, 0))

    cmap_dict = {}
    if use_cmap:
        norm = Normalize(vmin=min(cmap_range), vmax=max(cmap_range))
        cmap_range_list = [norm(c) for c in cmap_range]
        cmap_colour_list = rect_fill(cmap_range_list)  # type: ignore
        cmap_dict = dict(zip(cmap_range_list, cmap_colour_list))

    # Get x, y, coordinates and height, width of diagram
    from bigtree.utils.plot import reingold_tilford

    tree = tree.copy()
    reingold_tilford(
        tree,
        subtree_separation=_max_text_width + width_buffer,
        sibling_separation=_max_text_width + width_buffer,
        level_separation=_max_text_height + height_buffer,
        x_offset=0.5 * _max_text_width + margin.get("l", 0),
        y_offset=0.5 * _max_text_height + margin.get("t", 0),
        reverse=True,  # top-left corner is (0, 0)
    )

    _width, _height = 0, 0
    _width_margin = 0.5 * _max_text_width + margin.get("r", 0)
    _height_margin = 0.5 * _max_text_height + margin.get("b")
    for _, _, _node in yield_tree(tree, **kwargs):
        _width = max(_width, _node.get_attr("x") + _width_margin)
        _height = max(_height, _node.get_attr("y") + _height_margin)
    _width = int(round(_width + 0.5, 0))
    _height = int(round(_height + 0.5, 0))

    # Initialize and draw image
    image = Image.new("RGB", (_width, _height), bg_colour)
    image_draw = ImageDraw.Draw(image)

    for _, _, _node in yield_tree(tree, **kwargs):
        _x, _y = _node.get_attr("x"), _node.get_attr("y")
        x1, x2 = _x - 0.5 * _max_text_width, _x + 0.5 * _max_text_width
        y1, y2 = _y - 0.5 * _max_text_height, _y + 0.5 * _max_text_height
        # Draw box
        _rect_fill = rect_fill
        if use_cmap:
            _rect_fill = mpl.colors.rgb2hex(
                cmap_dict[norm(_node.get_attr(rect_cmap_attr, 0))]
            )
        image_draw.rectangle(
            [x1, y1, x2, y2], fill=_rect_fill, outline=rect_outline, width=rect_width
        )
        # Draw text
        image_draw.text(
            (x1 + rect_margin.get("l", 0), y1 + rect_margin.get("t", 0)),
            get_node_text(_node, node_content),
            font=font,
            fill=font_colour,
            align=text_align,
        )
        # Draw line to parent
        if _node.parent:
            _child_x, _child_y = (
                _node.get_attr("x"),
                _node.get_attr("y") - 0.5 * _max_text_height,
            )
            _parent_x, _parent_y = (
                _node.parent.get_attr("x"),
                _node.parent.get_attr("y") + 0.5 * _max_text_height,
            )
            middle_y = (_child_y + _parent_y) / 2
            image_draw.line(
                (_parent_x, _parent_y, _parent_x, middle_y),
                fill=rect_outline,
                width=rect_width,
            )
            image_draw.line(
                (_parent_x, middle_y, _child_x, middle_y),
                fill=rect_outline,
                width=rect_width,
            )
            image_draw.line(
                (_child_x, _child_y, _child_x, middle_y),
                fill=rect_outline,
                width=rect_width,
            )

    return image


@exceptions.optional_dependencies_image("Pillow")
def tree_to_pillow(
    tree: T,
    width: int = 0,
    height: int = 0,
    start_pos: Tuple[int, int] = (10, 10),
    font_family: str = "",
    font_size: int = 12,
    font_colour: Union[Tuple[int, int, int], str] = "black",
    bg_colour: Union[Tuple[int, int, int], str] = "white",
    **kwargs: Any,
) -> Image.Image:
    """Export tree to PIL.Image.Image object. Object can be converted to other formats, such as jpg, or png. Image will
    be similar format as `print_tree`, accepts additional keyword arguments as input to `yield_tree`.

    Examples:
        >>> from bigtree import Node, tree_to_pillow
        >>> root = Node("a", age=90)
        >>> b = Node("b", age=65, parent=root)
        >>> c = Node("c", age=60, parent=root)
        >>> d = Node("d", age=40, parent=b)
        >>> e = Node("e", age=35, parent=b)
        >>> pillow_image = tree_to_pillow(root)

        Export to image (PNG, JPG) file, etc.

        >>> pillow_image.save("assets/tree_pillow.png")
        >>> pillow_image.save("assets/tree_pillow.jpg")

        ![Export to pillow](https://github.com/kayjan/bigtree/raw/master/assets/tree_pillow.png)

    Args:
        tree: tree to be exported
        width: width of image, optional as width of image is calculated automatically
        height: height of image, optional as height of image is calculated automatically
        start_pos: start position of text, (x-offset, y-offset)
        font_family: file path of font family, requires .ttf file, defaults to DejaVuSans
        font_size: font size
        font_colour: font colour, accepts tuple of RGB values or string
        bg_colour: background of image, accepts tuple of RGB values or string

    Returns:
        Pillow object of tree, in condensed text format
    """
    # Initialize font
    font = _load_font(font_family, font_size)

    # Initialize text
    image_text = []
    for branch, stem, _node in yield_tree(tree, **kwargs):
        image_text.append(f"{branch}{stem}{_node.node_name}\n")

    # Calculate image dimension from text, otherwise override with argument
    def get_list_of_text_dimensions(
        text_list: List[str],
    ) -> List[Tuple[int, int, int, int]]:
        """Get list dimensions.

        Args:
            text_list: list of texts

        Returns:
            Bounding box dimensions (left, top, right, bottom)
        """
        _image = Image.new("RGB", (0, 0))
        _draw = ImageDraw.Draw(_image)
        return [_draw.textbbox((0, 0), text_line, font=font) for text_line in text_list]

    text_dimensions = get_list_of_text_dimensions(image_text)
    text_height = sum(
        [text_dimension[3] + text_dimension[1] for text_dimension in text_dimensions]
    )
    text_width = max(
        [text_dimension[2] + text_dimension[0] for text_dimension in text_dimensions]
    )
    image_text_str = "".join(image_text)
    width = max(width, text_width + 2 * start_pos[0])
    height = max(height, text_height + 2 * start_pos[1])

    # Initialize and draw image
    image = Image.new("RGB", (width, height), bg_colour)
    image_draw = ImageDraw.Draw(image)
    image_draw.text(start_pos, image_text_str, font=font, fill=font_colour)
    return image


def tree_to_mermaid(
    tree: T,
    title: str = "",
    theme: Optional[str] = None,
    rankdir: str = "TB",
    line_shape: str = "basis",
    node_colour: str = "",
    node_border_colour: str = "",
    node_border_width: float = 1,
    node_shape: str = "rounded_edge",
    node_shape_attr: Callable[[T], str] | str = "",
    edge_arrow: str = "normal",
    edge_arrow_attr: Callable[[T], str] | str = "",
    edge_label: str = "",
    node_attr: Callable[[T], str] | str = "",
    **kwargs: Any,
) -> str:
    r"""Export tree to mermaid Markdown text. Accepts additional keyword arguments as input to `yield_tree`.

    Parameters for customisations that apply to entire flowchart include:
        - Title, `title`
        - Theme, `theme`
        - Layout direction, `rankdir`
        - Line shape or curvature, `line_shape`
        - Fill colour of nodes, `node_colour`
        - Border colour of nodes, `node_border_colour`
        - Border width of nodes, `node_border_width`
        - Node shape, `node_shape`
        - Edge arrow style, `edge_arrow`

    Parameters for customisations that apply to customised nodes:
        - Fill colour of nodes, fill under `node_attr`
        - Border colour of nodes, stroke under `node_attr`
        - Border width of nodes, stroke-width under `node_attr`
        - Node shape, `node_shape_attr`
        - Edge arrow style, `edge_arrow_attr`
        - Edge label, `edge_label`

    **Accepted Parameter Values**

    Possible theme:
        - default
        - neutral: great for black and white documents
        - dark: great for dark-mode
        - forest: shades of geen
        - base: theme that can be modified, use it for customisations

    Possible rankdir:
        - `TB`: top-to-bottom
        - `BT`: bottom-to-top
        - `LR`: left-to-right
        - `RL`: right-to-left

    Possible line_shape:
        - `basis`
        - `bumpX`: used in LR or RL direction
        - `bumpY`
        - `cardinal`: undirected
        - `catmullRom`: undirected
        - `linear`:
        - `monotoneX`: used in LR or RL direction
        - `monotoneY`
        - `natural`
        - `step`: used in LR or RL direction
        - `stepAfter`
        - `stepBefore`: used in LR or RL direction

    Possible node_shape:
        - `rounded_edge`: rectangular with rounded edges
        - `stadium`: (_) shape, rectangular with rounded ends
        - `subroutine`: ||_|| shape, rectangular with additional line at the ends
        - `cylindrical`: database node
        - `circle`: circular
        - `asymmetric`: >_| shape
        - `rhombus`: decision node
        - `hexagon`: <_> shape
        - `parallelogram`: /_/ shape
        - `parallelogram_alt`: \\_\\ shape, inverted parallelogram
        - `trapezoid`: /_\\ shape
        - `trapezoid_alt`: \\_/ shape, inverted trapezoid
        - `double_circle`

    Possible edge_arrow:
        - `normal`: directed arrow, shaded arrowhead
        - `bold`: bold directed arrow
        - `dotted`: dotted directed arrow
        - `open`: line, undirected arrow
        - `bold_open`: bold line
        - `dotted_open`: dotted line
        - `invisible`: no line
        - `circle`: directed arrow with filled circle arrowhead
        - `cross`: directed arrow with cross arrowhead
        - `double_normal`: bidirectional directed arrow
        - `double_circle`: bidirectional directed arrow with filled circle arrowhead
        - `double_cross`: bidirectional directed arrow with cross arrowhead

    Refer to mermaid [documentation](http://mermaid.js.org/syntax/flowchart.html) for more information.
    Paste the output into any markdown file renderer to view the flowchart, alternatively visit the
    mermaid playground [here](https://mermaid.live/).

    !!! note

        Advanced mermaid flowchart functionalities such as subgraphs and interactions (script, click) are not supported.

    Examples:
        >>> from bigtree import tree_to_mermaid
        >>> root = Node("a", node_shape="rhombus")
        >>> b = Node("b", edge_arrow="bold", edge_label="Child 1", parent=root)
        >>> c = Node("c", edge_arrow="dotted", edge_label="Child 2", parent=root)
        >>> d = Node("d", node_style="fill:yellow, stroke:black", parent=b)
        >>> e = Node("e", parent=b)
        >>> graph = tree_to_mermaid(root)
        >>> print(graph)
        ```mermaid
        %%{ init: { 'flowchart': { 'curve': 'basis' } } }%%
        flowchart TB
        0("a") --> 0-0("b")
        0-0 --> 0-0-0("d")
        0-0 --> 0-0-1("e")
        0("a") --> 0-1("c")
        classDef default stroke-width:1
        ```

        **Customise node shape, edge label, edge arrow, and custom node attributes**

        >>> graph = tree_to_mermaid(
        ...     root,
        ...     title="Mermaid Diagram",
        ...     theme="forest",
        ...     node_shape_attr="node_shape",
        ...     edge_label="edge_label",
        ...     edge_arrow_attr="edge_arrow",
        ...     node_attr="node_style",
        ... )
        >>> print(graph)
        ```mermaid
        ---
        title: Mermaid Diagram
        ---
        %%{ init: { 'flowchart': { 'curve': 'basis' }, 'theme': 'forest' } }%%
        flowchart TB
        0{"a"} ==>|Child 1| 0-0("b")
        0-0 --> 0-0-0("d"):::class0-0-0
        0-0 --> 0-0-1("e")
        0{"a"} -.->|Child 2| 0-1("c")
        classDef default stroke-width:1
        classDef class0-0-0 fill:yellow, stroke:black
        ```

    Args:
        tree: tree to be exported
        title: title
        theme: theme or colour scheme
        rankdir: layout direction, accepts 'TB' (top to bottom), 'BT' (bottom to top), 'LR' (left to right), 'RL' (right
            to left)
        line_shape: line shape or curvature
        node_colour: fill colour of nodes, can be colour name or hexcode
        node_border_colour: border colour of nodes, can be colour name or hexcode
        node_border_width: width of node border
        node_shape: node shape, sets the shape of every node
        node_shape_attr: If string type, it refers to ``Node`` attribute for node shape. If callable type, it takes in
            the node itself and returns the node shape. This sets the shape of custom nodes, and overrides default
            `node_shape`
        edge_arrow: edge arrow style from parent to itself, sets the arrow style of every edge
        edge_arrow_attr: If string type, it refers to ``Node`` attribute for edge arrow style. If callable type, it takes
            in the node itself and returns the edge arrow style. This sets the edge arrow style of custom nodes from
            parent to itself, and overrides default `edge_arrow`
        edge_label: ``Node`` attribute for edge label from parent to itself
        node_attr: If string type, it refers to ``Node`` attribute for node style. If callable type, it takes in the node
            itself and returns the node style. This overrides `node_colour`, `node_border_colour`, and `node_border_width`

    Returns:
        Mermaid string of tree
    """
    from bigtree.tree.helper import clone_tree

    themes = constants.MermaidConstants.THEMES
    rankdirs = constants.MermaidConstants.RANK_DIR
    line_shapes = constants.MermaidConstants.LINE_SHAPES
    node_shapes = constants.MermaidConstants.NODE_SHAPES
    edge_arrows = constants.MermaidConstants.EDGE_ARROWS

    # Assertions
    if theme:
        assertions.assert_str_in_list("theme", theme, themes)
    assertions.assert_str_in_list("rankdir", rankdir, rankdirs)
    assertions.assert_key_in_dict("node_shape", node_shape, node_shapes)
    assertions.assert_str_in_list("line_shape", line_shape, line_shapes)
    assertions.assert_key_in_dict("edge_arrow", edge_arrow, edge_arrows)

    mermaid_template = """```mermaid\n{title}{line_style}\nflowchart {rankdir}\n{flows}\n{styles}\n```"""
    flowchart_template = "{from_ref}{from_name}{from_style} {arrow}{arrow_label} {to_ref}{to_name}{to_style}"
    style_template = "classDef {style_name} {style}"

    # Content
    theme_mermaid = f", 'theme': '{theme}'" if theme else ""
    title = f"---\ntitle: {title}\n---\n" if title else ""
    line_style = f"%%{{ init: {{ 'flowchart': {{ 'curve': '{line_shape}' }}{theme_mermaid} }} }}%%"
    styles = []
    flows = []

    def _construct_style(
        _style_name: str,
        _node_colour: str,
        _node_border_colour: str,
        _node_border_width: float,
    ) -> str:
        """Construct style for Mermaid.

        Args:
            _style_name: style name
            _node_colour: node colour
            _node_border_colour: node border colour
            _node_border_width: node border width

        Returns:
            Style
        """
        style = []
        if _node_colour:
            style.append(f"fill:{_node_colour}")
        if _node_border_colour:
            style.append(f"stroke:{_node_border_colour}")
        if _node_border_width:
            style.append(f"stroke-width:{_node_border_width}")
        if not style:
            raise ValueError("Unable to construct style!")
        return style_template.format(style_name=_style_name, style=",".join(style))

    default_style = _construct_style(
        "default", node_colour, node_border_colour, node_border_width
    )
    styles.append(default_style)

    class MermaidNode(node.Node):
        """Mermaid Node, adds property `mermaid_name`"""

        @property
        def mermaid_name(self) -> str:
            """Reference name for MermaidNode, must be unique for each node.

            Returns:
                Name of mermaid node
            """
            if self.is_root:
                return "0"
            return f"{self.parent.mermaid_name}-{self.parent.children.index(self)}"

    def _get_attr(
        _node: T,
        attr_parameter: str | Callable[[T], str],
        default_parameter: str,
    ) -> str:
        """Get custom attribute if available, otherwise return default parameter.

        Args:
            _node: node to get custom attribute, can be accessed as node attribute or a callable that takes in the node
            attr_parameter: custom attribute parameter
            default_parameter: default parameter if there is no attr_parameter

        Returns:
            Node attribute
        """
        _choice = default_parameter
        if attr_parameter:
            if isinstance(attr_parameter, str):
                _choice = _node.get_attr(attr_parameter, default_parameter)
            else:
                _choice = attr_parameter(_node)
        return _choice

    tree_mermaid: T = clone_tree(tree, MermaidNode)  # type: ignore
    for _, _, _node in yield_tree(tree_mermaid, **kwargs):
        if not _node.is_root:
            # Get custom style (node_shape_attr)
            _parent_node_name = ""
            _from_style = ""
            if _node.parent.is_root:
                # Get custom style for root (node_shape_attr, node_attr)
                _parent_node_name = node_shapes[
                    _get_attr(_node.parent, node_shape_attr, node_shape)
                ].format(label=_node.parent.node_name)

                if _get_attr(_node.parent, node_attr, "") and len(styles) < 2:
                    _from_style = _get_attr(_node.parent, node_attr, "")
                    _from_style_class = (
                        f"""class{_node.parent.get_attr("mermaid_name")}"""
                    )
                    styles.append(
                        style_template.format(
                            style_name=_from_style_class, style=_from_style
                        )
                    )
                    _from_style = f":::{_from_style_class}"
            _node_name = node_shapes[
                _get_attr(_node, node_shape_attr, node_shape)
            ].format(label=_node.node_name)

            # Get custom style (edge_arrow_attr, edge_label)
            _arrow = edge_arrows[_get_attr(_node, edge_arrow_attr, edge_arrow)]
            _arrow_label = (
                f"|{_node.get_attr(edge_label)}|" if _node.get_attr(edge_label) else ""
            )

            # Get custom style (node_attr)
            _to_style = _get_attr(_node, node_attr, "")
            if _to_style:
                _to_style_class = f"""class{_node.get_attr("mermaid_name")}"""
                styles.append(
                    style_template.format(style_name=_to_style_class, style=_to_style)
                )
                _to_style = f":::{_to_style_class}"

            flows.append(
                flowchart_template.format(
                    from_ref=_node.parent.get_attr("mermaid_name"),
                    from_name=_parent_node_name,
                    from_style=_from_style,
                    arrow=_arrow,
                    arrow_label=_arrow_label,
                    to_ref=_node.get_attr("mermaid_name"),
                    to_name=_node_name,
                    to_style=_to_style,
                )
            )

    return mermaid_template.format(
        title=title,
        line_style=line_style,
        rankdir=rankdir,
        flows="\n".join(flows),
        styles="\n".join(styles),
    )

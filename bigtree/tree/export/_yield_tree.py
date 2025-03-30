import collections
from typing import Iterable, List, Optional, Tuple, Type, TypeVar, Union

from bigtree.node import node
from bigtree.tree.export._stdout import (
    calculate_stem_pos,
    format_node,
    horizontal_join,
    vertical_join,
)
from bigtree.tree.helper import get_subtree
from bigtree.utils import constants, iterators

__all__ = [
    "YieldTree",
    "HYieldTree",
    "VYieldTree",
]

T = TypeVar("T", bound=node.Node)
TStyle = TypeVar(
    "TStyle",
    bound=Union[
        constants.BaseStyle,
        constants.BasePrintStyle,
        constants.BaseHPrintStyle,
        constants.BaseVPrintStyle,
    ],
)


def _get_style_class(
    base_style: Type[TStyle],
    style: Union[str, Iterable[str], TStyle],
    param_name: str,
) -> TStyle:
    """Get style class from style, which can be a string, style_class, or list of input to style_class.

    Args:
        base_style: style class to return
        style: style of print
        param_name: parameter name for error message

    Returns:
        Style class
    """
    if isinstance(style, str):
        return base_style.from_style(style)  # type: ignore
    elif isinstance(style, Iterable):
        n_fields = len(base_style.__dict__["__dataclass_fields__"])
        if len(list(style)) != n_fields:
            raise ValueError(
                f"Please specify the style of {n_fields} icons in `{param_name}`"
            )
        return base_style(*style)  # type: ignore
    return style


class BaseYieldTree:
    def __init__(
        self,
        tree: T,
        node_name_or_path: str = "",
        max_depth: int = 0,
        style: Union[
            str,
            Iterable[str],
            constants.BasePrintStyle,
            constants.BaseHPrintStyle,
            constants.BaseVPrintStyle,
        ] = "const",
        border_style: Optional[Union[str, Iterable[str], constants.BorderStyle]] = None,
    ):
        """Initialise yield tree class.

        Args:
            tree: tree to print
            node_name_or_path: node to print from, becomes the root node
            max_depth: maximum depth of tree to print, based on `depth` attribute
            style: style of print
            border_style: style of border
        """
        self._style_class: Type[constants.BaseStyle]
        tree = get_subtree(tree, node_name_or_path, max_depth)

        # Set style
        style_class = _get_style_class(self._style_class, style, "style")
        border_style_class: Optional[constants.BorderStyle] = None
        if border_style:
            border_style_class = _get_style_class(
                constants.BorderStyle, border_style, "border_style"
            )

        self.tree = tree
        self.style_class = style_class
        self.border_style_class = border_style_class
        self.space = " "

    def yield_tree(self, strip: bool) -> Union[List[str], Iterable[Tuple[str, str, T]]]:
        """Yield tree.

        Args:
            strip: whether to strip results

        Returns:
            List of tree string to print
        """
        raise NotImplementedError  # pragma: no cover


class YieldTree(BaseYieldTree):
    def __init__(
        self,
        tree: T,
        node_name_or_path: str = "",
        max_depth: int = 0,
        style: Union[str, Iterable[str], constants.BasePrintStyle] = "const",
    ):
        """Initialise yield tree class.

        Args:
            tree: tree to print
            node_name_or_path: node to print from, becomes the root node of printing
            max_depth: maximum depth of tree to print, based on `depth` attribute
            style: style of print
        """
        self._style_class = constants.BasePrintStyle
        super().__init__(tree, node_name_or_path, max_depth, style, None)
        self.style_class: constants.BasePrintStyle

    def yield_tree(self, strip: bool = True) -> Iterable[Tuple[str, str, T]]:
        """Yield tree.

        Args:
            strip: whether to strip results

        Returns:
            Iterable of tree string to print
        """
        space = self.space
        style_class: constants.BasePrintStyle = self.style_class

        gap_str = space * len(style_class.STEM)
        unclosed_depth = set()
        initial_depth = self.tree.depth
        for _node in iterators.preorder_iter(self.tree):
            pre_str = ""
            fill_str = ""
            if not _node.is_root:
                node_depth = _node.depth - initial_depth

                # Get fill_str (style_branch or style_stem_final)
                if _node.right_sibling:
                    unclosed_depth.add(node_depth)
                    fill_str = style_class.BRANCH
                else:
                    if node_depth in unclosed_depth:
                        unclosed_depth.remove(node_depth)
                    fill_str = style_class.STEM_FINAL

                # Get pre_str (style_stem, style_branch, style_stem_final, or gap)
                pre_str = ""
                for _depth in range(1, node_depth):
                    if _depth in unclosed_depth:
                        pre_str += style_class.STEM
                    else:
                        pre_str += gap_str

            yield pre_str, fill_str, _node


class HYieldTree(BaseYieldTree):
    def __init__(
        self,
        tree: T,
        alias: str = "node_name",
        node_name_or_path: str = "",
        max_depth: int = 0,
        intermediate_node_name: bool = True,
        spacing: int = 0,
        style: Union[str, Iterable[str], constants.BaseHPrintStyle] = "const",
        border_style: Optional[Union[str, Iterable[str], constants.BorderStyle]] = None,
    ):
        """Initialise yield tree class, yields tree in horizontal fashion.

        Args:
            tree: tree to print
            alias: node attribute to use for node name in tree as alias to `node_name`
            node_name_or_path: node to print from, becomes the root node of printing
            max_depth: maximum depth of tree to print, based on `depth` attribute
            intermediate_node_name: indicator if intermediate nodes have node names
            spacing: horizontal spacing between node displays
            style: style of print
            border_style: style of border
        """
        self._style_class = constants.BaseHPrintStyle
        super().__init__(tree, node_name_or_path, max_depth, style, border_style)
        self.style_class: constants.BaseHPrintStyle

        padding_depths = collections.defaultdict(int)
        if intermediate_node_name:
            for _idx, _children in enumerate(iterators.levelordergroup_iter(tree)):
                padding_depths[_idx + 1] = max(
                    [
                        len(
                            format_node(
                                _node,
                                alias,
                                intermediate_node_name,
                                self.style_class,
                                self.border_style_class,
                                add_buffer=False,
                            )[0]
                        )
                        for _node in _children
                    ]
                )
        self.padding_depths = padding_depths
        self.alias = alias
        self.intermediate_node_name = intermediate_node_name
        self.spacing = spacing

    def recursive(
        self, _node: Union[T, node.Node], _cur_depth: int
    ) -> Tuple[List[str], int]:
        """Get string for tree horizontally. Recursively iterate the nodes in post-order traversal manner.

        Args:
            _node: node to get string
            _cur_depth: current depth of node

        Returns:
            Intermediate/final result for node, index of branch
        """
        space = self.space
        style_class: constants.BaseHPrintStyle = self.style_class

        if not _node:
            # For binary node
            _node = node.Node(" ")
        node_display_lines = format_node(
            _node,
            self.alias,
            self.intermediate_node_name,
            self.style_class,
            self.border_style_class,
            self.padding_depths[_cur_depth],
        )
        node_mid = calculate_stem_pos(len(node_display_lines))

        children = list(_node.children) if any(list(_node.children)) else []
        if not len(children):
            return node_display_lines, node_mid

        result_children, result_idx = [], []
        cumulative_height = 0
        for idx, child in enumerate(children):
            result_child, result_branch_idx = self.recursive(child, _cur_depth + 1)
            result_idx.append(cumulative_height + result_branch_idx)
            cumulative_height += len(result_child)
            result_children.append(result_child)

        # Join children column
        children_display_lines = vertical_join(result_children)

        # Calculate index of first branch, last branch, total length, and midpoint
        first, last, total = (
            result_idx[0],
            result_idx[-1],
            len(children_display_lines),
        )
        mid = (first + last) // 2

        if len(children) == 1:
            # Special case for one child (need only one branch)
            line = space * first + style_class.BRANCH + space * (total - first - 1)
            line_prefix = line_suffix = line
        elif len(children) == 2 and (last - first == 1):
            # Special case for two children (need split_branch)
            # Create gap if two children occupy two rows
            children_display_lines.insert(last, "")
            last = first + 2
            mid = (last - first) // 2
            line_prefix = space * (first + 1) + style_class.BRANCH + space
            line = (
                space * first
                + style_class.FIRST_CHILD
                + style_class.SPLIT_BRANCH
                + style_class.LAST_CHILD
            )
            line_suffix = (
                space * first + style_class.BRANCH + space + style_class.BRANCH
            )
        else:
            line_prefix = space * (first + 1)
            line = space * first + style_class.FIRST_CHILD
            line_suffix = space * first + style_class.BRANCH
            for idx, (bef, aft) in enumerate(zip(result_idx, result_idx[1:])):
                line_prefix += space * (aft - bef)
                line += (
                    style_class.STEM * (aft - bef - 1) + style_class.SUBSEQUENT_CHILD
                )
                line_suffix += space * (aft - bef - 1) + style_class.BRANCH
            line = line[:-1] + style_class.LAST_CHILD
            line_suffix = line_suffix[:-1] + style_class.BRANCH
            if mid in result_idx:
                stem = style_class.MIDDLE_CHILD if mid else style_class.FIRST_CHILD
            else:
                stem = style_class.SPLIT_BRANCH
            line_prefix = (
                line_prefix[:mid] + style_class.BRANCH + line_prefix[mid + 1 :]  # noqa
            )
            line = line[:mid] + stem + line[mid + 1 :]  # noqa
        display_buffer = max(0, mid - node_mid)
        line_buffer = max(0, node_mid - mid)
        node_display_buffer = [len(node_display_lines[0]) * space] * display_buffer
        child_display_buffer = [len(children_display_lines[0]) * space] * line_buffer
        result = horizontal_join(
            [node_display_buffer + node_display_lines]
            + [list(" " * line_buffer + line_prefix)] * self.spacing
            + [list(" " * line_buffer + line)]
            + [list(" " * line_buffer + line_suffix)] * self.spacing
            + [child_display_buffer + children_display_lines]
        )
        return result, mid + line_buffer

    def yield_tree(self, strip: bool = True) -> List[str]:
        """Yield tree.

        Args:
            strip: whether to strip results

        Returns:
            List of tree string to print
        """
        result_tree, _ = self.recursive(self.tree, 1)
        if strip:
            return [result.rstrip() for result in result_tree]
        return result_tree


class VYieldTree(BaseYieldTree):
    def __init__(
        self,
        tree: T,
        alias: str = "node_name",
        node_name_or_path: str = "",
        max_depth: int = 0,
        intermediate_node_name: bool = True,
        spacing: int = 2,
        style: Union[str, Iterable[str], constants.BaseVPrintStyle] = "const",
        border_style: Optional[Union[str, Iterable[str], constants.BorderStyle]] = None,
    ):
        """Initialise yield tree class, yields tree in vertical fashion.

        Args:
            tree: tree to print
            alias: node attribute to use for node name in tree as alias to `node_name`
            node_name_or_path: node to print from, becomes the root node of printing
            max_depth: maximum depth of tree to print, based on `depth` attribute
            intermediate_node_name: indicator if intermediate nodes have node names
            spacing: horizontal spacing between node displays
            style: style of print
            border_style: style of border
        """
        self._style_class = constants.BaseVPrintStyle
        super().__init__(tree, node_name_or_path, max_depth, style, border_style)
        self.style_class: constants.BaseVPrintStyle
        self.alias = alias
        self.intermediate_node_name = intermediate_node_name
        self.spacing = spacing

    def recursive(self, _node: Union[T, node.Node]) -> Tuple[List[str], int]:
        """Get string for tree vertically. Recursively iterate the nodes in post-order traversal manner.

        Args:
            _node: node to get string

        Returns:
            Intermediate/final result for node, index of branch
        """
        space = self.space
        style_class: constants.BaseVPrintStyle = self.style_class

        if not _node:
            # For binary node
            _node = node.Node(" ", parent=node.Node(" "))
        node_display_lines = format_node(
            _node,
            self.alias,
            self.intermediate_node_name,
            self.style_class,
            self.border_style_class,
        )
        node_width = len(node_display_lines[0])
        node_mid = calculate_stem_pos(node_width)

        children = list(_node.children) if any(list(_node.children)) else []
        if not len(children):
            return node_display_lines, node_mid

        result_children, result_idx = [], []
        cumulative_width = 0
        for idx, child in enumerate(children):
            result_child, result_branch_idx = self.recursive(child)
            result_idx.append(cumulative_width + result_branch_idx)
            cumulative_width += len(result_child[0]) + self.spacing
            result_children.append(result_child)

        # Join children row
        children_display_lines = horizontal_join(result_children, self.spacing)

        # Calculate index of first branch, last branch, total length, and midpoint
        first, last, total = (
            result_idx[0],
            result_idx[-1],
            len(children_display_lines[0]),
        )
        mid = (first + last) // 2

        if len(children) == 1:
            # Special case for one child (need only one branch)
            line = space * first + style_class.BRANCH + space * (total - first - 1)
        else:
            line = space * first + style_class.FIRST_CHILD
            for idx, (bef, aft) in enumerate(zip(result_idx, result_idx[1:])):
                line += style_class.STEM * (aft - bef - 1)
                line += style_class.SUBSEQUENT_CHILD
            line = line[:-1] + style_class.LAST_CHILD
            line += space * (total - result_idx[-1] - 1)
            stem = (
                style_class.MIDDLE_CHILD
                if mid in result_idx
                else style_class.SPLIT_BRANCH
            )
            line = line[:mid] + stem + line[mid + 1 :]  # noqa
        display_buffer = max(0, mid - node_mid)
        line_buffer = max(0, node_mid - mid)
        result = vertical_join(
            [
                [
                    display_buffer * space + result_line
                    for result_line in node_display_lines
                ],
                [line_buffer * space + line],
                [
                    line_buffer * space + result_line
                    for result_line in children_display_lines
                ],
            ]
        )
        return result, mid + line_buffer

    def yield_tree(self, strip: bool = False) -> List[str]:
        """Yield tree.

        Args:
            strip: whether to strip results

        Returns:
            List of tree string to print
        """
        result_tree, _ = self.recursive(self.tree)
        if strip:
            return [result.rstrip() for result in result_tree]
        return result_tree

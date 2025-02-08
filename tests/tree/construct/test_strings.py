import unittest

import pytest

from bigtree.node import node
from bigtree.tree import construct
from bigtree.utils import exceptions
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
)
from tests.node.test_node import (
    assert_tree_structure_node_root,
    assert_tree_structure_node_root_sep,
)
from tests.test_constants import Constants
from tests.tree.construct.conftest import NodeA


class TestAddPathToTree(unittest.TestCase):
    def setUp(self):
        """
        Tree should have structure
        a
        |-- b
        |   |-- d
        |   +-- e
        |       |-- g
        |       +-- h
        +-- c
            +-- f
        """
        self.root = node.Node("a")
        self.path_list = ["a/b/d", "a/b/e", "a/b/e/g", "a/b/e/h", "a/c/f"]

    def tearDown(self):
        self.root = None
        self.path_list = None

    def test_add_path_to_tree(self):
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/f",
            "a/b/e/g",
            "a/b/e/h",
        ]
        for path in path_list:
            construct.add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_leaves(self):
        for path in self.path_list:
            construct.add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.add_path_to_tree(self.root, "")
        assert str(exc_info.value) == Constants.ERROR_NODE_PATH_EMPTY

    def test_add_path_to_tree_sep_leading(self):
        path_list = ["/a/b/d", "/a/b/e", "/a/b/e/g", "/a/b/e/h", "/a/c/f"]
        for path in path_list:
            construct.add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_sep_trailing(self):
        path_list = ["a/b/d/", "a/b/e/", "a/b/e/g/", "a/b/e/h/", "a/c/f/"]
        for path in path_list:
            construct.add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_sep_error(self):
        root1 = self.root.node_name
        root2 = "a\\b\\d"
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]

        with pytest.raises(exceptions.TreeError) as exc_info:
            for path in path_list:
                construct.add_path_to_tree(self.root, path)
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )

    def test_add_path_to_tree_sep(self):
        path_list = ["a\\b\\d", "a\\b\\e", "a\\b\\e\\g", "a\\b\\e\\h", "a\\c\\f"]

        for path in path_list:
            construct.add_path_to_tree(self.root, path, sep="\\")
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_sep_tree(self):
        self.root.sep = "\\"

        for path in self.path_list:
            construct.add_path_to_tree(self.root, path)
        assert_tree_structure_node_root_sep(self.root)

    def test_add_path_to_tree_duplicate_node_error(self):
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/d",  # duplicate
            "a/b/e/g",
            "a/b/e/h",
        ]

        with pytest.raises(exceptions.DuplicatedNodeError) as exc_info:
            for path in path_list:
                construct.add_path_to_tree(
                    self.root, path, duplicate_name_allowed=False
                )
        assert str(exc_info.value) == Constants.ERROR_NODE_DUPLICATE_NAME.format(
            name="d"
        )

    def test_add_path_to_tree_duplicate_node(self):
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/d",  # duplicate
            "a/b/e/g",
            "a/b/e/h",
        ]

        for path in path_list:
            construct.add_path_to_tree(self.root, path)
        assert_tree_structure_basenode_root(self.root)
        assert_tree_structure_node_root(self.root, f="/a/c/d")

    def test_add_path_to_tree_node_type(self):
        root = NodeA("a")
        for path in self.path_list:
            construct.add_path_to_tree(root, path)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(self.root)

    def test_add_path_to_tree_different_root_error(self):
        root1 = self.root.node_name
        root2 = "a/b"
        path_list = [
            "a",
            "a/b",
            "a/c",
            "a/b/d",
            "a/b/e",
            "a/c/f",
            "a/b/e/g",
            "a/b/e/h",
        ]
        with pytest.raises(exceptions.TreeError) as exc_info:
            for path in path_list:
                construct.add_path_to_tree(self.root, path, sep="-")
        assert str(exc_info.value) == Constants.ERROR_NODE_DIFFERENT_ROOT.format(
            root1=root1, root2=root2
        )


class TestStrToTree(unittest.TestCase):
    def setUp(self):
        """
        Tree should have structure
        a
        |-- b
        |   |-- d
        |   +-- e
        |       |-- g
        |       +-- h
        +-- c
            +-- f
        """
        self.tree_str = "a\n├── b\n│   ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f"

    def test_str_to_tree(self):
        root = construct.str_to_tree(self.tree_str)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_str_to_tree_with_prefix(self):
        root = construct.str_to_tree(self.tree_str, tree_prefix_list=["─"])
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_str_to_tree_with_multiple_prefix(self):
        root = construct.str_to_tree(self.tree_str, tree_prefix_list=["├──", "└──"])
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_ascii_character_error(self):
        node_str = "|-- b"
        tree_str = "a\n|-- b\n|   |-- d\n|   +-- e\n|       |-- g\n|       +-- h\n+-- c\n    +-- f"
        with pytest.raises(ValueError) as exc_info:
            construct.str_to_tree(tree_str)
        assert str(exc_info.value) == Constants.ERROR_NODE_STRING_PREFIX.format(
            node_str=node_str
        )

    def test_ascii_character_with_prefix(self):
        tree_str = "a\n|-- b\n|   |-- d\n|   +-- e\n|       |-- g\n|       +-- h\n+-- c\n    +-- f"
        root = construct.str_to_tree(tree_str, tree_prefix_list=["-"])
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_empty_string_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.str_to_tree("")
        assert str(exc_info.value) == Constants.ERROR_NODE_STRING_EMPTY

    def test_empty_newline_string_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.str_to_tree("\n\n")
        assert str(exc_info.value) == Constants.ERROR_NODE_STRING_EMPTY

    def test_unequal_prefix_length_error(self):
        branch = "│  ├── d"
        tree_str = "a\n├── b\n│  ├── d\n│   └── e\n│       ├── g\n│       └── h\n└── c\n    └── f"
        with pytest.raises(ValueError) as exc_info:
            construct.str_to_tree(tree_str)
        assert str(exc_info.value) == Constants.ERROR_NODE_STRING_PREFIX_LENGTH.format(
            branch=branch
        )


class TestNewickToTree(unittest.TestCase):
    def setUp(self):
        self.newick_str = "((d,(g,h)e)b,(f)c)a"
        self.newick_str_with_attr = "((d[&&NHX:age=40],(g[&&NHX:age=10],h[&&NHX:age=6])e[&&NHX:age=35])b[&&NHX:age=65],(f[&&NHX:age=38])c[&&NHX:age=60])a[&&NHX:age=90]"

    def tearDown(self):
        self.newick_str = None
        self.newick_str_with_attr = None

    def test_newick_to_tree(self):
        root = construct.newick_to_tree(self.newick_str)
        assert_tree_structure_basenode_root(root)

    def test_newick_to_tree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            construct.newick_to_tree("")
        assert str(exc_info.value) == Constants.ERROR_NODE_STRING_EMPTY

    def test_newick_to_tree_bracket_error(self):
        newick_strs_error = [
            (
                "((d:40[age=4(0],(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                12,
            ),  # NewickCharacter.OPEN_BRACKET, state
            (
                "((d:(40,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                4,
            ),  # NewickCharacter.OPEN_BRACKET, current_node
            (
                "((d(:40,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                3,
            ),  # NewickCharacter.OPEN_BRACKET, cumulative_string
            (
                "((d:40[age=),(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                11,
            ),  # NewickCharacter.CLOSE_BRACKET, state
            (
                "((d]:40,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                3,
            ),  # NewickCharacter.ATTR_END, state
            (
                "((d=:40,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                3,
            ),  # NewickCharacter.ATTR_KEY_VALUE, state
            (
                "((d:40[=,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                7,
            ),  # NewickCharacter.ATTR_KEY_VALUE, cumulative_string
            (
                "(('d:40[age=40],(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                2,
            ),  # NewickCharacter.ATTR_QUOTE, no end quote
            (
                "((d:40[a:ge=40],(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                8,
            ),  # NewickCharacter.SEP, state
            (
                "((d::40[age=40],(g:10,h:6)e:35)b:65,(f:38)c:60)a:90",
                4,
            ),  # NewickCharacter.SEP, current_node
            (
                "((d:40,(g:10,h:6)e:35)b:65,(f:38)c:60",
                37,
            ),  # final depth
        ]
        for newick_str, error_idx in newick_strs_error:
            with pytest.raises(ValueError) as exc_info:
                construct.newick_to_tree(newick_str)
            assert str(exc_info.value) == Constants.ERROR_NODE_NEWICK_NOT_CLOSED.format(
                index=error_idx
            )

    def test_newick_to_tree_length(self):
        newick_str_length = "((d:40,(g:10,h:6)e:35)b:65,(f:38)c:60)a:90"
        root = construct.newick_to_tree(newick_str_length, length_attr="age")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(root)
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_attr(self):
        root = construct.newick_to_tree(self.newick_str_with_attr)
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(
            root,
            a=("a", "90"),
            b=("b", "65"),
            c=("c", "60"),
            d=("d", "40"),
            e=("e", "35"),
            f=("f", "38"),
            g=("g", "10"),
            h=("h", "6"),
        )
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_attr_no_prefix(self):
        newick_str_no_attr_prefix = "((d[age=40],(g[age=10],h[age=6])e[age=35])b[age=65],(f[age=38])c[age=60])a[age=90]"
        root = construct.newick_to_tree(newick_str_no_attr_prefix, attr_prefix="")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(
            root,
            a=("a", "90"),
            b=("b", "65"),
            c=("c", "60"),
            d=("d", "40"),
            e=("e", "35"),
            f=("f", "38"),
            g=("g", "10"),
            h=("h", "6"),
        )
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_quote_name(self):
        newick_str_no_attr_prefix = "((d[age=40],('(g)'[age=10],h[age=6])e[age=35])b[age=65],(f[age=38])c[age=60])a[age=90]"
        root = construct.newick_to_tree(newick_str_no_attr_prefix, attr_prefix="")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(
            root,
            a=("a", "90"),
            b=("b", "65"),
            c=("c", "60"),
            d=("d", "40"),
            e=("e", "35"),
            f=("f", "38"),
            g=("(g)", "10"),
            h=("h", "6"),
        )
        assert_tree_structure_node_root(root, g="/a/b/e/(g)")

    def test_newick_to_tree_quote_attr_name(self):
        newick_str_no_attr_prefix = "((d[age=40],(g['(age)'=10],h[age=6])e[age=35])b[age=65],(f[age=38])c[age=60])a[age=90]"
        root = construct.newick_to_tree(newick_str_no_attr_prefix, attr_prefix="")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_quote_attr_value(self):
        newick_str_no_attr_prefix = "((d[age=40],(g[age='[10]'],h[age=6])e[age=35])b[age=65],(f[age=38])c[age=60])a[age=90]"
        root = construct.newick_to_tree(newick_str_no_attr_prefix, attr_prefix="")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(
            root,
            a=("a", "90"),
            b=("b", "65"),
            c=("c", "60"),
            d=("d", "40"),
            e=("e", "35"),
            f=("f", "38"),
            g=("g", "[10]"),
            h=("h", "6"),
        )
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_phylogenetic(self):
        newick_str_phylogenetic = "(((ADH2:0.1[&&NHX:S=human:E=1.1.1.1],ADH1:0.11[&&NHX:S=human:E=1.1.1.1]):0.05[&&NHX:S=Primates:E=1.1.1.1:D=Y:B=100],ADHY:0.1[&&NHX:S=nematode:E=1.1.1.1],ADHX:0.12[&&NHX:S=insect:E=1.1.1.1]):0.1[&&NHX:S=Metazoa:E=1.1.1.1:D=N],(ADH4:0.09[&&NHX:S=yeast:E=1.1.1.1],ADH3:0.13[&&NHX:S=yeast:E=1.1.1.1],ADH2:0.12[&&NHX:S=yeast:E=1.1.1.1],ADH1:0.11[&&NHX:S=yeast:E=1.1.1.1]):0.1[&&NHX:S=Fungi])[&&NHX:E=1.1.1.1:D=N]"
        root = construct.newick_to_tree(newick_str_phylogenetic, length_attr="length")
        assert_tree_structure_phylogenetic(root)
        assert_tree_structure_phylogenetic_attr(root)

    def test_newick_to_tree_phylogenetic_no_length_attr(self):
        newick_str_phylogenetic = "(((ADH2:0.1[&&NHX:S=human:E=1.1.1.1],ADH1:0.11[&&NHX:S=human:E=1.1.1.1]):0.05[&&NHX:S=Primates:E=1.1.1.1:D=Y:B=100],ADHY:0.1[&&NHX:S=nematode:E=1.1.1.1],ADHX:0.12[&&NHX:S=insect:E=1.1.1.1]):0.1[&&NHX:S=Metazoa:E=1.1.1.1:D=N],(ADH4:0.09[&&NHX:S=yeast:E=1.1.1.1],ADH3:0.13[&&NHX:S=yeast:E=1.1.1.1],ADH2:0.12[&&NHX:S=yeast:E=1.1.1.1],ADH1:0.11[&&NHX:S=yeast:E=1.1.1.1]):0.1[&&NHX:S=Fungi])[&&NHX:E=1.1.1.1:D=N]"
        root = construct.newick_to_tree(newick_str_phylogenetic)
        assert_tree_structure_phylogenetic(root)
        assert_tree_structure_phylogenetic_attr(root, attrs=["B", "D", "E", "S"])

    def test_newick_to_tree_node_type(self):
        root = construct.newick_to_tree(self.newick_str_with_attr, node_type=NodeA)
        assert isinstance(root, NodeA), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert all(
            isinstance(_node, NodeA) for _node in root.children
        ), Constants.ERROR_CUSTOM_TYPE.format(type="NodeA")
        assert_tree_structure_basenode_root(root)
        assert_tree_structure_basenode_root_attr(
            root,
            a=("a", "90"),
            b=("b", "65"),
            c=("c", "60"),
            d=("d", "40"),
            e=("e", "35"),
            f=("f", "38"),
            g=("g", "10"),
            h=("h", "6"),
        )
        assert_tree_structure_node_root(root)

    def test_newick_to_tree_invalid_character_error(self):
        newick_strs_error = [
            (
                """((d,(g,h)e)b,(f)c)"'a'\"""",
                19,
            ),  # NewickCharacter.ATTR_QUOTE, wrong order of bracket (name)
            (
                """((d,(g,h)e)b,(f[age="'38'"])c)a""",
                21,
            ),  # NewickCharacter.ATTR_QUOTE, wrong order of bracket (attr value)
        ]
        for newick_str, error_idx in newick_strs_error:
            with pytest.raises(ValueError) as exc_info:
                construct.newick_to_tree(newick_str)
            assert str(exc_info.value) == Constants.ERROR_NODE_NEWICK_NOT_CLOSED.format(
                index=error_idx
            )


def assert_tree_structure_phylogenetic(root):
    assert root.max_depth == 4, f"Expected max_depth 4, received {root.max_depth}"
    assert (
        len(list(root.descendants)) == 11
    ), f"Expected 11 descendants, received {len(root.descendants)}"
    assert root.node_name == "node3"
    assert [_node.node_name for _node in root.children] == ["node1", "node2"]
    assert [_node.node_name for _node in root["node1"].children] == [
        "node0",
        "ADHY",
        "ADHX",
    ]
    assert [_node.node_name for _node in root["node1"]["node0"].children] == [
        "ADH2",
        "ADH1",
    ]
    assert [_node.node_name for _node in root["node2"].children] == [
        "ADH4",
        "ADH3",
        "ADH2",
        "ADH1",
    ]


def assert_tree_structure_phylogenetic_attr(root, attrs=["B", "D", "E", "S", "length"]):
    from bigtree.utils.iterators import preorder_iter

    if "B" in attrs:
        expected = [
            None,
            None,
            "100",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
        actual = [_node.get_attr("B") for _node in preorder_iter(root)]
        assert expected == actual, f"Expected B to be {expected}, received {actual}"
    if "D" in attrs:
        expected = ["N", "N", "Y", None, None, None, None, None, None, None, None, None]
        actual = [_node.get_attr("D") for _node in preorder_iter(root)]
        assert expected == actual, f"Expected D to be {expected}, received {actual}"
    if "E" in attrs:
        expected = [
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            None,
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
            "1.1.1.1",
        ]
        actual = [_node.get_attr("E") for _node in preorder_iter(root)]
        assert expected == actual, f"Expected E to be {expected}, received {actual}"
    if "S" in attrs:
        expected = [
            None,
            "Metazoa",
            "Primates",
            "human",
            "human",
            "nematode",
            "insect",
            "Fungi",
            "yeast",
            "yeast",
            "yeast",
            "yeast",
        ]
        actual = [_node.get_attr("S") for _node in preorder_iter(root)]
        assert expected == actual, f"Expected S to be {expected}, received {actual}"
    if "length" in attrs:
        expected = [None, 0.1, 0.05, 0.1, 0.11, 0.1, 0.12, 0.1, 0.09, 0.13, 0.12, 0.11]
        actual = [_node.get_attr("length") for _node in preorder_iter(root)]
        assert (
            expected == actual
        ), f"Expected length to be {expected}, received {actual}"

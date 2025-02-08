import unittest

import pandas as pd
import polars as pl

from bigtree.tree import export
from tests.node.test_basenode import (
    assert_tree_structure_basenode_root,
    assert_tree_structure_basenode_root_attr,
)
from tests.node.test_node import assert_tree_structure_node_root


class TestTreeToDataFrame:
    @staticmethod
    def test_tree_to_dataframe(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a"],
                ["/a/b", "b"],
                ["/a/b/d", "d"],
                ["/a/b/e", "e"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c", "c"],
                ["/a/c/f", "f"],
            ],
            columns=["path", "name"],
        )
        actual = export.tree_to_dataframe(tree_node)
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_path_col(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a"],
                ["/a/b", "b"],
                ["/a/b/d", "d"],
                ["/a/b/e", "e"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c", "c"],
                ["/a/c/f", "f"],
            ],
            columns=["PATH", "name"],
        )
        actual = export.tree_to_dataframe(tree_node, path_col="PATH")
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_path_col_missing(tree_node):
        expected = pd.DataFrame(
            [
                ["a"],
                ["b"],
                ["d"],
                ["e"],
                ["g"],
                ["h"],
                ["c"],
                ["f"],
            ],
            columns=["name"],
        )
        actual = export.tree_to_dataframe(tree_node, path_col="")
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_name_col(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a"],
                ["/a/b", "b"],
                ["/a/b/d", "d"],
                ["/a/b/e", "e"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c", "c"],
                ["/a/c/f", "f"],
            ],
            columns=["path", "NAME"],
        )
        actual = export.tree_to_dataframe(tree_node, name_col="NAME")
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_name_col_missing(tree_node):
        expected = pd.DataFrame(
            [
                ["/a"],
                ["/a/b"],
                ["/a/b/d"],
                ["/a/b/e"],
                ["/a/b/e/g"],
                ["/a/b/e/h"],
                ["/a/c"],
                ["/a/c/f"],
            ],
            columns=["path"],
        )
        actual = export.tree_to_dataframe(tree_node, name_col="")
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_name_path_col_missing(tree_node):
        expected = pd.DataFrame()
        expected.index = range(8)
        actual = export.tree_to_dataframe(tree_node, name_col="", path_col="")
        pd.testing.assert_frame_equal(expected, actual, check_column_type=False)

    @staticmethod
    def test_tree_to_dataframe_parent_col(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a", None],
                ["/a/b", "b", "a"],
                ["/a/b/d", "d", "b"],
                ["/a/b/e", "e", "b"],
                ["/a/b/e/g", "g", "e"],
                ["/a/b/e/h", "h", "e"],
                ["/a/c", "c", "a"],
                ["/a/c/f", "f", "c"],
            ],
            columns=["path", "name", "parent"],
        )
        actual = export.tree_to_dataframe(tree_node, parent_col="parent")
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_attr_dict(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a", 90],
                ["/a/b", "b", 65],
                ["/a/b/d", "d", 40],
                ["/a/b/e", "e", 35],
                ["/a/b/e/g", "g", 10],
                ["/a/b/e/h", "h", 6],
                ["/a/c", "c", 60],
                ["/a/c/f", "f", 38],
            ],
            columns=["path", "name", "AGE"],
        )
        actual = export.tree_to_dataframe(tree_node, attr_dict={"age": "AGE"})
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_all_attr(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a", 90],
                ["/a/b", "b", 65],
                ["/a/b/d", "d", 40],
                ["/a/b/e", "e", 35],
                ["/a/b/e/g", "g", 10],
                ["/a/b/e/h", "h", 6],
                ["/a/c", "c", 60],
                ["/a/c/f", "f", 38],
            ],
            columns=["path", "name", "age"],
        )
        actual = export.tree_to_dataframe(tree_node, all_attrs=True)
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_max_depth(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a"],
                ["/a/b", "b"],
                ["/a/c", "c"],
            ],
            columns=["path", "name"],
        )
        actual = export.tree_to_dataframe(tree_node, max_depth=2)
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_skip_depth(tree_node):
        expected = pd.DataFrame(
            [
                ["/a/b/d", "d"],
                ["/a/b/e", "e"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c/f", "f"],
            ],
            columns=["path", "name"],
        )
        actual = export.tree_to_dataframe(tree_node, skip_depth=2)
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_leaf_only(tree_node):
        expected = pd.DataFrame(
            [
                ["/a/b/d", "d"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c/f", "f"],
            ],
            columns=["path", "name"],
        )
        actual = export.tree_to_dataframe(tree_node, leaf_only=True)
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_multiple_columns(tree_node):
        expected = pd.DataFrame(
            [
                ["/a", "a", None, 90],
                ["/a/b", "b", "a", 65],
                ["/a/b/d", "d", "b", 40],
                ["/a/b/e", "e", "b", 35],
                ["/a/b/e/g", "g", "e", 10],
                ["/a/b/e/h", "h", "e", 6],
                ["/a/c", "c", "a", 60],
                ["/a/c/f", "f", "c", 38],
            ],
            columns=["PATH", "NAME", "PARENT", "AGE"],
        )
        actual = export.tree_to_dataframe(
            tree_node,
            name_col="NAME",
            path_col="PATH",
            parent_col="PARENT",
            attr_dict={"age": "AGE"},
        )
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_multiple_cols_subset_tree(tree_node):
        expected = pd.DataFrame(
            [
                ["/a/b", "b", "a", 65],
                ["/a/b/d", "d", "b", 40],
                ["/a/b/e", "e", "b", 35],
                ["/a/b/e/g", "g", "e", 10],
                ["/a/b/e/h", "h", "e", 6],
            ],
            columns=["PATH", "NAME", "PARENT", "AGE"],
        )
        actual = export.tree_to_dataframe(
            tree_node.children[0],
            name_col="NAME",
            path_col="PATH",
            parent_col="PARENT",
            attr_dict={"age": "AGE"},
        )
        pd.testing.assert_frame_equal(expected, actual)

    @staticmethod
    def test_tree_to_dataframe_to_tree(tree_node):
        from bigtree.tree.construct import dataframe_to_tree

        d = export.tree_to_dataframe(tree_node, all_attrs=True)
        tree = dataframe_to_tree(d)
        assert_tree_structure_basenode_root(tree)
        assert_tree_structure_basenode_root_attr(tree)
        assert_tree_structure_node_root(tree)


class TestTreeToPolars:
    @staticmethod
    def test_tree_to_polars(tree_node):
        expected = pl.DataFrame(
            [
                ["/a", "a"],
                ["/a/b", "b"],
                ["/a/b/d", "d"],
                ["/a/b/e", "e"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c", "c"],
                ["/a/c/f", "f"],
            ],
            schema=["path", "name"],
        )
        actual = export.tree_to_polars(tree_node)
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_path_col(tree_node):
        expected = pl.DataFrame(
            [
                ["/a", "a"],
                ["/a/b", "b"],
                ["/a/b/d", "d"],
                ["/a/b/e", "e"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c", "c"],
                ["/a/c/f", "f"],
            ],
            schema=["PATH", "name"],
        )
        actual = export.tree_to_polars(tree_node, path_col="PATH")
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_path_col_missing(tree_node):
        expected = pl.DataFrame(
            [
                ["a"],
                ["b"],
                ["d"],
                ["e"],
                ["g"],
                ["h"],
                ["c"],
                ["f"],
            ],
            schema=["name"],
        )
        actual = export.tree_to_polars(tree_node, path_col="")
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_name_col(tree_node):
        expected = pl.DataFrame(
            [
                ["/a", "a"],
                ["/a/b", "b"],
                ["/a/b/d", "d"],
                ["/a/b/e", "e"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c", "c"],
                ["/a/c/f", "f"],
            ],
            schema=["path", "NAME"],
        )
        actual = export.tree_to_polars(tree_node, name_col="NAME")
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_name_col_missing(tree_node):
        expected = pl.DataFrame(
            [
                ["/a"],
                ["/a/b"],
                ["/a/b/d"],
                ["/a/b/e"],
                ["/a/b/e/g"],
                ["/a/b/e/h"],
                ["/a/c"],
                ["/a/c/f"],
            ],
            schema=["path"],
        )
        actual = export.tree_to_polars(tree_node, name_col="")
        assert expected.equals(actual)

    @staticmethod
    @unittest.skipIf(
        tuple(map(int, pl.__version__.split(".")[:2])) > (1, 9),
        reason="Not compatible with polars>1.9.0",
    )
    def test_tree_to_polars_name_path_col_missing_old_polars(tree_node):
        actual = export.tree_to_polars(tree_node, name_col="", path_col="")
        assert actual.is_empty()
        assert actual.shape == (0, 0)

    @staticmethod
    @unittest.skipIf(
        tuple(map(int, pl.__version__.split(".")[:2])) <= (1, 9),
        reason="Not compatible with polars<=1.9.0",
    )
    def test_tree_to_polars_name_path_col_missing(tree_node):
        actual = export.tree_to_polars(tree_node, name_col="", path_col="")
        assert actual.is_empty()
        assert actual.shape == (8, 0)

    @staticmethod
    def test_tree_to_polars_parent_col(tree_node):
        expected = pl.DataFrame(
            [
                ["/a", "a", None],
                ["/a/b", "b", "a"],
                ["/a/b/d", "d", "b"],
                ["/a/b/e", "e", "b"],
                ["/a/b/e/g", "g", "e"],
                ["/a/b/e/h", "h", "e"],
                ["/a/c", "c", "a"],
                ["/a/c/f", "f", "c"],
            ],
            schema=["path", "name", "parent"],
        )
        actual = export.tree_to_polars(tree_node, parent_col="parent")
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_attr_dict(tree_node):
        expected = pl.DataFrame(
            [
                ["/a", "a", 90],
                ["/a/b", "b", 65],
                ["/a/b/d", "d", 40],
                ["/a/b/e", "e", 35],
                ["/a/b/e/g", "g", 10],
                ["/a/b/e/h", "h", 6],
                ["/a/c", "c", 60],
                ["/a/c/f", "f", 38],
            ],
            schema=["path", "name", "AGE"],
        )
        actual = export.tree_to_polars(tree_node, attr_dict={"age": "AGE"})
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_all_attr(tree_node):
        expected = pl.DataFrame(
            [
                ["/a", "a", 90],
                ["/a/b", "b", 65],
                ["/a/b/d", "d", 40],
                ["/a/b/e", "e", 35],
                ["/a/b/e/g", "g", 10],
                ["/a/b/e/h", "h", 6],
                ["/a/c", "c", 60],
                ["/a/c/f", "f", 38],
            ],
            schema=["path", "name", "age"],
        )
        actual = export.tree_to_polars(tree_node, all_attrs=True)
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_max_depth(tree_node):
        expected = pl.DataFrame(
            [
                ["/a", "a"],
                ["/a/b", "b"],
                ["/a/c", "c"],
            ],
            schema=["path", "name"],
        )
        actual = export.tree_to_polars(tree_node, max_depth=2)
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_skip_depth(tree_node):
        expected = pl.DataFrame(
            [
                ["/a/b/d", "d"],
                ["/a/b/e", "e"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c/f", "f"],
            ],
            schema=["path", "name"],
        )
        actual = export.tree_to_polars(tree_node, skip_depth=2)
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_leaf_only(tree_node):
        expected = pl.DataFrame(
            [
                ["/a/b/d", "d"],
                ["/a/b/e/g", "g"],
                ["/a/b/e/h", "h"],
                ["/a/c/f", "f"],
            ],
            schema=["path", "name"],
        )
        actual = export.tree_to_polars(tree_node, leaf_only=True)
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_multiple_columns(tree_node):
        expected = pl.DataFrame(
            [
                ["/a", "a", None, 90],
                ["/a/b", "b", "a", 65],
                ["/a/b/d", "d", "b", 40],
                ["/a/b/e", "e", "b", 35],
                ["/a/b/e/g", "g", "e", 10],
                ["/a/b/e/h", "h", "e", 6],
                ["/a/c", "c", "a", 60],
                ["/a/c/f", "f", "c", 38],
            ],
            schema=["PATH", "NAME", "PARENT", "AGE"],
        )
        actual = export.tree_to_polars(
            tree_node,
            name_col="NAME",
            path_col="PATH",
            parent_col="PARENT",
            attr_dict={"age": "AGE"},
        )
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_multiple_cols_subset_tree(tree_node):
        expected = pl.DataFrame(
            [
                ["/a/b", "b", "a", 65],
                ["/a/b/d", "d", "b", 40],
                ["/a/b/e", "e", "b", 35],
                ["/a/b/e/g", "g", "e", 10],
                ["/a/b/e/h", "h", "e", 6],
            ],
            schema=["PATH", "NAME", "PARENT", "AGE"],
        )
        actual = export.tree_to_polars(
            tree_node.children[0],
            name_col="NAME",
            path_col="PATH",
            parent_col="PARENT",
            attr_dict={"age": "AGE"},
        )
        assert expected.equals(actual)

    @staticmethod
    def test_tree_to_polars_to_tree(tree_node):
        from bigtree.tree.construct import polars_to_tree

        d = export.tree_to_polars(tree_node, all_attrs=True)
        tree = polars_to_tree(d)
        assert_tree_structure_basenode_root(tree)
        assert_tree_structure_basenode_root_attr(tree)
        assert_tree_structure_node_root(tree)

import unittest

import pytest

from bigtree.binarytree import construct as binarytree_construct
from bigtree.node import binarynode
from tests.node.test_binarynode import assert_binarytree_structure_root2
from tests.test_constants import Constants


class BinaryNodeA(binarynode.BinaryNode):
    pass


class TestListToBinaryTree(unittest.TestCase):
    def setUp(self):
        self.nums_list = [1, 2, 3, 4, 5, 6, 7, 8]

    def tearDown(self):
        self.nums_list = None

    def test_list_to_binarytree(self):
        root = binarytree_construct.list_to_binarytree(self.nums_list)
        assert_binarytree_structure_root2(root)

    def test_list_to_binarytree_empty_error(self):
        with pytest.raises(ValueError) as exc_info:
            binarytree_construct.list_to_binarytree([])
        assert str(exc_info.value) == Constants.ERROR_BINARY_DAG_LIST_EMPTY.format(
            parameter="heapq_list"
        )

    def test_list_to_binarytree_node_type(self):
        root = binarytree_construct.list_to_binarytree(
            self.nums_list, node_type=BinaryNodeA
        )
        assert isinstance(root, BinaryNodeA), Constants.ERROR_CUSTOM_TYPE.format(
            type="BinaryNodeA"
        )
        assert_binarytree_structure_root2(root)

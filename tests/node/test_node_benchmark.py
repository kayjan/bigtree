import sys
from unittest.mock import patch

import pytest

from bigtree.node import node

sys.setrecursionlimit(2000)


def run_construct_node(
    depth: int, width: int = 1, parent_node: node.Node = None
) -> node.Node:
    """Create a balanced tree of depth `depth` and width `width`

    Args:
        depth (int): depth of tree
        width (int): width of tree, number of children of every node
        parent_node (Node): current parent node, used for recursion

    Returns:
        (Node)
    """
    if depth > 0:
        for _width in range(width):
            new_node = node.Node(f"{depth}.{_width}", parent=parent_node)
            run_construct_node(depth - 1, width, new_node)
        return new_node


@pytest.mark.benchmark(group="width_1_depth_10")
def test_node_benchmark_width_1_depth_10(benchmark):
    benchmark.pedantic(run_construct_node, (10, 1), iterations=10, rounds=2)


@pytest.mark.benchmark(group="width_1_depth_100")
def test_node_benchmark_width_1_depth_100(benchmark):
    benchmark.pedantic(run_construct_node, (100, 1), iterations=10, rounds=2)


@pytest.mark.benchmark(group="width_1_depth_1000")
def test_node_benchmark_width_1_depth_1000(benchmark):
    benchmark.pedantic(run_construct_node, (1000, 1), iterations=10, rounds=2)


@pytest.mark.benchmark(group="width_2_depth_10")
def test_node_benchmark_width_2_depth_10(benchmark):
    benchmark.pedantic(run_construct_node, (10, 2), iterations=10, rounds=2)


@pytest.mark.benchmark(group="width_1_depth_10")
@patch("bigtree.node.basenode.ASSERTIONS", "")
def test_node_benchmark_width_1_depth_10_no_assertions(benchmark):
    benchmark.pedantic(run_construct_node, (10, 1), iterations=10, rounds=2)


@pytest.mark.benchmark(group="width_1_depth_100")
@patch("bigtree.node.basenode.ASSERTIONS", "")
def test_node_benchmark_width_1_depth_100_no_assertions(benchmark):
    benchmark.pedantic(run_construct_node, (100, 1), iterations=10, rounds=2)


@pytest.mark.benchmark(group="width_1_depth_1000")
@patch("bigtree.node.basenode.ASSERTIONS", "")
def test_node_benchmark_width_1_depth_1000_no_assertions(benchmark):
    benchmark.pedantic(run_construct_node, (1000, 1), iterations=10, rounds=2)


@pytest.mark.benchmark(group="width_2_depth_10")
@patch("bigtree.node.basenode.ASSERTIONS", "")
def test_node_benchmark_width_2_depth_10_no_assertions(benchmark):
    benchmark.pedantic(run_construct_node, (10, 2), iterations=10, rounds=2)

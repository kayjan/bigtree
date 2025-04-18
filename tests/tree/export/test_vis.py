from bigtree.tree import export
from tests.test_constants import Constants

LOCAL = Constants.LOCAL


class TestTreeToVis:
    @staticmethod
    def test_tree_to_vis(tree_node):
        net = export.tree_to_vis(tree_node)
        if LOCAL:
            net.save_graph("tests/test_tree_to_vis.html")

    @staticmethod
    def test_tree_to_vis_big(tree_node_big):
        net = export.tree_to_vis(tree_node_big)
        if LOCAL:
            net.save_graph("tests/test_tree_to_vis_big.html")

    @staticmethod
    def test_tree_to_vis_custom_node_kwargs(tree_node):
        tree_node.set_attrs({"node_colour": "yellow"})
        net = export.tree_to_vis(tree_node, custom_node_kwargs={"color": "node_colour"})
        if LOCAL:
            net.save_graph("tests/test_tree_to_vis_custom_node_kwargs.html")

    @staticmethod
    def test_tree_to_vis_custom_node_kwargs_override(tree_node):
        node_kwargs = dict(color="black")
        tree_node.set_attrs({"node_colour": "yellow"})
        net = export.tree_to_vis(
            tree_node,
            custom_node_kwargs={"color": "node_colour"},
            node_kwargs=node_kwargs,
        )
        if LOCAL:
            net.save_graph("tests/test_tree_to_vis_custom_node_kwargs_override.html")

    @staticmethod
    def test_tree_to_vis_node_kwargs(tree_node):
        node_kwargs = dict(color="black")
        net = export.tree_to_vis(tree_node, node_kwargs=node_kwargs)
        if LOCAL:
            net.save_graph("tests/test_tree_to_vis_node_kwargs.html")

    @staticmethod
    def test_tree_to_vis_custom_edge_kwargs(tree_node):
        tree_node["b"].set_attrs({"node_weight": 10})
        net = export.tree_to_vis(tree_node, custom_edge_kwargs={"width": "node_weight"})
        if LOCAL:
            net.save_graph("tests/test_tree_to_vis_custom_edge_kwargs.html")

    @staticmethod
    def test_tree_to_vis_custom_edge_kwargs_override(tree_node):
        tree_node["b"].set_attrs({"node_weight": 10})
        edge_kwargs = dict(width=5)
        net = export.tree_to_vis(
            tree_node,
            edge_kwargs=edge_kwargs,
            custom_edge_kwargs={"width": "node_weight"},
        )
        if LOCAL:
            net.save_graph("tests/test_tree_to_vis_custom_edge_kwargs_override.html")

    @staticmethod
    def test_tree_to_vis_edge_kwargs(tree_node):
        edge_kwargs = dict(width=5)
        net = export.tree_to_vis(tree_node, edge_kwargs=edge_kwargs)
        if LOCAL:
            net.save_graph("tests/test_tree_to_vis_edge_kwargs.html")

    @staticmethod
    def test_tree_to_vis_network_kwargs(tree_node):
        network_kwargs = dict(
            height="750px", width="100%", bgcolor="#222222", font_color="white"
        )
        net = export.tree_to_vis(tree_node, network_kwargs=network_kwargs)
        if LOCAL:
            net.save_graph("tests/test_tree_to_vis_network_kwargs.html")

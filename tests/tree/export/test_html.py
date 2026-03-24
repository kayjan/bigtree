from unittest.mock import patch

from bigtree.tree import export

PATCH_UUID_PATH = "bigtree.tree.export.html.uuid.uuid4"


class TestTreeToHtml:
    folder_path = "tests/tree/export/data"

    @patch(PATCH_UUID_PATH)
    def test_tree_to_html(self, mock_uuid4, tree_node_style2):
        mock_uuid4.return_value.hex = "123456"
        html = export.tree_to_html(tree_node_style2)
        with open(f"{self.folder_path}/tree.html", "r") as file:
            expected_html = file.read()
        assert html == expected_html

    @patch(PATCH_UUID_PATH)
    def test_tree_to_html_all_attrs(self, mock_uuid4, tree_node_style2):
        mock_uuid4.return_value.hex = "123456"
        html = export.tree_to_html(tree_node_style2, all_attrs=True)
        with open(f"{self.folder_path}/tree_all_attrs.html", "r") as file:
            expected_html = file.read()
        assert html == expected_html

    @patch(PATCH_UUID_PATH)
    def test_tree_to_html_attr_list(self, mock_uuid4, tree_node_style2):
        mock_uuid4.return_value.hex = "123456"
        html = export.tree_to_html(tree_node_style2, attr_list=["age"])
        with open(f"{self.folder_path}/tree_attr_list.html", "r") as file:
            expected_html = file.read()
        assert html == expected_html

    @patch(PATCH_UUID_PATH)
    def test_tree_to_html_node_width_and_colour(self, mock_uuid4, tree_node_style2):
        mock_uuid4.return_value.hex = "123456"

        # Make the name longer
        tree_node_style2.name = "abcdefghijklmnopqrstuvwxyz"
        tree_node_style2["b"].name = "a very long name for test"

        html = export.tree_to_html(
            tree_node_style2,
            node_width=200,
            node_colour="#ADD8E6",
            all_attrs=True,
            height=700,
        )
        with open(f"{self.folder_path}/tree_node_width_and_colour.html", "r") as file:
            expected_html = file.read()
        assert html == expected_html

    @patch(PATCH_UUID_PATH)
    def test_tree_to_html_node_custom(self, mock_uuid4, tree_node_style2):
        mock_uuid4.return_value.hex = "123456"

        # Make the name longer
        tree_node_style2.name = "abcdefghijklmnopqrstuvwxyz"
        tree_node_style2["b"].name = "a very long name for test"

        html = export.tree_to_html(
            tree_node_style2,
            node_width=200,
            node_colour="fillcolor",
            all_attrs=True,
            height=700,
        )
        with open(f"{self.folder_path}/tree_node_custom.html", "r") as file:
            expected_html = file.read()
        assert html == expected_html

    @patch(PATCH_UUID_PATH)
    def test_tree_to_html_border(self, mock_uuid4, tree_node_style2):
        mock_uuid4.return_value.hex = "123456"

        html = export.tree_to_html(
            tree_node_style2,
            border_colour="#ADD8E6",
            border_radius=0,
            border_width=3,
            attr_list=["age", "cname"],
            height=700,
        )
        with open(f"{self.folder_path}/tree_border.html", "r") as file:
            expected_html = file.read()
        assert html == expected_html

    @patch(PATCH_UUID_PATH)
    def test_tree_to_html_border_custom(self, mock_uuid4, tree_node_style2):
        mock_uuid4.return_value.hex = "123456"

        html = export.tree_to_html(
            tree_node_style2,
            border_colour="border_colour",
            border_width="border_width",
            attr_list=["age", "cname"],
            height=700,
        )
        with open(f"{self.folder_path}/tree_border_custom.html", "r") as file:
            expected_html = file.read()
        assert html == expected_html

    @patch(PATCH_UUID_PATH)
    def test_tree_to_html_edge(self, mock_uuid4, tree_node_style2):
        mock_uuid4.return_value.hex = "123456"

        html = export.tree_to_html(
            tree_node_style2,
            edge_colour="#ADD8E6",
            edge_width=4,
            attr_list=["age", "cname"],
            height=700,
        )
        with open(f"{self.folder_path}/tree_edge.html", "r") as file:
            expected_html = file.read()
        assert html == expected_html

    @patch(PATCH_UUID_PATH)
    def test_tree_to_html_font(self, mock_uuid4, tree_node_style2):
        mock_uuid4.return_value.hex = "123456"

        # Make the name longer
        tree_node_style2.name = "abcdef"
        tree_node_style2["b"].name = "a very long name for test"

        html = export.tree_to_html(
            tree_node_style2,
            node_width=300,
            font_colour="#ADD8E6",
            font_title_size=20,
            font_size=15,
            attr_list=["age", "cname"],
            height=700,
        )
        with open(f"{self.folder_path}/tree_font.html", "r") as file:
            expected_html = file.read()
        assert html == expected_html

    @patch(PATCH_UUID_PATH)
    def test_tree_to_html_font_custom(self, mock_uuid4, tree_node_style2):
        mock_uuid4.return_value.hex = "123456"

        # Make the name longer
        tree_node_style2.name = "abcdef"
        tree_node_style2["b"].name = "a very long name for test"

        html = export.tree_to_html(
            tree_node_style2,
            font_colour="fillcolor",
            attr_list=["age", "cname"],
            height=700,
        )
        with open(f"{self.folder_path}/tree_font_custom.html", "r") as file:
            expected_html = file.read()
        assert html == expected_html

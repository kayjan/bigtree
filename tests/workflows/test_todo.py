import unittest

import pytest

from bigtree import AppToDo
from bigtree.utils.exceptions import SearchError
from tests.conftest import assert_console_output


class TestAppToDo(unittest.TestCase):
    def setUp(self):
        self.todoapp = AppToDo("To Do Items")

    def tearDown(self):
        self.todoapp = None

    @staticmethod
    def test_creation():
        todoapp = AppToDo("To Do Items")
        assert todoapp._root.name == "To Do Items"

    def test_add_list(self):
        self.todoapp.add_list("List 1")
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 2
        expected_n_children = 1
        expected_n_descendants = 1
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

    def test_add_list_duplicate(self):
        self.todoapp.add_list("List 1")
        self.todoapp.add_list("List 1")
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 2
        expected_n_children = 1
        expected_n_descendants = 1
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

    def test_prioritize_list(self):
        self.todoapp.add_list("List 1")
        self.todoapp.add_list("List 2")
        self.todoapp.prioritize_list("List 2")
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 2
        expected_n_children = 2
        expected_n_descendants = 2
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

        assert [node.node_name for node in self.todoapp._root.children] == [
            "List 2",
            "List 1",
        ], "Prioritizing did not work"

    def test_prioritize_list_error(self):
        self.todoapp.add_list("List 1")
        self.todoapp.add_list("List 2")
        with pytest.raises(ValueError) as exc_info:
            self.todoapp.prioritize_list("List 3")
        assert str(exc_info.value) == "List List 3 not found"

    def test_add_item_single(self):
        self.todoapp.add_item("Item 1")
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 3
        expected_n_children = 1
        expected_n_descendants = 2
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

    def test_add_item_single_list(self):
        self.todoapp.add_item("Item 1", "List 1")
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 3
        expected_n_children = 1
        expected_n_descendants = 2
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

    def test_add_item_multiple(self):
        self.todoapp.add_item(["Item 1", "Item 2"])
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 3
        expected_n_children = 1
        expected_n_descendants = 3
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

    def test_add_item_multiple_list(self):
        self.todoapp.add_item(["Item 1", "Item 2"], "List 1")
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 3
        expected_n_children = 1
        expected_n_descendants = 3
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

    def test_add_item_type_error(self):
        with pytest.raises(TypeError):
            self.todoapp.add_item(1)

    def test_remove_item_single(self):
        self.todoapp.add_item("Item 1")
        self.todoapp.remove_item("Item 1")
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 1
        expected_n_children = 0
        expected_n_descendants = 0
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

    def test_remove_item_single_list(self):
        self.todoapp.add_item("Item 1")
        self.todoapp.remove_item(["Item 1"], "General")
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 1
        expected_n_children = 0
        expected_n_descendants = 0
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

    def test_remove_duplicate_item(self):
        self.todoapp.add_item("Item 1")
        self.todoapp.add_item("Item 1", "List 1")
        self.todoapp.remove_item("Item 1", "List 1")
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 3
        expected_n_children = 1
        expected_n_descendants = 2
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

    def test_remove_duplicate_item_error(self):
        self.todoapp.add_item("Item 1")
        self.todoapp.add_item("Item 1", "List 1")
        with pytest.raises(SearchError):
            self.todoapp.remove_item("Item 1")

    def test_remove_item_multiple(self):
        self.todoapp.add_item(["Item 1", "Item 2"])
        self.todoapp.remove_item(["Item 1", "Item 2"])
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 1
        expected_n_children = 0
        expected_n_descendants = 0
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

    def test_remove_item_multiple_list(self):
        self.todoapp.add_item(["Item 1", "Item 2"])
        self.todoapp.remove_item(["Item 1", "Item 2"], "General")
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 1
        expected_n_children = 0
        expected_n_descendants = 0
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"

    def test_remove_item_error(self):
        with pytest.raises(TypeError):
            self.todoapp.remove_item(1)

    def test_prioritize_item(self):
        self.todoapp.add_item("Item 1", "List 1")
        self.todoapp.add_item("Item 2", "List 1")
        self.todoapp.prioritize_item("Item 2")
        max_depth = self.todoapp._root.max_depth
        n_children = len(list(self.todoapp._root.children))
        n_descendants = len(list(self.todoapp._root.descendants))
        expected_max_depth = 3
        expected_n_children = 1
        expected_n_descendants = 3
        assert (
            max_depth == expected_max_depth
        ), f"Expected depth to be {expected_max_depth}, received {max_depth}"
        assert (
            n_children == expected_n_children
        ), f"Expected number of children to be {expected_n_children}, received {n_children}"
        assert (
            n_descendants == expected_n_descendants
        ), f"Expected number of descendants to be {expected_n_descendants}, received {n_children}"
        assert [node.node_name for node in self.todoapp._root.children[0].children] == [
            "Item 2",
            "Item 1",
        ], "Prioritizing did not work"

    def test_prioritize_item_error(self):
        self.todoapp.add_item("Item 1", "List 1")
        self.todoapp.add_item("Item 2", "List 1")
        with pytest.raises(ValueError):
            self.todoapp.prioritize_item("Item 3")


@assert_console_output("Created list List 1")
def test_add_list_verbose():
    todoapp = AppToDo("To Do Items")
    todoapp.add_list("List 1")


@assert_console_output("Created list List 1")
def test_add_list_duplicate_verbose():
    todoapp = AppToDo("To Do Items")
    todoapp.add_list("List 1")
    todoapp.add_list("List 1")


@assert_console_output(["Created list General", "Created item Item 1"])
def test_add_item_single_verbose():
    todoapp = AppToDo("To Do Items")
    todoapp.add_item("Item 1")


@assert_console_output(["Created list List 1", "Created item Item 1"])
def test_add_item_single_list():
    todoapp = AppToDo("To Do Items")
    todoapp.add_item("Item 1", "List 1")


@assert_console_output(["Created list General", "Created items Item 1, Item 2"])
def test_add_item_multiple():
    todoapp = AppToDo("To Do Items")
    todoapp.add_item(["Item 1", "Item 2"])


@assert_console_output(["Created list List 1", "Created items Item 1, Item 2"])
def test_add_item_multiple_list_verbose():
    todoapp = AppToDo("To Do Items")
    todoapp.add_item(["Item 1", "Item 2"], "List 1")


@assert_console_output(
    [
        "Created list General",
        "Created item Item 1",
        "Removed items Item 1",
        "Removed list General",
    ]
)
def test_remove_item_single_verbose():
    todoapp = AppToDo("To Do Items")
    todoapp.add_item("Item 1")
    todoapp.remove_item("Item 1")


@assert_console_output(
    [
        "Created list General",
        "Created item Item 1",
        "Removed items Item 1",
        "Removed list General",
    ]
)
def test_remove_item_single_list_verbose():
    todoapp = AppToDo("To Do Items")
    todoapp.add_item("Item 1")
    todoapp.remove_item(["Item 1"], "General")


@assert_console_output(
    [
        "Created list General",
        "Created item Item 1",
        "Created list List 1",
        "Created item Item 1",
        "Removed items Item 1",
        "Removed list List 1",
    ]
)
def test_remove_duplicate_item():
    todoapp = AppToDo("To Do Items")
    todoapp.add_item("Item 1")
    todoapp.add_item("Item 1", "List 1")
    todoapp.remove_item("Item 1", "List 1")


@assert_console_output(
    [
        "Created list General",
        "Created items Item 1, Item 2",
        "Removed items Item 1, Item 2",
        "Removed list General",
    ]
)
def test_remove_item_multiple():
    todoapp = AppToDo("To Do Items")
    todoapp.add_item(["Item 1", "Item 2"])
    todoapp.remove_item(["Item 1", "Item 2"])


@assert_console_output(
    [
        "Created list General",
        "Created items Item 1, Item 2",
        "Removed items Item 1, Item 2",
        "Removed list General",
    ]
)
def test_remove_item_multiple_list():
    todoapp = AppToDo("To Do Items")
    todoapp.add_item(["Item 1", "Item 2"])
    todoapp.remove_item(["Item 1", "Item 2"], "General")

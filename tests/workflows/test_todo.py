import unittest

import pytest

from bigtree.utils import exceptions
from bigtree.workflows import app_todo
from tests.conftest import assert_console_output
from tests.test_constants import Constants


class TestAppToDo(unittest.TestCase):
    def setUp(self):
        self.todoapp = app_todo.AppToDo("To Do Items")

    def tearDown(self):
        self.todoapp = None

    @staticmethod
    def test_creation():
        todoapp = app_todo.AppToDo("To Do Items")
        assert todoapp._root.node_name == "To Do Items"

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

    def test_prioritize_list_error_item(self):
        self.todoapp.add_item("Item 1", "List 1")
        self.todoapp.add_item("Item 2", "List 1")
        with pytest.raises(ValueError) as exc_info:
            self.todoapp.prioritize_list("Item 2")
        assert str(exc_info.value) == "List Item 2 not found"

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
        with pytest.raises(TypeError) as exc_info:
            self.todoapp.add_item(1)
        assert str(exc_info.value) == Constants.ERROR_WORKFLOW_TODO_TYPE

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

    def test_remove_item_single_error(self):
        with pytest.raises(ValueError) as exc_info:
            self.todoapp.remove_item("Item 1")
        assert str(exc_info.value) == "Item Item 1 does not exist!"

    def test_remove_item_single_error_list(self):
        with pytest.raises(ValueError) as exc_info:
            self.todoapp.remove_item("Item 1", "General")
        assert str(exc_info.value) == "List General does not exist!"

    def test_remove_item_single_error_in_list(self):
        self.todoapp.add_item("Item 1")
        with pytest.raises(ValueError) as exc_info:
            self.todoapp.remove_item("Item 2", "General")
        assert str(exc_info.value) == "Item Item 2 does not exist!"

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

    def test_remove_item_single_list_error(self):
        with pytest.raises(ValueError) as exc_info:
            self.todoapp.remove_item(["Item 1"])
        assert str(exc_info.value) == "Item Item 1 does not exist!"

    def test_remove_item_single_list_error_in_list(self):
        self.todoapp.add_item("Item 1")
        with pytest.raises(ValueError) as exc_info:
            self.todoapp.remove_item(["Item 2"], "General")
        assert str(exc_info.value) == "Item Item 2 does not exist!"

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
        with pytest.raises(exceptions.SearchError) as exc_info:
            self.todoapp.remove_item("Item 1")
        assert str(exc_info.value).startswith(
            Constants.ERROR_SEARCH_LESS_THAN_N_ELEMENT.format(count=1)
        )

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
        with pytest.raises(TypeError) as exc_info:
            self.todoapp.remove_item(1)
        assert str(exc_info.value) == Constants.ERROR_WORKFLOW_TODO_TYPE

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

    def test_prioritize_item_error_list(self):
        self.todoapp.add_item("Item 1", "List 1")
        self.todoapp.add_item("Item 2", "List 2")
        with pytest.raises(ValueError) as exc_info:
            self.todoapp.prioritize_item("List 2")
        assert str(exc_info.value) == "List 2 is not an item"

    def test_prioritize_item_error(self):
        self.todoapp.add_item("Item 1", "List 1")
        self.todoapp.add_item("Item 2", "List 1")
        with pytest.raises(ValueError) as exc_info:
            self.todoapp.prioritize_item("Item 3")
        assert str(exc_info.value) == "Item Item 3 not found"


@assert_console_output("Created list List 1")
def test_add_list_verbose():
    todoapp = app_todo.AppToDo("To Do Items")
    todoapp.add_list("List 1")


@assert_console_output("Created list List 1")
def test_add_list_duplicate_verbose():
    todoapp = app_todo.AppToDo("To Do Items")
    todoapp.add_list("List 1")
    todoapp.add_list("List 1")


@assert_console_output(["Created list General", "Created item(s) Item 1"])
def test_add_item_single_verbose():
    todoapp = app_todo.AppToDo("To Do Items")
    todoapp.add_item("Item 1")


@assert_console_output(["Created list List 1", "Created item(s) Item 1"])
def test_add_item_single_list():
    todoapp = app_todo.AppToDo("To Do Items")
    todoapp.add_item("Item 1", "List 1")


@assert_console_output(["Created list General", "Created item(s) Item 1, Item 2"])
def test_add_item_multiple():
    todoapp = app_todo.AppToDo("To Do Items")
    todoapp.add_item(["Item 1", "Item 2"])


@assert_console_output(["Created list List 1", "Created item(s) Item 1, Item 2"])
def test_add_item_multiple_list_verbose():
    todoapp = app_todo.AppToDo("To Do Items")
    todoapp.add_item(["Item 1", "Item 2"], "List 1")


@assert_console_output(
    [
        "Created list General",
        "Created item(s) Item 1",
        "Removed item(s) Item 1",
        "Removed list General",
    ]
)
def test_remove_item_single_verbose():
    todoapp = app_todo.AppToDo("To Do Items")
    todoapp.add_item("Item 1")
    todoapp.remove_item("Item 1")


@assert_console_output(
    [
        "Created list General",
        "Created item(s) Item 1",
        "Removed item(s) Item 1",
        "Removed list General",
    ]
)
def test_remove_item_single_list_verbose():
    todoapp = app_todo.AppToDo("To Do Items")
    todoapp.add_item("Item 1")
    todoapp.remove_item(["Item 1"], "General")


@assert_console_output(
    [
        "Created list General",
        "Created item(s) Item 1",
        "Created list List 1",
        "Created item(s) Item 1",
        "Removed item(s) Item 1",
        "Removed list List 1",
    ]
)
def test_remove_duplicate_item():
    todoapp = app_todo.AppToDo("To Do Items")
    todoapp.add_item("Item 1")
    todoapp.add_item("Item 1", "List 1")
    todoapp.remove_item("Item 1", "List 1")


@assert_console_output(
    [
        "Created list General",
        "Created item(s) Item 1, Item 2",
        "Removed item(s) Item 1, Item 2",
        "Removed list General",
    ]
)
def test_remove_item_multiple():
    todoapp = app_todo.AppToDo("To Do Items")
    todoapp.add_item(["Item 1", "Item 2"])
    todoapp.remove_item(["Item 1", "Item 2"])


@assert_console_output(
    [
        "Created list General",
        "Created item(s) Item 1, Item 2",
        "Removed item(s) Item 1, Item 2",
        "Removed list General",
    ]
)
def test_remove_item_multiple_list():
    todoapp = app_todo.AppToDo("To Do Items")
    todoapp.add_item(["Item 1", "Item 2"])
    todoapp.remove_item(["Item 1", "Item 2"], "General")

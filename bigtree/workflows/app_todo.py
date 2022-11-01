import json
import logging
from typing import List, Union

from bigtree.node.node import Node
from bigtree.tree.construct import dict_to_tree
from bigtree.tree.export import print_tree, tree_to_dict
from bigtree.tree.search import find_children, find_name

logging.getLogger(__name__).addHandler(logging.NullHandler())


class AppToDo:
    """
    To-Do List Implementation with Big Tree.
      - To-Do List has three levels - app name, list name, and item name.
      - If list name is not given, item will be assigned to a `General` list.

    *Initializing and Adding Items*

    >>> from bigtree import AppToDo
    >>> app = AppToDo("To Do App")
    >>> app.add_item(item_name="Homework 1", list_name="School")
    >>> app.add_item(item_name=["Milk", "Bread"], list_name="Groceries", description="Urgent")
    >>> app.add_item(item_name="Cook")
    >>> app.show(style="const")
    To Do App
    ├── School
    │   └── Homework 1
    ├── Groceries
    │   ├── Milk [description=Urgent]
    │   └── Bread [description=Urgent]
    └── General
        └── Cook

    *Reorder List and Item*

    >>> app.prioritize_list(list_name="General")
    >>> app.show(style="const")
    To Do App
    ├── General
    │   └── Cook
    ├── School
    │   └── Homework 1
    └── Groceries
        ├── Milk [description=Urgent]
        └── Bread [description=Urgent]

    >>> app.prioritize_item(item_name="Bread")
    >>> app.show(style="const")
    To Do App
    ├── General
    │   └── Cook
    ├── School
    │   └── Homework 1
    └── Groceries
        ├── Bread [description=Urgent]
        └── Milk [description=Urgent]

    *Removing Items*

    >>> app.remove_item("Homework 1")
    >>> app.show(style="const")
    To Do App
    ├── General
    │   └── Cook
    └── Groceries
        ├── Bread [description=Urgent]
        └── Milk [description=Urgent]

    *Exporting and Importing List*

    >>> app.save("list.json")
    >>> app2 = AppToDo.load("list.json")
    >>> app2.show(style="const")
    To Do App
    ├── General
    │   └── Cook
    └── Groceries
        ├── Bread [description=Urgent]
        └── Milk [description=Urgent]
    """

    def __init__(
        self,
        app_name: str = "",
    ):
        """Initialize To-Do app

        Args:
            app_name (str): name of to-do app, optional
        """
        self._root = Node(app_name)

    def add_list(self, list_name: str, **kwargs) -> Node:
        """Add list to app

        If list is present, return list node, else a new list will be created

        Args:
            list_name (str): name of list

        Returns:
            (Node)
        """
        list_node = find_children(self._root, list_name)
        if not list_node:
            list_node = Node(list_name, parent=self._root, **kwargs)
            logging.info(f"Created list {list_name}")
        return list_node

    def prioritize_list(self, list_name: str):
        """Prioritize list in app, shift it to be the first list

        Args:
            list_name (str): name of list
        """
        list_node = find_children(self._root, list_name)
        if not list_node:
            raise ValueError(f"List {list_name} not found")
        current_children = list(self._root.children)
        current_children.remove(list_node)
        current_children.insert(0, list_node)
        self._root.children = current_children

    def add_item(self, item_name: Union[str, List[str]], list_name: str = "", **kwargs):
        """Add items to list

        Args:
            item_name (str/List[str]): items to be added
            list_name (str): list to add items to, optional
        """
        if not isinstance(item_name, str) and not isinstance(item_name, list):
            raise TypeError("Invalid data type for item")

        # Get list to add to
        if list_name:
            list_node = self.add_list(list_name)
        else:
            list_node = self.add_list("General")

        # Add items to list
        if isinstance(item_name, str):
            _ = Node(item_name, parent=list_node, **kwargs)
            logging.info(f"Created item {item_name}")
        elif isinstance(item_name, list):
            for _item in item_name:
                _ = Node(_item, parent=list_node, **kwargs)
            logging.info(f"Created items {', '.join(item_name)}")

    def remove_item(self, item_name: Union[str, List[str]], list_name: str = ""):
        """Remove items from list

        Args:
            item_name (str/List[str]): items to be added
            list_name (str): list to add items to, optional
        """
        if not isinstance(item_name, str) and not isinstance(item_name, list):
            raise TypeError("Invalid data type for item")

        # Check if items can be found
        items_to_remove = []
        parent_to_check = set()
        if list_name:
            list_node = find_children(self._root, list_name)
            if isinstance(item_name, str):
                item_node = find_children(list_node, item_name)
                items_to_remove.append(item_node)
                parent_to_check.add(item_node.parent)
            elif isinstance(item_name, list):
                for _item in item_name:
                    item_node = find_children(list_node, _item)
                    items_to_remove.append(item_node)
                    parent_to_check.add(item_node.parent)
        else:
            if isinstance(item_name, str):
                item_node = find_name(self._root, item_name)
                items_to_remove.append(item_node)
                parent_to_check.add(item_node.parent)
            elif isinstance(item_name, list):
                for _item in item_name:
                    item_node = find_name(self._root, _item)
                    items_to_remove.append(item_node)
                    parent_to_check.add(item_node.parent)

        # Remove items
        for item_node in items_to_remove:
            item_node.parent = None
        logging.info(
            f"Removed items {', '.join(item.node_name for item in items_to_remove)}"
        )

        # Remove list if empty
        for list_node in parent_to_check:
            if not len(list(list_node.children)):
                list_node.parent = None
                logging.info(f"Removed list {list_node.node_name}")

    def prioritize_item(self, item_name: str):
        """Prioritize item in list, shift it to be the first item in list

        Args:
            item_name (str): name of item
        """
        item_node = find_name(self._root, item_name)
        if not item_node:
            raise ValueError(f"Item {item_node} not found")
        current_parent = item_node.parent
        current_children = list(current_parent.children)
        current_children.remove(item_node)
        current_children.insert(0, item_node)
        current_parent.children = current_children

    def show(self, **kwargs):
        """Print tree to console"""
        print_tree(self._root, all_attrs=True, **kwargs)

    @staticmethod
    def load(json_path: str):
        """Load To-Do app from json

        Args:
            json_path (str): json load path

        Returns:
            (Self)
        """
        if not json_path.endswith(".json"):
            raise ValueError("Path should end with .json")

        with open(json_path, "r") as fp:
            app_dict = json.load(fp)
        _app = AppToDo("dummy")
        AppToDo.__setattr__(_app, "_root", dict_to_tree(app_dict["root"]))
        return _app

    def save(self, json_path: str):
        """Save To-Do app as json

        Args:
            json_path (str): json save path
        """
        if not json_path.endswith(".json"):
            raise ValueError("Path should end with .json")

        node_dict = tree_to_dict(self._root, all_attrs=True)
        app_dict = {"root": node_dict}
        with open(json_path, "w") as fp:
            json.dump(app_dict, fp)

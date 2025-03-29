from __future__ import annotations

import datetime as dt
from typing import Any, Optional, Union

from bigtree.node import node
from bigtree.tree import construct, export, search

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    from unittest.mock import MagicMock

    pydot = MagicMock()


class Calendar:
    """
    Calendar Implementation with Big Tree.
      - Calendar has four levels - year, month, day, and event name (with event attributes)

    Examples:
        # *Initializing and Adding Events*

        >>> from bigtree import Calendar
        >>> calendar = Calendar("My Calendar")
        >>> calendar.add_event("Gym", "2023-01-01 18:00")
        >>> calendar.add_event("Dinner", "2023-01-01", date_format="%Y-%m-%d", budget=20)
        >>> calendar.add_event("Gym", "2023-01-02 18:00")
        >>> calendar.show()
        My Calendar
        2023-01-01 00:00:00 - Dinner (budget: 20)
        2023-01-01 18:00:00 - Gym
        2023-01-02 18:00:00 - Gym

        # *Search for Events*

        >>> calendar.find_event("Gym")
        2023-01-01 18:00:00 - Gym
        2023-01-02 18:00:00 - Gym

        # *Removing Events*

        >>> import datetime as dt
        >>> calendar.delete_event("Gym", dt.date(2023, 1, 1))
        >>> calendar.show()
        My Calendar
        2023-01-01 00:00:00 - Dinner (budget: 20)
        2023-01-02 18:00:00 - Gym

        # *Export Calendar*

        >>> calendar.to_dataframe()
                                     path    name        date      time  budget
        0  /My Calendar/2023/01/01/Dinner  Dinner  2023-01-01  00:00:00    20.0
        1     /My Calendar/2023/01/02/Gym     Gym  2023-01-02  18:00:00     NaN
    """

    def __init__(self, name: str):
        self.calendar = node.Node(name)
        self.__sorted = True

    def add_event(
        self,
        event_name: str,
        event_datetime: Union[str, dt.datetime],
        date_format: str = "%Y-%m-%d %H:%M",
        **kwargs: Any,
    ) -> None:
        """Add event to calendar.

        Args:
            event_name: event name to be added
            event_datetime: event date and time
            date_format: specify datetime format if event_datetime is str
        """
        if isinstance(event_datetime, str):
            event_datetime = dt.datetime.strptime(event_datetime, date_format)
        year, month, day, date, time = (
            event_datetime.year,
            str(event_datetime.month).zfill(2),
            str(event_datetime.day).zfill(2),
            event_datetime.date(),
            event_datetime.time(),
        )
        event_path = f"{self.calendar.node_name}/{year}/{month}/{day}/{event_name}"
        event_attr = {"date": date, "time": time, **kwargs}
        if search.find_full_path(self.calendar, event_path):
            print(
                f"Event {event_name} exists on {date}, overwriting information for {event_name}"
            )
        construct.add_path_to_tree(
            tree=self.calendar,
            path=event_path,
            node_attrs=event_attr,
        )
        self.__sorted = False

    def delete_event(
        self, event_name: str, event_date: Optional[dt.date] = None
    ) -> None:
        """Delete event from calendar.

        Args:
            event_name: event name to be deleted
            event_date: event date to be deleted
        """
        if event_date:
            year, month, day = (
                event_date.year,
                str(event_date.month).zfill(2),
                str(event_date.day).zfill(2),
            )
            event_path = f"{self.calendar.node_name}/{year}/{month}/{day}/{event_name}"
            event = search.find_full_path(self.calendar, event_path)
            if event:
                self._delete_event(event)
            else:
                print(f"Event {event_name} does not exist on {event_date}")
        else:
            for event in search.findall(
                self.calendar, lambda node: node.node_name == event_name
            ):
                self._delete_event(event)

    def find_event(self, event_name: str) -> None:
        """Find event by name, prints result to console.

        Args:
            event_name: event name
        """
        if not self.__sorted:
            self._sort()
        for event in search.findall(
            self.calendar, lambda node: node.node_name == event_name
        ):
            self._show(event)

    def show(self) -> None:
        """Show calendar, prints result to console."""
        if not len(self.calendar.children):
            raise Exception("Calendar is empty!")
        if not self.__sorted:
            self._sort()
        print(self.calendar.node_name)
        for event in self.calendar.leaves:
            self._show(event)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Export calendar to DataFrame.

        Returns:
            pandas DataFrame of calendar
        """
        if not len(self.calendar.children):
            raise Exception("Calendar is empty!")
        data = export.tree_to_dataframe(self.calendar, all_attrs=True, leaf_only=True)
        compulsory_cols = ["path", "name", "date", "time"]
        other_cols = list(set(data.columns) - set(compulsory_cols))
        return data[compulsory_cols + other_cols]

    def _delete_event(self, event: node.Node) -> None:
        """Private method to delete event, delete parent node as well.

        Args:
            event: event to be deleted
        """
        if len(event.parent.children) == 1:
            if event.parent.parent:
                self._delete_event(event.parent)
            event.parent.parent = None
        else:
            event.parent = None

    def _sort(self) -> None:
        """Private method to sort calendar by event date, followed by event time"""
        for day_event in search.findall(self.calendar, lambda node: node.depth <= 4):
            if day_event.depth < 4:
                day_event.sort(key=lambda attr: attr.node_name)
            else:
                day_event.sort(key=lambda attr: attr.time)
        self.__sorted = True

    @staticmethod
    def _show(event: node.Node) -> None:
        """Private method to show event, handles the formatting of event.
        Prints result to console.

        Args:
            event: event
        """
        event_datetime = dt.datetime.combine(
            event.get_attr("date"), event.get_attr("time")
        )
        event_attrs = event.describe(
            exclude_attributes=["date", "time", "name"], exclude_prefix="_"
        )
        event_attrs_str = ", ".join([f"{attr[0]}: {attr[1]}" for attr in event_attrs])
        if event_attrs_str:
            event_attrs_str = f" ({event_attrs_str})"
        print(f"{event_datetime} - {event.node_name}{event_attrs_str}")

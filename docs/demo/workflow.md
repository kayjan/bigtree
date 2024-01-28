---
title: Workflow Demonstration
---

# 📋 Workflow Demonstration

There are existing implementations of workflows to showcase how `bigtree` can be used!

## To Do Application
There are functions to:

- Add or remove list to To-Do application
- Add or remove item to list, default list is the 'General' list
- Prioritize a list/item by reordering them as first list/item
- Save and import To-Do application to and from an external JSON file
- Show To-Do application, which prints tree to console

```python
from bigtree import AppToDo

app = AppToDo("To Do App")
app.add_item(item_name="Homework 1", list_name="School")
app.add_item(item_name=["Milk", "Bread"], list_name="Groceries", description="Urgent")
app.add_item(item_name="Cook")
app.show()
# To Do App
# ├── School
# │   └── Homework 1
# ├── Groceries
# │   ├── Milk [description=Urgent]
# │   └── Bread [description=Urgent]
# └── General
#     └── Cook

app.save("list.json")
app2 = AppToDo.load("list.json")
```

## Calendar Application

There are functions to:

- Add or remove event from Calendar
- Find event by name, or name and date
- Display calendar, which prints events to console
- Export calendar to pandas DataFrame

```python
import datetime as dt
from bigtree import Calendar

calendar = Calendar("My Calendar")
calendar.add_event("Gym", "2023-01-01 18:00")
calendar.add_event("Dinner", "2023-01-01", date_format="%Y-%m-%d", budget=20)
calendar.add_event("Gym", "2023-01-02 18:00")
calendar.show()
# My Calendar
# 2023-01-01 00:00:00 - Dinner (budget: 20)
# 2023-01-01 18:00:00 - Gym
# 2023-01-02 18:00:00 - Gym

calendar.find_event("Gym")
# 2023-01-01 18:00:00 - Gym
# 2023-01-02 18:00:00 - Gym

calendar.delete_event("Gym", dt.date(2023, 1, 1))
calendar.show()
# My Calendar
# 2023-01-01 00:00:00 - Dinner (budget: 20)
# 2023-01-02 18:00:00 - Gym

data_calendar = calendar.to_dataframe()
data_calendar
#                              path    name        date      time  budget
# 0  /My Calendar/2023/01/01/Dinner  Dinner  2023-01-01  00:00:00    20.0
# 1     /My Calendar/2023/01/02/Gym     Gym  2023-01-02  18:00:00     NaN
```

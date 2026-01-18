# Working with Classes

Custom classes can be assigned to Node as `data` attribute, or any other attribute name.

```python
from bigtree import Node


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.icon = ":open_file_folder:"

    def __str__(self):
         return f"Folder<{self.name}>"


class File:
    def __init__(self, name: str):
        self.name = name
        self.icon = ":memo:"

    def __str__(self):
         return f"File<{self.name}>"

folder_documents = Node("My Documents", data=Folder("Documents"))
file_photo1 = Node("photo1.jpg", data=File("photo.jpg"))
file_photo2 = Node("photo2.jpg", data=File("photo.jpg"))
folder_documents.children = [file_photo1, file_photo2]

folder_documents.show(rich=True, icon_prefix_attr="data.icon")
# 📂 My Documents
# ├── 📝 photo1.jpg
# └── 📝 photo2.jpg

folder_documents.show(alias="data", rich=True, icon_prefix_attr="data.icon")
# 📂 Folder<Documents>
# ├── 📝 File<photo.jpg>
# └── 📝 File<photo.jpg>
```

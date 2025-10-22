import os


class ASSERTIONS:
    FLAG: bool = bool(os.environ.get("BIGTREE_CONF_ASSERTIONS", True))

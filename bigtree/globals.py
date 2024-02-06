import os

ASSERTIONS: bool = bool(os.environ.get("BIGTREE_CONF_ASSERTIONS", True))

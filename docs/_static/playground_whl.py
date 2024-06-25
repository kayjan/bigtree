import os

import requests

# Output files
OUTPUT_JS = "docs/_static/"

DEFAULT_COMMANDS = [""]

PLAYGROUND_WHEELS = [
    "https://files.pythonhosted.org/packages/97/9c/372fef8377a6e340b1704768d20daaded98bf13282b5327beb2e2fe2c7ef/pygments-2.17.2-py3-none-any.whl",
]

CONFIG = """\
var colorNotebook = {{
    "playgroundWheels": {},
    "notebookWheels": [],
    "defaultPlayground": "{}"
}}
"""


if __name__ == "__main__":

    if os.path.exists(OUTPUT_JS + "playground-config.js"):
        os.remove(OUTPUT_JS + "playground-config.js")

    # Scrape whl file
    response = requests.get("https://pypi.org/pypi/bigtree/json")
    PACKAGE_WHEEL = [
        url["url"] for url in response.json()["urls"] if url["url"].endswith("whl")
    ]
    assert len(PACKAGE_WHEEL), "Cannot find package wheel"

    # Create the config that specifies which wheels need to be used
    config = (
        CONFIG.format(
            str(PLAYGROUND_WHEELS + PACKAGE_WHEEL), "\n".join(DEFAULT_COMMANDS)
        )
        .replace("\r", "")
        .encode("utf-8")
    )
    with open(OUTPUT_JS + "playground-config.js", "wb") as f:
        f.write(config)

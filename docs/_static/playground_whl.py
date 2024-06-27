import os

import requests

# Parameters
OUTPUT_JS = "docs/_static/"
PLAYGROUND_WHEELS = [
    "https://files.pythonhosted.org/packages/97/9c/372fef8377a6e340b1704768d20daaded98bf13282b5327beb2e2fe2c7ef/pygments-2.17.2-py3-none-any.whl",
]
PACKAGES = ["bigtree"]

DEFAULT_COMMANDS = [""]
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
    PACKAGE_WHEELS = []
    for package in PACKAGES:
        response = requests.get(f"https://pypi.org/pypi/{package}/json")
        package_wheel = [
            url["url"] for url in response.json()["urls"] if url["url"].endswith("whl")
        ]
        if len(package_wheel) > 1:
            package_wheel = sorted([url for url in package_wheel if "macos" in url])[
                -1:
            ]
        PACKAGE_WHEELS.extend(package_wheel)
    print("Fetched whls:", PACKAGE_WHEELS)

    # Create the config that specifies which wheels need to be used
    config = (
        CONFIG.format(
            str(PLAYGROUND_WHEELS + PACKAGE_WHEELS), "\n".join(DEFAULT_COMMANDS)
        )
        .replace("\r", "")
        .encode("utf-8")
    )
    with open(OUTPUT_JS + "playground-config.js", "wb") as f:
        f.write(config)

import glob
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

# Output files
OUTPUT_WHL = "docs/wheels/"
OUTPUT_JS = "docs/_static/"

# Build message output
# BUILD_WHL_MESSAGE = f"{OUTPUT_WHL}(.*whl)"
# BUILD_WHL_COMMAND = [sys.executable, "-m", "hatch", "build", OUTPUT_WHL]
BUILD_WHL_MESSAGE = r"Successfully built ([-_0-9.a-zA-Z]+?\.whl)"
BUILD_WHL_COMMAND = [sys.executable, "-m", "build", "--wheel", "-o", OUTPUT_WHL]

DEFAULT_COMMANDS = [""]

PLAYGROUND_WHEELS = [
    "https://files.pythonhosted.org/packages/97/9c/372fef8377a6e340b1704768d20daaded98bf13282b5327beb2e2fe2c7ef/pygments-2.17.2-py3-none-any.whl",
    "https://files.pythonhosted.org/packages/d3/58/7d2dd906add6bd3481ee80beafb00af292866ed4ce3fa18cd168cb7bab74/bigtree-0.19.0-py3-none-any.whl",
]

CONFIG = """\
var colorNotebook = {{
    "playgroundWheels": {},
    "notebookWheels": [],
    "defaultPlayground": "{}"
}}
"""


def build_package():
    """Build wheel"""

    if sys.platform.startswith("win"):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            BUILD_WHL_COMMAND,
            stdout=subprocess.PIPE,
            startupinfo=startupinfo,
            shell=False,
            env=os.environ.copy(),
        )
    else:
        process = subprocess.Popen(
            BUILD_WHL_COMMAND,
            stdout=subprocess.PIPE,
            shell=False,
            env=os.environ.copy(),
        )
    out, _ = process.communicate()
    build_message = out.decode("utf-8")
    m = re.compile(BUILD_WHL_MESSAGE).search(build_message)
    print(build_message)

    return process.returncode, m.group(1) if m else ""


def download_wheel(url, dest):
    """Download wheel"""

    print("Downloading: {}".format(url))
    try:
        response = urllib.request.urlopen(url)
        status = response.status
        if status == 200:
            status = 0
            with open(dest, "wb") as f:
                print("Writing: {}".format(dest))
                f.write(response.read())
    except urllib.error.HTTPError as e:
        status = e.status

    if status:
        print("Failed to download, received status code {}".format(status))

    return status


if __name__ == "__main__":

    PLAYGROUND = {}
    for url in PLAYGROUND_WHEELS:
        PLAYGROUND[os.path.join(OUTPUT_WHL, url.split("/")[-1])] = url

    # Clean up all old wheels and js file
    for file in glob.glob(OUTPUT_WHL + "*.whl"):
        if file not in PLAYGROUND.keys():
            os.remove(file)

    if os.path.exists(OUTPUT_JS + "playground-config.js"):
        os.remove(OUTPUT_JS + "playground-config.js")

    # Clean up build directory
    if os.path.exists("build"):
        shutil.rmtree("build")

    if not os.path.exists("docs/wheels"):
        os.mkdir("docs/wheels")

    # Build wheel
    status = 0
    # status, package = build_package()
    # if not status:
    #     for file, url in PLAYGROUND.items():
    #         if os.path.exists(file):
    #             print("Skipping: {}".format(file))
    #             continue
    #         status = download_wheel(url, file)
    #         if status:
    #             break

    if not status:
        # Build up a list of wheels needed for playgrounds and notebooks
        # playground = [
        #     os.path.basename(file_path) for file_path in PLAYGROUND.keys()
        # ] + [package]

        # Create the config that specifies which wheels need to be used
        config = (
            CONFIG.format(str(PLAYGROUND_WHEELS), "\n".join(DEFAULT_COMMANDS))
            .replace("\r", "")
            .encode("utf-8")
        )
        with open(OUTPUT_JS + "playground-config.js", "wb") as f:
            f.write(config)

    print("FAILED :(" if status else "SUCCESS :)")
    sys.exit(status)

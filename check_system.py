# encoding: utf-8
"""System checker.

This script performs a series of checks on the system to see if everything is
ready to run the analysis pipeline.
"""

import importlib
import os
import platform
import re
from pathlib import Path

import mne

from config import fname

if platform.system() in ("Darwin", "Linux"):
    unicode = True
else:  # Windows
    unicode = False

# Check to see if the python dependencies are fullfilled.
dependencies = Path("requirements.txt").read_text().split()

print("Checking dependencies:")
missing = list()
for dep_string in dependencies:
    # Convert the dependency string in the TOML file to a plain python package name.
    package_name = re.split(r"[<>=!~\[]", dep_string)[0].replace("-", "_").strip()

    try:
        mod = importlib.import_module(package_name)
        if unicode:
            print(f"├☑ {package_name:<21}", end="")
        else:
            print(f" + {package_name:<21}", end="")
        if hasattr(mod, "__version__"):
            print(mod.__version__)
        else:
            print()
    except ImportError:
        if unicode:
            print(f"├☐ {package_name:<21}", end="")
        else:
            print(f" - {package_name:<21}", end="")
        missing.append(package_name)
print()

# Raise an error if dependencies are not met
if len(missing) > 0:
    raise ImportError(f"Missing dependencies: {' '.join(missing)}")

# Check that the data is present on the system
if not os.path.exists(fname.orig_path):
    raise ValueError(
        "The `orig_data_path` points to a directory that does not contain any data "
        f"({fname.orig_path}). Run `make_example_data.py` first."
    )

# Prints some information about the system
mne.sys_info()

with open(fname.system_check, "w") as f:
    f.write("System check OK.")

print(
    "\nAll seems to be in order.\n"
    "You can now run the entire pipeline with: python -m doit"
)

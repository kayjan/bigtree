---
title: Installation
---

# 💻 Installation

`bigtree` requires Python 3.8+. There are two ways to install `bigtree`, with pip (recommended) or conda.

## Installation with pip

### Basic Installation

To install `bigtree`, run the following line in command prompt:

<!-- termynal -->
```console
$ pip install bigtree
---> 100%
Installed
```

### Installing optional dependencies

`bigtree` have a number of optional dependencies, which can be installed using "extras" syntax.

<!-- termynal -->
```console
$ pip install 'bigtree[extra_1, extra_2]'
```

Examples of extra packages include:

- `all`: include all optional dependencies
- `image`: for exporting tree to image
- `matplotlib`: for plotting trees
- `pandas`: for pandas methods
- `polars`: for polars methods

For `image` extra dependency, you may need to install more plugins.

<!-- termynal -->
```console
$ brew install gprof2dot  # for MacOS
$ conda install graphviz  # for Windows
```


## Installation with conda

To install `bigtree` with conda, run the following line in command prompt:

<!-- termynal -->
```console
$ conda install -c conda-forge bigtree
```

---
title: Installation
---

# 💻 Installation

There are two ways to install `bigtree`, with pip (recommended) or conda.

## Installation with pip

To install `bigtree`, run the following line in command prompt:

<!-- termynal -->
```console
$ pip install bigtree
---> 100%
Installed
```

If tree needs to use pandas or polars methods, it requires additional dependencies.
Run the following lines in command prompt:

<!-- termynal -->
```console
$ pip install 'bigtree[pandas]'
$ pip install 'bigtree[polars]'
```

If tree needs to be exported to image, it requires additional dependencies.
Run the following lines in command prompt:

<!-- termynal -->
```console
$ pip install 'bigtree[image]'
$ brew install gprof2dot  # for MacOS
$ conda install graphviz  # for Windows
```

Alternatively, install all optional dependencies with the following line in command prompt:

<!-- termynal -->
```console
$ pip install 'bigtree[all]'
```

## Installation with conda

To install `bigtree` with conda, run the following line in command prompt:

<!-- termynal -->
```console
$ conda install -c conda-forge bigtree
```

---
title: Contributing
---

# 🍪 Contributing
bigtree is a tree implementation package for Python. It integrates with Python lists, dictionaries, pandas and
polars DataFrame.

Thank you for taking the time to contribute. Contributing to this package is an excellent opportunity to dive into
tree implementations.

## Set Up

First, [fork the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo) and
clone the forked repository.

```console
$ git clone git@github.com:<your-username>/bigtree.git
```

Next, create a virtual environment and activate it.

=== "conda"
    ```console
    $ conda create -n bigtree_venv python=3.10
    $ conda activate bigtree_venv
    ```

=== "venv"
    ```console
    $ python -m venv .venv
    $ source .venv/bin/activate
    ```

To check if it worked,

=== "conda"
    ```console
    $ which pip
    /<some directory>/envs/bigtree_venv/bin/pip
    ```

=== "venv"
    ```console
    $ which pip
    /<current directory>/.venv/bin/pip
    ```

From the project folder, install the required python packages locally in editable mode and set up pre-commit checks.

    $ python -m pip install -e ".[all]"
    $ python -m pip install pre-commit
    $ pre-commit install

## Developing

After making your changes, create a new branch, add and commit your changed files.
In this example, let's assume the changed file is `README.md`.
If there are any pre-commit changes or comments, do modify, re-add and re-commit your files.

```console
$ git checkout -b chore/update-readme
$ git add README.md
$ git commit -m "chore: updated README"
```

Push your changes to your created branch and [create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) from your fork.

```console
$ git push origin chore/update-readme
```

## Testing

If there are changes related to code, make sure to add or update the tests accordingly.
Run the following lines of code and ensure the <mark>unit tests pass</mark> and the
<mark>code coverage is 100%</mark>.

```console
$ python -m pip install pytest pytest-benchmark pytest-cov coverage
$ pytest --cov-report=term-missing --cov-config=pyproject.toml --cov=bigtree
```

## Documentation

If there are changes related to code, make sure to add or update the documentations and docstrings accordingly.

For documentation, `bigtree` uses [mkdocs](https://www.mkdocs.org) for documentation and previews can be viewed
by running the following lines of code.

```console
$ python -m pip install hatch
$ hatch run mkdocs:build
$ hatch run mkdocs:serve
```

For docstrings, ensure that the description is most updated and existing, added, or modified sample code examples
in docstring still work. Run the following lines of code to generate the <mark>coverage report and test report for
docstrings</mark>. Refer to the console log for information on the file location of the reports.

```console
$ python -m pip install hatch
$ hatch run docs:coverage
$ hatch run docs:doctest
```

## Consequent Changes

Please [open an issue](https://github.com/kayjan/bigtree/issues/new/choose) to discuss important changes before
embarking on an implementation.

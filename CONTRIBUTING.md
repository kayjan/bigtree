bigtree is a tree implementation package for Python. It integrates with Python lists, dictionaries, and pandas DataFrame.


Thank you for taking the time to contribute. Contributing to this package is an excellent opportunity to dive into tree implementations.


Please read these before contributing

- [How to fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

## Steps

- First, fork the repository. Click on the fork button.

- Clone your fork locally.


```
git clone git@github.com:<your-username>/bigtree.git
```

- Create a virtual environment and activate it

- Install the package locally in editable mode

```
python -m pip install -e .
```

- Install pre-commit

```
python -m pip install pre-commit
```

- Activate pre-commit

```
pre-commit install
```

- Create a new branch, for example

```
git checkout -b chore/update-readme
```

- Add your changed files, here is an example for the README

```
git add README.md
```

- Commit your changes

```
git commit -m "chore: updated README"
```

If there were pre-commit changes, re-add your files then re-commit.

- Push your changes

```
git push origin chore/update-readme
```

- Then, [create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) from your fork

## Code-related changes

If your change is related to the code, please make sure the tests pass:

```
pytest tests/
```

Make sure your add/update the tests and documentations accordingly.

## Conventions and standards


This project formats code using black and isort.

It is also recommended to follow [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) when writing commit messages.

When creating branches, it is recommended to create them in the format

```
type/action
```

Example

```
git checkout -b feat/add-this
```

The project uses the pytest package for testing.

## For consequent changes

Please [open an issue](https://github.com/kayjan/bigtree/issues/new/choose) to discuss important changes before embarking on an implementation.

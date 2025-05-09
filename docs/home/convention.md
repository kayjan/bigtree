---
title: Convention and Standards
---

# 💬 Convention and Standards


## Git Workflow

When creating branches, it is recommended to create them in the format `type/action`. For example,

```console
$ git checkout -b feat/add-this
```

This project enforces [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
when writing commit messages.

- The regex for conventional commits is as such `(?s)(build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)(\(\S+\))?!?:( [^\n\r]+)((\n\n.*)|(\s*))?$`.

## Code Style and Format

As much as possible, this project follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
During pre-commit checks, this project checks and formats code using `black`, `flake8`, `isort`, and `mypy`.

Some general rules to follow:

- For **type hints**
  - Keep input types generic and output types specific. From more general to less general:
    - Iterable > Collection > Sequence > List/Set/Tuple
    - Mapping > MutableMapping > Dictionary
  - Use immutable defaults
  - Use `Optional` type if the input is nullable
- For **docstrings**
  - Do not mention the type as it is implied from the type hint

## Testing

For testing, this project uses `pytest` and `coverage` package for testing of codes,
and `doctest` and `docstr-coverage` package for testing of docstrings.

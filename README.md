# Unicode-CJK

## Installing

This package requires [PyICU], which requires some libraries installed.
Please see the [Installing PyICU](https://gitlab.pyicu.org/main/pyicu#installing-pyicu).

[PyICU]: https://pyicu.org

```shell-session
pipenv install
```

## Build the Data File

```shell-session
./scripts/build.sh

```

## Committing Changes

If you are planning to commit changes,
please install the dev packages as well:
```shell-session
pipenv install -d
```
and run the pre-commit checks:
```shell-session
./scripts/precommit.sh
```

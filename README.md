# Unicode-CJK

## Installing

This package requires [PyICU], which requires some libraries.
Please see the [Installing PyICU](https://gitlab.pyicu.org/main/pyicu#installing-pyicu).

[PyICU]: https://pyicu.org

```shell-session
pipenv install
```

## Build the Data File

Before running scripts, please make sure you are in the virtualenv.
```shell-session
pipenv shell
```
Then this script builds the data file.
```shell-session
./scripts/build.sh
```

## Code Changes

If you are planning to commit code changes,
please install the dev packages as well:
```shell-session
pipenv install -d
```
and run the pre-commit checks:
```shell-session
./scripts/precommit.sh
```

# Unicode auto-spacing

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

## Links

* [Unicode Auto Spacing (Proposal) L2/24-057](https://www.unicode.org/L2/L2024/24057-auto-spacing-prop.pdf)
* Old: [Proposal to add a property for auto inter-script spacing L2/23-283](https://www.unicode.org/L2/L2023/23283-auto-spacing-prop.pdf)
* [The current data file](https://github.com/kojiishi/unicode-auto-spacing/blob/main/auto-spacing.txt)
  * [In a spreadsheet format](https://docs.google.com/spreadsheets/d/1Y8gIy5ExavkUD3SWz8cgXvns8xfawfZh6-kaLT7Dju8/edit?usp=sharing)

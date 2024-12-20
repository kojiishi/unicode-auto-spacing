# Unicode auto-spacing

The proposal is
[available here](https://kojiishi.github.io/unicode-auto-spacing/).
The source is in [docs/index.html](docs/index.html).

## Installing

After cloning the repository:
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

> [!NOTE]
> The `build.sh` caches the Unicode data files locally,
> and uses the cached data files if available.
> To force downloading the data files,
> such as when the Unicode data is updated,
> please add the "`-f`" option.
> ```shell-session
> ./scripts/build.sh -f
> ```

You can then view the diff by regular `git` commands:
```shell-session
git diff
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

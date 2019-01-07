# reporeleaser [![Build Status](https://travis-ci.com/ludeeus/reporeleaser.svg?branch=master)](https://travis-ci.com/ludeeus/reporeleaser)

_Create a new release for your repo._  

This will create a new release for your repo.  
In the description of that release it will list all commits since the last release.

## Install

**Require Python version 3.5.3+**

```bash
python3 -m pip install -U reporeleaser
```

### Example

```bash
reporeleaser --token aaabbbccc111222333 --repo ludeeus/customjson --release patch
```

This example will create a new release for `` with this information:

#### Tag name

Current version + 1 for patch, example `1.1.4`

#### Release name

Current version + 1 for patch, example `1.1.4`

#### Release description

```markdown
## Changes

- Add cmd option --version
- lint
- Reorder stuff for version handling
- Fix customjson_update_pending
- Adds customjson_update_pending

[Full Changelog][changelog]

***

This release was created with [reporeleaser][reporeleaser] :tada:

[reporeleaser]: https://pypi.org/project/reporeleaser/
[changelog]: https://github.com/ludeeus/customjson/compare/1.1.3...1.1.4
```

**NB!: it is recommended to run it one time with `--test` to make sure the data is correct.**

#### CLI options

param | alias | description
-- | -- | --
`--token` | `-T` | An GitHub `access_token` with `repo` permissions.
`--repo` | `-R` | The repo you want to show info for, can be added multiple times, is optional.
`--release` | `None` | Can be `major`, `minor`, `patch`, `initial` or a custom tag name.
`--test` | `None` | This will print to console, and not create the release.
`--version` | `-V` | Print the installed version.


You can **only** use `major`, `minor`, `patch` if your tags are one of these:

- MAJOR.MINOR.PATCH
- vMAJOR.MINOR.PATCH

examples:

- 1.1.3
- v1.1.3

***

[![BuyMeCoffee](https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667)](https://www.buymeacoffee.com/ludeeus)
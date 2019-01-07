# reporeleaser [![Build Status](https://travis-ci.com/ludeeus/reporeleaser.svg?branch=master)](https://travis-ci.com/ludeeus/reporeleaser)

_Create a new release for your repo._  

## Install

**Require Python version 3.5.3+**

```bash
python3 -m pip install -U reporeleaser
```

### Example

```bash
reporeleaser --token aaabbbccc111222333 --mode component
```

```bash
reporeleaser --token aaabbbccc111222333 --mode component --repo sensor.trakt
```

```bash
reporeleaser --token aaabbbccc111222333 --mode component --repo sensor.trakt --repo sensor.brewdog
```

#### CLI options

param | alias | description
-- | -- | --
`--token` | `-T` | An GitHub `access_token` with `repo` permissions.
`--repo` | `-R` | The repo you want to show info for, can be added multiple times, is optional.
`--release_type` | `None` | Can be `major`, `minor`, `patch` or a custom tag name.
`--test` | `None` | This will print to console, and not create the release.
`--version` | `-V` | Print the installed version.

***

[![BuyMeCoffee](https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667)](https://www.buymeacoffee.com/ludeeus)
# Scripts to rule them all(-ish)

Previously we've been happily ticking along using `Makefile` to define all common actions. When it comes to testing on `TeamCity` it is required to use `Docker` and the `python-3.8` containers we want to use do _not_ contain `make`.

Helpfully `github` has a common pattern that they use called _'Scripts to rule them all'_. These scripts are used in a few high profile `python` libraries, namely `fastapi` and the `encode` libraries.

## Overview

By normalising scripts across all projects the effort to pick up a project becomes easier
and testing/ci becomes more uniform. By ensuring we can run these scripts in containers
in `TeamCity` and locally using `make` the environment will be simple and repeatable.

## Scripts

### `scripts/install`

[`scripts/env`](env) assumes there is an existing `python38` environment and will install `poetry`
for dependency management and the install the project

[`scripts/install`](install) assumes there is an existing `python38` environment and will install `poetry`
for dependency management and the install the project

### `scripts/lint`

[`scripts/lint`](lint) runs quick code formatting checks using `black`, `flake8` and `isort`. These have
t minimal configuration to ensure consistent code formatting.

### `scripts/mypy`

[`scripts/mypy`](mypy) runs static analysis to ensure types are valid. This is useful for flagging code
smell even if tests are passing.

### `scripts/test`

[`scripts/test`](test) runs `pytest test`. We actually want to be using `tox` here but there are currently issues with using
`tox` reliably with the `docker` environment.

### `scripts/release`

[`scripts/release`](release) runs creates a new commit and tag while bumping the version in `pyproject.toml`.
The developer is then responsible for pushing this commit/tag to `gitlab` to trigger the `ci` to run [publish](#scripts-publish).


### `scripts/publish`

[`scripts/publish`](publish) builds the wheel and pushes it to the private pypi repo using `poetry`.

### `scripts/format`

[`scripts/format`](format) formats the repo using `black`, `isort` and `autopep8`. Ideally this should be setup to run on save when developing.

### `scripts/docs`

[`scripts/docs`](docs) builds the documentation in `docs/` and uses `rsync` to copy it to the internal doc site.

# Continuous integration

The repository uses [GitHub Actions](.github/workflows/ci.yml) for test and build validation on every push and pull request. The workflow does not deploy or require secrets.

## Supported projects

- **Node.js**: `package.json`, with dependency installation selected from `pnpm-lock.yaml`, `yarn.lock`, Bun lockfiles, or npm lockfiles. Existing `lint`, `typecheck`, `type-check`, `test`, and `build` scripts are run; missing scripts are skipped.
- **Python**: `pyproject.toml` and/or `requirements.txt`. Requirements are installed, and checks are enabled by the relevant configuration: Ruff or Flake8, mypy, pytest, and Python build metadata.

This repository is a Python project. Its CI build installs the package and runs the tests configured in `pyproject.toml`.

An empty repository, or one without a supported manifest, passes with a visible notice. A detected project's failing install, check, or build fails the workflow.

## Extending CI

Update `.github/workflows/ci.yml` when adding another ecosystem or project convention. Keep detection explicit, install dependencies before running checks, and gate each command on the script or configuration that enables it. Prefer lockfile-based, reproducible installs for new package managers.

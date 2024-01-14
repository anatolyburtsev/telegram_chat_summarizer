
Project Template with Poetry and Pre-commit Hooks
================================================
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![pre-commit](https://github.com/anatolyburtsev/python-project-template/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/anatolyburtsev/python-project-template/actions/workflows/pre-commit.yml)

### Getting started

Install poetry:

```bash
pip install poetry
```

Install dependencies:
```bash
poetry install
```

Activate poetry virtual environment
```bash
poetry shell
```

Run script in poetry virtual env
```bash
poetry run python my_script.py
```

Add and install new dependency:
```bash
poetry add requests
```

Update all dependencies:
```bash
poetry update
```

Pre-commit Hooks: Code Quality and Consistency
---------------------------------------------
Install the hooks by running:

```bash
pre-commit install
```

Running Hooks Manually:

```bash
pre-commit run --all-files
```

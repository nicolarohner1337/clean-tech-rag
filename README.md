# Clean Tech RAG

Welcome to Clean Tech RAG! This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. Poetry provides an easy way to manage project dependencies while ensuring reproducibility and consistency across environments. This guide will help you get started with using Poetry as part of our development workflow.

## Prerequisites

Before you start, make sure you have Poetry installed. If not, you can install Poetry by following the instructions on the [official documentation](https://python-poetry.org/docs/#installation).

- Add Kaggle API keys in `.env` file
- - `KAGGLE_username` & `KAGGLE_key`
## Getting Started

Set this so that the virtual environment is created in the project directory:
```bash
poetry config virtualenvs.in-project true
```

### Installation

Once you have Poetry installed, you can set up the project dependencies by running the following command in the project's root directory:

```bash
poetry install
```

### Activating the Virtual Environment

```bash
poetry shell
```

### Adding Dependencies
```bash
poetry add <package-name>
```


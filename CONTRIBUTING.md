# Contributing Guide

Thank you for your interest in the Folder Compare project! This document will guide you on how to contribute to this project.

## Development Environment Setup

1. Clone the repository:
   ```bash
   git clone https://gitlab.com/username/folder-compare.git
   cd folder-compare
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style and Quality

We use the following tools to maintain code quality:

- **Black**: Automatic code formatting
- **isort**: Import statement sorting
- **mypy**: Type checking
- **flake8**: Code style checking

Before submitting code, please run the following commands:

```bash
# Code formatting
black src tests
isort src tests

# Code checking
mypy src
flake8 src tests
```

## Testing

We use unittest for testing. Before submitting code, please ensure all tests pass:

```bash
python -m unittest discover -s tests
```

To generate a test coverage report:

```bash
pytest --cov=src/folder_compare tests/
```

## Submitting Code

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Commit your changes:
   ```bash
   git commit -m "Descriptive commit message"
   ```

3. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Merge Request

## Release Process

1. Update the version number (in `setup.py`)
2. Update CHANGELOG.md
3. Create a tag:
   ```bash
   git tag -a v0.x.0 -m "Version 0.x.0"
   git push origin v0.x.0
   ```

## Reporting Issues

If you find any bugs or have feature requests, please create an issue on the GitLab project page. Please describe the issue in as much detail as possible, including:

- Operating system and Python version
- Steps to reproduce the issue
- Actual result vs. expected result
- Any error messages or logs

Thank you for your contribution! 
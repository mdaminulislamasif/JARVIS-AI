# Contributing to JARVIS AI

First off, thank you for considering contributing to JARVIS AI! It's people like you that make JARVIS AI such a great tool.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- **Be respectful** and inclusive
- **Be collaborative** and constructive
- **Be patient** with newcomers
- **Focus on what is best** for the community

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed**
- **Explain which behavior you expected**
- **Include screenshots if possible**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List some examples** of how it would be used

### Your First Code Contribution

Unsure where to begin? You can start by looking through these issues:

- **Beginner issues** - issues which should only require a few lines of code
- **Help wanted issues** - issues which should be a bit more involved

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the style guidelines
6. Issue that pull request!

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- pip

### Setup Steps

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/jarvis-ai.git
   cd jarvis-ai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make your changes**

6. **Test your changes**
   ```bash
   python -m pytest tests/
   ```

## 📝 Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Quotes**: Single quotes for strings, double quotes for docstrings

### Code Structure

```python
"""
Module docstring explaining the purpose of the module.
"""

import standard_library
import third_party_library
import local_module


class MyClass:
    """Class docstring."""
    
    def __init__(self):
        """Initialize the class."""
        pass
    
    def my_method(self, param):
        """
        Method docstring.
        
        Args:
            param: Description of parameter
            
        Returns:
            Description of return value
        """
        pass
```

### Documentation

- **All public functions** must have docstrings
- **Use type hints** where appropriate
- **Keep comments up to date** with code changes
- **Write clear commit messages**

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high code coverage

## 💬 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding missing tests
- **chore**: Changes to build process or auxiliary tools

### Examples

```
feat(voice): add Bangla language support

- Added Bangla voice recognition
- Updated voice selector
- Added Bangla vocabulary database

Closes #123
```

```
fix(panel): resolve button click issue

Fixed issue where buttons were not responding
to click events in the Antigravity panel.

Fixes #456
```

## 🔄 Pull Request Process

1. **Update the README.md** with details of changes if needed
2. **Update the documentation** with any new features
3. **Add tests** for new functionality
4. **Ensure all tests pass**
5. **Update the CHANGELOG.md** with your changes
6. **Request review** from maintainers
7. **Address review comments** promptly
8. **Squash commits** if requested
9. **Wait for approval** and merge

### PR Checklist

- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
- [ ] Any dependent changes have been merged

## 🏷️ Issue and PR Labels

- **bug**: Something isn't working
- **enhancement**: New feature or request
- **documentation**: Improvements or additions to documentation
- **good first issue**: Good for newcomers
- **help wanted**: Extra attention is needed
- **question**: Further information is requested
- **wontfix**: This will not be worked on
- **duplicate**: This issue or PR already exists
- **invalid**: This doesn't seem right

## 📞 Getting Help

If you need help, you can:

- Open an issue with the **question** label
- Email: asifgk.hacer@gmail.com
- Check existing documentation

## 🎉 Recognition

Contributors will be recognized in:

- README.md contributors section
- CHANGELOG.md for their contributions
- GitHub contributors page

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to JARVIS AI! 🚀

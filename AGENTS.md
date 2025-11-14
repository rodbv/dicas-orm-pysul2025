# Django Project Guidelines for AI Agents

This document provides guidelines for working on Django projects using TDD (Test-Driven Development) and pytest.

## Code Style and PEPs

### PEP 8 - Style Guide for Python Code

Follow PEP 8 for all Python code:
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black default) or 79 characters (PEP 8 strict)
- Use snake_case for function and variable names
- Use PascalCase for class names
- Use UPPER_CASE for constants

### PEP 257 - Docstring Conventions

- Write docstrings for all public modules, functions, classes, and methods
- Use triple double-quotes: `"""Docstring here."""`
- For one-line docstrings, end with a period
- For multi-line docstrings, use a summary line, blank line, then detailed description

### Import Organization (PEP 8 Section on Imports)

**CRITICAL: Imports must be:**
1. **At the top of the file** (after module docstrings and comments)
2. **Sorted and organized** in this order:
   - Standard library imports
   - Related third-party imports
   - Local application/library specific imports
3. **Grouped** with blank lines between groups
4. **Sorted alphabetically** within each group

**Use `isort` to automatically organize imports:**
```bash
# Install isort
uv add --dev isort

# Check import order
uv run isort --check-only .

# Auto-fix import order
uv run isort .
```

**Example of correct import order:**
```python
# Standard library
import os
from pathlib import Path
from typing import Optional

# Third-party
from django.db import models
from django.contrib.auth.models import User
import pytest

# Local application
from blog.models import Post
from blog.views import PostListView
```

**DO NOT:**
- ❌ Put imports in the middle of the file
- ❌ Mix import groups without blank lines
- ❌ Use wildcard imports (`from module import *`) except in specific cases
- ❌ Import unused modules

### PEP 484 - Type Hints

Use type hints for function parameters and return types:
```python
def get_user_posts(user: User) -> list[Post]:
    """Return all posts by a user."""
    return Post.objects.filter(author=user)
```

## Test-Driven Development (TDD)

### TDD Workflow

1. **Red**: Write a failing test first
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve the code while keeping tests green

### Test Structure

- Write tests before implementation
- One test should test one thing
- Use descriptive test names: `test_<what>_<condition>_<expected_result>`
- Keep tests simple and readable

### Example TDD Flow

```python
# 1. Write failing test
def test_post_has_published_status():
    post = Post(title="Test", content="Content")
    assert post.status == "published"

# 2. Implement minimal code to pass
class Post(models.Model):
    status = models.CharField(default="published", max_length=20)

# 3. Refactor if needed
```

## Django Best Practices

### Models

**DO:**
- ✅ Use descriptive field names
- ✅ Add `__str__` methods to models
- ✅ Use `Meta` class for model metadata
- ✅ Add `verbose_name` and `verbose_name_plural` in Meta
- ✅ Use appropriate field types and constraints
- ✅ Add indexes for frequently queried fields
- ✅ Use `related_name` for ForeignKey/ManyToMany relationships

**DON'T:**
- ❌ Use generic names like `name`, `field1`, `data`
- ❌ Forget to add `on_delete` for ForeignKey
- ❌ Create unnecessary database queries (use `select_related` and `prefetch_related`)

### Views

**DO:**
- ✅ Use class-based views when appropriate
- ✅ Keep views thin - move logic to models or services
- ✅ Use proper HTTP status codes
- ✅ Handle exceptions appropriately

**DON'T:**
- ❌ Put business logic in views
- ❌ Make database queries in loops
- ❌ Return sensitive data in error messages

### Querysets

**DO:**
- ✅ Use `select_related()` for ForeignKey relationships
- ✅ Use `prefetch_related()` for ManyToMany and reverse ForeignKey
- ✅ Use `only()` and `defer()` to limit fields when needed
- ✅ Use `exists()` instead of `count()` when checking existence
- ✅ Use `get_or_create()` and `update_or_create()` when appropriate

**DON'T:**
- ❌ Use `all()` when you can filter
- ❌ Make queries in loops (N+1 problem)
- ❌ Use `count()` when you only need to check existence

## Pytest Best Practices

### Test Organization

- Place tests in `tests/` directory or alongside code as `test_*.py` files
- Use pytest fixtures for test data setup
- Use pytest markers for organizing tests (`@pytest.mark.django_db`, `@pytest.mark.slow`)

### Django-Specific Pytest Usage

**DO:**
- ✅ Use `@pytest.mark.django_db` for database access
- ✅ Use `pytest-django` fixtures (`client`, `admin_client`, `django_user_model`)
- ✅ Use factories (e.g., `factory_boy`) for test data
- ✅ Use `pytest.fixture` for reusable test setup

**Example:**
```python
import pytest
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_post_creation():
    User = get_user_model()
    user = User.objects.create_user(username="test", password="test")
    post = Post.objects.create(title="Test", author=user)
    assert post.author == user
```

### Test Fixtures

Create reusable fixtures in `conftest.py`:
```python
import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(username="test", password="test")

@pytest.fixture
def post(user):
    return Post.objects.create(title="Test", author=user)
```

## Common Dos and Don'ts

### DO ✅

- ✅ Write tests first (TDD)
- ✅ Keep functions and classes small and focused
- ✅ Use meaningful variable and function names
- ✅ Add docstrings to public APIs
- ✅ Use Django's built-in features (admin, auth, etc.)
- ✅ Use migrations for all database changes
- ✅ Keep settings organized (use environment variables for secrets)
- ✅ Use `gettext_lazy` for translatable strings
- ✅ Validate data at the model level
- ✅ Use Django's `Q` objects for complex queries
- ✅ Cache expensive operations
- ✅ Use logging instead of print statements

### DON'T ❌

- ❌ Commit secrets or sensitive data
- ❌ Hardcode URLs (use `reverse()` and `get_absolute_url()`)
- ❌ Make database queries in templates
- ❌ Use `save()` in loops (use `bulk_create()`, `bulk_update()`)
- ❌ Ignore migrations
- ❌ Use `null=True` on CharField/TextField without `blank=True`
- ❌ Use `print()` for debugging (use logging or debugger)
- ❌ Import models in the middle of files
- ❌ Create circular imports
- ❌ Use `eval()` or `exec()`
- ❌ Ignore security warnings
- ❌ Write tests that depend on each other
- ❌ Leave commented-out code

## File Organization

```
project/
├── config/          # Django project settings
├── app_name/        # Django apps
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── tests.py
├── tests/           # Additional tests (if using separate test dir)
├── manage.py
├── requirements.txt # or pyproject.toml with uv
└── conftest.py      # Pytest configuration
```

## Tools and Commands

### Code Quality Tools

```bash
# Format code (Black)
uv add --dev black
uv run black .

# Sort imports (isort)
uv add --dev isort
uv run isort .

# Lint code (ruff or flake8)
uv add --dev ruff
uv run ruff check .
uv run ruff check --fix .

# Type checking (mypy)
uv add --dev mypy django-stubs
uv run mypy .
```

### Testing Commands

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run specific test file
uv run pytest tests/test_models.py

# Run tests in watch mode (if pytest-watch installed)
uv run ptw
```

## Environment Variables

Use environment variables for configuration:
- `SECRET_KEY`
- `DEBUG`
- `DATABASE_URL`
- `ALLOWED_HOSTS`

Use `python-decouple` or `django-environ` for managing environment variables.

## Security Considerations

- Never commit `SECRET_KEY` or other secrets
- Use `DEBUG=False` in production
- Validate and sanitize user input
- Use Django's CSRF protection
- Use `@login_required` or `@permission_required` decorators
- Use Django's password hashing (never store plain passwords)
- Keep dependencies updated

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [PEP 8](https://peps.python.org/pep-0008/)
- [PEP 257](https://peps.python.org/pep-0257/)
- [PEP 484](https://peps.python.org/pep-0484/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/design-philosophies/)

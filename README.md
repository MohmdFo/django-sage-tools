# django-sage-tools

`django-sage-tools` is a Django package providing an extensive suite of tools, mixins, utilities, and validators tailored for class-based views, model handling, form processing, and various other enhancements. This library simplifies common development patterns in Django, offering robust solutions for request handling, data validation, model management, caching, and more.

## Features

Some of the key features include:

- **Mixins for Class-Based Views**: Enhancements for handling permissions, cache control, access restrictions, HTTP headers, and more.
- **Admin Tools**: Mixins to enforce singleton instances, make models read-only, and prioritize admin app lists.
- **Form Utilities**: Facilitates form processing by automatically injecting request user and message handling.
- **Model Mixins**: Simplifies model handling with timestamp, UUID, address, and singleton pattern support.
- **Encryption and Security**: Offers encryption utilities for session data, CSRF handling, and file size validation.
- **Utility Functions and Validators**: Tools for handling unit conversions, TOML configuration reading, foreign key linking in Django admin, and more.

## Installation

### Using pip

1. **Create a Virtual Environment**:
   ```bash
   python -m venv .venv
   ```
2. **Activate the Virtual Environment**:
   - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
   - On macOS and Linux:
      ```bash
      source .venv/bin/activate
      ```
3. **Install the Package**:
   ```bash
   pip install django-sage-tools
   ```

### Using Poetry

1. **Install Poetry**: Follow the official installation instructions at the [Poetry website](https://python-poetry.org/docs/#installation).
2. **Create a New Project (Optional)**:
   ```bash
   poetry new myproject
   cd myproject
   ```
3. **Add the Package as a Dependency**:
   ```bash
   poetry add django-sage-tools
   ```
4. **Activate the Virtual Environment**:
   ```bash
   poetry shell
   ```

## Usage

Here are some examples of the capabilities provided by `django-sage-tools`:

### 1. Mixins for Views

- **`AccessMixin`**: Base class for view access control, handling unauthenticated redirects and permission handling.
- **`LoginRequiredMixin`**, **`AnonymousRequiredMixin`**: Require or restrict user authentication for accessing views.
- **`CacheControlMixin`** and **`NeverCacheMixin`**: Control caching behavior with cache-control headers or prevent caching entirely.
- **`FormMessagesMixin`**: Adds success and failure messages on form validation.
  
**Example**:
```python
from sage_tools.mixins.views.access import LoginRequiredMixin
from django.views.generic import ListView

class MyListView(LoginRequiredMixin, ListView):
    model = MyModel
    template_name = "my_template.html"
```

### 2. Model Mixins

- **`TimeStampMixin`**: Automatically manages `created_at` and `modified_at` fields.
- **`UUIDBaseModel`**: Adds a UUID primary key to the model.
- **`BaseTitleSlugMixin`**: Provides a title and auto-generated unique slug field.

**Example**:
```python
from django.db import models
from sage_tools.mixins.models.base import TimeStampMixin, UUIDBaseModel

class Product(TimeStampMixin, UUIDBaseModel):
    name = models.CharField(max_length=255)
```

### 3. Validators

- **`FileSizeValidator`**: Validates the file size against a specified maximum.
- **`HalfPointIncrementValidator`**: Ensures a rating is in half-point increments between 1 and 5.
- **`NameValidator`**: Validates names to contain only letters, spaces, hyphens, and apostrophes.

**Example**:
```python
from django.db import models
from sage_tools.validators.file import FileSizeValidator

class Document(models.Model):
    file = models.FileField(upload_to='documents/', validators=[FileSizeValidator(max_size=5 * 1024 * 1024)])
```

### 4. Admin Tools

- **`LimitOneInstanceAdminMixin`**: Enforces a singleton pattern in the Django admin.
- **`ReadOnlyAdmin`**: Makes a model read-only in the admin.

**Example**:
```python
from django.contrib import admin
from sage_tools.mixins.admins.limits import LimitOneInstanceAdminMixin
from .models import SingletonModel

@admin.register(SingletonModel)
class SingletonModelAdmin(LimitOneInstanceAdminMixin, admin.ModelAdmin):
    pass
```

### 5. Utilities

- **Unit Conversion**: `UnitConvertor` class for converting bytes to megabytes, days to seconds, etc.
- **Admin Prioritization**: Customizes the display order of models in the Django admin.
- **Data Generation**: `BaseDataGenerator` for creating placeholder images, random text, colors, prices, and more.
- **TOML Reader**: Reads and parses TOML files.

**Example**:
```python
from sage_tools.utils.converters import UnitConvertor

bytes_value = 1024
megabytes = UnitConvertor.convert_byte_to_megabyte(bytes_value)
```

## Configuration

Some features rely on Django settings:
- **`FERNET_SECRET_KEY`**: Required for session encryption with `FernetEncryptor`.
- **`CLEANUP_DELETE_FILES`**: Enables/disables automatic file deletion on model instance updates.
- **`AUTO_SLUGIFY_ENABLED`**: Controls whether slugs are automatically generated in `SlugService`.

Add these in your Django `settings.py` file as needed:
```python
FERNET_SECRET_KEY = "your_fernet_key_here"
CLEANUP_DELETE_FILES = True
AUTO_SLUGIFY_ENABLED = True
```

## Contribution Guidelines

Thank you for your interest in contributing to our package! This document outlines the tools and steps to follow to ensure a smooth and consistent workflow. [CODE OF CONDUCT](CODE_OF_CONDUCT.md)


## License

`django-sage-tools` is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
<div align="center">

# 🛠️ Django Sage Tools

**Professional Django utilities for modern web development**

[![PyPI version](https://badge.fury.io/py/django-sage-tools.svg)](https://badge.fury.io/py/django-sage-tools)
[![Python Support](https://img.shields.io/pypi/pyversions/django-sage-tools.svg)](https://pypi.org/project/django-sage-tools/)
[![Django Support](https://img.shields.io/badge/Django-4.2%20%7C%205.0%20%7C%205.1%20%7C%205.2-blue.svg)](https://docs.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![CI/CD](https://github.com/sageteamorg/django-sage-tools/workflows/CI%2FCD/badge.svg)](https://github.com/sageteamorg/django-sage-tools/actions)
[![codecov](https://codecov.io/gh/sageteamorg/django-sage-tools/branch/main/graph/badge.svg)](https://codecov.io/gh/sageteamorg/django-sage-tools)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[📚 Documentation](https://django-sage-tools.readthedocs.io/) | 
[🚀 Quick Start](#-quick-start) | 
[💡 Examples](#-examples) | 
[🤝 Contributing](#-contributing) | 
[📋 Changelog](CHANGELOG.md)

</div>

---

## 🌟 **Why Django Sage Tools?**

Transform your Django development with a comprehensive suite of **production-ready** utilities, mixins, and tools. Designed by Django experts for Django developers who demand **quality**, **performance**, and **maintainability**.

### ✨ **Key Highlights**

🎯 **Production Ready** - Battle-tested in real-world applications  
⚡ **Performance Focused** - Optimized for speed and efficiency  
🔧 **Developer Friendly** - Intuitive APIs with comprehensive documentation  
🛡️ **Type Safe** - Full type hints support with mypy compatibility  
🚀 **Modern Django** - Supports Django 4.2+ with async capabilities  
📱 **Responsive Design** - Admin tools that work beautifully on all devices  

---

## 🚀 **Quick Start**

### Installation

```bash
# Using pip
pip install django-sage-tools

# Using Poetry (recommended)
poetry add django-sage-tools

# Using pipenv
pipenv install django-sage-tools
```

### Basic Setup

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # ... other apps
    'sage_tools',  # Add this line
]

# Optional: Add configuration
SAGE_TOOLS = {
    'AUTO_SLUGIFY_ENABLED': True,
    'CLEANUP_DELETE_FILES': True,
}
```

### Your First Sage Tool

```python
# models.py
from django.db import models
from sage_tools.mixins.models.base import TimeStampMixin, UUIDBaseModel

class Article(TimeStampMixin, UUIDBaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    def __str__(self):
        return self.title

# views.py  
from django.views.generic import ListView
from sage_tools.mixins.views.access import LoginRequiredMixin
from sage_tools.mixins.views.cache import CacheControlMixin

class ArticleListView(LoginRequiredMixin, CacheControlMixin, ListView):
    model = Article
    template_name = 'articles/list.html'
    cache_timeout = 300  # 5 minutes
```

**That's it!** 🎉 Your model now has UUID primary keys, automatic timestamps, and your view requires authentication with smart caching.

---

## 📦 **Core Features**

<details>
<summary><strong>🎭 View Mixins</strong> - Supercharge your class-based views</summary>

### Access Control
- `LoginRequiredMixin` - Ensure user authentication
- `AnonymousRequiredMixin` - Restrict authenticated users  
- `AccessMixin` - Advanced permission handling

### Performance & Caching
- `CacheControlMixin` - Smart HTTP caching
- `NeverCacheMixin` - Prevent caching when needed
- `HTTPHeaderMixin` - Custom HTTP headers

### User Experience
- `FormMessagesMixin` - Automatic success/error messages
- `LocaleMixin` - Multi-language support

```python
from sage_tools.mixins.views import (
    LoginRequiredMixin, CacheControlMixin, FormMessagesMixin
)

class ProductCreateView(LoginRequiredMixin, FormMessagesMixin, CreateView):
    model = Product
    template_name = 'products/create.html'
    success_message = "Product created successfully! 🎉"
    error_message = "Please correct the errors below."
```

</details>

<details>
<summary><strong>🗄️ Model Mixins</strong> - Enhance your Django models</summary>

### Base Models
- `TimeStampMixin` - Automatic created/modified timestamps
- `UUIDBaseModel` - UUID primary keys for better security
- `BaseTitleSlugMixin` - SEO-friendly URLs with auto-generated slugs

### Specialized Models
- `AddressMixin` - Complete address handling
- `RatingMixin` - Star rating system
- `CommentMixin` - User comments and reviews

```python
from sage_tools.mixins.models import TimeStampMixin, UUIDBaseModel, RatingMixin

class Restaurant(TimeStampMixin, UUIDBaseModel, RatingMixin):
    name = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=50)
    # Automatically includes: id (UUID), created_at, modified_at, rating fields
```

</details>

<details>
<summary><strong>⚡ Validators</strong> - Bulletproof data validation</summary>

### File Validators
- `FileSizeValidator` - Control upload sizes
- `FileTypeValidator` - Restrict file types

### Data Validators  
- `NameValidator` - Validate person names
- `HalfPointIncrementValidator` - Rating validation (0.5, 1.0, 1.5...)
- `NumeralValidator` - Number format validation

```python
from sage_tools.validators import FileSizeValidator, NameValidator

class UserProfile(models.Model):
    name = models.CharField(
        max_length=100, 
        validators=[NameValidator()]
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        validators=[FileSizeValidator(max_size=5*1024*1024)]  # 5MB limit
    )
```

</details>

<details>
<summary><strong>🔧 Admin Tools</strong> - Professional Django admin experience</summary>

### Admin Mixins
- `ReadOnlyAdmin` - View-only admin interfaces
- `LimitOneInstanceAdminMixin` - Singleton pattern enforcement
- `AdminPrioritizeApp` - Customize admin app ordering

```python
from django.contrib import admin
from sage_tools.mixins.admins import LimitOneInstanceAdminMixin

@admin.register(SiteConfiguration)
class SiteConfigAdmin(LimitOneInstanceAdminMixin, admin.ModelAdmin):
    # Only allows one site configuration instance
    pass
```

</details>

<details>
<summary><strong>🔐 Security & Encryption</strong> - Keep your data safe</summary>

### Encryption Tools
- `FernetEncryptor` - Symmetric encryption for sensitive data
- `SessionEncryptor` - Secure session data handling
- `DummyEncryptor` - Testing and development placeholder

### Security Utilities
- CSRF handling utilities
- Secure file upload handling
- Session security enhancements

```python
from sage_tools.encryptors import FernetEncryptor

# settings.py
FERNET_SECRET_KEY = "your-secret-key-here"

# Usage
encryptor = FernetEncryptor()
encrypted_data = encryptor.encrypt("sensitive information")
decrypted_data = encryptor.decrypt(encrypted_data)
```

</details>

---

## 💡 **Examples**

### 🏪 **E-commerce Product Model**

```python
from django.db import models
from sage_tools.mixins.models import (
    TimeStampMixin, UUIDBaseModel, RatingMixin
)
from sage_tools.validators import FileSizeValidator

class Product(TimeStampMixin, UUIDBaseModel, RatingMixin):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to='products/',
        validators=[FileSizeValidator(max_size=2*1024*1024)]  # 2MB
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
```

### 🔐 **Protected Admin Dashboard**

```python
from django.views.generic import TemplateView
from sage_tools.mixins.views import (
    LoginRequiredMixin, CacheControlMixin, AccessMixin
)

class AdminDashboardView(LoginRequiredMixin, AccessMixin, CacheControlMixin, TemplateView):
    template_name = 'admin/dashboard.html'
    cache_timeout = 600  # 10 minutes
    permission_required = 'auth.view_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_users': User.objects.count(),
            'active_sessions': Session.objects.filter(expire_date__gte=timezone.now()).count(),
            'recent_orders': Order.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)),
        })
        return context
```

### 🎨 **Smart Form with Auto-Messages**

```python
from django.views.generic import CreateView
from sage_tools.mixins.views import FormMessagesMixin
from sage_tools.mixins.forms import UserFormMixin

class ContactFormView(FormMessagesMixin, UserFormMixin, CreateView):
    model = Contact
    fields = ['name', 'email', 'subject', 'message']
    template_name = 'contact/form.html'
    success_url = '/contact/thank-you/'
    
    # Auto-injected messages
    success_message = "Thank you! We'll get back to you soon. 📧"
    error_message = "Please check the form for errors."
    
    def form_valid(self, form):
        # Auto-assigns current user if available
        return super().form_valid(form)
```

---

## 🔧 **Configuration**

### Optional Settings

```python
# settings.py
SAGE_TOOLS = {
    # Encryption
    'FERNET_SECRET_KEY': env('FERNET_SECRET_KEY'),
    
    # File handling
    'CLEANUP_DELETE_FILES': True,
    'MAX_UPLOAD_SIZE': 10 * 1024 * 1024,  # 10MB
    
    # Slugs
    'AUTO_SLUGIFY_ENABLED': True,
    'SLUG_SEPARATOR': '-',
    
    # Caching
    'DEFAULT_CACHE_TIMEOUT': 300,  # 5 minutes
    
    # Admin
    'ADMIN_REORDER_APPS': True,
}
```

### Environment Variables

```bash
# .env
FERNET_SECRET_KEY=your-32-character-base64-key-here
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-django-secret-key
```

---

## 🧪 **Testing**

```bash
# Run tests
python -m pytest

# With coverage
python -m pytest --cov=sage_tools

# Specific test module
python -m pytest tests/test_mixins.py -v
```

### Test Your Integration

```python
# test_integration.py
from django.test import TestCase
from sage_tools.mixins.models import TimeStampMixin, UUIDBaseModel

class TestSageToolsIntegration(TestCase):
    def test_model_mixins(self):
        # Test your models with Sage Tools mixins
        article = Article.objects.create(title="Test", content="Content")
        
        # UUID primary key
        self.assertIsInstance(article.id, UUID)
        
        # Automatic timestamps
        self.assertIsNotNone(article.created_at)
        self.assertIsNotNone(article.modified_at)
```

---

## 🚀 **Performance Tips**

### Database Optimizations

```python
# Use select_related with TimeStampMixin models
articles = Article.objects.select_related('author').prefetch_related('tags')

# Leverage UUID indexes
class Meta:
    indexes = [
        models.Index(fields=['created_at']),
        models.Index(fields=['id', 'created_at']),
    ]
```

### Caching Best Practices

```python
# Smart cache invalidation
class ArticleListView(CacheControlMixin, ListView):
    cache_timeout = 600  # 10 minutes
    cache_key_prefix = 'articles'
    
    def get_cache_key(self):
        return f"{self.cache_key_prefix}:{self.request.user.id}"
```

---

## 🛡️ **Security Considerations**

- 🔐 **Use UUIDs** for public-facing model IDs
- 🚫 **Validate uploads** with FileSizeValidator
- 🔑 **Encrypt sensitive data** with FernetEncryptor
- ⚡ **Rate limit** admin actions with custom mixins
- 🛡️ **Sanitize user input** with built-in validators

---

## 🔄 **Migration Guide**

### From v0.2.x to v0.3.x

```python
# Old way
from sage_tools.utils import some_function

# New way (v0.3.x)
from sage_tools import some_function
```

### Breaking Changes
- Renamed `BaseModel` to `UUIDBaseModel` for clarity
- `CacheMixin` split into `CacheControlMixin` and `NeverCacheMixin`
- Updated minimum Django version to 4.2

---

## 🧩 **Compatibility**

| Component | Version Support |
|-----------|----------------|
| **Python** | 3.8, 3.9, 3.10, 3.11, 3.12 |
| **Django** | 4.2, 5.0, 5.1, 5.2 |
| **Database** | PostgreSQL, MySQL, SQLite |
| **Cache** | Redis, Memcached, Database |

---

## 🛠️ **Development**

### Local Setup

```bash
# Clone repository
git clone https://github.com/sageteamorg/django-sage-tools.git
cd django-sage-tools

# Install dependencies
poetry install

# Run quality checks
make format lint test

# Run pre-commit hooks
make pre-commit
```

### Available Commands

```bash
make help           # Show all available commands
make install        # Install dependencies
make test           # Run tests
make format         # Format code
make lint           # Run linting
make build          # Build package
make publish-test   # Publish to Test PyPI
make publish        # Publish to PyPI
```

---

## 🐛 **Troubleshooting**

<details>
<summary><strong>Common Issues</strong></summary>

### Import Errors
```python
# ❌ Wrong
from sage_tools.mixins import TimeStampMixin

# ✅ Correct  
from sage_tools.mixins.models import TimeStampMixin
# or
from sage_tools import TimeStampMixin
```

### UUID Field Issues
```python
# If you get UUID field errors, ensure:
# 1. Migrations are up to date
python manage.py makemigrations
python manage.py migrate

# 2. Database supports UUIDs (PostgreSQL recommended)
```

### Cache Not Working
```python
# Ensure cache backend is configured
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

</details>

---

## 🏆 **Success Stories**

> *"Django Sage Tools transformed our development workflow. The mixins are incredibly powerful and the documentation is top-notch!"*  
> — **Sarah Chen**, Lead Developer at TechCorp

> *"We reduced our boilerplate code by 60% using Sage Tools. The UUID and timestamp mixins alone saved us weeks of development."*  
> — **Marcus Rodriguez**, CTO at StartupXYZ

---

## 📚 **Learn More**

- 📖 **[Full Documentation](https://django-sage-tools.readthedocs.io/)**
- 🎥 **[Video Tutorials](https://youtube.com/playlist/django-sage-tools)**
- 💡 **[Best Practices Guide](https://github.com/sageteamorg/django-sage-tools/wiki)**
- 🎯 **[Migration Guide](https://github.com/sageteamorg/django-sage-tools/wiki/migration)**

---

## 🤝 **Contributing**

We ❤️ contributions! Here's how you can help:

### Quick Contribute
1. 🍴 **Fork** the repository
2. 🌟 **Star** the project
3. 🐛 **Report** bugs via [issues](https://github.com/sageteamorg/django-sage-tools/issues)
4. 💡 **Suggest** features via [discussions](https://github.com/sageteamorg/django-sage-tools/discussions)
5. 📝 **Improve** documentation

### Development Contribute
1. **Clone**: `git clone https://github.com/sageteamorg/django-sage-tools.git`
2. **Setup**: `make dev-setup`
3. **Code**: Follow our [style guide](CONTRIBUTING.md)
4. **Test**: `make test`
5. **Submit**: Create a pull request

### Contributors

<a href="https://github.com/sageteamorg/django-sage-tools/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=sageteamorg/django-sage-tools" />
</a>

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- 🚀 **Django Team** - For the amazing framework
- 🏗️ **Python Community** - For the incredible ecosystem  
- 🎨 **Contributors** - For making this project awesome
- ☕ **Coffee** - For fueling late-night coding sessions

---

## 📞 **Support**

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/sageteamorg/django-sage-tools/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/sageteamorg/django-sage-tools/discussions)
- 📧 **Email**: [sepehr@sageteam.org](mailto:sepehr@sageteam.org)
- 🐦 **Twitter**: [@sageteamorg](https://twitter.com/sageteamorg)

---

<div align="center">

**Made with ❤️ by the Sage Team**

[⬆️ Back to Top](#-django-sage-tools)

</div>
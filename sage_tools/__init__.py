"""
Django Sage Tools - Comprehensive Django utility package.

Provides mixins, validators, decorators, and tools for enhanced Django development.
"""

__version__ = "2.0.0"
__author__ = "Sepehr Akbarzadeh"
__email__ = "sepehr@sageteam.org"

# Safe imports (no Django dependencies)
from .encryptors.base import Encryptor
from .encryptors.dummy import DummyEncryptor
from .utils.converters import UnitConvertor
from .validators.file import FileSizeValidator
from .validators.numeral import HalfPointIncrementValidator
from .validators.string import NameValidator

# Import non-model components safely
try:
    from .encryptors.fernet_encrypt import FernetEncryptor
except ImportError:
    # FernetEncryptor requires cryptography package
    FernetEncryptor = None


# Lazy imports for Django-dependent components
def get_model_mixins():
    """Get model mixins (lazy import to avoid app registry issues)."""
    from .mixins.models.base import BaseTitleSlugMixin, TimeStampMixin, UUIDBaseModel

    return {
        "BaseTitleSlugMixin": BaseTitleSlugMixin,
        "TimeStampMixin": TimeStampMixin,
        "UUIDBaseModel": UUIDBaseModel,
    }


def get_view_mixins():
    """Get view mixins (lazy import to avoid app registry issues)."""
    from .mixins.views.access import (
        AccessMixin,
        AnonymousRequiredMixin,
        LoginRequiredMixin,
    )
    from .mixins.views.cache import CacheControlMixin, NeverCacheMixin

    return {
        "AccessMixin": AccessMixin,
        "AnonymousRequiredMixin": AnonymousRequiredMixin,
        "LoginRequiredMixin": LoginRequiredMixin,
        "CacheControlMixin": CacheControlMixin,
        "NeverCacheMixin": NeverCacheMixin,
    }


def get_admin_mixins():
    """Get admin mixins (lazy import to avoid app registry issues)."""
    from .mixins.admins.limits import LimitOneInstanceAdminMixin, ReadOnlyAdmin

    return {
        "LimitOneInstanceAdminMixin": LimitOneInstanceAdminMixin,
        "ReadOnlyAdmin": ReadOnlyAdmin,
    }


def get_form_mixins():
    """Get form mixins (lazy import to avoid app registry issues)."""
    from .mixins.forms.user import FormMessagesMixin

    return {
        "FormMessagesMixin": FormMessagesMixin,
    }


def get_data_generator():
    """Get data generator (lazy import to avoid app registry issues)."""
    from .repository.generator.base import BaseDataGenerator

    return BaseDataGenerator


def get_slug_service():
    """Get slug service (lazy import to avoid app registry issues)."""
    from .services.slug import SlugService

    return SlugService


# Define what's available for direct import (safe components only)
__all__ = [
    # Version info
    "__version__",
    # Safe imports (no Django dependencies)
    "Encryptor",
    "DummyEncryptor",
    "FernetEncryptor",  # May be None if cryptography not installed
    "UnitConvertor",
    "FileSizeValidator",
    "HalfPointIncrementValidator",
    "NameValidator",
    # Lazy import functions for Django-dependent components
    "get_model_mixins",
    "get_view_mixins",
    "get_admin_mixins",
    "get_form_mixins",
    "get_data_generator",
    "get_slug_service",
]


# Add a helper function to get all mixins at once
def get_all_mixins():
    """Get all mixins in one call (lazy import)."""
    mixins = {}
    mixins.update(get_model_mixins())
    mixins.update(get_view_mixins())
    mixins.update(get_admin_mixins())
    mixins.update(get_form_mixins())
    return mixins


__all__.append("get_all_mixins")

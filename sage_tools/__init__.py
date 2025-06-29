"""
Django Sage Tools - Comprehensive Django utility package.

Provides mixins, validators, decorators, and tools for enhanced Django development.
"""

__version__ = "0.3.6"
__author__ = "Sepehr Akbarzadeh"
__email__ = "sepehr@sageteam.org"

# Encryptors
from .encryptors.base import Encryptor
from .encryptors.dummy import DummyEncryptor
from .encryptors.fernet_encrypt import FernetEncryptor
from .mixins.admins.limits import LimitOneInstanceAdminMixin, ReadOnlyAdmin
from .mixins.forms.user import FormMessagesMixin
from .mixins.models.base import BaseTitleSlugMixin, TimeStampMixin, UUIDBaseModel

# Core mixins
from .mixins.views.access import AccessMixin, AnonymousRequiredMixin, LoginRequiredMixin
from .mixins.views.cache import CacheControlMixin, NeverCacheMixin
from .repository.generator.base import BaseDataGenerator
from .services.slug import SlugService

# Utilities
from .utils.converters import UnitConvertor

# Validators
from .validators.file import FileSizeValidator
from .validators.numeral import HalfPointIncrementValidator
from .validators.string import NameValidator

__all__ = [
    # Version info
    "__version__",
    # View mixins
    "AccessMixin",
    "LoginRequiredMixin",
    "AnonymousRequiredMixin",
    "CacheControlMixin",
    "NeverCacheMixin",
    "FormMessagesMixin",
    # Model mixins
    "TimeStampMixin",
    "UUIDBaseModel",
    "BaseTitleSlugMixin",
    # Admin mixins
    "LimitOneInstanceAdminMixin",
    "ReadOnlyAdmin",
    # Validators
    "FileSizeValidator",
    "HalfPointIncrementValidator",
    "NameValidator",
    # Utilities
    "UnitConvertor",
    "BaseDataGenerator",
    "SlugService",
    # Encryptors
    "Encryptor",
    "FernetEncryptor",
    "DummyEncryptor",
]

"""Django Sage Tools System Checks."""

from typing import List

from django.conf import settings
from django.core.checks import CheckMessage, Error, Warning


def check_sage_tools_configuration(app_configs, **kwargs) -> List[CheckMessage]:
    """Check Sage Tools configuration for common issues."""
    errors = []

    # Check for Fernet secret key if using encryption
    if hasattr(settings, "SAGE_TOOLS"):
        sage_tools_config = settings.SAGE_TOOLS

        # Check Fernet encryption configuration
        if sage_tools_config.get("FERNET_SECRET_KEY"):
            fernet_key = sage_tools_config.get("FERNET_SECRET_KEY")
            if not isinstance(fernet_key, str) or len(fernet_key) < 32:
                errors.append(
                    Error(
                        "FERNET_SECRET_KEY must be a valid 32-character base64 key.",
                        hint="Use Fernet.generate_key() to generate a proper key.",
                        id="sage_tools.E001",
                    )
                )

        # Check cache configuration if caching mixins are used
        if not hasattr(settings, "CACHES") or not settings.CACHES:
            errors.append(
                Warning(
                    "No cache configuration found. Cache mixins will not work properly.",
                    hint="Configure Django caching for optimal performance with Sage Tools.",
                    id="sage_tools.W001",
                )
            )

    # Check for Django admin if admin mixins are used
    if "django.contrib.admin" not in settings.INSTALLED_APPS:
        errors.append(
            Warning(
                "Django admin not installed. Admin mixins will not function.",
                hint="Add 'django.contrib.admin' to INSTALLED_APPS if using admin mixins.",
                id="sage_tools.W002",
            )
        )

    # Check database configuration for UUID fields
    db_engine = settings.DATABASES.get("default", {}).get("ENGINE", "")
    if "sqlite" in db_engine:
        errors.append(
            Warning(
                "SQLite detected. UUID performance may be suboptimal.",
                hint="Consider PostgreSQL for better UUID support in production.",
                id="sage_tools.W003",
            )
        )

    return errors

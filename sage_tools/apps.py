"""Django Sage Tools App Configuration."""

from django.apps import AppConfig
from django.core.checks import register
from django.utils.translation import gettext_lazy as _


class SageToolsConfig(AppConfig):
    """Configuration for Django Sage Tools application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "sage_tools"
    verbose_name = _("Django Sage Tools")

    def ready(self) -> None:
        """Initialize the app when Django starts."""
        super().ready()

        # Register system checks
        from .checks import check_sage_tools_configuration

        register(check_sage_tools_configuration)

        # Import signals if any exist
        try:
            from . import signals  # noqa: F401
        except ImportError:
            pass

        # Auto-discover and register admin customizations
        self._setup_admin_integrations()

    def _setup_admin_integrations(self) -> None:
        """Set up Django admin integrations."""
        try:
            from .utils.admin_prioritize import AdminPrioritizeApp

            # Apply admin app prioritization if configured
            AdminPrioritizeApp.setup()
        except ImportError:
            # Admin not available or admin prioritize not configured
            pass

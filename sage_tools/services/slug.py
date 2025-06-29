"""Slug generation service for Django models."""

import logging
from typing import Any, Optional

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.utils.text import slugify

logger = logging.getLogger(__name__)


class SlugService:
    """A service class for handling slug creation and uniqueness for a given model instance.

    The `SlugService` class provides methods to create slugs from the instance title,
    check if a slug has been modified, and ensure the uniqueness of slugs within the model.
    It uses caching to improve performance and supports various configuration options.

    Features:
        - Automatic slug generation from title
        - Unique slug enforcement with counter suffixes
        - Performance optimization through caching
        - Configurable slug generation settings
        - Robust error handling and logging

    Example:
        >>> instance = MyModel(title="My Great Title")
        >>> service = SlugService(instance)
        >>> instance.slug = service.create_unique_slug()
        >>> instance.save()
    """

    def __init__(
        self, instance: Any, slug_field: str = "slug", title_field: str = "title"
    ) -> None:
        """Initialize the slug service.

        Args:
            instance: The model instance to generate a slug for
            slug_field: Name of the slug field (default: 'slug')
            title_field: Name of the title field (default: 'title')

        Raises:
            ValueError: If required fields are missing from the instance
        """
        self.instance = instance
        self.slug_field = slug_field
        self.title_field = title_field

        # Validate instance has required fields
        if not hasattr(instance, slug_field):
            raise ValueError(f"Instance must have a '{slug_field}' field")
        if not hasattr(instance, title_field):
            raise ValueError(f"Instance must have a '{title_field}' field")

        # Configuration
        self.auto_slugify_enabled: bool = getattr(
            settings, "AUTO_SLUGIFY_ENABLED", True
        )
        self.max_slug_length: int = getattr(settings, "MAX_SLUG_LENGTH", 50)
        self.cache_timeout: int = getattr(
            settings, "SLUG_CACHE_TIMEOUT", 300  # 5 minutes
        )
        self.use_cache: bool = getattr(settings, "SLUG_USE_CACHE", True)

    def _get_title(self) -> str:
        """Get the title from the instance."""
        title = getattr(self.instance, self.title_field, "")
        if not title:
            raise ValueError(f"Instance {self.title_field} field is empty")
        return str(title)

    def _get_current_slug(self) -> str:
        """Get the current slug from the instance."""
        return getattr(self.instance, self.slug_field, "") or ""

    def _create_slug(self) -> str:
        """Generate a slug from the instance title if auto-slugify is enabled,
        otherwise use the existing slug.

        Returns:
            Generated or existing slug string
        """
        if self.auto_slugify_enabled:
            title = self._get_title()
            base_slug = slugify(title, allow_unicode=True)
            # Truncate if necessary, leaving room for counter suffix
            if (
                len(base_slug) > self.max_slug_length - 10
            ):  # Reserve space for "-999999"
                base_slug = base_slug[: self.max_slug_length - 10]
            return base_slug

        current_slug = self._get_current_slug()
        if not current_slug:
            # Fallback to auto-generation if no slug exists
            logger.warning(
                f"Auto-slugify disabled but no slug found for {self.instance.__class__.__name__}. "
                "Generating from title as fallback."
            )
            return self._create_slug_from_title()
        return current_slug

    def _create_slug_from_title(self) -> str:
        """Create slug from title regardless of auto_slugify setting."""
        title = self._get_title()
        return slugify(title, allow_unicode=True)

    def _get_cache_key(self, slug: str) -> str:
        """Generate cache key for slug uniqueness check."""
        model_name = self.instance.__class__.__name__.lower()
        return f"slug_exists:{model_name}:{slug}"

    def _is_slug_unique(self, slug: str) -> bool:
        """Check if a given slug is unique among the instances.

        Uses caching to improve performance for repeated checks.

        Args:
            slug: The slug to check for uniqueness

        Returns:
            True if slug is unique, False otherwise
        """
        if not slug:
            return False

        # Check cache first
        if self.use_cache:
            cache_key = self._get_cache_key(slug)
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return not cached_result  # Cache stores existence, we want uniqueness

        # Query database
        try:
            queryset = type(self.instance).objects.filter(**{self.slug_field: slug})
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)

            exists = queryset.exists()

            # Cache the result
            if self.use_cache:
                cache_key = self._get_cache_key(slug)
                cache.set(cache_key, exists, self.cache_timeout)

            return not exists

        except Exception as e:
            logger.error(f"Error checking slug uniqueness for '{slug}': {e}")
            return False

    def _generate_unique_slug(self, base_slug: str) -> str:
        """Generate a unique slug by appending a counter if needed.

        Args:
            base_slug: The base slug to make unique

        Returns:
            A unique slug string
        """
        if not base_slug:
            raise ValueError("Base slug cannot be empty")

        new_slug = base_slug
        counter = 1
        max_attempts = 1000  # Prevent infinite loops

        while not self._is_slug_unique(new_slug) and counter <= max_attempts:
            counter_str = str(counter)
            available_length = (
                self.max_slug_length - len(counter_str) - 1
            )  # -1 for hyphen
            truncated_base = (
                base_slug[:available_length] if available_length > 0 else base_slug
            )
            new_slug = f"{truncated_base}-{counter_str}"
            counter += 1

        if counter > max_attempts:
            logger.error(
                f"Failed to generate unique slug after {max_attempts} attempts for base: {base_slug}"
            )
            # Fallback: use timestamp
            import time

            timestamp = str(int(time.time()))
            available_length = self.max_slug_length - len(timestamp) - 1
            truncated_base = (
                base_slug[:available_length] if available_length > 0 else base_slug
            )
            new_slug = f"{truncated_base}-{timestamp}"

        return new_slug

    def has_slug_changed(self, new_slug: Optional[str] = None) -> bool:
        """Check if the slug has been modified compared to the stored slug.

        Args:
            new_slug: The new slug to compare (optional, will generate if not provided)

        Returns:
            True if slug has changed, False otherwise
        """
        if not self.instance.pk:
            return False

        try:
            existing_instance = type(self.instance).objects.get(pk=self.instance.pk)
            existing_slug = getattr(existing_instance, self.slug_field, "")

            if new_slug is None:
                new_slug = self._create_slug()

            return existing_slug != new_slug

        except type(self.instance).DoesNotExist:
            logger.warning(f"Instance with pk {self.instance.pk} not found in database")
            return False
        except Exception as e:
            logger.error(f"Error checking slug change: {e}")
            return False

    @transaction.atomic
    def create_unique_slug(self) -> str:
        """Create and return a unique slug for the instance.

        This method is wrapped in a database transaction to ensure consistency.

        Returns:
            A unique slug string

        Raises:
            ValueError: If slug generation fails
        """
        try:
            base_slug = self._create_slug()
            if not base_slug:
                raise ValueError("Generated base slug is empty")

            unique_slug = self._generate_unique_slug(base_slug)

            logger.debug(
                f"Generated slug '{unique_slug}' for {self.instance.__class__.__name__}"
            )
            return unique_slug

        except Exception as e:
            logger.error(f"Failed to create unique slug: {e}")
            raise ValueError(f"Slug generation failed: {e}") from e

    def clear_cache(self, slug: Optional[str] = None) -> None:
        """Clear cached slug existence data.

        Args:
            slug: Specific slug to clear from cache (optional, clears current slug if not provided)
        """
        if not self.use_cache:
            return

        if slug is None:
            slug = self._get_current_slug()

        if slug:
            cache_key = self._get_cache_key(slug)
            cache.delete(cache_key)
            logger.debug(f"Cleared cache for slug: {slug}")

    def validate_slug(self, slug: str) -> bool:
        """Validate that a slug meets basic requirements.

        Args:
            slug: The slug to validate

        Returns:
            True if valid, False otherwise
        """
        if not slug:
            return False

        if len(slug) > self.max_slug_length:
            return False

        # Check for valid slug characters (letters, numbers, hyphens, underscores)
        import re

        if not re.match(r"^[\w-]+$", slug):
            return False

        return True

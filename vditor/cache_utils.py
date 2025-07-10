"""
Cache utilities for Django Vditor.

This module provides caching functionality to improve performance
of the Vditor editor components.
"""

import hashlib
import logging
from functools import wraps
from typing import Any, Callable, Optional

from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

# Default cache timeouts (in seconds)
DEFAULT_CONFIG_CACHE_TIMEOUT = 300  # 5 minutes
DEFAULT_TEMPLATE_CACHE_TIMEOUT = 3600  # 1 hour
DEFAULT_STATIC_CACHE_TIMEOUT = 86400  # 24 hours

# Cache version for invalidation
CACHE_VERSION = "1.0"


def get_cache_key(*args: Any, prefix: str = "vditor") -> str:
    """Generate a cache key from arguments with version control.

    Args:
        *args: Arguments to include in cache key
        prefix: Cache key prefix

    Returns:
        Generated cache key
    """
    # Create a hash of the arguments for a consistent key
    key_data = "|".join(str(arg) for arg in args)
    # Use full hash to avoid collisions
    key_hash = hashlib.sha256(key_data.encode()).hexdigest()
    return f"{prefix}:{CACHE_VERSION}:{key_hash}"


def cache_result(timeout: Optional[int] = None, key_prefix: str = "vditor") -> Callable:
    """Decorator to cache function results with improved error handling.

    Args:
        timeout: Cache timeout in seconds
        key_prefix: Prefix for cache keys

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # Generate cache key from function name and arguments
                cache_key = get_cache_key(
                    func.__name__, args, tuple(sorted(kwargs.items())), 
                    prefix=key_prefix
                )

                # Try to get from cache first
                result = cache.get(cache_key)
                if result is not None:
                    logger.debug(f"Cache hit for {func.__name__}: {cache_key}")
                    return result

                # Cache miss - execute function
                logger.debug(f"Cache miss for {func.__name__}: {cache_key}")
                result = func(*args, **kwargs)

                # Store in cache with error handling
                cache_timeout = timeout or DEFAULT_CONFIG_CACHE_TIMEOUT
                try:
                    cache.set(cache_key, result, cache_timeout)
                except Exception as e:
                    logger.warning(f"Failed to cache result for {func.__name__}: {e}")
                    # Continue without caching rather than failing

                return result
            except Exception as e:
                logger.error(f"Cache decorator error for {func.__name__}: {e}")
                # Fallback to direct function call
                return func(*args, **kwargs)

        return wrapper

    return decorator


class ConfigCache:
    """Cache manager for Vditor configurations."""

    @staticmethod
    def get_config(config_name: str) -> Optional[dict]:
        """Get configuration from cache.

        Args:
            config_name: Name of configuration

        Returns:
            Cached configuration dict or None if not found
        """
        cache_key = f"vditor_config:{config_name}"
        return cache.get(cache_key)

    @staticmethod
    def set_config(
        config_name: str, config_dict: dict, timeout: Optional[int] = None
    ) -> None:
        """Store configuration in cache.

        Args:
            config_name: Name of configuration
            config_dict: Configuration dictionary
            timeout: Cache timeout in seconds
        """
        cache_key = f"vditor_config:{config_name}"
        cache_timeout = timeout or DEFAULT_CONFIG_CACHE_TIMEOUT
        cache.set(cache_key, config_dict, cache_timeout)
        logger.debug(
            f"Cached configuration '{config_name}' for {cache_timeout} seconds"
        )

    @staticmethod
    def invalidate_config(config_name: str) -> None:
        """Invalidate configuration cache.

        Args:
            config_name: Name of configuration to invalidate
        """
        cache_key = f"vditor_config:{config_name}"
        cache.delete(cache_key)
        logger.debug(f"Invalidated configuration cache for '{config_name}'")

    @staticmethod
    def invalidate_all() -> None:
        """Invalidate all configuration caches."""
        # This is a simple implementation - in production you might want
        # to use cache versioning or store keys in a set
        try:
            if hasattr(cache, "delete_pattern"):
                cache.delete_pattern("vditor_config:*")
            else:
                # Fallback for cache backends that don't support patterns
                logger.warning("Cache backend doesn't support pattern deletion")
        except Exception as e:
            logger.error(f"Failed to invalidate all configs: {e}")


class MediaCache:
    """Cache manager for static media files."""

    @staticmethod
    def get_media_hash() -> str:
        """Get hash for media files to enable cache busting.

        Returns:
            Hash string for current media files
        """
        cache_key = "vditor_media_hash"
        media_hash = cache.get(cache_key)

        if media_hash is None:
            # Generate new hash based on settings and current time
            import time

            hash_data = f"{settings.STATIC_URL}:{settings.MEDIA_URL}:{time.time()}"
            media_hash = hashlib.md5(hash_data.encode()).hexdigest()[:8]
            cache.set(cache_key, media_hash, DEFAULT_STATIC_CACHE_TIMEOUT)

        return media_hash

    @staticmethod
    def invalidate_media() -> None:
        """Invalidate media cache (for when static files change)."""
        cache.delete("vditor_media_hash")
        logger.debug("Invalidated media cache")


def warm_cache() -> None:
    """Warm up commonly used caches."""
    try:
        from .configs import VditorConfig

        # Warm up default configuration
        default_config = VditorConfig("default")
        ConfigCache.set_config("default", dict(default_config))

        logger.info("Cache warming completed successfully")
    except Exception as e:
        logger.error(f"Cache warming failed: {e}")


def clear_all_caches() -> None:
    """Clear all Vditor-related caches."""
    try:
        ConfigCache.invalidate_all()
        MediaCache.invalidate_media()
        logger.info("All Vditor caches cleared")
    except Exception as e:
        logger.error(f"Failed to clear caches: {e}")

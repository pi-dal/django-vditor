"""
Django management command for Vditor cache operations.
"""

from django.core.management.base import BaseCommand, CommandError

from vditor.cache_utils import clear_all_caches, warm_cache


class Command(BaseCommand):
    help = "Manage Vditor caches"

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=["clear", "warm", "info"],
            help="Action to perform on caches",
        )

    def handle(self, *args, **options):
        action = options["action"]

        if action == "clear":
            self.stdout.write("Clearing all Vditor caches...")
            try:
                clear_all_caches()
                self.stdout.write(
                    self.style.SUCCESS("Successfully cleared all Vditor caches")
                )
            except Exception as e:
                raise CommandError(f"Failed to clear caches: {e}")

        elif action == "warm":
            self.stdout.write("Warming up Vditor caches...")
            try:
                warm_cache()
                self.stdout.write(
                    self.style.SUCCESS("Successfully warmed up Vditor caches")
                )
            except Exception as e:
                raise CommandError(f"Failed to warm caches: {e}")

        elif action == "info":
            self.stdout.write("Vditor Cache Information:")
            self.stdout.write("========================")

            try:
                from django.core.cache import cache
                from vditor.cache_utils import ConfigCache, MediaCache

                # Try to get some cache stats
                self.stdout.write(f"Cache backend: {cache.__class__.__name__}")

                # Check if default config is cached
                default_config = ConfigCache.get_config("default")
                if default_config:
                    self.stdout.write("✓ Default configuration is cached")
                else:
                    self.stdout.write("✗ Default configuration not in cache")

                # Check media hash
                media_hash = MediaCache.get_media_hash()
                self.stdout.write(f"Media hash: {media_hash}")

            except Exception as e:
                self.stdout.write(f"Error getting cache info: {e}")

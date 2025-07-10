"""
Django management command for Vditor cache operations and performance monitoring.
"""

from django.core.management.base import BaseCommand, CommandError

from vditor.cache_utils import clear_all_caches, warm_cache


class Command(BaseCommand):
    help = "Manage Vditor caches and view performance metrics"

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=["clear", "warm", "info", "metrics"],
            help="Action to perform on caches or view metrics",
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

        elif action == "metrics":
            self.stdout.write("Vditor Performance Metrics:")
            self.stdout.write("==========================")

            try:
                from vditor.views import get_upload_metrics
                
                metrics = get_upload_metrics()
                
                if not metrics:
                    self.stdout.write("No upload metrics available yet.")
                    return
                
                for metric_type, data in metrics.items():
                    self.stdout.write(f"\n{metric_type.upper()} Uploads:")
                    self.stdout.write(f"  Count: {data['count']}")
                    if data['count'] > 0:
                        self.stdout.write(f"  Average Time: {data['avg_time']:.3f}s")
                        self.stdout.write(
                            f"  Total Size: {data['total_size'] / (1024*1024):.2f}MB"
                        )
                        self.stdout.write(
                            f"  Average Size: {data['avg_size'] / 1024:.2f}KB"
                        )
                    else:
                        self.stdout.write("  No uploads recorded")
                
                # Calculate overall stats
                total_uploads = sum(data['count'] for data in metrics.values())
                if total_uploads > 0:
                    self.stdout.write(f"\nOverall Statistics:")
                    self.stdout.write(f"  Total Uploads: {total_uploads}")
                    
                    total_time = sum(data['total_time'] for data in metrics.values())
                    avg_time = total_time / total_uploads
                    self.stdout.write(f"  Average Processing Time: {avg_time:.3f}s")
                    
                    total_size = sum(data['total_size'] for data in metrics.values())
                    avg_size = total_size / total_uploads
                    self.stdout.write(f"  Average File Size: {avg_size / 1024:.2f}KB")
                    
            except Exception as e:
                self.stdout.write(f"Error getting metrics: {e}")

from django.core.management.base import BaseCommand
from search_service.indexing import init_indices


class Command(BaseCommand):
    help = "Initialize OpenSearch indices with mappings"

    def handle(self, *args, **options):
        try:
            self.stdout.write("Initializing OpenSearch indices...")
            init_indices()
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully initialized OpenSearch indices"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to initialize OpenSearch indices: {str(e)}"
                )
            )

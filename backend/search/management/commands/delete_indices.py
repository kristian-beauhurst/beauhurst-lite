from django.core.management.base import BaseCommand
from search_service.client import get_opensearch_client


class Command(BaseCommand):
    help = "Delete all OpenSearch indices"

    def handle(self, *args, **options):
        """Handle the command."""
        client = get_opensearch_client()

        if client.indices.exists(index="companies"):
            client.indices.delete(index="companies")
            self.stdout.write(
                self.style.SUCCESS("Successfully deleted companies index")
            )

        if client.indices.exists(index="employees"):
            client.indices.delete(index="employees")
            self.stdout.write(
                self.style.SUCCESS("Successfully deleted employees index")
            )

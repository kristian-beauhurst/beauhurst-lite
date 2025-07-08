import os
from opensearchpy import OpenSearch


def get_opensearch_client():
    return OpenSearch(
        hosts=[os.environ.get("OPENSEARCH_HOST", "http://localhost:9200")],
        http_auth=(
            os.environ.get("OPENSEARCH_USER", "admin"),
            os.environ.get("OPENSEARCH_PASS", "admin"),
        ),
        timeout=30,
        use_ssl=False,
        verify_certs=False,
    )

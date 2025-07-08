from .client import get_opensearch_client

COMPANY_INDEX = "companies"
EMPLOYEE_INDEX = "employees"

COMPANY_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "companies_house_id": {"type": "keyword"},
            "name": {"type": "text", "analyzer": "standard"},
            "description": {"type": "text", "analyzer": "standard"},
            "date_founded": {"type": "date"},
            "country": {
                "properties": {
                    "id": {"type": "integer"},
                    "iso_code": {"type": "keyword"},
                    "name": {"type": "keyword"},
                }
            },
            "active": {"type": "boolean"},
            "employee_count": {"type": "integer"},
            "total_deals_amount": {"type": "float"},
            "last_deal_amount": {"type": "float"},
            "last_deal_date": {"type": "date"},
            "created": {"type": "date"},
            "modified": {"type": "date"},
        }
    }
}

EMPLOYEE_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "text", "analyzer": "standard"},
            "job_title": {"type": "text", "analyzer": "standard"},
            "gender": {"type": "keyword"},
            "email": {"type": "keyword"},
            "phone_number": {"type": "keyword"},
            "company": {
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "text", "analyzer": "standard"},
                }
            },
            "created": {"type": "date"},
            "modified": {"type": "date"},
        }
    }
}


def init_indices():
    client = get_opensearch_client()

    if not client.indices.exists(index=COMPANY_INDEX):
        client.indices.create(index=COMPANY_INDEX, body=COMPANY_MAPPING)

    if not client.indices.exists(index=EMPLOYEE_INDEX):
        client.indices.create(index=EMPLOYEE_INDEX, body=EMPLOYEE_MAPPING)


def index_company(company_data):
    client = get_opensearch_client()
    client.index(
        index=COMPANY_INDEX,
        id=company_data["id"],
        body=company_data,
        refresh=True,
    )


def index_employee(employee_data):
    client = get_opensearch_client()
    client.index(
        index=EMPLOYEE_INDEX,
        id=employee_data["id"],
        body=employee_data,
        refresh=True,
    )


def delete_company(company_id):
    client = get_opensearch_client()
    client.delete(index=COMPANY_INDEX, id=company_id, refresh=True)


def delete_employee(employee_id):
    client = get_opensearch_client()
    client.delete(index=EMPLOYEE_INDEX, id=employee_id, refresh=True)

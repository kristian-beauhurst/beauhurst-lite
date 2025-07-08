from .client import get_opensearch_client
import logging

logger = logging.getLogger(__name__)


def build_search_body(
    index_type: str,
    query: str,
    size: int = 10,
    date_from: str = None,
    date_to: str = None,
    deal_amount_min: float = None,
    deal_amount_max: float = None,
    country_codes: list[str] = None,
    employee_count_min: int = None,
    employee_count_max: int = None,
    sort_by: str = None,
    sort_order: str = None,
) -> dict:
    """
    Build the search body for opensearch query

    args:
        index_type: type of index to search ('companies' or 'employees')
        query: search query string
        size: number of results to return
        date_from: filter companies founded on or after this date
        date_to: filter companies founded on or before this date
        deal_amount_min: min deal amount to filter by
        deal_amount_max: max deal amount to filter by
        country_codes: list of country ISO codes to filter by
        employee_count_min: min number of employees
        employee_count_max: max number of employees
        sort_by: field to sort by
        sort_order: sort order ('asc' or 'desc')

    returns:
        dict containing the search query body
    """
    search_body = {
        "size": size,
        "query": {
            "bool": {
                "must": [],
                "filter": [],
                "should": [],
                "minimum_should_match": 0,
            }
        },
    }

    if query:
        if index_type == "companies":
            search_body["query"]["bool"]["must"].append(
                {
                    "prefix": {
                        "name": {
                            "value": query.lower(),
                            "case_insensitive": True,
                        }
                    }
                }
            )
        else:  # employees
            search_body["query"]["bool"]["must"].append(
                {
                    "bool": {
                        "should": [
                            {
                                "prefix": {
                                    "name": {
                                        "value": query,
                                        "boost": 4,
                                    }
                                }
                            },
                            {
                                "match": {
                                    "name": {
                                        "query": query,
                                        "boost": 3,
                                        "fuzziness": "AUTO",
                                    }
                                }
                            },
                            {
                                "match": {
                                    "job_title": {
                                        "query": query,
                                        "boost": 2,
                                        "fuzziness": "AUTO",
                                    }
                                }
                            },
                            {
                                "match": {
                                    "email": {
                                        "query": query,
                                        "boost": 1,
                                        "fuzziness": "AUTO",
                                    }
                                }
                            },
                        ],
                        "minimum_should_match": 1,
                    }
                }
            )
    else:
        # if no query, match all docs
        search_body["query"]["bool"]["must"].append({"match_all": {}})

    if index_type == "companies":
        # date range filter
        if date_from or date_to:
            date_range = {"range": {"date_founded": {}}}
            if date_from:
                date_range["range"]["date_founded"]["gte"] = date_from
            if date_to:
                date_range["range"]["date_founded"]["lte"] = date_to
            search_body["query"]["bool"]["filter"].append(date_range)

        # total deals amount range filter
        if deal_amount_min is not None and deal_amount_min != "":
            deal_range = {"range": {"total_deals_amount": {}}}
            deal_range["range"]["total_deals_amount"]["gte"] = deal_amount_min
            if deal_amount_max is not None and deal_amount_max != "":
                deal_range["range"]["total_deals_amount"][
                    "lte"
                ] = deal_amount_max
            search_body["query"]["bool"]["filter"].append(deal_range)
        elif deal_amount_max is not None and deal_amount_max != "":
            deal_range = {"range": {"total_deals_amount": {}}}
            deal_range["range"]["total_deals_amount"]["lte"] = deal_amount_max
            search_body["query"]["bool"]["filter"].append(deal_range)

        if country_codes:
            search_body["query"]["bool"]["filter"].append(
                {"terms": {"country.iso_code": country_codes}}
            )

        # employee count range filter
        if employee_count_min is not None and employee_count_min != "":
            employee_range = {"range": {"employee_count": {}}}
            employee_range["range"]["employee_count"][
                "gte"
            ] = employee_count_min
            if employee_count_max is not None and employee_count_max != "":
                employee_range["range"]["employee_count"][
                    "lte"
                ] = employee_count_max
            search_body["query"]["bool"]["filter"].append(employee_range)
        elif employee_count_max is not None and employee_count_max != "":
            employee_range = {"range": {"employee_count": {}}}
            employee_range["range"]["employee_count"][
                "lte"
            ] = employee_count_max
            search_body["query"]["bool"]["filter"].append(employee_range)

        # boost active companies
        search_body["query"]["bool"]["should"].append(
            {"term": {"active": {"value": True, "boost": 1.5}}}
        )

    if sort_by:
        search_body["sort"] = [
            {sort_by: {"order": sort_order if sort_order else "asc"}}
        ]

    return search_body


def search_companies_and_employees(
    query: str,
    search_type: str = "all",
    size: int = 10,
    date_from: str = None,
    date_to: str = None,
    deal_amount_min: float = None,
    deal_amount_max: float = None,
    country_codes: list[str] = None,
    employee_count_min: int = None,
    employee_count_max: int = None,
    sort_by: str = None,
    sort_order: str = None,
) -> dict:
    client = get_opensearch_client()
    search_types = set(search_type.split(","))
    msearch_body = []

    if not search_types or "all" in search_types:
        search_types = {"companies", "employees"}

    if "companies" in search_types:
        company_body = build_search_body(
            "companies",
            query,
            size,
            date_from,
            date_to,
            deal_amount_min,
            deal_amount_max,
            country_codes,
            employee_count_min,
            employee_count_max,
            sort_by,
            sort_order,
        )
        msearch_body.extend([{"index": "companies"}, company_body])

    if "employees" in search_types:
        employee_body = build_search_body(
            "employees",
            query,
            size,
            date_from,
            date_to,
            deal_amount_min,
            deal_amount_max,
            country_codes,
            employee_count_min,
            employee_count_max,
            sort_by,
            sort_order,
        )
        msearch_body.extend([{"index": "employees"}, employee_body])

    if not msearch_body:
        return {
            "companies": [],
            "employees": [],
            "total": {"companies": 0, "employees": 0},
        }

    response = client.msearch(body=msearch_body)

    results = {
        "companies": [],
        "employees": [],
        "total": {"companies": 0, "employees": 0},
    }
    response_index = 0

    if "companies" in search_types:
        company_response = response["responses"][response_index]
        if "hits" in company_response:
            results["companies"] = [
                hit["_source"] for hit in company_response["hits"]["hits"]
            ]
            results["total"]["companies"] = company_response["hits"]["total"][
                "value"
            ]
            if "aggregations" in company_response:
                results["aggregations"] = company_response["aggregations"]
        response_index += 1

    if "employees" in search_types:
        employee_response = response["responses"][response_index]
        if "hits" in employee_response:
            results["employees"] = [
                hit["_source"] for hit in employee_response["hits"]["hits"]
            ]
            results["total"]["employees"] = employee_response["hits"]["total"][
                "value"
            ]

    return results

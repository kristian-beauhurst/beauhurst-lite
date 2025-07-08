from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from search_service.queries import search_companies_and_employees
import logging

logger = logging.getLogger(__name__)

RESULT_TYPE_TO_TITLE = {
    "companies": "Companies",
    "employees": "Employees",
}

FILTER_CONFIG = {
    "type": {
        "type": "checkbox",
        "label": "Search Type",
        "options": [
            {"value": "all", "label": "All"},
            {"value": "companies", "label": "Companies"},
            {"value": "employees", "label": "Employees"},
        ],
        "default": ["all"],
    },
    "date_range": {
        "type": "date_range",
        "label": "Founded Date Range",
        "fields": [
            {
                "name": "date_from",
                "label": "From",
                "type": "date",
                "placeholder": "YYYY-MM-DD",
            },
            {
                "name": "date_to",
                "label": "To",
                "type": "date",
                "placeholder": "YYYY-MM-DD",
            },
        ],
    },
    "deal_amount": {
        "type": "number_range",
        "label": "Deal Amount",
        "fields": [
            {
                "name": "deal_amount_min",
                "label": "Minimum",
                "type": "number",
                "placeholder": "Enter minimum amount",
            },
            {
                "name": "deal_amount_max",
                "label": "Maximum",
                "type": "number",
                "placeholder": "Enter maximum amount",
            },
        ],
    },
    "employee_count": {
        "type": "number_range",
        "label": "Employee Count",
        "fields": [
            {
                "name": "employee_count_min",
                "label": "Minimum",
                "type": "number",
                "placeholder": "Enter minimum count",
            },
            {
                "name": "employee_count_max",
                "label": "Maximum",
                "type": "number",
                "placeholder": "Enter maximum count",
            },
        ],
    },
    "country": {
        "type": "multi_select",
        "label": "Countries",
        "options": [
            {"value": "GB", "label": "United Kingdom"},
            {"value": "US", "label": "United States"},
            {"value": "FR", "label": "France"},
            {"value": "DE", "label": "Germany"},
            {"value": "ES", "label": "Spain"},
            {"value": "IT", "label": "Italy"},
            {"value": "NL", "label": "Netherlands"},
            {"value": "SE", "label": "Sweden"},
            {"value": "CH", "label": "Switzerland"},
            {"value": "IE", "label": "Ireland"},
        ],
    },
    "sort": {
        "type": "select",
        "label": "Sort By",
        "options": [
            {"value": "name", "label": "Name"},
            {"value": "date_founded", "label": "Founded Date"},
            {"value": "employee_count", "label": "Employee Count"},
            {"value": "total_deals_amount", "label": "Total Deal Amount"},
            {"value": "last_deal_date", "label": "Last Deal Date"},
        ],
        "order": {
            "type": "select",
            "label": "Sort Order",
            "options": [
                {"value": "asc", "label": "Ascending"},
                {"value": "desc", "label": "Descending"},
            ],
            "default": "desc",
        },
    },
}


def render_search_results(results):
    """
    Render search results into a normalized format with sections.

    Args:
        results: Raw search results from search_companies_and_employees

    Returns:
        dict: Normalized results with sections
    """
    sections = []

    for result_type, title in RESULT_TYPE_TO_TITLE.items():
        type_results = results.get(result_type, [])
        if type_results:
            normalized_results = []
            for result in type_results:
                normalized_result = {
                    "title": result.get("name", ""),
                    "subtitle": result.get("description", ""),
                    "id": result.get("id"),
                    "url": f"/{result_type}/{result.get('id')}",
                }
                normalized_results.append(normalized_result)

            sections.append(
                {
                    "title": title,
                    "count": len(normalized_results),
                    "results": normalized_results,
                }
            )

    return {"sections": sections}


class SearchView(APIView):
    """
    API endpoint for searching companies and employees.
    """

    def get(self, request):
        """
        Search api endpoint.

        Query params:
            q: Search query string
            type: Type of search ('all', 'companies', 'employees') -
                can be multiple
            size: Number of results to return (default: 10)
            date_from: Filter companies founded on or after this date
                (YYYY-MM-DD)
            date_to: Filter companies founded on or before this date
                (YYYY-MM-DD)
            deal_amount_min: Minimum deal amount to filter by
            deal_amount_max: Maximum deal amount to filter by
            country: Country ISO code to filter by (can be multiple)
            employee_count_min: Minimum number of employees
            employee_count_max: Maximum number of employees
            sort_by: Field to sort by
            sort_order: Sort order ('asc' or 'desc')
        """

        query = request.query_params.get("q", "")
        search_types = request.query_params.getlist("type", ["all"])
        size = int(request.query_params.get("size", 10))

        allowed_types = {"all", "companies", "employees"}
        if not all(t in allowed_types for t in search_types):
            return Response(
                {
                    "error": (
                        "Invalid search type. Must be one of: "
                        "all, companies, employees"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "all" in search_types:
            search_type = "all"
        else:
            search_type = ",".join(search_types)

        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        deal_amount_min = request.query_params.get("deal_amount_min")
        deal_amount_max = request.query_params.get("deal_amount_max")
        if deal_amount_min:
            deal_amount_min = float(deal_amount_min)
        if deal_amount_max:
            deal_amount_max = float(deal_amount_max)

        country_codes = request.query_params.getlist("country")

        employee_count_min = request.query_params.get("employee_count_min")
        employee_count_max = request.query_params.get("employee_count_max")
        if employee_count_min:
            employee_count_min = int(employee_count_min)
        if employee_count_max:
            employee_count_max = int(employee_count_max)

        sort_by = request.query_params.get("sort_by")
        sort_order = request.query_params.get("sort_order")
        if sort_order and sort_order not in ["asc", "desc"]:
            return Response(
                {"error": "Invalid sort order. Must be 'asc' or 'desc'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            results = search_companies_and_employees(
                query=query,
                search_type=search_type,
                size=size,
                date_from=date_from,
                date_to=date_to,
                deal_amount_min=deal_amount_min,
                deal_amount_max=deal_amount_max,
                country_codes=country_codes,
                employee_count_min=employee_count_min,
                employee_count_max=employee_count_max,
                sort_by=sort_by,
                sort_order=sort_order,
            )
            rendered_results = render_search_results(results)
            return Response(rendered_results)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RawSearchView(APIView):
    """
    API endpoint for searching companies and employees, returning raw results.
    """

    def get(self, request):
        """
        Raw search api endpoint. Only difference from SearchView is that it
        returns the raw, unrendered results from the search.

        Query Params:
            q: Search query string
            type: Type of search ('all', 'companies', 'employees') -
                can be multiple
            size: Number of results to return (default: 10)
            date_from: Filter companies founded on or after this date
                (YYYY-MM-DD)
            date_to: Filter companies founded on or before this date
                (YYYY-MM-DD)
            deal_amount_min: Minimum deal amount to filter by
            deal_amount_max: Maximum deal amount to filter by
            country: Country ISO code to filter by (can be multiple)
            employee_count_min: Minimum number of employees
            employee_count_max: Maximum number of employees
            sort_by: Field to sort by
            sort_order: Sort order ('asc' or 'desc')
        """
        query = request.query_params.get("q", "")
        search_types = request.query_params.getlist("type", ["all"])
        size = int(request.query_params.get("size", 10))

        allowed_types = {"all", "companies", "employees"}
        if not all(t in allowed_types for t in search_types):
            return Response(
                {
                    "error": (
                        "Invalid search type. Must be one of: "
                        "all, companies, employees"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "all" in search_types:
            search_type = "all"
        else:
            search_type = ",".join(search_types)

        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        deal_amount_min = request.query_params.get("deal_amount_min")
        deal_amount_max = request.query_params.get("deal_amount_max")
        if deal_amount_min:
            deal_amount_min = float(deal_amount_min)
        if deal_amount_max:
            deal_amount_max = float(deal_amount_max)

        country_codes = request.query_params.getlist("country")

        employee_count_min = request.query_params.get("employee_count_min")
        employee_count_max = request.query_params.get("employee_count_max")
        if employee_count_min:
            employee_count_min = int(employee_count_min)
        if employee_count_max:
            employee_count_max = int(employee_count_max)

        sort_by = request.query_params.get("sort_by")
        sort_order = request.query_params.get("sort_order")
        if sort_order and sort_order not in ["asc", "desc"]:
            return Response(
                {"error": "Invalid sort order. Must be 'asc' or 'desc'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            results = search_companies_and_employees(
                query=query,
                search_type=search_type,
                size=size,
                date_from=date_from,
                date_to=date_to,
                deal_amount_min=deal_amount_min,
                deal_amount_max=deal_amount_max,
                country_codes=country_codes,
                employee_count_min=employee_count_min,
                employee_count_max=employee_count_max,
                sort_by=sort_by,
                sort_order=sort_order,
            )
            return Response(results)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FilterConfigView(APIView):
    """
    API endpoint for retrieving search filter configurations.
    """

    def get(self, request):
        return Response(FILTER_CONFIG)

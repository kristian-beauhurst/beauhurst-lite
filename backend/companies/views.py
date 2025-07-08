from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Company, Employee, Deal
from .serializers import CompanySerializer, EmployeeSerializer, DealSerializer


def most_recently_founded_companies(limit=10):
    companies = []
    for comp in Company.objects.all():
        serialized = {
            "companies_house_id": comp.companies_house_id,
            "name": comp.name,
            "description": comp.description,
            "date_founded": comp.date_founded,
            "country__iso_code": comp.country.iso_code,
            "creator__username": comp.creator.username,
        }
        companies.append(serialized)

    if limit:
        companies = companies[:limit]
    return sorted(companies, key=lambda comp: comp["date_founded"])


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(detail=True, methods=["get"])
    def employees(self, request, pk=None):
        company = self.get_object()
        employees = Employee.objects.filter(company=company)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def deals(self, request, pk=None):
        company = self.get_object()
        deals = Deal.objects.filter(company=company)
        serializer = DealSerializer(deals, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.query_params.get("company_id")
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset

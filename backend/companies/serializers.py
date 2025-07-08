from rest_framework import serializers

from .models import Company, Employee, Deal, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "iso_code", "name"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "name", "job_title", "gender", "email", "phone_number"]


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ["id", "date_of_deal", "amount_raised"]


class CompanySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source="country", write_only=True
    )
    employees = EmployeeSerializer(many=True, read_only=True)
    deals = DealSerializer(many=True, read_only=True)
    creator_username = serializers.CharField(
        source="creator.username", read_only=True
    )

    class Meta:
        model = Company
        fields = [
            "id",
            "companies_house_id",
            "name",
            "description",
            "date_founded",
            "country",
            "country_id",
            "active",
            "created",
            "modified",
            "creator_username",
            "employees",
            "deals",
        ]
        read_only_fields = ["id", "created", "modified"]

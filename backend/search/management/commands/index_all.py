from django.core.management.base import BaseCommand
from companies.models import Company, Employee
from search_service.indexing import index_company, index_employee
from tqdm import tqdm


class Command(BaseCommand):
    help = "Index all companies and employees in OpenSearch"

    def add_arguments(self, parser):
        parser.add_argument(
            "--companies-only",
            action="store_true",
            help="Index only companies",
        )
        parser.add_argument(
            "--employees-only",
            action="store_true",
            help="Index only employees",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=100,
            help="Number of records to process in each batch (default: 100)",
        )

    def handle(self, *args, **options):
        """Handle the command."""
        companies_only = options.get("companies_only", False)
        employees_only = options.get("employees_only", False)
        batch_size = options.get("batch_size", 100)

        if not companies_only and not employees_only:
            companies_only = True
            employees_only = True

        if companies_only:
            self.stdout.write("Indexing companies...")
            total_companies = Company.objects.count()
            companies = Company.objects.iterator(chunk_size=batch_size)
            for company in tqdm(
                companies, total=total_companies, desc="Companies"
            ):
                deals = company.deal_set.all().order_by("-date_of_deal")
                total_deals_amount = sum(deal.amount_raised for deal in deals)
                last_deal = deals.first()

                company_data = {
                    "id": company.id,
                    "companies_house_id": company.companies_house_id,
                    "name": company.name,
                    "description": company.description,
                    "date_founded": company.date_founded,
                    "country": {
                        "id": company.country.id,
                        "iso_code": company.country.iso_code,
                        "name": company.country.name,
                    },
                    "active": company.active,
                    "employee_count": company.employee_set.count(),
                    "total_deals_amount": total_deals_amount,
                    "last_deal_amount": (
                        last_deal.amount_raised if last_deal else None
                    ),
                    "last_deal_date": (
                        last_deal.date_of_deal if last_deal else None
                    ),
                    "created": company.created,
                    "modified": company.modified,
                }
                index_company(company_data)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully indexed {total_companies} companies"
                )
            )

        if employees_only:
            self.stdout.write("Indexing employees...")
            total_employees = Employee.objects.count()
            employees = Employee.objects.iterator(chunk_size=batch_size)
            for employee in tqdm(
                employees, total=total_employees, desc="Employees"
            ):
                employee_data = {
                    "id": employee.id,
                    "name": employee.name,
                    "job_title": employee.job_title,
                    "email": employee.email,
                    "company": {
                        "id": employee.company.id,
                        "name": employee.company.name,
                    },
                }
                index_employee(employee_data)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully indexed {total_employees} employees"
                )
            )

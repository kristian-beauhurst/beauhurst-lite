from django.core.management.base import BaseCommand
import random
from faker import Faker
from companies.models import Company, Employee, Country
import logging

logger = logging.getLogger(__name__)

fake = Faker()

COMPANY_TYPES = [
    "Tech",
    "Finance",
    "Healthcare",
    "Retail",
    "Manufacturing",
    "Education",
    "Energy",
    "Transportation",
    "Media",
    "Construction",
]

JOB_TITLES = [
    "Software Engineer",
    "Data Scientist",
    "Product Manager",
    "UX Designer",
    "DevOps Engineer",
    "Business Analyst",
    "Marketing Manager",
    "Sales Representative",
    "HR Manager",
    "Financial Analyst",
    "Operations Manager",
    "Project Manager",
    "Customer Success Manager",
    "Content Writer",
    "Research Scientist",
]

COUNTRIES = [
    {"id": 1, "iso_code": "GB", "name": "United Kingdom"},
    {"id": 2, "iso_code": "US", "name": "United States"},
    {"id": 3, "iso_code": "DE", "name": "Germany"},
    {"id": 4, "iso_code": "FR", "name": "France"},
    {"id": 5, "iso_code": "ES", "name": "Spain"},
    {"id": 6, "iso_code": "IT", "name": "Italy"},
    {"id": 7, "iso_code": "NL", "name": "Netherlands"},
    {"id": 8, "iso_code": "SE", "name": "Sweden"},
    {"id": 9, "iso_code": "CH", "name": "Switzerland"},
    {"id": 10, "iso_code": "IE", "name": "Ireland"},
]


def get_or_create_countries():
    countries = []
    for country_data in COUNTRIES:
        country, created = Country.objects.get_or_create(
            iso_code=country_data["iso_code"],
            defaults={"name": country_data["name"]},
        )
        countries.append(country)
    return countries


def generate_company(countries):
    company_type = random.choice(COMPANY_TYPES)
    name = f"{fake.company()} {company_type}"
    date_founded = fake.date_between(start_date="-20y", end_date="now")
    country = random.choice(countries)

    return Company(
        name=name,
        description=fake.text(max_nb_chars=200),
        date_founded=date_founded,
        country=country,
        active=random.choice([True, False]),
        companies_house_id=fake.uuid4(),
    )


def generate_employee(company):
    return Employee(
        company=company,
        name=fake.name(),
        job_title=random.choice(JOB_TITLES),
        gender=random.choice(["M", "F", "O"]),
        email=fake.email(),
        phone_number=fake.phone_number(),
    )


class Command(BaseCommand):
    help = "Generates test data for companies and employees"

    def add_arguments(self, parser):
        parser.add_argument(
            "--companies",
            type=int,
            default=1000,
            help="Number of companies to generate",
        )
        parser.add_argument(
            "--employees-per-company",
            type=int,
            default=10,
            help="Average number of employees per company",
        )

    def handle(self, *args, **options):
        num_companies = options["companies"]
        avg_employees = options["employees_per_company"]

        self.stdout.write("Setting up countries...")
        countries = get_or_create_countries()

        self.stdout.write(f"Generating {num_companies} companies...")
        companies = []
        for i in range(num_companies):
            company = generate_company(countries)
            companies.append(company)

            if (i + 1) % 100 == 0:
                self.stdout.write(f"Generated {i + 1} companies...")

        self.stdout.write("Saving companies to database...")
        Company.objects.bulk_create(companies)

        total_employees = 0
        self.stdout.write("Generating employees...")

        for company in companies:
            num_employees = int(random.gauss(avg_employees, avg_employees / 2))
            num_employees = max(1, min(num_employees, 1000))

            employees = []
            for _ in range(num_employees):
                employee = generate_employee(company)
                employees.append(employee)
                total_employees += 1

            Employee.objects.bulk_create(employees)

            if total_employees % 1000 == 0:
                self.stdout.write(f"Generated {total_employees} employees...")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully generated {num_companies} companies and "
                f"{total_employees} employees"
            )
        )

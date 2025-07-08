import datetime
import random

from django.core.management.base import BaseCommand

from ...factories import (
    CompanyFactory,
    CountryFactory,
    DealFactory,
    EmployeeFactory,
    UserFactory,
)


class Command(BaseCommand):
    help = "Populate your database with some dummy (but realistic) data"

    def handle(self, *args, **options):
        users = UserFactory.create_batch(10)
        countries = CountryFactory.create_batch(5)

        companies = []
        for _ in range(20):
            company = CompanyFactory(country=random.choice(countries))
            companies.append(company)
            n = random.randint(0, 5)
            if n:
                EmployeeFactory.create_batch(n, company=company)

        for year in range(2010, datetime.date.today().year):
            for month in range(1, 13):
                for _ in range(random.randint(0, 5)):
                    deal_date = datetime.date(year, month, random.randint(1, 28))
                    DealFactory(company=random.choice(companies), date_of_deal=deal_date)

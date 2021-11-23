"""
Management Command: python manage.py generate_data
generiere Testdaten für Company und Employee
"""
import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from company.models import Company, Employee
from company.factories import CompanyFactory, EmployeeFactory

NUM_COMPANIES = 10
NUM_EMPLOYEES = 200


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        print("Deleting model data...")
        for model in [Company, Employee]:
            model.objects.all().delete()

        print("data successfully deleted ...")
        print("Creating Companies...")

        companies = []
        for _ in range(NUM_COMPANIES):
            company = CompanyFactory()
            company.slug = slugify(company.name)
            if company.company_type in ["food"]:
                company.has_restaurants = random.choice([True, False])
            company.save()
            companies.append(company)

        print("Creating Employees...")
        for _ in range(NUM_EMPLOYEES):
            company = random.choice(companies)
            employee = EmployeeFactory(company=company)
            employee.save()

        print("{} companies and {} employees created!".format(
            NUM_COMPANIES,
            NUM_EMPLOYEES)
        )

""" 
zwei Klassen, um Fake-Daten zu erzeugen (Company und Employee-Fakedaten)
"""
import arrow
import factory
from . import models


class CompanyFactory(factory.django.DjangoModelFactory):
    """erzeuge ein Fake-Objekt einer Company. Dazu wird der Faker genutzt 
    """

    class Meta:
        model = models.Company

    name = factory.Faker('company')
    description = factory.Faker('paragraph')
    slogan = factory.Faker('catch_phrase')
    company_type = factory.Iterator(['tech', 'food'])


class EmployeeFactory(factory.django.DjangoModelFactory):
    """erzeuge ein Fake-Objekt eines Employee.
    """
    class Meta:
        model = models.Employee

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    company = factory.SubFactory(CompanyFactory)

    date_of_entry = factory.Faker(
        'date_between_dates',
        date_start=arrow.now().shift(days=-900).datetime,
        date_end=arrow.now().datetime
    )

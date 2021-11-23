from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .validators import date_in_future_validator, digits_only_validator, illegal_symbol_validator

# eine neue App muss immer in den settings.py registriert werden
# python manage.py sqlmigrate company 0001 => SQL der Migration für die gewählte DB
# Konvention vor Konfiguration
# from company.models import Company
""" 
Aktionen des Model-Managers:
============================

GEnau ein Objekt selektieren
-------------------------------------
get() liefert genau EIN Objekt! (ansonsten fehler!)
second = Company.objects.get(pk=2)  


Slicing von Querysets 
-------------------------------------
(um Anzahl zu beschneiden)
qs = Company.objects.all()[:2] => die ersten zwei Objekte via all().


Objekte sortieren mit order_by
-------------------------------------
qs = Company.objects.order_by('-number_of_employees') # absteigend nach Employees
qs = Company.objects.order_by('name) # aufsteigend nach Name


Anzahl der Objekte eines Modells:
-------------------------------------
anzahl = Company.objects.count()  # SQL: SELECT COUNT(*) besser als
anzahl = len(Company.objects.all()) # weil count auf der DB operiert

Company.objects.values() => liefert QS mit Dictionaries


Objekte Filter
================
Querysets, die zb. durch Company.objects.all() entstehen, lassen sich filtern.

Filtere alle Objekte, die ein kleines e im Namen beinhalten:
--------------------------------------------------------------
e_comp = Company.objects.all().filter(name__contains="e")

Filtere alle Objekte, die mehr als 5 Employees haben:
--------------------------------------------------------------
e_comp = Company.objects.all().filter(number_of_employees__gt=5)


"""


class DateMixin(models.Model):
    """Datemixin überall dort nutzen, wo created_at und updated_at benötigt wird
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """astract bedeutet: lege DateMixin nicht als Tabelle (DB) sondern nutze sie nur
        als Vorlage"""
        abstract = True


# class DescriptionMixin(models.Model):
#     """DescriptionMixin fügt eine Beschreibungsfeld hinzu
#     (soll das Mixin-Prinzip verdeutlichen)
#     in echt so besser nicht nutzen. NUR BEISPIEL, wird nicht eingesetzt.
#     """
#     description = models.TextField("Beschreibung der Firma")

#     class Meta:
#         """astract bedeutet: lege DateMixin nicht als Tabelle (DB)
#         sondern nutze sie nur
#         als Vorlage"""
#         abstract = True


class Company(DateMixin):
    """Beschreibt eine Firma
    """

    COMPANY_TYPES = (
        ("tech", "Tech Business"),
        ("food", "Food Industry"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Companies"

    name = models.CharField(max_length=100, unique=True,
                            validators=[MinLengthValidator(3),
                                        digits_only_validator])
    description = models.TextField("Beschreibung der Firma", validators=[illegal_symbol_validator])
    slug = models.SlugField(blank=True)  # 127.0.0.1:8000/company/slogan-gmbh

    # null = Feld darf in DB leer sein. blank = im HTML-Formular darf
    # dieses Feld leer sein.
    slogan = models.CharField(max_length=100, null=True, blank=True)
    # number_of_employees = models.IntegerField() obsolet

    has_restaurants = models.BooleanField(default=False)

    # tech oder food wird in DB eintragen
    company_type = models.CharField(
        max_length=8,
        choices=COMPANY_TYPES
    )

    def num_of_employees(self):
        # Gut: Daten aus der DB zählen
        return self.employees.count()

    def __len__(self):
        # Schlecht: alle Daten aus der DB holen und mit Python zählen
        return len(self.employees.all())

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        """ Mit der clean-Methode lassen sich feldübergreifende Valisierungen umsetzen.
        So kann zwischen mehreren Feldern einer Modell-Instanz validiert werden, z.B.
        company_type und has_restaurants
        """
        if self.has_restaurants and self.company_type not in ["food"]:
            raise ValidationError("Firma ist nicht im Food-Sektor")

        if self.slogan == self.name:
            raise ValidationError("Slogan und Name dürfen nicht identisch sein")

    def save(self, *args, **kwargs):
        """wenn bisher kein Slug existiert, erstelle einen"""
        if not self.slug:
            self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)


class Employee(DateMixin):
    first_name = models.CharField(max_length=50, validators=[illegal_symbol_validator]) # darf kein @-Symbol beinhalten
    last_name = models.CharField(max_length=50)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name='employees')

    date_of_entry = models.DateField(null=True, blank=True, validators=[
                                    date_in_future_validator])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

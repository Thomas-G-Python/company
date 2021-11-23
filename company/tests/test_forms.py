from django.test import TestCase, Client
from company.models import Company
from company.models import Employee
from django.utils.text import slugify
from django.shortcuts import reverse
from datetime import date
#from company import views
#from event_manager.company.views import company_add


class CompanyFormTest(TestCase):
    """ Wir erstellen via Formular Absenden ein Testobjekt in der DB,
    und prüfen dieses dann.

    Unit-Test Schritte:
    1) Test-Objekt/Test-Daten anlegen
    2) Aktion durchführen, zb. Formular absenden

    Beispiele für Assert-Statements:
    self.assertTrue(True) => ich behaupte, True ist wahr
    self.assertEqual("a", "a") => ich behaupte, "a" ist gleich "a"
    self.assertNotEqual("a", "b") => ich behaupte, "a" ist ungleich "b"

    """

    def setUp(self):
        """wird VOR jeder Testfunktion(!) aufgerufen. hier kann der Client
        und die Payload zum Beispiel angelegt werden."""
        self.client = Client()  # der User, der das Formular abschickt
        self.payload = {
            "name": "Mc Donalds GmbH",
            "description": "bla bla bla",
            "company_type": "food",
            "has_restaurants": True,
            "slogan": "das ist der slogan"
        }


    def test_company_has_proper_slug(self):
        """prüfe, ob nach Absenden des Formulars das Objekt 
        mit dem richtigen Slug angelegt wurde (klein, keine Leerzeichen)
        """
        # Formular absenden:        
        self.client.post(reverse("company:company_add"), self.payload)
        # Instanziierung auch der Test-Datenbank-Klasse 
        company = Company.objects.get(name=self.payload.get("name"))
        # Vergleich zwischen dem aus der Test-Datenbank instanziierten (geladenen) slug und dem hier fest eingetippten
        self.assertEqual(company.slug, "mc-donalds-gmbh")
        # Vergleich zwischen dem wieder aus der Test-Datenbank inst,/gel. slug und dem aus dem payload-Objekt geladenen Namen,
        # welcher über die Funktion slugify zum Test-Datenbank-Slug wird
        self.assertEqual(company.slug, slugify(self.payload.get("name")))
        # Wenn einer dieser assertEquals Falso ergibt, folgt eine Fehlermeldung, d.h.... 
        # beide assertEquals sind sozusagen über ein UND nicht nicht über ein ODER verknüpft


    def test_company_type_is_food_and_has_restaurant(self):
        """Prüfen, ob eine Firma vom Typ food UND zugleich has_restaurant True 
        ist"""
        self.client.post(reverse("company:company_add"), self.payload)
        company_exist = Company.objects.filter(
            name=self.payload.get("name")).exists()

            # exists gibt True zurück, wenn Company.objects.filter(..) mind. einen Wert enthält

        # Objekt muss eingetragen sein, weil food und Restaurant erlaubt ist
        self.assertTrue(company_exist)


    def test_company_type_is_tech_and_has_restaurant(self):
            """Prüfen, ob eine Firma vom Typ tech UND zugleich has_restaurant True 
            ist"""
            self.payload["company_type"] = "tech"
            self.client.post(reverse("company:company_add"), self.payload)
            company_exist = Company.objects.filter(
                name=self.payload.get("name")).exists()

            # Objekt darf nicht eingetragen sein,
            # weil company_type=tech und Restaurant NICHT erlaubt sind
            self.assertFalse(company_exist)


    def test_not_get_company_with_only_digits_in_db(self):
        """Prüfen. ob ein Firmen-Name, der nur aus Zahlen besteht, 
        in die DB eingetragen wird"""
        self.payload["name"] = "1111"
        self.client.post(reverse("company:company_add"), self.payload)
        company_exist = Company.objects.filter(
            name=self.payload.get("name")).exists()

        self.assertFalse(company_exist)


#    def test_name_to_short(self):
#        self.payload["name"] = "a"
#        self.cliet.post(reverse("company:company_add"), self.payload)
#        company_exist = Company

    # Test, ob Firma mit selben Namen 2mal existiert
    def test_create_companies_with_same_name(self):
        # Testtabelle ist - noch - leer
            #  1. Anfrage
        self.client.post(reverse("company:company_add"), self.payload)
            # 2. Anfrage
        self.client.post(reverse("company:company_add"), self.payload)
            # Company.objects.all() bezieht sich nur auf diese Testdatenbank
        companies = Company.objects.filter(name=self.payload.get("name"))
        self.assertEqual(len(companies), 1)
            # oder alternativ:
        self.assertLessEqual(len(companies), 2)


    # Test Driven Design: Zuerst Test Schreiben und erst dann Code implementieren
    def test_description_with_add_symbol(self):
        self.payload["description"] = "test@test"
        self.client.post(reverse("company:company_add"), self.payload)
        company_exist = Company.objects.filter(
            name=self.payload.get("name")).exists()
        self.assertFalse(company_exist)


class EmployeeFormTest(TestCase):
    def setUp(self):
        self.client = Client()  # der User, das Formular abschickt
        company_payload = {
            "name": "Mc Donalds GmbH",
            "description": "bla bla bla",
            "company_type": "food",
            "has_restaurants": True,
            "slogan": "das ist der slogan"
        }
        company = Company.objects.create(**company_payload)
        # Shortcut für
        # company = Company(**company)
        # company.save()

        self.payload = {
            "first_name": "Tom",
            "last_name": "Jerry",
            "date_of_entry": date.today(),
            "company_id": 7,
            "company": company
        }


    def test_eintrittsdatum_nicht_in_der_Zukunft(self):
#        print("Datum: ", self.payload.name)

#        self.payload["date_of_entry"] = date(2020, 10, 10) #!!
        self.client.post(reverse("company:employee_add", args=[7]), self.payload) #!! wo füge ich wie die company_id ein ???
        entry_date = Company.objects.get(date_of_entry=self.payload.get("date_of_entry"))

        self.assertGreater(self.payload.get("date_of_entry"), entry_date)
#        self.assertTrue(abs(date_of_entry - self.payload.get("date_of_entry")))


"""

    def test_company_has_proper_slug(self):
        #prüfe, ob nach Absenden des Formulars das Objekt 
        #mit dem richtigen Slug angelegt wurde (klein, keine Leerzeichen)
        
        # Formular absenden:        
        self.client.post(reverse("company:company_add"), self.payload)
        # Instanziierung auch der Test-Datenbank-Klasse 
        company = Company.objects.get(name=self.payload.get("name"))
        # Vergleich zwischen dem aus der Test-Datenbank instanziierten (geladenen) slug und dem hier fest eingetippten
        self.assertEqual(company.slug, "mc-donalds-gmbh")
        # Vergleich zwischen dem wieder aus der Test-Datenbank inst,/gel. slug und dem aus dem payload-Objekt geladenen Namen,
        # welcher über die Funktion slugify zum Test-Datenbank-Slug wird
        self.assertEqual(company.slug, slugify(self.payload.get("name")))
        # Wenn einer dieser assertEquals Falso ergibt, folgt eine Fehlermeldung, d.h.... 
        # beide assertEquals sind sozusagen über ein UND nicht nicht über ein ODER verknüpft




        # Test Driven Design: Zuerst Test Schreiben und erst dann Code implementieren
    def test_description_with_add_symbol(self):
        self.payload["description"] = "test@test"
        self.client.post(reverse("company:company_add"), self.payload)
        company_exist = Company.objects.filter(
            name=self.payload.get("name")).exists()
        self.assertFalse(company_exist)
"""


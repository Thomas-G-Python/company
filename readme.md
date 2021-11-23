# Django Tutorial

## 1) neues Projekt erstellen
> django-admin startproject company_manager

## neue App "company" anlegen

> python manage.py startapp company

### App in den settings.py registrieren

> MY_APPS = [
>     'first_app',
>    'company',
> ]

> INSTALLED_APPS += MY_APPS

## Model erstellen
Neue Models werden in der Datei models.py einer App angelegt.

### Migration
Damit die Models in der Datenbank verfügbar sind, müssen sie migriert werden.
Dazu erstmal die Migrationsdatei erstellen:
> python manage.py makemigrations

und dann die Migration durchführen
> python manage.py migrate

Um zu Prüfen, wie das SQL aussieht, welches eine Migrationsdatei erstellt, kann dieser Befehl a
ausgeführt werden:
> python manage.py sqlmigrate appname 0001


## Die Django Administrationsoberfläche
Django bietet eine Administrationsoberfläche. Um einen Admin-User zu erstellen, der sich einloggen kann, führt man folgendes Kommando aus:

> python manage.py createsuperuser

Ausfüllen des Dialogs:

> Benutzername: admin
> E-Mail-Adresse:
> Password:
> Password (again):
> Superuser created successfully.

### Entwicklungsserver starten
> python manage.py runserver

### in die Administrationsoberfläche einloggen
> http://127.0.0.1/admin

### Modell Company registrieren
In der Datei admin.py wird das Modell registriert und für die Administrationsoberfläche
verfügbar gemacht:

> admin.site.register(Company)


# Models filtern und selektieren:

## Selektieren mit einem Manager

Genau ein Objekt selektieren
-------------------------------------
get() liefert IMMER genau EIN Objekt! (ansonsten fehler!)
> second = Company.objects.get(pk=2)  


Slicing von Querysets 
-------------------------------------
(um Anzahl zu beschneiden)
> qs = Company.objects.all()[:2] => die ersten zwei Objekte via all().


Objekte sortieren mit order_by
-------------------------------------
> qs = Company.objects.order_by('-number_of_employees') # absteigend nach Employees
> qs = Company.objects.order_by('name) # aufsteigend nach Name


Anzahl der Objekte eines Modells:
-------------------------------------
> anzahl = Company.objects.count()  # SQL: SELECT COUNT(*) besser als
> anzahl = len(Company.objects.all()) # weil count auf der DB operiert

Queryset als Dictionary
-------------------------------------
> obj = Company.objects.values() 


## Filtern eines Querysets
Querysets, die zb. durch Company.objects.all() entstehen, lassen sich filtern.

Filtere alle Objekte, die ein kleines e im Namen beinhalten:
--------------------------------------------------------------
> e_comp = Company.objects.all().filter(name__contains="e")


Filtere alle Objekte, die mehr als 5 Employees haben:
--------------------------------------------------------------
> e_comp = Company.objects.all().filter(number_of_employees__gt=5)

Mehr zu Django Field-Lookups hier:
https://docs.djangoproject.com/en/3.1/ref/models/querysets/#field-lookups

## Foreign Key Relation (1:n)

    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name='employees')

### Löschen von Foreign Keys
> on_delete.SET_NULL => setzt Foreign Key auf Null (dazu muss null=True)
> on_delete.CASCADE => löscht Kindobjekte
> on_delete.PROTECT => Relation kann nur gelöscht werden, wenn keine Referenzen darauf

### Related Name
sprechender Name, wenn auf Kindobjekte zugegriffen wird:
> comp = Company.objects.get(pk=4)
> comp.employees

### Related Manager
> comp.employees ist ein Related Manager. Über ihn lässt sich zum Beispiel filtern
> c.employees.filter(first_name__contains="a")


### Filter Beispiele:

Filtere alle Mitarbeiter der Firma mit id=4, die ein kleines u im Nachnamen haben:
----------------------------------------------------------------------------------
> r = Company.objects.get(pk=4).employees.filter(last_name__contains="u")


Filtere alle Firmen, die Angstellte mit einem kleinen "o" im Vornamen haben:
-----------------------------------------------------------------------------
> result = Company.objects.filter(employees__first_name__contains='o').distinct()


Filtere alle Employees, die in Firmen arbeiten, die den Buchstaben "a" enthalten:
---------------------------------------------------------------------------------
> Employee.objects.filter(company__name__icontains="a")



## Template Tags and Filter
https://docs.djangoproject.com/en/3.2/ref/templates/builtins/#built-in-filter-reference

Beispiele für Filter:
> {{comp.description|truncatewords:2}}<br>
> Branche: {{comp.company_type}}<br>
> Branche: {{comp.get_company_type_display}}<br>
> Angestellte: {{comp.num_of_employees|add:"2"}}<br>
> Länge des Firmennamens: {{comp.name|length}}


## Testdatendanlegen 
pip install factory_boy

Folgende Command erstellen: python manage.py generate_data


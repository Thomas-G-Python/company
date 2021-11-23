from django.contrib import admin
from . models import Company, Employee

# einfachste Möglichkeit (out of the box)
# admin.site.register(Company)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # Felder auf der Detailseite
    # fields = ('name', 'company_type', 'slogan', 'description')

    # Attribute auf der Übersichtsseite
    list_display = ('id', 'name', 'company_type', 'num_of_employees', 'has_restaurants')

    # anklickbare Felder (um auf Detailseite zu kommen)
    list_display_links = ('id', 'name')

    # Suchfeld
    search_fields = ('name', 'slogan')

    prepopulated_fields = {"slug": ('name',)}


# Company Admin registrieren
# besser @admin.register-Decorator nutzen: @admin.register(Company)
# admin.site.register(Company, CompanyAdmin)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'last_name', 'company'
    list_display_links = 'id', 'first_name', 'last_name'
    search_fields = 'first_name', 'last_name'
    # autocomplete_fields = ['company']?

# eine kleine Aenderung


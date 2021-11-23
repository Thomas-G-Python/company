from django.urls import path
from . import views

app_name = "company"

urlpatterns = [
    # http://127.0.0.1:8000
    path('', views.list_companies, name="list_companies"),

    # http://127.0.0.1:8000/company/3
    path('company/<int:id>', views.single_company, name="single_company"),

    # http://127.0.0.1:8000/company/add (GET=> Formular anzeigen,
    # POST=>Daten eintragen in DB)
    path('company/add', views.company_add, name="company_add"),

    # http://127.0.0.1:8000/company/hallo-welt-gmbh
    path('company/<slug:slug>',
         views.single_company_by_slug,
         name="single_company_by_slug"),

    # http://127.0.0.1:8000/company/3/update (GET=> Formular anzeigen,
    # POST=>Daten eintragen in DB)
    path('company/<int:id>/update', views.company_update, name="company_update"),

    # Mitarbeiter für Firma hinzufügen
    # http://127.0.0.1:8000/company/3/employee/add
    path('company/<int:company_id>/employee/add',
         views.employee_add,
         name="employee_add"
         ),

    # v http://127.0.0.1/company/sensor-bleach-gbmh/employee/33/update
    path('company/<slug:slug>/employee/<int:id>/update',
         views.employee_update,
         name='employee_update'
         ),

    # http://127.0.0.1:8000/company/hallo-welt-gmbh/employee/2
    path('company/<slug:slug>/employee/<int:pk>',
         views.EmployeeDetail.as_view(),
         name="employee_detail"),


    # http://127.0.0.1:8000/company/hallo-welt-gmbh/employees
    #     path("company/<slug:slug>/employees",
    #          views.EmployeeList.as_view(),
    #          name="employees"
    #          ),

    # http://127.0.0.1:8000/company/hallo-welt-gmbh/delete
    path("company/<slug:slug>/delete",
         views.CompanyDelete.as_view(),
         name="company_delete"
         ),

    # http://127.0.0.1:8000/company/hallo-welt-gmbh/employee/3/delete
    path("company/<slug:slug>/employee/<int:pk>/delete",
         views.EmployeeDelete.as_view(),
         name="employee_delete"
         ),
]

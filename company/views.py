from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.http import HttpResponse, Http404
from . models import Company, Employee
from . forms import CompanyForm, EmployeeForm
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView,
                                       DeleteView,
                                       UpdateView)
from django.views.generic.list import ListView


def list_companies_ohne_template(request):
    """Beispiel für eine View ohne template"""

    companies = Company.objects.all()

    c = []
    for company in companies:
        c.append(company.name)
    return HttpResponse("<br>".join(c))


def list_companies(request):
    """
    http://127.0.0.1:8000
    """

    companies = Company.objects.prefetch_related("employees").all()

    return render(request, 'company/companies.html', {
        'companies': companies
    })


def single_company(request, id):
    """
    http://127.0.0.1:8000/company/3
    """
    try:
        company = Company.objects.get(pk=id)
    except Company.DoesNotExist:
        raise Http404("Diese Firma existiert nicht!")

    return render(request, 'company/single.html', {
        'comp': company,
        'title': "Super Titel hier",
    })


def single_company_by_slug(request, slug):
    """
    Firma über ihren "Slug" aufrufen. slug = Kurzwort
    http://127.0.0.1:8000/company/slogan-gmbh
    """
    company = get_object_or_404(Company, slug=slug)
    # company = get_object_or_404(Company.objects.prefetch_related(), slug=slug)

    return render(request, 'company/single.html', {
        'comp': company,
        'title': "Super Titel hier",
    })


def company_update(request, id):
    """
    http://127.0.0.1:8000/company/3/update
    """
    c = get_object_or_404(Company, pk=id)
    form = CompanyForm(request.POST or None, instance=c)

    if form.is_valid():
        form.save()
        messages.success(request, 'Das hat geklappt.')
        return redirect('company:single_company', id=id)

    return render(request, "company/update.html", {
        "form": form
    })


def company_add(request):
    """ 
    http://127.0.0.1:8000/company/add
    """
    if request.method == "POST":
        form = CompanyForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Das hat geklappt.')
            return redirect('company:list_companies')
        messages.error(request, 'Das hat leider nicht geklappt.')
    else:
        form = CompanyForm()

    return render(request, "company/add.html", {
        "form": form
    })


def employee_update(request, slug, id):
    """
    http://127.0.0.1/company/sensor-bleach-gbmh/employee/33/update
    """
    employee = get_object_or_404(Employee, pk=id)
    # instance=employee => lade Daten aus der DB beim ersten Aufruf des Forms
    form = EmployeeForm(request.POST or None, instance=employee)

    if form.is_valid():
        form.save()
        return redirect('company:employee_detail', slug=slug, pk=id)

    return render(request, 'company/employee_update.html', {'form': form})


def employee_add(request, company_id):
    """ 
    Mitarbeiter für eine bestimmte Firma hinzufügen
    http://127.0.0.1:8000/company/3/employee/add
    """

    # zuerst prüfen, ob Company Eintrag überhaupt existiert
    company = get_object_or_404(Company, pk=company_id)

    if request.method == "POST":
        form = EmployeeForm(request.POST or None)
        if form.is_valid():

            # wir wollen company nicht im Formular haben, da wir Mitarbeiter einer
            # bestimmten Firma eintragen wollen.
            # save() gibt Instanz eines neues Employee-Objekts
            employee = form.save(commit=False)
            employee.company = company
            employee.save()
            return redirect('company:single_company', id=company_id)
    else:
        form = EmployeeForm()

    return render(request, "company/employee_add.html", {
        "company": company,
        "form": form
    })


class EmployeeDetail(DetailView):
    model = Employee
    template_name = "company/employee_detail.html"


class CompanyDelete(DeleteView):
    # default Templates: company_confirm_delete
    model = Company

    def get_success_url(self) -> str:
        return reverse("company:list_companies")


class EmployeeDelete(DeleteView):
    model = Employee

    def get_success_url(self) -> str:
        company = self.object.company
        return reverse("company:single_company_by_slug",
                       kwargs={'slug': company.slug}
                       )


"""
class EmployeeList(ListView):

    http: // 127.0.0.1: 8000/company/edwards-robinson/employees
    Beispiel für eine Generic-Class-Based-View

    model = Employee
    context_object_name = "employees"  # name of iterable in template
    template_name = "company/employee_list.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = Employee.objects.filter(
            company__slug=self.kwargs["slug"]).order_by('-first_name')
        return queryset
"""

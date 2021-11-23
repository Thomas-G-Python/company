from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from . models import Company, Employee


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ('company',)

        labels = {
            "first_name": "Vorname",
            "last_name": "Nachname",
            "date_of_entry": "in der Firma seit"
        }

        widgets = {
            "date_of_entry": forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': 'date'
            })
        }


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'

        labels = {
            "company_type": "Kategorie",
            "description": "Beschreibung"
        }
        exclude = ('slug',)

    def clean_slogan(self):
        """Input Feld 'slogan' auf Form-Ebene validieren 
        (Validierung auf Modell-Ebene findet im Modell statt)
        """
        slogan = self.cleaned_data['slogan']
        if isinstance(slogan, str) and '@' in slogan:
            raise ValidationError("Das @-Zeichen ist nicht erlaubt")

        return slogan

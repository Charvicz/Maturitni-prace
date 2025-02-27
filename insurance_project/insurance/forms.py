from django import forms
from .models import InsuredPerson, SubInsurance, Insurance, InsuredPerson 
from django.forms.widgets import SelectDateWidget, NumberInput
import datetime

CZ_MONTHS = {
    1: 'leden', 
    2: 'únor', 
    3: 'březen', 
    4: 'duben', 
    5: 'květen', 
    6: 'červen', 
    7: 'červenec', 
    8: 'srpen', 
    9: 'září', 
    10: 'říjen', 
    11: 'listopad', 
    12: 'prosinec'
}

class InsuredPersonForm(forms.ModelForm):
    class Meta:
        model = InsuredPerson
        fields = ['first_name', 'last_name', 'birth_date', 'phone']
        widgets = {
            'birth_date': SelectDateWidget(
                years=range(1900, datetime.date.today().year + 1),
                months=CZ_MONTHS
            )
        }


        
class InsuredForm(forms.ModelForm):
    class Meta:
        model = InsuredPerson
        fields = ['first_name', 'last_name', 'birth_date', 'phone']  # Pole, které může uživatel upravit
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),  # Použij typ "date" pro datum
        }


class SubInsuranceForm(forms.ModelForm):
    class Meta:
        model = SubInsurance
        fields = ['name', 'price']
        
        
class InsuranceForm(forms.ModelForm):
    # Pole pro podpojistění – bude renderováno jako sady zaškrtávacích políček
    sub_insurances = forms.MultipleChoiceField(
        choices=[],  # Volby se naplní pomocí JS dle zvoleného typu
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Vyberte podpojistění"
    )

    class Meta:
        model = Insurance
        fields = ['insurance_type', 'duration_years', 'sub_insurances']
        widgets = {
            # Pokud např. 'duration_years' je pole s roky, můžeme použít vlastní widget:
            'duration_years': forms.Select(choices=[(i, i) for i in range(datetime.date.today().year, 1899, -1)]),
        }



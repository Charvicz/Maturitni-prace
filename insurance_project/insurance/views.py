from django.shortcuts import render, redirect, get_object_or_404
from .forms import InsuredPersonForm, SubInsuranceForm, InsuredForm, InsuranceForm
from .models import InsuredPerson, SubInsurance, Insurance
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

def index(request):
    return render(request, "insurance/index.html")

def add_insured(request):
    if request.method == 'POST':
        form = InsuredPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = InsuredPersonForm()
    
    return render(request, 'insurance/add_insured.html', {'form': form})

# Zobrazí seznam pojištěných
def insured_list(request):
    persons = InsuredPerson.objects.all()
    return render(request, 'insurance/insured_list.html', {'persons': persons})

# Funkce pro přidání pojištění
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import InsuranceForm
from .models import InsuredPerson, Insurance, SubInsurance

def add_insurance(request, insured_person_id):
    insured_person = get_object_or_404(InsuredPerson, id=insured_person_id)
    
    if request.method == 'POST':
        form = InsuranceForm(request.POST)
        if form.is_valid():
            # Uložení pojištění a přiřazení pojištěnému
            insurance = form.save(commit=False)
            insurance.insured_person = insured_person
            insurance.save()    
            
            # Automatické vytvoření podpojištění podle typu pojištění
            sub_insurances = []
            if insurance.insurance_type == 'life':
                sub_insurances = [
                    ('Úrazové pojištění', 200),
                    ('Invalidita', 300),
                    ('Nemocnice', 150),
                ]
            elif insurance.insurance_type == 'travel':
                sub_insurances = [
                    ('Ztráta zavazadel', 100),
                    ('Úrazové pojištění', 150),
                    ('Pojištění storna', 200),
                ]
            elif insurance.insurance_type == 'property':
                sub_insurances = [
                    ('Pojištění domácnosti', 250),
                    ('Pojištění odpovědnosti', 180),
                    ('Pojištění proti požáru', 350),
                ]
            
            # Pokud existují podpojištění, přidáme je
            for name, price in sub_insurances:
                SubInsurance.objects.create(insurance=insurance, name=name, price=price)
                
            # Přesměrování na předchozí stránku, pokud je k dispozici, nebo na detail pojištěného
            previous_page = request.META.get('HTTP_REFERER', 'insured_detail')
            return HttpResponseRedirect(previous_page)
            
    else:
        form = InsuranceForm()
    
    return render(request, 'insurance/add_insurance.html', {'form': form, 'insured_person': insured_person})


def add_insured_with_subinsurance(request):
    if request.method == 'POST':
        person_form = InsuredPersonForm(request.POST)
        insurance_type = request.POST.get('insurance_type')  # např. 'life', 'travel', 'property'
        # Získáme seznam vybraných podpojistění (jména, např. "Úrazové pojištění", atd.)
        selected_subs = request.POST.getlist('sub_insurances')
        
        if person_form.is_valid():
            # Uložíme pojištěnce
            person = person_form.save()
            # Vytvoříme záznam pojištění bez ceny/doby (nechceme nastavovat cenu)
            insurance = Insurance.objects.create(
                insured_person=person,
                insurance_type=insurance_type,
                duration_years=0  # nebo jiná výchozí hodnota, pokud nepotřebuješ ukládat cenu/dobu
            )
            
            # Možné podpojistění pro každý typ:
            sub_insurance_options = {
                'life': [
                    ('Úrazové pojištění', 200),
                    ('Invalidita', 300),
                    ('Nemocnice', 150),
                ],
                'travel': [
                    ('Ztráta zavazadel', 100),
                    ('Úrazové pojištění', 150),
                    ('Pojištění storna', 200),
                ],
                'property': [
                    ('Pojištění domácnosti', 250),
                    ('Pojištění odpovědnosti', 180),
                    ('Pojištění proti požáru', 350),
                ]
            }
            
            # Vytvoříme pouze ta podpojistění, která uživatel vybral:
            for name, price in sub_insurance_options.get(insurance_type, []):
                if name in selected_subs:
                    SubInsurance.objects.create(
                        insurance=insurance,
                        name=name,
                        price=price
                    )
            
            return redirect('index')
    else:
        person_form = InsuredPersonForm()
    
    # Renderujeme šablonu, kterou si vytvoříš níže
    return render(request, 'insurance/add_insured_with_subinsurance.html', {
        'person_form': person_form
    })



def search_insured(request):
    query_first = request.GET.get('first_name', '')
    query_last = request.GET.get('last_name', '')
    results = None

    # Pokud uživatel zadal alespoň jedno kritérium, provedeme vyhledávání
    if query_first or query_last:
        results = InsuredPerson.objects.all()
        if query_first:
            results = results.filter(first_name__icontains=query_first)
        if query_last:
            results = results.filter(last_name__icontains=query_last)

        # Pokud je nalezen právě jeden výsledek, přesměrujeme přímo na detail
        if results.count() == 1:
            person = results.first()
            return redirect('insured_detail', person_id=person.id)
    
    return render(request, 'insurance/search_insured.html', {
        'results': results,
        'first_name': query_first,
        'last_name': query_last,
    })

def insured_detail(request, person_id):
    person = get_object_or_404(InsuredPerson, id=person_id)
    return render(request, 'insurance/insured_detail.html', {'person': person})

def delete_insured_with_password(request, person_id):
    person = get_object_or_404(InsuredPerson, id=person_id)
    error = None
    # Nastav si heslo, které musí být zadáno – ideálně si to dej do settings nebo získávej bezpečně
    ADMIN_DELETE_PASSWORD = 'tajneheslo'
    
    if request.method == 'POST':
        entered_password = request.POST.get('password', '')
        if entered_password == ADMIN_DELETE_PASSWORD:
            person.delete()
            # Po smazání přesměrujeme na stránku se seznamem pojištěných
            return redirect('insured_list')
        else:
            error = "Zadané heslo je nesprávné."
    
    return render(request, 'insurance/delete_insured_confirm.html', {
        'person': person,
        'error': error,
    })



def edit_insured(request, person_id):
    person = get_object_or_404(InsuredPerson, id=person_id)
    if request.method == 'POST':
        form = InsuredPersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('insured_detail', person_id=person.id)
    else:
        form = InsuredPersonForm(instance=person)
    
    return render(request, 'insurance/edit_insured.html', {'form': form, 'person': person})


def delete_insurance(request, insurance_id):
    """ Odstraní konkrétní pojištění a přesměruje zpět na předchozí stránku. """
    insurance = get_object_or_404(Insurance, id=insurance_id)
    person_id = insurance.insured_person.id  # Získání ID pojištěného

    # Smazání pojištění
    insurance.delete()

    # Přesměrování zpět na stránku, odkud uživatel přišel
    previous_page = request.META.get('HTTP_REFERER')

    if previous_page:
        return HttpResponseRedirect(previous_page)  # Vrátíme uživatele na stejnou stránku
    else:
        # Pokud není dostupný referer, přesměrujeme na detail pojištěného
        return redirect(reverse('detail_insured', args=[person_id]))

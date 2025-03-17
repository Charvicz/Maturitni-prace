from django.db import models
from datetime import date


# Model pro pojištěnou osobu
class InsuredPerson(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True) # Datum narození místo věku
    phone = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        import datetime
        if not self.birth_date:
            return "Neznámé"  # nebo vrátit např. 0, či prázdný string
        today = datetime.date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age


# Model pro pojištění
class Insurance(models.Model):
    TYPE_CHOICES = [
        ('life', 'Životní pojištění'),
        ('travel', 'Cestovní pojištění'),
        ('property', 'Majetkové pojištění'),
    ]
    
    insured_person = models.ForeignKey(InsuredPerson, on_delete=models.CASCADE)
    insurance_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    duration_years = models.IntegerField()

    def __str__(self):
        return f"{self.get_insurance_type_display()} ({self.duration_years} let)"

# Model pro podpojištění
class SubInsurance(models.Model):
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name


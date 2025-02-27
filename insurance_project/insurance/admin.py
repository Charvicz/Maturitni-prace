from django.contrib import admin
from .models import InsuredPerson, Insurance, SubInsurance

# Register your models here.
admin.site.register(InsuredPerson)
admin.site.register(Insurance)
admin.site.register(SubInsurance)
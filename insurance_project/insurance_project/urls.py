from django.contrib import admin
from django.urls import path, include
from insurance import views  # Importuj pohledy z aplikace insurance

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.index, name='index'),
    path('', include('insurance.urls')),
    path('add_insured/', views.add_insured, name='add_insured'),
    path('insured_list/', views.insured_list, name='insured_list'),
    path('add_insurance/<int:insured_person_id>/', views.add_insurance, name='add_insurance'),
]


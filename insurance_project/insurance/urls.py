from django.urls import path
from . import views
from .views import edit_insured, delete_insurance


urlpatterns = [
    path('', views.index, name='index'),
    path('add_insured/', views.add_insured, name='add_insured'),
    path('insured_list/', views.insured_list, name='insured_list'),
    path('add_insurance/<int:insured_person_id>/', views.add_insurance, name='add_insurance'),
    path('add_insured_with_insurance/', views.add_insured_with_subinsurance, name='add_insured_with_insurance'),
    path('search_insured/', views.search_insured, name='search_insured'),
    path('insured/<int:person_id>/', views.insured_detail, name='insured_detail'),
    path('delete_insured/<int:person_id>/', views.delete_insured, name='delete_insured'), 
    path('edit_insured/<int:person_id>/', edit_insured, name='edit_insured'),
    path('delete_insurance/<int:insurance_id>/', delete_insurance, name='delete_insurance'),
]

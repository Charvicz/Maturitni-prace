from django.urls import path
from . import views
from .views import edit_insured, delete_insurance
from .views import delete_insured_with_password


urlpatterns = [
    path('', views.index, name='index'),
    path('insured_list/', views.insured_list, name='insured_list'),
    path('add_insurance/<int:insured_person_id>/', views.add_insurance, name='add_insurance'),
    path('add_insured_with_insurance/', views.add_insured_with_subinsurance, name='add_insured_with_insurance'),
    path('search_insured/', views.search_insured, name='search_insured'),
    path('insured/<int:person_id>/', views.insured_detail, name='insured_detail'),
    path('edit_insured/<int:person_id>/', edit_insured, name='edit_insured'),
    path('delete_insurance/<int:insurance_id>/', delete_insurance, name='delete_insurance'),
    path('delete_insured_with_password/<int:person_id>/', delete_insured_with_password, name='delete_insured_with_password'),


]

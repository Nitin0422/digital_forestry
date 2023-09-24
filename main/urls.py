from django.urls import path
from . import views

app_name= 'main'

urlpatterns = [
    path('', views.login_request, name='login'),
    path('registration/', views.registration, name='register'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_request, name='logout'),
    path('home/account-information/', views.account_information_view, name="account_information"),
    path('home/account-information-form/', views.account_information_form_view, name="account_form"),
    path('home/account/edit', views.edit_account_information, name="edit_account_information"),
    path('home/land-information/', views.land_information_view, name="land_information"),
    path('home/land-information/add', views.land_information_add, name="land_information_add"),
    path('home/land-information/edit/<int:land_information_id>', views.land_information_edit, name="land_information_edit"),
    path('home/land-information/delete/<int:land_information_id>', views.land_information_delete, name="land_information_delete"),
    path('home/strs/', views.strs_information_view, name="strs")
]
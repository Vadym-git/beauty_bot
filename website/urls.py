from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('services/', views.services_view, name='services'),
    path('services/delete/<int:s_id>/', views.delete_service, name='d_service'),
    path('edit-service/<int:id>', views.edit_service, name='edit_service'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('account/', views.user_account, name='account'),
    path('logout/', views.logout_view, name='logout'),
    path('cities/<str:county>/', views.get_cities, name='cities'),
    path('policy/', views.policy, name='policy'),
    path('add/', views.add_cities, name='add'),

]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('carte/<int:pk>/', views.carte_prisonnier, name='carte_prisonnier'),
    path('alertes/', views.alertes, name='alertes'),
]
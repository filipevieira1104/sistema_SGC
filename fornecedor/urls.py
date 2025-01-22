from django.urls import path
from . import views

urlpatterns = [
    path('fornecedor/', views.fornecedor, name='fornecedor')
]

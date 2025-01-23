from django.urls import path
from . import views

urlpatterns = [
    path('criar_solicitacao/', views.criar_solicitacao, name='criar_solicitacao'),
    path('preencher_budget/', views.preencher_budget, name='preencher_budget'),
]
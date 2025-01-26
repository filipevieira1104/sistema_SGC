from django.urls import path
from . import views

urlpatterns = [
    path('criar_solicitacao/', views.criar_solicitacao, name='criar_solicitacao'),
    path('preencher_budget/', views.preencher_budget, name='preencher_budget'),
    path('minhas_solicitacoes/', views.minhas_solicitacoes, name='minhas_solicitacoes'),
    path('aprovar_orcamento/<int:contrato_id>/', views.aprovar_orcamento, name='aprovar_orcamento'),
]
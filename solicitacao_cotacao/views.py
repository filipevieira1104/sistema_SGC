from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import SolicitacaoCotacao, Budget
from contrato.models import Contrato

@login_required
def criar_solicitacao(request):
    contratos = Contrato.objects.filter(solicitacao__usuario=request.user)
    if request.method == "GET":
        return render(request, 'solicitacao.html', {'contratos': contratos})
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        if not all([titulo, descricao]):
            messages.warning(request, 'Preencha todos os campos')
            return redirect('criar_solicitacao')
        
        SolicitacaoCotacao.objects.create(
            usuario=request.user,
            titulo=titulo,
            descricao=descricao
        )
        messages.success(request, 'Solicitação de orçamento criada com sucesso!')
        return redirect('criar_solicitacao')

@login_required
def preencher_budget(request):
    # Verifica se já existe um orçamento para o usuário
    try:
        budget = Budget.objects.get(usuario=request.user)
    except Budget.DoesNotExist:
        budget = None

    if request.method == 'POST':
        budgeta = request.POST.get('budgeta')
        budgetm = request.POST.get('budgetm')

        # Se não houver nenhum budget salvo, cria um novo
        if not budget:
            budget = Budget(usuario=request.user,
                            budget_anual=budgeta, budget_mensal=budgetm
                            )
        else:
            budget.budget_anual = budgeta
            budget.budget_mensal = budgetm

        budget.save()
        messages.success(request, "Budget salvo com sucesso!")
        return redirect('criar_solicitacao')  # Redireciona de volta para a página de criação de solicitação

    return render(request, 'solicitacao.html', {'budget': budget})  # Passa o budget atual para o template
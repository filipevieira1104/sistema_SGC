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

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Budget

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Budget

@login_required
def preencher_budget(request):
    # Verifica se já existe um orçamento para o usuário
    try:
        budget = Budget.objects.get(usuario=request.user)
    except Budget.DoesNotExist:
        budget = None

    if request.method == 'POST':
        # Obtém os valores dos campos ou mantém os existentes caso estejam vazios
        budgeta = request.POST.get('budgeta', None)
        budgetm = request.POST.get('budgetm', None)

        # Se os valores estiverem vazios, mantém os valores já preenchidos
        if not budgeta:
            budgeta = budget.budget_anual if budget else None
        if not budgetm:
            budgetm = budget.budget_mensal if budget else None

        # Se o usuário clicou em "Alterar Budget", o campo será desbloqueado
        if 'alterar' in request.POST:
            # Permite a edição dos campos
            budgeta = None
            budgetm = None

        # Se não houver nenhum budget salvo, cria um novo
        if not budget:
            budget = Budget(usuario=request.user, budget_anual=budgeta, budget_mensal=budgetm)
        else:
            # Atualiza o orçamento existente
            budget.budget_anual = budgeta
            budget.budget_mensal = budgetm

        try:
            budget.save()
            if 'alterar' in request.POST:
                messages.success(request, "Budget atualizado com sucesso!")
            else:
                messages.success(request, "Budget salvo com sucesso!")
        except ValueError as e:
            messages.error(request, f"Erro ao salvar budget: {e}")

        return redirect('preencher_budget')  # Redireciona para a página de orçamento

    return render(request, 'solicitacao.html', {'budget': budget})
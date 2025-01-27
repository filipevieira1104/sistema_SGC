from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import SolicitacaoCotacao, Budget
from contrato.models import Contrato
from notificacao.models import Notificacao

@login_required
def criar_solicitacao(request):
    if request.method == "GET":
        return render(request, 'solicitacao.html')
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        if not all([titulo, descricao]):
            messages.warning(request, 'Preencha todos os campos')
            return redirect('criar_solicitacao')
        
        solicitacao = SolicitacaoCotacao.objects.create(
            usuario=request.user,
            titulo=titulo,
            descricao=descricao
        )

        # Criando a notificação para os administradores
        admins = User.objects.filter(is_superuser=True)  # Pega os administradores
        for admin in admins:
            Notificacao.objects.create(
                usuario=admin,
                mensagem=f"Novo pedido: Solicitação de orçamento: {solicitacao.titulo}."
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
        # Obtém os valores dos campos de orçamento
        budgeta = request.POST.get('budgeta', None)
        budgetm = request.POST.get('budgetm', None)

        # Se não houver nenhum budget salvo, cria um novo
        if not budget:
            budget = Budget(usuario=request.user, budget_anual=budgeta, budget_mensal=budgetm)
        else:
            # Atualiza o orçamento existente
            budget.budget_anual = budgeta
            budget.budget_mensal = budgetm

        # Salva o orçamento e verifica erros
        try:
            budget.save()
            messages.success(request, "Budget salvo com sucesso!")
        except ValueError as e:
            messages.error(request, f"Erro ao salvar budget: {e}")

        
    return render(request, 'solicitacao.html', {'budget': budget})

@login_required
def minhas_solicitacoes(request):
    # Marcando as notificações como lidas ao acessar a página
    Notificacao.objects.filter(usuario=request.user, lido=False).update(lido=True)
    # Recupera todas as solicitações do usuário
    solicitacoes = SolicitacaoCotacao.objects.filter(usuario=request.user).order_by('id')
    contratos = Contrato.objects.filter(solicitacao__usuario=request.user)

    # Verificando se já existe um orçamento aprovado para cada solicitação
    for solicitacao in solicitacoes:
        solicitacao.orcamento_aprovado = solicitacao.contrato_set.filter(aprovado=True).exists()

    # Paginando as solicitações (1 solicitação por página)
    paginator = Paginator(solicitacoes, 1)  # 1 solicitação por página
    page_number = request.GET.get('page')  # Pegando o número da página da URL
    page_obj = paginator.get_page(page_number)  # Pega a página solicitada

    # Recupera os contratos aprovados
    contratos_aprovados = Contrato.objects.filter(solicitacao__usuario=request.user, aprovado=True)
    
    # Conta o número de orçamentos aprovados
    quantidade_orcamentos_aprovados = contratos_aprovados.count()

    # Recupera o orçamento do usuário
    try:
        budget = Budget.objects.get(usuario=request.user)
    except Budget.DoesNotExist:
        budget = None

    # Passando as solicitações paginadas para o template
    return render(request, 'retorno_solicitacao.html', {'page_obj': page_obj, 'contratos': contratos, 'contratos_aprovados': contratos_aprovados, 'quantidade_orcamentos_aprovados': quantidade_orcamentos_aprovados, 'budget': budget})


@login_required
def aprovar_orcamento(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)
    
    # Garantir que o orçamento só pode ser aprovado se a solicitação ainda não tiver um orçamento aprovado
    if not contrato.solicitacao.contrato_set.filter(aprovado=True).exists():
        # Desabilitar a aprovação para todos os outros orçamentos desta solicitação
        contrato.solicitacao.contrato_set.update(aprovado=False)

        # Agora, aprovar o orçamento escolhido
        contrato.aprovado = True
        contrato.save()
        messages.success(request, "Orçamento aprovado com sucesso!")
    else:
        messages.warning(request, "Já existe um orçamento aprovado para esta solicitação.")
    
    return redirect('minhas_solicitacoes')


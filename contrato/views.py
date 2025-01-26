from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contrato, SolicitacaoCotacao
from notificacao.models import Notificacao

@login_required
def adicionar_orcamento(request, solicitacao_id):
    # Verifica se a solicitação existe e pertence ao usuário
    solicitacao = SolicitacaoCotacao.objects.get(id=solicitacao_id, usuario=request.user)

    if request.method == 'POST':
        fornecedor = request.POST['fornecedor']
        valor_proposta = request.POST['valor_proposta']
        especificacoes_tecnicas = request.POST['especificacoes_tecnicas']
        anexo = request.FILES.get('anexo')

        # Cria o novo contrato (orçamento)
        contrato = Contrato.objects.create(
            solicitacao=solicitacao,
            fornecedor=fornecedor,
            valor_proposta=valor_proposta,
            especificacoes_tecnicas=especificacoes_tecnicas,
            anexo=anexo
        )

        # Cria a notificação para o usuário
        notificacao = Notificacao.objects.create(
            usuario=request.user,
            mensagem=f"Novo orçamento foi adicionado à sua solicitação: {solicitacao.titulo}"
        )

        messages.success(request, "Orçamento adicionado com sucesso!")
        return redirect('minhas_solicitacoes')  # Redireciona para a página de solicitação do usuário

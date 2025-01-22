from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import SolicitacaoCotacao
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
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('criar_solicitacao')
        
        SolicitacaoCotacao.objects.create(
            usuario = request.user,
            titulo=titulo,
            descricao=descricao
        )
        messages.add_message(request, constants.SUCCESS, 'Solicitacao de orçamento criada com sucesso!')
        return redirect('criar_solicitacao')      
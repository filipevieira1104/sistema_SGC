from .models import Notificacao

def notificacoes_na_navbar(request):
    if request.user.is_authenticated:
        # Conta notificações não lidas para usuário autenticado
        new_orcamentos = Notificacao.objects.filter(usuario=request.user, lido=False).count()
    else:
        new_orcamentos = 0
    return {'new_orcamentos': new_orcamentos}        
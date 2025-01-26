from django.contrib import admin
from django.contrib import messages
from notificacao.models import Notificacao
from .models import Contrato

class ContratoAdmin(admin.ModelAdmin):
    list_display = ['id', 'solicitacao', 'fornecedor', 'valor_proposta', 'data_contrato']
    search_fields = ['fornecedor__nome', 'solicitacao__titulo']

    def save_model(self, request, obj, form, change):
        # Salva o contrato normalmente
        super().save_model(request, obj, form, change)

        # Cria uma notificação após salvar o contrato
        if not change:  # Se não for uma edição, mas uma criação de contrato
            notificacao = Notificacao.objects.create(
                usuario=obj.solicitacao.usuario,  # O usuário da solicitação
                mensagem=f"Novo orçamento foi adicionado à sua solicitação: {obj.solicitacao.titulo}",
                lido=False  # Marcar como não lida inicialmente
            )
            messages.success(request, "Orçamento adicionado e notificação criada com sucesso!")

# Registra o modelo no admin
admin.site.register(Contrato, ContratoAdmin)

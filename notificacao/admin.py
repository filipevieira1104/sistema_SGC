from django.contrib import admin
from .models import Notificacao

class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensagem', 'data_criacao', 'lido')
    list_filter = ('lido', 'data_criacao')
    actions = ['marcar_como_lido']

    def marcar_como_lido(self, request, queryset):
        queryset.update(lido=True)
        self.message_user(request, "Notificação(s) marcada(s) como lida(s).")

admin.site.register(Notificacao, NotificacaoAdmin)

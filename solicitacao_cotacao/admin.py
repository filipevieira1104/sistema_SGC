from django.contrib import admin
from .models import SolicitacaoCotacao, Budget

class SolicitacaoCotacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'titulo', 'descricao', 'status']
    list_editable = ['status']

admin.site.register(SolicitacaoCotacao, SolicitacaoCotacaoAdmin)
admin.site.register(Budget)
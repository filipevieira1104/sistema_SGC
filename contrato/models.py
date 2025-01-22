from django.db import models
from fornecedor.models import Fornecedor
from solicitacao_cotacao.models import SolicitacaoCotacao
from decimal import Decimal

class Contrato(models.Model):
    solicitacao = models.ForeignKey(SolicitacaoCotacao, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    data_contrato = models.DateTimeField(auto_now_add=True)
    valor_proposta = models.DecimalField(max_digits=10, decimal_places=2)
    especificacoes_tecnicas = models.TextField()
    anexo = models.FileField(upload_to='contratos')

    def __str__(self):
        return self.solicitacao.titulo
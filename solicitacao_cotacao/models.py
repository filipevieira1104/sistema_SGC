from django.db import models
from django.contrib.auth.models import User

class SolicitacaoCotacao(models.Model):
    SOLICITACAO_STATUS = [
        ('pendente', 'Pendente'),
        ('em negociacao', 'Em negociação'),
        ('cotacao finalizada', 'Cotação Finalizada')
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitacoes')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=SOLICITACAO_STATUS, default='pendente')

    def __str__(self):
        return self.titulo
    
class Budget(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    budget_anual = models.DecimalField(max_digits=10, decimal_places=2)
    budget_mensal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.budget_anual} / {self.budget_mensal}"   
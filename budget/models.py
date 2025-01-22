from django.db import models

class Budget(models.Model):
    budget_anual = models.DecimalField(max_digits=10, decimal_places=2)
    budget_mensal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.budget_anual, self.budget_mensal
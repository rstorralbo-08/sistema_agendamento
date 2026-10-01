from django.db import models


class Servico(models.Model):
    descricao = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    duracao = models.PositiveIntegerField(help_text="Duração estimada em minutos")
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ['descricao']

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"
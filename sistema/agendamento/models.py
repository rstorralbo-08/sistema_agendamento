from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Agendamento(models.Model):
    class StatusAgendamento(models.TextChoices):
        AGENDADO = 'AGENDADO', 'Agendado'
        REALIZADO = 'REALIZADO', 'Realizado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    # Referência por string ('app_label.ModelName') para evitar problemas de dependência circular
    cliente = models.ForeignKey(
        'clientes.Cliente', 
        on_delete=models.PROTECT, 
        related_name='agendamentos'
    )
    servico = models.ForeignKey(
        'servicos.Servico', 
        on_delete=models.PROTECT, 
        related_name='agendamentos'
    )
    data = models.DateField()
    horario = models.TimeField()
    observacao = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=StatusAgendamento.choices,
        default=StatusAgendamento.AGENDADO
    )

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['-data', '-horario']
        # Regra 5: Impede duplicidade de data e horário
        constraints = [
            models.UniqueConstraint(
                fields=['data', 'horario'], 
                name='unique_agendamento_data_horario'
            )
        ]

    def clean(self):
        super().clean()

        # Regra 1: Cliente inativo
        if self.cliente_id and not self.cliente.ativo:
            raise ValidationError({'cliente': 'Não é permitido criar agendamento para um cliente inativo.'})

        # Regra 2: Serviço inativo
        if self.servico_id and not self.servico.ativo:
            raise ValidationError({'servico': 'Não é permitido criar agendamento para um serviço inativo.'})

        # Regra 3: Data anterior à atual
        if self.data and self.data < timezone.now().date():
            raise ValidationError({'data': 'A data do agendamento não pode ser anterior à data de hoje.'})

    def __str__(self):
        return f"{self.cliente.nome} - {self.servico.descricao} ({self.data} às {self.horario})"
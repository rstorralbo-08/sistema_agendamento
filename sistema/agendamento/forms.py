from datetime import datetime, timedelta
from django import forms
from django.utils import timezone
from .models import Agendamento
from clientes.models import Cliente
from servicos.models import Servico


class AgendamentoForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Selecione um cliente"
    )
    servico = forms.ModelChoiceField(
        queryset=Servico.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Selecione um serviço"
    )

    class Meta:
        model = Agendamento
        fields = ['cliente', 'servico', 'data', 'horario', 'status', 'observacao']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'horario': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        horario = cleaned_data.get('horario')
        servico = cleaned_data.get('servico')

        # Regra: Não permitir agendamento para data anterior à atual
        if data and data < timezone.localdate():
            self.add_error('data', 'A data do agendamento não pode ser anterior à data de hoje.')

        # Validação de sobreposição por duração
        if data and horario and servico:
            novo_inicio = datetime.combine(data, horario)
            novo_fim = novo_inicio + timedelta(minutes=servico.duracao)

            # Buscar agendamentos do mesmo dia que não estejam cancelados
            agendamentos_dia = Agendamento.objects.filter(data=data).exclude(status='CANCELADO')

            # Se for edição, exclui o próprio registro da checagem
            if self.instance and self.instance.pk:
                agendamentos_dia = agendamentos_dia.exclude(pk=self.instance.pk)

            for ag in agendamentos_dia:
                ag_inicio = datetime.combine(ag.data, ag.horario)
                ag_fim = ag_inicio + timedelta(minutes=ag.servico.duracao)

                # Verifica sobreposição de horário
                if novo_inicio < ag_fim and novo_fim > ag_inicio:
                    inicio_str = ag_inicio.strftime('%H:%M')
                    fim_str = ag_fim.strftime('%H:%M')
                    
                    self.add_error(
                        'horario',
                        f'Em atendimento ao cliente "{ag.cliente.nome}" que começou às {inicio_str} e acaba às {fim_str}.'
                    )
                    break

        return cleaned_data
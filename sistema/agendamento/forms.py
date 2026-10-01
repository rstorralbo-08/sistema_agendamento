from django import forms
from django.utils import timezone
from .models import Agendamento
from clientes.models import Cliente
from servicos.models import Servico


class AgendamentoForm(forms.ModelForm):
    # Regras 1 e 2 na interface: exibir apenas clientes e serviços ativos no dropdown
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

        # Regra 3: Não permitir agendamento para data anterior à data atual
        if data and data < timezone.now().date():
            self.add_error('data', 'A data do agendamento não pode ser anterior à data de hoje.')

        # Regra 5: Não permitir dois agendamentos para o mesmo horário e data
        if data and horario:
            conflito = Agendamento.objects.filter(data=data, horario=horario)
            if self.instance and self.instance.pk:
                conflito = conflito.exclude(pk=self.instance.pk)
            
            if conflito.exists():
                self.add_error('horario', 'Já existe um agendamento marcado para esta data e horário.')

        return cleaned_data
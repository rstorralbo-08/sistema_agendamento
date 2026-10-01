from django import forms
from .models import Servico


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['descricao', 'valor', 'duracao', 'ativo']
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: Manutenção de computador, Formatação...'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01', 
                'placeholder': '0.00'
            }),
            'duracao': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Duração em minutos (ex: 60)'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'descricao': 'Descrição do Serviço',
            'valor': 'Valor (R$)',
            'duracao': 'Duração (em minutos)',
            'ativo': 'Serviço Ativo',
        }
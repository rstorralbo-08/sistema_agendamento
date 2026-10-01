from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from clientes.models import Cliente
from servicos.models import Servico
from agendamento.models import Agendamento


@login_required
def dashboard(request):
    hoje = timezone.now().date()

    total_clientes = Cliente.objects.count()
    total_servicos = Servico.objects.filter(ativo=True).count()
    agendamentos_hoje = Agendamento.objects.filter(data=hoje).count()
    agendamentos_realizados = Agendamento.objects.filter(status='REALIZADO').count()

    contexto = {
        'total_clientes': total_clientes,
        'total_servicos': total_servicos,
        'agendamentos_hoje': agendamentos_hoje,
        'agendamentos_realizados': agendamentos_realizados,
    }
    return render(request, 'core/dashboard.html', contexto)
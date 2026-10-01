from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Agendamento
from .forms import AgendamentoForm


@login_required
def listar_agendamentos(request):
    # Filtro opcional por status ou data
    status_filtro = request.GET.get('status', '').strip()
    data_filtro = request.GET.get('data', '').strip()

    agendamentos = Agendamento.objects.select_related('cliente', 'servico').all()

    if status_filtro:
        agendamentos = agendamentos.filter(status=status_filtro)
    if data_filtro:
        agendamentos = agendamentos.filter(data=data_filtro)

    contexto = {
        'agendamentos': agendamentos,
        'status_filtro': status_filtro,
        'data_filtro': data_filtro,
        'opcoes_status': Agendamento.StatusAgendamento.choices,
    }
    return render(request, 'agendamento/lista.html', contexto)


@login_required
def novo_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento registado com sucesso!')
            return redirect('agendamento:listar')
    else:
        form = AgendamentoForm()

    return render(request, 'agendamento/formulario.html', {
        'form': form, 
        'titulo': 'Registar Novo Agendamento'
    })


@login_required
def editar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect('agendamento:listar')
    else:
        form = AgendamentoForm(instance=agendamento)

    return render(request, 'agendamento/formulario.html', {
        'form': form, 
        'agendamento': agendamento, 
        'titulo': f'Editar Agendamento #{agendamento.id}'
    })


@login_required
def excluir_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    if request.method == 'POST':
        agendamento.delete()
        messages.success(request, 'Agendamento cancelado/excluído com sucesso!')
        return redirect('agendamento:listar')

    return render(request, 'agendamento/confirmar_exclusao.html', {'agendamento': agendamento})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import ProtectedError

from .models import Servico
from .forms import ServicoForm


@login_required
def listar_servicos(request):
    termo_busca = request.GET.get('busca', '').strip()
    if termo_busca:
        servicos = Servico.objects.filter(descricao__icontains=termo_busca)
    else:
        servicos = Servico.objects.all()

    contexto = {
        'servicos': servicos,
        'termo_busca': termo_busca,
    }
    return render(request, 'servicos/lista.html', contexto)


@login_required
def novo_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço registrado com sucesso!')
            return redirect('servicos:listar')
    else:
        form = ServicoForm()

    return render(request, 'servicos/formulario.html', {
        'form': form, 
        'titulo': 'Registrar Novo Serviço'
    })


@login_required
def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso!')
            return redirect('servicos:listar')
    else:
        form = ServicoForm(instance=servico)

    return render(request, 'servicos/formulario.html', {
        'form': form, 
        'servico': servico, 
        'titulo': f'Editar Serviço: {servico.descricao}'
    })


@login_required
def excluir_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)

    if request.method == 'POST':
        try:
            servico.delete()
            messages.success(request, 'Serviço removido com sucesso!')
        except ProtectedError:
            messages.error(
                request, 
                f'Não é possível remover o serviço "{servico.descricao}" porque existem agendamentos associados a este serviço.'
            )
        return redirect('servicos:listar')

    return render(request, 'servicos/confirmar_exclusao.html', {'servico': servico})


@login_required
def alternar_status_servico(request, pk):
    """Permite ativar ou desativar o serviço com um clique."""
    servico = get_object_or_404(Servico, pk=pk)
    servico.ativo = not servico.ativo
    servico.save()

    estado = "ativado" if servico.ativo else "desativado"
    messages.info(request, f'O serviço "{servico.descricao}" foi {estado} com sucesso!')
    return redirect('servicos:listar')
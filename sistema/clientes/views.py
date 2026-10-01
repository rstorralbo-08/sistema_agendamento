from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import ProtectedError

from .models import Cliente
from .forms import ClienteForm


@login_required
def listar_clientes(request):
    termo_busca = request.GET.get('busca', '').strip()
    if termo_busca:
        # Pesquisa por nome (case-insensitive)
        clientes = Cliente.objects.filter(nome__icontains=termo_busca)
    else:
        clientes = Cliente.objects.all()

    contexto = {
        'clientes': clientes,
        'termo_busca': termo_busca,
    }
    return render(request, 'clientes/lista.html', contexto)


@login_required
def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado com sucesso!')
            return redirect('clientes:listar')
    else:
        form = ClienteForm()

    return render(request, 'clientes/formulario.html', {'form': form, 'titulo': 'Registar Novo Cliente'})


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do cliente atualizados com sucesso!')
            return redirect('clientes:listar')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/formulario.html', {
        'form': form, 
        'cliente': cliente, 
        'titulo': f'Editar Cliente: {cliente.nome}'
    })


@login_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        try:
            cliente.delete()
            messages.success(request, 'Cliente removido com sucesso!')
        except ProtectedError:
            # Regra 4: Impede a exclusão se existirem agendamentos vinculados
            messages.error(
                request, 
                f'Não é possível remover o cliente "{cliente.nome}" porque existem agendamentos vinculados a este registo.'
            )
        return redirect('clientes:listar')

    return render(request, 'clientes/confirmar_exclusao.html', {'cliente': cliente})


@login_required
def alternar_status_cliente(request, pk):
    """Permite ativar ou desativar o cliente com um clique."""
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.ativo = not cliente.ativo
    cliente.save()
    
    estado = "ativado" if cliente.ativo else "desativado"
    messages.info(request, f'Cliente "{cliente.nome}" foi {estado} com sucesso!')
    return redirect('clientes:listar')
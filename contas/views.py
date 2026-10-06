from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Transacao
from .forms import TransacaoForm

@login_required
def painel(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.usuario = request.user
            transacao.save()
            return redirect('painel')
    else:
        form = TransacaoForm()

    transacoes = Transacao.objects.filter(usuario=request.user).order_by('-data')
    
    receitas = Transacao.objects.filter(usuario=request.user, tipo='R').aggregate(Sum('valor'))['valor__sum'] or 0
    despesas = Transacao.objects.filter(usuario=request.user, tipo='D').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = receitas - despesas

    context = {
        'transacoes': transacoes,
        'receitas': receitas,
        'despesas': despesas,
        'saldo': saldo,
        'form': form,
    }
    return render(request, 'contas/painel.html', context)

@login_required
def editar_transacao(request, pk):
    transacao = get_object_or_404(Transacao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = TransacaoForm(request.POST, instance=transacao)
        if form.is_valid():
            form.save()
            return redirect('painel')
    else:
        form = TransacaoForm(instance=transacao)

    return render(request, 'contas/editar_transacao.html', {'form': form, 'transacao': transacao})

@login_required
def deletar_transacao(request, pk):
    transacao = get_object_or_404(Transacao, pk=pk, usuario=request.user)
    transacao.delete()
    return redirect('painel')

def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('painel')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registrar.html', {'form': form})
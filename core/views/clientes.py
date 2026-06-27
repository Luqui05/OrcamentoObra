from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import ClienteForm
from core.models import Cliente


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "core/cliente/list.html"
    context_object_name = "clientes"


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = "core/cliente/detail.html"
    context_object_name = "cliente"


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/form.html"
    success_url = reverse_lazy("cliente_list")

    extra_context = {
        "titulo": "Cadastrar cliente",
        "botao": "Salvar",
    }


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/form.html"
    success_url = reverse_lazy("cliente_list")

    extra_context = {
        "titulo": "Editar cliente",
        "botao": "Atualizar",
    }


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("cliente_list")

    extra_context = {
        "titulo": "Excluir cliente",
        "cancel_url_name": "cliente_list",
    }

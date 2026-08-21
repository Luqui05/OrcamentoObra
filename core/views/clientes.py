from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import ClienteForm
from core.models import Cliente
from core.views.mixins import (
    ClienteGroupRequiredMixin,
    LoginRequiredMixin,
    UserScopedQuerySetMixin,
)


class ClienteListView(
    LoginRequiredMixin, ClienteGroupRequiredMixin, UserScopedQuerySetMixin, ListView
):
    model = Cliente
    template_name = "core/cliente/list.html"
    context_object_name = "clientes"
    user_filter = "usuario"
    paginate_by = 10


class ClienteDetailView(
    LoginRequiredMixin, ClienteGroupRequiredMixin, UserScopedQuerySetMixin, DetailView
):
    model = Cliente
    template_name = "core/cliente/detail.html"
    context_object_name = "cliente"
    user_filter = "usuario"


class ClienteCreateView(LoginRequiredMixin, ClienteGroupRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/form.html"
    success_url = reverse_lazy("cliente_list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    extra_context = {
        "titulo": "Cadastrar cliente",
        "botao": "Salvar",
    }


class ClienteUpdateView(
    LoginRequiredMixin, ClienteGroupRequiredMixin, UserScopedQuerySetMixin, UpdateView
):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/form.html"
    success_url = reverse_lazy("cliente_list")
    user_filter = "usuario"

    extra_context = {
        "titulo": "Editar cliente",
        "botao": "Atualizar",
    }


class ClienteDeleteView(
    LoginRequiredMixin, ClienteGroupRequiredMixin, UserScopedQuerySetMixin, DeleteView
):
    model = Cliente
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("cliente_list")
    user_filter = "usuario"

    extra_context = {
        "titulo": "Excluir cliente",
        "cancel_url_name": "cliente_list",
    }

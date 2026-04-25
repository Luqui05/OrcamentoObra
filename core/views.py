from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ClienteForm, ObraForm
from .models import Cliente, Obra


class HomeTemplateView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_clientes"] = Cliente.objects.count()
        context["total_obras"] = Obra.objects.count()
        return context


class SobreTemplateView(TemplateView):
    template_name = "core/sobre.html"


class ClienteListView(ListView):
    model = Cliente
    template_name = "core/cliente/list.html"
    context_object_name = "clientes"


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "core/cliente/detail.html"
    context_object_name = "cliente"


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/form.html"
    success_url = reverse_lazy("cliente_list")

    extra_context = {
        "titulo": "Cadastrar cliente",
        "botao": "Salvar",
    }


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/form.html"
    success_url = reverse_lazy("cliente_list")

    extra_context = {
        "titulo": "Editar cliente",
        "botao": "Atualizar",
    }


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("cliente_list")

    extra_context = {
        "titulo": "Excluir cliente",
        "cancel_url_name": "cliente_list",
    }


class ObraListView(ListView):
    model = Obra
    template_name = "core/obra/list.html"
    context_object_name = "obras"


class ObraDetailView(DetailView):
    model = Obra
    template_name = "core/obra/detail.html"
    context_object_name = "obra"


class ObraCreateView(CreateView):
    model = Obra
    form_class = ObraForm
    template_name = "core/form.html"
    success_url = reverse_lazy("obra_list")

    extra_context = {
        "titulo": "Cadastrar obra",
        "botao": "Salvar",
        "cancel_url_name": "obra_list",
    }


class ObraUpdateView(UpdateView):
    model = Obra
    form_class = ObraForm
    template_name = "core/form.html"
    success_url = reverse_lazy("obra_list")

    extra_context = {
        "titulo": "Editar obra",
        "botao": "Atualizar",
        "cancel_url_name": "obra_list",
    }


class ObraDeleteView(DeleteView):
    model = Obra
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("obra_list")

    extra_context = {
        "titulo": "Excluir obra",
        "cancel_url_name": "obra_list",
    }

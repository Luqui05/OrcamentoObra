from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import ObraForm
from core.models import Obra
from core.utils import montar_galeria_obra


class ObraListView(LoginRequiredMixin, ListView):
    model = Obra
    template_name = "core/obra/list.html"
    context_object_name = "obras"


class ObraDetailView(LoginRequiredMixin, DetailView):
    model = Obra
    template_name = "core/obra/detail.html"
    context_object_name = "obra"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orcamentos"] = self.object.orcamentos.all()
        context["atualizacoes"] = self.object.atualizacoes.all()
        return context


class ObraGaleriaView(LoginRequiredMixin, DetailView):
    model = Obra
    template_name = "core/obra/galeria.html"
    context_object_name = "obra"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        galeria_items = montar_galeria_obra(self.object)
        context["galeria_items"] = galeria_items
        context["galeria_midias"] = [item for item in galeria_items if item["tipo"] == "imagem"]
        context["galeria_documentos"] = [item for item in galeria_items if item["tipo"] == "documento"]
        context["galeria_orcamentos"] = [item for item in galeria_items if item["tipo"] == "orcamento"]
        return context


class ObraCreateView(LoginRequiredMixin, CreateView):
    model = Obra
    form_class = ObraForm
    template_name = "core/form.html"
    success_url = reverse_lazy("obra_list")

    extra_context = {
        "titulo": "Cadastrar obra",
        "botao": "Salvar",
        "cancel_url_name": "obra_list",
    }


class ObraUpdateView(LoginRequiredMixin, UpdateView):
    model = Obra
    form_class = ObraForm
    template_name = "core/form.html"
    success_url = reverse_lazy("obra_list")

    extra_context = {
        "titulo": "Editar obra",
        "botao": "Atualizar",
        "cancel_url_name": "obra_list",
    }


class ObraDeleteView(LoginRequiredMixin, DeleteView):
    model = Obra
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("obra_list")

    extra_context = {
        "titulo": "Excluir obra",
        "cancel_url_name": "obra_list",
    }

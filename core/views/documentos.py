from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import DocumentoForm
from core.models import Documento
from core.views.mixins import (
    ClienteGroupRequiredMixin,
    LoginRequiredMixin,
    ObraContextMixin,
    ObraRelatedQuerySetMixin,
    AutorQuerySetMixin,
)


class DocumentoListView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    ObraContextMixin,
    AutorQuerySetMixin,
    ListView,
):
    model = Documento
    template_name = "core/documento/list.html"
    context_object_name = "documentos"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(obra=self.obra)

    def get_context_data(self, **kwargs):
        return super().get_context_data(obra=self.obra, **kwargs)


class DocumentoDetailView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    AutorQuerySetMixin,
    ObraRelatedQuerySetMixin,
    DetailView,
):
    model = Documento
    template_name = "core/documento/detail.html"
    context_object_name = "documento"


class DocumentoCreateView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    ObraContextMixin,
    SuccessMessageMixin,
    CreateView,
):
    success_message = "Documento cadastrado."
    model = Documento
    form_class = DocumentoForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id})

    @transaction.atomic
    def form_valid(self, form):
        form.instance.obra = self.bloquear_obra()
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Adicionar documento",
            "botao": "Salvar",
        })
        return context


class DocumentoUpdateView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    AutorQuerySetMixin,
    ObraRelatedQuerySetMixin,
    SuccessMessageMixin,
    UpdateView,
):
    success_message = "Documento atualizado."
    model = Documento
    form_class = DocumentoForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Editar documento",
            "botao": "Atualizar",
            "cancel_url": reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id}),
        })
        return context


class DocumentoDeleteView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    AutorQuerySetMixin,
    ObraRelatedQuerySetMixin,
    SuccessMessageMixin,
    DeleteView,
):
    success_message = "Documento excluído."
    model = Documento
    template_name = "core/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Excluir documento",
            "cancel_url": reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id}),
        })
        return context

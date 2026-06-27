from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import DocumentoForm
from core.models import Documento, Obra


class DocumentoListView(LoginRequiredMixin, ListView):
    model = Documento
    template_name = "core/documento/list.html"
    context_object_name = "documentos"

    def get_queryset(self):
        obra_pk = self.kwargs.get("obra_pk")
        return Documento.objects.filter(obra__pk=obra_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obra_pk = self.kwargs.get("obra_pk")
        context["obra"] = Obra.objects.get(pk=obra_pk)
        return context


class DocumentoDetailView(LoginRequiredMixin, DetailView):
    model = Documento
    template_name = "core/documento/detail.html"
    context_object_name = "documento"


class DocumentoCreateView(LoginRequiredMixin, CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def get_initial(self):
        initial = super().get_initial()
        obra_pk = self.kwargs.get("obra_pk")
        if obra_pk:
            initial["obra"] = Obra.objects.get(pk=obra_pk)
        return initial

    def form_valid(self, form):
        obra_pk = self.kwargs.get("obra_pk")
        if obra_pk:
            form.instance.obra = Obra.objects.get(pk=obra_pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Adicionar documento",
            "botao": "Salvar",
        })
        return context


class DocumentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Documento
    form_class = DocumentoForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Editar documento",
            "botao": "Atualizar",
            "cancel_url": reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk}),
        })
        return context


class DocumentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Documento
    template_name = "core/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Excluir documento",
            "cancel_url": reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk}),
        })
        return context

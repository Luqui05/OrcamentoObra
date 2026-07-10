from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import DocumentoForm
from core.models import Documento, Obra
from core.views.mixins import UserScopedQuerySetMixin


class DocumentoListView(LoginRequiredMixin, ListView):
    model = Documento
    template_name = "core/documento/list.html"
    context_object_name = "documentos"

    def get_queryset(self):
        obra_pk = self.kwargs.get("obra_pk")
        return Documento.objects.filter(
            Q(obra__cliente_principal__usuario=self.request.user)
            | Q(obra__clientes__usuario=self.request.user),
            obra__pk=obra_pk,
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obra_pk = self.kwargs.get("obra_pk")
        context["obra"] = get_object_or_404(
            Obra,
            Q(cliente_principal__usuario=self.request.user)
            | Q(clientes__usuario=self.request.user),
            pk=obra_pk,
        )
        return context


class DocumentoDetailView(LoginRequiredMixin, UserScopedQuerySetMixin, DetailView):
    model = Documento
    template_name = "core/documento/detail.html"
    context_object_name = "documento"

    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )


class DocumentoCreateView(LoginRequiredMixin, CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = "core/form.html"

    def get_obra(self):
        return get_object_or_404(
            Obra,
            Q(cliente_principal__usuario=self.request.user)
            | Q(clientes__usuario=self.request.user),
            pk=self.kwargs["obra_pk"],
        )

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def get_initial(self):
        initial = super().get_initial()
        initial["obra"] = self.get_obra()
        return initial

    def form_valid(self, form):
        form.instance.obra = self.get_obra()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Adicionar documento",
            "botao": "Salvar",
        })
        return context


class DocumentoUpdateView(LoginRequiredMixin, UserScopedQuerySetMixin, UpdateView):
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

    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )


class DocumentoDeleteView(LoginRequiredMixin, UserScopedQuerySetMixin, DeleteView):
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

    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )

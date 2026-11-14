from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import AtualizacaoObraForm
from core.models import AtualizacaoObra
from core.views.mixins import (
    ClienteGroupRequiredMixin,
    LoginRequiredMixin,
    ObraContextMixin,
    ObraRelatedQuerySetMixin,
    bloquear_obra_do_usuario,
)


class AtualizacaoObraListView(
    LoginRequiredMixin, ClienteGroupRequiredMixin, ObraContextMixin, ListView
):
    model = AtualizacaoObra
    template_name = "core/atualizacao/list.html"
    context_object_name = "atualizacoes"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(obra=self.obra)

    def get_context_data(self, **kwargs):
        return super().get_context_data(obra=self.obra, **kwargs)


class AtualizacaoObraDetailView(
    LoginRequiredMixin, ClienteGroupRequiredMixin, ObraRelatedQuerySetMixin, DetailView
):
    model = AtualizacaoObra
    template_name = "core/atualizacao/detail.html"
    context_object_name = "atualizacao"


class AtualizacaoObraCreateView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    ObraContextMixin,
    SuccessMessageMixin,
    CreateView,
):
    success_message = "Atualização cadastrada."
    model = AtualizacaoObra
    form_class = AtualizacaoObraForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id})

    @transaction.atomic
    def form_valid(self, form):
        form.instance.obra = self.bloquear_obra()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obra = self.obra
        context.update(
            {
                "titulo": "Adicionar atualização da obra",
                "botao": "Salvar",
                "cancel_url": reverse_lazy("obra_detail", kwargs={"pk": obra.pk}),
            }
        )
        return context


class AtualizacaoObraUpdateView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    ObraRelatedQuerySetMixin,
    SuccessMessageMixin,
    UpdateView,
):
    success_message = "Atualização editada."
    model = AtualizacaoObra
    form_class = AtualizacaoObraForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "titulo": "Editar atualização da obra",
                "botao": "Atualizar",
                "cancel_url": reverse_lazy(
                    "obra_detail", kwargs={"pk": self.object.obra_id}
                ),
            }
        )
        return context


class AtualizacaoObraDeleteView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    ObraRelatedQuerySetMixin,
    SuccessMessageMixin,
    DeleteView,
):
    success_message = "Atualização excluída."
    model = AtualizacaoObra
    template_name = "core/confirm_delete.html"
    http_method_names = ["get", "head", "post", "options"]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        objeto = super().get_object()
        bloquear_obra_do_usuario(request.user, objeto.obra_id)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.request.method != "POST":
            return super().get_object(queryset)
        queryset = queryset or self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        if not queryset.filter(pk=pk).exists():
            raise Http404
        return get_object_or_404(AtualizacaoObra.objects.select_for_update(), pk=pk)

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id})

    def form_valid(self, form):
        if self.object.imagens.exclude(cadastrado_por=self.request.user).exists():
            messages.error(
                self.request,
                "Esta atualização tem imagens que você não pode alterar.",
            )
            return redirect(self.get_success_url())
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "titulo": "Excluir atualização da obra",
                "cancel_url": reverse_lazy(
                    "obra_detail", kwargs={"pk": self.object.obra_id}
                ),
            }
        )
        return context

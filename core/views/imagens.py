from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import ImagemObraForm
from core.models import AtualizacaoObra, ImagemObra
from core.views.mixins import (
    ClienteGroupRequiredMixin,
    LoginRequiredMixin,
    ObraContextMixin,
    ObraRelatedQuerySetMixin,
    AutorQuerySetMixin,
    bloquear_obra_do_usuario,
)


class ImagemObraListView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    ObraContextMixin,
    AutorQuerySetMixin,
    ListView,
):
    model = ImagemObra
    template_name = "core/imagem/list.html"
    context_object_name = "imagens"
    paginate_by = 9

    def get_queryset(self):
        return super().get_queryset().filter(obra=self.obra).select_related("atualizacao_obra", "obra")

    def get_context_data(self, **kwargs):
        return super().get_context_data(obra=self.obra, **kwargs)


class ImagemObraDetailView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    AutorQuerySetMixin,
    ObraRelatedQuerySetMixin,
    DetailView,
):
    model = ImagemObra
    template_name = "core/imagem/detail.html"
    context_object_name = "imagem"


class ImagemObraCreateView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    ObraContextMixin,
    SuccessMessageMixin,
    CreateView,
):
    success_message = "Imagem cadastrada."
    model = ImagemObra
    form_class = ImagemObraForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["obra"] = self.obra
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        obra = self.bloquear_obra()
        form.instance.obra = obra
        form.instance.cadastrado_por = self.request.user
        atualizacao = form.cleaned_data.get("atualizacao_obra")
        if atualizacao:
            form.instance.atualizacao_obra = get_object_or_404(
                AtualizacaoObra.objects.select_for_update(),
                pk=atualizacao.pk,
                obra=obra,
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Adicionar imagem da obra",
            "botao": "Salvar",
        })
        return context


class ImagemObraUpdateView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    AutorQuerySetMixin,
    ObraRelatedQuerySetMixin,
    SuccessMessageMixin,
    UpdateView,
):
    success_message = "Imagem atualizada."
    model = ImagemObra
    form_class = ImagemObraForm
    template_name = "core/form.html"

    def get_queryset(self):
        return super().get_queryset().select_related("obra", "atualizacao_obra")

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["obra"] = self.object.obra
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        obra = bloquear_obra_do_usuario(self.request.user, self.object.obra_id)
        atualizacao = form.cleaned_data.get("atualizacao_obra")
        if atualizacao:
            form.instance.atualizacao_obra = get_object_or_404(
                AtualizacaoObra.objects.select_for_update(),
                pk=atualizacao.pk,
                obra=obra,
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Editar imagem da obra",
            "botao": "Atualizar",
            "cancel_url": reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id}),
        })
        return context


class ImagemObraDeleteView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    AutorQuerySetMixin,
    ObraRelatedQuerySetMixin,
    SuccessMessageMixin,
    DeleteView,
):
    success_message = "Imagem excluída."
    model = ImagemObra
    template_name = "core/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Excluir imagem da obra",
            "cancel_url": reverse_lazy("obra_detail", kwargs={"pk": self.object.obra_id}),
        })
        return context

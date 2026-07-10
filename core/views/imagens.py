from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import ImagemObraForm
from core.models import ImagemObra, Obra
from core.views.mixins import UserScopedQuerySetMixin


class ImagemObraListView(LoginRequiredMixin, ListView):
    model = ImagemObra
    template_name = "core/imagem/list.html"
    context_object_name = "imagens"

    def get_queryset(self):
        obra_pk = self.kwargs.get("obra_pk")
        return ImagemObra.objects.filter(
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


class ImagemObraDetailView(LoginRequiredMixin, UserScopedQuerySetMixin, DetailView):
    model = ImagemObra
    template_name = "core/imagem/detail.html"
    context_object_name = "imagem"

    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )


class ImagemObraCreateView(LoginRequiredMixin, CreateView):
    model = ImagemObra
    form_class = ImagemObraForm
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["obra"] = self.get_obra()
        return kwargs

    def form_valid(self, form):
        form.instance.obra = self.get_obra()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Adicionar imagem da obra",
            "botao": "Salvar",
        })
        return context


class ImagemObraUpdateView(LoginRequiredMixin, UserScopedQuerySetMixin, UpdateView):
    model = ImagemObra
    form_class = ImagemObraForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["obra"] = self.object.obra
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Editar imagem da obra",
            "botao": "Atualizar",
            "cancel_url": reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk}),
        })
        return context

    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )


class ImagemObraDeleteView(LoginRequiredMixin, UserScopedQuerySetMixin, DeleteView):
    model = ImagemObra
    template_name = "core/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Excluir imagem da obra",
            "cancel_url": reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk}),
        })
        return context

    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import AtualizacaoObraForm
from core.models import AtualizacaoObra, Obra
from core.views.mixins import UserScopedQuerySetMixin


class AtualizacaoObraListView(LoginRequiredMixin, ListView):
    model = AtualizacaoObra
    template_name = "core/atualizacao/list.html"
    context_object_name = "atualizacoes"

    def get_queryset(self):
        obra_pk = self.kwargs.get("obra_pk")
        return AtualizacaoObra.objects.filter(
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


class AtualizacaoObraDetailView(LoginRequiredMixin, UserScopedQuerySetMixin, DetailView):
    model = AtualizacaoObra
    template_name = "core/atualizacao/detail.html"
    context_object_name = "atualizacao"

    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )


class AtualizacaoObraCreateView(LoginRequiredMixin, CreateView):
    model = AtualizacaoObra
    form_class = AtualizacaoObraForm
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

    def form_valid(self, form):
        form.instance.obra = self.get_obra()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obra = self.get_obra()
        context.update(
            {
                "titulo": "Adicionar atualização da obra",
                "botao": "Salvar",
                "cancel_url": reverse_lazy("obra_detail", kwargs={"pk": obra.pk}),
            }
        )
        return context


class AtualizacaoObraUpdateView(LoginRequiredMixin, UserScopedQuerySetMixin, UpdateView):
    model = AtualizacaoObra
    form_class = AtualizacaoObraForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "titulo": "Editar atualização da obra",
                "botao": "Atualizar",
                "cancel_url": reverse_lazy(
                    "obra_detail", kwargs={"pk": self.object.obra.pk}
                ),
            }
        )
        return context

    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )


class AtualizacaoObraDeleteView(LoginRequiredMixin, UserScopedQuerySetMixin, DeleteView):
    model = AtualizacaoObra
    template_name = "core/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "titulo": "Excluir atualização da obra",
                "cancel_url": reverse_lazy(
                    "obra_detail", kwargs={"pk": self.object.obra.pk}
                ),
            }
        )
        return context

    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )

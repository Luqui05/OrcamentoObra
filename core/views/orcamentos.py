from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import get_object_or_404

from core.forms import OrcamentoForm
from core.models import Orcamento, Obra
from core.views.mixins import UserScopedQuerySetMixin


class OrcamentoDetailView(LoginRequiredMixin, UserScopedQuerySetMixin, DetailView):
    model = Orcamento
    template_name = "core/orcamento/detail.html"
    context_object_name = "orcamento"
    
    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )


class OrcamentoCreateView(LoginRequiredMixin, CreateView):
    model = Orcamento
    form_class = OrcamentoForm
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
        response = super().form_valid(form)

        # Marcar orçamentos anteriores da mesma obra como RECUSADO
        from django.utils import timezone

        Orcamento.objects.filter(obra=self.object.obra).exclude(pk=self.object.pk).exclude(status=Orcamento.StatusChoices.RECUSADO).update(status=Orcamento.StatusChoices.RECUSADO, data_resposta=timezone.now())

        return response

    extra_context = {
        "titulo": "Cadastrar orçamento",
        "botao": "Salvar",
    }


class OrcamentoUpdateView(LoginRequiredMixin, UserScopedQuerySetMixin, UpdateView):
    model = Orcamento
    form_class = OrcamentoForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        latest = obj.obra.orcamentos.order_by("-data_emissao").first()
        if not latest or obj.pk != latest.pk:
            raise PermissionDenied("Somente o orçamento mais recente pode ser editado.")
        return super().dispatch(request, *args, **kwargs)

    extra_context = {
        "titulo": "Editar orçamento",
        "botao": "Atualizar",
    }
    
    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )


class OrcamentoDeleteView(LoginRequiredMixin, UserScopedQuerySetMixin, DeleteView):
    model = Orcamento
    template_name = "core/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Excluir orçamento"
        context["cancel_url"] = reverse_lazy(
            "obra_detail", kwargs={"pk": self.object.obra.pk}
        )
        return context
    
    def get_user_filter(self):
        return Q(obra__cliente_principal__usuario=self.request.user) | Q(
            obra__clientes__usuario=self.request.user
        )

from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from core.forms import OrcamentoForm
from core.models import Orcamento, Obra


class OrcamentoDetailView(DetailView):
    model = Orcamento
    template_name = "core/orcamento/detail.html"
    context_object_name = "orcamento"


class OrcamentoCreateView(CreateView):
    model = Orcamento
    form_class = OrcamentoForm
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

    extra_context = {
        "titulo": "Cadastrar orçamento",
        "botao": "Salvar",
    }


class OrcamentoUpdateView(UpdateView):
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


class OrcamentoDeleteView(DeleteView):
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

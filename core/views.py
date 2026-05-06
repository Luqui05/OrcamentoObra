from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import (
    AtualizacaoObraForm,
    ClienteForm,
    ObraForm,
    OrcamentoForm,
)
from .models import AtualizacaoObra, Cliente, Obra, Orcamento


class HomeTemplateView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_clientes"] = Cliente.objects.count()
        context["total_obras"] = Obra.objects.count()
        return context


class SobreTemplateView(TemplateView):
    template_name = "core/sobre.html"


class ClienteListView(ListView):
    model = Cliente
    template_name = "core/cliente/list.html"
    context_object_name = "clientes"


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "core/cliente/detail.html"
    context_object_name = "cliente"


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/form.html"
    success_url = reverse_lazy("cliente_list")

    extra_context = {
        "titulo": "Cadastrar cliente",
        "botao": "Salvar",
    }


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/form.html"
    success_url = reverse_lazy("cliente_list")

    extra_context = {
        "titulo": "Editar cliente",
        "botao": "Atualizar",
    }


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("cliente_list")

    extra_context = {
        "titulo": "Excluir cliente",
        "cancel_url_name": "cliente_list",
    }


class ObraListView(ListView):
    model = Obra
    template_name = "core/obra/list.html"
    context_object_name = "obras"


class ObraDetailView(DetailView):
    model = Obra
    template_name = "core/obra/detail.html"
    context_object_name = "obra"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orcamentos"] = self.object.orcamentos.all()
        context["atualizacoes"] = self.object.atualizacoes.all()
        return context


class ObraCreateView(CreateView):
    model = Obra
    form_class = ObraForm
    template_name = "core/form.html"
    success_url = reverse_lazy("obra_list")

    extra_context = {
        "titulo": "Cadastrar obra",
        "botao": "Salvar",
        "cancel_url_name": "obra_list",
    }


class ObraUpdateView(UpdateView):
    model = Obra
    form_class = ObraForm
    template_name = "core/form.html"
    success_url = reverse_lazy("obra_list")

    extra_context = {
        "titulo": "Editar obra",
        "botao": "Atualizar",
        "cancel_url_name": "obra_list",
    }


class ObraDeleteView(DeleteView):
    model = Obra
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("obra_list")

    extra_context = {
        "titulo": "Excluir obra",
        "cancel_url_name": "obra_list",
    }


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


class AtualizacaoObraListView(ListView):
    model = AtualizacaoObra
    template_name = "core/atualizacao/list.html"
    context_object_name = "atualizacoes"

    def get_queryset(self):
        obra_pk = self.kwargs.get("obra_pk")
        return AtualizacaoObra.objects.filter(obra__pk=obra_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obra_pk = self.kwargs.get("obra_pk")
        context["obra"] = Obra.objects.get(pk=obra_pk)
        return context


class AtualizacaoObraDetailView(DetailView):
    model = AtualizacaoObra
    template_name = "core/atualizacao/detail.html"
    context_object_name = "atualizacao"


class AtualizacaoObraCreateView(CreateView):
    model = AtualizacaoObra
    form_class = AtualizacaoObraForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def form_valid(self, form):
        obra_pk = self.kwargs.get("obra_pk")
        form.instance.obra = Obra.objects.get(pk=obra_pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obra_pk = self.kwargs.get("obra_pk")
        context.update(
            {
                "titulo": "Adicionar atualização da obra",
                "botao": "Salvar",
                "cancel_url": reverse_lazy("obra_detail", kwargs={"pk": obra_pk}),
            }
        )
        return context


class AtualizacaoObraUpdateView(UpdateView):
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


class AtualizacaoObraDeleteView(DeleteView):
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

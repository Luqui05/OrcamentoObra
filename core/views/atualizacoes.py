from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import AtualizacaoObraForm
from core.models import AtualizacaoObra, Obra


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

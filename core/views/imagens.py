from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.forms import ImagemObraForm
from core.models import ImagemObra, Obra


class ImagemObraListView(LoginRequiredMixin, ListView):
    model = ImagemObra
    template_name = "core/imagem/list.html"
    context_object_name = "imagens"

    def get_queryset(self):
        obra_pk = self.kwargs.get("obra_pk")
        return ImagemObra.objects.filter(obra__pk=obra_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obra_pk = self.kwargs.get("obra_pk")
        context["obra"] = Obra.objects.get(pk=obra_pk)
        return context


class ImagemObraDetailView(LoginRequiredMixin, DetailView):
    model = ImagemObra
    template_name = "core/imagem/detail.html"
    context_object_name = "imagem"


class ImagemObraCreateView(LoginRequiredMixin, CreateView):
    model = ImagemObra
    form_class = ImagemObraForm
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse_lazy("obra_detail", kwargs={"pk": self.object.obra.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        obra_pk = self.kwargs.get("obra_pk")
        if obra_pk:
            kwargs["obra"] = Obra.objects.get(pk=obra_pk)
        return kwargs

    def form_valid(self, form):
        obra_pk = self.kwargs.get("obra_pk")
        if obra_pk:
            form.instance.obra = Obra.objects.get(pk=obra_pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Adicionar imagem da obra",
            "botao": "Salvar",
        })
        return context


class ImagemObraUpdateView(LoginRequiredMixin, UpdateView):
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


class ImagemObraDeleteView(LoginRequiredMixin, DeleteView):
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

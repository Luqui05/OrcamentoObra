from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
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
    ImagemObraForm,
    ObraForm,
    OrcamentoForm,
)
from .forms import DocumentoForm
from .models import AtualizacaoObra, Cliente, ImagemObra, Obra, Orcamento, Documento


def montar_galeria_obra(obra):
    """Monta os itens da galeria unificada (imagens, documentos e orcamentos)."""
    galeria = []

    for img in obra.imagens.all():
        if img.imagem:
            galeria.append(
                {
                    "tipo": "imagem",
                    "titulo": img.legenda or "Imagem",
                    "descricao": "",
                    "url": img.imagem.url,
                    "data": img.data_upload,
                    "obj": img,
                }
            )

    for doc in obra.documentos.all():
        galeria.append(
            {
                "tipo": "documento",
                "titulo": doc.titulo,
                "descricao": doc.descricao,
                "url": doc.arquivo.url,
                "data": doc.data_upload,
                "obj": doc,
            }
        )

    for orc in obra.orcamentos.all():
        if orc.arquivo_pdf:
            galeria.append(
                {
                    "tipo": "orcamento",
                    "titulo": f"Orcamento v{orc.versao}",
                    "descricao": orc.descricao,
                    "url": orc.arquivo_pdf.url,
                    "data": orc.data_emissao,
                    "obj": orc,
                }
            )

    galeria.sort(key=lambda item: item["data"], reverse=True)
    return galeria


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


class ObraGaleriaView(DetailView):
    model = Obra
    template_name = "core/obra/galeria.html"
    context_object_name = "obra"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        galeria_items = montar_galeria_obra(self.object)
        context["galeria_items"] = galeria_items
        context["galeria_midias"] = [item for item in galeria_items if item["tipo"] == "imagem"]
        context["galeria_documentos"] = [item for item in galeria_items if item["tipo"] == "documento"]
        context["galeria_orcamentos"] = [item for item in galeria_items if item["tipo"] == "orcamento"]
        return context


class DocumentoListView(ListView):
    model = Documento
    template_name = "core/documento/list.html"
    context_object_name = "documentos"

    def get_queryset(self):
        obra_pk = self.kwargs.get("obra_pk")
        return Documento.objects.filter(obra__pk=obra_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obra_pk = self.kwargs.get("obra_pk")
        context["obra"] = Obra.objects.get(pk=obra_pk)
        return context


class DocumentoDetailView(DetailView):
    model = Documento
    template_name = "core/documento/detail.html"
    context_object_name = "documento"


class DocumentoCreateView(CreateView):
    model = Documento
    form_class = DocumentoForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Adicionar documento",
            "botao": "Salvar",
        })
        return context


class DocumentoUpdateView(UpdateView):
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


class DocumentoDeleteView(DeleteView):
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


class ImagemObraListView(ListView):
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


class ImagemObraDetailView(DetailView):
    model = ImagemObra
    template_name = "core/imagem/detail.html"
    context_object_name = "imagem"


class ImagemObraCreateView(CreateView):
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


class ImagemObraUpdateView(UpdateView):
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


class ImagemObraDeleteView(DeleteView):
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

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import F, Prefetch, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from core.filter import ObraFilter
from core.forms import ObraForm
from core.models import Documento, ImagemObra, Obra
from core.utils import montar_galeria_obra
from core.views.mixins import (
    ClienteGroupRequiredMixin,
    FilteredListMixin,
    LoginRequiredMixin,
    UserScopedQuerySetMixin,
    bloquear_obra_do_usuario,
)


class ObraListView(
    LoginRequiredMixin, ClienteGroupRequiredMixin, FilteredListMixin,
    UserScopedQuerySetMixin, ListView
):
    model = Obra
    template_name = "core/obra/list.html"
    context_object_name = "obras"
    paginate_by = 10
    filterset_class = ObraFilter

    def get_queryset(self):
        return super().get_queryset().select_related("cliente_principal")

    def get_user_filter(self):
        return Q(cliente_principal__usuario=self.request.user) | Q(
            clientes__usuario=self.request.user
        )


class ObraDetailView(
    LoginRequiredMixin, ClienteGroupRequiredMixin, UserScopedQuerySetMixin, DetailView
):
    model = Obra
    template_name = "core/obra/detail.html"
    context_object_name = "obra"

    def get_queryset(self):
        imagens = (
            ImagemObra.objects.filter(
                cadastrado_por=self.request.user, obra_id=F("atualizacao_obra__obra_id")
            )
            .exclude(imagem="")
            .order_by("-data_upload", "-pk")[:1]
        )
        return super().get_queryset().select_related("cliente_principal").prefetch_related(
            "clientes",
            Prefetch("atualizacoes__imagens", queryset=imagens, to_attr="imagens_visiveis"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orcamentos"] = self.object.orcamentos.all()
        context["atualizacoes"] = self.object.atualizacoes.all()
        return context
    
    def get_user_filter(self):
        return Q(cliente_principal__usuario=self.request.user) | Q(
            clientes__usuario=self.request.user
        )


class ObraGaleriaView(
    LoginRequiredMixin, ClienteGroupRequiredMixin, UserScopedQuerySetMixin, DetailView
):
    model = Obra
    template_name = "core/obra/galeria.html"
    context_object_name = "obra"

    def get_queryset(self):
        usuario = self.request.user
        return super().get_queryset().prefetch_related(
            Prefetch(
                "imagens",
                queryset=ImagemObra.objects.filter(cadastrado_por=usuario),
                to_attr="imagens_visiveis",
            ),
            Prefetch(
                "documentos",
                queryset=Documento.objects.filter(cadastrado_por=usuario),
                to_attr="documentos_visiveis",
            ),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        galeria_items = montar_galeria_obra(self.object)
        context["galeria_items"] = galeria_items
        context["galeria_midias"] = [
            item for item in galeria_items if item["tipo"] == "imagem"
        ]
        context["galeria_documentos"] = [
            item for item in galeria_items if item["tipo"] == "documento"
        ]
        context["galeria_orcamentos"] = [
            item for item in galeria_items if item["tipo"] == "orcamento"
        ]
        return context

    def get_user_filter(self):
        return Q(cliente_principal__usuario=self.request.user) | Q(
            clientes__usuario=self.request.user
        )


class ObraCreateView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    success_message = "Obra cadastrada."
    model = Obra
    form_class = ObraForm
    template_name = "core/form.html"
    success_url = reverse_lazy("obra_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario"] = self.request.user
        return kwargs

    extra_context = {
        "titulo": "Cadastrar obra",
        "botao": "Salvar",
        "cancel_url_name": "obra_list",
    }


class ObraUpdateView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    UserScopedQuerySetMixin,
    SuccessMessageMixin,
    UpdateView,
):
    success_message = "Obra atualizada."
    model = Obra
    form_class = ObraForm
    template_name = "core/form.html"
    success_url = reverse_lazy("obra_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario"] = self.request.user
        return kwargs

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        objeto = self.get_object()
        bloquear_obra_do_usuario(request.user, objeto.pk)
        return super().post(request, *args, **kwargs)

    extra_context = {
        "titulo": "Editar obra",
        "botao": "Atualizar",
        "cancel_url_name": "obra_list",
    }
    
    def get_user_filter(self):
        return Q(cliente_principal__usuario=self.request.user) | Q(
            clientes__usuario=self.request.user
        )


class ObraDeleteView(
    LoginRequiredMixin,
    ClienteGroupRequiredMixin,
    UserScopedQuerySetMixin,
    SuccessMessageMixin,
    DeleteView,
):
    success_message = "Obra excluída."
    model = Obra
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("obra_list")
    http_method_names = ["get", "head", "post", "options"]

    extra_context = {
        "titulo": "Excluir obra",
        "cancel_url_name": "obra_list",
    }

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        objeto = super().get_object()
        bloquear_obra_do_usuario(request.user, objeto.pk)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        usuario = self.request.user
        if (
            self.object.documentos.exclude(cadastrado_por=usuario).exists()
            or self.object.imagens.exclude(cadastrado_por=usuario).exists()
        ):
            messages.error(
                self.request,
                "Esta obra tem anexos que você não pode excluir.",
            )
            return redirect("obra_detail", pk=self.object.pk)
        return super().form_valid(form)
    
    def get_user_filter(self):
        return Q(cliente_principal__usuario=self.request.user) | Q(
            clientes__usuario=self.request.user
        )

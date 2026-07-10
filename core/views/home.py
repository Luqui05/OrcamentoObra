from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from core.models import (
    AtualizacaoObra,
    Cliente,
    Documento,
    ImagemObra,
    Obra,
    Orcamento,
)


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obras = Obra.objects.filter(
            Q(cliente_principal__usuario=self.request.user)
            | Q(clientes__usuario=self.request.user)
        ).distinct()
        orcamentos = Orcamento.objects.filter(obra__in=obras)
        context["total_clientes"] = Cliente.objects.filter(
            usuario=self.request.user
        ).count()
        context["total_obras"] = obras.count()
        context["total_orcamentos"] = orcamentos.count()
        context["orcamentos_pendentes"] = orcamentos.filter(
            status=Orcamento.StatusChoices.PENDENTE
        ).count()
        context["total_documentos"] = Documento.objects.filter(obra__in=obras).count()
        context["total_imagens"] = ImagemObra.objects.filter(obra__in=obras).count()
        context["total_atualizacoes"] = AtualizacaoObra.objects.filter(
            obra__in=obras
        ).count()
        context["obras_recentes"] = obras.select_related(
            "cliente_principal"
        ).order_by("-data_cadastro")[:5]
        return context


class SobreTemplateView(TemplateView):
    template_name = "core/sobre.html"

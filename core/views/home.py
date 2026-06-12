from django.views.generic import TemplateView

from core.models import (
    AtualizacaoObra,
    Cliente,
    Documento,
    ImagemObra,
    Obra,
    Orcamento,
)


class HomeTemplateView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_clientes"] = Cliente.objects.count()
        context["total_obras"] = Obra.objects.count()
        context["total_orcamentos"] = Orcamento.objects.count()
        context["orcamentos_pendentes"] = Orcamento.objects.filter(
            status=Orcamento.StatusChoices.PENDENTE
        ).count()
        context["total_documentos"] = Documento.objects.count()
        context["total_imagens"] = ImagemObra.objects.count()
        context["total_atualizacoes"] = AtualizacaoObra.objects.count()
        context["obras_recentes"] = Obra.objects.select_related(
            "cliente_principal"
        ).order_by("-data_cadastro")[:5]
        return context


class SobreTemplateView(TemplateView):
    template_name = "core/sobre.html"

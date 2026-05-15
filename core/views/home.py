from django.views.generic import TemplateView

from core.models import Cliente, Obra


class HomeTemplateView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_clientes"] = Cliente.objects.count()
        context["total_obras"] = Obra.objects.count()
        return context


class SobreTemplateView(TemplateView):
    template_name = "core/sobre.html"

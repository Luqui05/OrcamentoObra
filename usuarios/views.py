from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CadastroUsuarioForm


class CadastroUsuarioView(CreateView):
    form_class = CadastroUsuarioForm
    template_name = "usuarios/cadastro.html"
    success_url = reverse_lazy("cliente_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

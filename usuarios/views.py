from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CadastroUsuarioForm


class CadastroUsuarioView(CreateView):
    form_class = CadastroUsuarioForm
    template_name = "usuarios/cadastro.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Conta criada com sucesso. Bem-vindo ao OrcamentoObra!")
        return response

from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .constants import CLIENTE_GROUP_NAME
from .forms import CadastroUsuarioForm


class CadastroUsuarioView(CreateView):
    form_class = CadastroUsuarioForm
    template_name = "usuarios/cadastro.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        response = super().form_valid(form)
        grupo_clientes, _ = Group.objects.get_or_create(name=CLIENTE_GROUP_NAME)
        self.object.groups.add(grupo_clientes)
        login(self.request, self.object)
        messages.success(self.request, "Conta criada com sucesso. Bem-vindo ao OrcamentoObra!")
        return response

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .constants import CLIENTE_GROUP_NAME


class CadastroUsuarioTests(TestCase):
    def test_novo_usuario_e_adicionado_ao_grupo_clientes(self):
        response = self.client.post(
            reverse("cadastro_usuario"),
            {
                "username": "novo.cliente",
                "email": "novo.cliente@example.com",
                "password1": "Uma-senha-segura-2026",
                "password2": "Uma-senha-segura-2026",
            },
        )

        self.assertRedirects(response, reverse("index"))
        usuario = get_user_model().objects.get(username="novo.cliente")
        self.assertTrue(usuario.groups.filter(name=CLIENTE_GROUP_NAME).exists())

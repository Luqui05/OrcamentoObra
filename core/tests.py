from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Obra


class CorePublicAccessTests(TestCase):
    def setUp(self):
        usuario = get_user_model().objects.create_user(
            username="cliente.teste",
            password="senha-teste",
        )
        self.cliente = Cliente.objects.create(
            usuario=usuario,
            nome="Cliente Teste",
            cpf="123.456.789-00",
            telefone="(45) 99999-0000",
        )
        self.obra = Obra.objects.create(
            titulo="Reforma residencial",
            descricao="Reforma completa",
            endereco="Rua Central, 123",
            cliente_principal=self.cliente,
        )
        self.obra.clientes.add(self.cliente)

    def test_home_is_public(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")

    def test_obra_crud_pages_are_public(self):
        urls = [
            reverse("obra_list"),
            reverse("obra_create"),
            reverse("obra_detail", args=[self.obra.pk]),
            reverse("obra_update", args=[self.obra.pk]),
            reverse("obra_delete", args=[self.obra.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)

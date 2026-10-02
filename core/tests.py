from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from usuarios.constants import CLIENTE_GROUP_NAME

from .models import Cliente, Obra, Orcamento


class CoreAccessTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username="cliente.teste",
            password="senha-teste",
        )
        grupo_clientes, _ = Group.objects.get_or_create(name=CLIENTE_GROUP_NAME)
        self.usuario.groups.add(grupo_clientes)

        self.cliente = Cliente.objects.create(
            usuario=self.usuario,
            nome="Cliente Teste",
            cpf="123.456.789-00",
            telefone="(45) 99999-0000",
        )
        self.obra = self.criar_obra("Reforma residencial")

    def criar_obra(self, titulo):
        obra = Obra.objects.create(
            titulo=titulo,
            descricao="Reforma completa",
            endereco="Rua Central, 123",
            cliente_principal=self.cliente,
        )
        obra.clientes.add(self.cliente)
        return obra

    def test_usuario_anonimo_e_redirecionado_para_login(self):
        orcamento = Orcamento.objects.create(
            obra=self.obra,
            versao=1,
            descricao="Orçamento inicial",
            valor_total="1500.00",
            arquivo_pdf=SimpleUploadedFile(
                "orcamento.pdf", b"arquivo de teste", content_type="application/pdf"
            ),
        )
        urls = (
            reverse("index"),
            reverse("obra_list"),
            reverse("orcamento_update", args=[orcamento.pk]),
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))

    def test_membro_do_grupo_clientes_acessa_as_views(self):
        self.client.force_login(self.usuario)
        urls = [
            reverse("index"),
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

    def test_usuario_fora_do_grupo_recebe_forbidden(self):
        usuario_sem_grupo = get_user_model().objects.create_user(
            username="sem.grupo",
            password="senha-teste",
        )
        self.client.force_login(usuario_sem_grupo)

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 403)

    def test_lista_de_obras_e_paginada(self):
        for indice in range(10):
            self.criar_obra(f"Obra {indice:02d}")
        self.client.force_login(self.usuario)

        response = self.client.get(reverse("obra_list"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].count, 11)
        self.assertEqual(len(response.context["obras"]), 1)
        self.assertContains(response, "2 de 2")

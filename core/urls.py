from django.urls import path

from .views import (
    ClienteCreateView,
    ClienteDeleteView,
    ClienteDetailView,
    ClienteListView,
    ClienteUpdateView,
    HomeTemplateView,
    ObraCreateView,
    ObraDeleteView,
    ObraDetailView,
    ObraListView,
    ObraUpdateView,
    SobreTemplateView,
    OrcamentoDetailView,
    OrcamentoCreateView,
    OrcamentoUpdateView,
    OrcamentoDeleteView,
    AtualizacaoObraListView,
    AtualizacaoObraCreateView,
    AtualizacaoObraDetailView,
    AtualizacaoObraUpdateView,
    AtualizacaoObraDeleteView,
)

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="index"),
    path("sobre/", SobreTemplateView.as_view(), name="sobre"),
    # Clientes
    path("clientes/", ClienteListView.as_view(), name="cliente_list"),
    path("clientes/novo/", ClienteCreateView.as_view(), name="cliente_create"),
    path("clientes/<int:pk>/", ClienteDetailView.as_view(), name="cliente_detail"),
    path(
        "clientes/<int:pk>/editar/", ClienteUpdateView.as_view(), name="cliente_update"
    ),
    path(
        "clientes/<int:pk>/excluir/", ClienteDeleteView.as_view(), name="cliente_delete"
    ),
    # Obras
    path("obras/", ObraListView.as_view(), name="obra_list"),
    path("obras/nova/", ObraCreateView.as_view(), name="obra_create"),
    path("obras/<int:pk>/", ObraDetailView.as_view(), name="obra_detail"),
    path("obras/<int:pk>/editar/", ObraUpdateView.as_view(), name="obra_update"),
    path("obras/<int:pk>/excluir/", ObraDeleteView.as_view(), name="obra_delete"),
    
    # Orcamento
    path(
        "orcamentos/<int:pk>/", OrcamentoDetailView.as_view(), name="orcamento_detail"
    ),
    path(
        "obras/<int:obra_pk>/orcamentos/novo/",
        OrcamentoCreateView.as_view(),
        name="orcamento_create",
    ),
    path(
        "orcamentos/<int:pk>/editar/",
        OrcamentoUpdateView.as_view(),
        name="orcamento_update",
    ),
    path(
        "orcamentos/<int:pk>/excluir/",
        OrcamentoDeleteView.as_view(),
        name="orcamento_delete",
    ),
    
    # AtualizacaoObra
    path(
        "obra/<int:obra_pk>/atualizacoes/",
        AtualizacaoObraListView.as_view(),
        name="atualizacao_list",
    ),
    path(
        "obra/<int:obra_pk>/atualizacao/nova/",
        AtualizacaoObraCreateView.as_view(),
        name="atualizacao_create",
    ),
    path(
        "atualizacao/<int:pk>/",
        AtualizacaoObraDetailView.as_view(),
        name="atualizacao_detail",
    ),
    path(
        "atualizacao/<int:pk>/editar/",
        AtualizacaoObraUpdateView.as_view(),
        name="atualizacao_update",
    ),
    path(
        "atualizacao/<int:pk>/excluir/",
        AtualizacaoObraDeleteView.as_view(),
        name="atualizacao_delete",
    ),
]

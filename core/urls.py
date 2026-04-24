from django.urls import path

from .views import (
    ClienteCreateView,
    ClienteDeleteView,
    ClienteDetailView,
    ClienteListView,
    ClienteUpdateView,
    SobreTemplateView,
)

urlpatterns = [
    path("", SobreTemplateView.as_view(), name="sobre"),
    path("clientes/", ClienteListView.as_view(), name="cliente_list"),
    path("clientes/novo/", ClienteCreateView.as_view(), name="cliente_create"),
    path("clientes/<int:pk>/", ClienteDetailView.as_view(), name="cliente_detail"),
    path("clientes/<int:pk>/editar/", ClienteUpdateView.as_view(), name="cliente_update"),
    path("clientes/<int:pk>/excluir/", ClienteDeleteView.as_view(), name="cliente_delete"),
]

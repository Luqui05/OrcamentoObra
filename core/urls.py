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
)

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="index"),
    path("sobre/", SobreTemplateView.as_view(), name="sobre"),
    path("clientes/", ClienteListView.as_view(), name="cliente_list"),
    path("clientes/novo/", ClienteCreateView.as_view(), name="cliente_create"),
    path("clientes/<int:pk>/", ClienteDetailView.as_view(), name="cliente_detail"),
    path("clientes/<int:pk>/editar/", ClienteUpdateView.as_view(), name="cliente_update"),
    path("clientes/<int:pk>/excluir/", ClienteDeleteView.as_view(), name="cliente_delete"),
    path("obras/", ObraListView.as_view(), name="obra_list"),
    path("obras/nova/", ObraCreateView.as_view(), name="obra_create"),
    path("obras/<int:pk>/", ObraDetailView.as_view(), name="obra_detail"),
    path("obras/<int:pk>/editar/", ObraUpdateView.as_view(), name="obra_update"),
    path("obras/<int:pk>/excluir/", ObraDeleteView.as_view(), name="obra_delete"),
]

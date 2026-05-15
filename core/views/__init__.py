from .home import HomeTemplateView, SobreTemplateView
from .clientes import (
    ClienteListView,
    ClienteDetailView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView,
)
from .obras import (
    ObraListView,
    ObraDetailView,
    ObraGaleriaView,
    ObraCreateView,
    ObraUpdateView,
    ObraDeleteView,
)
from .documentos import (
    DocumentoListView,
    DocumentoDetailView,
    DocumentoCreateView,
    DocumentoUpdateView,
    DocumentoDeleteView,
)
from .imagens import (
    ImagemObraListView,
    ImagemObraDetailView,
    ImagemObraCreateView,
    ImagemObraUpdateView,
    ImagemObraDeleteView,
)
from .orcamentos import (
    OrcamentoDetailView,
    OrcamentoCreateView,
    OrcamentoUpdateView,
    OrcamentoDeleteView,
)
from .atualizacoes import (
    AtualizacaoObraListView,
    AtualizacaoObraDetailView,
    AtualizacaoObraCreateView,
    AtualizacaoObraUpdateView,
    AtualizacaoObraDeleteView,
)

__all__ = [
    # home
    "HomeTemplateView",
    "SobreTemplateView",
    # clientes
    "ClienteListView",
    "ClienteDetailView",
    "ClienteCreateView",
    "ClienteUpdateView",
    "ClienteDeleteView",
    # obras
    "ObraListView",
    "ObraDetailView",
    "ObraGaleriaView",
    "ObraCreateView",
    "ObraUpdateView",
    "ObraDeleteView",
    # documentos
    "DocumentoListView",
    "DocumentoDetailView",
    "DocumentoCreateView",
    "DocumentoUpdateView",
    "DocumentoDeleteView",
    # imagens
    "ImagemObraListView",
    "ImagemObraDetailView",
    "ImagemObraCreateView",
    "ImagemObraUpdateView",
    "ImagemObraDeleteView",
    # orcamentos
    "OrcamentoDetailView",
    "OrcamentoCreateView",
    "OrcamentoUpdateView",
    "OrcamentoDeleteView",
    # atualizacoes
    "AtualizacaoObraListView",
    "AtualizacaoObraDetailView",
    "AtualizacaoObraCreateView",
    "AtualizacaoObraUpdateView",
    "AtualizacaoObraDeleteView",
]

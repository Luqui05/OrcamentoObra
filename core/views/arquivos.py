import mimetypes
from pathlib import PurePosixPath

from django.http import FileResponse, Http404
from django.views.generic import DetailView

from core.models import Documento, ImagemObra, Orcamento
from core.views.mixins import (
    AutorQuerySetMixin,
    ClienteGroupRequiredMixin,
    LoginRequiredMixin,
    ObraRelatedQuerySetMixin,
)


class ArquivoView(
    LoginRequiredMixin, ClienteGroupRequiredMixin, ObraRelatedQuerySetMixin, DetailView
):
    tipos_imagem_inline = {
        "image/avif", "image/bmp", "image/gif", "image/jpeg", "image/png",
        "image/tiff", "image/webp", "image/x-icon", "image/vnd.microsoft.icon",
    }
    exibir_imagem = False

    def get(self, request, *args, **kwargs):
        arquivo = getattr(self.get_object(), self.campo_arquivo)
        if not arquivo:
            raise Http404

        nome = PurePosixPath(arquivo.name).name
        tipo, _ = mimetypes.guess_type(nome)
        inline = self.exibir_imagem and tipo in self.tipos_imagem_inline
        try:
            conteudo = arquivo.open("rb")
        except FileNotFoundError as exc:
            raise Http404 from exc

        response = FileResponse(
            conteudo,
            filename=nome,
            as_attachment=not inline,
            content_type=tipo if inline else "application/octet-stream",
        )
        response["X-Content-Type-Options"] = "nosniff"
        response["Cache-Control"] = "private, no-store"
        return response


class DocumentoArquivoView(AutorQuerySetMixin, ArquivoView):
    model = Documento
    campo_arquivo = "arquivo"


class ImagemObraArquivoView(AutorQuerySetMixin, ArquivoView):
    model = ImagemObra
    campo_arquivo = "imagem"
    exibir_imagem = True


class OrcamentoArquivoView(ArquivoView):
    model = Orcamento
    campo_arquivo = "arquivo_pdf"

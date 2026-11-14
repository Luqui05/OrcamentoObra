"""Utils e helpers do app core."""
from typing import List

from django.urls import reverse

from core.models import Obra


def montar_galeria_obra(obra: Obra) -> List[dict]:
    """Monta os itens da galeria unificada (imagens, documentos e orcamentos)."""
    galeria = []

    for img in obra.imagens_visiveis:
        if img.imagem:
            galeria.append(
                {
                    "tipo": "imagem",
                    "titulo": img.legenda or "Imagem",
                    "descricao": "",
                    "url": reverse("imagem_arquivo", args=[img.pk]),
                    "data": img.data_upload,
                    "obj": img,
                }
            )

    for doc in obra.documentos_visiveis:
        if not doc.arquivo:
            continue
        galeria.append(
            {
                "tipo": "documento",
                "titulo": doc.titulo,
                "descricao": doc.descricao,
                "url": reverse("documento_arquivo", args=[doc.pk]),
                "data": doc.data_upload,
                "obj": doc,
            }
        )

    for orc in obra.orcamentos.all():
        if orc.arquivo_pdf:
            galeria.append(
                {
                    "tipo": "orcamento",
                    "titulo": f"Orcamento v{orc.versao}",
                    "descricao": orc.descricao,
                    "url": reverse("orcamento_arquivo", args=[orc.pk]),
                    "data": orc.data_emissao,
                    "obj": orc,
                }
            )

    galeria.sort(key=lambda item: item["data"], reverse=True)
    return galeria

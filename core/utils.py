"""Utils e helpers do app core."""
from typing import List

from core.models import ImagemObra, Documento, Orcamento, Obra


def montar_galeria_obra(obra: Obra) -> List[dict]:
    """Monta os itens da galeria unificada (imagens, documentos e orcamentos)."""
    galeria = []

    for img in obra.imagens.all():
        if img.imagem:
            galeria.append(
                {
                    "tipo": "imagem",
                    "titulo": img.legenda or "Imagem",
                    "descricao": "",
                    "url": img.imagem.url,
                    "data": img.data_upload,
                    "obj": img,
                }
            )

    for doc in obra.documentos.all():
        galeria.append(
            {
                "tipo": "documento",
                "titulo": doc.titulo,
                "descricao": doc.descricao,
                "url": doc.arquivo.url,
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
                    "url": orc.arquivo_pdf.url,
                    "data": orc.data_emissao,
                    "obj": orc,
                }
            )

    galeria.sort(key=lambda item: item["data"], reverse=True)
    return galeria

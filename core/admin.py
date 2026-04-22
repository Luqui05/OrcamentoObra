from django.contrib import admin

from .models import (
    AtualizacaoObra,
    Cliente,
    Documento,
    ImagemObra,
    Obra,
    Orcamento,
)

admin.site.register(Cliente)
admin.site.register(Obra)
admin.site.register(Orcamento)
admin.site.register(Documento)
admin.site.register(AtualizacaoObra)
admin.site.register(ImagemObra)
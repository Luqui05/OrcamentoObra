from django.contrib import admin

from .models import (
    AtualizacaoObra,
    Cliente,
    Documento,
    ImagemObra,
    Obra,
    Orcamento,
)

class AdministracaoSomenteSuperusuario(admin.ModelAdmin):
    """Modelos com arquivos/autoria ficam fora do admin de contas staff comuns."""

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(Cliente)
admin.site.register(Obra, AdministracaoSomenteSuperusuario)
admin.site.register(Orcamento)
admin.site.register(Documento, AdministracaoSomenteSuperusuario)
admin.site.register(AtualizacaoObra, AdministracaoSomenteSuperusuario)
admin.site.register(ImagemObra, AdministracaoSomenteSuperusuario)

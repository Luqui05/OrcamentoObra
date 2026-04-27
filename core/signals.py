from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage

from .models import Orcamento, Documento, ImagemObra


@receiver(pre_save, sender=Orcamento)
def deletar_arquivo_pdf_antigo_orcamento(sender, instance, **kwargs):
    """Remove arquivo PDF antigo ao atualizar orçamento."""
    if not instance.pk:
        return
    
    try:
        obj_antigo = Orcamento.objects.get(pk=instance.pk)
    except Orcamento.DoesNotExist:
        return
    
    if obj_antigo.arquivo_pdf != instance.arquivo_pdf:
        if obj_antigo.arquivo_pdf:
            if default_storage.exists(obj_antigo.arquivo_pdf.name):
                default_storage.delete(obj_antigo.arquivo_pdf.name)


@receiver(post_delete, sender=Orcamento)
def deletar_arquivo_pdf_orcamento(sender, instance, **kwargs):
    """Remove arquivo PDF ao excluir orçamento."""
    if instance.arquivo_pdf:
        if default_storage.exists(instance.arquivo_pdf.name):
            default_storage.delete(instance.arquivo_pdf.name)


@receiver(pre_save, sender=Documento)
def deletar_arquivo_antigo_documento(sender, instance, **kwargs):
    """Remove arquivo antigo ao atualizar documento."""
    if not instance.pk:
        return
    
    try:
        obj_antigo = Documento.objects.get(pk=instance.pk)
    except Documento.DoesNotExist:
        return
    
    if obj_antigo.arquivo != instance.arquivo:
        if obj_antigo.arquivo:
            if default_storage.exists(obj_antigo.arquivo.name):
                default_storage.delete(obj_antigo.arquivo.name)


@receiver(post_delete, sender=Documento)
def deletar_arquivo_documento(sender, instance, **kwargs):
    """Remove arquivo ao excluir documento."""
    if instance.arquivo:
        if default_storage.exists(instance.arquivo.name):
            default_storage.delete(instance.arquivo.name)


@receiver(pre_save, sender=ImagemObra)
def deletar_imagem_antiga(sender, instance, **kwargs):
    """Remove imagem antiga ao atualizar."""
    if not instance.pk:
        return
    
    try:
        obj_antigo = ImagemObra.objects.get(pk=instance.pk)
    except ImagemObra.DoesNotExist:
        return
    
    if obj_antigo.imagem != instance.imagem:
        if obj_antigo.imagem:
            if default_storage.exists(obj_antigo.imagem.name):
                default_storage.delete(obj_antigo.imagem.name)


@receiver(post_delete, sender=ImagemObra)
def deletar_imagem(sender, instance, **kwargs):
    """Remove imagem ao excluir registro."""
    if instance.imagem:
        if default_storage.exists(instance.imagem.name):
            default_storage.delete(instance.imagem.name)

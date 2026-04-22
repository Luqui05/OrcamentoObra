from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

class Cliente(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cliente",
    )
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["nome"]
        
    def __str__(self):
        return self.nome
    
class Obra(models.Model):
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    endereco = models.CharField(max_length=255)
    clientes = models.ManyToManyField(Cliente, related_name="obras", blank=True)
    cliente_principal = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="obras_principais",
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_cadastro"]

    def clean(self):
        super().clean()
        if self.pk and self.cliente_principal_id:
            if self.clientes.exists() and not self.clientes.filter(
                pk=self.cliente_principal_id
            ).exists():
                raise ValidationError(
                    {
                        "cliente_principal": (
                            "O cliente principal deve estar entre os clientes da obra."
                        )
                    }
                )

    def __str__(self):
        return self.titulo

class Orcamento(models.Model):
    class StatusChoices(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        APROVADO = "APROVADO", "Aprovado"
        RECUSADO = "RECUSADO", "Recusado"

    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name="orcamentos")
    versao = models.PositiveIntegerField()
    descricao = models.TextField()
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    arquivo_pdf = models.FileField(upload_to="orcamentos/pdfs/")
    data_emissao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDENTE,
    )
    mensagem_cliente = models.TextField(blank=True)
    data_resposta = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-data_emissao"]
        constraints = [
            models.UniqueConstraint(
                fields=["obra", "versao"],
                name="orcamento_obra_versao_unica",
            )
        ]

    def __str__(self):
        return f"Orçamento da obra {self.obra.titulo} - versão {self.versao}"
    
class Documento(models.Model):
    class TipoDocumento(models.TextChoices):
        PROJETO = "PROJETO", "Projeto"
        ORCAMENTO = "ORCAMENTO", "Orçamento"
        CONTRATO = "CONTRATO", "Contrato"
        NOTA_FISCAL = "NOTA_FISCAL", "Nota fiscal"
        OUTRO = "OUTRO", "Outro"

    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name="documentos")
    titulo = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=20, choices=TipoDocumento.choices)
    arquivo = models.FileField(upload_to="documentos/arquivos/")
    descricao = models.TextField(blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_upload"]

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_documento_display()})"
    
class AtualizacaoObra(models.Model):
    obra = models.ForeignKey(
        Obra,
        on_delete=models.CASCADE,
        related_name="atualizacoes",
    )
    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    semana_referencia = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data"]

    def __str__(self):
        return f"{self.titulo} - semana {self.semana_referencia}"
    
class ImagemObra(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name="imagens")
    atualizacao_obra = models.ForeignKey(
        AtualizacaoObra,
        on_delete=models.SET_NULL,
        related_name="imagens",
        blank=True,
        null=True,
    )
    imagem = models.ImageField(upload_to="obras/imagens/")
    legenda = models.CharField(max_length=255, blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_upload"]

    def clean(self):
        super().clean()
        if self.atualizacao_obra and self.atualizacao_obra.obra_id != self.obra_id:
            raise ValidationError(
                {
                    "atualizacao_obra": (
                        "A atualização da obra deve pertencer à mesma obra da imagem."
                    )
                }
            )

    def __str__(self):
        return self.legenda or f"Imagem da obra {self.obra.titulo}"

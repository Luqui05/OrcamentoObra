from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


COTA_MENSAL_PADRAO = 50_000


class ConfiguracaoIA(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    ativo = models.BooleanField("assistente ativo", default=False)
    endpoint = models.URLField("URL de Chat Completions", max_length=500)
    modelo = models.CharField(max_length=120)
    chave_api = models.CharField("chave da API", max_length=1000)
    cota_mensal_padrao = models.PositiveIntegerField(
        "cota mensal padrão (tokens)", default=COTA_MENSAL_PADRAO
    )
    limite_resposta_tokens = models.PositiveIntegerField(
        "limite de tokens por resposta",
        default=800,
        validators=[MinValueValidator(1), MaxValueValidator(4096)],
    )

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name="ia_config_unica")]

    @classmethod
    def atual(cls):
        return cls.objects.filter(pk=1).first()


class AcessoIA(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="acesso_ia"
    )
    ativo = models.BooleanField("acesso ao assistente", default=False)
    cota_mensal = models.PositiveIntegerField(
        "cota mensal individual (tokens)", blank=True, null=True
    )


class ConsumoMensalIA(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consumos_ia"
    )
    mes = models.DateField()
    tokens_usados = models.PositiveBigIntegerField(default=0)
    tokens_reservados = models.PositiveBigIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["usuario", "mes"], name="ia_consumo_usuario_mes_unico")
        ]


class RequisicaoIA(models.Model):
    class Origem(models.TextChoices):
        ASSISTENTE = "assistente", "Assistente"
        TESTE_CONEXAO = "teste_conexao", "Teste de conexão"

    class Status(models.TextChoices):
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        SUCESSO = "sucesso", "Concluída"
        BLOQUEADA = "bloqueada", "Bloqueada"
        ERRO = "erro", "Erro"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="requisicoes_ia",
        null=True,
    )
    origem = models.CharField(max_length=20, choices=Origem.choices)
    status = models.CharField(max_length=20, choices=Status.choices)
    modelo = models.CharField(max_length=120, blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    concluida_em = models.DateTimeField(blank=True, null=True)
    mes = models.DateField()
    tokens_entrada = models.PositiveBigIntegerField(blank=True, null=True)
    tokens_saida = models.PositiveBigIntegerField(blank=True, null=True)
    tokens_debitados = models.PositiveBigIntegerField(default=0)
    tokens_reservados = models.PositiveBigIntegerField(default=0)
    detalhe = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-criada_em", "-pk"]
        indexes = [models.Index(fields=["usuario", "mes"], name="ia_requisicao_usuario_mes")]


class InteracaoAssistente(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interacoes_ia"
    )
    requisicao = models.OneToOneField(
        RequisicaoIA, on_delete=models.CASCADE, related_name="interacao"
    )
    pergunta = models.TextField()
    resposta = models.TextField()
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-pk"]
        indexes = [models.Index(fields=["usuario", "-id"], name="ia_interacao_usuario_recente")]

import json
from datetime import timedelta
from http.client import HTTPException
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.views.decorators.debug import sensitive_variables

from .models import (
    COTA_MENSAL_PADRAO,
    AcessoIA,
    ConfiguracaoIA,
    ConsumoMensalIA,
    InteracaoAssistente,
    RequisicaoIA,
)


class ErroIA(Exception):
    def __init__(self, mensagem, codigo_http):
        super().__init__(mensagem)
        self.codigo_http = codigo_http


class _SemRedirecionamento(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def mes_atual():
    return timezone.localdate().replace(day=1)


def cota_do_usuario(configuracao, acesso):
    if acesso and acesso.cota_mensal is not None:
        return acesso.cota_mensal
    return configuracao.cota_mensal_padrao if configuracao else COTA_MENSAL_PADRAO


def reconciliar_requisicoes_pendentes(usuario=None, mes=None):
    """Fecha reservas de chamadas que não terminaram após o tempo máximo de rede."""
    corte = timezone.now() - timedelta(minutes=2)
    pendentes = RequisicaoIA.objects.filter(
        status=RequisicaoIA.Status.EM_ANDAMENTO,
        criada_em__lt=corte,
    )
    if usuario is not None:
        pendentes = pendentes.filter(usuario=usuario)
    if mes is not None:
        pendentes = pendentes.filter(mes=mes)

    for pk in list(pendentes.values_list("pk", flat=True)):
        with transaction.atomic():
            encerrou = RequisicaoIA.objects.filter(
                pk=pk, status=RequisicaoIA.Status.EM_ANDAMENTO,
            ).update(
                status=RequisicaoIA.Status.ERRO,
                detalhe="A chamada foi interrompida; o consumo foi contabilizado pela reserva.",
                concluida_em=timezone.now(),
                tokens_debitados=F("tokens_reservados"),
                tokens_reservados=0,
            )
            if not encerrou:
                continue

            requisicao = RequisicaoIA.objects.get(pk=pk)
            reserva = requisicao.tokens_debitados
            if reserva and requisicao.usuario_id is not None:
                ConsumoMensalIA.objects.filter(
                    usuario_id=requisicao.usuario_id, mes=requisicao.mes,
                ).update(
                    # O provedor pode ter cobrado a chamada antes da interrupção.
                    tokens_reservados=F("tokens_reservados") - reserva,
                    tokens_usados=F("tokens_usados") + reserva,
                )


def endpoint_https_valido(endpoint):
    try:
        url = urlsplit(endpoint)
        url.port  # Valida a porta quando informada.
        return (
            url.scheme == "https"
            and bool(url.hostname)
            and url.username is None
            and url.password is None
            and not url.fragment
        )
    except ValueError:
        return False


@sensitive_variables()
def _enviar_ao_provedor(configuracao, mensagens, limite_resposta):
    corpo = json.dumps(
        {
            "model": configuracao.modelo,
            "messages": mensagens,
            "max_completion_tokens": limite_resposta,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    requisicao = Request(
        configuracao.endpoint,
        data=corpo,
        headers={
            "Authorization": f"Bearer {configuracao.chave_api}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with build_opener(_SemRedirecionamento()).open(requisicao, timeout=15) as resposta:
        corpo_resposta = resposta.read(1_000_001)
        if len(corpo_resposta) > 1_000_000:
            raise ValueError("Resposta HTTP maior que o limite aceito.")
        return json.loads(corpo_resposta)


def _ler_tokens(dados, campo):
    valor = dados.get(campo)
    return valor if type(valor) is int and 0 <= valor <= 2_147_483_647 else None


def _concluir(
    consumo, requisicao, reserva, status, detalhe="", texto="", pergunta="",
    tokens_entrada=None, tokens_saida=None, tokens_debitados=0,
):
    with transaction.atomic():
        # Assim como na reconciliação, adquira o bloqueio da requisição antes
        # de atualizar o consumo. A transição condicional tem um único vencedor.
        encerrou = RequisicaoIA.objects.filter(
            pk=requisicao.pk, status=RequisicaoIA.Status.EM_ANDAMENTO,
        ).update(
            status=status,
            detalhe=detalhe,
            concluida_em=timezone.now(),
            tokens_reservados=0,
            tokens_entrada=tokens_entrada,
            tokens_saida=tokens_saida,
            tokens_debitados=tokens_debitados,
        )
        if not encerrou:
            return False
        ConsumoMensalIA.objects.filter(pk=consumo.pk).update(
            tokens_reservados=F("tokens_reservados") - reserva,
            tokens_usados=F("tokens_usados") + tokens_debitados,
        )
        if status == RequisicaoIA.Status.SUCESSO and requisicao.origem == RequisicaoIA.Origem.ASSISTENTE:
            InteracaoAssistente.objects.create(
                usuario_id=requisicao.usuario_id,
                requisicao=requisicao,
                pergunta=pergunta,
                resposta=texto,
            )
    return True


@sensitive_variables()
def chamar_ia(usuario, mensagens, *, origem):
    """Envia mensagens de Chat Completions com cota, auditoria e tratamento de falhas."""
    configuracao = ConfiguracaoIA.atual()
    acesso = AcessoIA.objects.filter(usuario=usuario).first()
    mes = mes_atual()
    auditoria = {
        "usuario": usuario,
        "mes": mes,
        "origem": origem,
        "modelo": configuracao.modelo if configuracao else "",
    }

    def recusar(status, mensagem, codigo_http):
        RequisicaoIA.objects.create(
            **auditoria, status=status, detalhe=mensagem, concluida_em=timezone.now()
        )
        raise ErroIA(mensagem, codigo_http)

    teste_conexao = origem == RequisicaoIA.Origem.TESTE_CONEXAO
    if teste_conexao and not (usuario.is_active and usuario.is_superuser):
        recusar(RequisicaoIA.Status.BLOQUEADA, "Acesso administrativo necessário.", 403)
    if not teste_conexao and (not usuario.is_active or not acesso or not acesso.ativo):
        recusar(RequisicaoIA.Status.BLOQUEADA, "Seu acesso ao assistente está desativado.", 403)
    if (
        configuracao is None
        or not configuracao.modelo
        or not configuracao.chave_api
        or not endpoint_https_valido(configuracao.endpoint)
        or (not teste_conexao and not configuracao.ativo)
    ):
        recusar(RequisicaoIA.Status.ERRO, "A configuração da IA está indisponível.", 503)

    reconciliar_requisicoes_pendentes(usuario=usuario, mes=mes)
    limite_resposta = configuracao.limite_resposta_tokens
    if teste_conexao:
        limite_resposta = min(limite_resposta, 128)
    # Bytes de texto e margem para a formatação interna de Chat Completions.
    entrada_estimada = 128 + sum(
        len(mensagem["content"].encode("utf-8")) + 64 for mensagem in mensagens
    )
    reserva = entrada_estimada + limite_resposta
    consumo, _ = ConsumoMensalIA.objects.get_or_create(usuario=usuario, mes=mes)
    cota = cota_do_usuario(configuracao, acesso)

    with transaction.atomic():
        reservou = ConsumoMensalIA.objects.filter(
            pk=consumo.pk,
            tokens_reservados__lte=cota - reserva - F("tokens_usados"),
        ).update(tokens_reservados=F("tokens_reservados") + reserva)
        if reservou:
            requisicao = RequisicaoIA.objects.create(
                **auditoria, status=RequisicaoIA.Status.EM_ANDAMENTO, tokens_reservados=reserva
            )
    if not reservou:
        recusar(
            RequisicaoIA.Status.BLOQUEADA,
            "O saldo da sua cota mensal não cobre esta requisição.",
            429,
        )

    def concluir(status, detalhe="", **resultado):
        if not _concluir(consumo, requisicao, reserva, status, detalhe, **resultado):
            raise ErroIA("O prazo para concluir a requisição de IA foi excedido.", 504) from None

    try:
        dados = _enviar_ao_provedor(configuracao, mensagens, limite_resposta)
    except HTTPError as erro:
        erro.close()
        rejeitada = 400 <= erro.code < 500 and erro.code != 408
        mensagem = f"O provedor de IA retornou HTTP {erro.code}."
        concluir(
            RequisicaoIA.Status.ERRO, mensagem,
            tokens_debitados=0 if rejeitada else reserva,
        )
        raise ErroIA(mensagem, 502) from None
    except (OSError, HTTPException, ValueError, RecursionError):
        mensagem = "Não foi possível obter uma resposta válida do provedor de IA."
        concluir(
            RequisicaoIA.Status.ERRO, mensagem,
            tokens_debitados=reserva,
        )
        raise ErroIA(mensagem, 502) from None

    uso = dados.get("usage") if isinstance(dados, dict) else None
    uso = uso if isinstance(uso, dict) else {}
    entrada = _ler_tokens(uso, "prompt_tokens")
    saida = _ler_tokens(uso, "completion_tokens")
    total = _ler_tokens(uso, "total_tokens")
    if total is None and entrada is not None and saida is not None:
        total = entrada + saida
    tokens_debitados = total if total is not None else reserva
    detalhe_uso = ""
    if total is None:
        detalhe_uso = "O provedor não informou o total de tokens. Débito calculado pela reserva."
    elif total > reserva:
        detalhe_uso = "O total informado pelo provedor excedeu a reserva. Débito pelo consumo real."

    try:
        texto = dados["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        texto = None

    if isinstance(texto, str):
        # JSON pode conter NUL ou surrogates avulsos, rejeitados pelo PostgreSQL.
        texto = texto.replace("\0", "").encode("utf-8", errors="replace").decode("utf-8").strip()

    if not texto or not isinstance(texto, str):
        mensagem = "O provedor de IA não retornou uma resposta em texto."
        concluir(
            RequisicaoIA.Status.ERRO,
            f"{mensagem} {detalhe_uso}".strip(),
            tokens_entrada=entrada, tokens_saida=saida, tokens_debitados=tokens_debitados,
        )
        raise ErroIA(mensagem, 502)

    concluir(
        RequisicaoIA.Status.SUCESSO,
        detalhe=detalhe_uso,
        texto=texto,
        pergunta=mensagens[-1]["content"],
        tokens_entrada=entrada,
        tokens_saida=saida,
        tokens_debitados=tokens_debitados,
    )
    return texto

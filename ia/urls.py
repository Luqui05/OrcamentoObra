from django.urls import path

from .views import (
    AssistenteView,
    ConfiguracaoView,
    EditarAcessoView,
    EnviarMensagemView,
    IAPorUsuarioView,
    MeuConsumoView,
    RequisicoesView,
    TestarConexaoView,
)


app_name = "ia"

urlpatterns = [
    path("", AssistenteView.as_view(), name="assistente"),
    path("mensagem/", EnviarMensagemView.as_view(), name="enviar_mensagem"),
    path("meu-consumo/", MeuConsumoView.as_view(), name="meu_consumo"),
    path("requisicoes/", RequisicoesView.as_view(), name="requisicoes"),
    path("configuracao/", ConfiguracaoView.as_view(), name="configuracao"),
    path("configuracao/testar/", TestarConexaoView.as_view(), name="testar_conexao"),
    path("usuarios/", IAPorUsuarioView.as_view(), name="ia_por_usuario"),
    path("usuarios/<int:usuario_pk>/editar/", EditarAcessoView.as_view(), name="editar_acesso"),
]

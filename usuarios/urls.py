from django.contrib.auth import views as auth_views
from django.urls import path

from .views import CadastroUsuarioView

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("cadastro/", CadastroUsuarioView.as_view(), name="cadastro_usuario"),
]

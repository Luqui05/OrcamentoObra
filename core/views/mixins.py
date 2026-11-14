from braces.views import GroupRequiredMixin, LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from core.models import Obra
from usuarios.constants import CLIENTE_GROUP_NAME


class ClienteGroupRequiredMixin(GroupRequiredMixin):
    """Restringe as views do domínio aos usuários do grupo Clientes."""

    group_required = CLIENTE_GROUP_NAME
    raise_exception = True
    redirect_unauthenticated_users = True


class UserScopedQuerySetMixin:
    user_filter = None

    def get_user_filter(self):
        if self.user_filter is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} precisa definir user_filter."
            )
        return self.user_filter

    def get_queryset(self):
        queryset = super().get_queryset()
        user_filter = self.get_user_filter()

        if isinstance(user_filter, Q):
            return queryset.filter(user_filter).distinct()

        return queryset.filter(**{user_filter: self.request.user}).distinct()


def obras_do_usuario(usuario):
    return Obra.objects.filter(
        Q(cliente_principal__usuario=usuario) | Q(clientes__usuario=usuario)
    ).distinct()


def bloquear_obra_do_usuario(usuario, obra_pk):
    """Trava a obra antes de mutações em seus vínculos ou anexos."""
    obra = Obra.objects.select_for_update().filter(pk=obra_pk).first()
    if obra is None or not obras_do_usuario(usuario).filter(pk=obra_pk).exists():
        raise Http404
    return obra


class ObraContextMixin:
    def dispatch(self, request, *args, **kwargs):
        self.obra = get_object_or_404(
            obras_do_usuario(request.user), pk=kwargs["obra_pk"]
        )
        return super().dispatch(request, *args, **kwargs)

    def bloquear_obra(self):
        obra = bloquear_obra_do_usuario(self.request.user, self.obra.pk)
        self.obra = obra
        return obra


class ObraRelatedQuerySetMixin:
    def get_queryset(self):
        return super().get_queryset().filter(obra__in=obras_do_usuario(self.request.user))


class AutorQuerySetMixin:
    def get_queryset(self):
        return super().get_queryset().filter(cadastrado_por=self.request.user)


class FilteredListMixin:
    def get_queryset(self):
        self.filterset = self.filterset_class(
            data=self.request.GET, queryset=super().get_queryset()
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context

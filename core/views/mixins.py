from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q


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

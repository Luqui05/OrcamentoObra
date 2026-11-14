import django_filters
from django import forms

from core.models import Cliente, Obra


class ClienteFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        lookup_expr="icontains", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    ativo = django_filters.ChoiceFilter(
        choices=(("true", "Sim"), ("false", "Não")),
        widget=forms.Select(attrs={"class": "form-select"}),
        method="filter_ativo",
    )

    def filter_ativo(self, queryset, name, value):
        return queryset.filter(ativo=value == "true")

    class Meta:
        model = Cliente
        fields = ("nome", "ativo")


class ObraFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(
        label="Título",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    endereco = django_filters.CharFilter(
        label="Endereço",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Obra
        fields = ("titulo", "endereco")

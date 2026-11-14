from django import forms

from django.db.models import Q

from .models import (
    AtualizacaoObra,
    Cliente,
    ImagemObra,
    Obra,
    Orcamento,
    Documento,
)


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "cpf", "telefone", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ObraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)

        if usuario is not None:
            clientes = Q(usuario=usuario)
            principais = clientes
            if self.instance.pk:
                clientes = clientes | Q(pk__in=self.instance.clientes.values("pk"))
                principais = principais | Q(pk=self.instance.cliente_principal_id)
            self.fields["clientes"].queryset = Cliente.objects.filter(clientes)
            self.fields["cliente_principal"].queryset = Cliente.objects.filter(principais)

    class Meta:
        model = Obra
        fields = ["titulo", "descricao", "endereco", "clientes", "cliente_principal"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "clientes": forms.SelectMultiple(attrs={"class": "form-select"}),
            "cliente_principal": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cliente_principal = cleaned_data.get("cliente_principal")
        clientes = cleaned_data.get("clientes")

        if cliente_principal and clientes and cliente_principal not in clientes:
            self.add_error(
                "cliente_principal",
                "O cliente principal deve estar entre os clientes da obra.",
            )

        if self.instance.pk and cliente_principal and clientes is not None:
            usuarios_selecionados = {cliente.usuario_id for cliente in clientes}
            usuarios_selecionados.add(cliente_principal.usuario_id)
            usuarios_removidos = (
                Cliente.objects.filter(
                    Q(pk=self.instance.cliente_principal_id)
                    | Q(pk__in=self.instance.clientes.values("pk"))
                )
                .exclude(usuario_id__in=usuarios_selecionados)
                .values("usuario_id")
            )
            if (
                self.instance.documentos.filter(
                    cadastrado_por_id__in=usuarios_removidos
                ).exists()
                or self.instance.imagens.filter(
                    cadastrado_por_id__in=usuarios_removidos
                ).exists()
            ):
                self.add_error(
                    "clientes",
                    "Mantenha vinculados à obra os clientes que cadastraram documentos ou imagens.",
                )

        return cleaned_data


class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = ["versao", "descricao", "valor_total", "arquivo_pdf", "status"]
        widgets = {
            "versao": forms.NumberInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "valor_total": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "arquivo_pdf": forms.FileInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class AtualizacaoObraForm(forms.ModelForm):
    class Meta:
        model = AtualizacaoObra
        fields = ["titulo", "descricao", "semana_referencia"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "semana_referencia": forms.NumberInput(attrs={"class": "form-control"}),
        }

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ["titulo", "tipo_documento", "arquivo", "descricao"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_documento": forms.Select(attrs={"class": "form-select"}),
            "arquivo": forms.FileInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class ImagemObraForm(forms.ModelForm):
    atualizacao_obra = forms.ModelChoiceField(
        queryset=AtualizacaoObra.objects.none(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = ImagemObra
        fields = ["atualizacao_obra", "imagem", "legenda"]
        widgets = {
            "imagem": forms.FileInput(attrs={"class": "form-control"}),
            "legenda": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        obra = kwargs.pop("obra", None)
        super().__init__(*args, **kwargs)

        obra = obra or getattr(self.instance, "obra", None)
        self._obra = obra
        if obra:
            self.instance.obra = obra
            self.fields["atualizacao_obra"].queryset = AtualizacaoObra.objects.filter(
                obra=obra
            )

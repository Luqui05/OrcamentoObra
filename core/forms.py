from django import forms

from .models import (
    AtualizacaoObra,
    Cliente,
    ImagemObra,
    Obra,
    Orcamento,
)


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["usuario", "nome", "cpf", "telefone", "ativo"]
        widgets = {
            "usuario": forms.Select(attrs={"class": "form-select"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ObraForm(forms.ModelForm):
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

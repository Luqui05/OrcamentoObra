from django import forms

from .models import AcessoIA, ConfiguracaoIA
from .services import endpoint_https_valido


class ConfiguracaoIAForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoIA
        fields = (
            "ativo", "endpoint", "modelo", "chave_api", "cota_mensal_padrao",
            "limite_resposta_tokens",
        )
        widgets = {"chave_api": forms.PasswordInput()}
        help_texts = {
            "endpoint": "Informe a URL HTTPS completa do endpoint Chat Completions.",
            "cota_mensal_padrao": "Aplica-se às contas sem cota individual. Zero bloqueia chamadas.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chave_salva = self.instance.chave_api
        self.initial.pop("chave_api", None)
        if self.chave_salva:
            self.fields["chave_api"].required = False
            self.fields["chave_api"].help_text = "Deixe em branco para manter a chave salva."

    def clean_endpoint(self):
        endpoint = self.cleaned_data["endpoint"]
        if not endpoint_https_valido(endpoint):
            raise forms.ValidationError("Use uma URL HTTPS, sem credenciais nem fragmento.")
        return endpoint

    def clean_chave_api(self):
        return self.cleaned_data["chave_api"] or self.chave_salva


class AcessoIAForm(forms.ModelForm):
    class Meta:
        model = AcessoIA
        fields = ("ativo", "cota_mensal")
        help_texts = {
            "cota_mensal": "Deixe em branco para usar a cota padrão. Zero bloqueia chamadas."
        }


class PerguntaForm(forms.Form):
    pergunta = forms.CharField(
        label="Sua pergunta",
        max_length=2000,
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
    )

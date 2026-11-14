# Instruções para agentes

## Contexto e organização

- Leia `contexto_projeto.md` antes de alterar comportamento ou regras de negócio, quando esse arquivo estiver disponível.
- O projeto é Django 5.2.11. As configurações estão em `OrcamentoObra/`; as aplicações são `core` (domínio principal) e `usuarios` (cadastro e autenticação).
- Em `core`, modelos e formulários ficam em `models.py` e `forms.py`; as views são organizadas por domínio em `core/views/`, e as rotas em `core/urls.py`. Templates ficam em `core/templates/core/`. A aplicação `usuarios` mantém views, formulários, rotas e templates em seu próprio pacote.
- Migrações existentes ficam em `core/migrations/` e `usuarios/migrations/`. Arquivos enviados usam `MEDIA_ROOT` e funções `upload_to` nos modelos.
- Consulte a skill `.agents/skills/desenvolvimento-django/SKILL.md` para mudanças no código Django.

## Acesso e isolamento

- Endpoints do domínio principal combinam autenticação e associação ao grupo `Clientes`; examine os mixins e a view concreta antes de alterar a política.
- Os dados são relacionados a `Cliente.usuario`; obras são acessíveis pela relação do usuário com o cliente principal ou com os clientes associados. Recursos vinculados à obra herdam esse escopo.
- Ao implementar ou alterar leitura, escrita ou exclusão de dados, consulte `.agents/skills/revisao-seguranca-isolamento/SKILL.md`. Não trate filtros de interface como controle de acesso.

## Commits

- Use `.agents/skills/padrao-commit/SKILL.md` ao preparar uma mensagem de commit.

## Verificação

- Os testes Django estão em `core/tests.py` e `usuarios/tests.py`. Acrescente ou ajuste testes junto com mudanças comportamentais, sobretudo para acesso entre usuários.
- Quando apropriado, use os comandos padrão do Django pelo `manage.py`, por exemplo `python manage.py check` e `python manage.py test`. Não presuma que ambiente, dependências ou banco externo já estejam configurados.
- Informe com clareza quais verificações foram executadas e seus resultados; não declare sucesso sem evidência.

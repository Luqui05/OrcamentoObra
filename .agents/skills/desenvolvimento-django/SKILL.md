---
name: desenvolvimento-django
description: Use when changing models, forms, views, URLs, templates, migrations, or tests in this Django repository.
---

# Desenvolvimento Django neste repositório

## Antes de editar

1. Leia `contexto_projeto.md` para entender as regras de negócio disponíveis.
2. Localize o fluxo afetado: modelos e formulários em `core/`, views por domínio em `core/views/`, rotas em `core/urls.py` e templates em `core/templates/core/`; autenticação e cadastro ficam em `usuarios/`.
3. Confira os modelos e formulários associados antes de alterar uma view. Formulários `ModelForm` declaram explicitamente seus campos; views de criação frequentemente associam o objeto pai no servidor.

## Implementação

- Siga a organização existente por domínio e use CBVs quando estiver estendendo um fluxo que já as utiliza.
- Use nomes de rotas e `reverse_lazy` seguindo os padrões próximos. Não duplique validações de domínio sem verificar se já existem no formulário ou modelo.
- Mudanças em campos ou relações persistidos normalmente exigem uma migração Django em `core/migrations/` ou `usuarios/migrations/`, conforme a app proprietária.
- Uploads são armazenados sob `MEDIA_ROOT`; confirme o modelo, o `upload_to` e os formulários antes de alterar o fluxo de arquivos.
- Para comportamento que afeta acesso a registros, aplique também a skill `revisao-seguranca-isolamento`.

## Verificação

- Atualize os testes da app afetada em `core/tests.py` ou `usuarios/tests.py`; cubra comportamento e permissões relevantes.
- Use `python manage.py check` para as verificações do projeto e `python manage.py test` (ou o alvo específico apropriado) para os testes. A configuração local pode usar SQLite quando `DEBUG` está habilitado; com `DATABASE_URL`, o projeto espera PostgreSQL. Não assuma que o banco ou dependências estão disponíveis.
- Se não puder executar uma verificação, registre explicitamente essa limitação em vez de inferir que passou.

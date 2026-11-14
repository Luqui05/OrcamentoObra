---
name: revisao-seguranca-isolamento
description: Use when reviewing or changing authentication, authorization, querysets, object ownership, uploads, or user-visible data in this project.
---

# Revisão de segurança e isolamento por usuário

Revise cada caminho de acesso ao objeto no servidor. Login e pertencimento ao grupo são controles distintos do vínculo do registro com o usuário.

## Modelo de acesso observado

- As views de `core` usam `LoginRequiredMixin` e `ClienteGroupRequiredMixin`; este último exige o grupo `Clientes`.
- `Cliente.usuario` associa o cliente a `settings.AUTH_USER_MODEL`.
- Uma obra é relacionada ao usuário por `cliente_principal__usuario` ou `clientes__usuario`.
- Orçamentos, documentos, atualizações e imagens pertencem a uma obra. Ao consultar esses objetos, derive o escopo de acesso pelas relações com a obra.
- `UserScopedQuerySetMixin` filtra `get_queryset()` pelo usuário; para expressões `Q`, usa `distinct()`. Os mixins estão em `core/views/mixins.py`.

Esses são padrões do código existente, não uma afirmação de que todas as rotas ou caminhos de arquivo já estejam protegidos. Verifique a implementação concreta afetada.

## Checklist por operação

1. **Listar e detalhar:** limite o queryset no servidor ao usuário autenticado. Confirme que IDs fornecidos na URL não permitem buscar objetos de outro usuário; teste detalhe com objeto de outro usuário.
2. **Editar e excluir:** aplique o escopo também ao objeto carregado pela view (`get_queryset()` ou consulta equivalente). Não dependa de links ocultos, botões desabilitados ou validação somente no template.
3. **Criar e relacionar:** derive proprietário e objeto pai do `request.user` e de uma consulta já autorizada. Não aceite como confiáveis IDs de usuário, cliente, obra ou atualização submetidos pelo navegador.
4. **Formulários com relações:** restrinja as opções selecionáveis às entidades do escopo autorizado. Para relações aninhadas, garanta que pertençam ao mesmo objeto pai; valide no servidor.
5. **Arquivos e mídia:** autorize o registro antes de expor seus metadados ou links. Ao mexer em downloads ou uploads, confira também como o serviço de mídia é servido; `MEDIA_ROOT` e `MEDIA_URL` por si só não demonstram autorização por usuário.
6. **Rotas e métodos:** confira os métodos HTTP aceitos, proteção CSRF em operações mutáveis via formulários, redirecionamentos e comportamento para anônimo, usuário sem grupo e usuário sem vínculo.

## Evidência de revisão

- Para cada operação, verifique pelo menos um caso permitido e um acesso negado entre usuários distintos, incluindo acesso direto por URL/ID.
- Considere duplicação de resultados em relações muitos-para-muitos; mantenha `distinct()` quando a junção puder repetir registros.
- Amplie `core/tests.py` ou `usuarios/tests.py` conforme a app e a rota afetadas. Testes existentes cobrem redirecionamento de anônimo, acesso de membro do grupo e bloqueio de usuário sem grupo, mas não provam por si sós o isolamento de todos os recursos.
- Relate rotas, operações e cenários efetivamente revisados. Não declare isolamento completo a partir de inspeção de uma única view.

---
name: padrao-commit
description: Use when writing or revising a Git commit message for this repository.
---

# Padrão de mensagem de commit

Escreva mensagens curtas, em português, no formato observado no histórico recente:

```text
<tipo>: <descrição objetiva>
```

O histórico usa `feat:`; para manter a mensagem clara, use o tipo que descreve a mudança, como `feat` (funcionalidade), `fix` (correção), `docs` (documentação), `test` (testes), `refactor` (reestruturação sem mudança funcional) ou `chore` (manutenção).

Regras:

- Descreva uma única intenção por commit, começando com verbo no presente e em minúsculas após os dois-pontos.
- Prefira uma frase específica e concisa, sem ponto final. Exemplo: `docs: documenta o fluxo de acesso às obras`.
- Não diga que algo foi testado se isso não ocorreu; resultados de verificação pertencem ao corpo ou à descrição do trabalho, não substituem a mensagem de assunto.
- Se o assunto não explica a mudança sem contexto adicional, torne-o mais específico.

# OrcamentoObra

OrcamentoObra é um sistema acadêmico para gerenciar obras, clientes, orçamentos,
documentos, imagens e atualizações de andamento.

## Como navegar

- O painel inicial apresenta totais e atalhos para obras e clientes.
- Em **Obras**, localize a obra e selecione **Detalhar** para consultar as
  informações e os conteúdos vinculados à obra.
- Na página da obra, consulte seus orçamentos, documentos, atualizações e
  imagens. A galeria reúne os registros visuais da obra.
- Em **Clientes**, consulte seus cadastros. O cliente principal é responsável
  pela obra e pode haver outros clientes vinculados.
- O menu de conta permite entrar, sair e alterar a senha. A tela de entrada
  dá acesso ao cadastro e à recuperação de senha.

## Entidades da aplicação

- **Obra:** título, descrição, endereço, cliente principal e clientes associados.
- **Orçamento:** proposta vinculada à obra com versão, descrição, valor total,
  PDF e estado (pendente, aprovado ou recusado).
- **Documento:** arquivo vinculado à obra, classificado como projeto, orçamento,
  contrato, nota fiscal ou outro.
- **Atualização:** registro de andamento associado a uma obra e a uma semana
  de referência.
- **Imagem:** registro visual da obra, com legenda opcional e possibilidade de
  vínculo a uma atualização.

## Assistente e consumo

O assistente explica como usar a aplicação. A tela **Meu consumo** apresenta
a cota mensal, os tokens consumidos e o saldo para novas requisições. O acesso
e a cota podem ser administrados por usuário. A cota usa o mês civil, no fuso
horário da aplicação.

## Anexos existentes antes do controle de autoria

Documentos e imagens já cadastrados antes da migração de autoria permanecem
armazenados, mas ficam fora das telas e downloads dos clientes enquanto
`cadastrado_por` estiver vazio. Um superusuário pode atribuir o autor pelo Django
Admin somente quando houver evidência de quem cadastrou o arquivo; não deduza a
autoria apenas pelos clientes vinculados à obra, que pode ser compartilhada.

# QUALITY

Use este arquivo como checklist de qualidade antes de finalizar trabalho relevante.

## Checklist Geral

- A tarefa do usuario foi atendida.
- O escopo foi respeitado.
- Nenhum arquivo existente foi sobrescrito sem cuidado.
- A documentacao afetada foi atualizada.
- `SESSION.md` foi atualizado quando houve trabalho relevante.
- `DECISIONS.md` foi atualizado quando houve decisao importante.
- Tarefa concluida em `TASKS.md` recebeu evidencia de fechamento com procedimento e resultado.
- Tarefa que depende de resposta foi movida para "Aguardando Usuario", com pergunta, resposta e marcador bloqueada.
- `CONSENSUS.md` foi usado quando houve conflito, duvida relevante ou pedido de debate entre modelos. Cada entrada declara `Metodo`, `Exposicao previa a outras posicoes` e `Rodada`; achado tambem declara se escapou de verificacao.

## Checklist Para Estrutura Multiagente

- A raiz mantem apenas os arquivos Markdown de entrada dos agentes.
- `CLAUDE.md` aponta para `AGENTS.md` sem duplicar regras.
- `GEMINI.md` aponta para `AGENTS.md` sem duplicar regras.
- `AGENTS.md` proibe regras de produto, arquitetura ou processo nos arquivos-ponte.
- `AGENTS.md` define dois niveis de leitura (trivial vs relevante).
- `AGENTS.md` define regra de desempate (usuario > menor risco reversivel > parar e pedir humano).
- `AGENTS.md` aponta para `SESSION.md`, `MEMORY.md` e `CONSENSUS.md`.
- `SESSION.md` tem modelo pronto para novas sessoes com handover direcionado.
- `MEMORY.md` existe e descreve criterio de promocao, sobrescrita ativa e cuidado com dados sensiveis.
- `CONSENSUS.md` diferencia debate, consenso e decisao final, com `Status` e `Proximo passo`.
- `docs/archive/` existe com indice em `README.md` para a politica de rotacao.
- `PROMPTS.md` contem prompts reutilizaveis (quando existir).
- O bloco gerenciado de `AGENTS.md` esta integro (marcadores `ai-project-structure` presentes e pareados).

## Checklist De Atualizacao De Memoria

Atualize apenas o arquivo cuja funcao foi acionada na sessao:

- `SESSION.md` recebeu nova entrada quando houve trabalho cronologico relevante.
- `MEMORY.md` recebeu novo aprendizado quando havia algo util para sessoes futuras (criterio de promocao satisfeito).
- `MEMORY.md` nao contem dados sensiveis nem fatos efemeros.
- Pendencias acionaveis da sessao foram refletidas em `TASKS.md`.
- Tarefas novas receberam ID `T-NNN` unico (sem reutilizar IDs antigos).
- Specs afetadas tiveram o `Status` atualizado, e nenhuma tarefa teve status marcado dentro da spec (status vive so em `TASKS.md`).
- Nada foi preenchido por inferencia onde faltava contexto (regra "Nunca Inferir").
- `DECISIONS.md` recebeu decisao formal quando aplicavel.
- `CHANGELOG.md` registrou mudanca relevante na estrutura ou no produto.

## Testes E Validacao

Quando o projeto tiver codigo, registrar aqui:

- comandos de teste;
- comandos de lint;
- comandos de build;
- criterios manuais de aceitacao;
- cenarios que precisam ser verificados antes de finalizar.

## Criterios De Aceite

- A estrutura deve ser facil de entender por humanos e por IA.
- A memoria do projeto deve reduzir retrabalho entre sessoes.
- As regras centrais devem ficar em um unico lugar.
- O fluxo de consenso deve ser usado apenas quando agregar valor.

# PROMPTS

Prompts reutilizaveis para trabalhar com esta estrutura.

## Criar Ou Organizar Projeto Com Esta Estrutura

```md
Use esta estrutura multiagente ao criar ou organizar um projeto tocado por IA. Mantenha na raiz apenas AGENTS.md, CLAUDE.md e GEMINI.md. Coloque a memoria do projeto em docs/. Use AGENTS.md como fonte central, docs/SESSION.md para continuidade entre sessoes e docs/CONSENSUS.md quando modelos diferentes precisarem debater antes de uma decisao.
```

## Pedir Opiniao Ao Claude

```md
Claude, esta estrutura foi criada para manter projetos tocados por IA organizados, com uma fonte central de regras em AGENTS.md, memoria de sessoes em docs/SESSION.md e debate entre modelos em docs/CONSENSUS.md. Analise a estrutura e sugira melhorias se encontrar algo que possa deixar o fluxo mais claro, seguro ou facil de manter.
```

## Iniciar Nova Sessao De IA

```md
Leia AGENTS.md e depois consulte docs/SESSION.md, docs/PROJECT_CONTEXT.md, docs/TASKS.md e docs/QUALITY.md. Continue a partir do estado mais recente do projeto e registre no final da sessao o que foi feito, decisoes, pendencias e proximo passo.
```

## Solicitar Consenso Entre Modelos

```md
Use docs/CONSENSUS.md para registrar sua posicao sobre esta decisao. Inclua contexto, recomendacao, riscos, tradeoffs e o que voce considera necessario para chegar a um consenso com outros modelos.
```

## Revisao Antes De Finalizar

```md
Revise a mudanca usando docs/QUALITY.md. Verifique se a tarefa foi atendida, se o escopo foi respeitado, se a memoria da sessao precisa ser atualizada e se alguma decisao deve ir para docs/DECISIONS.md.
```


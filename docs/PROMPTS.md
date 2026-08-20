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

## Rodar Os Evals Da Skill Em Outra Ferramenta

Os evals de `docs/skills/ai-project-structure/evals/evals.json` precisam rodar nas tres ferramentas (Claude Code, Codex CLI, Gemini CLI) antes de uma versao da skill ser considerada validada. Os dois prompts abaixo cobrem Codex e Gemini.

Tres coisas mudam entre as ferramentas e ja estao ajustadas em cada prompt:

| | Codex CLI | Gemini CLI |
|---|---|---|
| Invocacao | `$ai-project-structure` ou `/skills` | ativa pela `description`, sem citar o nome |
| Skill instalada | `~/.agents/skills/ai-project-structure` | `~/.gemini/skills/ai-project-structure` |
| Diretorio de teste | `/tmp/skill-v2-tests-codex/` | `/tmp/skill-v2-tests-gemini/` |

Rode o Codex primeiro. Assim a ultima ferramenta encontra as outras duas ja registradas e consegue fechar a tarefa e a spec na mesma sessao.

Ao reaproveitar em versoes futuras, troque o numero da tarefa, o numero da spec e a linha de baseline pelos valores da rodada corrente.

### Codex CLI

```text
Invoque a skill $ai-project-structure.

Contexto: projeto /Users/adejaimejunioer/Dev/2026/ai-project-structure. Leia AGENTS.md, docs/SESSION.md (entrada de 2026-08-20 sobre T-002 e T-003), docs/TASKS.md e docs/specs/0001-skill-v2.md antes de comecar. Esta sessao fecha a parte Codex CLI da tarefa T-002.

Regras da sessao (valem para tudo):
- Nunca use o caractere travessao (em dash, U+2014) em nenhum texto.
- Nunca inicialize git, nem nos diretorios de teste.
- Nunca sobrescreva arquivo existente sem me perguntar.
- Trabalhe os testes em diretorios temporarios fora do repo (/tmp/skill-v2-tests-codex/), um subdiretorio limpo por eval.
- A skill instalada esta em ~/.agents/skills/ai-project-structure (fonte canonica em docs/skills/ai-project-structure/). Use a copia instalada, nao a fonte: o objetivo e testar o que esta instalado nesta ferramenta.

TAREFA (T-002): rodar os 7 evals de docs/skills/ai-project-structure/evals/evals.json nesta ferramenta.

Para cada eval, na ordem 1 a 7:
1. Crie um subdiretorio limpo (ex: /tmp/skill-v2-tests-codex/eval-01/). Para os evals 6 e 7, copie antes o fixture indicado no campo "files" (evals/fixtures/v1-project ou evals/fixtures/broken-project) para dentro do subdiretorio e trabalhe sobre a copia, nunca sobre o fixture original. Confira o hash do fixture antes e depois para provar que ficou intacto.
2. Execute o prompt do eval exatamente como esta no JSON, com o diretorio de trabalho no subdiretorio.
3. Compare o que aconteceu com o expected_output do eval. Cheque em especial: perguntas numeradas so quando falta resposta; nada criado antes das respostas no eval 4; marcadores ai-project-structure:core:start v2.0.0 presentes; docs/specs/ so quando pedido; assets/partials/ nunca copiado para o projeto; no eval 6, nada sobrescrito sem confirmacao e secao "Regra Local Do Time" preservada em "Regras Do Projeto"; no eval 7, validador acusando os 2 erros com exit 1.
4. Rode o validador no resultado: python3 ~/.agents/skills/ai-project-structure/scripts/validate_structure.py <subdiretorio>.
5. Registre veredito PASSOU ou FALHOU com a divergencia exata.

Referencia: no Claude Code os 7 evals passaram em 2026-08-20 (7/7), com validador exit 0 nos evals 1 a 6 e exit 1 com os 2 erros esperados no eval 7. Se algum eval falhar aqui, avalie primeiro se e diferenca de comportamento da ferramenta antes de concluir que e defeito da skill.

Se algum eval falhar por defeito da skill (nao do teste), pare, me mostre o problema e proponha a correcao na fonte canonica antes de continuar. Correcao aplicada exige rodar ./install.sh de novo e repetir o eval.

ENCERRAMENTO:
- Atualize docs/TASKS.md. T-002 so vai para Concluidas quando as tres ferramentas (Claude Code, Codex CLI, Gemini CLI) tiverem passado. Claude Code ja passou. Se o Gemini CLI ainda nao tiver rodado, mantenha T-002 em Em Andamento e atualize a nota dizendo quais ferramentas ja passaram.
- Se T-002 fechar (as tres ferramentas aprovadas), complete "Evidencia De Conclusao" da spec 0001-skill-v2 com os comandos executados e o resultado, e mude o Status para Concluida.
- Adicione entrada no docs/SESSION.md com os 7 headings e rode o validador no repo como checagem final. Espere 0 erros; os 4 avisos em entradas de 2026-04-25 sao historicos conhecidos.
- Relatorio final: tabela eval x veredito e o que ficou pendente.
- Me pergunte antes de apagar /tmp/skill-v2-tests-codex/.
```

### Gemini CLI

```text
Contexto: projeto /Users/adejaimejunioer/Dev/2026/ai-project-structure. Leia AGENTS.md, docs/SESSION.md (entrada de 2026-08-20 sobre T-002 e T-003), docs/TASKS.md e docs/specs/0001-skill-v2.md antes de comecar. Esta sessao fecha a parte Gemini CLI da tarefa T-002.

Regras da sessao (valem para tudo):
- Nunca use o caractere travessao (em dash, U+2014) em nenhum texto.
- Nunca inicialize git, nem nos diretorios de teste.
- Nunca sobrescreva arquivo existente sem me perguntar.
- Trabalhe os testes em diretorios temporarios fora do repo (/tmp/skill-v2-tests-gemini/), um subdiretorio limpo por eval.
- A skill instalada esta em ~/.gemini/skills/ai-project-structure (fonte canonica em docs/skills/ai-project-structure/). Use a copia instalada, nao a fonte: o objetivo e testar o que esta instalado nesta ferramenta.

TAREFA (T-002): rodar os 7 evals de docs/skills/ai-project-structure/evals/evals.json nesta ferramenta.

Para cada eval, na ordem 1 a 7:
1. Crie um subdiretorio limpo (ex: /tmp/skill-v2-tests-gemini/eval-01/). Para os evals 6 e 7, copie antes o fixture indicado no campo "files" (evals/fixtures/v1-project ou evals/fixtures/broken-project) para dentro do subdiretorio e trabalhe sobre a copia, nunca sobre o fixture original. Confira o hash do fixture antes e depois para provar que ficou intacto.
2. Execute o prompt do eval exatamente como esta no JSON, com o diretorio de trabalho no subdiretorio.
3. Compare o que aconteceu com o expected_output do eval. Cheque em especial: perguntas numeradas so quando falta resposta; nada criado antes das respostas no eval 4; marcadores ai-project-structure:core:start v2.0.0 presentes; docs/specs/ so quando pedido; assets/partials/ nunca copiado para o projeto; no eval 6, nada sobrescrito sem confirmacao e secao "Regra Local Do Time" preservada em "Regras Do Projeto"; no eval 7, validador acusando os 2 erros com exit 1.
4. Rode o validador no resultado: python3 ~/.gemini/skills/ai-project-structure/scripts/validate_structure.py <subdiretorio>.
5. Registre veredito PASSOU ou FALHOU com a divergencia exata.

Um teste extra vale aqui: a skill deve disparar sozinha, so pela description, sem eu citar o nome dela. Registre se isso aconteceu ou se foi preciso pedir explicitamente.

Referencia: no Claude Code os 7 evals passaram em 2026-08-20 (7/7), com validador exit 0 nos evals 1 a 6 e exit 1 com os 2 erros esperados no eval 7. Se algum eval falhar aqui, avalie primeiro se e diferenca de comportamento da ferramenta antes de concluir que e defeito da skill.

Se algum eval falhar por defeito da skill (nao do teste), pare, me mostre o problema e proponha a correcao na fonte canonica antes de continuar. Correcao aplicada exige rodar ./install.sh de novo e repetir o eval.

ENCERRAMENTO:
- Atualize docs/TASKS.md. T-002 so vai para Concluidas quando as tres ferramentas (Claude Code, Codex CLI, Gemini CLI) tiverem passado. Claude Code ja passou. Se esta for a ultima ferramenta e tudo passou, mova T-002 para Concluidas com a data; senao, atualize a nota dizendo quais ferramentas ja passaram.
- Se T-002 fechar (as tres ferramentas aprovadas), complete "Evidencia De Conclusao" da spec 0001-skill-v2 com os comandos executados e o resultado, e mude o Status para Concluida.
- Adicione entrada no docs/SESSION.md com os 7 headings e rode o validador no repo como checagem final. Espere 0 erros; os 4 avisos em entradas de 2026-04-25 sao historicos conhecidos.
- Relatorio final: tabela eval x veredito e o que ficou pendente.
- Me pergunte antes de apagar /tmp/skill-v2-tests-gemini/.
```


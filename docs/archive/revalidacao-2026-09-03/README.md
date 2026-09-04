# Revalidacao adversarial da skill 2.5.1, 2026-09-03

Material bruto da rodada registrada em `docs/CONSENSUS.md` como REVAL-1 a REVAL-7 (REVAL-5 esta em `CONSENSUS-2026.md`). Cada arquivo e a saida integral do agente ou do teste, com uma unica transformacao: todo travessao (U+2014) virou hifen simples, porque o verificador do repositorio reprova o caractere em qualquer arquivo versionado. A contagem por arquivo esta abaixo; nada mais foi editado. Os prompts sao os enviados.

Modelo por superficie (todos cegos, num worktree com o corpo das entradas contemporaneas de `CONSENSUS.md` retirado e nota no lugar):

| Superficie | Ataque | Comando | Verificou |
|---|---|---|---|
| 1 core | Grok 4.6 | `cursor-agent -p --mode ask --force --model cursor-grok-4.6-xhigh` | Claude no codigo |
| 2 validador | Codex GPT-5.6 sol | `codex exec -s read-only -m gpt-5.6-sol -c model_reasoning_effort="xhigh"` | Claude no codigo |
| 3 loop | Gemini 3.7 Flash | `cursor-agent -p --mode ask --force --model gemini-3.7-flash-high` | Claude com agente falso |
| 4 evals | Claude executou 24 mutacoes; Codex previu (mesmo perfil da 2) | ver `mutacoes-*.txt` | previsao contra execucao, nos dois sentidos |
| 5 fluxos | Claude Opus 5 pela skill instalada | `claude -p --permission-mode bypassPermissions --model opus --effort high` | Claude por diff contra assets |
| 6 templates | Grok 4.6 | mesmo perfil da 1 | Claude no template |
| 7 distribuicao | Codex morreu na cota (312k tokens); GPT-5.6 sol via cursor | `cursor-agent -p --mode ask --force --model gpt-5.6-sol-high` | Claude em HOME falso |

Kimi, GLM e Gemini 3.8 nao existiam mais no catalogo do `cursor-agent` nesta data.

Acrescentados em 2026-09-04: o log da rodada de loop que fechou T-065 com Codex `gpt-5.6-terra`, e a rodada 3 de mutacoes que prova o portao novo; depois, as duas rodadas de loop de T-069 (a primeira parou com pergunta, a segunda fechou e publicou a 2.6.0), e a rodada de T-070 (2.7.0, verde de primeira), e as de T-072 e T-071 (2.8.0).

## Arquivos

| Arquivo | Bytes originais | Travessoes trocados |
|---|---|---|
| `posicao-selada-claude.md` | 6361 | 0 |
| `prompt-s1-grok.md` | 4416 | 0 |
| `prompt-s2-codex.md` | 4530 | 0 |
| `prompt-s3-gemini.md` | 5235 | 0 |
| `prompt-s4-codex-mutacoes.md` | 4734 | 0 |
| `prompt-s6-grok.md` | 5063 | 0 |
| `prompt-s7-codex.md` | 5082 | 0 |
| `s1-grok-4.6-xhigh.md` | 20778 | 0 |
| `s2-codex-gpt-5.6-sol-xhigh.md` | 14753 | 0 |
| `s3-gemini-3.7-flash.md` | 14956 | 0 |
| `s4-codex-gpt-5.6-sol-xhigh.md` | 21744 | 0 |
| `s6-grok-4.6-xhigh.md` | 17777 | 0 |
| `s7-gpt-5.6-sol-high-cursor.md` | 7386 | 0 |
| `s5-claude-opus-scaffold.txt` | 1004 | 0 |
| `s5-claude-opus-atualizacao.txt` | 2137 | 5 |
| `s5-claude-opus-spec.txt` | 1172 | 1 |
| `s5-claude-opus-loop-ativacao.txt` | 1125 | 0 |
| `mutacoes-claude.txt` | 3962 | 0 |
| `mutacoes-claude-rodada2.txt` | 1675 | 0 |
| `s1-claude-verifica-grok.txt` | 510 | 0 |
| `s2-claude-falsos-negativos.txt` | 1856 | 0 |
| `s2-claude-verifica-codex.txt` | 801 | 0 |
| `s3-claude-hostil.txt` | 2629 | 0 |
| `s3-claude-verifica-gemini.txt` | 864 | 0 |
| `s6-claude-dia-seguinte.txt` | 552 | 0 |
| `s7-claude-install.txt` | 5339 | 0 |
| `s7-codex-morreu-na-cota.txt` | 0 | 0 |
| `loop-t065-codex-terra.txt` | 739141 | 0 |
| `mutacoes-claude-rodada3.txt` | 2696 | 0 |
| `loop-t069-codex-terra-rodada1.txt` | 316255 | 0 |
| `loop-t069-codex-terra-rodada2.txt` | 722706 | 0 |
| `loop-t070-codex-terra.txt` | 1219602 | 0 |
| `loop-t072-codex-terra.txt` | 477909 | 0 |
| `loop-t071-codex-terra.txt` | 322496 | 0 |

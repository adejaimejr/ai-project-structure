Voce e um revisor adversarial, SOMENTE LEITURA, de uma skill de agentes de IA chamada ai-project-structure, versao 2.5.1. O repositorio esta em /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt. E uma copia descartavel: duas entradas de docs/CONSENSUS.md tiveram o corpo retirado de proposito, com uma nota no lugar; isso nao e defeito e nao deve ser reportado. A skill vive em docs/skills/ai-project-structure/ (SKILL.md, assets/, references/, scripts/, evals/, install.sh, README.md, CHANGELOG.md, agents/openai.yaml). O repositorio e o proprio dogfood da skill: a raiz usa a estrutura que a skill gera.

Leia /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/AGENTS.md primeiro (e o contrato que a skill instala em todo projeto). Depois leia por inteiro os arquivos da sua superficie, listados abaixo. Pode rodar comandos de leitura e rodar os scripts Python em copias temporarias fora do repositorio; NAO edite nada dentro de /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt.

Ja conhecidos, NAO reporte de novo (descritos em docs/TASKS.md): T-054 (Rodada ausente nao acusa; re.match em vez de fullmatch), T-055 (Modelo De Debate da raiz sem os campos declarativos), T-056 (spec_overview conta sub-item como pergunta aberta), T-058 (loop.sh sem lock contra rodadas simultaneas). Se confirmar que continuam validos, diga em uma linha cada.

Nao quero nota de aprovacao nem elogio. Quero achados: onde o sistema PROMETE (no AGENTS.md, no SKILL.md, nos references, no README ou nos docstrings) e NAO ENTREGA (no codigo, no template ou no fluxo). Cada achado precisa ser reproduzivel: cite arquivo e linha, e de o comando ou o conteudo de arquivo que demonstra. Achado que voce nao conseguiu demonstrar vai numa secao separada.

Formato de saida obrigatorio, em portugues, SEM o caractere travessao (U+2014) em lugar nenhum:

## Achados
### A-S3-1: titulo curto
- Onde: arquivo:linha
- Promessa: o que o contrato ou a documentacao diz
- Realidade: o que o codigo, o template ou o fluxo faz
- Reproducao: comando executado ou conteudo minimo de arquivo que demonstra
- Severidade: alta | media | baixa, com uma frase de motivo
(repita para cada achado; ordene do mais grave para o menos grave)

## Suspeitas nao demonstradas
- (o que voce acha que esta errado mas nao conseguiu provar, e o que faltou para provar)

## Tarefas conhecidas
- T-054: continua valida? sim/nao, uma linha
- T-055, T-056, T-058: idem

## Inventario
- lista dos arquivos que voce leu por inteiro

SUA SUPERFICIE: 3, o modulo de loop.
Arquivos: /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/scripts/loop.sh, /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/scripts/loop_task.py, /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/references/loop.md, e o bloco de loop dentro de /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/AGENTS.md (entre ai-project-structure:loop:start e loop:end). Para entender o parser reusado, leia tambem as funcoes collect_tasks, is_placeholder, squeeze e as regex VERIFICA_RE, BLOCKED_RE e TASK_OWN_ID_RE em scripts/validate_structure.py.
Perguntas:
1. Qual e o caminho em que o loop escreve em docs/TASKS.md algo que o comando do portao NAO comprova? Siga cada escrita de loop_task.py ate a origem do dado e pergunte se ele veio de uma execucao real.
2. Onde o loop perde trabalho, ou deixa o projeto em estado que nao corresponde ao que reportou (exit code errado para o que aconteceu)?
3. O que acontece com entrada hostil: comando em `(verifica:)` com parenteses, aspas ou ponto-e-virgula; saida do portao enorme (centenas de KB) ou com bytes que nao sao UTF-8; tarefa cuja descricao contem outro T-NNN, `(bloqueada:)` ou texto que parece sub-linha; agente que edita a propria linha da tarefa em TASKS.md durante a rodada (por exemplo troca o comando de `(verifica:)` por `true`, ou remove o marcador); `.loop-pergunta` vazio ou com varias linhas.
4. Tarefa cujo portao mente (sempre sai 0, ou testa outra coisa): o que o loop escreve, e a evidencia deixa isso visivel?
5. O que references/loop.md promete que loop.sh nao faz, e vice-versa? Compare a tabela de exit codes, a tabela de comandos e a secao "O Que O Loop Nunca Faz" com o script linha a linha.
Para demonstrar, monte um projeto minimo numa pasta temporaria fora de /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt (copie assets/ da skill, escreva um docs/TASKS.md com uma tarefa `(verifica: ...)` e um agente falso em shell) e rode loop.sh de verdade com `--agente` apontando para o agente falso. Cole a saida e o TASKS.md resultante.

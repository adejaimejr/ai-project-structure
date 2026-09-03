Voce e um revisor adversarial, SOMENTE LEITURA, de uma skill de agentes de IA chamada ai-project-structure, versao 2.5.1. O repositorio esta em /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt. E uma copia descartavel: duas entradas de docs/CONSENSUS.md tiveram o corpo retirado de proposito, com uma nota no lugar; isso nao e defeito e nao deve ser reportado. A skill vive em docs/skills/ai-project-structure/ (SKILL.md, assets/, references/, scripts/, evals/, install.sh, README.md, CHANGELOG.md, agents/openai.yaml). O repositorio e o proprio dogfood da skill: a raiz usa a estrutura que a skill gera.

Leia /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/AGENTS.md primeiro (e o contrato que a skill instala em todo projeto). Depois leia por inteiro os arquivos da sua superficie, listados abaixo. Pode rodar comandos de leitura e rodar os scripts Python em copias temporarias fora do repositorio; NAO edite nada dentro de /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt.

Ja conhecidos, NAO reporte de novo (descritos em docs/TASKS.md): T-054 (Rodada ausente nao acusa; re.match em vez de fullmatch), T-055 (Modelo De Debate da raiz sem os campos declarativos), T-056 (spec_overview conta sub-item como pergunta aberta), T-058 (loop.sh sem lock contra rodadas simultaneas). Se confirmar que continuam validos, diga em uma linha cada.

Nao quero nota de aprovacao nem elogio. Quero achados: onde o sistema PROMETE (no AGENTS.md, no SKILL.md, nos references, no README ou nos docstrings) e NAO ENTREGA (no codigo, no template ou no fluxo). Cada achado precisa ser reproduzivel: cite arquivo e linha, e de o comando ou o conteudo de arquivo que demonstra. Achado que voce nao conseguiu demonstrar vai numa secao separada.

Formato de saida obrigatorio, em portugues, SEM o caractere travessao (U+2014) em lugar nenhum:

## Achados
### A-S7-1: titulo curto
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

SUA SUPERFICIE: 7, a distribuicao: /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/install.sh, agents/openai.yaml, README.md (da skill, nao o da raiz) e CHANGELOG.md (da skill). Leia tambem SKILL.md e evals/verify_repository.py (funcao verificar_install) para saber o que e prometido sobre a instalacao.
Perguntas:
1. O install.sh e idempotente de verdade? Rode-o de verdade com HOME apontando para uma pasta temporaria fora de /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt (export HOME=<tmp>; bash install.sh) duas vezes e compare as arvores. Depois teste: instalacao parcial (interrompa ou simule falha no meio, por exemplo removendo permissao de escrita de um subdiretorio do destino), destino ja existente e DIFERENTE (edite um arquivo no destino e um arquivo extra que nao existe na fonte, reinstale, veja o que sobra e o que some), `--uninstall` com e sem `--project`, `--project` em pasta sem git, e argumentos combinados (`--uninstall --claude`, `--all --project`). Cole comandos e saidas.
2. O que ele NAO distribui esta certo? Compare a lista NAO_DISTRIBUIDO do verify_repository.py, o comentario do install.sh, e o que o README diz; confira se __pycache__ vai junto.
3. agents/openai.yaml declara allow_implicit_invocation: true. O que o Codex CLI 0.152.1 instalado nesta maquina faz com isso? Confira em `codex --help`, `codex skills --help` se existir, nas strings do binario (`strings $(readlink -f $(command -v codex))` pode ser um wrapper node; o binario real fica em node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex) e em ~/.codex/ se houver documentacao ou cache. Diga o que conseguiu confirmar e o que nao.
4. O README.md da skill descreve o que o codigo faz hoje, ou envelheceu? Confira item a item: arvore de conteudo do pacote, lista de fixtures, secao "Instalacao manual" (o que ela copia e o que a skill precisa para funcionar), lista de checks do validador contra CODIGOS, exit codes, flags, versao citada. O mesmo para o CHANGELOG: alguma entrada descreve comportamento que o codigo atual nao tem?
5. Onde a versao 2.5.1 aparece escrita em prosa (fora do frontmatter, dos marcadores e do heading do CHANGELOG) e quem confere?

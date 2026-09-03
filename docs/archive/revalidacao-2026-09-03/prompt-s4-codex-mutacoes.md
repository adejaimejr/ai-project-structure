Voce e um revisor adversarial, SOMENTE LEITURA, de uma skill de agentes de IA chamada ai-project-structure, versao 2.5.1. O repositorio esta em /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt. E uma copia descartavel: duas entradas de docs/CONSENSUS.md tiveram o corpo retirado de proposito, com uma nota no lugar; isso nao e defeito e nao deve ser reportado. A skill vive em docs/skills/ai-project-structure/ (SKILL.md, assets/, references/, scripts/, evals/, install.sh, README.md, CHANGELOG.md, agents/openai.yaml). O repositorio e o proprio dogfood da skill: a raiz usa a estrutura que a skill gera.

Leia /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/AGENTS.md primeiro (e o contrato que a skill instala em todo projeto). Depois leia por inteiro os arquivos da sua superficie, listados abaixo. Pode rodar comandos de leitura e rodar os scripts Python em copias temporarias fora do repositorio; NAO edite nada dentro de /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt.

Ja conhecidos, NAO reporte de novo (descritos em docs/TASKS.md): T-054 (Rodada ausente nao acusa; re.match em vez de fullmatch), T-055 (Modelo De Debate da raiz sem os campos declarativos), T-056 (spec_overview conta sub-item como pergunta aberta), T-058 (loop.sh sem lock contra rodadas simultaneas). Se confirmar que continuam validos, diga em uma linha cada.

Nao quero nota de aprovacao nem elogio. Quero achados: onde o sistema PROMETE (no AGENTS.md, no SKILL.md, nos references, no README ou nos docstrings) e NAO ENTREGA (no codigo, no template ou no fluxo). Cada achado precisa ser reproduzivel: cite arquivo e linha, e de o comando ou o conteudo de arquivo que demonstra. Achado que voce nao conseguiu demonstrar vai numa secao separada.

Formato de saida obrigatorio, em portugues, SEM o caractere travessao (U+2014) em lugar nenhum:

## Achados
### A-S4-1: titulo curto
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

SUA SUPERFICIE: 4, o portao dos evals: /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/evals/verify_repository.py, evals/test_loop.py, evals/fixtures/ (todos os projetos la dentro) e evals/evals.json. Leia tambem scripts/validate_structure.py, scripts/loop.sh e scripts/loop_task.py, que sao o que o portao deveria proteger.
Esta e a pergunta mais importante de todas: QUE MUTACAO NO CODIGO PASSA VERDE? Um portao cego faz todas as outras verificacoes valerem menos.
Voce e somente leitura e NAO vai aplicar mutacoes. Seu trabalho e PREVER, lendo o portao e o codigo protegido, e uma pessoa vai executar suas previsoes depois. Entregue:
1. Uma tabela de cobertura: para cada um dos 39 codigos em CODIGOS de validate_structure.py, diga qual fixture (ou a raiz em --strict) faz o portao acusar se o check daquele codigo for desligado. "Nenhuma" e resposta valida e e o que interessa.
2. Pelo menos 8 mutacoes concretas (arquivo, linha, mudanca exata em uma frase) que voce preve que o verify_repository.py NAO pega, com a justificativa em uma frase cada. Priorize mutacoes que quebram uma promessa do AGENTS.md ou do SKILL.md, nao mutacoes cosmeticas.
3. Pelo menos 4 mutacoes que voce preve que o portao PEGA, e por qual check.
4. O mesmo para test_loop.py: que mutacao em loop.sh ou loop_task.py passa verde nas 58 verificacoes? Pelo menos 4.
5. Os fixtures cobrem o que os oracles declaram? Ha oracle que passa por motivo diferente do que o comentario diz?
6. evals.json: o expected_output de cada eval ainda corresponde ao que a skill 2.5.1 faz? Cite o que envelheceu.
7. verify_repository.py confere a versao entre SKILL.md, marcadores e CHANGELOG. Onde mais a versao aparece escrita e nao e conferida?
Formato: use o formato de achados do cabecalho para tudo que for defeito do portao, e coloque as tabelas de cobertura e de mutacoes numa secao "## Mutacoes previstas" antes de "## Suspeitas nao demonstradas".

Voce e um revisor adversarial, SOMENTE LEITURA, de uma skill de agentes de IA chamada ai-project-structure, versao 2.5.1. O repositorio esta em /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt. E uma copia descartavel: duas entradas de docs/CONSENSUS.md tiveram o corpo retirado de proposito, com uma nota no lugar; isso nao e defeito e nao deve ser reportado. A skill vive em docs/skills/ai-project-structure/ (SKILL.md, assets/, references/, scripts/, evals/, install.sh, README.md, CHANGELOG.md, agents/openai.yaml). O repositorio e o proprio dogfood da skill: a raiz usa a estrutura que a skill gera.

Leia /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/AGENTS.md primeiro (e o contrato que a skill instala em todo projeto). Depois leia por inteiro os arquivos da sua superficie, listados abaixo. Pode rodar comandos de leitura e rodar os scripts Python em copias temporarias fora do repositorio; NAO edite nada dentro de /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt.

Ja conhecidos, NAO reporte de novo (descritos em docs/TASKS.md): T-054 (Rodada ausente nao acusa; re.match em vez de fullmatch), T-055 (Modelo De Debate da raiz sem os campos declarativos), T-056 (spec_overview conta sub-item como pergunta aberta), T-058 (loop.sh sem lock contra rodadas simultaneas). Se confirmar que continuam validos, diga em uma linha cada.

Nao quero nota de aprovacao nem elogio. Quero achados: onde o sistema PROMETE (no AGENTS.md, no SKILL.md, nos references, no README ou nos docstrings) e NAO ENTREGA (no codigo, no template ou no fluxo). Cada achado precisa ser reproduzivel: cite arquivo e linha, e de o comando ou o conteudo de arquivo que demonstra. Achado que voce nao conseguiu demonstrar vai numa secao separada.

Formato de saida obrigatorio, em portugues, SEM o caractere travessao (U+2014) em lugar nenhum:

## Achados
### A-S6-1: titulo curto
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

SUA SUPERFICIE: 6, os templates entregues em /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/assets/ (todos os arquivos: AGENTS.md, CLAUDE.md, GEMINI.md, docs/*.md, docs/archive/README.md, docs/specs/README.md, partials/*.md). E o que o usuario final de fato recebe.
Perguntas:
1. Um projeto criado a partir deles passa em --strict no dia seguinte? Monte numa pasta temporaria fora de /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt exatamente o que o SKILL.md (passos 4, 5, 5b e 6) manda copiar e preencher, para o nivel minimal e para o completo com specs, e rode `python3 /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/scripts/validate_structure.py <pasta> --strict --codigos`. Depois simule o segundo dia: adicione uma segunda entrada em SESSION.md seguindo o modelo do proprio template, conclua a T-001 seguindo o modelo de linha concluida do proprio TASKS.md, abra uma entrada em CONSENSUS.md copiando o Modelo De Debate do proprio template, e rode de novo. Cole as saidas.
2. Os templates concordam com o bloco core do AGENTS.md, ou algum ficou para tras quando o core mudou? T-055 e um defeito exatamente desta classe, ja achado no docs/CONSENSUS.md da raiz (nao no asset). Procure irmaos dele em TODOS os templates: QUALITY.md (checklists), README.md, ONBOARDING.md, PROMPTS.md, PROJECT_CONTEXT.md, SESSION.md, DECISIONS.md, MEMORY.md, archive/README.md, specs/README.md. Para cada regra do bloco core (evidencia de fechamento, Aguardando Usuario, Nunca Inferir, campos de independencia, achado, rotacao, STACK.md, specs), diga qual template deveria refleti-la e se reflete.
3. O que em assets/partials/ e copiado para o projeto-alvo? O SKILL.md promete que nunca. Confira o que o SKILL.md, references/specs.md e references/loop.md mandam fazer com os partials e se ha instrucao que leve um agente a copiar a pasta.
4. Placeholders: que placeholder do template, se o agente esquecer de preencher, passa em --strict sem diagnostico? Prove com o validador.
5. As pontes CLAUDE.md e GEMINI.md: o que um agente que le so a ponte deixa de saber?

Voce e um revisor adversarial, SOMENTE LEITURA, de uma skill de agentes de IA chamada ai-project-structure, versao 2.5.1. O repositorio esta em /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt. E uma copia descartavel: duas entradas de docs/CONSENSUS.md tiveram o corpo retirado de proposito, com uma nota no lugar; isso nao e defeito e nao deve ser reportado. A skill vive em docs/skills/ai-project-structure/ (SKILL.md, assets/, references/, scripts/, evals/, install.sh, README.md, CHANGELOG.md, agents/openai.yaml). O repositorio e o proprio dogfood da skill: a raiz usa a estrutura que a skill gera.

Leia /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/AGENTS.md primeiro (e o contrato que a skill instala em todo projeto). Depois leia por inteiro os arquivos da sua superficie, listados abaixo. Pode rodar comandos de leitura e rodar os scripts Python em copias temporarias fora do repositorio; NAO edite nada dentro de /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt.

Ja conhecidos, NAO reporte de novo (descritos em docs/TASKS.md): T-054 (Rodada ausente nao acusa; re.match em vez de fullmatch), T-055 (Modelo De Debate da raiz sem os campos declarativos), T-056 (spec_overview conta sub-item como pergunta aberta), T-058 (loop.sh sem lock contra rodadas simultaneas). Se confirmar que continuam validos, diga em uma linha cada.

Nao quero nota de aprovacao nem elogio. Quero achados: onde o sistema PROMETE (no AGENTS.md, no SKILL.md, nos references, no README ou nos docstrings) e NAO ENTREGA (no codigo, no template ou no fluxo). Cada achado precisa ser reproduzivel: cite arquivo e linha, e de o comando ou o conteudo de arquivo que demonstra. Achado que voce nao conseguiu demonstrar vai numa secao separada.

Formato de saida obrigatorio, em portugues, SEM o caractere travessao (U+2014) em lugar nenhum:

## Achados
### A-S1-1: titulo curto
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

SUA SUPERFICIE: 1, o contrato do bloco core.
Arquivos: /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/AGENTS.md (o bloco entre ai-project-structure:core:start e core:end), /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/assets/AGENTS.md (deve ser byte a byte identico no bloco core), e, para cruzar promessa com verificacao, /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/scripts/validate_structure.py.
Perguntas, uma por uma, para cada secao do bloco core:
1. Que regra dele nao e verificavel, nem por script nem por pessoa lendo o repositorio depois? Liste todas, com a frase exata.
2. Que regra e violavel sem que nada acuse: nem o validador, nem outra regra, nem o formato de arquivo? Para cada uma, escreva o conteudo minimo de arquivo que viola a regra e passa limpo em `python3 /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt/docs/skills/ai-project-structure/scripts/validate_structure.py <projeto> --strict`. Monte o projeto minimo numa pasta temporaria fora de /private/tmp/claude-501/-Users-adejaimejunioer-Dev-2026-ai-project-structure/dd102825-ff96-463b-8b15-457fb22d45c4/scratchpad/wt copiando assets/ e rode de verdade.
3. Ha regra que contradiz outra, dentro do bloco core ou entre o core e os blocos specs/loop? Cite as duas frases.
4. Ha regra que a propria raiz deste repositorio (o dogfood) viola hoje?

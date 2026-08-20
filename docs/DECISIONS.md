# DECISIONS

Registro de decisoes importantes do projeto.

## Modelo

```md
## AAAA-MM-DD - Titulo da decisao

### Decisao

- 

### Motivo

- 

### Impacto

- 
```

## 2026-04-25 - Estrutura multiagente com raiz minima

### Decisao

- Manter na raiz apenas os arquivos Markdown de entrada dos agentes: `AGENTS.md`, `CLAUDE.md` e `GEMINI.md`.
- Colocar a memoria do projeto dentro de `docs/`.
- Usar `AGENTS.md` como fonte central de instrucoes.
- Usar `SESSION.md` para continuidade entre sessoes.
- Usar `CONSENSUS.md` para debate entre modelos quando necessario.

### Motivo

- Evitar duplicacao de regras entre agentes.
- Facilitar continuidade entre sessoes de IA.
- Manter a raiz limpa e previsivel.
- Permitir que modelos diferentes opinem antes de decisoes importantes.

### Impacto

- Claude Code e Gemini passam a usar arquivos-ponte.
- Novos agentes devem ler `AGENTS.md`.
- Mudancas importantes precisam atualizar a memoria do projeto.

## 2026-04-25 - Evolucao da estrutura: MEMORY.md e oito melhorias

### Decisao

- Adicionado `docs/MEMORY.md` como memoria persistente em quatro tipos (User / Feedback / Project / Reference), com criterio de promocao e sobrescrita ativa.
- Adicionado `docs/archive/` com indice em `README.md` para rotacao de `SESSION.md` e `CONSENSUS.md`.
- `AGENTS.md` reescrito definindo: imutabilidade dos arquivos-ponte, dois niveis de leitura (trivial vs relevante), regra de desempate (usuario > menor risco reversivel > parar e pedir humano), atualizacao por gatilho, criterio de "onde escrever cada coisa", politica de rotacao, e que `CONSENSUS.md` so e para duvidas reais.
- Template de `SESSION.md` atualizado com handover direcionado (agente sugerido + motivo) e secao de "Aprendizados Para MEMORY.md".
- Template de `CONSENSUS.md` atualizado com `Status` (aberto | resolvido | arquivado) e `Proximo passo` quando aberto.
- `QUALITY.md` recebeu checklist de atualizacao por gatilho e de cuidados com `MEMORY.md`.
- Skill `ai-project-structure` sincronizada com a estrutura nova.

### Motivo

- Tri-consenso entre Claude, Gemini e Codex em `docs/CONSENSUS.md` (entrada `2026-04-25 - Adicao de MEMORY.md e detalhamento das melhorias`).
- Cobrir lacuna de "o que o projeto aprendeu" sem inflar `SESSION.md` ou `DECISIONS.md`.
- Reduzir overhead de leitura/atualizacao em mudancas triviais.
- Garantir que a estrutura nao colapse por baixa adocao operacional.

### Impacto

- Novos projetos criados pela skill ja nascem com a versao nova.
- Agentes precisam ler `MEMORY.md` em mudancas relevantes.
- Pendencias de sessao acionaveis devem virar tasks em `TASKS.md` antes de fechar a sessao.
- `CONSENSUS.md` ganha ciclo de vida (aberto / resolvido / arquivado) e regra de desempate explicita.
- `SESSION.md` e `CONSENSUS.md` passam a rotacionar para `docs/archive/` quando crescerem.

## 2026-08-20 - Skill v2.0.0: emprestimos do specsfy sem a cerimonia

### Decisao

- Evoluir a skill para 2.0.0 importando do specsfy (github.com/promovaweb/specsfy): entrevista numerada com opcoes numeradas ("Avançar" adia e nunca autoriza inferir), regra "Nunca Inferir" no `AGENTS.md`, `TASKS.md` com IDs `T-NNN`, blocos gerenciados com versao (`ai-project-structure:core`/`:specs`), validador executavel com exit code, e modulo opcional de specs leve (`docs/specs/`, arquivos `NNNN-slug.md` com campo `Status`).
- NAO importar: pipeline multi-skill numerado, minimo de 3 criterios/testes por requisito, sistema de attestation, CLI/TUI, monitor de contexto bloqueante.
- Anti-drift: `TASKS.md` e a unica fonte de status de tarefa; specs listam apenas T-IDs.
- Validador roda do diretorio da skill instalada (nao e copiado ao projeto) e usa apenas biblioteca padrao do Python 3.
- Proibir o caractere travessao (em dash, U+2014) em todos os textos do projeto e do core da skill; o validador acusa ocorrencias como erro.

### Motivo

- Analise do specsfy (repo + videos do autor) mostrou que a dor raiz e comum (contexto para a IA sem reler tudo), mas o publico e o eixo diferem: specsfy e pipeline de especificacao para vibe coding; nossa skill e memoria multiagente entre sessoes. Importar mecanismos pontuais resolve nossas lacunas (TASKS sem estrutura, validacao em prosa, sem versionamento/atualizacao) sem herdar a cerimonia.
- Travessao proibido por pedido explicito do usuario em 2026-08-20.

### Impacto

- Novos projetos nascem com estrutura v2 (marcadores versionados, TASKS com IDs, regra anti-travessao).
- Projetos v1 sao atualizaveis pelo fluxo `references/atualizacao.md`, com diff por bloco e confirmacao por item.
- `python3 <skill>/scripts/validate_structure.py <projeto>` vira o gate de qualidade da estrutura.
- O meta-projeto passa a usar a propria v2 (specs ativo; spec `0001-skill-v2`).

## 2026-05-26 - Distribuicao da skill via Agent Skills Open Standard

### Decisao

- Distribuir a skill `ai-project-structure` como um unico pacote no formato **Agent Skills Open Standard** (frontmatter YAML `name` + `description`), valido para Claude Code, Codex CLI e Gemini CLI ao mesmo tempo. Nao manter formatos separados por ferramenta.
- Caminhos canonicos de instalacao: Claude `~/.claude/skills/`, Codex `~/.agents/skills/`, Gemini `~/.gemini/skills/` (e os equivalentes `.<tool>/skills/` por-projeto).
- Adotar `install.sh` na pasta da skill como mecanismo oficial de instalacao/atualizacao/remocao.
- A instalacao copia apenas `SKILL.md`, `assets/` e `agents/`; `evals/`, `install.sh` e `README.md` ficam so na fonte.

### Motivo

- A partir de fins de 2025 o formato `SKILL.md` virou padrao aberto adotado por Claude Code, Codex e Gemini (entre outros), eliminando a necessidade de tres formatos distintos.
- O caminho de skills do Codex e `~/.agents/skills/`; o registro anterior usava `~/.codex/skills/`, que nao e lido pelo Codex.

### Impacto

- Uma unica fonte (`docs/skills/ai-project-structure/`) gera a instalacao nas tres ferramentas; atualizar = editar a fonte e rodar `install.sh`.
- Registro anterior de instalacao (2026-04-25) fica **substituido** por este: aquela instalacao nao persistiu e apontava o Codex para o caminho errado.


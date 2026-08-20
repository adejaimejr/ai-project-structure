# README

Este projeto usa uma estrutura Markdown preparada para trabalho com agentes de IA.

A raiz fica limpa e contem apenas os arquivos de entrada dos agentes:

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`

A memoria do projeto fica em `docs/`.

## Como Comecar

Para humanos:

1. Leia este arquivo.
2. Leia `PROJECT_CONTEXT.md`.
3. Veja o estado atual em `TASKS.md`.
4. Consulte `SESSION.md` para saber o que aconteceu nas ultimas sessoes.

Para agentes de IA:

1. Leia `../AGENTS.md`.
2. Siga a ordem de leitura definida nele.
3. Atualize `SESSION.md` ao final de trabalho relevante.

## Arquivos Principais

Nucleo (sempre presente):

- `PROJECT_CONTEXT.md`: contexto permanente do projeto.
- `SESSION.md`: registro cronologico das sessoes de IA.
- `MEMORY.md`: memoria persistente (preferencias, licoes, refs externas).
- `CONSENSUS.md`: debate entre modelos para chegar a consenso.
- `TASKS.md`: tarefas atuais e proximos passos.
- `DECISIONS.md`: decisoes importantes.
- `QUALITY.md`: criterios de qualidade e validacao.
- `CHANGELOG.md`: mudancas relevantes na estrutura ou no produto.
- `archive/`: sessoes e debates antigos rotacionados.

Opcionais (estrutura completa, ou criados quando o projeto precisar):

- `ARCHITECTURE.md`: visao tecnica.
- `API.md`: contratos de API.
- `DATA_MODEL.md`: modelo de dados.
- `GLOSSARY.md`: termos, siglas e nomes internos.
- `ONBOARDING.md`: guia de entrada no projeto.
- `ROADMAP.md`: direcao de medio prazo.
- `PROMPTS.md`: prompts reutilizaveis.
- `STACK.md`: mapa da stack (tecnologias, pacotes, links de documentacao oficial).

Modulo opcional:

- `specs/`: specs de features (o que sera construido), quando o modulo estiver ativo.


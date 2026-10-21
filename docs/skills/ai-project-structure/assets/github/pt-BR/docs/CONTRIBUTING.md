# Contribuindo

Obrigado por ajudar. Este arquivo explica como propor uma mudanca no projeto.

## Idiomas

- A camada GitHub (README, este arquivo, `SECURITY.md`, o codigo de conduta, templates de issue e de PR, workflows e releases) e escrita em portugues (pt-BR).
- `AGENTS.md`, `docs/` e a memoria do projeto seguem o idioma definido em `AGENTS.md`.

## Portoes

Rode os comandos listados na secao "Testes E Validacao" de `docs/QUALITY.md` antes de abrir um pull request. Essa secao e a definicao unica de "passou" para este projeto, e o CI roda os mesmos comandos.

O CI tambem valida a estrutura Markdown do projeto (`AGENTS.md` e `docs/`) em modo estrito.

## Sem travessao

O caractere travessao (em dash, U+2014) e proibido em arquivos Markdown. Use dois-pontos, virgula, ponto-e-virgula, parenteses ou hifen simples.

## Commits

Siga o formato de commit registrado em `AGENTS.md`. Cite a tarefa como `(T-NNN)` quando houver.

## Pull requests

- Mudanca em codigo entra em `main` por pull request, com o check `ci` verde.
- Nunca faca force push em `main` e nunca apague `main`.
- Preencha o template do pull request: o que mudou, por que e como voce verificou.

## Releases

Um bump de versao exige tudo isto:

1. Atualizar a versao e a secao do CHANGELOG.
2. Criar uma tag anotada `vX.Y.Z` no commit do bump: `git tag -a vX.Y.Z`.
3. Enviar a tag: `git push origin vX.Y.Z`.
4. Publicar uma Release no GitHub para a tag.

Tag sem bump, ou bump sem tag, e erro.

## Configuracao do repositorio

A configuracao do repositorio (descricao, topics, rulesets, labels) e feita pela CLI `gh`, nunca por um agente por conta propria. O checklist esta em `references/github.md` da skill de estrutura.

## Onde cada coisa e registrada

As regras do projeto vivem em `AGENTS.md`. O trabalho e registrado em `docs/TASKS.md`, `docs/SESSION.md`, `docs/DECISIONS.md` e `docs/CHANGELOG.md`; veja `AGENTS.md` para saber o que vai em cada um.

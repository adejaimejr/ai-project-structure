# AGENTS.md

<!-- ai-project-structure:core:start v2.13.0 -->

Este e o arquivo central de instrucao para qualquer agente de IA neste projeto.

<!-- ai-project-structure:core:end -->

<!-- ai-project-structure:github:start v9.9.9 -->
## Camada GitHub (Modulo Opcional Ativo)

Este projeto tem a camada GitHub gerada pela skill: `.github/`, arquivos de comunidade em `docs/`, `ci.yml` e `dependabot.yml`.

- **Raiz minima, com excecao.** Alem dos arquivos de entrada dos agentes, a raiz aceita `README.md`, `LICENSE`, `.gitignore`, `.github/` e dotfiles de configuracao (como `.gitattributes`). Nenhum outro diretorio na raiz.
- **Comunidade em `docs/`.** `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` e `PULL_REQUEST_TEMPLATE.md` vivem em `docs/`, nao na raiz.
- **Idioma.** A camada GitHub (README, arquivos de comunidade, templates, workflows e corpo de release) segue o idioma escolhido na ativacao. Este arquivo e `docs/` seguem em pt-BR. A proibicao do travessao vale nos dois idiomas.
- **Mudanca por pull request.** Mudanca em codigo vai para `main` por pull request com o `ci` verde. Nunca force push nem delecao em `main`.
- **Tag e Release a cada bump.** Todo bump de versao termina em tag anotada `vX.Y.Z` no commit do bump (`git tag -a vX.Y.Z` e `git push origin vX.Y.Z`) e em uma Release no GitHub. Tag sem bump ou bump sem tag e erro.
- **Configuracao pela CLI `gh`.** Descricao, topics, rulesets e labels do repositorio sao feitos pela CLI `gh`, nunca pela skill, e so com o sim do usuario. O checklist esta em `references/github.md` da skill `ai-project-structure`.
- **`ci.yml` e gerado, nao inventado.** Ele roda o validador da estrutura, baixado da Release da skill com conferencia do `.sha256`, e o comando de "Testes E Validacao" de `docs/QUALITY.md`. Se a secao estiver vazia, o placeholder fica visivel; ninguem preenche comando por inferencia.

## Regras Do Projeto

(Vazio.)

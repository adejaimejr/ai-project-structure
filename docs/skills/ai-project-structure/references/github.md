# GitHub: Ativar Modulo, Configurar O Repositorio E Publicar Versao

Modulo opcional. **Nunca entra no scaffold sem resposta explicita** na pergunta 5 da entrevista, e nunca e oferecido por conta propria no meio de outro fluxo: ativar e sempre pedido do usuario.

**A skill nao roda `gh`, nem `git push`, nem nada com efeito fora da pasta do projeto.** Ela copia arquivos e insere um bloco em `AGENTS.md`. A configuracao do repositorio no GitHub e o fluxo de versao ficam como checklist, feitos pela pessoa ou pelo agente de chat com o sim dela, comando a comando (coerente com "Nao inicialize repositorio git" do `SKILL.md`).

## O Que O Modulo Entrega

- Arquivos de comunidade em `docs/`: `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `PULL_REQUEST_TEMPLATE.md`.
- `.github/ISSUE_TEMPLATE/` (`bug.yml`, `feature.yml`, `config.yml`), `.github/dependabot.yml` e `.github/workflows/ci.yml`.
- `.gitattributes` (`* text=auto eol=lf`).
- Um bloco gerenciado `github` em `AGENTS.md`, de `assets/partials/AGENTS-github-block.md`, com as regras de fluxo: raiz minima com `.github/` e dotfiles, comunidade em `docs/`, mudanca por pull request, tag anotada e Release a cada bump.

Os arquivos vivem em `assets/github/en/` e `assets/github/pt-BR/`, com a mesma lista nas duas linguas. Nao existe `release.yml` no modulo: ele empacota a skill deste repositorio e projeto comum nao tem pacote para publicar (DEC-001 da spec 0007). O fluxo de versao esta em "Fluxo Bump, Tag E Release" abaixo.

## Ativar O Modulo Em Projeto Existente

1. Confirme que o projeto usa a estrutura e esta na versao atual (marcadores em `AGENTS.md`; se estiver atras, ofereca primeiro o fluxo de `atualizacao.md`).
2. Confirme a **lingua** dos arquivos, `en` ou `pt-BR`. Sem resposta, nao ative (regra "Nunca Inferir"): "Avançar" adia a ativacao, nao escolhe lingua.
3. Pergunte **item a item**, com opcoes numeradas, os dois opcionais:
   - `docs/CODE_OF_CONDUCT.md`: default **sim** (e o que leva o perfil de comunidade do GitHub a 100);
   - `.gitattributes`: default **nao** (`eol=lf` muda o checkout no Windows).

   Os demais arquivos da lista entram sempre.
4. Para cada arquivo da lista da lingua escolhida em `assets/github/<lingua>/`, copie para o mesmo caminho relativo no projeto. **Arquivo que ja existe no destino e pulado, nunca mesclado**, e entra na lista "pulados" do relatorio (DEC-007). Nao mexa num `ci.yml` alheio nem sobrescreva sem confirmacao. Crie `.github/` e as subpastas que faltarem.
5. Preencha os placeholders do `.github/workflows/ci.yml` que voce acabou de copiar (se ele foi pulado, nao ha o que preencher):
   - `{{SKILL_VERSION}}`: a versao da skill que esta ativando o modulo (campo `version` do `SKILL.md`, por exemplo `2.14.0`). Ela fixa no CI a Release de onde o validador e baixado.
   - `{{QUALITY_COMMAND}}`: o comando da secao "Testes E Validacao" de `docs/QUALITY.md` do projeto, mostrado ao usuario para confirmar que e mesmo o portao do projeto. Comando de varias linhas entra com a indentacao do passo `run: |`. Se o projeto precisa de runtime ou dependencias para rodar o comando, avise que falta um passo de setup antes dele.
   - Se a secao estiver vazia, com o texto do template ("Quando o projeto tiver codigo, registrar aqui") ou sem comando executavel: **deixe o placeholder `{{QUALITY_COMMAND}}` visivel e avise** o usuario de que o CI falha ate ele preencher. Nunca invente comando (regra "Nunca Inferir"); ofereca preencher a secao primeiro.
6. Insira o conteudo de `assets/partials/AGENTS-github-block.md` em `AGENTS.md`, depois do ultimo bloco gerenciado e antes de "## Regras Do Projeto". Se o bloco `github` ja existir, nao duplique. A versao do marcador acompanha a dos demais blocos.
7. Registre: entrada em `docs/SESSION.md` e linha em `docs/CHANGELOG.md` do projeto.
8. Relate ao usuario: lingua escolhida, arquivos criados, **arquivos pulados** por ja existirem, placeholder que ficou visivel (se ficou), e que a configuracao do repositorio (proxima secao) e dele.

Rode `validate_structure.py <projeto> --strict`: ele confere os marcadores do bloco `github` (par, versao e coerencia com os demais blocos), nao o conteudo dos arquivos de `.github/` e `docs/`.

Desativar e remover o bloco entre os marcadores `github` e apagar os arquivos copiados que a pessoa nao quer mais.

## O Que O Passo De Validacao Do CI Prova (E O Que Nao)

O `ci.yml` gerado tem um passo que baixa o zip da Release da skill, `ai-project-structure-X.Y.Z.zip`, e o `.sha256` da mesma Release, confere com `sha256sum -c` e roda `validate_structure.py . --strict`. O passo seguinte roda o comando de "Testes E Validacao".

**Limite declarado:** o `.sha256` vem da mesma Release do zip. Ele prova **integridade** do download (o arquivo nao se corrompeu no caminho), nao **autenticidade** (quem publicou a Release). Quem controlasse a Release poderia trocar zip e checksum juntos. Projeto com exigencia maior deve fixar o hash em um lugar que ele controle, ou revisar o zip antes de adotar a versao.

## Checklist De Configuracao Do Repositorio

Feito pela pessoa, ou pelo agente de chat com o sim dela a cada comando. A skill nunca executa. Confira a flag na maquina antes de rodar (`gh <comando> --help`): a CLI muda entre versoes.

1. **Descricao e topics**, pela CLI:

   ```bash
   gh repo edit OWNER/REPO --description "<uma frase>" --add-topic <topic> --add-topic <outro>
   ```

2. **Rulesets de `main`.** Dois, e o motivo e que check obrigatorio em ruleset tambem rejeita push direto em `main`, contra a regra de deixar mudanca so em `docs/` ir direta:
   - `main`: bloqueia delecao e force push (`deletion`, `non_fast_forward`), sem bypass;
   - `main-ci`: exige o check `ci` (`required_status_checks` com o contexto `ci`), com bypass do admin do repositorio.

   ```bash
   gh api -X POST repos/OWNER/REPO/rulesets --input - <<'JSON'
   {"name": "main", "target": "branch", "enforcement": "active",
    "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
    "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}], "bypass_actors": []}
   JSON
   gh api -X POST repos/OWNER/REPO/rulesets --input - <<'JSON'
   {"name": "main-ci", "target": "branch", "enforcement": "active",
    "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
    "rules": [{"type": "required_status_checks", "parameters": {"strict_required_status_checks_policy": false,
      "do_not_enforce_on_create": false, "required_status_checks": [{"context": "ci", "integration_id": 15368}]}}],
    "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]}
   JSON
   ```

   O check `ci` so existe depois da primeira rodada do `ci.yml`: ative o `main-ci` depois de um PR com o CI verde. Confirme com `gh ruleset list` e `gh ruleset view`.

3. **Labels**, uma a uma com `gh label create <nome> --description "<texto>" --color <hex6>` (`--force` atualiza uma existente). Rotule so o que o projeto usa; as labels padrao do GitHub bastam para comecar.

4. **Wiki e Projects desligados** quando nao usados: `gh repo edit OWNER/REPO --enable-wiki=false --enable-projects=false`.

5. **Perfil de comunidade**: depois de tudo, a aba Insights, Community Standards do repositorio deve estar completa (README, licenca, codigo de conduta, contribuicao, politica de seguranca, templates). Licenca e README sao do projeto, nao do modulo.

Armadilhas ja vividas, para ninguem repetir:

- **Token sem permissao.** O token do `gh` de uma sandbox pode ter contents e pull requests, mas nao Administration nem Actions: write. Criar ruleset e disparar workflow dao HTTP 403. A saida e o usuario conceder a permissao ou agir pela interface web; nao tente contornar.
- **Workflow novo ou alterado passa por `actionlint` antes do merge.** Rodar localmente o script de cada passo nao avalia as expressoes `${{ }}`: um `runner.temp` no `env` do job fez o GitHub recusar o workflow inteiro (HTTP 422) e a simulacao local nao viu.

## Fluxo Bump, Tag E Release

Todo bump de versao termina em tag anotada e em Release (regra do bloco `github` de `AGENTS.md`):

1. **Bump em pull request.** Mude a versao e adicione a secao `## X.Y.Z - AAAA-MM-DD` ao `CHANGELOG.md`. Mudanca em codigo vai para `main` por pull request com o `ci` verde; so mudanca em `docs/` pode ir direta, se a regra do projeto deixar.
2. **Merge** com o `ci` verde.
3. **Tag anotada no commit do bump**, nunca em commit anterior:

   ```bash
   git tag -a vX.Y.Z -m "X.Y.Z"
   git push origin vX.Y.Z
   ```

   Tag sem bump, ou bump sem tag, e erro.
4. **Release** no GitHub para a tag. O `release.yml` e do projeto, nao do modulo: projeto que tem um publica a Release a partir da secao do CHANGELOG; sem workflow, `gh release create vX.Y.Z --verify-tag --notes-file <arquivo>` com o corpo da secao.
5. **Confira**: `gh release list` mostra a versao como Latest e, se a Release carrega artefato, o `.sha256` confere.

Armadilha: **push de tag roda o workflow que existe no commit tagueado.** Tag em commit anterior ao `release.yml` nunca o dispara. Para publicar versao antiga existe o `workflow_dispatch` com a entrada `tag` (`gh workflow run release.yml -f tag=vX.Y.Z`), se o workflow o declarar.

## O Que Este Modulo Nunca Faz

- Rodar `gh`, `git push`, criar tag, Release, ruleset ou label.
- Mesclar com arquivo que ja existe no projeto: ele e pulado e listado.
- Inventar o comando de `{{QUALITY_COMMAND}}`.
- Ativar sem resposta explicita na pergunta 5, ou escolher a lingua por inferencia.
- Copiar `assets/partials/` para o projeto: o bloco entra em `AGENTS.md`, o arquivo nao.

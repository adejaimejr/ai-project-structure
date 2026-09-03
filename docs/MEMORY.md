# MEMORY

Memoria persistente do projeto. Aqui ficam fatos consolidados que valem "a partir de agora, sempre" e que se acumulam ao longo do tempo.

## Diferenca Para Outros Arquivos

- `PROJECT_CONTEXT.md`: o que o projeto **e** (estrutural, raramente muda).
- `MEMORY.md`: o que o projeto **aprendeu** (acumula com o tempo).
- `SESSION.md`: o que **aconteceu** em data X (cronologico).
- `DECISIONS.md`: o que foi **decidido** formalmente.

Regra rapida: cronologico vai pro `SESSION.md`. Decisao formal vai pro `DECISIONS.md`. Fato persistente nao-decidido (preferencia, licao, ref externa) vai pro `MEMORY.md`. Estrutural permanente vai pro `PROJECT_CONTEXT.md`.

## Criterio De Promocao

Algo so sai de `SESSION.md` para `MEMORY.md` quando:

- e util para sessoes futuras (nao apenas para a sessao corrente);
- e reutilizavel (nao e detalhe especifico de uma tarefa pontual);
- ja esta consolidado (nao e hipotese ou impressao recente).

Em duvida, deixe em `SESSION.md`. Memoria curta e melhor que memoria errada.

## Sobrescrita Ativa

Fatos podem ficar obsoletos. Quando isso acontecer:

- marque o fato antigo como `~~texto~~ (substituido em AAAA-MM-DD)`;
- adicione o fato novo logo em seguida;
- nao apague o historico - registrar a mudanca ajuda a entender por que mudou.

Se um fato em `MEMORY.md` virar contexto estrutural permanente, promova para `PROJECT_CONTEXT.md` e remova daqui.

## Dados Sensiveis

Nao registre credenciais, tokens, dados pessoais ou informacoes confidenciais. Em duvida, escreva no menor nivel de detalhe util.

## Tipos De Memoria

### User

Quem e o usuario, suas preferencias, contexto e expertise.

Exemplo de entrada: "Usuario prefere portugues claro e respostas curtas."

### Feedback

Guidance de "faca/nao faca isso". Cada item: regra, motivo e quando aplicar.

Exemplo de entrada:

- **Regra:** nao usar mocks em testes de migracao.
- **Por que:** mocks passaram em Q4/2025 mas migracao quebrou em producao.
- **Quando aplicar:** qualquer teste que envolva schema do banco.

### Project

Fatos sobre o projeto descobertos na pratica que nao estao em `PROJECT_CONTEXT.md`.

Exemplo de entrada: "Build em CI exige Node 20.x; 22.x quebra a etapa de bundling."

### Reference

Pointers para sistemas externos.

Exemplo de entrada: "Issues do produto X sao trackeadas no Linear projeto INGEST."

## Registros

### User

- Perfis de loop, por intencao e ferramenta. Registrados em 2026-09-02 a pedido do usuario, para nao ter que digitar o comando na hora de chamar o `loop.sh`:
  - Claude, planejar: `claude -p --permission-mode bypassPermissions --model fable --effort max`
  - Claude, executar: `claude -p --permission-mode bypassPermissions --model opus --effort high`. Use `--effort xhigh` quando a tarefa for dificil; os niveis sao low, medium, high, xhigh e max.
  - Codex, planejar: `codex exec -s workspace-write --skip-git-repo-check -m gpt-5.6-sol -c model_reasoning_effort="high"`
  - Codex, executar: `codex exec -s workspace-write --skip-git-repo-check -m gpt-5.6-terra -c model_reasoning_effort="high"`
  - Grok, executar: `grok --always-approve -m grok-4.6 --effort high -p`. O usuario ainda nao tem plano no Grok; ate ter, roda em credito.
- Nome de modelo envelhece rapido. Os acima foram conferidos em 2026-09-02 contra `claude --help` (aliases `fable`, `opus`, `sonnet`) e `~/.codex/models_cache.json` (`gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`). Confira de novo antes de confiar.
- O usuario usa Claude e Codex por assinatura, e pretende assinar o Grok. O custo em dolar que as CLIs imprimem e preco de tabela da API e nao corresponde ao que ele paga.

### Feedback

- **Regra:** nunca usar o caractere travessao (em dash, U+2014) em textos do projeto ou da skill; usar dois-pontos, ponto-e-virgula, virgula, parenteses ou hifen simples. **Por que:** pedido explicito do usuario em 2026-08-20; o validador da skill acusa ocorrencias como erro. **Quando aplicar:** qualquer texto escrito neste repositorio e nos templates que a skill gera.

### Project

- Check que procura um caractere proibido tem de escrever esse caractere escapado no proprio codigo. O `verify_repository.py` foi escrito com o travessao literal na comparacao e se acusou na primeira execucao (2026-09-02). Use `"\u2014"`, como o `validate_structure.py` ja fazia.
- O `install.sh` da skill nao distribui tudo o que existe na fonte canonica: `evals/`, `install.sh`, `README.md` e `CHANGELOG.md` ficam apenas em `docs/skills/ai-project-structure/` e nao aparecem em `~/.claude/skills/`, `~/.agents/skills/` nem `~/.gemini/skills/` (verificado por `diff -rq` em 2026-09-02). Ferramenta que deve ficar restrita ao repositorio vai em `evals/`; o que vai em `scripts/` chega na maquina de todo usuario.

### Reference

- specsfy (inspiracao da v2 da skill): github.com/promovaweb/specsfy. Metodologia SDD pt-BR; analisada em 2026-08-20; o que importamos e o que descartamos esta em `docs/DECISIONS.md` e no CHANGELOG da skill.


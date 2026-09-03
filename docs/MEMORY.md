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

- Perfis de loop, por intencao e ferramenta. Registrados em 2026-09-02 a pedido do usuario, para nao ter que digitar o comando na hora de chamar o `loop.sh`. Executar tem tres niveis, escolhidos conforme a dificuldade da tarefa:
  - Claude, planejar: `claude -p --permission-mode bypassPermissions --model fable --effort max`
  - Claude, executar: `claude -p --permission-mode bypassPermissions --model opus --effort high`
  - Claude, executar-dificil: `claude -p --permission-mode bypassPermissions --model opus --effort xhigh`
  - Claude, executar-muito-dificil: `claude -p --permission-mode bypassPermissions --model opus --effort max`
  - Codex, planejar: `codex exec -s workspace-write --skip-git-repo-check -m gpt-5.6-sol -c model_reasoning_effort="high"`
  - Codex, executar: `codex exec -s workspace-write --skip-git-repo-check -m gpt-5.6-terra -c model_reasoning_effort="high"`
  - Codex, executar-dificil: `codex exec -s workspace-write --skip-git-repo-check -m gpt-5.6-terra -c model_reasoning_effort="xhigh"`
  - Codex, executar-muito-dificil: `codex exec -s workspace-write --skip-git-repo-check -m gpt-5.6-terra -c model_reasoning_effort="max"`
  - Grok, planejar: `grok --always-approve -m grok-4.6 --effort xhigh -p`. O `xhigh` e o teto do Grok, e planejar merece o teto.
  - Grok, executar: `grok --always-approve -m grok-4.6 --effort high -p`
  - Grok, executar-dificil: `grok --always-approve -m grok-4.6 --effort xhigh -p`
  - Grok, executar-muito-dificil: `grok --always-approve -m grok-4.6 --effort xhigh -p`. **E o mesmo comando de `executar-dificil`, por decisao do usuario em 2026-09-02**: a escada do Grok termina em `xhigh` (a interface chama de "Extra High"; confirmado no menu e nas strings do binario, que so trazem `low`, `medium`, `high` e `xhigh`), e ficar sem opcao no degrau mais alto era pior que repetir o teto. Ao cair nesse degrau no Grok, **diga que ja e o teto da ferramenta** e ofereca outra se a tarefa parecer precisar de mais.
  - O usuario ainda nao tem plano no Grok; ate ter, roda em credito.
  - opencode, planejar: `opencode run --auto -m deepseek/deepseek-v4-pro`
  - opencode, executar: `opencode run --auto -m deepseek/deepseek-v4-flash`
  - opencode, executar-dificil: `opencode run --auto -m deepseek/deepseek-v4-flash`. Mesmo modelo do degrau base, por decisao do usuario em 2026-09-03: o `flash` deu conta da mesma tarefa que o `pro` na validacao, entao subir de modelo cedo demais so encarece.
  - opencode, executar-muito-dificil: `opencode run --auto -m deepseek/deepseek-v4-pro`. O `pro` e o topo do DeepSeek no catalogo do opencode; ao cair nesse degrau, diga que ja e o teto e ofereca outra ferramenta.
  - No opencode a escada e **por modelo, nao por esforco**: o catalogo nao declara conjunto de variantes para os modelos DeepSeek, entao `--variant` pode ser inerte ali. A rodada de validacao do `pro` usou `--variant high`, mas o flag foi retirado dos perfis: nao houve como confirmar que ele muda alguma coisa, e flag que aparenta controle sem ter e pior que flag nenhuma.
  - Os dois modelos foram exercitados em 2026-09-02 no subprojeto `durakit`: portao verde na tentativa 1 nos dois, e os dois acertaram os casos que as regras determinam e a suite nao cobre.
  - Comportamento observado em 2026-09-03, projeto de conteudo: com a regra "nao apague o que falha" apenas no bloco do `AGENTS.md`, o `deepseek-v4-flash` apagou a frase que continha um link quebrado, duas vezes, para o portao passar. Com a mesma regra no prompt do `loop.sh`, passou a perguntar. Claude e Codex perguntaram nas duas versoes. Se um dia a regra sair do prompt, e esse o modelo que quebra primeiro.
  - **Atencao ao custo:** DeepSeek entra por chave de API, entao e cobranca por token de verdade, diferente de Claude e Codex. Precos do catalogo em 2026-09-02, por 1M de tokens: `flash` 0,14 de entrada e 0,28 de saida; `pro` 0,435 e 0,87.
  - Rotulo de interface nao e o valor da CLI. No Claude, "Extra" e `xhigh`. No Codex, o menu mostra Light, Medium, High, Extra High e Ultra, que sao `low`, `medium`, `high`, `xhigh` e `ultra`; o nivel `max` existe no catalogo e nao aparece nesse menu.
  - `ultra` do Codex nao e so mais esforco: o catalogo o descreve como "maximum reasoning with automatic task delegation", ou seja, ele abre subagentes, e a interface avisa que consome limite mais rapido. Por isso os perfis param em `max`: dentro de uma rodada de loop, com ate 3 tentativas e sem ninguem olhando, delegacao automatica multiplica consumo de plano sem aviso.
- Nome de modelo e nivel de esforco envelhecem rapido. Os acima foram conferidos em 2026-09-02: `claude --help` da os aliases (`fable`, `opus`, `sonnet`) e os niveis (`low, medium, high, xhigh, max`); `~/.codex/models_cache.json` da os modelos e os niveis por modelo (`sol` e `terra` vao ate `ultra`). Confira de novo antes de confiar.
- O usuario usa Claude e Codex por assinatura, e pretende assinar o Grok. O custo em dolar que as CLIs imprimem e preco de tabela da API e nao corresponde ao que ele paga.

### Feedback

- **Regra:** portao novo so entra depois de voce quebrar de proposito o que ele deveria pegar, e ver ele acusar. **Por que:** em 2026-09-03, cinco mutacoes temporarias derrubaram duas verificacoes que pareciam boas: contar linhas `[AVISO]` aceitava regressao compensada, e o `strip_fences` podia quebrar sem nenhuma das cinco fixtures acusar. Nas duas vezes, o portao estava verde e cego, e nenhuma leitura do codigo tinha mostrado isso. **Quando aplicar:** ao escrever ou revisar qualquer check, fixture ou eval. Reverta a mutacao de um backup proprio, nunca de `git checkout` (regra abaixo), e registre na evidencia o que cada mutacao produziu.
- **Regra:** para reverter mutacao temporaria em arquivo versionado com trabalho **nao commitado** por cima, guarde o original com `cp` antes e restaure dele. Nunca `git checkout <arquivo>`. **Por que:** em 2026-09-03 isso apagou a reescrita inteira do `verify_repository.py`, que estava pronta e nao commitada; `git checkout` restaura do index, nao do estado anterior a mutacao. **Quando aplicar:** sempre que a mutacao de teste cair em arquivo que voce esta editando na mesma sessao.
- **Regra:** nunca usar o caractere travessao (em dash, U+2014) em textos do projeto ou da skill; usar dois-pontos, ponto-e-virgula, virgula, parenteses ou hifen simples. **Por que:** pedido explicito do usuario em 2026-08-20; o validador da skill acusa ocorrencias como erro. **Quando aplicar:** qualquer texto escrito neste repositorio e nos templates que a skill gera.

### Project

- Ponte so existe para ferramenta que nao le `AGENTS.md` sozinha. Verificado em 2026-09-03 contando referencias dentro dos proprios binarios: Grok cita `AGENTS.md` 46 vezes e opencode 29, e nenhum dos dois procura `GROK.md` ou `OPENCODE.md`. Codex tambem le `AGENTS.md` direto, que e o padrao Agent Skills. Sobram Claude Code, que entra por `CLAUDE.md`, e Gemini CLI, por `GEMINI.md`. Criar ponte para as outras seria arquivo morto. Como bonus, Grok e opencode tambem olham `CLAUDE.md` por compatibilidade, e a nossa ponte so aponta para o `AGENTS.md`, entao isso ajuda.
- A skill fechou a versao 2.3.0 em 2026-09-02, com o modulo de loop: a estrutura passou a executar tarefa verificavel, nao so descreve-la. Publicada no GitHub e instalada nos tres destinos globais.
- Gemini CLI nao roda nesta maquina: a conta cai em `IneligibleTierError`, com o free tier do Gemini Code Assist descontinuado para este cliente, que foi mandado migrar para Antigravity. Nao e defeito do modulo de loop, e nao adianta reinvestigar sem mudar de conta.
- A evidencia de uma tarefa fechada pelo loop vale exatamente o que o portao dela vale. Numa bancada com tres ferramentas, duas fecharam tarefa com bug numa regra de borda que a suite nao cobria, e a evidencia estava correta. O argumento completo esta em `references/loop.md`, secao "A Evidencia Vale O Que O Portao Vale"; antes de declarar `(verifica:)` numa tarefa, pergunte se aquele comando falharia caso o trabalho saisse errado.

- Check novo que e AVISO nao separa fixture pelo exit code. O padrao de fixture do repositorio (par `valido`/`invalido` com exit code esperado no `FIXTURES`) so funciona porque os checks da 2.2.0 eram ERRO. Ao adicionar check de nivel AVISO, o par precisa rodar em `--strict` **e** conferir quais avisos sairam, por motivo e por entrada, nao so quantos. Contar linhas `[AVISO]` nao basta: aceita regressao compensada, em que um aviso certo some e outro errado aparece. Achado `0005-A1` em `docs/CONSENSUS.md`, revalidado pelo Codex na rodada 2; decisao de 2026-09-03 em `docs/DECISIONS.md`; implementado na 2.5.0, com identificador estavel por diagnostico e a flag `--codigos` (`NIVEL|CODIGO|ARQUIVO|SUJEITO`) como contrato do portao.
- Check que procura um caractere proibido tem de escrever esse caractere escapado no proprio codigo. O `verify_repository.py` foi escrito com o travessao literal na comparacao e se acusou na primeira execucao (2026-09-02). Use `"\u2014"`, como o `validate_structure.py` ja fazia.
- O `install.sh` da skill nao distribui tudo o que existe na fonte canonica: `evals/`, `install.sh`, `README.md` e `CHANGELOG.md` ficam apenas em `docs/skills/ai-project-structure/` e nao aparecem em `~/.claude/skills/`, `~/.agents/skills/` nem `~/.gemini/skills/` (verificado por `diff -rq` em 2026-09-02). Ferramenta que deve ficar restrita ao repositorio vai em `evals/`; o que vai em `scripts/` chega na maquina de todo usuario.

### Reference

- specsfy (inspiracao da v2 da skill): github.com/promovaweb/specsfy. Metodologia SDD pt-BR; analisada em 2026-08-20; o que importamos e o que descartamos esta em `docs/DECISIONS.md` e no CHANGELOG da skill.


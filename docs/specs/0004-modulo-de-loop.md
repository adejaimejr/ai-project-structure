# Spec 0004 - Modulo de loop (skill 2.3.0)

**Status:** Rascunho
**Criada em:** 2026-09-02
**Esforco:** G, primeira parte da estrutura que executa em vez de descrever. Depende de respostas do usuario antes de virar `Definida`.

## Problema E Resultado Esperado

- Problema: hoje a estrutura descreve trabalho verificavel e nao executa nada. Quem roda o portao e a pessoa, turno a turno. Um projeto com `(verifica: <comando>)` declarado em tarefa aberta e com comando real em `QUALITY.md` ja tem tudo que um loop precisaria para trabalhar sozinho, e essa informacao fica parada.
- Problema: o parecer de 2026-09-02 mostrou por que o loop nao podia entrar na 2.2.0 (ver DEC-003): no dia zero de um projeto scaffoldado nao existe suite de teste, e um loop cujo unico portao e "o Markdown esta bem formado" e pior que nenhum loop, porque parece um portao. Isso continua verdade para projeto novo, e deixou de ser verdade para projeto maduro.
- Resultado esperado: um modulo opcional, ativado sob demanda em projeto que ja tem portao real, que pega tarefa elegivel, trabalha, roda o comando declarado e para quando o portao falha ou quando falta resposta humana. Nunca no scaffold.
- Resultado esperado: um projeto que nao ativa o modulo nao paga nada por ele, nem em instrucao no bloco core, nem em arquivo.

## Escopo

### Incluido

Ja decidido em versoes anteriores, entra sem nova discussao:

- Modulo opcional no mesmo padrao do modulo de specs: `references/loop.md` (fluxo detalhado), `assets/partials/AGENTS-loop-block.md` (bloco de insercao), marcadores proprios `ai-project-structure:loop:start|end`, ativado sob demanda e nunca copiado para o projeto-alvo como template.
- Portao de ativacao: a secao "Testes E Validacao" de `QUALITY.md` do projeto-alvo precisa ter comando real. Sem isso, a skill recusa a ativacao e explica o motivo (DEC-005 mandou a exigencia para ca, em vez de virar aviso do validador).
- O loop le `(verifica: <comando>)` como criterio de elegibilidade da tarefa, sem renomear a convencao ja distribuida (DEC-001).
- Nunca ativado no scaffold, em nenhum nivel (DEC-003).
- `verify_repository.py` estendido para cobrir o bloco e o partial novos, como ja faz com `core` e `specs`.

### Fora Do Escopo

- Ativacao automatica, por heuristica ou por deteccao de "o projeto tem codigo". A ativacao e sempre pedido explicito do usuario.
- Qualquer instrucao de loop no bloco `core`. O custo de leitura recai so em quem ativou.
- Reescrita das convencoes da 2.2.0. O loop consome `(verifica:)`, `Evidencia:` e `Aguardando Usuario` como estao.

## Criterios De Aceite

Derivaveis do que ja esta decidido:

- Projeto sem o modulo ativado nao ganha nenhum arquivo, nenhum marcador e nenhuma linha no `AGENTS.md`.
- Ativacao em projeto com "Testes E Validacao" vazio ou so com o texto do template e recusada, com a razao dita ao usuario.
- Ativacao em projeto com comando real insere o bloco `loop` entre o ultimo bloco gerenciado e "## Regras Do Projeto", em v2.3.0, e cria `references/loop.md` na skill (nao no projeto).
- Scaffold minimal e scaffold completa continuam sem qualquer vestigio do modulo.
- `verify_repository.py` confere o bloco `loop` e o partial com a mesma paridade que ja exige de `core` e `specs`.
- Nenhum travessao (U+2014) em arquivo novo ou alterado.

Os criterios de comportamento do loop (o que ele executa, quando para, o que registra) **nao podem ser escritos ainda**: dependem das respostas em "Perguntas Abertas". Sem elas, qualquer criterio aqui seria inventado, que e o que a regra "Nunca Inferir" proibe.

## Decisoes

- DEC-001 (herdada da spec 0003): o marcador de verificacao se chama `(verifica:)` e o loop o le como criterio de elegibilidade, sem renomear.
- DEC-003 (herdada da spec 0003): o loop nunca entra no scaffold. A ressalva do Codex naquela rodada continua valendo e e o que esta spec executa: "nao ativar" nao implica "nao disponibilizar caminho de ativacao".
- DEC-005 (herdada da spec 0003): a exigencia de comando real em `QUALITY.md` nao virou check do validador; virou pre-requisito de ativacao deste modulo.

## Tarefas

- (Vazio ate a spec virar `Definida`. Abrir tarefa de implementacao antes das respostas seria comprar escopo que ainda nao existe.)

## Perguntas Abertas

- P-1: **O que o loop percorre?** Uma tarefa por vez, escolhida pelo usuario? A primeira elegivel de "Em Andamento"? Toda a secao ate esvaziar? Proposta, nao decidida: uma tarefa por vez, indicada no comando. E o menor blast radius e o mais facil de abandonar no meio.
- P-2: **Quando ele para?** Candidatos: portao falhou; tarefa concluida com evidencia; N iteracoes; teto de custo; tempo de parede. Quais valem, e com que valor padrao?
- P-3: **Qual ferramenta executa?** Claude Code headless (`claude -p`), `codex exec`, ambas, ou um `loop.sh` neutro que recebe o comando do agente como parametro? A escolha muda o que o modulo distribui.
- P-4: **Ele pode escrever na memoria sozinho?** Mover linha em `TASKS.md`, escrever `Evidencia:`, abrir entrada em `SESSION.md`. Se sim, a evidencia passa a ser escrita pela mesma coisa que deveria ser cobrada por ela. Se nao, o loop para e pede a mao humana no fim de cada tarefa.
- P-5: **Worktree isolado por padrao?** A spec 0003 citou isolamento em worktree como parte do modulo. Padrao ligado, desligado, ou pergunta na ativacao?
- P-6: **O que acontece quando o loop esbarra em falta de contexto?** A regra "Nunca Inferir" manda perguntar. O loop nao tem com quem falar. Proposta, nao decidida: mover a tarefa para `## Aguardando Usuario` com a pergunta preenchida e encerrar o loop, em vez de seguir para a proxima tarefa.
- P-7: **Notificacao ao parar:** nada, som no terminal, notificacao do sistema, ou arquivo de relatorio? A spec 0003 citou notificacao sem definir forma.
- P-8: **"Automacao do consenso" e "teto de custo"** apareceram na lista da 0003. Entram na 2.3.0 ou ficam para depois? A 2.3.0 fica mais defensavel pequena.

## Evidencia De Conclusao

- Verificacao: (A preencher.)
- Resultado: (A preencher.)

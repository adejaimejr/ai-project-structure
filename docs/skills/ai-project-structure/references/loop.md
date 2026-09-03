# Loop: Ativar Modulo E Rodar Uma Tarefa

Modulo opcional. **Nunca entra no scaffold**: um projeto recem-criado nao tem suite de teste, e um loop cujo unico portao e "o Markdown esta bem formado" e pior que nenhum loop, porque parece um portao.

## Portao De Ativacao

O modulo so pode ser ativado em projeto que ja tem verificacao de verdade. Antes de tocar qualquer arquivo:

1. Leia a secao "Testes E Validacao" de `docs/QUALITY.md` do projeto-alvo.
2. Se ela estiver vazia, ou ainda com o texto do template ("Quando o projeto tiver codigo, registrar aqui"), ou sem nenhum comando executavel, **recuse a ativacao** e diga o motivo: sem portao real, o loop nao teria como saber se o trabalho ficou bom. Ofereca preencher a secao primeiro.
3. Se houver comando, mostre ao usuario o que voce encontrou e peca confirmacao de que aquilo e mesmo o portao do projeto. Nao infira.

Esta exigencia e pre-requisito de ativacao, nao check do validador: detectar "o projeto tem codigo" por heuristica e fragil e dispararia em todo projeto de conteudo.

## Ativar O Modulo

1. Confirme que o projeto usa a estrutura e esta na versao atual (marcadores em `AGENTS.md`; se estiver atras, ofereca primeiro o fluxo de `atualizacao.md`).
2. Insira o conteudo de `assets/partials/AGENTS-loop-block.md` em `AGENTS.md`, depois do ultimo bloco gerenciado e antes de "## Regras Do Projeto". Se o bloco `loop` ja existir, nao duplique.
3. Nao copie nenhum arquivo novo para o projeto: o `loop.sh` vive na skill instalada, nao no projeto-alvo.
4. Registre: entrada em `docs/SESSION.md` e linha em `docs/CHANGELOG.md` do projeto.

Desativar e remover o bloco entre os marcadores `loop`. Nada mais fica para tras.

## O Ciclo

Uma rodada trata **uma** tarefa:

1. **Elegibilidade.** A tarefa indicada precisa existir em "Em Andamento" ou "Proximas Tarefas" e ter `(verifica: <comando>)` na linha. Sem isso, a rodada termina antes de chamar o agente, com codigo diferente de zero.
2. **Trabalho.** O agente recebe a tarefa e o `AGENTS.md` do projeto, que ja traz os limites do bloco de loop.
3. **Portao.** Roda o comando declarado em `(verifica:)`, no diretorio do projeto.
4. **Realimentacao.** Portao falhou e ainda ha tentativa: a saida do comando volta como contexto para a proxima. Essa realimentacao e a unica coisa que o loop faz melhor que uma pessoa rodando o comando na mao; sem ela o modulo nao teria razao de existir.
5. **Fecho.** Portao passou: move a tarefa para "## Concluidas" com a data do dia e escreve a sub-linha de evidencia, com `tipo=comando`, `procedimento` igual ao comando declarado e `resultado` com a saida real.
6. **Desistencia.** Esgotou as tentativas: nada se move, nada de evidencia, relatorio com as saidas de todas as tentativas, exit diferente de zero.
7. **Bloqueio.** O agente sinalizou falta de contexto obrigatorio: a tarefa vai para "## Aguardando Usuario" com a pergunta escrita, e a rodada para.

## Uso

```bash
loop.sh --tarefa T-042 --agente "claude -p"
loop.sh --tarefa T-042 --agente "codex exec" --tentativas 5
loop.sh --tarefa T-042 --agente "gemini -p" --projeto /caminho/do/projeto
```

- `--tarefa` (obrigatorio): o `T-NNN`.
- `--agente` (obrigatorio): comando headless da ferramenta que voce usa. O script nao assume nenhuma.
- `--tentativas` (padrao 3).
- `--projeto` (padrao: diretorio atual).

Exit 0 apenas quando o portao passou e a tarefa foi fechada. Qualquer outro caminho sai diferente de zero, o que deixa a composicao por fora funcionar:

```bash
loop.sh --tarefa T-042 --agente "claude -p" && say pronto
```

## Isolamento

O `loop.sh` roda onde voce o chamar, e nao cria worktree. Quem quiser isolar faz antes, com o que o git ja oferece:

```bash
git worktree add ../projeto-loop -b loop/T-042
cd ../projeto-loop
loop.sh --tarefa T-042 --agente "claude -p"
```

Isso foi deixado de fora do modulo de proposito: a estrutura nem sempre vive em repositorio git, e trazer a rodada de volta viraria merge em `TASKS.md`, o arquivo mais editado do projeto.

## O Que O Loop Nunca Faz

- Escolher sozinho em que tarefa trabalhar.
- Fechar tarefa que nao declarou comando.
- Escrever evidencia de `tipo=revisao-manual` ou `tipo=conferencia`.
- Escrever em `SESSION.md`, `MEMORY.md`, `DECISIONS.md`, `AGENTS.md` ou em specs.
- Inventar a resposta que falta. Falta de contexto vira pergunta registrada e parada, nunca inferencia.

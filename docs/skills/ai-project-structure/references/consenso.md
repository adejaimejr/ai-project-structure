# Consenso: Rodar Uma Rodada Automatizada

Uso opcional, sem ativacao: `scripts/consenso.py` vem com a skill e nao toca em `AGENTS.md`. Ele roda N agentes sobre a mesma pergunta, cada um numa copia isolada do projeto, guarda o que cada um disse e escreve em `docs/CONSENSUS.md` so o que a execucao comprova. **Dizer se as posicoes concordam e julgamento, e o julgamento e da pessoa.**

A independencia deixa de ser declaracao e vira propriedade da execucao: cada participante recebe a propria copia, fora do projeto, e nenhuma posicao contemporanea existe nela. O script e a unica coisa que escreve na entrada; os agentes opinam e mais nada.

## Uso

Tres subcomandos. `--projeto` vale `.` por padrao.

```bash
# Rodada 1, cega. A pergunta vai em arquivo.
consenso.py debate --projeto DIR --pergunta pergunta.txt \
  --agente codex "codex exec -s read-only --skip-git-repo-check" \
  --agente cursor "cursor-agent -p --mode ask --force" \
  --titulo "Tema do consenso" --dono "usuario"

# Rodada 2 em diante: o numero e as posicoes anteriores sao seus.
consenso.py debate --projeto DIR --pergunta pergunta.txt --rodada 2 \
  --anterior docs/consensus/<run-id-da-rodada-1> \
  --agente codex "..." --agente cursor "..."

# Revalida a disposicao de um achado que ja existe em CONSENSUS.md.
consenso.py achado --projeto DIR --entrada "2026-10-21 - Titulo do achado" --rodada 2 \
  --agente codex "codex exec -s read-only --skip-git-repo-check"

# Continua uma rodada que nao chegou a `concluida`.
consenso.py retomar --projeto DIR <run-id>
```

Flags de `debate`:

- `--pergunta` (obrigatorio): **arquivo** com a pergunta.
- `--agente ID COMANDO` (repetivel, minimo dois): o `ID` nomeia a pasta e a secao da posicao (distinto, sem barra); o comando e o agente em modo headless. O script nao assume nenhuma ferramenta. O prompt entra como **ultimo argumento**, grande que seja, sem corte e sem resumo. O comando e separado por espaco: argumento com espaco dentro de aspas nao e suportado.
- `--titulo`, `--dono`: texto da entrada e quem le as posicoes e julga (padroes `Debate` e `usuario`).
- `--rodada N` (padrao 1): o script **nunca deduz** o numero.
- `--anterior CAMINHO` (repetivel): arquivo (entra na integra) ou diretorio de rodada em `docs/consensus/` (entra todo `<id>/stdout.txt`). Obrigatorio da rodada 2 em diante e proibido na 1.
- `--pendente TEXTO`: o que a rodada anterior deixou em aberto. Obrigatorio da rodada 4 em diante, proibido na 1; o texto e humano, o script nao inventa.

Flags de `achado`: `--entrada` (titulo exato da entrada, sem o `## `; ela precisa ter `**Achado:**` e `**Rodada:**`), `--rodada` (1 ou mais, obrigatoria), `--agente` (repetivel, minimo um), `--pergunta` (arquivo opcional com pergunta extra), `--dono` e `--pendente` (como no debate; `--pendente` obrigatorio da rodada 4). A entrada-alvo vai inteira no prompt, e o envelope diz que se avalia a **disposicao**, nao o achado.

## Comandos Somente-Leitura Por Ferramenta

O agente de parecer nao escreve nada. Use o modo que a propria CLI oferece para isso:

| Ferramenta | Comando para `--agente` |
|---|---|
| Codex | `codex exec -s read-only --skip-git-repo-check` |
| cursor-agent (Grok e outros) | `cursor-agent -p --mode ask --force` |

Modelo e esforco entram como flags da CLI (`-m <modelo>`, `-c model_reasoning_effort="high"`, `--model <modelo>`) e **vem dos perfis de consenso em `docs/MEMORY.md`, secao `## User`**, nunca de um nome de modelo inventado ou guardado na skill. Confira o nome na `--help` ou na lista de modelos da propria CLI.

A copia isolada torna a escrita inofensiva: o que o agente gravar morre com a copia. Mas **a leitura e o que vale**. Ele le o projeto inteiro da copia (inclusive `.git` e arquivos de ambiente, que a copia nao exclui), e o isolamento real vem de material separado por participante, nunca de pedir cegueira no prompt. Por isso o modo somente-leitura e boa pratica, nao a garantia.

## O Que A Execucao Garante

- Uma copia por participante, em diretorio temporario fora do projeto, sem `docs/consensus/`, sem `.consenso-lock` e sem `__pycache__`.
- Debate rodada 1: as entradas de `CONSENSUS.md` ficam retidas na copia (os modelos cercados ficam). Rodada 2 em diante e achado levam `CONSENSUS.md` inteiro: o publicado e anterior, e na revalidacao a entrada sob revisao e o objeto da pergunta.
- Rodada 2 em diante leva as posicoes anteriores **na integra, depois da pergunta**. Resumo ali devolveria o problema de quem transcreve a critica ser o criticado.
- Bruto e manifesto gravados assim que cada agente termina, antes de qualquer minuta.
- `CONSENSUS.md` so muda no fim, uma vez, por substituicao atomica do arquivo inteiro. Rodada interrompida o deixa byte a byte como estava.
- Travessao (U+2014) na saida do agente vira hifen so na minuta; o bruto fica intacto.

## Exit Codes

| Codigo | Significado |
|---|---|
| 0 | rodada `concluida`: minuta (debate) ou revalidacao (achado) escrita em `CONSENSUS.md`. Vale tambem com falha de um agente, se ao menos um deu posicao; a falha aparece em `**Falhas:**` |
| 1 | erro de uso ou recusa antes de chamar agente (pergunta ou projeto inexistente, `--rodada` ou `--anterior` ou `--pendente` inconsistentes, entrada de achado inexistente ou repetida, id repetido, `docs/consensus/` no `.gitignore`); ou rodada **interrompida** por SIGINT ou SIGTERM, com `status=interrompida` no manifesto; ou escrita recusada, com `status=recusada-na-escrita` |
| 2 | nenhum participante deu posicao (`status=sem-posicao`); `CONSENSUS.md` intacto |
| 5 | outra rodada ja esta ativa no projeto (lock `.consenso-lock`); nenhum arquivo foi alterado por esta chamada |
| 6 | padrao de segredo: na pergunta, na entrada ou num `--anterior` (nenhum agente foi chamado, nada foi gravado), ou na saida de um agente (`status=parada-segredo`, bruto guardado fora do projeto, nenhuma minuta) |

Os codigos 3 e 4 do `loop.sh` nao existem aqui. As mensagens de interrupcao, de lock ocupado e de exit 6 **citam** o comando de retomada com o run-id; nenhuma mensagem o executa.

## Sidecar Em `docs/consensus/`

Cada rodada ganha a pasta `docs/consensus/<AAAA-MM-DD-HHMMSS>-<modo>/` (com sufixo `-2`, `-3` se duas caem no mesmo segundo):

```text
docs/consensus/<run-id>/
  manifesto.json     # comando integral, diretorio, exit, hashes de insumo e saida
  pergunta.txt       # copia da pergunta (debate; achado, se houve --pergunta)
  entrada.txt        # a entrada sob revisao (so achado)
  <id>/prompt.txt    # exatamente o que o agente recebeu
  <id>/stdout.txt    # a posicao, bruta
  <id>/stderr.txt
```

O manifesto guarda `status` (`em-andamento`, `concluida`, `interrompida`, `parada-segredo`, `sem-posicao`, `recusada-na-escrita`), a rodada, os participantes e seus resultados (`posicao`, `falha`, `retido-por-segredo`), os `anteriores` com hash, os `agentes` e as `retomadas`. O sidecar **mora no repositorio e nao pode ir para o `.gitignore`**: sem o bruto ao lado, ninguem confere a minuta, e a operacao recusa rodar com `docs/consensus/` ignorado.

## Forma Da Entrada

A entrada nasce com `**Status:** aberto` e `**Proximo passo:**` com dono humano, e traz a ponte para o sidecar:

- `**Origem:** automacao` marca a entrada como automatizada. Sem ela, o validador nao cobra nada novo.
- `**Manifesto:**` lista, por caminho a partir da raiz, o manifesto de cada rodada (`docs/consensus/<run-id>/manifesto.json`).
- `**Participantes:**` lista os ids que rodaram; `**Falhas:**` os que falharam (`nenhuma` e lista vazia).
- Debate: `### Posicao De <id>` por participante com posicao, `### Falha De <id>` por falha, e as secoes de julgamento com `- (A preencher.)`.
- Achado: `### Revalidacao De <id>` por participante e `### Falha De <id>` por falha, inseridas na entrada existente. Status, achado e o resto ficam como estavam.
- As posicoes entram em citacao Markdown, linha a linha, sem resumo.

O validador (`validate_structure.py`) confere por AVISO que cada id de `**Participantes:**` tem a secao, que cada id de `**Falhas:**` tem `### Falha De <id>` e que cada manifesto resolve. Avisos so travam o exit code com `--strict`.

## Rodada 2 E Achado

Na rodada 2 em diante, o numero da rodada e as posicoes anteriores sao escolha da pessoa: o script nao deduz nenhum dos dois. No debate, `**Exposicao previa a outras posicoes:**` e `nao` na rodada 1 e `sim` da 2 em diante. No achado e sempre `sim`, porque a entrada sob revisao esta a vista. Da rodada 4, `--pendente` e obrigatorio.

Revalidar um achado e uma rodada como qualquer outra: quem revalida e outro modelo, a disposicao continua de quem registrou o achado, e a rodada conta em `**Rodada:** N de N`.

## Retomada

Rodada que nao chegou a `concluida` (interrompida, parada por segredo, sem posicao, escrita recusada) se continua **so por comando explicito**:

```bash
consenso.py retomar --projeto DIR <run-id>
```

Quem ja tem `<id>/stdout.txt` fica como esta, sem nova chamada. Quem nao tem roda de novo, em copia isolada e com a varredura de segredo de sempre. Material retido por segredo que a pessoa **moveu a mao** para `<run-id>/<id>/` vira posicao (`aceito_por_humano` no manifesto), sem varredura nova: a palavra humana ja foi dada. Se todos os brutos existem, so escreve a minuta.

Recusa com exit 1: run inexistente, run `concluida`, manifesto de versao anterior sem os parametros, pergunta ou entrada diferentes do hash gravado. Lock ocupado sai 5; segredo na pergunta, na entrada ou num anterior sai 6.

## Segredo Na Saida

Antes de gravar qualquer bruto, a operacao varre stdout e stderr atras de: chave AWS (`AKIA...`), cabecalho de chave privada PEM, rotulo com valor (`api_key`, `token`, `secret`, `password` seguidos de `=` ou `:` e 16 ou mais caracteres), prefixos `ghp_`, `sk-` e `xox`, e URL com senha. Achou: a rodada **para**, o material fica fora do projeto, o caminho e informado e sai 6. **Nada e redigido**, porque redacao destruiria a evidencia que o bruto existe para guardar. Para aceitar, a pessoa le o material, move a mao e manda retomar.

## O Que A Operacao Nunca Faz

- **Sintetizar** as posicoes. Elas entram literais.
- **Declarar convergencia** nem dizer que ha acordo.
- **Decidir por maioria.** Sem convergencia, quem decide e o usuario.
- **Escrever julgamento.** `Pontos De Acordo`, `Riscos E Tradeoffs`, `Consenso Final` e `Decisao Para Registrar Em DECISIONS.md` nascem com `- (A preencher.)` e sao da pessoa. Status e `aberto`; fechar e dela.
- **Redigir segredo.** Ou o bruto entra como veio, ou nao entra.
- **Retomar sozinha.** Retomada e palavra humana, por comando.
- Deduzir o numero da rodada, as posicoes anteriores ou o modelo do agente.
- Inventar posicao de agente que nao rodou.

## Limites Declarados

- **A varredura de segredo tem falso negativo.** Ela cobre os padroes acima e nada mais: qualquer segredo de outro formato passa e entra no repositorio. Tem tambem falso positivo, que para uma rodada legitima ate alguem olhar. A varredura olha o que o agente escreveu, nao o que ele leu na copia.
- **Nao ha teto de custo.** N agentes, esforco alto e rodada 2 em diante queimam plano: modelo caro (como o Sol) so quando a pessoa pedir.
- **`docs/MEMORY.md` desatualizado dispara o revisor errado.** O script nao le a memoria; o agente de chat le e monta o `--agente`. Perfil velho vira modelo velho.
- Um argumento de comando aceita cerca de 128KB no Linux: prompt maior falha na execucao do agente (exit 127, registrado como falha dele) e nunca e truncado.
- A entrada e escrita so em `CONSENSUS.md` com fim de linha LF.
- Os campos `**Metodo:**` e `**Exposicao previa a outras posicoes:**` agora descrevem um fato da execucao, mas o validador continua checando forma, nao veracidade.
- O filho do Cloudroom (`scripts/cloudroom_agente.py`) nao entra como participante: ele roda na pasta da thread, onde o `consenso.py` grava o bruto de cada participante, o que quebra a rodada 1 cega, e a sandbox propria nao devolve a resposta. Detalhe em `references/cloudroom.md`.

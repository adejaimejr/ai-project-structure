# CONSENSUS

Use este arquivo quando modelos diferentes precisarem debater para chegar a um consenso.

Ele nao substitui `DECISIONS.md`. Quando o debate gerar uma decisao importante, copie a decisao final para `DECISIONS.md`.

## Quando Usar

Use este arquivo quando:

- houver discordancia entre agentes;
- a decisao tiver impacto em arquitetura, produto, dados, seguranca ou custo;
- a tarefa tiver risco alto;
- o usuario pedir opiniao de outro modelo;
- a resposta correta depender de tradeoffs.

Nao use para decisoes simples ou tarefas obvias.

## Entrada Automatizada

Quando a rodada e rodada por `consenso.py` (da skill `ai-project-structure`), a entrada nasce de uma minuta escrita pelo script, nao por um modelo. Ela e a mesma entrada do modelo abaixo, com campos a mais que ligam o texto ao que a execucao comprova:

- `**Origem:**` `automacao`. Marca a entrada como automatizada. O validador so cobra os campos abaixo de quem declara este.
- `**Manifesto:**` caminho, a partir da raiz, do manifesto de cada rodada (`docs/consensus/<run-id>/manifesto.json`), separados por virgula. Ali ficam o comando integral, o diretorio, o exit code e os hashes de insumo e saida; a entrada traz so a ponte.
- `**Participantes:**` ids dos agentes que rodaram, separados por virgula. Cada id tem a secao `### Posicao De <id>` (na revalidacao de achado, `### Revalidacao De <id>`).
- `**Falhas:**` ids que falharam, ou `nenhuma`. Cada id tem a secao `### Falha De <id>`, no lugar da posicao.

O bruto de cada agente fica em `docs/consensus/<run-id>/<id>/stdout.txt` e **nao pode ir para o `.gitignore`**: sem ele ninguem confere a posicao. As posicoes entram literais, em citacao, sem resumo. As secoes de julgamento nascem com "(A preencher.)" e sao de quem le: o script nao sintetiza, nao declara convergencia e nao decide por maioria. A entrada nasce com `**Status:** aberto`. Os campos `Metodo`, `Exposicao previa a outras posicoes` e `Rodada` passam a descrever um fato da execucao; o validador continua checando a forma, nunca a veracidade.

## Modelo De Debate

```md
## AAAA-MM-DD - Tema do consenso

**Status:** aberto | resolvido | arquivado

**Proximo passo:** (preencher quando o status for `aberto`, com dono claro)

**Metodo:** pareceres-independentes | debate-aberto

**Exposicao previa a outras posicoes:** sim | nao

**Rodada:** 1 de 1

### Contexto

- 

### Pergunta Ou Decisao

- 

### Posicao Do Codex

- 

### Posicao Do Claude

- 

### Posicao Do Gemini

- 

### Pontos De Acordo

- 

### Riscos E Tradeoffs

- 

### Consenso Final

- 

### Decisao Para Registrar Em DECISIONS.md

- 
```

## Achado

Nem todo uso deste arquivo e debate. Quando a validacao cruzada encontra um defeito, risco ou lacuna, isso e um **achado**, e vira entrada propria, com `**Status:**` e `**Proximo passo:**` proprios.

- `**Achado:**` traz o identificador do achado. Ele e livre, amarrado a unidade de trabalho do projeto (`N10`, `API-3`, o que o projeto ja usar): o validador confere que o campo existe e tem valor, e nunca opina sobre o valor.
- `**Escapou de verificacao:**` `sim` ou `nao`, dizendo se a verificacao que ja existia deixou o achado passar. Declarou `sim`? A entrada traz a secao `### Por Que Nada Pegou Antes`.
- A disposicao do achado e de quem o registra; a revalidacao dela e de outro modelo, e conta como rodada.
- Achado so vira tarefa em `TASKS.md` depois de a disposicao concluir que ha trabalho, e a tarefa cita o achado na linha.

Nao ha teto de rodadas. Da quarta rodada em diante a entrada declara `**Pendente da rodada anterior:**`, dizendo o que a rodada anterior deixou em aberto.

## Ponto Cego Da Validacao Cruzada

Rodada verde e ausencia de objecao, nao prova de que funciona. Modelos que leem o mesmo texto herdam o mesmo ponto cego, e defeito que so existe em contexto de execucao real sobrevive a N rodadas de leitura.

## Modelo De Achado

```md
## AAAA-MM-DD - Titulo curto do achado

**Achado:** <identificador livre, ex: N10>

**Status:** aberto | resolvido | arquivado

**Proximo passo:** (preencher quando o status for `aberto`, com dono claro)

**Metodo:** pareceres-independentes | debate-aberto

**Exposicao previa a outras posicoes:** sim | nao

**Rodada:** 1 de 1

**Escapou de verificacao:** sim | nao

**Pendente da rodada anterior:** (obrigatorio da rodada 4 em diante)

### Contexto

- 

### O Que Foi Encontrado

- 

### Disposicao

- (o que quem registrou o achado decidiu fazer, e por que)

### Revalidacao

- (modelo distinto avaliando a disposicao acima, nao o achado em si)

### Por Que Nada Pegou Antes

(obrigatoria quando `**Escapou de verificacao:**` for `sim`; corte a secao quando for `nao`)

- O que passou verde: 
- Mecanismo do ponto cego: 
- Conserto de portao proposto: 

### Decisao Para Registrar Em DECISIONS.md

- 
```

## Registros

As entradas anteriores a 2026-09-03 (e as duas rodadas de P-7/P-8 e P-9 da spec 0006, que continuam `aberto` aguardando calibragem do usuario em T-053) foram rotacionadas para `docs/archive/CONSENSUS-2026.md`. Abaixo ficam os dois achados mais recentes da revalidacao adversarial de 2026-09-03 (REVAL-6 e REVAL-7). A entrada REVAL-5 (fluxos de scaffold, atualizacao e specs), unica que fechou `resolvido` sem defeito, foi rotacionada no mesmo dia para `docs/archive/CONSENSUS-2026.md` por tamanho; REVAL-1 a REVAL-4, todas `resolvido`, foram rotacionadas para o mesmo arquivo em 2026-10-21, antes da bancada real da automacao do consenso (T-083), porque o arquivo estava a poucos bytes do teto de 30KB.

## 2026-10-21 - Diretorio de corrida incompleto em docs/consensus/ (T-083)

**Status:** aberto

**Proximo passo:** usuario le as posicoes e preenche as secoes de julgamento

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Origem:** automacao

**Manifesto:** docs/consensus/2026-10-21-043054-debate/manifesto.json

**Participantes:** codex, sol

**Falhas:** nenhuma

### Contexto

- Modo: debate
- Rodada: 1 de 1
- N: 2
- Data: 2026-10-21
- Manifesto: docs/consensus/2026-10-21-043054-debate/manifesto.json

### Pergunta Ou Decisao

> O que o validador (scripts/validate_structure.py) deve fazer com um diretorio de corrida incompleto em docs/consensus/ (manifesto com status em-andamento ou interrompida, participante sem stdout.txt, ou pasta sem manifesto.json)? Opcoes em jogo: ignorar por completo (como hoje), avisar so quando uma entrada de docs/CONSENSUS.md aponta para ele, ou avisar sempre que existir. Considere a DEC-009 da spec 0006 (bruto e manifesto moram no repositorio desde o inicio; retomada so por comando explicito) e o custo de falso positivo numa rodada legitimamente em andamento. Leia o codigo do validador e do consenso.py na copia antes de responder.

### Posicao De codex

> O validador deve avisar somente quando uma entrada de `docs/CONSENSUS.md` apontar para o diretório incompleto.
> 
> Isso preserva a DEC-009: o material bruto e o manifesto podem existir no repositório desde o início, e uma corrida só é retomada por comando explícito. Portanto, uma pasta isolada, inclusive com manifesto `em-andamento`, `interrompida`, participante sem `stdout.txt` ou sem manifesto, não prova corrupção nem exige intervenção.
> 
> Já uma referência em `CONSENSUS.md` transforma aquele diretório em evidência declarada de uma rodada. Nesse caso, a incompletude quebra a rastreabilidade e o aviso é apropriado.
> 
> Avisar sempre criaria falso positivo durante uma rodada legítima em andamento. Ignorar sempre permitiria referências documentais quebradas sem detecção.

### Posicao De sol

> Não consegui ler a cópia: as tentativas de acesso falharam antes de executar os comandos, com `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
> 
> Sem ler `scripts/validate_structure.py`, `consenso.py` e a DEC-009 completa, não tenho base para emitir o parecer solicitado. Escolher uma opção agora contrariaria sua exigência de leitura e a regra “Nunca Inferir”.
> 
> É necessário restabelecer o acesso à cópia ou fornecer o conteúdo desses arquivos. Nenhum arquivo foi alterado.

### Pontos De Acordo

- (A preencher.)

### Riscos E Tradeoffs

- (A preencher.)

### Consenso Final

- (A preencher.)

### Decisao Para Registrar Em DECISIONS.md

- (A preencher.)

## 2026-10-21 - Diretorio de corrida incompleto em docs/consensus/ (T-083, segunda rodada 1 cega, sandbox sem bubblewrap)

**Status:** aberto

**Proximo passo:** usuario le as posicoes e preenche as secoes de julgamento

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Origem:** automacao

**Manifesto:** docs/consensus/2026-10-21-114042-debate/manifesto.json

**Participantes:** codex, sol

**Falhas:** nenhuma

### Contexto

- Modo: debate
- Rodada: 1 de 1
- N: 2
- Data: 2026-10-21
- Manifesto: docs/consensus/2026-10-21-114042-debate/manifesto.json

### Pergunta Ou Decisao

> O que o validador (scripts/validate_structure.py) deve fazer com um diretorio de corrida incompleto em docs/consensus/ (manifesto com status em-andamento ou interrompida, participante sem stdout.txt, ou pasta sem manifesto.json)? Opcoes em jogo: ignorar por completo (como hoje), avisar so quando uma entrada de docs/CONSENSUS.md aponta para ele, ou avisar sempre que existir. Considere a DEC-009 da spec 0006 (bruto e manifesto moram no repositorio desde o inicio; retomada so por comando explicito) e o custo de falso positivo numa rodada legitimamente em andamento. Leia o codigo do validador e do consenso.py na copia antes de responder.

### Posicao De codex

> Minha posição: avisar somente quando `docs/CONSENSUS.md` apontar para a corrida.
> 
> DEC-009 torna diretórios incompletos um estado normal: o manifesto nasce como `em-andamento`, o bruto é salvo antes da minuta e uma interrupção preserva esse material no repositório sem alterar `CONSENSUS.md`. Avisar sempre transformaria uma rodada legítima em andamento em falso positivo, inclusive se alguém rodar o validador durante a execução.
> 
> O escopo correto é a integridade de uma alegação publicada:
> 
> - Sem ponte em `CONSENSUS.md`: ignorar pasta sem manifesto, manifesto não concluído e participante sem `stdout.txt`. O `consenso.py retomar` é o mecanismo explícito para inspecionar e continuar esse estado.
> - Com ponte em `**Manifesto:**`: avisar se o manifesto não existe, não pode ser lido, não tem `status: concluida`, ou se um participante registrado como artefato da rodada não tem o `stdout.txt` esperado. Uma entrada publicada jamais deveria apontar para corrida ainda em curso, pois o script só escreve a minuta no fim e só marca `concluida` depois dela.
> - Severidade: AVISO, bloqueante apenas em `--strict`, coerente com os checks opt-in de `**Origem:**` da DEC-007.
> 
> Hoje o validador já segue parcialmente esse limite: só verifica se o caminho de manifesto citado resolve. Ele não varre `docs/consensus/` nem interpreta o conteúdo do manifesto. Eu estenderia essa verificação vinculada, sem adicionar uma varredura global do sidecar.

### Posicao De sol

> Minha recomendação é **avisar somente quando uma entrada automatizada de `docs/CONSENSUS.md` aponta para a corrida incompleta**, preservando o opt-in por `**Origem:**`. O diagnóstico deve ser AVISO, coerente com a DEC-007.
> 
> A DEC-009 torna a existência de material incompleto no repositório um estado previsto. Ela não exige que toda corrida seja retomada ou publicada. Avisar sempre transformaria uma execução legítima, ou uma interrupção preservada corretamente, em falha de `--strict`.
> 
> O código confirma essa distinção:
> 
> - `abrir_rodada()` cria a pasta antes da gravação do manifesto. Existe uma janela legítima com pasta sem `manifesto.json`.
> - `_rodar_debate()` grava o manifesto como `em-andamento` antes de executar os agentes. Os arquivos `stdout.txt` aparecem conforme cada participante termina.
> - Uma interrupção pode deixar participantes sem registro nem stdout, deliberadamente. `_retomar()` identifica esses participantes e só os chama mediante comando explícito.
> - `fechar_debate()` publica a minuta antes de selar o manifesto como `concluida`.
> 
> Esses comportamentos estão em [consenso.py](/tmp/consenso-5emyxgmf/projeto/docs/skills/ai-project-structure/scripts/consenso.py:385). Portanto, incompletude isolada não comprova defeito.
> 
> Eu adotaria esta regra:
> 
> | Situação | Comportamento |
> |---|---|
> | Corrida sem referência em entrada automatizada | Não emitir diagnóstico de incompletude |
> | Entrada aponta para manifesto ausente | AVISO, como já ocorre |
> | Entrada aponta para manifesto ilegível ou com status `em-andamento` ou `interrompida` | AVISO de proveniência incompleta |
> | Entrada aponta para corrida cujo bruto esperado está ausente | AVISO, identificando corrida e participante |
> | Stdout existe, mas está vazio por falha registrada | Não considerar incompleto apenas pelo tamanho |
> 
> Hoje, [check_consensus_origem()](/tmp/consenso-5emyxgmf/projeto/docs/skills/ai-project-structure/scripts/validate_structure.py:572) verifica a existência do manifesto, mas explicitamente não examina seu conteúdo. Assim, **a opção intermediária exige ampliar a verificação**: um manifesto existente pode esconder status incompleto ou ausência do bruto. Ignorar esses problemas mesmo depois da publicação enfraquece a ponte de proveniência da DEC-008.
> 
> Há uma ressalva de concorrência: como a minuta e o manifesto são gravados separadamente, o validador pode observar a entrada recém-publicada antes do status `concluida`. O aviso deve descrever o estado observado, sem afirmar corrupção ou abandono. Uma nova validação após o encerramento resolve essa janela. Eu não acrescentaria heurísticas de idade ou existência do lock: o lock é por projeto e pode ficar órfão.
> 
> O custo aceito dessa escolha é deixar corridas interrompidas sem referência fora do diagnóstico padrão. Se houver necessidade de descobrir material esquecido, isso cabe numa inspeção explícita de corridas pendentes. Não deve impor a obrigação de retomar, apagar ou publicar material para obter validação verde.
> 
> O validador também não deve retomar corridas, limpar locks ou reparar artefatos. A DEC-009 reserva a retomada ao comando humano explícito.

### Pontos De Acordo

- (A preencher.)

### Riscos E Tradeoffs

- (A preencher.)

### Consenso Final

- (A preencher.)

### Decisao Para Registrar Em DECISIONS.md

- (A preencher.)

## 2026-10-21 - Spec 0008, P-2 e P-3: adaptador Cloudroom e isolamento por copia (rodada 1 cega)

**Status:** resolvido

**Proximo passo:** nenhum; ratificado pelo usuario em 2026-10-21 no chat, sobre texto redigido pelo Opus (coordenador, nao participante).

**Metodo:** pareceres-independentes

**Exposicao previa a outras posicoes:** nao

**Rodada:** 1 de 1

**Origem:** automacao

**Manifesto:** docs/consensus/2026-10-21-161813-debate/manifesto.json

**Participantes:** luna, terra

**Falhas:** nenhuma

### Contexto

- Modo: debate
- Rodada: 1 de 1
- N: 2
- Data: 2026-10-21
- Manifesto: docs/consensus/2026-10-21-161813-debate/manifesto.json

### Pergunta Ou Decisao

> Spec 0008 (docs/specs/0008-adaptador-cloudroom.md, em Rascunho), perguntas P-2 e P-3.
> 
> Contexto: a skill quer que `loop.sh` e `consenso.py` possam usar um subagente do Cloudroom (`room-cli thread spawn`) como agente, por um wrapper `scripts/cloudroom_agente.py` que se comporta como CLI headless, sem mudar os dois scripts. A spec propoe (DEC-002 e DEC-003) que o wrapper sirva so ao loop e que o consenso fique fora.
> 
> Fatos medidos com a CLI real (cloudroom 0.1.67, 2026-10-21), que voce nao consegue reproduzir daqui e deve tomar como dados:
> - `room-cli thread spawn` aceita so `--provider --model --reasoning-level --service-tier --title --shared-sandbox|--top-level --prompt|--prompt-file` e recusa qualquer outra opcao; nao ha opcao de diretorio.
> - Com `--shared-sandbox`, o filho rodou na pasta da thread pai: pedido para imprimir `pwd`, respondeu `/code/ai-project-structure`, independentemente de onde o pai estava.
> - Sem `--shared-sandbox`, o filho ganha sandbox propria com copia do codigo (commits e nao commitados) em outra branch; nao aparece em `thread list`, e `thread output` devolve so a nota "Its replies arrive as messages when its turns end".
> 
> P-2: com `--shared-sandbox`, da para manter o isolamento por copia por participante da DEC-003 da spec 0006 (docs/specs/0006-automacao-do-consenso.md)? Se nao, o que sobra e verificavel?
> P-3: o modo sem `--shared-sandbox` serve ao consenso, atrapalha, ou e inviavel? Em qual modo cada pacote (debate, achado, loop) deve rodar, ou nenhum?
> 
> Leia o codigo antes de opinar: `docs/skills/ai-project-structure/scripts/consenso.py` (copia, prompt, gravacao do bruto), `scripts/loop.sh` (como chama o agente, `find -newer`, `--tempo-maximo`) e as DEC-003 e DEC-009 da spec 0006. Concorde ou discorde de DEC-002 e DEC-003 da spec 0008 com motivo, aponte o que estiver errado ou faltando, e proponha alternativa verificavel se houver. Responda em portugues, sem o caractere travessao.

### Posicao De luna

> ## P-2: `--shared-sandbox` não preserva o isolamento da DEC-003
> 
> Discordo da DEC-002 como conclusão sobre o modo compartilhado. A evidência sustenta que o filho não começa na pasta de trabalho corrente do processo que o chamou: começa na pasta da thread pai. Portanto, passar o caminho da cópia no prompt, ou fazer `cd` antes de chamar `room-cli`, não prende o filho nessa cópia.
> 
> Isso quebra o isolamento de `consenso.py`. O script cria uma cópia por participante, remove `docs/consensus/` e, no debate, retém os registros anteriores de `docs/CONSENSUS.md`. Mas o adaptador chamado como agente receberia um prompt que aponta para uma cópia e abriria o filho no espaço compartilhado da thread pai. O caminho no prompt não impede o filho de ler outros arquivos disponíveis nesse espaço. Como `consenso.py` grava cada bruto assim que o participante termina, um participante posterior também poderia alcançar a posição anterior se ela estiver nesse espaço. Isso contraria tanto a DEC-003 da 0006 quanto o critério de aceite que exige isolamento verificável sem confiar no relato do agente.
> 
> O que sobra verificável com a proposta atual é uma afirmação de escopo: o adaptador não será usado nos perfis de debate e achado, e a documentação explicará o motivo. Isso não demonstra isolamento; evita alegá-lo. A alternativa verificável já existe no código: deixar `consenso.py` chamar os agentes diretamente, preservando a cópia separada por participante, a retenção dos registros no debate e a gravação dos brutos fora das cópias de execução. Para voltar a considerar Cloudroom no consenso, seria necessário um modo de execução que comprovadamente desse a cada filho um espaço distinto, com captura da resposta integral e sem acesso às posições contemporâneas. Os fatos fornecidos não mostram que a CLI ofereça isso.
> 
> ## P-3: sandbox própria não serve aos três pacotes automatizados
> 
> Concordo com a DEC-003 em excluir o modo sem `--shared-sandbox` dos pacotes automatizados, mas ajustaria a explicação: pelo comportamento medido, ele não é apenas inconveniente. O adaptador não consegue obter a resposta pelo `thread output`; recebe somente a nota de que as respostas chegam como mensagens quando os turnos terminam. Logo, não consegue cumprir o contrato de CLI do wrapper, que precisa devolver a resposta pelo stdout e um exit code.
> 
> Para o consenso, há também um problema de isolamento e proveniência. A cópia privada leva o conteúdo existente, incluindo `docs/CONSENSUS.md` e `docs/consensus/`. Ela não fornece a cópia específica por participante, preparada por `consenso.py` segundo o debate ou o achado. Além disso, sem a resposta no processo, `consenso.py` não pode gravar o bruto e o manifesto quando o participante termina, como exige a DEC-009 da 0006.
> 
> Para o loop, o filho trabalha numa cópia em outra branch. O `loop.sh` verifica alterações com `find -newer` na árvore de `$PROJETO` e executa o portão ali. Alterações feitas apenas na cópia privada não satisfazem esse fluxo. A falta de resposta capturável também impede o adaptador de entregar ao loop a saída esperada.
> 
> Assim, minha recomendação por pacote é:
> 
> | Pacote | Modo recomendado |
> |---|---|
> | Debate | Nenhum modo Cloudroom medido. Manter os agentes diretos de `consenso.py`. |
> | Achado | Nenhum modo Cloudroom medido. Manter os agentes diretos de `consenso.py`. |
> | Loop | `--shared-sandbox`, condicionado a o espaço compartilhado corresponder ao projeto que o loop precisa alterar. |
> 
> Há uma ressalva importante à DEC-004 da spec 0008: o `loop.sh` aceita `--projeto DIR` e roda o comando do agente após `cd "$PROJETO"`, mas o `room-cli` medido inicia o filho na pasta da thread pai, independentemente do diretório do chamador. Portanto, não está demonstrado que o filho sempre alterará o `$PROJETO` indicado. A bancada descrita em T-103 pode validar o caso em que o projeto coincide com a pasta compartilhada da thread; não sustenta, sozinha, uma alegação para qualquer `--projeto`. Eu restringiria a documentação a esse caso demonstrado, ou exigiria que o critério real prove que o filho altera o caminho indicado pelo loop e que o `find -newer` o detecta.
> 
> Em resumo: manteria o adaptador restrito ao loop e fora do consenso, mas mudaria os fundamentos registrados. Para o consenso, `--shared-sandbox` falha no isolamento por participante; sem compartilhamento, falha na coleta mecânica da resposta e no acesso à cópia preparada para cada participante. Para o loop, o compartilhamento é o único modo plausível entre os dois, mas sua compatibilidade com `--projeto` precisa ser delimitada ao que a bancada real comprovar.

### Posicao De terra

> Discordo de usar o adaptador no consenso e concordo com DEC-002 e DEC-003, com uma ressalva de escopo para o loop.
> 
> **P-2: `--shared-sandbox` não preserva o isolamento da DEC-003.** O `consenso.py` cria uma cópia temporária por participante, remove `docs/consensus/` dela e, no debate de rodada 1, retém os registros de `CONSENSUS.md`. Porém o Cloudroom inicia o filho no workspace da thread pai, não no `cwd` da chamada do wrapper nem na cópia passada ao `executa()`.
> 
> Assim, o caminho da cópia no prompt é somente instrução. Não impede o filho de ler o projeto real. Isso viola a propriedade relevante da DEC-003: separar o material acessível a cada participante, não apenas pedir que ignore conteúdo.
> 
> Também conflita diretamente com a DEC-009. Enquanto os participantes executam em paralelo, `rodar_participantes()` grava `stdout.txt`, `stderr.txt` e `manifesto.json` no `docs/consensus/<run>/` real assim que cada um termina. Um filho compartilhado ainda em execução pode ler esse sidecar. Logo, “bruto e manifesto gravados onde agentes contemporâneos não alcançam” deixa de ser verdadeiro.
> 
> O que sobra verificável é mais estreito:
> 
> - O orquestrador criou cópias distintas e registrou seus caminhos no manifesto.
> - O wrapper chamou o Cloudroom em modo compartilhado e coletou uma resposta.
> - A política pode proibir perfis de consenso que apontem para o wrapper.
> 
> Nada disso prova que o participante trabalhou na cópia, nem que não leu a posição contemporânea.
> 
> **P-3: sem `--shared-sandbox` é inviável para o contrato atual do wrapper.** Embora dê uma sandbox própria, o processo que chama `room-cli` não consegue consultar a saída, esperar uma conclusão observável nem receber o exit code do filho. A resposta vai como mensagem para a thread pai, fora do stdout do wrapper. Além disso, a alteração fica em outra branch, então o `find -newer` e o portão do `loop.sh` observam o projeto pai inalterado.
> 
> A cópia implícita desse modo também não é a cópia preparada por `consenso.py`: ela não garante a exclusão de `docs/consensus/`, a retenção dos registros na rodada 1, nem a entrada exata de achado que deve ficar visível.
> 
> Minha matriz é:
> 
> | Pacote | Modo recomendado |
> |---|---|
> | Debate | Nenhum modo Cloudroom atual. Manter CLI direta executada na cópia por participante. |
> | Achado | Nenhum modo Cloudroom atual. Manter CLI direta, com a entrada sob revisão no material isolado. |
> | Loop | `--shared-sandbox`, desde que o projeto alvo seja o workspace da thread pai. |
> | Sem compartilhamento | Nenhum dos três. |
> 
> A ressalva para o loop é importante: DEC-004 afirma que o filho pode editar o caminho absoluto de `$PROJETO`. A sonda de `pwd` prova apenas o diretório inicial do filho, não que qualquer valor de `--projeto` seja montado e gravável pelo filho. O adaptador deve documentar e testar o pré-requisito: ele serve para executar o loop no projeto da thread Cloudroom que o iniciou. Não deve prometer funcionar com um projeto arbitrário passado por `--projeto`.
> 
> A alternativa verificável para permitir consenso no futuro exige uma capacidade nova do Cloudroom, não um ajuste de prompt:
> 
> 1. `spawn` precisa aceitar uma raiz de workspace ou uma cópia privada por participante.
> 2. Essa raiz deve ser a única árvore do projeto montada ao filho, sem acesso ao projeto pai e ao sidecar contemporâneo.
> 3. A API precisa expor polling programático de resposta, estado e erro para esse tipo de filho.
> 4. A bancada precisa demonstrar, por observação do ambiente e não pela declaração do modelo, que a escrita relativa cai na cópia certa e que `docs/consensus/<run>/` do pai não está acessível.
> 
> Enquanto isso não existir, o caminho direto já usado por `consenso.py` é a alternativa correta: ele inicia o comando com `cwd` igual à cópia específica, registra prompt, saída, hashes e diretório no manifesto, e preserva o desenho de DEC-003 e DEC-009.
> 
> Portanto, manter DEC-002 é correto. Manter DEC-003 também é correto, mas eu acrescentaria explicitamente que a inviabilidade do modo sem compartilhamento é do contrato headless atual, e que o suporte do modo compartilhado ao loop é limitado ao workspace da thread pai.

### Pontos De Acordo

- Os dois concordam que o adaptador serve so ao `loop.sh`. No consenso, o modo compartilhado quebra o isolamento por copia (o filho le o projeto real e o bruto do outro participante gravado em `docs/consensus/`), e o modo de sandbox propria nao devolve a resposta ao processo que chamou.
- Os dois acharam, sem um ver o outro, o mesmo excesso na DEC-004 da spec 0008: a sonda de `pwd` prova so o diretorio inicial do filho, entao o loop so e garantido quando o `--projeto` e a pasta da thread.

### Riscos E Tradeoffs

- O consenso continua invisivel no Cloudroom, que era parte do motivo original da spec 0008.
- Ele so volta a ser opcao se o Cloudroom ganhar uma pasta isolada por filho, sem acesso ao projeto pai, e um jeito programatico de ler a resposta dele (requisitos listados pelo `terra`).

### Consenso Final

- DEC-002 e DEC-003 da spec 0008 ratificadas. DEC-004 restrita a `--projeto` igual a pasta da thread, ja aplicada na spec, nas tarefas T-102 e T-103 e no `portao_t102.py`.

### Decisao Para Registrar Em DECISIONS.md

- Sim: "O adaptador Cloudroom nao entra no consenso enquanto o Cloudroom nao isolar um filho por pasta", registrada em `docs/DECISIONS.md` em 2026-10-21.

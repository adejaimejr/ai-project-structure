# Adaptador Cloudroom

`scripts/cloudroom_agente.py` faz um filho do Cloudroom se comportar como CLI headless: recebe o prompt como ultimo argumento, imprime a resposta no stdout e sai com um codigo. Assim o `loop.sh` o aceita em `--agente` sem mudar uma linha. Ele so usa a biblioteca padrao do python3 e chama `room-cli thread spawn --shared-sandbox` por baixo: o filho aparece na barra do Cloudroom, com o titulo da tarefa, e roda na mesma sandbox da thread que chamou o loop.

## Uso

O adaptador so existe dentro de uma thread do Cloudroom, que e quem tem o `room-cli` no PATH. Sem `room-cli`, ele sai com 1 antes de qualquer chamada.

Comando de perfil (o que vai em `--agente`):

```bash
python3 <skill>/scripts/cloudroom_agente.py --provider claude-code --model claude-sonnet-5-5
```

A chamada do loop, com `--projeto` igual a pasta da thread:

```bash
<skill>/scripts/loop.sh --tarefa T-042 --projeto "$PWD" \
  --agente "python3 <skill>/scripts/cloudroom_agente.py --provider claude-code --model claude-sonnet-5-5"
```

Opcoes aceitas: `--provider` (obrigatorio), `--model`, `--reasoning-level`, `--service-tier`, `--titulo`, `--arquivar` e `--intervalo` (segundos entre consultas, padrao 10). O adaptador recusa qualquer outra, inclusive `--top-level`, `--prompt` e `--prompt-file`, com exit 1. O titulo da thread vem de `--titulo`; sem ele, `loop T-NNN` tirado do prompt; sem isso, a primeira linha do prompt (80 caracteres). O id do filho sai no stderr como `thread=<id>` desde o spawn. Com `--arquivar`, a thread filha e arquivada depois de a resposta ser lida com sucesso; sem a opcao ela fica na barra para conferir.

O adaptador nao tem tempo limite proprio: quem limita e o `--tempo-maximo` do loop.

## Exit Codes

| Codigo | Significado |
|---|---|
| 0 | Resposta integral do filho no stdout, mais uma quebra de linha. |
| 1 | Uso invalido, `room-cli` ausente do PATH ou spawn recusado pela CLI. |
| 2 | Filho falhou, foi parado ou terminou sem resposta; o erro vai para o stderr. |
| 143 | SIGTERM ou SIGINT recebido: o adaptador chama `room-cli thread stop ID` e sai em ate 5 s. |

## Limites Declarados

- **O adaptador nao serve ao `consenso.py`, nem em debate nem em achado.** O filho roda na pasta da thread, nao numa copia por participante, e le o projeto real, onde o `consenso.py` grava o bruto de cada participante assim que ele encerra: o segundo alcanca a posicao do primeiro e a rodada 1 cega deixa de ser cega. O `room-cli` nao tem opcao de diretorio para prender o filho numa copia.
- **Filho em sandbox propria fica fora.** Sem `--shared-sandbox` o filho nao aparece em `thread list` e `thread output` nao devolve a resposta, so avisa que ela chega como mensagem ao fim do turno; o adaptador nao tem como esperar nem coletar. Por isso ele acrescenta `--shared-sandbox` sempre e recusa pedir outro modo.
- **Thread Local no Mac nao foi exercitada.** So foi exercitado em thread Cloud: o comportamento de `--shared-sandbox` em thread Local no Mac nao foi conferido, e `--machine cloud` fica recusado.
- **O loop so vale com `--projeto` igual a pasta da thread do Cloudroom.** O filho compartilhado comeca na pasta da thread e escreve no mesmo sistema de arquivos, entao a deteccao de arquivo mexido e o tempo maximo do loop enxergam o trabalho dele. Com outro `--projeto`, nada garante que o filho escreva la: o adaptador nao promete isso.
- **O mock de `evals/mock_room_cli.py` e copia da CLI de 2026-10-21 (cloudroom 0.1.67).** A bateria passa contra essa copia, nao contra a CLI viva: se o `room-cli` mudar o formato de `thread spawn` ou de `thread output`, o mock envelhece e a bateria continua verde sem provar nada.

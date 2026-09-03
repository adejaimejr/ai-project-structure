---
name: ai-project-structure
version: "2.5.0"
description: Use sempre que o usuario quiser iniciar um projeto novo de IA, criar a estrutura inicial de um repositorio multiagente, ou fazer scaffold de um projeto Markdown que sera tocado por varias IAs. Dispare mesmo que o usuario nao mencione a skill por nome - basta o pedido envolver frases como "inicia projeto novo", "cria projeto", "scaffold projeto", "estrutura inicial", "novo repo de IA", "inicia projeto de IA", "monta a base do projeto", "cria a pasta do projeto", ou qualquer pedido para preparar um diretorio com AGENTS.md, CLAUDE.md, GEMINI.md e memoria em docs/ (SESSION, MEMORY, CONSENSUS, DECISIONS, TASKS, etc). Use tambem quando o usuario quiser converter um diretorio existente para esta estrutura, ATUALIZAR um projeto que ja usa a estrutura para a versao mais nova da skill, VALIDAR a estrutura existente, ativar o modulo de specs (docs/specs/) em um projeto existente, ou ativar, rodar e configurar o modulo de loop (perfis de modelo e esforco por intencao e ferramenta). Esta skill cria os arquivos de fato, nao apenas explica como criar.
---

# AI Project Structure

Esta skill **cria a estrutura Markdown multiagente em um projeto novo**, copiando os templates de `assets/` para o destino, preenchendo `PROJECT_CONTEXT.md` com nome e objetivo informados pelo usuario, e abrindo a primeira entrada em `SESSION.md`.

A estrutura tem como nucleo:
- raiz minima com arquivos de entrada dos agentes (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`);
- memoria do projeto em `docs/` com `PROJECT_CONTEXT`, `SESSION`, `MEMORY`, `CONSENSUS`, `TASKS`, `DECISIONS`, `QUALITY`, `CHANGELOG` e `archive/`;
- arquivos opcionais (`ARCHITECTURE`, `API`, `DATA_MODEL`, `GLOSSARY`, `ONBOARDING`, `ROADMAP`, `PROMPTS`, `STACK`);
- modulo opcional de specs (`docs/specs/`) para trabalho tamanho-feature;
- modulo opcional de loop, que executa uma tarefa verificavel sem supervisao. Nunca entra no scaffold e so pode ser ativado em projeto que ja tem comando real em "Testes E Validacao" de `QUALITY.md`.

A partir da versao 2.2.0 a estrutura tambem cobra que o trabalho seja verificavel:

- toda tarefa concluida em `TASKS.md` carrega uma sub-linha `Evidencia:`, e a tarefa aberta pode declarar antes como sera verificada com `(verifica: <comando>)`;
- tarefa travada por pergunta ao usuario vai para a secao `## Aguardando Usuario`, com a pergunta registrada e um campo para a resposta;
- cada entrada de `CONSENSUS.md` declara `Metodo`, `Exposicao previa a outras posicoes` e `Rodada`, para que consenso fraco nao fique parecido com consenso forte.

A partir da versao 2.4.0, `CONSENSUS.md` deixa de servir so para debate:

- entrada que declara `**Achado:** <identificador>` e um **achado**, com disposicao de quem registrou e revalidacao por outro modelo. O identificador e livre; o validador confere que o campo existe e tem valor;
- achado que declarou `**Escapou de verificacao:** sim` traz a secao `Por Que Nada Pegou Antes`, que transforma defeito escapado em conserto de portao;
- o teto de tres rodadas saiu. Da quarta rodada em diante a entrada declara `**Pendente da rodada anterior:**`.

## Fluxo

Execute na ordem.

### 0. Identifique o modo

Se o destino ja tem `AGENTS.md` e `docs/SESSION.md` com entradas reais (datas fora de blocos de codigo), isto NAO e um scaffold novo: siga o fluxo de **Atualizacao** em `references/atualizacao.md` desta skill. Se o usuario pediu para validar a estrutura ou criar/ativar specs em projeto existente, veja as secoes no fim deste arquivo. Caso contrario, siga os passos abaixo.

### 1. Confirme o diretorio de destino

Por padrao o destino e o diretorio atual de trabalho (`pwd`). Pergunte ao usuario "criar a estrutura aqui em `<pwd>` ou em outro caminho?" e use o que ele responder. Se ele indicar uma pasta que ainda nao existe, crie-a.

### 2. Verifique conflitos antes de criar

Liste arquivos do destino que coincidem com algum arquivo da estrutura. Se houver conflito, **nao sobrescreva** - pare e pergunte ao usuario o que fazer. Veja a secao "Resolucao De Conflitos" abaixo.

### 3. Entrevista

Regra de ouro: se o pedido inicial do usuario ja respondeu uma pergunta, NAO a repita - registre a resposta e siga. Faca apenas as perguntas em aberto, numeradas, com opcoes numeradas. Toda pergunta aceita resposta livre. "Avançar" adia a resposta e vira pendencia registrada - **nunca autoriza inferir a resposta**.

O usuario pode responder tudo de uma vez (ex: "1: minha-loja; 2: loja de camisetas; 3: 1; 4: 1").

```text
**1. Qual o nome do projeto?**
   1. Usar o nome da pasta de destino: "<nome-da-pasta>"
   2. Escrever outra resposta

**2. Qual o objetivo do projeto?** (uma a tres frases: o que faz e para quem)
   1. Escrever a resposta
   2. Avançar - deixa "(A preencher.)" no PROJECT_CONTEXT.md e cria a tarefa
      "Preencher objetivo do projeto" em TASKS.md

**3. Estrutura completa ou minimal?**
   1. Minimal (recomendado para comecar) - so o nucleo
   2. Completa - nucleo + opcionais (ARCHITECTURE, API, DATA_MODEL, GLOSSARY,
      ONBOARDING, ROADMAP, PROMPTS, STACK)
   3. Escrever outra resposta (ex: "minimal + ARCHITECTURE")

**4. Ativar o modulo de specs (docs/specs/)?**
   1. Nao (recomendado) - da para ativar depois pedindo a esta skill
   2. Sim - cria docs/specs/README.md e insere o bloco de specs em AGENTS.md
```

Sem preferencia clara nas perguntas 3 e 4, sugira as opcoes marcadas como recomendadas.

Nao pergunte sobre git. **Nao inicialize repositorio git** a menos que o usuario peca explicitamente.

### 4. Copie os arquivos do `assets/` desta skill para o destino

Mantenha exatamente a estrutura de pastas (raiz + `docs/` + `docs/archive/`).

**Nucleo (sempre criado):**

```
AGENTS.md
CLAUDE.md
GEMINI.md
docs/README.md
docs/PROJECT_CONTEXT.md
docs/SESSION.md
docs/MEMORY.md
docs/CONSENSUS.md
docs/TASKS.md
docs/DECISIONS.md
docs/QUALITY.md
docs/CHANGELOG.md
docs/archive/README.md
```

**Opcionais (so para "completa"):**

```
docs/ARCHITECTURE.md
docs/API.md
docs/DATA_MODEL.md
docs/GLOSSARY.md
docs/ONBOARDING.md
docs/ROADMAP.md
docs/PROMPTS.md
docs/STACK.md
```

`STACK.md` tambem pode nascer depois, sozinho, quando o projeto ganhar codigo: e o mapa de tecnologias, pacotes e links de documentacao oficial que o agente consulta antes de mexer na stack.

**Modulo de specs (so se ativado na pergunta 4):**

- copie `assets/docs/specs/README.md` para `docs/specs/README.md`;
- insira o conteudo de `assets/partials/AGENTS-specs-block.md` em `AGENTS.md`, logo apos o marcador `<!-- ai-project-structure:core:end -->` e antes de "## Regras Do Projeto".

**Nunca copie `assets/partials/` para o projeto-alvo** - e material de insercao da skill, nao template de arquivo.

### 5. Preencha `docs/PROJECT_CONTEXT.md`

Substitua os placeholders das secoes:

- **Objetivo Do Projeto**: cole o objetivo informado pelo usuario. Se o usuario avancou a pergunta 2, deixe "(A preencher.)" e crie a tarefa "Preencher objetivo do projeto" em `TASKS.md` - nunca invente um objetivo.
- **Publico Ou Usuario Final**: deixe placeholder marcando que o usuario deve preencher (ex: "(A preencher.)").

Mantenha as demais secoes como estao no template - elas serao preenchidas pelo usuario depois. Adicione no topo, antes da primeira secao, uma linha indicando o nome do projeto:

```md
**Nome do projeto:** <nome informado>
```

### 5b. Preencha a data de adocao em `docs/TASKS.md`

No cabecalho de `docs/TASKS.md`, troque o placeholder do marcador `(convencoes-2-2-0-desde: AAAA-MM-DD)` pela data de hoje. E a data a partir da qual a evidencia de fechamento passa a ser cobrada nesse projeto. Sem ela, o validador nao cobra evidencia de nenhuma tarefa.

### 6. Adicione a primeira entrada em `docs/SESSION.md`

O template termina no fim do bloco cercado de "Modelo Para Nova Sessao". Insira **depois** desse bloco, no fim do arquivo, nunca dentro da cerca:

```md
## AAAA-MM-DD - <agente que executou (ex: Claude, Codex, Gemini)>

### Objetivo

- Inicializar a estrutura multiagente para o projeto "<nome>".

### O Que Foi Feito

- Criada a estrutura Markdown multiagente (nivel <completa | minimal>) em <caminho absoluto>.
- `PROJECT_CONTEXT.md` preenchido com nome e objetivo informados pelo usuario.

### Arquivos Criados Ou Alterados

- (Listar todos os arquivos criados, com caminho relativo a raiz do novo projeto.)

### Decisoes Tomadas

- Nivel de estrutura escolhido: <completa | minimal>.
- Modulo de specs: <ativado | nao ativado>.

### Aprendizados Para MEMORY.md

- Nenhum.

### Pendencias

- Preencher os demais campos de `PROJECT_CONTEXT.md` (publico, estado atual, restricoes, fora de escopo).
- Preencher `TASKS.md` com tarefas iniciais.

### Proximo Passo Recomendado

- Agente sugerido (ou "qualquer agente"): qualquer agente.
- Motivo: estrutura pronta; proxima acao depende do projeto.
```

Use a data de hoje no formato AAAA-MM-DD.

### 7. Reporte ao usuario

No final, liste de forma curta:

- caminho absoluto do destino;
- nivel escolhido (completa ou minimal) e se o modulo de specs foi ativado;
- versao da estrutura: 2.5.0;
- arquivos criados (em arvore);
- proximo passo sugerido: preencher os demais campos de `PROJECT_CONTEXT.md` e adicionar tarefas iniciais em `TASKS.md`;
- oferta: "quer validar a estrutura? `python3 <dir-desta-skill>/scripts/validate_structure.py <destino>`".

## Resolucao De Conflitos

Se um arquivo do destino tem o mesmo nome de um arquivo da estrutura:

- **Conteudo identico ao template**: pule esse arquivo, nao precisa fazer nada.
- **Conteudo diferente**: pergunte ao usuario, por arquivo:
  - **(a) preservar o existente** (pular esse arquivo);
  - **(b) substituir pelo template** (sobrescreve apos confirmacao explicita);
  - **(c) mostrar diff e decidir caso a caso**.

Nunca sobrescreva sem confirmacao explicita do usuario para aquele arquivo. Em duvida, prefira preservar - o usuario sempre pode substituir manualmente depois.

Se o destino ja parece ser um projeto desta estrutura (ja tem `AGENTS.md` e `docs/SESSION.md` com entradas reais), nao siga com o scaffold: use o fluxo de **Atualizacao** (`references/atualizacao.md`) - provavelmente o usuario quer atualizar ou validar, nao recriar.

## Atualizar Ou Validar Estrutura Existente

Para projeto que ja usa esta estrutura:

- **Atualizar** para a versao atual da skill (v1 → v2, ou v2 → v2.x): siga `references/atualizacao.md`. O fluxo detecta a versao pelos marcadores em `AGENTS.md`, mostra diff por bloco e nunca sobrescreve sem confirmacao por item.
- **Validar**: rode `python3 <dir-desta-skill>/scripts/validate_structure.py <projeto>` e reporte o resultado. `--strict` trata avisos como falha. `--codigos` troca o relatorio por uma linha por diagnostico (`NIVEL|CODIGO|ARQUIVO|SUJEITO`): e o que usar para montar portao, porque o codigo e estavel e a redacao da mensagem nao.

## Criar Spec Ou Ativar O Modulo Em Projeto Existente

Siga `references/specs.md` para: ativar o modulo de specs em um projeto que nao o tem, ou criar uma nova spec (`docs/specs/NNNN-slug.md`) com entrevista curta e tarefas em `TASKS.md`.

## Rodar Uma Tarefa Com O Loop

Quando o usuario pedir para rodar o loop em uma tarefa (ex: "roda o loop na T-042", "manda a T-042 para o loop executar"), **monte a chamada para ele**. Ele nao deve precisar lembrar flags.

1. **Confirme que o modulo esta ativo** no projeto: o `AGENTS.md` precisa ter o bloco entre `ai-project-structure:loop:start` e `loop:end`. Sem isso, ofereca a ativacao (secao abaixo) em vez de rodar.
2. **Confira a tarefa.** Ela precisa ter `(verifica: <comando>)`. Se nao tiver, nao invente um comando: mostre a tarefa e pergunte qual comando prova que ela ficou pronta. Tarefa sem portao nao entra no loop.
3. **Leia os perfis** em `docs/MEMORY.md`, secao `## User`. Eles mapeiam intencao e ferramenta para o comando do agente. Se nao existirem, pergunte qual ferramenta e qual modelo usar, e **ofereca registrar o perfil** ali para nao perguntar de novo. Nunca invente nome de modelo nem flag: se nao souber, pergunte (regra "Nunca Inferir").
4. **Se os perfis de executar tiverem degraus de esforco**, proponha um a partir da tarefa e diga o motivo em uma linha, seguindo "Escolher O Nivel De Esforco" em `references/loop.md`. Na duvida entre dois, proponha o mais baixo.
5. **Monte e mostre o comando antes de rodar**, para o usuario poder corrigir:

```bash
<dir-desta-skill>/scripts/loop.sh --tarefa T-042 --agente "<perfil escolhido>"
```

6. **Rode e reporte** o que aconteceu, traduzindo o exit code: 0 fechou com evidencia, 2 o portao falhou em todas as tentativas, 3 a tarefa foi para "Aguardando Usuario" com uma pergunta, 4 o comando do agente esta mal configurado. Em 3, mostre a pergunta que ficou registrada.

A tabela de comandos por ferramenta, as armadilhas de flag e o formato dos perfis estao em `references/loop.md`.

**Configurar os perfis**: quando o usuario pedir para ver, trocar ou criar perfil ("configura os perfis do loop", "que modelo o loop esta usando", "quero trocar o modelo"), siga a secao "Configurar Os Perfis" de `references/loop.md`. Ela mostra o que existe hoje, pergunta o que mudar com opcoes numeradas e confirma os nomes de modelo na propria CLI antes de gravar.

## Ativar O Modulo De Loop

Siga `references/loop.md`. **Nunca ative no scaffold**, em nenhum nivel, e nunca ofereca a ativacao por conta propria: ela e sempre pedido explicito do usuario.

Antes de tocar qualquer arquivo, confira o portao: a secao "Testes E Validacao" de `docs/QUALITY.md` do projeto-alvo precisa ter comando executavel. Vazia, ou ainda com o texto do template, a ativacao e **recusada**, com o motivo dito ao usuario. Um loop sem portao real nao sabe se o trabalho ficou bom, e um portao falso e pior que nenhum.

## Arquivos Em `assets/`

Os templates ficam em `assets/`:

```text
assets/
  AGENTS.md
  CLAUDE.md
  GEMINI.md
  partials/
    AGENTS-specs-block.md   (material de insercao; nunca copiado ao projeto)
    AGENTS-loop-block.md    (idem, so quando o modulo de loop e ativado)
  docs/
    README.md
    PROJECT_CONTEXT.md
    SESSION.md
    MEMORY.md
    CONSENSUS.md
    TASKS.md
    DECISIONS.md
    QUALITY.md
    CHANGELOG.md
    PROMPTS.md
    ARCHITECTURE.md
    API.md
    DATA_MODEL.md
    GLOSSARY.md
    ONBOARDING.md
    ROADMAP.md
    STACK.md
    specs/
      README.md             (so copiado quando o modulo de specs e ativado)
    archive/
      README.md
```

Eles sao templates limpos: `SESSION.md`, `CONSENSUS.md`, `TASKS.md`, `DECISIONS.md`, `CHANGELOG.md` e `ROADMAP.md` nao trazem entradas historicas. `PROJECT_CONTEXT.md` tem placeholders que voce preenche no passo 5.

## Validacao

Antes de finalizar, rode o validador:

```bash
python3 <dir-desta-skill>/scripts/validate_structure.py <destino>
```

Zero erros esperado em scaffold recem-criado. Se o Python nao estiver disponivel, confira manualmente:

- todos os arquivos esperados foram criados no destino (lista do passo 4 conforme o nivel escolhido);
- `PROJECT_CONTEXT.md` foi preenchido com nome e objetivo informados (ou "(A preencher.)" registrado como pendencia, se o usuario avancou);
- `SESSION.md` recebeu a primeira entrada (passo 6) e nao apenas o template;
- `AGENTS.md` contem os marcadores `ai-project-structure:core:start`/`end` (e `specs`, se ativado);
- nenhum arquivo existente foi sobrescrito sem permissao;
- `docs/archive/` existe (mesmo que so com `README.md`);
- `docs/TASKS.md` tem a secao `## Aguardando Usuario` e a data preenchida no marcador `(convencoes-2-2-0-desde:)`;
- nenhum repositorio git foi inicializado (a menos que o usuario tenha pedido).

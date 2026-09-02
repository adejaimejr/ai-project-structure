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

- 

### Feedback

- **Regra:** nunca usar o caractere travessao (em dash, U+2014) em textos do projeto ou da skill; usar dois-pontos, ponto-e-virgula, virgula, parenteses ou hifen simples. **Por que:** pedido explicito do usuario em 2026-08-20; o validador da skill acusa ocorrencias como erro. **Quando aplicar:** qualquer texto escrito neste repositorio e nos templates que a skill gera.

### Project

- O `install.sh` da skill nao distribui tudo o que existe na fonte canonica: `evals/`, `install.sh`, `README.md` e `CHANGELOG.md` ficam apenas em `docs/skills/ai-project-structure/` e nao aparecem em `~/.claude/skills/`, `~/.agents/skills/` nem `~/.gemini/skills/` (verificado por `diff -rq` em 2026-09-02). Ferramenta que deve ficar restrita ao repositorio vai em `evals/`; o que vai em `scripts/` chega na maquina de todo usuario.

### Reference

- specsfy (inspiracao da v2 da skill): github.com/promovaweb/specsfy. Metodologia SDD pt-BR; analisada em 2026-08-20; o que importamos e o que descartamos esta em `docs/DECISIONS.md` e no CHANGELOG da skill.


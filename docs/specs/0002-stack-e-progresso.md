# Spec 0002 - STACK.md e projecao de progresso (skill 2.1.0)

**Status:** Concluida
**Criada em:** 2026-08-20
**Esforco:** M, duas features pequenas e independentes na mesma versao.

## Problema E Resultado Esperado

- Problema: a estrutura nao tem um mapa dedicado de stack (tecnologias, pacotes, links de documentacao oficial) que aponte o modelo para a fonte certa antes de mexer em codigo; e ver o progresso exige ler TASKS.md e cada spec manualmente.
- Resultado esperado: template opcional `docs/STACK.md` e flag `--progress` no validador com projecao somente-leitura de tarefas e specs, lancados como skill 2.1.0.

## Escopo

### Incluido

- Template `assets/docs/STACK.md` (tecnologias, pacotes principais, "Onde Consultar Primeiro", notas de compatibilidade).
- `AGENTS.md` core: STACK.md em "Onde Escrever Cada Coisa" e gatilho de atualizacao proprio.
- `validate_structure.py --progress`: contagem de tarefas por secao, status por spec, tarefas concluidas/total, perguntas abertas. Nunca edita nada.
- Versao da skill para 2.1.0; marcadores dos blocos para v2.1.0; evals atualizados (eval 2 inclui STACK; eval 8 novo para progresso).
- Dogfood: `docs/STACK.md` do meta-projeto preenchido; bloco core da raiz atualizado para v2.1.0 preservando o restante do arquivo.

### Fora Do Escopo

- Runner de testes por stack (Laravel, Pest etc.); comandos do projeto continuam em `QUALITY.md`.
- TUI, `--watch`, porcentagens de milestone.

## Criterios De Aceite

- `--progress` mostra tarefas por secao e, por spec, status + concluidas/total; retorna exit 0 e nao altera nenhum arquivo.
- Scaffold "completa" passa a incluir `docs/STACK.md`; scaffold minimal nao o cria.
- Validador continua exit 0 no meta-projeto e nos scaffolds simulados; fixture quebrada continua com os 2 erros esperados.
- Tres instalacoes identicas apos `./install.sh`.
- Nenhum travessao (U+2014) em arquivo novo ou alterado.

## Decisoes

- DEC-001: validacao de stack (rodar testes de Laravel etc.) fica fora; o mapa em STACK.md aponta a documentacao e QUALITY.md guarda os comandos. Motivo: a skill valida estrutura, nao entrega de codigo.
- DEC-002: progresso como flag do validador existente, nao script novo nem CLI. Motivo: zero dependencia nova, um unico ponto de manutencao.
- DEC-003: projecao de progresso e somente-leitura por regra (licao do specsfy-progress, que nunca edita gates).

## Tarefas

- T-005: criar template STACK.md e integrar ao core e ao scaffold
- T-006: implementar --progress no validador
- T-007: atualizar evals, reinstalar e validar tudo

## Perguntas Abertas

- (Vazio.)

## Evidencia De Conclusao

- Verificacao: `./install.sh` + `diff -rq` entre os tres destinos; `validate_structure.py` no scaffold completa simulado, no meta-projeto, nas fixtures v1 e broken; `--progress` no meta-projeto e nas duas fixtures; varredura de travessao no repo.
- Resultado: paridade OK nos tres destinos; scaffold completa com STACK.md exit 0; meta-projeto exit 0 (4 avisos historicos de SESSION); fixture v1 exit 0 com INFOs; fixture broken com os 2 erros esperados; `--progress` mostrando 0001 (3/3, Concluida) e 0002 (3/3, Concluida) sem alterar arquivos; nenhum travessao no repo.

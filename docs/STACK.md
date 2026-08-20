# STACK

Com o que o projeto e construido e onde consultar cada tecnologia. Use este arquivo para apontar o modelo ao lugar certo antes de resolver um problema ou desenvolver algo que dependa da stack.

## Como Manter

- Atualize quando qualquer tecnologia ou pacote relevante entrar, sair ou mudar de versao.
- Registre a documentacao oficial de cada tecnologia; link certo evita resposta inventada.
- Comandos de teste, lint e build ficam em `QUALITY.md`; aqui fica o mapa da stack.
- Liste os pacotes principais, nao a arvore inteira de dependencias.

## Tecnologias

| Tecnologia | Versao | Papel no projeto | Documentacao |
| --- | --- | --- | --- |
| Markdown | n/a | Todo o conteudo da estrutura e dos templates | https://www.markdownguide.org |
| Python 3 (stdlib) | 3.8+ | Validador `validate_structure.py` (sem dependencias externas) | https://docs.python.org/3/library/ |
| Bash | 3.2+ | Instalador `install.sh` | https://www.gnu.org/software/bash/manual/ |
| Agent Skills Open Standard | n/a | Formato da skill (SKILL.md com frontmatter name/description) lido por Claude Code, Codex CLI e Gemini CLI | ver `docs/skills/ai-project-structure/README.md` |

## Pacotes E Dependencias Principais

| Pacote | Versao | Para que serve |
| --- | --- | --- |
| (nenhum) | n/a | O projeto nao tem dependencias externas por decisao (validador so stdlib) |

## Onde Consultar Primeiro

- Duvida sobre regex ou pathlib no validador: documentacao da stdlib do Python (modulos `re`, `pathlib`, `unicodedata`, `argparse`).
- Duvida sobre o formato ou instalacao da skill: `docs/skills/ai-project-structure/README.md` e `SKILL.md`.
- Duvida sobre regras da estrutura: `AGENTS.md` na raiz (bloco core) e `docs/README.md`.
- Duvida sobre compatibilidade do `install.sh`: manual do Bash (o macOS traz Bash 3.2; evitar recursos de Bash 4+).

## Notas De Compatibilidade

- O validador precisa rodar com o Python 3 do sistema, sem pip; nao adicionar imports fora da stdlib.
- `install.sh` precisa funcionar no Bash 3.2 do macOS; evitar arrays associativos e `mapfile`.
- `sed -i` no macOS exige argumento vazio (`sed -i ''`); scripts de manutencao devem considerar isso.

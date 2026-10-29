# Estado atual — Parametric Fit Validation Lab

Revisão documental: **13/10/2026**, America/Sao_Paulo. Git inicial limpo em `main`.

## Observado

`pyproject.toml` requer Python >=3.10 e publica entrada `fitlab`. `fitlab/model.py` valida dimensões/parede e calcula folgas/classificação; `mesh.py` constrói holder anular e insert sólido, escreve STL ASCII e conta arestas; `cli.py` gera relatório e SVG.

Existem `tests/test_fit.py` e `tests/test_mesh.py`, além de JSON de exemplo e SVG em docs. Não foram executados nem usados para declarar encaixe validado.

## Operação identificada

O README fornece `python -m fitlab.cli examples/close-fit.json --output generated` e `pytest -q`, com instalação por editable package. Todos **não executado nesta tarefa**. O manifest não declara bibliotecas externas de runtime; pytest é citado para testes.

A CLI grava holder/insert STL, JSON e SVG; retorna 0 somente se printable e ambas as malhas passam `is_watertight`, caso contrário 2. Nenhuma saída foi regenerada ou aberta.

## Retomada

Última etapa comprovada: notas/instruções organizadas e links conferidos. Malhas, parede, folga e comportamento físico não foram certificados. Os limiares implementados são a referência de cálculo, não uma tolerância universal de fabricação.

Sugestões não aprovadas:

1. Definir especificação/critério físico apropriados antes de usar em uma peça real.
2. Em validação autorizada, registrar testes executados e parâmetros do artefato.
3. Manter inserts neutros e geometria sanitizada, conforme a fronteira do README.

[Arquitetura](ARQUITETURA.md) e [índice](INDEX.md).

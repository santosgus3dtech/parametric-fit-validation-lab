# Arquitetura e regras — Parametric Fit Validation Lab

Fontes: `fitlab/model.py`, `mesh.py`, `cli.py`, `pyproject.toml` e README.

JSON → `FitSpec` → `analyze_fit` → holder/insert triangulados → STL + relatório JSON + SVG. Módulos `model`, `mesh`, `report` e `cli` separam responsabilidade; o código lido comprova fluxo, sem execução.

## Critérios implementados

`FitSpec.validate` rejeita dimensão <=0, diâmetro externo <=cavidade e parede abaixo de `minimum_wall_mm` (default 1.2).

Folga diametral = cavidade − insert; radial = diametral/2; axial = altura holder − altura insert. A classificação usa: negativa → interference; <0.20 → press; <=0.50 → close; acima → free. Colisão ocorre com folga diametral ou axial negativa; printable exige ausência de colisão e parede suficiente.

As malhas são construídas por anéis e triangulação com 64 segmentos por padrão. A função de checagem por arestas faz parte do fluxo de aceite da CLI; não equivale a medir deformação de filamento ou tolerância da impressora.

O README restringe o laboratório a geometria neutra. Não foram deduzidas decisões históricas nem aprovadas novas regras. [Estado atual](ESTADO-ATUAL.md).

# Parametric Fit Validation Lab

[English / README principal](README.md) · Português (Brasil)

Um pequeno laboratório de engenharia de geometria para projetar e validar encaixes
cilíndricos impressos em 3D, sem modelos proprietários ou imagens de referência de terceiros.

![Análise de encaixe gerada](docs/images/fit-analysis.svg)

## O que faz

- Lê uma especificação JSON com dimensões.
- Calcula folgas diametral, radial e axial.
- Classifica encaixes por interferência, por pressão, ajustados e livres.
- Impõe uma espessura mínima de parede imprimível.
- Gera malhas STL estanques para o suporte e o inserto de referência.
- Verifica a contagem de arestas de uma malha manifold antes de aceitar a saída.
- Produz um relatório legível por máquina e uma vista de engenharia em SVG.

## Executar

```bash
python -m pip install -e .
python -m fitlab.cli examples/close-fit.json --output generated
```

Arquivos gerados:

- `holder.stl`
- `insert.stl`
- `fit-report.json`
- `fit-analysis.svg`

## Testar

```bash
python -m pip install pytest
pytest -q
```

## Limites do projeto

Este laboratório público foi reconstruído em torno de um inserto cilíndrico neutro.
Ele não inclui referências a produtos de marcas, imagens baixadas de marketplaces,
arquivos privados do Blender ou geometria de clientes.

## Licença

MIT

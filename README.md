# Automação Power BI — Cactus Elétrica

## Objetivo

Automatizar a preparação e o tratamento de planilhas Excel para utilização em relatórios e dashboards no Power BI.

## Tecnologias

- Python
- Pandas
- OpenPyXL
- Power BI
- Git/GitHub

## Estrutura atual

- `entrada/` — arquivos Excel para processamento.
- `dados tratados/` — arquivos tratados, organizados por tipo de relatório.
- `saida_erros/` — registros de erros encontrados durante o processamento.
- `processados/` — arquivos já processados.
- `fluxo.py` — entrada, validação, processamento e saída.
- `tratamento.py` — identificação e tratamento geral e específico dos relatórios.

## Fluxo

`Entrada → Validação → Identificação → Tratamento Geral → Tratamento Específico → Saída`

## Status

Projeto em desenvolvimento.

Atualmente, o sistema possui:

- validação e carregamento de arquivos Excel;
- identificação de relatórios pelo conteúdo da planilha;
- tratamento geral dos dados;
- tratamento específico para **Faturamento por Período**;
- organização dos arquivos por tipo de relatório;
- registro de erros e movimentação dos arquivos processados;
- integração com Git/GitHub.

## Pendentes

-  Adicionar identificação dos demais tipos de relatório.
-  Implementar tratamentos específicos dos demais relatórios.
-  Implementar processamento em lote dos arquivos.
-  Definir nomes de saída automaticamente conforme o relatório.
-  Automatizar a execução sem necessidade de abrir o VS Code.
-  Finalizar integração/atualização dos dados no Power BI.
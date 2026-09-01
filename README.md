# Automação Power BI — Cactus Elétrica

## Objetivo

Automatizar o processo de preparação e tratamento de dados de planilhas Excel para utilização em relatórios e dashboards no Power BI.

## Tecnologias

* Python
* Pandas
* OpenPyXL
* Power BI

## Estrutura atual

* `entrada/` — arquivos Excel recebidos para processamento.
* `Dados Tratados/` — arquivos após o tratamento.
* `saida_erros/` — registros de erros encontrados durante o processamento.
* `tratamento.py` — código principal da automação.

## Status

 Projeto em desenvolvimento.

Atualmente, o sistema já possui:

* identificação do arquivo Excel mais recente;
* validação do arquivo;
* carregamento dos dados com Pandas;
* tratamento inicial dos dados;
* geração do arquivo tratado;
* registro de erros;
* integração com Git/GitHub.

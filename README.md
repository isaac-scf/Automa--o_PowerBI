# Automação Power BI

Projeto desenvolvido para automatizar a organização e o tratamento de dados utilizados em relatórios e dashboards no Power BI.

## Objetivo

Facilitar a transformação de dados de planilhas em informações organizadas, reduzindo tarefas manuais e preparando os dados para análise no Power BI.

Fluxo geral:

Fonte de dados → Tratamento → Arquivos organizados → Power BI

## Tecnologias utilizadas

- Python 3.11
- Conda / Miniconda
- Pandas
- NumPy
- OpenPyXL
- Excel
- Power BI

## Estrutura do projeto

```text
Automação PBI/
├── entrada/
├── Dados Tratados/
├── fluxo.py
├── rodar_fluxo.bat
├── environment.yml
├── .gitignore
└── README.md
```

### Principais arquivos e pastas

- `entrada/`: armazena os arquivos Excel utilizados como fonte de dados.
- `Dados Tratados/`: armazena os arquivos gerados após o tratamento.
- `fluxo.py`: arquivo principal responsável pela execução do fluxo.
- `rodar_fluxo.bat`: atalho que ativa o ambiente correto e executa o fluxo.
- `environment.yml`: registra o ambiente Conda e suas dependências.
- `.gitignore`: define arquivos e pastas que não devem ser versionados.

## Ambiente de execução

O projeto utiliza o ambiente Conda:

```text
powerbi_env
```

O ambiente possui Python 3.11 e as bibliotecas necessárias para leitura, tratamento e organização dos dados.

Para recriar o ambiente:

```bash
conda env create -f environment.yml
```

Para ativá-lo:

```bash
conda activate powerbi_env
```

## Problema encontrado e solução

Durante os testes iniciais, o NumPy instalado por `pip` dentro de um ambiente `venv` teve um de seus arquivos binários bloqueado pelo Smart App Control do Windows.

Como o Pandas depende do NumPy, isso impedia a execução normal do fluxo.

A solução foi migrar o ambiente para o Conda, utilizando o Miniconda e instalando as dependências por meio do canal Conda. Dessa forma, o projeto passou a utilizar o ambiente `powerbi_env`.

O antigo ambiente baseado em `venv` e os arquivos de dependências via `pip` foram removidos por não serem mais necessários.

## Execução

### Pelo atalho

Execute o arquivo:

```text
rodar_fluxo.bat
```

Ele ativa o ambiente `powerbi_env` e executa o `fluxo.py`.

### Pelo terminal

```bash
conda activate powerbi_env
python fluxo.py
```

## Funcionalidades atuais

O projeto está sendo desenvolvido para:

- Ler arquivos de entrada;
- Organizar e tratar os dados;
- Gerar arquivos para utilização no Power BI;
- Gerar curvas ABC de faturamento, clientes e produtos;
- Gerar a curva de faturamento por período;
- Preparar os dados para análises e dashboards.

## Próximas etapas

- Aprimorar as validações dos dados;
- Criar uma tabela de resumo geral;
- Melhorar a organização dos arquivos gerados;
- Conectar os dados tratados ao Power BI;
- Investigar a integração entre Omie, Google Sheets e Power BI.

## Status

**Em desenvolvimento**

O projeto utiliza atualmente o ambiente Conda `powerbi_env`, com execução automatizada pelo arquivo `rodar_fluxo.bat`.
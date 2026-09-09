import pandas as pd


# ==============================
# IDENTIFICAÇÃO DO RELATÓRIO
# ==============================

TIPOS_RELATORIO = {
    "Faturamento por Período": "faturamento_periodo",
    "Faturamento por Produto": "faturamento_produto",
    "Faturamento por Cliente": "faturamento_cliente",
}

TIPOS_FATURAMENTO = (
    "faturamento_periodo",
    "faturamento_produto",
    "faturamento_cliente",
)


def identificar_relatorio(df: pd.DataFrame) -> str:

    if df is None or df.empty:
        return "desconhecido"

    primeira_celula = str(df.iloc[0, 0]).strip()

    return TIPOS_RELATORIO.get(
        primeira_celula,
        "desconhecido"
    )


# ==============================
# TRATAMENTO ESTRUTURAL
# ==============================

def estruturar_faturamento(df: pd.DataFrame) -> pd.DataFrame:

    titulo = str(df.iloc[0, 0]).strip()

    # Linha 6 vira cabeçalho
    cabecalho = df.iloc[5].tolist()

    # Mantém somente os dados a partir da linha 7
    df = df.iloc[6:].copy()

    df.columns = cabecalho

    # Remove Total Geral
    if not df.empty:
        df = df.iloc[:-1]

    df = df.reset_index(drop=True)

    # Guarda o título para o fluxo.py recolocar no Excel
    df.attrs["titulo_relatorio"] = titulo

    return df


# ==============================
# TRATAMENTO GERAL
# ==============================

def limpeza_geral(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Células vazias
    df = df.replace(r"^\s*$", pd.NA, regex=True).infer_objects(copy=False)

    # Remove linhas e colunas completamente vazias
    df = df.dropna(axis=0, how="all")
    df = df.dropna(axis=1, how="all")

    # Limpa espaços dos textos
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].apply(
            lambda valor: valor.strip()
            if isinstance(valor, str)
            else valor
        )

    # Padroniza cabeçalhos
    df.columns = [
        " ".join(str(coluna).strip().split())
        for coluna in df.columns
    ]

    # Remove linhas de totalização
    termos_totalizacao = {
        "total",
        "total geral",
        "subtotal"
    }

    def eh_total(linha):
        return any(
            isinstance(valor, str)
            and valor.strip().lower() in termos_totalizacao
            for valor in linha
        )

    df = df[~df.apply(eh_total, axis=1)]

    return df.reset_index(drop=True)


# ==============================
# TRATAMENTOS ESPECÍFICOS
# ==============================

def tratar_faturamento(df: pd.DataFrame) -> pd.DataFrame:
    return df


def tratar_desconhecido(df: pd.DataFrame) -> pd.DataFrame:
    return df


# ==============================
# MAPA DE TRATAMENTOS
# ==============================

TRATAMENTOS_ESPECIFICOS = {
    "faturamento_periodo": tratar_faturamento,
    "faturamento_produto": tratar_faturamento,
    "faturamento_cliente": tratar_faturamento,
    "desconhecido": tratar_desconhecido,
}


# ==============================
# MAPA DE DESTINOS
# ==============================

DESTINOS_POR_TIPO = {
    "faturamento_periodo":
        "dados tratados/Faturamento por Período",

    "faturamento_produto":
        "dados tratados/Faturamento por Produto",

    "faturamento_cliente":
        "dados tratados/Faturamento por Cliente",

    "desconhecido":
        "dados tratados",
}


# ==============================
# MAPA DE NOMES
# ==============================

NOMES_POR_TIPO = {
    "faturamento_periodo":
        "Faturamento por Período",

    "faturamento_produto":
        "Faturamento por Produto",

    "faturamento_cliente":
        "Faturamento por Cliente",

    "desconhecido":
        "Desconhecido",
}


# ==============================
# PROCESSAMENTO
# ==============================

def processar_relatorio(df: pd.DataFrame):

    print("=== ETAPA DE TRATAMENTO DOS DADOS ===")

    # 1. Identificação
    tipo = identificar_relatorio(df)

    print(f"Tipo identificado: {tipo}")

    # 2. Tratamento estrutural
    if tipo in TIPOS_FATURAMENTO:
        print("Aplicando estrutura do relatório...")
        df = estruturar_faturamento(df)

    # 3. Tratamento geral
    print("Aplicando regras gerais...")
    df = limpeza_geral(df)

    # 4. Tratamento específico final
    funcao = TRATAMENTOS_ESPECIFICOS.get(
        tipo,
        tratar_desconhecido
    )

    df = funcao(df)

    print(f"Linhas após tratamento: {df.shape[0]}")
    print(f"Colunas após tratamento: {df.shape[1]}")
    print(
        f"Destino definido: "
        f"{DESTINOS_POR_TIPO.get(tipo, 'dados tratados')}"
    )
    print()

    return df, tipo
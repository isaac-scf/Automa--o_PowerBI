import pandas as pd


# ==============================
# IDENTIFICAÇÃO
# ==============================

def identificar_relatorio(df):
    if df is None or df.empty:
        return "desconhecido"

    primeira_linha = df.iloc[0].fillna("").astype(str)

    texto = " ".join(
        valor.strip() for valor in primeira_linha if valor.strip()
    ).lower()

    if "faturamento por período" in texto:
        return "faturamento_periodo"

    return "desconhecido"


# ==============================
# TRATAMENTO GERAL
# ==============================

def limpeza_geral(df):
    df = df.copy()

    # Remove espaços dos textos
    for coluna in df.columns:
        if df[coluna].dtype == "object":
            df[coluna] = df[coluna].apply(
                lambda x: x.strip() if isinstance(x, str) else x
            )

    # Padroniza células vazias
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # Remove linhas e colunas completamente vazias
    df = df.dropna(axis=0, how="all")
    df = df.dropna(axis=1, how="all")

    # Padroniza cabeçalhos
    df.columns = [
        " ".join(str(col).strip().split())
        for col in df.columns
    ]

    # Remove linhas de totalização
    def eh_total(linha):
        texto = " ".join(
            str(valor).strip().lower()
            for valor in linha.fillna("")
            if str(valor).strip()
        )

        return (
            texto.startswith("total geral")
            or texto.startswith("subtotal")
            or texto.startswith("total")
        )

    df = df[~df.apply(eh_total, axis=1)]

    return df.reset_index(drop=True)


# ==============================
# FATURAMENTO POR PERÍODO
# ==============================

def tratar_faturamento_periodo(df):
    if df is None or df.empty:
        return df

    if len(df) < 6:
        print("Aviso: Faturamento por Período possui menos de 6 linhas.")
        return df

    # Linha 6 vira o cabeçalho
    df.columns = (
        df.iloc[5]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Remove linhas 1 até 6
    df = df.iloc[6:].copy()

    # Remove última linha (Total Geral)
    if not df.empty:
        df = df.iloc[:-1]

    return df.reset_index(drop=True)


# ==============================
# RELATÓRIO DESCONHECIDO
# ==============================

def tratar_desconhecido(df):
    print("Aviso: tipo de relatório não identificado.")
    return df


# ==============================
# MAPAS
# ==============================

TRATAMENTOS_ESPECIFICOS = {
    "faturamento_periodo": tratar_faturamento_periodo,
    "desconhecido": tratar_desconhecido
}

DESTINOS_POR_TIPO = {
    "faturamento_periodo": "dados tratados/Faturamento por Período",
    "desconhecido": "dados tratados"
}

NOMES_POR_TIPO = {
    "faturamento_periodo": "Faturamento por Período",
    "desconhecido": "Desconhecido"
}


# ==============================
# PROCESSAMENTO
# ==============================

def processar_relatorio(df):
    print("=== ETAPA DE TRATAMENTO DOS DADOS ===")

    # 1. Identificação
    tipo = identificar_relatorio(df)
    print(f"Tipo identificado: {tipo}")

    # 2. Tratamento específico estrutural
    if tipo == "faturamento_periodo":
        df = tratar_faturamento_periodo(df)

    # 3. Tratamento geral
    df = limpeza_geral(df)

    # 4. Tratamento específico final
    if tipo != "faturamento_periodo":
        funcao = TRATAMENTOS_ESPECIFICOS.get(
            tipo,
            tratar_desconhecido
        )
        df = funcao(df)

    print(f"Linhas após tratamento: {len(df)}")
    print(f"Colunas após tratamento: {len(df.columns)}")
    print(f"Destino: {DESTINOS_POR_TIPO.get(tipo, 'dados tratados')}")

    return df, tipo
import pandas as pd


# ==============================
# IDENTIFICAÇÃO DO RELATÓRIO
# ==============================

def identificar_relatorio(df: pd.DataFrame) -> str:
    """
    Identifica o tipo de relatório através da primeira linha
    da planilha.

    A identificação acontece antes de qualquer tratamento.
    O nome do arquivo não é utilizado, pois pode ser genérico,
    como 'pivot.xlsx'.
    """

    if df is None or df.empty:
        return "desconhecido"

    # Linha 1 da planilha = índice 0 no Pandas
    primeira_linha = df.iloc[0].fillna("").astype(str)

    texto_identificacao = " ".join(
        valor.strip()
        for valor in primeira_linha
        if valor.strip()
    ).lower()

    # ------------------------------
    # FATURAMENTO POR PERÍODO
    # ------------------------------

    if "faturamento por período" in texto_identificacao:
        return "faturamento_periodo"

    return "desconhecido"


# ==============================
# TRATAMENTO GERAL
# ==============================

def limpeza_geral(df: pd.DataFrame) -> pd.DataFrame:
    """
    Regras gerais aplicadas a todos os relatórios.

    Regras:
    - remover colunas completamente vazias;
    - remover linhas completamente vazias;
    - remover espaços desnecessários dos textos;
    - padronizar cabeçalhos;
    - padronizar células vazias;
    - remover linhas de totalização claramente identificadas.

    Uma coluna só é removida quando estiver completamente vazia.
    """

    if df is None:
        return df

    df = df.copy()

    # ------------------------------
    # 1. Remover espaços desnecessários
    # ------------------------------

    for coluna in df.columns:

        if df[coluna].dtype == "object":

            df[coluna] = df[coluna].apply(
                lambda valor: valor.strip()
                if isinstance(valor, str)
                else valor
            )

    # ------------------------------
    # 2. Transformar células vazias
    #    em valores nulos
    # ------------------------------

    df = df.replace(
        r"^\s*$",
        pd.NA,
        regex=True
    )

    # ------------------------------
    # 3. Remover linhas completamente vazias
    # ------------------------------

    df = df.dropna(
        axis=0,
        how="all"
    )

    # ------------------------------
    # 4. Remover colunas completamente vazias
    # ------------------------------

    df = df.dropna(
        axis=1,
        how="all"
    )

    # ------------------------------
    # 5. Padronizar cabeçalhos
    # ------------------------------

    novos_cabecalhos = []

    for coluna in df.columns:

        cabecalho = str(coluna).strip()

        # Remove espaços duplicados
        cabecalho = " ".join(
            cabecalho.split()
        )

        novos_cabecalhos.append(cabecalho)

    df.columns = novos_cabecalhos

    # ------------------------------
    # 6. Remover linhas de totalização
    # ------------------------------

    indices_para_remover = []

    for indice, linha in df.iterrows():

        valores = (
            linha
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
        )

        texto_linha = " ".join(
            valor
            for valor in valores
            if valor
        )

        if (
            texto_linha.startswith("total geral")
            or texto_linha.startswith("subtotal")
            or texto_linha.startswith("total")
        ):
            indices_para_remover.append(indice)

    if indices_para_remover:

        df = df.drop(
            index=indices_para_remover
        )

    # ------------------------------
    # 7. Reorganizar índice
    # ------------------------------

    df = df.reset_index(
        drop=True
    )

    return df


# ==============================
# TRATAMENTO ESPECÍFICO
# FATURAMENTO POR PERÍODO
# ==============================

def tratar_faturamento_periodo(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Tratamento específico do relatório
    'Faturamento por Período'.

    Estrutura original:

        Linha 1       → identificação
        Linhas 2-5    → informações do relatório
        Linha 6       → cabeçalho verdadeiro
        Linhas seguintes → dados
        Última linha   → Total Geral

    Resultado:

        Linha 6 passa a ser o cabeçalho.
        Linhas 1-5 são removidas.
        Dados permanecem.
        Última linha (Total Geral) é removida.
    """

    if df is None or df.empty:
        return df

    df = df.copy()

    # ------------------------------
    # Verificar se existe linha 6
    # ------------------------------

    if len(df) < 6:

        print(
            "Aviso: o relatório possui menos de "
            "6 linhas. Tratamento específico "
            "não foi aplicado."
        )

        return df

    # ------------------------------
    # LINHA 6 → CABEÇALHO
    # ------------------------------

    # Pandas começa o índice em 0.
    #
    # Linha 1 → índice 0
    # Linha 2 → índice 1
    # Linha 3 → índice 2
    # Linha 4 → índice 3
    # Linha 5 → índice 4
    # Linha 6 → índice 5

    novo_cabecalho = (
        df.iloc[5]
        .fillna("")
        .astype(str)
        .str.strip()
        .tolist()
    )

    # ------------------------------
    # REMOVER LINHAS 1 ATÉ 6
    # ------------------------------

    # Os dados começam depois da linha 6.
    df = df.iloc[6:].copy()

    # ------------------------------
    # DEFINIR NOVO CABEÇALHO
    # ------------------------------

    df.columns = novo_cabecalho

    # ------------------------------
    # REMOVER ÚLTIMA LINHA
    # ------------------------------

    # A última linha do relatório
    # corresponde ao Total Geral.

    if not df.empty:

        df = df.iloc[:-1].copy()

    # ------------------------------
    # RESETAR ÍNDICE
    # ------------------------------

    df = df.reset_index(
        drop=True
    )

    return df


# ==============================
# TRATAMENTO DESCONHECIDO
# ==============================

def tratar_desconhecido(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Caso o relatório não seja identificado,
    nenhum tratamento específico é aplicado.
    """

    print(
        "Aviso: tipo de relatório não identificado."
    )

    return df


# ==============================
# MAPA DE TRATAMENTOS
# ==============================

TRATAMENTOS_ESPECIFICOS = {

    "faturamento_periodo":
        tratar_faturamento_periodo,

    "desconhecido":
        tratar_desconhecido,
}


# ==============================
# MAPA DE DESTINOS
# ==============================

DESTINOS_POR_TIPO = {

    "faturamento_periodo":
        "dados tratados/Faturamento por Período",

    "desconhecido":
        "dados tratados",
}


# ==============================
# NOMES DOS RELATÓRIOS
# ==============================

NOMES_POR_TIPO = {

    "faturamento_periodo":
        "Faturamento por Período",

    "desconhecido":
        "Desconhecido",
}


# ==============================
# PONTO DE ENTRADA
# CHAMADO PELO fluxo.py
# ==============================

def processar_relatorio(
    df: pd.DataFrame
) -> tuple:

    """
    Processa o relatório depois que ele passou
    por TODAS as validações do fluxo.py.

    ORDEM:

        1. Identificação pela linha 1
        2. Definição do tipo
        3. Tratamento específico estrutural
        4. Tratamento geral
        5. Tratamento específico final
        6. Retorno do resultado
    """

    print(
        "=== ETAPA DE TRATAMENTO DOS DADOS ==="
    )

    # ==============================
    # 1. IDENTIFICAÇÃO
    # ==============================

    tipo_relatorio = identificar_relatorio(df)

    nome_relatorio = NOMES_POR_TIPO.get(
        tipo_relatorio,
        "Desconhecido"
    )

    print(
        f"Tipo identificado: {tipo_relatorio}"
    )

    print(
        f"Nome do relatório: {nome_relatorio}"
    )

    # ==============================
    # 2. TRATAMENTO ESPECÍFICO
    #    DA ESTRUTURA
    # ==============================

    if tipo_relatorio == "faturamento_periodo":

        print(
            "Aplicando estrutura do "
            "Faturamento por Período..."
        )

        df = tratar_faturamento_periodo(df)

    # ==============================
    # 3. TRATAMENTO GERAL
    # ==============================

    print(
        "Aplicando regras gerais..."
    )

    df = limpeza_geral(df)

    # ==============================
    # 4. TRATAMENTO ESPECÍFICO FINAL
    # ==============================

    # Aqui ficam regras específicas adicionais
    # que futuramente poderão ser aplicadas
    # depois da limpeza geral.

    if tipo_relatorio != "faturamento_periodo":

        funcao_tratamento = (
            TRATAMENTOS_ESPECIFICOS.get(
                tipo_relatorio,
                tratar_desconhecido
            )
        )

        df = funcao_tratamento(df)

    # ==============================
    # RESULTADO
    # ==============================

    print(
        f"Linhas após tratamento: "
        f"{df.shape[0]}"
    )

    print(
        f"Colunas após tratamento: "
        f"{df.shape[1]}"
    )

    print(
        f"Destino definido: "
        f"{DESTINOS_POR_TIPO.get(tipo_relatorio, 'dados tratados')}"
    )

    print()

    return df, tipo_relatorio
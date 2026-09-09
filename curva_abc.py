import os
import pandas as pd


# ==============================
# CONFIGURAÇÕES
# ==============================

COLUNAS_VALOR_POR_TIPO = {
    "faturamento_produto": ["Total de Mercadoria"],
    "faturamento_cliente": ["Valor de Mercadoria", "Total de Mercadoria"],
}

COLUNAS_IDENTIFICACAO_POR_TIPO = {
    "faturamento_produto": "Descrição do Produto (completa)",
    "faturamento_cliente": "Cliente (Nome Fantasia)",
}

PASTA_CURVAS = "curvas"


# ==============================
# CÁLCULO DA CURVA ABC
# ==============================

def calcular_curva_abc(
    df: pd.DataFrame,
    coluna_valor: str,
    coluna_identificacao: str | None = None
) -> pd.DataFrame:

    if coluna_valor not in df.columns:
        colunas = ", ".join(str(coluna) for coluna in df.columns)

        raise ValueError(
            f"Coluna de valor '{coluna_valor}' não encontrada. "
            f"Colunas disponíveis: {colunas}"
        )

    df = df.copy()

    df[coluna_valor] = pd.to_numeric(
        df[coluna_valor],
        errors="coerce"
    )

    df = df.sort_values(
        by=coluna_valor,
        ascending=False
    ).reset_index(drop=True)

    total = df[coluna_valor].sum()

    df["% do Total"] = (
        df[coluna_valor] / total * 100
    ).round(2)

    df["% Acumulado"] = (
        df["% do Total"].cumsum()
    ).round(2)

    def classificar(percentual):
        if percentual <= 80:
            return "A"
        elif percentual <= 95:
            return "B"
        return "C"

    df["Classificação ABC"] = (
        df["% Acumulado"].apply(classificar)
    )

    if coluna_identificacao in df.columns:
        df = df[
            [
                coluna_identificacao,
                coluna_valor,
                "% do Total",
                "% Acumulado",
                "Classificação ABC",
            ]
        ]

    return df


# ==============================
# GERAÇÃO DO ARQUIVO
# ==============================

def gerar_curva_abc(
    df_tratado: pd.DataFrame,
    tipo_relatorio: str,
    nome_arquivo: str
) -> None:

    coluna_valor = next(
        (
            coluna
            for coluna in COLUNAS_VALOR_POR_TIPO[tipo_relatorio]
            if coluna in df_tratado.columns
        ),
        None
    )

    if coluna_valor is None:
        print("Coluna de valor não encontrada. Curva ABC não gerada.")
        return

    coluna_identificacao = COLUNAS_IDENTIFICACAO_POR_TIPO.get(
        tipo_relatorio
    )

    try:
        df_curva = calcular_curva_abc(
            df_tratado,
            coluna_valor,
            coluna_identificacao
        )

    except ValueError as erro:
        print(f"Não foi possível gerar a Curva ABC: {erro}")
        return

    os.makedirs(PASTA_CURVAS, exist_ok=True)

    nome_base, _ = os.path.splitext(nome_arquivo)
    nome_curva = f"curvaABC_{nome_base}.xlsx"

    caminho_saida = os.path.join(
        PASTA_CURVAS,
        nome_curva
    )

    df_curva.to_excel(
        caminho_saida,
        index=False
    )

    print(f"Curva ABC gerada: {caminho_saida}")


# ==============================
# PERGUNTA AO USUÁRIO
# ==============================

def perguntar_e_gerar_curva_abc(
    df_tratado: pd.DataFrame,
    tipo_relatorio: str,
    nome_arquivo: str
) -> None:

    if tipo_relatorio not in COLUNAS_VALOR_POR_TIPO:
        return

    resposta = input(
        "\nDeseja gerar a Curva ABC desta planilha? (S/N): "
    ).strip().lower()

    if resposta not in ("s", "sim"):
        return

    gerar_curva_abc(
        df_tratado,
        tipo_relatorio,
        nome_arquivo
    )
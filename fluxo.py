import os
import glob
import shutil
from datetime import datetime

import pandas as pd

import tratamento
import curva_abc


PASTA_ENTRADA = "entrada"
PASTA_SAIDA = "dados tratados"
PASTA_ERROS = "saida_erros"
PASTA_PROCESSADOS = "processados"

EXTENSOES_VALIDAS = ("*.xlsx", "*.xls")
EXTENSOES_VALIDAS_SUFIXO = (".xlsx", ".xls")


# ==============================
# ETAPA DE ENTRADA
# ==============================

def encontrar_arquivos_excel(pasta: str) -> list:
    arquivos = []

    for extensao in EXTENSOES_VALIDAS:
        arquivos.extend(
            glob.glob(os.path.join(pasta, extensao))
        )

    return arquivos


def selecionar_arquivo_mais_recente(arquivos: list) -> str:
    return max(arquivos, key=os.path.getmtime)


def encontrar_arquivos_invalidos(pasta: str) -> list:
    arquivos_invalidos = []

    for arquivo in glob.glob(os.path.join(pasta, "*")):
        if os.path.isfile(arquivo):
            _, extensao = os.path.splitext(arquivo)

            if extensao.lower() not in EXTENSOES_VALIDAS_SUFIXO:
                arquivos_invalidos.append(arquivo)

    return arquivos_invalidos


# ==============================
# ETAPA DE VALIDAÇÃO
# ==============================

def registrar_erro(motivo: str, caminho_arquivo: str) -> str:
    os.makedirs(PASTA_ERROS, exist_ok=True)

    agora = datetime.now()
    carimbo = agora.strftime("%Y-%m-%d_%H%M%S")
    caminho_log = os.path.join(
        PASTA_ERROS,
        f"erro_{carimbo}.txt"
    )

    with open(caminho_log, "w", encoding="utf-8") as arquivo:
        arquivo.write(
            f"Data/Hora: {agora.strftime('%d/%m/%Y %H:%M:%S')}\n"
        )
        arquivo.write(f"Arquivo: {caminho_arquivo}\n")
        arquivo.write(f"Motivo: {motivo}\n")

    return caminho_log


def validar_dados(df: pd.DataFrame) -> bool:
    return (
        df is not None
        and not df.empty
        and df.shape[0] > 0
        and df.shape[1] > 0
    )


def mover_para_processados(
    caminho_original: str,
    sucesso: bool
) -> str:

    os.makedirs(PASTA_PROCESSADOS, exist_ok=True)

    nome_arquivo = os.path.basename(caminho_original)

    if not sucesso:
        nome_arquivo = f"ERRO_{nome_arquivo}"

    caminho_destino = os.path.join(
        PASTA_PROCESSADOS,
        nome_arquivo
    )

    shutil.move(
        caminho_original,
        caminho_destino
    )

    return caminho_destino


def tratar_erro(
    motivo: str,
    caminho_arquivo: str
):
    print(f"Validação falhou: {motivo}")

    caminho_log = registrar_erro(
        motivo,
        caminho_arquivo
    )

    print(f"Erro registrado em: {caminho_log}")

    if os.path.isfile(caminho_arquivo):
        caminho_movido = mover_para_processados(
            caminho_arquivo,
            sucesso=False
        )
        print(f"Arquivo movido para: {caminho_movido}")

    print("Programa encerrado com segurança.")


# ==============================
# ETAPA DE SAÍDA
# ==============================

def salvar_dados_tratados(
    df: pd.DataFrame,
    pasta_destino: str
) -> str:

    os.makedirs(pasta_destino, exist_ok=True)

    titulo = df.attrs.get("titulo_relatorio")

    if titulo:
        nome_saida = f"{titulo} - Tratado.xlsx"
    else:
        nome_saida = "Relatorio - Tratado.xlsx"

    caminho_saida = os.path.join(
        pasta_destino,
        nome_saida
    )

    if titulo:
        with pd.ExcelWriter(
            caminho_saida,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                startrow=1
            )

            writer.book.active.cell(
                row=1,
                column=1,
                value=titulo
            )
    else:
        df.to_excel(
            caminho_saida,
            index=False
        )

    print("=== SAÍDA DOS DADOS ===")
    print(f"Arquivo criado: {nome_saida}")
    print(f"Local: {caminho_saida}")
    print(f"Linhas finais: {df.shape[0]}")
    print(f"Colunas finais: {df.shape[1]}")
    print("Automação concluída com sucesso!")

    return caminho_saida


# ==============================
# PROGRAMA PRINCIPAL
# ==============================

def main():

    print(
        "=== ETAPA DE ENTRADA - "
        "Automação Cactus Elétrica ===\n"
    )

    # Verifica arquivos inválidos
    arquivos_invalidos = encontrar_arquivos_invalidos(
        PASTA_ENTRADA
    )

    if arquivos_invalidos:
        motivo = (
            "Formato de arquivo não suportado. "
            "Apenas arquivos Excel (.xlsx ou .xls) são aceitos."
        )

        for arquivo in arquivos_invalidos:
            tratar_erro(
                motivo,
                arquivo
            )

        return

    # Procura os arquivos Excel
    arquivos = encontrar_arquivos_excel(
        PASTA_ENTRADA
    )

    if not arquivos:
        print(
            f"Nenhum arquivo Excel foi encontrado "
            f"na pasta '{PASTA_ENTRADA}'."
        )
        print(
            "Coloque um arquivo .xlsx ou .xls "
            "nessa pasta e rode o script novamente."
        )
        return

    caminho_selecionado = selecionar_arquivo_mais_recente(
        arquivos
    )

    nome_arquivo = os.path.basename(
        caminho_selecionado
    )

    print(f"Arquivos Excel encontrados: {len(arquivos)}")
    print(
        f"Arquivo selecionado (mais recente): "
        f"{nome_arquivo}"
    )
    print(
        f"Caminho completo: "
        f"{caminho_selecionado}\n"
    )

    print("=== ETAPA DE VALIDAÇÃO ===")

    # Verifica se o arquivo ainda existe
    if not os.path.isfile(caminho_selecionado):
        tratar_erro(
            "O arquivo selecionado não existe mais no disco.",
            caminho_selecionado
        )
        return

    # Verifica a extensão
    _, extensao = os.path.splitext(
        caminho_selecionado
    )

    if extensao.lower() not in EXTENSOES_VALIDAS_SUFIXO:
        tratar_erro(
            f"Extensão '{extensao}' não é um Excel válido "
            "(.xlsx ou .xls).",
            caminho_selecionado
        )
        return

    # Carrega a planilha sem assumir cabeçalho
    try:
        df_bruto = pd.read_excel(
            caminho_selecionado,
            header=None
        )

    except Exception as erro:
        tratar_erro(
            f"O Pandas não conseguiu abrir o arquivo. "
            f"Detalhe: {erro}",
            caminho_selecionado
        )
        return

    print("=== Resumo do arquivo carregado ===")
    print(f"Linhas: {df_bruto.shape[0]}")
    print(f"Colunas: {df_bruto.shape[1]}\n")

    if not validar_dados(df_bruto):
        tratar_erro(
            "O DataFrame está vazio ou não possui "
            "linhas/colunas suficientes.",
            caminho_selecionado
        )
        return

    print(
        "Validação concluída: dados válidos, "
        "seguindo para o tratamento.\n"
    )

    # ==============================
    # TRATAMENTO
    # ==============================

    df_tratado, tipo_relatorio = (
        tratamento.processar_relatorio(
            df_bruto
        )
    )

    print(
        f"Relatório identificado como: "
        f"{tipo_relatorio}\n"
    )

    # Define o destino conforme o tipo do relatório
    pasta_destino = tratamento.DESTINOS_POR_TIPO.get(
        tipo_relatorio,
        PASTA_SAIDA
    )

    salvar_dados_tratados(
        df_tratado,
        pasta_destino
    )

    curva_abc.perguntar_e_gerar_curva_abc(
    df_tratado,
    tipo_relatorio,
    nome_arquivo
    )

    # Move o arquivo original após o processamento
    caminho_movido = mover_para_processados(
        caminho_selecionado,
        sucesso=True
    )

    print(
        f"Arquivo original movido para: "
        f"{caminho_movido}"
    )


if __name__ == "__main__":
    main()
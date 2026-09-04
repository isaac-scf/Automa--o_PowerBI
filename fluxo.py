import os
import glob
import shutil
from datetime import datetime

import pandas as pd
import tratamento


PASTA_ENTRADA = "entrada"
PASTA_SAIDA = "dados tratados"
PASTA_ERROS = "saida_erros"
PASTA_PROCESSADOS = "processados"

EXTENSOES_VALIDAS = (".xlsx", ".xls")


# ==============================
# ENTRADA
# ==============================

def encontrar_arquivos_excel(pasta):
    arquivos = []

    for extensao in EXTENSOES_VALIDAS:
        arquivos.extend(
            glob.glob(os.path.join(pasta, f"*{extensao}"))
        )

    return arquivos


def selecionar_arquivo_mais_recente(arquivos):
    return max(arquivos, key=os.path.getmtime)


def encontrar_arquivos_invalidos(pasta):
    invalidos = []

    for arquivo in glob.glob(os.path.join(pasta, "*")):
        if os.path.isfile(arquivo):
            extensao = os.path.splitext(arquivo)[1].lower()

            if extensao not in EXTENSOES_VALIDAS:
                invalidos.append(arquivo)

    return invalidos


# ==============================
# VALIDAÇÃO
# ==============================

def registrar_erro(motivo, caminho_arquivo):
    os.makedirs(PASTA_ERROS, exist_ok=True)

    agora = datetime.now()
    carimbo = agora.strftime("%Y-%m-%d_%H%M%S")

    caminho_log = os.path.join(
        PASTA_ERROS,
        f"erro_{carimbo}.txt"
    )

    with open(caminho_log, "w", encoding="utf-8") as log:
        log.write(
            f"Data/Hora: {agora.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Arquivo: {caminho_arquivo}\n"
            f"Motivo: {motivo}\n"
        )

    return caminho_log


def validar_dados(df):
    return (
        df is not None
        and not df.empty
        and df.shape[0] > 0
        and df.shape[1] > 0
    )


def tratar_erro(motivo, caminho_arquivo):
    print(f"Validação falhou: {motivo}")

    log = registrar_erro(
        motivo,
        caminho_arquivo
    )

    print(f"Erro registrado em: {log}")

    if os.path.isfile(caminho_arquivo):
        destino = mover_para_processados(
            caminho_arquivo,
            sucesso=False
        )

        print(f"Arquivo movido para: {destino}")

    print("Programa encerrado com segurança.\n")


def mover_para_processados(caminho_original, sucesso):
    os.makedirs(PASTA_PROCESSADOS, exist_ok=True)

    nome = os.path.basename(caminho_original)

    if not sucesso:
        nome = f"ERRO_{nome}"

    destino = os.path.join(
        PASTA_PROCESSADOS,
        nome
    )

    shutil.move(
        caminho_original,
        destino
    )

    return destino


# ==============================
# SAÍDA
# ==============================

def salvar_dados_tratados(df, caminho_original, tipo_relatorio):

    pasta_destino = tratamento.DESTINOS_POR_TIPO.get(
        tipo_relatorio,
        PASTA_SAIDA
    )

    os.makedirs(
        pasta_destino,
        exist_ok=True
    )

    nome_base = os.path.splitext(
        os.path.basename(caminho_original)
    )[0]

    nome_saida = f"{nome_base}_tratado.xlsx"

    caminho_saida = os.path.join(
        pasta_destino,
        nome_saida
    )

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

    # Procura arquivos Excel
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

    # Seleciona o mais recente
    caminho_selecionado = selecionar_arquivo_mais_recente(
        arquivos
    )

    nome_arquivo = os.path.basename(
        caminho_selecionado
    )

    print(
        f"Arquivos Excel encontrados: {len(arquivos)}"
    )

    print(
        f"Arquivo selecionado (mais recente): "
        f"{nome_arquivo}"
    )

    print(
        f"Caminho completo: "
        f"{caminho_selecionado}\n"
    )

    print("=== ETAPA DE VALIDAÇÃO ===")

    # Arquivo existe?
    if not os.path.isfile(caminho_selecionado):

        tratar_erro(
            "O arquivo selecionado não existe mais no disco.",
            caminho_selecionado
        )

        return

    # Extensão válida?
    extensao = os.path.splitext(
        caminho_selecionado
    )[1].lower()

    if extensao not in EXTENSOES_VALIDAS:

        tratar_erro(
            f"Extensão '{extensao}' não é um Excel válido.",
            caminho_selecionado
        )

        return

    # Tenta abrir o Excel
    try:

        df = pd.read_excel(
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
    print(f"Linhas: {df.shape[0]}")
    print(f"Colunas: {df.shape[1]}\n")

    # Dados válidos?
    if not validar_dados(df):

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

    df, tipo_relatorio = tratamento.processar_relatorio(df)

    # ==============================
    # SAÍDA
    # ==============================

    salvar_dados_tratados(
        df,
        caminho_selecionado,
        tipo_relatorio
    )

    # Move original após sucesso
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
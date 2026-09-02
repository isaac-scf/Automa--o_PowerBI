import os
import glob
import shutil
from datetime import datetime
import pandas as pd

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
    arquivos_encontrados = []

    for extensao in EXTENSOES_VALIDAS:
        caminho_busca = os.path.join(pasta, extensao)
        arquivos_encontrados.extend(glob.glob(caminho_busca))

    return arquivos_encontrados


def selecionar_arquivo_mais_recente(lista_arquivos: list) -> str:
    arquivo_mais_recente = max(
        lista_arquivos,
        key=os.path.getmtime
    )

    return arquivo_mais_recente


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
    caminho_log = os.path.join(PASTA_ERROS, f"erro_{carimbo}.txt")

    with open(caminho_log, "w", encoding="utf-8") as arquivo_log:
        arquivo_log.write(
            f"Data/Hora: {agora.strftime('%d/%m/%Y %H:%M:%S')}\n"
        )
        arquivo_log.write(f"Arquivo: {caminho_arquivo}\n")
        arquivo_log.write(f"Motivo: {motivo}\n")

    return caminho_log


def validar_dados(df: pd.DataFrame) -> bool:
    if df is None:
        return False

    if df.empty:
        return False

    if df.shape[0] == 0 or df.shape[1] == 0:
        return False

    return True


def mover_para_processados(caminho_original: str, sucesso: bool) -> str:
    """
    Move o arquivo original (que já passou pelo código, com sucesso
    ou não) da pasta "entrada" para "processados". Isso garante que
    ele nunca mais seja encontrado/selecionado numa próxima execução.

    Se "sucesso" for False, o arquivo é renomeado com o prefixo
    "ERRO_" para ficar visualmente identificável dentro da mesma
    pasta "processados" — o motivo detalhado do erro continua
    registrado à parte, em "saida_erros".
    """
    os.makedirs(PASTA_PROCESSADOS, exist_ok=True)

    nome_arquivo = os.path.basename(caminho_original)

    if not sucesso:
        nome_arquivo = f"ERRO_{nome_arquivo}"

    caminho_destino = os.path.join(PASTA_PROCESSADOS, nome_arquivo)

    shutil.move(caminho_original, caminho_destino)

    return caminho_destino


# ==============================
# ETAPA DE TRATAMENTO
# ==============================

def tratar_dados(df: pd.DataFrame) -> pd.DataFrame:

    print("=== ETAPA DE TRATAMENTO DOS DADOS ===")

    # REGRA DE TESTE
    # Manter somente as 10 últimas linhas
    df = df.tail(10)

    print(f"Linhas após o tratamento: {df.shape[0]}")
    print(f"Colunas após o tratamento: {df.shape[1]}\n")

    # ==========================================
    # ESPAÇO PARA FUTURAS REGRAS DE TRATAMENTO
    # ==========================================

    return df


# ==============================
# ETAPA DE SAÍDA
# ==============================

def salvar_dados_tratados(
    df: pd.DataFrame,
    caminho_original: str
) -> str:

    os.makedirs(PASTA_SAIDA, exist_ok=True)

    nome_original = os.path.basename(caminho_original)

    nome_base, _ = os.path.splitext(nome_original)

    nome_saida = f"{nome_base}_tratado.xlsx"

    caminho_saida = os.path.join(
        PASTA_SAIDA,
        nome_saida
    )

    df.to_excel(caminho_saida, index=False)

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

    print("=== ETAPA DE ENTRADA - Automação Cactus Elétrica ===\n")

    # Procura arquivos inválidos na pasta
    arquivos_invalidos = encontrar_arquivos_invalidos(PASTA_ENTRADA)

    if arquivos_invalidos:
        for arquivo_invalido in arquivos_invalidos:

            motivo = (
                "Formato de arquivo não suportado. "
                "Apenas arquivos Excel (.xlsx ou .xls) são aceitos."
            )

            print(f"Validação falhou: {motivo}")
            print(f"Arquivo: {arquivo_invalido}")

            caminho_log = registrar_erro(
                motivo,
                arquivo_invalido
            )

            print(f"Erro registrado em: {caminho_log}")

            caminho_movido = mover_para_processados(
                arquivo_invalido,
                sucesso=False
            )

            print(f"Arquivo movido para: {caminho_movido}")

        print("Programa encerrado com segurança.")
        return

    # Procura os arquivos Excel
    arquivos = encontrar_arquivos_excel(PASTA_ENTRADA)

    # Verifica se encontrou algum arquivo
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

    # Seleciona o arquivo mais recente
    caminho_selecionado = selecionar_arquivo_mais_recente(arquivos)

    nome_arquivo = os.path.basename(caminho_selecionado)

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

    # Valida se o arquivo ainda existe no disco
    if not os.path.isfile(caminho_selecionado):
        motivo = "O arquivo selecionado não existe mais no disco."
        print(f"Validação falhou: {motivo}")
        caminho_log = registrar_erro(motivo, caminho_selecionado)
        print(f"Erro registrado em: {caminho_log}")
        # Não há arquivo pra mover: ele já não existe no disco.
        print("Programa encerrado com segurança.")
        return

    # Valida se a extensão é um Excel aceito
    _, extensao_arquivo = os.path.splitext(caminho_selecionado)

    if extensao_arquivo.lower() not in EXTENSOES_VALIDAS_SUFIXO:
        motivo = (
            f"Extensão '{extensao_arquivo}' "
            "não é um Excel válido (.xlsx ou .xls)."
        )

        print(f"Validação falhou: {motivo}")

        caminho_log = registrar_erro(
            motivo,
            caminho_selecionado
        )

        print(f"Erro registrado em: {caminho_log}")

        caminho_movido = mover_para_processados(
            caminho_selecionado,
            sucesso=False
        )

        print(f"Arquivo movido para: {caminho_movido}")
        print("Programa encerrado com segurança.")
        return

    # Valida se o Pandas consegue abrir o arquivo
    try:
        df = pd.read_excel(caminho_selecionado)

    except Exception as erro:
        motivo = (
            f"O Pandas não conseguiu abrir o arquivo. "
            f"Detalhe: {erro}"
        )

        print(f"Validação falhou: {motivo}")

        caminho_log = registrar_erro(
            motivo,
            caminho_selecionado
        )

        print(f"Erro registrado em: {caminho_log}")

        caminho_movido = mover_para_processados(
            caminho_selecionado,
            sucesso=False
        )

        print(f"Arquivo movido para: {caminho_movido}")
        print("Programa encerrado com segurança.")
        return

    print("=== Resumo do arquivo carregado ===")
    print(f"Linhas: {df.shape[0]}")
    print(f"Colunas: {df.shape[1]}\n")

    # Valida se o DataFrame não está vazio e tem linhas/colunas
    if not validar_dados(df):
        motivo = (
            "O DataFrame está vazio ou não possui "
            "linhas/colunas suficientes."
        )

        print(f"Validação falhou: {motivo}")

        caminho_log = registrar_erro(
            motivo,
            caminho_selecionado
        )

        print(f"Erro registrado em: {caminho_log}")

        caminho_movido = mover_para_processados(
            caminho_selecionado,
            sucesso=False
        )

        print(f"Arquivo movido para: {caminho_movido}")
        print("Programa encerrado com segurança.")
        return

    print(
        "Validação concluída: dados válidos, "
        "seguindo para o tratamento.\n"
    )

    # Trata os dados
    df = tratar_dados(df)

    # Salva o resultado
    salvar_dados_tratados(
        df,
        caminho_selecionado
    )

    # Move o arquivo original para "processados", já com sucesso
    caminho_movido = mover_para_processados(
        caminho_selecionado,
        sucesso=True
    )

    print(f"Arquivo original movido para: {caminho_movido}")


if __name__ == "__main__":
    main()
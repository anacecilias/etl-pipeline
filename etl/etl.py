# etl.py
import pandas as pd
import unicodedata
import os
import json
from sqlalchemy import create_engine

# -------- CONFIG --------

def carregar_config(caminho="config.json"):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

# -------- EXTRACT --------

def ler_arquivo(caminho):
    ext = caminho.lower().split(".")[-1]

    if ext in ["xlsx", "xls", "ods"]:
        return pd.read_excel(caminho)
    elif ext in ["csv", "tsv"]:
        sep = "\t" if ext == "tsv" else ","
        return pd.read_csv(caminho, sep=sep)
    else:
        raise ValueError("Formato de arquivo não suportado.")

def ler_banco(engine_url, tabela):
    engine = create_engine(engine_url)
    return pd.read_sql_table(tabela, engine)

# -------- TRANSFORM --------

def normalizar_texto(texto):
    texto = str(texto).upper().strip()
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return texto

def filtrar_tabulacoes(df, config):
    idx = config["coluna_tabulacao"]
    validas = [normalizar_texto(t) for t in config["tabulacoes_validas"]]

    df["TAB_NORM"] = df.iloc[:, idx].apply(normalizar_texto)
    return df[df["TAB_NORM"].isin(validas)]

def organizar(df, config):
    mapeamento = config["mapeamento_colunas"]
    fixas = config.get("colunas_fixas", {})

    out = pd.DataFrame()

    for nome_saida, idx_entrada in mapeamento.items():
        out[nome_saida] = df.iloc[:, idx_entrada]

    for nome_saida, valor in fixas.items():
        out[nome_saida] = valor

    return out

def separar_por_coluna(df, coluna):
    separados = {}
    col_norm = f"{coluna}_NORM"
    df[col_norm] = df[coluna].apply(normalizar_texto)

    for valor in df[coluna].dropna().unique():
        vnorm = normalizar_texto(valor)
        separados[vnorm] = df[df[col_norm] == vnorm]

    return separados

# -------- LOAD --------

def salvar_csvs(dfs, pasta, prefixo="EXPORT"):
    os.makedirs(pasta, exist_ok=True)
    arquivos = []

    for nome, df in dfs.items():
        nome_arquivo = f"{prefixo}_{nome}.csv"
        caminho = os.path.join(pasta, nome_arquivo)
        df.to_csv(caminho, index=False, encoding="utf-8-sig")
        arquivos.append(nome_arquivo)  # retorna só o nome (melhor pra API)

    return arquivos

# -------- PIPELINE --------

def run_etl_from_file(caminho_arquivo):
    config = carregar_config()

    df_raw = ler_arquivo(caminho_arquivo)
    df_filtrado = filtrar_tabulacoes(df_raw, config)
    df_out = organizar(df_filtrado, config)

    col_split = config.get("split_por")
    if col_split:
        dfs = separar_por_coluna(df_out, col_split)
    else:
        dfs = {"resultado": df_out}

    pasta = config["saida"]["pasta"]
    prefixo = config["saida"].get("prefixo", "EXPORT")

    arquivos = salvar_csvs(dfs, pasta, prefixo)

    return {
        "linhas_processadas": len(df_out),
        "arquivos_gerados": arquivos
    }

def run_etl_from_db(engine_url, tabela):
    config = carregar_config()

    df_raw = ler_banco(engine_url, tabela)
    df_filtrado = filtrar_tabulacoes(df_raw, config)
    df_out = organizar(df_filtrado, config)

    col_split = config.get("split_por")
    if col_split:
        dfs = separar_por_coluna(df_out, col_split)
    else:
        dfs = {"resultado": df_out}

    pasta = config["saida"]["pasta"]
    prefixo = config["saida"].get("prefixo", "EXPORT")

    arquivos = salvar_csvs(dfs, pasta, prefixo)

    return {
        "linhas_processadas": len(df_out),
        "arquivos_gerados": arquivos
    }
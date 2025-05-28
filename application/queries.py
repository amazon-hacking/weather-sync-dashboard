import pandas as pd

def get_poluentes_unicos(engine):
    query = "SELECT DISTINCT poluente FROM gold.poluentes_por_bairro"
    return pd.read_sql(query, engine)

def get_poluente_por_bairro(engine, poluente):
    query = """
        SELECT bairro, media_valor
        FROM gold.poluentes_por_bairro
        WHERE poluente = %s
    """
    return pd.read_sql(query, engine, params=(poluente,))

def get_bairros_disponiveis(engine):
    query = "SELECT DISTINCT bairro FROM gold.media_humidade_por_bairro_e_dia"
    return pd.read_sql(query, engine)

def get_temperatura(engine, params):
    query = """
        SELECT data, bairro, temperatura_media
        FROM gold.media_temperatura_por_bairro_e_dia
        WHERE data BETWEEN %(data_ini)s AND %(data_fim)s
          AND bairro = ANY(%(bairros)s)
        ORDER BY data, bairro
    """
    return pd.read_sql(query, engine, params=params)

def get_umidade(engine, params):
    query = """
        SELECT data, bairro, humidade_media
        FROM gold.media_humidade_por_bairro_e_dia
        WHERE data BETWEEN %(data_ini)s AND %(data_fim)s
          AND bairro = ANY(%(bairros)s)
        ORDER BY data, bairro
    """
    return pd.read_sql(query, engine, params=params)

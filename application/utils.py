import pandas as pd

def checagem_data(df):
    """
    Prepara os dados de data para exibição nos gráficos.
    Mantém a data original para ordenação e cria uma versão formatada para exibição.
    """
    if df.empty:
        return df
    
    # Se a coluna data já está como datetime, mantém uma cópia
    if pd.api.types.is_datetime64_any_dtype(df["data"]):
        # Cria uma coluna auxiliar para ordenação (mantém como datetime)
        df["data_ordenacao"] = df["data"]
        # Formata para exibição brasileira
        df["data_formatada"] = df["data"].dt.strftime('%d/%m/%Y')
    else:
        # Se já está como string, tenta converter de volta para datetime
        try:
            # Tenta diferentes formatos de data
            df["data_ordenacao"] = pd.to_datetime(df["data"], format='%d/%m/%Y', errors='coerce')
            if df["data_ordenacao"].isna().all():
                df["data_ordenacao"] = pd.to_datetime(df["data"], format='%Y-%m-%d', errors='coerce')
            df["data_formatada"] = df["data_ordenacao"].dt.strftime('%d/%m/%Y')
        except:
            # Se não conseguir converter, usa a string original
            df["data_formatada"] = df["data"].astype(str)
            df["data_ordenacao"] = df["data"].astype(str)
    
    # Ordena pelo datetime real antes de retornar
    if "data_ordenacao" in df.columns and not df["data_ordenacao"].isna().all():
        df = df.sort_values("data_ordenacao")
    
    # Converte para string para compatibilidade com o código existente
    df["data"] = df["data_formatada"].astype(str)
    
    return df
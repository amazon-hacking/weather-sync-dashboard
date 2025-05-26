# # POLUENTE POR BAIRRO 💚💚

import streamlit as st
import pandas as pd
import pandasql as ps
from sqlalchemy import create_engine
import altair as alt

# Conexão para criar uma engine do SQLalchemy
db_config = st.secrets["tembo_db"]

username = db_config["username"]
password = db_config["password"]
host = db_config["host"]
port = db_config["port"]
database = db_config["database"]

engine = create_engine(f"postgresql://{username}:{password}@{host}/{database}")

# MÉDIA DE POLUENTES POR BAIRRO NO PERÍODO INTERIRO 💚💚

query_poluentes_unicos = "SELECT DISTINCT poluente FROM gold.poluentes_por_bairro"
poluentes = pd.read_sql(query_poluentes_unicos, engine)

poluente_escolhido = st.radio(
    "Qual o poluente que será analisado? (Clique em uma opção)",
    poluentes["poluente"].tolist(),
)

# Query filtrada direto no banco para o poluente escolhido
query_poluentes_por_bairro = f"""
    SELECT bairro, media_valor
    FROM gold.poluentes_por_bairro
    WHERE poluente = %s
"""

df_filtrado = pd.read_sql(query_poluentes_por_bairro, engine, params=(poluente_escolhido,))

chart = (
    alt.Chart(df_filtrado)
    .mark_bar(color="#4caf50")
    .encode(
        y=alt.Y('bairro:N', sort='-x', title='Bairro'),  
        x=alt.X('media_valor:Q', title='Média de Poluentes'),  
        tooltip=['bairro', 'media_valor']
    )
    .properties(
        title=f"Média de {poluente_escolhido} por bairro",
        width=700,
        height=400
    )
)

st.altair_chart(chart, use_container_width=True)

# TEMPERATURA E HUMIDADE MEDIAS POR PERÍODO E BAIRRO 💚💚

data_ini = st.date_input("Data inicial")
data_fim = st.date_input("Data final")
bairro = st.selectbox("Selecione o bairro", options=pd.read_sql("SELECT DISTINCT bairro FROM gold.media_humidade_por_bairro_e_dia", engine))
params = (bairro, data_ini, data_fim)

query_temperatura_periodo = """
    SELECT * FROM gold.media_temperatura_por_bairro_e_dia
    WHERE bairro = %s AND data BETWEEN %s AND %s
    ORDER BY data;
"""

query_umidade_periodo = """
    SELECT * FROM gold.media_humidade_por_bairro_e_dia
    WHERE bairro = %s AND data BETWEEN %s AND %s
    ORDER BY data;
"""

# TEMPERATURA:

consulta_temp = pd.read_sql(query_temperatura_periodo, engine, params=params)
if pd.api.types.is_datetime64_any_dtype(consulta_temp["data"]): # Checa se é datetime
    consulta_temp["data"] = consulta_temp["data"].dt.strftime('%d/%m/%Y') # Converte a data para formato brasileiro
consulta_temp["data"] = consulta_temp["data"].astype(str)

if not consulta_temp.empty:
    chart = alt.Chart(consulta_temp).mark_bar().encode(
        x=alt.X("data:N", title="Data"), #O :N garante que o eixo X seja tratado como NOMINAL
        y=alt.Y("temperatura_media:Q", title="Temperatura Média"), #O :Q garante que o eixo Y seja tratado como quantitativo
        tooltip=["data", "temperatura_media"]
    ).properties(
        width=700,
        height=400,
        title=f"Temperatura média diária - {bairro}"
    )

    st.altair_chart(chart, use_container_width=True) #container_width=True garante responsividade
else:
    st.warning("Nenhum dado encontrado para o período e bairro selecionados.")
    
# UMIDADE:

consulta_umidade = pd.read_sql(query_umidade_periodo, engine, params=params)
if pd.api.types.is_datetime64_any_dtype(consulta_umidade["data"]): # Checa se é datetime
    consulta_umidade["data"] = consulta_umidade["data"].dt.strftime('%d/%m/%Y') # Converte a data para formato brasileiro
consulta_umidade["data"] = consulta_umidade["data"].astype(str)

if not consulta_umidade.empty:
    chart = alt.Chart(consulta_umidade).mark_bar().encode(
        x=alt.X("data:N", title="Data"), #O :N garante que o eixo X seja tratado como NOMINAL
        y=alt.Y("humidade_media:Q", title="Umidade Média"), #O :Q garante que o eixo Y seja tratado como quantitativo
        tooltip=["data", "humidade_media"]
    ).properties(
        width=700,
        height=400,
        title=f"Umidade média diária - {bairro}"
    )

    st.altair_chart(chart, use_container_width=True) #container_width=True garante responsividade
else:
    st.warning("Nenhum dado encontrado para o período e bairro selecionados.")

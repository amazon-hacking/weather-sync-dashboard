# # POLUENTE POR BAIRRO 💚💚

import streamlit as st
import pandas as pd
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
query_poluentes_por_bairro = """
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

# Inputs do usuário
data_ini = st.date_input("Data inicial")
data_fim = st.date_input("Data final")
bairros_disponiveis = pd.read_sql("SELECT DISTINCT bairro FROM gold.media_humidade_por_bairro_e_dia", engine)
bairros = st.multiselect("Selecione os bairros", options=bairros_disponiveis['bairro'].tolist())

# Parâmetros para Queries de Temp. e Umi.
params = {
        "data_ini": data_ini,
        "data_fim": data_fim,
        "bairros": bairros,
        }

query_temperatura_periodo = """
        SELECT data, bairro, temperatura_media
        FROM gold.media_temperatura_por_bairro_e_dia
        WHERE data BETWEEN %(data_ini)s AND %(data_fim)s
          AND bairro = ANY(%(bairros)s)
        ORDER BY data, bairro
    """

query_umidade_periodo = """
    SELECT data, bairro, humidade_media
    FROM gold.media_humidade_por_bairro_e_dia
    WHERE data BETWEEN %(data_ini)s AND %(data_fim)s
        AND bairro = ANY(%(bairros)s)
    ORDER BY data, bairro
"""

# Faz as consultas no banco
consulta_temp = pd.read_sql(query_temperatura_periodo, engine, params=params)
consulta_umidade = pd.read_sql(query_umidade_periodo, engine, params=params)

# Passando as datas para string
for df in [consulta_temp, consulta_umidade]:
    if pd.api.types.is_datetime64_any_dtype(df["data"]):
        df["data"] = df["data"].dt.strftime('%d/%m/%Y')
    df["data"] = df["data"].astype(str)

# Garantindo que as datas estão no formato correto
def checagem_data(consulta):
    if pd.api.types.is_datetime64_any_dtype(consulta["data"]): # Checa se é datetime
        consulta["data"] = consulta["data"].dt.strftime('%d/%m/%Y') # Converte a data para formato brasileiro
    consulta["data"] = consulta["data"].astype(str)
    
# TEMPERATURA:

checagem_data(consulta_temp)

if not consulta_temp.empty:
    chart_temp = alt.Chart(consulta_temp).mark_bar().encode(
        x=alt.X("data:N", title="Data", axis=alt.Axis(labelAngle=-45)), #O :N garante que o eixo X seja tratado como NOMINAL
        y=alt.Y("temperatura_media:Q", title="Temperatura Média"),  #O :Q garante que o eixo Y seja tratado como quantitativo
        color=alt.Color("bairro:N", title="Bairro"),
        tooltip=["data", "bairro", "temperatura_media"]
    ).properties(
        width=max(700, 40 * consulta_temp['data'].nunique()),  # largura proporcional ao número de dias
        height=400,
        title="Temperatura média diária por bairro"
    )
    
    st.altair_chart(chart_temp.interactive(), use_container_width=True) #container_width=True garante responsividade
else:
    st.warning("Nenhum dado encontrado para o período e bairro selecionados.")
    
# UMIDADE:

checagem_data(consulta_umidade)

if not consulta_umidade.empty:
    chart_umidade = alt.Chart(consulta_umidade).mark_bar().encode(
        x=alt.X("data:N", title="Data", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("humidade_media:Q", title="Umidade Média"),
        color=alt.Color("bairro:N", title="Bairro"),
        xOffset="bairro:N",
        tooltip=["data", "bairro", "humidade_media"]
    ).properties(
        width=max(700, 40 * consulta_umidade['data'].nunique()),
        height=400,
        title="Umidade média diária por bairro"
    )

    st.altair_chart(chart_umidade.interactive(), use_container_width=True)
else:
    st.warning("Nenhum dado encontrado para o período e bairro selecionados.")

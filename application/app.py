# application/app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from application.db import get_engine
from application.queries import *
from application.charts import *
from application.utils import checagem_data

engine = get_engine()

# Poluentes
poluentes = get_poluentes_unicos(engine)
poluente_escolhido = st.radio("Escolha um poluente:", poluentes["poluente"].tolist())
df_poluente = get_poluente_por_bairro(engine, poluente_escolhido)

if 'mostrar_grafico_poluentes' not in st.session_state:
    st.session_state.mostrar_grafico_poluentes = True

st.button("Trocar Exibição", key="troca_exibicao_poluentes",
          on_click=lambda: st.session_state.update({"mostrar_grafico_poluentes": not st.session_state.mostrar_grafico_poluentes}))

if st.session_state.mostrar_grafico_poluentes:
    st.altair_chart(chart_poluente(df_poluente, poluente_escolhido), use_container_width=True)
else:
    st.dataframe(df_poluente)

# Temperatura e Umidade
data_ini = st.date_input("Data inicial")
data_fim = st.date_input("Data final")
bairros = st.multiselect("Selecione os bairros", get_bairros_disponiveis(engine)['bairro'].tolist())

params = {"data_ini": data_ini, "data_fim": data_fim, "bairros": bairros}

df_temp = checagem_data(get_temperatura(engine, params))
df_umi = checagem_data(get_umidade(engine, params))

if 'mostrar_grafico_umi_temp' not in st.session_state:
    st.session_state.mostrar_grafico_umi_temp = True

st.button("Trocar Exibição", key="troca_exibicao_umi_temp",
          on_click=lambda: st.session_state.update({"mostrar_grafico_umi_temp": not st.session_state.mostrar_grafico_umi_temp}))

if not df_temp.empty:
    if st.session_state.mostrar_grafico_umi_temp:
        st.altair_chart(chart_temperatura(df_temp).interactive(), use_container_width=True)
    else:
        st.dataframe(df_temp)
else:
    st.warning("Nenhum dado de temperatura encontrado.")

if not df_umi.empty:
    if st.session_state.mostrar_grafico_umi_temp:
        st.altair_chart(chart_umidade(df_umi).interactive(), use_container_width=True)
    else:
        st.dataframe(df_umi)
else:
    st.warning("Nenhum dado de umidade encontrado.")

# POLUENTE POR BAIRRO 💚💚

# import streamlit as st
# import pandas as pd
# import pandasql as ps

# # Conexão com banco
# conn = st.connection("tembo_db")
# df = conn.query("select * from gold.poluentes_por_bairro")

# # Botões de seleção única
# poluente_escolhido = st.radio(
#     "Qual o poluente que será anlisado?",
#     ["Dióxido de enxofre", "Dióxido de nitrogênio", "Monóxido de carbono", "Ozônio", "Partículas em suspensão finas (<2,5μm)", "Partículas em suspensão inaláveis (<10μm)"],
#     index=None,
# )

# # Consulta filtrada da view
# query = f"""
#     SELECT 
#         bairro, media_valor
#     FROM df
#     WHERE poluente = '{poluente_escolhido}'
# """
# df_filtrado = ps.sqldf(query, locals())

# # Construção das tabelas e gráficos
# tab1, tab2 = st.tabs(["📊 Gráfico", "📋 Tabela"])
# tab1.area_chart(df_filtrado.set_index("bairro"), color=['#1BF59B'], height=250)
# tab2.dataframe(df_filtrado, height=250, use_container_width=True)
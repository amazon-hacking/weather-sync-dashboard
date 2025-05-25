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

# TEMPERATURA E HUMIDADE MEDIAS DIARIAS E MENSAIS POR BAIRRO 💚💚

# query = 'SELECT * FROM gold.media_temperatura_por_bairro_e_dia;'
# df_temperatura_por_bairro_e_dia = pd.read_sql(query, conn)
# query = 'SELECT * FROM gold.media_humidade_por_bairro_e_dia;'
# df_humidade_por_bairro_e_dia = pd.read_sql(query, conn)
# query = 'SELECT bairro, data as mês, temperatura_media FROM gold.media_temperatura_por_bairro_e_mes;'
# df_temperatura_por_bairro_e_mes = pd.read_sql(query, conn)
# query = 'SELECT bairro, data as mês, humidade_media FROM gold.media_humidade_por_bairro_e_mes;'
# df_humidade_por_bairro_e_mes = pd.read_sql(query, conn)

# df_temperatura_por_bairro_e_mes['mês'] = pd.to_datetime(df_temperatura_por_bairro_e_mes['mês'])
# df_humidade_por_bairro_e_mes['mês'] = pd.to_datetime(df_humidade_por_bairro_e_mes['mês'])
# df_temperatura_por_bairro_e_mes['mês'] = df_temperatura_por_bairro_e_mes['mês'].dt.month
# df_humidade_por_bairro_e_mes['mês'] = df_humidade_por_bairro_e_mes['mês'].dt.month

# st.title('Temperatura média diária de cada bairro')

# bairros_selecionados_temperatura_dia = []
# for bairro in df_temperatura_por_bairro_e_dia['bairro'].unique():
#     if st.checkbox(bairro, value=True, key=f'temp_dia_{bairro}'):
#         bairros_selecionados_temperatura_dia.append(bairro)

# df_filtrado_temperatura_dia = df_temperatura_por_bairro_e_dia[df_temperatura_por_bairro_e_dia['bairro'].isin(bairros_selecionados_temperatura_dia)]
# st.line_chart(df_filtrado_temperatura_dia, x='data', y='temperatura_media', color='bairro', x_label='Data', y_label='Temperatura média')

# st.title('Humidade média diária de cada bairro')

# bairros_selecionados_humidade_dia = []
# for bairro in df_humidade_por_bairro_e_dia['bairro'].unique():
#     if st.checkbox(bairro, value=True, key=f'hum_dia_{bairro}'):
#         bairros_selecionados_humidade_dia.append(bairro)

# df_filtrado_humidade_dia = df_humidade_por_bairro_e_dia[df_humidade_por_bairro_e_dia['bairro'].isin(bairros_selecionados_humidade_dia)]
# st.line_chart(df_filtrado_humidade_dia, x='data', y='humidade_media', color='bairro', x_label='Data', y_label='Humidade média')

# st.title('Temperatura média por mês de cada bairro')

# bairros_selecionados_temperatura_mes = []
# for bairro in df_temperatura_por_bairro_e_mes['bairro'].unique():
#     if st.checkbox(bairro, value=True, key=f'temp_mes_{bairro}'):
#         bairros_selecionados_temperatura_mes.append(bairro)

# df_filtrado_temperatura_mes = df_temperatura_por_bairro_e_mes[df_temperatura_por_bairro_e_mes['bairro'].isin(bairros_selecionados_temperatura_mes)]
# st.bar_chart(df_filtrado_temperatura_mes, x='mês', y='temperatura_media', color='bairro', stack=False, x_label='Mês', y_label='Temperatura média')

# st.title('Humidade média por mês de cada bairro')

# bairros_selecionados_humidade_mes = []
# for bairro in df_humidade_por_bairro_e_mes['bairro'].unique():
#     if st.checkbox(bairro, value=True, key=f'hum_mes_{bairro}'):
#         bairros_selecionados_humidade_mes.append(bairro)

# df_filtrado_humidade_mes = df_humidade_por_bairro_e_mes[df_humidade_por_bairro_e_mes['bairro'].isin(bairros_selecionados_humidade_mes)]
# st.bar_chart(df_filtrado_humidade_mes, x='mês', y='humidade_media', color='bairro', stack=False, x_label='Mês', y_label='Humidade média')
